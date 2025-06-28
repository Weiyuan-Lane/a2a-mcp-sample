from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    AuthorizationCodeOAuthFlow,
    OAuth2SecurityScheme,
    OAuthFlows,
    SecurityScheme,
)
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

def routes_from(
        agent_card: AgentCard,
        agent_skills: list[AgentSkill],
        ):
    """
    Returns a list of routes for the agent A2A wrapper.
    """
    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor, task_store=InMemoryTaskStore()
    )

    a2a_app = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    return a2a_app.routes()

