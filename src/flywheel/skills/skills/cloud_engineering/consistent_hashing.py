import hashlib
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ConsistentHashing:
    def __init__(self, num_replicas: int = 3):
        self.ring = {}
        self.sorted_keys = []
        self.num_replicas = num_replicas

    def add_node(self, node_id: str):
        for i in range(self.num_replicas):
            key = hashlib.md5(f"{node_id}_{i}".encode()).hexdigest()
            self.ring[key] = node_id
        self.sorted_keys = sorted(self.ring.keys())


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "hash")
    try:
        if action == "hash":
            ch = ConsistentHashing(3)
            ch.add_node("node1")
            ch.add_node("node2")
            return {
                "result": {"ring_size": len(ch.ring)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
