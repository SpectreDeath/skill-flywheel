import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class LangGraphACP:
    def __init__(self):
        self.agents = []

    def add_agent(self, name: str, role: str):
        self.agents.append({"name": name, "role": role})


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "run")
    try:
        if action == "run":
            graph = LangGraphACP()
            graph.add_agent("agent1", "coordinator")
            return {
                "result": {"agents": len(graph.agents)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
