import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class PBFTByzantineSimulator:
    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.nodes = [{"id": i, "byzantine": False} for i in range(num_nodes)]

    def set_byzantine(self, node_id: int):
        if node_id < len(self.nodes):
            self.nodes[node_id]["byzantine"] = True


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "simulate")
    try:
        if action == "simulate":
            sim = PBFTByzantineSimulator(4)
            sim.set_byzantine(2)
            byzantine = [n for n in sim.nodes if n["byzantine"]]
            return {
                "result": {"total_nodes": 4, "byzantine_count": len(byzantine)},
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
