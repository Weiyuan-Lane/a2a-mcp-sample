import os
import sys
# Add the current directory to Python path to find src module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.agents import LlmAgent
from src.a2a_tools.google_search import GoogleSearchAgent
from src.a2a_tools.hello_world_greeter import HelloWorldGreeterAgent
from src.a2a_tools.financial_planner import FinancialPlannerAgent
from src.a2a_tools.chart_maker import ChartMakerAgent

from dotenv import load_dotenv
load_dotenv()

PROMPT = """
    You are master of all agents. You are able to delegate tasks to the appropriate agents.
"""

google_search_agent = GoogleSearchAgent(agent_url=os.getenv("GOOGLE_SEARCH_AGENT_URL"))
hello_world_greeter_agent = HelloWorldGreeterAgent(agent_url=os.getenv("HELLO_WORLD_GREETER_AGENT_URL"))
financial_planner_agent = FinancialPlannerAgent(agent_url=os.getenv("FINANCIAL_PLANNER_AGENT_URL"))
chart_maker_agent = ChartMakerAgent(agent_url=os.getenv("CHART_MAKER_AGENT_URL"))

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='a2a_agent_master',
    description='A helpful assistant help delegate tasks to other agents',
    instruction=PROMPT,
    tools=[
        google_search_agent.invoke_google_search_agent_via_a2a,
        hello_world_greeter_agent.invoke_hello_world_greeter_agent_via_a2a,
        financial_planner_agent.invoke_financial_planner_agent_via_a2a,
        chart_maker_agent.invoke_chart_maker_agent_via_a2a,
    ],
)
