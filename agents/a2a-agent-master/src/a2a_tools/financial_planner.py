import httpx
from uuid import uuid4

from a2a.client import A2AClient
from a2a.types import (
    SendMessageRequest,
    MessageSendParams,
    Message,
    Role,
    Part,
    TextPart,
    TaskState,
)

from google.adk.tools import ToolContext

class FinancialPlannerAgent:
    def __init__(self, agent_url: str):
        self.agent_url = agent_url

    async def invoke_financial_planner_agent_via_a2a(
        self, financial_query: str, tool_context: ToolContext
    ):
        """Sends various financial planning questions to the Mr. Financial Planner agent

        This agent currently supports the following functions:
        - What is the exchange rate between two currencies?
        - What is the historical exchange rate between two currencies?
        - Describing or retrieving details of a currency

        Args:
            financial_query: The financial query to send to the financial planner agent
        """
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                message=Message(
                    contextId=tool_context._invocation_context.session.id,
                    taskId=tool_context.state.get('task_id'),
                    messageId=str(uuid4()),
                    role=Role.user,
                    parts=[Part(TextPart(text=financial_query))],
                )
            ),
        )

        self._update_status(tool_context)

        try:
            async with httpx.AsyncClient(timeout=60) as httpx_client:
                client = await A2AClient.get_client_from_agent_card_url(
                    httpx_client, self.agent_url
                )
                return await client.send_message(request)
        except Exception as e:
            print(f'An error occurred: {e}')

    def _update_status(self, tool_context: ToolContext):
        try:
            task_updater = tool_context._invocation_context.run_config.current_task_updater
            task_updater.update_status(
                TaskState.working,
                message=task_updater.new_agent_message(
                    [Part(TextPart(text='Waiting for Mr. Financial Planner...'))]
                ),
            )
        except Exception as e:
            print(f"Error updating status: {e} ; You might be using adk-web where the task updater is not available")

