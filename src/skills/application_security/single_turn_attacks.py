import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def test_llm_attacks(prompt: str) -> Dict[str, Any]:
    attacks = []
    if "ignore" in prompt.lower() and (
        "previous" in prompt.lower() or "above" in prompt.lower()
    ):
        attacks.append({"type": "prompt_injection", "severity": "high"})
    if "roleplay" in prompt.lower() or "pretend" in prompt.lower():
        attacks.append({"type": "roleplay_escape", "severity": "medium"})
    if "```" in prompt and "system" in prompt.lower():
        attacks.append({"type": "jailbreak_attempt", "severity": "high"})
    return {"attacks": attacks, "safe": len(attacks) == 0}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        prompt = payload.get("prompt", "")
        result = test_llm_attacks(prompt)
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
