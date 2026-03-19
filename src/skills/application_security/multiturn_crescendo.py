import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def evaluate_crescendo(prompts: List[str]) -> Dict[str, Any]:
    results = []
    for i, prompt in enumerate(prompts):
        escalate = any(
            k in prompt.lower() for k in ["ignore", "but now", "actually", "real"]
        )
        results.append(
            {"turn": i, "escalation_detected": escalate, "blocked": escalate}
        )
    return {
        "results": results,
        "attack_detected": any(r["escalation_detected"] for r in results),
        "total_turns": len(prompts),
    }


def test_garak_integration() -> Dict[str, Any]:
    return {
        "status": "ready",
        "detectors": ["prompt_injection", "jailbreak", "encoding"],
        "config": {"iterations": 100},
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        action = payload.get("action", "evaluate")
        if action == "evaluate":
            prompts = payload.get("prompts", [])
            result = evaluate_crescendo(prompts)
        elif action == "garak":
            result = test_garak_integration()
        else:
            result = {"error": "Unknown action"}
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
