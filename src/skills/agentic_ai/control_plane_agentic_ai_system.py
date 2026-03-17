import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ControlPlaneAgenticAiSystem:
    def __init__(self):
        self.controls = []

    def add_control(self, name: str, policy: str) -> Dict:
        control = {
            "name": name,
            "policy": policy,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.controls.append(control)
        return control


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "add")
    try:
        if action == "add":
            system = ControlPlaneAgenticAiSystem()
            result = system.add_control(
                payload.get("name", "control"), payload.get("policy", "")
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
