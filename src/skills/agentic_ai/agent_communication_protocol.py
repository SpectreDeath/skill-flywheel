import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class AgentCommunicationProtocol:
    def __init__(self):
        self.messages = []

    def send_message(self, from_agent: str, to_agent: str, message: str) -> Dict:
        msg = {
            "from": from_agent,
            "to": to_agent,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }
        self.messages.append(msg)
        return msg


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "send")
    try:
        if action == "send":
            protocol = AgentCommunicationProtocol()
            msg = protocol.send_message("agent1", "agent2", "hello")
            return {"result": {"message": msg}, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
