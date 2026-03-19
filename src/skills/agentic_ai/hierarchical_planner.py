import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class HierarchicalPlanner:
    def __init__(self):
        self.plans = []

    def create_plan(self, goal: str, steps: List[str]) -> Dict:
        plan = {
            "goal": goal,
            "steps": steps,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.plans.append(plan)
        return plan


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "plan")
    try:
        if action == "plan":
            planner = HierarchicalPlanner()
            plan = planner.create_plan(
                payload.get("goal", "default"), payload.get("steps", [])
            )
            return {"result": {"plan": plan}, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
