import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class MCPTutorialServer:
    def __init__(self):
        self.endpoints = []

    def add_endpoint(self, path: str, handler):
        self.endpoints.append({"path": path, "handler": handler})


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "start")
    try:
        if action == "start":
            server = MCPTutorialServer()
            server.add_endpoint("/tutorial", None)
            return {
                "result": {"endpoints": len(server.endpoints)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
