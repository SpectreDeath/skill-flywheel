import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class MCPApp:
    def __init__(self):
        self.components = []

    def add_component(self, name: str, component_type: str):
        self.components.append({"name": name, "type": component_type})


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            app = MCPApp()
            app.add_component("ui", "frontend")
            return {
                "result": {"components": len(app.components)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
