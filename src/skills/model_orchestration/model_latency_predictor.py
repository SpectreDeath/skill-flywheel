import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class ModelLatencyPredictor:
    def __init__(self):
        self.historical_data = []

    def record_latency(
        self, model_id: str, input_tokens: int, output_tokens: int, latency_ms: float
    ):
        self.historical_data.append(
            {
                "model_id": model_id,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency_ms": latency_ms,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def predict(self, model_id: str, input_tokens: int, output_tokens: int) -> Dict:
        relevant = [d for d in self.historical_data if d["model_id"] == model_id]
        if not relevant:
            return {"predicted_latency_ms": 1000, "confidence": 0.5}

        total_tokens = input_tokens + output_tokens
        avg_per_token = sum(
            d["latency_ms"] / max(1, d["input_tokens"] + d["output_tokens"])
            for d in relevant
        ) / len(relevant)
        predicted = avg_per_token * total_tokens

        return {"predicted_latency_ms": predicted, "confidence": 0.8}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "predict")

    try:
        if action == "predict":
            model_id = payload.get("model_id", "gpt-4")
            input_tokens = payload.get("input_tokens", 100)
            output_tokens = payload.get("output_tokens", 50)

            predictor = ModelLatencyPredictor()
            result = predictor.predict(model_id, input_tokens, output_tokens)
            return {
                "result": result,
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "record":
            model_id = payload.get("model_id")
            input_tokens = payload.get("input_tokens")
            output_tokens = payload.get("output_tokens")
            latency_ms = payload.get("latency_ms")

            predictor = ModelLatencyPredictor()
            predictor.record_latency(model_id, input_tokens, output_tokens, latency_ms)
            return {"result": {"status": "recorded"}, "metadata": {"action": action}}

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action},
            }

    except Exception as e:
        logger.error("Error in model_latency_predictor: {}".format(e))
        return {"result": {"error": str(e)}, "metadata": {"action": action}}
