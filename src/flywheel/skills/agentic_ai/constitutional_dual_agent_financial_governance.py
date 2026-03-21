import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ConstitutionalDualAgentFinancialGovernance:
    def __init__(self):
        self.governances = []

    def govern(self, agent_id: str, rules: List[str]) -> Dict:
        governance = {
            "agent_id": agent_id,
            "rules": rules,
            "governed_at": datetime.utcnow().isoformat(),
        }
        self.governances.append(governance)
        return governance


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "govern")
    try:
        if action == "govern":
            system = ConstitutionalDualAgentFinancialGovernance()
            result = system.govern(
                payload.get("agent_id", ""), payload.get("rules", [])
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
