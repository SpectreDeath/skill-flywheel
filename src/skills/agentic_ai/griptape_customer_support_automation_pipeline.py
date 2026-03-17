import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class GriptapeCustomerSupportAutomationPipeline:
    def __init__(self):
        self.pipelines = []

    def create_pipeline(self, name: str, steps: List[str]) -> Dict:
        pipeline = {
            "name": name,
            "steps": steps,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.pipelines.append(pipeline)
        return pipeline


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            pipe = GriptapeCustomerSupportAutomationPipeline()
            result = pipe.create_pipeline(
                payload.get("name", "pipeline"), payload.get("steps", [])
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
