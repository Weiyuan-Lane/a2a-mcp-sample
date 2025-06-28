import os
import uvicorn
from starlette.applications import Starlette

from dotenv import load_dotenv
load_dotenv()

HOST=os.getenv('HOST', default='localhost')
PORT=int(os.getenv('PORT', default='8000'))

def start_web_server():
    # Add your non-agent routes here before we start the server
    all_routes = []

    # all_routes.extend(get_a2a_routes())
    # all_routes.extend(get_basic_interaction_routes())

    app = Starlette(routes=all_routes)
    uvicorn.run(app, host=HOST, port=PORT)

if __name__ == "__main__":
    start_web_server()
