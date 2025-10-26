from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from agent import root_agent

def get_a2a_starlette_app(fqdn: str):
    # A2A Agent Skill definition
    skill = AgentSkill(
        id="a2a_agent_master",
        name="Task Delegation tool",
        description="A helpful assistant help delegate tasks to other agents",
        tags=["agent task delegation"],
        examples=[
            "Help me find the latest news on AI"
        ],
    )

    # A2A Agent Card definition
    agent_card = AgentCard(
        name="A2A Agent Master",
        description="An agent that is master of all agents",
        url=fqdn,
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    return to_a2a(root_agent, agent_card=agent_card)
