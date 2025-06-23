from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from . import prompt

from dotenv import load_dotenv
load_dotenv()

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='google_search',
    description='A helpful assistant to help with performing Google searches and rendering the results.',
    instruction=prompt.PROMPT,
    tools=[google_search],
)
