from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH

def get_financial_planner_agent(agent_url: str):
    return RemoteA2aAgent(
        name="financial_planner_agent",
        description="A helpful assistant that helps with financial planning.",
        agent_card=(
            f"{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}"
        ),
    )
