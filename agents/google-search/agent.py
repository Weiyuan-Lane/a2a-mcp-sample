from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from dotenv import load_dotenv
load_dotenv()

PROMPT = """
  You are a helpful assistant that can search the web for information. When you receive a query, you will perform a web search and return the most relevant results.
"""

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='google_search',
    description='A helpful assistant to help with performing Google searches and rendering the results.',
    instruction=PROMPT,
    tools=[google_search],
)
