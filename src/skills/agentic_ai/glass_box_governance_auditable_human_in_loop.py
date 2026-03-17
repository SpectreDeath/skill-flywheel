import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class GlassBoxGovernanceAuditableHumanInLoop:
    def __init__(self):
        self.audits = []

    def create_audit(self, action: str, user: str) -> Dict:
        audit = {
            "action": action,
            "user": user,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.audits.append(audit)
        return audit


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "audit")
    try:
        if action == "audit":
            governance = GlassBoxGovernanceAuditableHumanInLoop()
            result = governance.create_audit(
                payload.get("action", "action"), payload.get("user", "system")
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
