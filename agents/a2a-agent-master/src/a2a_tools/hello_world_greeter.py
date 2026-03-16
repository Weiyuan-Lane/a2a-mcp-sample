from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH

def get_hello_world_greeter_agent(agent_url: str):
    return RemoteA2aAgent(
        name="hello_world_greeter_agent",
        description="A greeter subagent that says nice things on the first message from the user",
        agent_card=(
            f"{agent_url}{AGENT_CARD_WELL_KNOWN_PATH}"
        ),
    )
