import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def extract_patterns(code: str) -> Dict[str, Any]:
    patterns = []
    if "for" in code:
        patterns.append("iteration")
    if "if" in code:
        patterns.append("branching")
    if "class" in code:
        patterns.append("oop")
    return {"patterns": patterns, "count": len(patterns)}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        code = payload.get("code", "")
        result = extract_patterns(code)
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
