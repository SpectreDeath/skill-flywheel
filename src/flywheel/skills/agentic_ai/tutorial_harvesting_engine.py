import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


class TutorialHarvestingEngine:
    def __init__(self):
        self.tutorials = []

    def harvest_tutorial(self, url: str) -> Dict:
        tutorial = {"url": url, "harvested_at": datetime.utcnow().isoformat()}
        self.tutorials.append(tutorial)
        return tutorial


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "harvest")
    try:
        if action == "harvest":
            engine = TutorialHarvestingEngine()
            result = engine.harvest_tutorial(payload.get("url", ""))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
