from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH

def get_google_search_agent(agent_url: str):
    return RemoteA2aAgent(
        name="google_search_agent",
        description="A helpful assistant to help with performing Google searches and rendering the results.",
        agent_card=(
            f"{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}"
        ),
    )
