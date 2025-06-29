import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

from dotenv import load_dotenv
load_dotenv()

PROMPT = """
    You are an assistant that can help with financial planning. Your capabilities are as follows:

    - Get exchange rate data given some currency input
"""

EXCHANGE_RATE_MCP_SERVER_URL=os.getenv('EXCHANGE_RATE_MCP_SERVER_URL', default='http://localhost:8080/mcp')

exchange_rate_mcp_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=EXCHANGE_RATE_MCP_SERVER_URL,
        timeout=60
    )
)

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='financial_planner',
    description='A helpful assistant that helps with financial planning.',
    instruction=PROMPT,
    tools=[
        exchange_rate_mcp_toolset
    ],
)
