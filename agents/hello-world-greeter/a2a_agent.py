from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from agent import root_agent

def get_a2a_starlette_app(fqdn: str):
    # A2A Agent Skill definition
    skill_with_name = AgentSkill(
        id="first_message_greeting_with_user_name",
        name="First greeting with name tool",
        description="A helpful assistant to greet the users interacting with it with their name",
        tags=["first message greeting with user's name"],
        examples=["Hi there, my name is John", "I'm Wayne, great to meet you"],
    )
    skill_without_name = AgentSkill(
        id="first_message_greeting_without_name",
        name="First greeting without name tool",
        description="A helpful assistant to greet the users interacting with it without their name",
        tags=["first message greeting without user's name"],
        examples=["Hi there", "Greetings", "Meow"],
    )

    # A2A Agent Card definition
    agent_card = AgentCard(
        name="Hello World Greeter",
        description="A greeter agent that says nice things on the first message from the user",
        url=fqdn,
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            skill_with_name,
            skill_without_name,
        ],
    )

    return to_a2a(root_agent, agent_card=agent_card)
