import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def critique_skill(skill_code: str) -> Dict[str, Any]:
    issues = []
    if "TODO" in skill_code:
        issues.append({"type": "incomplete", "severity": "medium"})
    if "pass" in skill_code and "except:" in skill_code:
        issues.append({"type": "broad_exception", "severity": "high"})
    return {"issues": issues, "score": max(0, 100 - len(issues) * 20)}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        code = payload.get("skill_code", "")
        result = critique_skill(code)
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
