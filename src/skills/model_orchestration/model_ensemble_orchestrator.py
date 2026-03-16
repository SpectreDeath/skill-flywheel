import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class ModelEnsembleOrchestrator:
    def __init__(self):
        self.models = []

    def add_model(self, model_id: str, weight: float = 1.0):
        self.models.append({"model_id": model_id, "weight": weight})

    def dispatch(self, prompt: str) -> List[Dict]:
        responses = []
        for model in self.models:
            responses.append(
                {
                    "model_id": model["model_id"],
                    "response": "Response from {}".format(model["model_id"]),
                    "weight": model["weight"],
                }
            )
        return responses

    def vote(self, responses: List[Dict]) -> Dict:
        vote_counts = {}
        for r in responses:
            response = r.get("response", "")
            vote_counts[response] = vote_counts.get(response, 0) + r.get("weight", 1)

        winner = max(vote_counts.items(), key=lambda x: x[1])
        total = sum(vote_counts.values())
        confidence = winner[1] / total if total > 0 else 0

        return {
            "result": winner[0],
            "vote_counts": vote_counts,
            "confidence": confidence,
        }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "ensemble")

    try:
        if action == "ensemble":
            prompt = payload.get("prompt", "")
            orchestrator = ModelEnsembleOrchestrator()
            orchestrator.add_model("gpt-4", weight=1.5)
            orchestrator.add_model("claude-3", weight=1.5)
            orchestrator.add_model("llama-3", weight=1.0)

            responses = orchestrator.dispatch(prompt)
            result = orchestrator.vote(responses)
            return {
                "result": result,
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "add_model":
            model_id = payload.get("model_id")
            weight = payload.get("weight", 1.0)
            orchestrator = ModelEnsembleOrchestrator()
            orchestrator.add_model(model_id, weight)
            return {"result": {"status": "added"}, "metadata": {"action": action}}

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action},
            }

    except Exception as e:
        logger.error("Error in model_ensemble_orchestrator: {}".format(e))
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
