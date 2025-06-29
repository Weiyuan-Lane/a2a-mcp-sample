from google.adk.agents import RunConfig
from pydantic import ConfigDict
from a2a.server.tasks import TaskUpdater

class A2ARunConfig(RunConfig):
    """Custom override of ADK RunConfig to smuggle extra data through the event loop."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    current_task_updater: TaskUpdater
