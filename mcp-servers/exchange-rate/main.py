import asyncio
import httpx
import os
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from dotenv import load_dotenv
load_dotenv()

HOST=os.getenv('HOST', default='localhost')
PORT=int(os.getenv('PORT', default='8000'))

mcp = FastMCP("Currency MCP Server")
CURRENCY_API_HOST = 'https://api.frankfurter.app' # IF this doesn't work, try https://api.frankfurter.dev/v1

@mcp.custom_route("/health", methods=["GET"])
async def liveness_check(request: Request) -> JSONResponse:
    """Liveness probe endpoint for health checks"""
    return JSONResponse({})

@mcp.tool()
def get_currency_data(
    currency: str,
):
    """Use this to get current data of a currency.

    Args:
        currency: The target currency to get data for (e.g., "USD").

    Returns:
        A dict for the currency data
    """

    try:
        currency_upper = currency.upper()

        r = httpx.get(
            f"{CURRENCY_API_HOST}/latest",
            params = {
                'base': currency_upper,
            },
        )
        data = r.json()

        if 'message' in data:
            return { 'error': f"API request failed with error: {data['message']}" }

        return data

    except httpx.HTTPError as e:
        return { 'error': f"API request failed with error: {e}" }
    except ValueError:
        return { 'error': f"API request failed with invalid response body as: {data}"}
    except Exception as e:
        return { 'error': f"API request failed with error: {e}" }

@mcp.tool()
def convert_from_one_currency_to_another_currency(
    from_currency: str,
    to_currency: str,
    amount: float = 1.0,
):
    """Use this to calculate exchange_rate from one currency to another currency.

    Args:
        from_currency: The original currency to convert from (e.g., "USD").
        to_currency: The new currency to convert to (e.g., "EUR").
        amount: The amount of the original currency to convert. Default to 1.0 if not provided.

    Returns:
        A dict for the exchange rate outcome
    """

    try:
        from_currency_upper = from_currency.upper()
        to_currency_upper = to_currency.upper()

        r = httpx.get(
            f"{CURRENCY_API_HOST}/latest",
            params = {
                'from': from_currency_upper,
                'to': to_currency_upper,
            },
        )
        data = r.json()

        if 'message' in data:
            return { 'error': f"API request failed with error: {data['message']}" }
        if 'rates' not in data or to_currency_upper not in data['rates']:
            return { 'error': f"API request failed with missing exchange rate data for: {from_currency_upper} --> {to_currency_upper}" }

        exchange_rate = data['rates'][to_currency_upper]
        converted_amount = exchange_rate * amount

        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "exchange_rate": exchange_rate,
            "converted_amount": converted_amount
        }

    except httpx.HTTPError as e:
        return { 'error': f"API request failed with error: {e}" }
    except ValueError:
        return { 'error': f"API request failed with invalid response body as: {data}"}
    except Exception as e:
        return { 'error': f"API request failed with error: {e}" }

@mcp.tool()
def exchange_rate_time_series_data(
    from_currency: str,
    to_currency: str,
    start_date: str,
    end_date: str,
):
    """Use this to obtain time series (or historical) data from one currency to another currency, across two givendates.

    Args:
        from_currency: The original currency to convert from (e.g., "USD").
        to_currency: The new currency to convert to (e.g., "EUR").
        start_date: The start date for the time series in YYYY-MM-DD format (e.g., "2024-01-01").
        end_date: The end date for the time series in YYYY-MM-DD format (e.g., "2024-01-01").

    Returns:
        A dict for time series data on the exchange rate between the two currencies
    """

    try:
        from_currency_upper = from_currency.upper()
        to_currency_upper = to_currency.upper()

        print(f"DEBUG Data: {from_currency_upper} --> {to_currency_upper} --> {start_date} --> {end_date}")

        r = httpx.get(
            f"{CURRENCY_API_HOST}/{start_date}..{end_date}",
            params = {
                'base': from_currency_upper,
                'symbols': to_currency_upper,
            },
        )
        data = r.json()

        if 'message' in data:
            return { 'error': f"API request failed with error: {data['message']}" }
        if 'rates' not in data:
            return { 'error': f"API request failed with missing time series data" }

        exchange_rate_time_series = data['rates']
        exchange_rates = {}

        for date, rate in exchange_rate_time_series.items():
            exchange_rates[date] = rate[to_currency_upper]

        return {
            "from_currency": from_currency_upper,
            "to_currency": to_currency_upper,
            "exchange_rates": exchange_rates,
        }
    except httpx.HTTPError as e:
        print(f"DEBUG Data: ERROR 1 {e}")
        return { 'error': f"API request failed with error: {e}" }
    except ValueError:
        print(f"DEBUG Data: ERROR 2 {data}")
        return { 'error': f"API request failed with invalid response body as: {data}"}
    except Exception as e:
        print(f"DEBUG Data: ERROR 3 {e}")
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

