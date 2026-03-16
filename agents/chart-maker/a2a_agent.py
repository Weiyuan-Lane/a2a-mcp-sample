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
        id="chart_maker",
        name="Chart Maker skill",
        description="Makes charts using the QuickChart.io",
        tags=["create chart", "make chart"],
        examples=["Can you make me a line chart? I'd like it to show monthly data from January to May. Please include two datasets: one for 'Dogs' with values 50, 60, 70, 180, 190 (blue line, no fill) and another for 'Cats' with values 100, 200, 300, 400, 500 (green line, no fill)."],
    )

    # A2A Agent Card definition
    agent_card = AgentCard(
        name="Chart Maker Agent",
        description="A agent that wraps around the QuickChart.io API powered MCP server to make charts",
        url=fqdn,
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text", "image"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

    return to_a2a(root_agent, agent_card=agent_card)
