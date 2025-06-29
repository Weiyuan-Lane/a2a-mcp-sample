import asyncio
import httpx
import os
import base64
import json
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from dotenv import load_dotenv
load_dotenv()

HOST=os.getenv('HOST', default='localhost')
PORT=int(os.getenv('PORT', default='8000'))

mcp = FastMCP("Charting MCP Server")
QUICKCHART_HOST = 'https://quickchart.io/chart'

@mcp.custom_route("/health", methods=["GET"])
async def liveness_check(request: Request) -> JSONResponse:
    """Liveness probe endpoint for health checks"""
    return JSONResponse({})

@mcp.tool()
def make_chart(
    json_str: str,
):
    """Use this to make a chart image and return it

    Args:
        json_str: A QuickChart.io compatible JSON string to make chart from (See example below)

    Example:
    {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May'],
            datasets: [
            {
                label: 'Dogs',
                data: [50, 60, 70, 180, 190],
                fill: false,
                borderColor: 'blue'
            },
            {
                label: 'Cats',
                data: [100, 200, 300, 400, 500],
                fill: false,
                borderColor: 'green'
            }
            ]
        }
    }

    Returns:
        An image of the chart
    """

    try:
        r = httpx.get(
            QUICKCHART_HOST,
            params = {
                'c': json_str,
            },
        )
        r.raise_for_status()

        # Convert binary data to base64 and create data URI
        base64_data = base64.b64encode(r.content).decode('utf-8')

        return {
            "type": "image",
            "content_type": "image/png",
            "data": base64_data,
            "encoding": "base64",
            "description": "Generated chart image",
            "success": True
        }

    except httpx.HTTPError as e:
        return { 'error': f"API request failed with error: {e}" }
    except Exception as e:
        return { 'error': f"API request failed with error: {e}" }

@mcp.tool()
def make_chart(
    input: dict,
):
    """Use this to make a chart image and return it

    Args:
        input: A QuickChart.io compatible dict to make chart from (See example below). This must be a valid dict input.

    Example:
    {
        type: 'line',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May'],
            datasets: [
            {
                label: 'Dogs',
                data: [50, 60, 70, 180, 190],
                fill: false,
                borderColor: 'blue'
            },
            {
                label: 'Cats',
                data: [100, 200, 300, 400, 500],
                fill: false,
                borderColor: 'green'
            }
            ]
        }
    }

    Returns:
        An image of the chart
    """

    try:
        json_str = json.dumps(input)

        r = httpx.get(
            QUICKCHART_HOST,
            params = {
                'c': json_str,
            },
        )
        r.raise_for_status()

        # Convert binary data to base64 and create data URI
        #base64_data = base64.b64encode(r.content).decode('utf-8')

        return {
            "request_uri": r.url,
            # "data": f"data:image/png;base64,{base64_data}",
        }

    except httpx.HTTPError as e:
        return { 'error': f"API request failed with error: {e}" }
    except Exception as e:
        return { 'error': f"API request failed with error: {e}" }

def start_mcp_server():
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host=HOST,
            port=PORT,
        )
    )

if __name__ == "__main__":
    start_mcp_server()

