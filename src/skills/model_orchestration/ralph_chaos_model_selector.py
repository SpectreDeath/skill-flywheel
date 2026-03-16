import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class RalphChaosModelSelector:
    def __init__(self):
        self.models = {}
        self.chaos_scenarios = [
            "latency_spike",
            "model_failure",
            "timeout",
            "rate_limit",
        ]

    def register_model(self, model_id: str, resilience_score: float):
        self.models[model_id] = {"resilience_score": resilience_score, "failures": 0}

    def select_for_chaos(self, scenario: str) -> Optional[str]:
        if scenario not in self.chaos_scenarios:
            return None

        candidates = [
            m for m, info in self.models.items() if info["resilience_score"] > 0.7
        ]
        if not candidates:
            return list(self.models.keys())[0] if self.models else None
        return max(candidates, key=lambda m: self.models[m]["resilience_score"])


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "select")

    try:
        if action == "select":
            scenario = payload.get("scenario", "latency_spike")
            selector = RalphChaosModelSelector()
            selector.register_model("gpt-4", resilience_score=0.8)
            selector.register_model("claude-3", resilience_score=0.9)
            selector.register_model("llama-3", resilience_score=0.6)

            selected = selector.select_for_chaos(scenario)
            return {
                "result": {"selected_model": selected, "scenario": scenario},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "register":
            model_id = payload.get("model_id")
            resilience_score = payload.get("resilience_score", 0.5)
            selector = RalphChaosModelSelector()
            selector.register_model(model_id, resilience_score)
            return {"result": {"status": "registered"}, "metadata": {"action": action}}

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action},
            }

    except Exception as e:
        logger.error("Error in ralph_chaos_model_selector: {}".format(e))
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
