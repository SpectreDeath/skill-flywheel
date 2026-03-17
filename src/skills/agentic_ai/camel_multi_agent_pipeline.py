import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class CamelMultiAgentPipeline:
    def __init__(self):
        self.pipelines = []

    def create_pipeline(self, name: str, agents: List[str]) -> Dict:
        pipeline = {
            "name": name,
            "agents": agents,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.pipelines.append(pipeline)
        return pipeline


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            pipeline = CamelMultiAgentPipeline()
            result = pipeline.create_pipeline(
                payload.get("name", "pipeline"), payload.get("agents", [])
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
