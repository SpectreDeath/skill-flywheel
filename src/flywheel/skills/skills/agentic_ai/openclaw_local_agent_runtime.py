import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


class OpenclawLocalAgentRuntime:
    def __init__(self):
        self.runtimes = []

    def create_runtime(self, name: str) -> Dict:
        runtime = {"name": name, "created_at": datetime.utcnow().isoformat()}
        self.runtimes.append(runtime)
        return runtime


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            runtime = OpenclawLocalAgentRuntime()
            result = runtime.create_runtime(payload.get("name", "runtime"))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
