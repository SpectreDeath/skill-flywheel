import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class StreamingDecisionAgentOnlineReplanning:
    def __init__(self):
        self.decisions = []

    def make_decision(self, context: Dict) -> Dict:
        decision = {"context": context, "decided_at": datetime.utcnow().isoformat()}
        self.decisions.append(decision)
        return decision


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "decide")
    try:
        if action == "decide":
            agent = StreamingDecisionAgentOnlineReplanning()
            result = agent.make_decision(payload.get("context", {}))
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
