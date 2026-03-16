import os
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from a2a_agent import get_a2a_starlette_app

from dotenv import load_dotenv
load_dotenv()

HOST=os.getenv('HOST', default='localhost')
WELL_KNOWN_HOST=os.getenv('WELL_KNOWN_HOST', default='localhost')
PORT=int(os.getenv('PORT', default='8000'))

async def liveness_check(request: Request) -> JSONResponse:
    """Liveness probe endpoint for health checks"""
    return JSONResponse({})

def start_web_server():
    a2a_app = get_a2a_starlette_app(f"http://{WELL_KNOWN_HOST}:{PORT}/")

    # Add your non-agent routes here before we start the server
    a2a_app.add_route("/health", liveness_check, methods=["GET"])

    uvicorn.run(a2a_app, host=HOST, port=PORT)

if __name__ == "__main__":
    start_web_server()
