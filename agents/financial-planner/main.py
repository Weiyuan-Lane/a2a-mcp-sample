import os
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from a2a_agent import get_a2a_routes

from dotenv import load_dotenv
load_dotenv()

HOST=os.getenv('HOST', default='localhost')
WELL_KNOWN_HOST=os.getenv('WELL_KNOWN_HOST', default='localhost')
PORT=int(os.getenv('PORT', default='8000'))

async def liveness_check(request: Request) -> JSONResponse:
    """Liveness probe endpoint for health checks"""
    return JSONResponse({})

def start_web_server():
    # Add your non-agent routes here before we start the server
    all_routes = [
        Route("/health", liveness_check, methods=["GET"]),
    ]

    all_routes.extend(get_a2a_routes(f"http://{WELL_KNOWN_HOST}:{PORT}/"))

    app = Starlette(routes=all_routes)
    uvicorn.run(app, host=HOST, port=PORT)

if __name__ == "__main__":
    start_web_server()
