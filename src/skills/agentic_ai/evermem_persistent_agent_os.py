import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class EvermemPersistentAgentOs:
    def __init__(self):
        self.agents = []

    def create_agent(self, name: str) -> Dict:
        agent = {"name": name, "created_at": datetime.utcnow().isoformat()}
        self.agents.append(agent)
        return agent


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "create")
    try:
        if action == "create":
            os = EvermemPersistentAgentOs()
            result = os.create_agent(payload.get("name", "agent"))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
