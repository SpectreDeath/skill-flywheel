import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def analyze_complexity(code: str) -> Dict[str, Any]:
    loops = code.count("for") + code.count("while")
    recursion = code.count("def ") + code.count("async def")
    return {
        "time_complexity": "O(n^{})".format(loops),
        "space_complexity": "O({})".format(recursion),
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        code = payload.get("code", "")
        result = analyze_complexity(code)
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
