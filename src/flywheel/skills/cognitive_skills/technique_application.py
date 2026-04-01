"""
Technique Application Module

Apply proven methods and standard procedures to solve problems efficiently.
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass


TECHNIQUES = {
    "sorting": {
        "small_n": "insertion_sort",
        "large_n": "quick_sort",
        "stable": "merge_sort",
        "nearly_sorted": "insertion_sort",
    },
    "searching": {
        "sorted": "binary_search",
        "unsorted": "linear_search",
        "exact_key": "hash_lookup",
        "closest": "binary_search_tree",
    },
    "debugging": {
        "api_error": "check_logs_database_code_config",
        "performance": "profile_measure_optimize",
        "crash": "stack_trace_core_dump",
    },
}


@dataclass
class Technique:
    """Represents a technique."""

    name: str
    steps: List[str]
    applicable_scenarios: str = ""


class TechniqueApplicator:
    """
    Applies proven techniques.

    Framework:
    1. Identify Problem Type
    2. Select Technique
    3. Apply Faithfully
    4. Verify Result
    5. Adapt if Needed
    """

    def __init__(self):
        self.applied_techniques: List[Dict] = []

    def identify_problem_type(self, problem: str) -> str:
        """
        Identify the type of problem.

        Args:
            problem: Problem description

        Returns:
            Problem type
        """
        problem_lower = problem.lower()

        if any(word in problem_lower for word in ["sort", "order", "arrange"]):
            return "sorting"
        elif any(word in problem_lower for word in ["find", "search", "locate"]):
            return "searching"
        elif any(word in problem_lower for word in ["bug", "error", "fail", "crash"]):
            return "debugging"
        elif any(word in problem_lower for word in ["optimize", "performance", "slow"]):
            return "optimization"
        else:
            return "general"

    def select_technique(self, problem_type: str, constraints: Dict = None) -> str:
        """
        Select appropriate technique.

        Args:
            problem_type: Type of problem
            constraints: Constraints affecting selection

        Returns:
            Selected technique name
        """
        constraints = constraints or {}

        if problem_type in TECHNIQUES:
            base = TECHNIQUES[problem_type]

            if constraints.get("small_data"):
                return base.get("small_n", "custom")
            elif constraints.get("stable"):
                return base.get("stable", "custom")
            elif constraints.get("nearly_sorted"):
                return base.get("nearly_sorted", "custom")
            else:
                return base.get("large_n", base.get("unsorted", "custom"))

        return "custom_solution"

    def apply_technique(self, technique: str, problem_data: Any) -> Dict:
        """
        Apply a technique to problem data.

        Args:
            technique: Technique name
            problem_data: Data to process

        Returns:
            Application result
        """
        result = {
            "technique": technique,
            "applied": True,
            "steps_executed": self._get_default_steps(technique),
            "result": f"Applied {technique} to data",
        }

        self.applied_techniques.append(result)
        return result

    def _get_default_steps(self, technique: str) -> List[str]:
        """Get default steps for a technique."""
        steps_map = {
            "binary_search": ["Locate middle", "Compare", "Narrow range", "Repeat"],
            "quick_sort": ["Pick pivot", "Partition", "Recursively sort"],
            "merge_sort": ["Divide", "Recursively sort", "Merge"],
            "debugging": ["Identify error", "Check logs", "Examine code", "Fix"],
        }
        return steps_map.get(technique, ["Step 1", "Step 2", "Step 3"])

    def verify_result(self, result: Any, expected: Any) -> Dict:
        """Verify technique application result."""
        return {
            "result": result,
            "expected": expected,
            "verified": result == expected,
            "match": str(result) == str(expected)
            if not isinstance(result, type(expected))
            else result == expected,
        }

    def execute_procedure(self, procedure: Callable, inputs: Dict) -> Dict:
        """
        Execute a procedure with given inputs.

        Args:
            procedure: Procedure function
            inputs: Input parameters

        Returns:
            Execution result
        """
        try:
            result = procedure(**inputs)
            return {"success": True, "result": result, "error": None}
        except Exception as e:
            return {"success": False, "result": None, "error": str(e)}


def apply_technique(technique: str, data: Any) -> Dict:
    """Quick technique application."""
    applicator = TechniqueApplicator()
    return applicator.apply_technique(technique, data)


# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "apply_technique")
    timestamp = _dt.datetime.now().isoformat()
    kwargs = {k: v for k, v in payload.items() if k != "action"}

    instance = TechniqueApplicator()

    if action == "get_info":
        return {"result": {"name": "technique_application", "actions": ['apply_technique', 'execute_procedure', 'identify_problem_type', 'select_technique', 'verify_result'] }, "metadata": {"action": action, "timestamp": timestamp}}

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    result = method(**kwargs)
    if _inspect.isawaitable(result):
        result = await result
    return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
