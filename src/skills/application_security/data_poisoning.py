import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def detect_label_flipping(dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
    flipped = []
    for i, sample in enumerate(dataset):
        if "label" in sample and "original_label" in sample:
            if sample["label"] != sample["original_label"]:
                flipped.append(
                    {
                        "index": i,
                        "flipped_from": sample["original_label"],
                        "flipped_to": sample["label"],
                    }
                )
    return {
        "flipped_samples": flipped,
        "count": len(flipped),
        "suspicious": len(flipped) > len(dataset) * 0.05,
    }


def simulate_attack(
    dataset: List[Dict[str, Any]], target_label: str, poison_rate: float
) -> Dict[str, Any]:
    poison_count = int(len(dataset) * poison_rate)
    return {
        "poisoned_count": poison_count,
        "target_label": target_label,
        "method": "label_flipping",
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        action = payload.get("action", "detect")
        if action == "detect":
            dataset = payload.get("dataset", [])
            result = detect_label_flipping(dataset)
        elif action == "simulate":
            dataset = payload.get("dataset", [])
            target = payload.get("target_label", "malicious")
            rate = payload.get("poison_rate", 0.1)
            result = simulate_attack(dataset, target, rate)
        else:
            result = {"error": "Unknown action"}
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
