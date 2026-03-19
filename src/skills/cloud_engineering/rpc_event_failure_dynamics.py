import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class DistributedFailureDynamics:
    def __init__(self):
        self.rpc_failures = []
        self.event_failures = []

    def simulate_rpc_failure(self, node_id: str):
        self.rpc_failures.append({"type": "rpc", "node": node_id, "recovered": False})

    def simulate_event_failure(self, node_id: str):
        self.event_failures.append(
            {"type": "event", "node": node_id, "recovered": False}
        )


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "simulate")
    try:
        if action == "simulate":
            sim = DistributedFailureDynamics()
            sim.simulate_rpc_failure("node1")
            sim.simulate_event_failure("node2")
            return {
                "result": {
                    "rpc_failures": len(sim.rpc_failures),
                    "event_failures": len(sim.event_failures),
                },
                "metadata": {"action": action},
            }
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
