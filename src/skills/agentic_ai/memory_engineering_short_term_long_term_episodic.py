import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class MemoryEngineeringShortTermLongTermEpisodic:
    def __init__(self):
        self.memories = {"short_term": [], "long_term": [], "episodic": []}

    def store(self, memory_type: str, content: str) -> Dict:
        memory = {
            "type": memory_type,
            "content": content,
            "stored_at": datetime.utcnow().isoformat(),
        }
        if memory_type in self.memories:
            self.memories[memory_type].append(memory)
        return memory


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "store")
    try:
        if action == "store":
            engine = MemoryEngineeringShortTermLongTermEpisodic()
            result = engine.store(
                payload.get("memory_type", "short_term"), payload.get("content", "")
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
