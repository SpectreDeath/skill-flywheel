import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


class MultiAgentIncidentResponseHaystack:
    def __init__(self):
        self.incidents = []

    def respond_to_incident(self, incident_id: str, severity: str) -> Dict:
        response = {
            "incident_id": incident_id,
            "severity": severity,
            "responded_at": datetime.utcnow().isoformat(),
        }
        self.incidents.append(response)
        return response


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "respond")
    try:
        if action == "respond":
            system = MultiAgentIncidentResponseHaystack()
            result = system.respond_to_incident(
                payload.get("incident_id", ""), payload.get("severity", "low")
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
