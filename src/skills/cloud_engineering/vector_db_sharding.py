import hashlib
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class VectorDBSharding:
    def __init__(self, num_shards: int):
        self.num_shards = num_shards
        self.shards = {i: [] for i in range(num_shards)}

    def shard_key(self, vector_id: str) -> int:
        return int(hashlib.md5(vector_id.encode()).hexdigest(), 16) % self.num_shards

    def add_vector(self, vector_id: str, embedding: List[float]):
        shard = self.shard_key(vector_id)
        self.shards[shard].append({"id": vector_id, "embedding": embedding})
        return shard


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "shard")
    try:
        if action == "shard":
            db = VectorDBSharding(4)
            shard = db.add_vector("vec1", [0.1, 0.2, 0.3])
            return {
                "result": {"shard": shard, "total_shards": 4},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
