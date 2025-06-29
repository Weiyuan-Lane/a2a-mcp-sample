from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    AgentCard,
    FilePart,
    FileWithBytes,
    FileWithUri,
    Part,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils.errors import ServerError
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.apps import A2AStarletteApplication
from a2a.server.tasks import InMemoryTaskStore

from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk import Runner

from google.genai import types
from agent import root_agent


def get_a2a_routes(fqdn: str):
    # A2A Agent Skill definition
    currency_retrieval_skill = AgentSkill(
        id="currency_retrieval",
        name="Currency retrieval tool",
        description="Retrieve the details of a currency",
        tags=["currency", "currency details"],
        examples=["Tell me about the USD"],
    )

    exchange_rate_retrieval_skill = AgentSkill(
        id="exchange_rate_retrieval",
        name="Exchange rate retrieval tool",
        description="Retrieve the exchange rate between two currencies",
        tags=["retrieve exchange rate", "calculate exchange rate"],
        examples=["Convert 100 USD to EUR", "Can you tell me the exchange rate of USD to EUR?"],
    )

    time_series_exchange_rate_retrieval_skill = AgentSkill(
        id="time_series_exchange_rate_retrieval",
        name="Time series exchange rate retrieval tool",
        description="Retrieve the historical exchange rate between two currencies, across multiple time periods",
        tags=["time series exchange rate", "time series exchange rate retrieval"],
        examples=["Tell me about the USD to EUR exchange rate from 2024-01-01 to 2025-01-01", "Retrieve the time series data from 12th December 2020 to 12th December 2021, for USD to EUR"],
    )

    # A2A Agent Card definition
    agent_card = AgentCard(
        name="Financial Planner Agent",
        description="Host a series of financial planning tools",
        url=fqdn,
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            currency_retrieval_skill,
            exchange_rate_retrieval_skill,
            time_series_exchange_rate_retrieval_skill,
        ],
    )

    # Create the ADK runner and executor.
    runner = Runner(
        app_name=agent_card.name,
        agent=root_agent,
        artifact_service=InMemoryArtifactService(),
        session_service=InMemorySessionService(),
        memory_service=InMemoryMemoryService(),
    )
    agent_executor = ADKAgentExecutor(runner, agent_card)

    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor, task_store=InMemoryTaskStore()
    )

    a2a_app = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    return a2a_app.routes()

class ADKAgentExecutor(AgentExecutor):
    """An AgentExecutor that runs an ADK-based Agent."""

    def __init__(self, runner: Runner, card: AgentCard):
        self.runner = runner
        self._card = card

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ):
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        if not context.current_task:
            await updater.submit()
        await updater.start_work()
        await self._process_request(
            types.UserContent(
                parts=convert_a2a_parts_to_genai(context.message.parts),
            ),
            context,
            updater,
        )

    async def cancel(self):
        # Ideally: kill any ongoing tasks.
        # Maybe not a good idea for production, but if we have reference to the task, we can cancel it.
        raise ServerError(error=UnsupportedOperationError())

    # Runner needs session id for your agent to work
    async def _upsert_session(self, context: RequestContext):
        """Upsert a session."""

        user_id = 'anonymous'
        if context.call_context and context.call_context.user.is_authenticated:
            user_id = context.call_context.user.username

        session = await self.runner.session_service.get_session(
            app_name=self.runner.app_name,
            user_id=user_id,
            session_id=context.context_id,
        ) or await self.runner.session_service.create_session(
            app_name=self.runner.app_name,
            user_id=user_id,
            session_id=context.context_id,
        )

        return session

    # Process the request of the agent.
    async def _process_request(
        self,
        new_message: types.UserContent,
        context: RequestContext,
        updater: TaskUpdater,
    ):
        """Process the request of the agent."""
        session = await self._upsert_session(context)

        async for event in self.runner.run_async(
            session_id=session.id,
            user_id=session.user_id,
            new_message=new_message,
        ):
            if event.is_final_response():
                parts = convert_genai_parts_to_a2a(event.content.parts)
                await updater.add_artifact(parts)
                await updater.complete()
                break
            if not event.get_function_calls():
                await updater.update_status(
                    TaskState.working,
                    message=updater.new_agent_message(
                        convert_genai_parts_to_a2a(event.content.parts),
                    ),
                )

def convert_a2a_parts_to_genai(parts: list[Part]) -> list[types.Part]:
    """Convert a list of A2A Part types into a list of Google Gen AI Part types."""
    return [convert_a2a_part_to_genai(part) for part in parts]

def convert_a2a_part_to_genai(part: Part) -> types.Part:
    """Convert a single A2A Part type into a Google Gen AI Part type."""
    part = part.root
    if isinstance(part, TextPart):
        return types.Part(text=part.text)
    if isinstance(part, FilePart):
        if isinstance(part.file, FileWithUri):
            return types.Part(
                file_data=types.FileData(
                    file_uri=part.file.uri, mime_type=part.file.mime_type
                )
            )
        if isinstance(part.file, FileWithBytes):
            return types.Part(
                inline_data=types.Blob(
                    data=part.file.bytes, mime_type=part.file.mime_type
                )
            )
        raise ValueError(f'Unsupported file type: {type(part.file)}')
    raise ValueError(f'Unsupported part type: {type(part)}')

def convert_genai_parts_to_a2a(parts: list[types.Part]) -> list[Part]:
    """Convert a list of Google Gen AI Part types into a list of A2A Part types."""
    return [
        convert_genai_part_to_a2a(part)
        for part in parts
        if (part.text or part.file_data or part.inline_data)
    ]

def convert_genai_part_to_a2a(part: types.Part) -> Part:
    """Convert a single Google Gen AI Part type into an A2A Part type."""
    if part.text:
        return TextPart(text=part.text)
    if part.file_data:
        return FilePart(
            file=FileWithUri(
                uri=part.file_data.file_uri,
                mime_type=part.file_data.mime_type,
            )
        )
    if part.inline_data:
        return Part(
            root=FilePart(
                file=FileWithBytes(
                    bytes=part.inline_data.data,
                    mime_type=part.inline_data.mime_type,
                )
            )
        )
    raise ValueError(f'Unsupported part type: {part}')
