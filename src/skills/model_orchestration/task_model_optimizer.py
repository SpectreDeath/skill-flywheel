import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class TaskModelOptimizer:
    def __init__(self):
        self.task_profiles = {}

    def add_task_profile(
        self, task_type: str, recommended_model: str, min_capability: int
    ):
        self.task_profiles[task_type] = {
            "recommended_model": recommended_model,
            "min_capability": min_capability,
        }

    def optimize(self, task_type: str, available_models: List[Dict]) -> Optional[Dict]:
        if task_type not in self.task_profiles:
            return available_models[0] if available_models else None

        profile = self.task_profiles[task_type]
        candidates = [
            m
            for m in available_models
            if m.get("capability", 0) >= profile["min_capability"]
        ]

        if not candidates:
            return available_models[0] if available_models else None
        return min(candidates, key=lambda m: m.get("cost", 1))


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "optimize")

    try:
        if action == "optimize":
            task_type = payload.get("task_type", "reasoning")
            optimizer = TaskModelOptimizer()
            optimizer.add_task_profile("reasoning", "gpt-4", 8)
            optimizer.add_task_profile("coding", "claude-3", 7)
            optimizer.add_task_profile("creative", "llama-3", 6)

            available = [
                {"model_id": "gpt-4", "capability": 9, "cost": 0.03},
                {"model_id": "claude-3", "capability": 8, "cost": 0.015},
                {"model_id": "llama-3", "capability": 6, "cost": 0.001},
            ]

            result = optimizer.optimize(task_type, available)
            return {
                "result": {"optimized_model": result},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "add_profile":
            task_type = payload.get("task_type")
            recommended_model = payload.get("recommended_model")
            min_capability = payload.get("min_capability", 5)
            optimizer = TaskModelOptimizer()
            optimizer.add_task_profile(task_type, recommended_model, min_capability)
            return {"result": {"status": "added"}, "metadata": {"action": action}}

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action},
            }

    except Exception as e:
        logger.error("Error in task_model_optimizer: {}".format(e))
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
