import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def select_samples(
    data: List[Dict[str, Any]], strategy: str, n: int
) -> List[Dict[str, Any]]:
    if strategy == "random":
        import random

        return random.sample(data, min(n, len(data)))
    elif strategy == "uncertainty":
        return sorted(data, key=lambda x: x.get("uncertainty", 0), reverse=True)[:n]
    return data[:n]


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        data = payload.get("data", [])
        strategy = payload.get("strategy", "random")
        n = payload.get("n", 10)
        result = select_samples(data, strategy, n)
        return {
            "result": {"selected": result, "count": len(result)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
