import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class Test:
    def __init__(self):
        self.results = []

    def run(self, name: str) -> Dict:
        result = {"name": name, "passed": True, "ran_at": datetime.utcnow().isoformat()}
        self.results.append(result)
        return result


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "run")
    try:
        if action == "run":
            test = Test()
            result = test.run(payload.get("name", "test"))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
