import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class AnemoiSemiCentralizedPeerCriticLoop:
    def __init__(self):
        self.loops = []

    def create_loop(self, name: str) -> Dict:
        loop = {"name": name, "created_at": datetime.utcnow().isoformat()}
        self.loops.append(loop)
        return loop


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            loop = AnemoiSemiCentralizedPeerCriticLoop()
            result = loop.create_loop(payload.get("name", "loop"))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
