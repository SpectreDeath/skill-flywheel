import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class RagPipelineBuilder:
    def __init__(self):
        self.pipelines = []

    def build_pipeline(self, name: str, components: List[str]) -> Dict:
        pipeline = {
            "name": name,
            "components": components,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.pipelines.append(pipeline)
        return pipeline


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "build")
    try:
        if action == "build":
            builder = RagPipelineBuilder()
            result = builder.build_pipeline(
                payload.get("name", "pipeline"), payload.get("components", [])
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
