import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class HueyAsyncTasks:
    def __init__(self):
        self.tasks = []

    def create_task(self, task_name: str, queue: str = "default"):
        task = {"name": task_name, "queue": queue, "status": "pending"}
        self.tasks.append(task)
        return task


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "task")
    try:
        if action == "task":
            huey = HueyAsyncTasks()
            task = huey.create_task("process_data", "high_priority")
            return {"result": {"task": task}, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
