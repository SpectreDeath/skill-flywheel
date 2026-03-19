import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def run_benchmark(model_input: str, attack_type: str = "fgsm") -> Dict[str, Any]:
    attacks = {
        "fgsm": "Fast Gradient Sign Method",
        "cw": "Carlini-Wagner",
        "pgd": "Projected Gradient Descent",
    }
    return {
        "attack_type": attacks.get(attack_type, "unknown"),
        "input": model_input[:50],
        "adversarial_modified": True,
        "robustness_score": 0.75,
    }


def measure_robustness(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(results)
    if total == 0:
        return {"robustness": 0, "sample_size": 0}
    successful = sum(1 for r in results if r.get("adversarial_modified"))
    return {
        "robustness_score": 1 - (successful / total),
        "sample_size": total,
        "status": "measured",
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        action = payload.get("action", "benchmark")
        if action == "benchmark":
            model_input = payload.get("model_input", "")
            attack = payload.get("attack_type", "fgsm")
            result = run_benchmark(model_input, attack)
        elif action == "measure":
            results = payload.get("results", [])
            result = measure_robustness(results)
        else:
            result = {"error": "Unknown action"}
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
