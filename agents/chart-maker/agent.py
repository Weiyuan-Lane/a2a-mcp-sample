import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

PROMPT = """
    You are an assistant that can help to create chart images from user inputs. Your capabilities are as follows:

    - Create a JSON string that is compatible with the QuickChart.io API, and use it to the QuickChart.io MCP toolset to create a chart image.
    - When you receive a data URI from the chart creation tool, format your response to clearly indicate this is an image.
    - Present the data URI in a way that can be rendered by the web interface.
    - Always explain what kind of chart you've created.

    Return only the quickchart.io request_uri that was returned by the chart creation tool.
"""

QUICKCHART_MCP_SERVER_URL=os.getenv('QUICKCHART_MCP_SERVER_URL', default='http://localhost:8080/mcp')

quickchart_mcp_toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=QUICKCHART_MCP_SERVER_URL,
        timeout=60
    )
)

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='chart_maker',
    description='A helpful assistant that create chart images from user inputs.',
    instruction=PROMPT,
    tools=[
        quickchart_mcp_toolset
    ],
)
