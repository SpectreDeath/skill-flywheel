import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class PydanticAiContractFirstAgenticDecision:
    def __init__(self):
        self.contracts = []

    def create_contract(self, name: str, schema: Dict) -> Dict:
        contract = {
            "name": name,
            "schema": schema,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.contracts.append(contract)
        return contract


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            system = PydanticAiContractFirstAgenticDecision()
            result = system.create_contract(
                payload.get("name", "contract"), payload.get("schema", {})
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
