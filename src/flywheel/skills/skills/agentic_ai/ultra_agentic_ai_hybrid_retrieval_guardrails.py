import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


class UltraAgenticAiHybridRetrievalGuardrails:
    def __init__(self):
        self.guardrails = []

    def add_guardrail(self, name: str, rule: str) -> Dict:
        guardrail = {
            "name": name,
            "rule": rule,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.guardrails.append(guardrail)
        return guardrail


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "add")
    try:
        if action == "add":
            system = UltraAgenticAiHybridRetrievalGuardrails()
            result = system.add_guardrail(
                payload.get("name", "guardrail"), payload.get("rule", "")
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
