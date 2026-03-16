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
        id="google_search",
        name="Google Search tool",
        description="Does google searches and returns the results",
        tags=["google search"],
        examples=["Find me search results on AI", "Find me the wikipedia article on Penang"],
    )

    # A2A Agent Card definition
    agent_card = AgentCard(
        name="Google Search Agent",
        description="Does google searches and returns the results",
        url=fqdn,
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    return to_a2a(root_agent, agent_card=agent_card)
