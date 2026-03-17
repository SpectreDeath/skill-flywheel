import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class Mem0UniversalMemoryLayerAgents:
    def __init__(self):
        self.layers = []

    def create_layer(self, name: str) -> Dict:
        layer = {"name": name, "created_at": datetime.utcnow().isoformat()}
        self.layers.append(layer)
        return layer


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            mem0 = Mem0UniversalMemoryLayerAgents()
            result = mem0.create_layer(payload.get("name", "layer"))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
