import uvicorn
from src.server import agent_application

if __name__ == "__main__":
  config = uvicorn.Config(agent_application.build(), host="0.0.0.0", port=8080, log_level="info", reload_dirs=["/app/src"])
  server = uvicorn.Server(config)
  server.run()
