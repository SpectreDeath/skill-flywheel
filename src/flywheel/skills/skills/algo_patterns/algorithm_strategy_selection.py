import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def select_algorithm(
    problem_type: str, input_size: int, constraints: Dict[str, Any]
) -> Dict[str, Any]:
    algos = {
        "search": {"small": "linear", "large": "binary"},
        "sort": {"small": "insertion", "medium": "merge", "large": "quick"},
        "graph": {"dense": "floyd-warshall", "sparse": "dijkstra"},
        "string": {"exact": "kmp", "approx": "bloom"},
    }
    size = "small" if input_size < 100 else "medium" if input_size < 10000 else "large"
    selected = algos.get(problem_type, {}).get(size, "default")
    return {
        "problem_type": problem_type,
        "input_size": input_size,
        "recommended_algorithm": selected,
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        problem_type = payload.get("problem_type", "search")
        input_size = payload.get("input_size", 100)
        constraints = payload.get("constraints", {})
        result = select_algorithm(problem_type, input_size, constraints)
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
