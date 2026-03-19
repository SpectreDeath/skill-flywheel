import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


class PersistentMemoryPersonalisedAgenticAi:
    def __init__(self):
        self.memories = []

    def store_memory(self, user_id: str, content: str) -> Dict:
        memory = {
            "user_id": user_id,
            "content": content,
            "stored_at": datetime.utcnow().isoformat(),
        }
        self.memories.append(memory)
        return memory


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "store")
    try:
        if action == "store":
            ai = PersistentMemoryPersonalisedAgenticAi()
            result = ai.store_memory(
                payload.get("user_id", ""), payload.get("content", "")
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
