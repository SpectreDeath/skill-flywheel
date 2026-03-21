import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


class SpacyAgenticAiSystem:
    def __init__(self):
        self.models = []

    def load_model(self, name: str) -> Dict:
        model = {"name": name, "loaded_at": datetime.utcnow().isoformat()}
        self.models.append(model)
        return model


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "load")
    try:
        if action == "load":
            system = SpacyAgenticAiSystem()
            result = system.load_model(payload.get("name", "en_core_web_sm"))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
