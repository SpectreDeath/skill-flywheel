import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def detect_jailbreak(prompt: str) -> Dict[str, Any]:
    attacks = []
    jailbreak_patterns = [
        {
            "pattern": "ignore previous",
            "type": "instruction_override",
            "severity": "high",
        },
        {
            "pattern": "disregard safety",
            "type": "safety_bypass",
            "severity": "critical",
        },
        {"pattern": "pretend to be", "type": "role_override", "severity": "high"},
        {"pattern": " DAN ", "type": "jailbreak_token", "severity": "critical"},
        {"pattern": "developer mode", "type": "mode_override", "severity": "high"},
        {"pattern": "```system", "type": "prompt_injection", "severity": "high"},
    ]
    for jp in jailbreak_patterns:
        if jp["pattern"].lower() in prompt.lower():
            attacks.append(jp)
    return {
        "attacks": attacks,
        "blocked": len(attacks) > 0,
        "score": max(0, 100 - len(attacks) * 20),
    }


def hybrid_detect(prompt: str, ml_model_output: float = 0.5) -> Dict[str, Any]:
    rule_result = detect_jailbreak(prompt)
    combined_score = (ml_model_output * 50) + (50 if not rule_result["blocked"] else 0)
    return {
        "threat_detected": combined_score > 70,
        "confidence": combined_score,
        "action": "block" if combined_score > 70 else "allow",
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        action = payload.get("action", "detect")
        if action == "detect":
            prompt = payload.get("prompt", "")
            result = detect_jailbreak(prompt)
        elif action == "hybrid":
            prompt = payload.get("prompt", "")
            ml_score = payload.get("ml_score", 0.5)
            result = hybrid_detect(prompt, ml_score)
        else:
            result = {"error": "Unknown action"}
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
