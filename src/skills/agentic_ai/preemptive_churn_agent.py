import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


class PreemptiveChurnAgent:
    def __init__(self):
        self.predictions = []

    def predict_churn(self, user_id: str, features: Dict) -> Dict:
        prediction = {
            "user_id": user_id,
            "features": features,
            "predicted_at": datetime.utcnow().isoformat(),
        }
        self.predictions.append(prediction)
        return prediction


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "predict")
    try:
        if action == "predict":
            agent = PreemptiveChurnAgent()
            result = agent.predict_churn(
                payload.get("user_id", ""), payload.get("features", {})
            )
            return {"result": result, "metadata": {"action": action}}
        return {"result": {"error": "Unknown action"}, "metadata": {"action": action}}
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
