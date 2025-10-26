from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH

def get_chart_maker_agent(agent_url: str):
    return RemoteA2aAgent(
        name="chart_maker_agent",
        description="A helpful assistant that create chart images from user inputs.",
        agent_card=(
            f"{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}"
        ),
    )
