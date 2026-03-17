import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class GriptapeLocalAgenticStoryPipeline:
    def __init__(self):
        self.stories = []

    def create_story(self, prompt: str) -> Dict:
        story = {"prompt": prompt, "created_at": datetime.utcnow().isoformat()}
        self.stories.append(story)
        return story


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            pipeline = GriptapeLocalAgenticStoryPipeline()
            result = pipeline.create_story(payload.get("prompt", ""))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
