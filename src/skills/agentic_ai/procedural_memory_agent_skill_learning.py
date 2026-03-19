import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ProceduralMemoryAgentSkillLearning:
    def __init__(self):
        self.skills = []

    def learn_skill(self, name: str, procedure: List[str]) -> Dict:
        skill = {
            "name": name,
            "procedure": procedure,
            "learned_at": datetime.utcnow().isoformat(),
        }
        self.skills.append(skill)
        return skill


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "learn")
    try:
        if action == "learn":
            learner = ProceduralMemoryAgentSkillLearning()
            result = learner.learn_skill(
                payload.get("name", "skill"), payload.get("procedure", [])
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
