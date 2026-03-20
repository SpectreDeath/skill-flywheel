import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MCPAgentDemo:
    def __init__(self):
        self.demos = []

    def add_demo(self, name: str, steps: List[str]):
        self.demos.append({"name": name, "steps": steps})


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "demo")
    try:
        if action == "demo":
            demo = MCPAgentDemo()
            demo.add_demo("search", ["init", "query", "results"])
            return {
                "result": {"demos": len(demo.demos)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
