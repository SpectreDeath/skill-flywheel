import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class MCPAgent:
    def __init__(self):
        self.tools = []

    def register_tool(self, name: str, handler):
        self.tools.append({"name": name, "handler": handler})


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "run")
    try:
        if action == "run":
            agent = MCPAgent()
            agent.register_tool("search", lambda x: {"result": "search results"})
            return {
                "result": {"status": "agent_ran", "tools": len(agent.tools)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
