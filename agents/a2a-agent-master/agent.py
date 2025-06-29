import os
import sys
# Add the current directory to Python path to find src module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.agents import LlmAgent
from src.a2a_tools.google_search import GoogleSearchAgent

from dotenv import load_dotenv
load_dotenv()

PROMPT = """
    You are master of all agents. You are able to delegate tasks to the appropriate agents.
"""

google_search_agent = GoogleSearchAgent(agent_url=os.getenv("GOOGLE_SEARCH_AGENT_URL"))

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='a2a_agent_master',
    description='A helpful assistant help delegate tasks to other agents',
    instruction=PROMPT,
    tools=[
        google_search_agent.invoke_google_search_agent_via_a2a,
    ],
)
