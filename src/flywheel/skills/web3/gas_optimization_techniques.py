import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def analyze_contract_gas(contract_code: str) -> Dict[str, Any]:
    analysis = {
        "total_functions": 0,
        "high_gas_functions": [],
        "optimization_suggestions": [],
        "estimated_total_gas": 0,
    }

    lines = contract_code.split("\n")

    storage_ops = 0
    loops = 0
    external_calls = 0

    for line in lines:
        line_lower = line.lower()

        if "function" in line_lower:
            analysis["total_functions"] += 1

        if any(kw in line_lower for kw in ["sstore", "storage"]):
            storage_ops += 1

        if any(kw in line_lower for kw in ["for", "while", "do"]):
            loops += 1

        if any(kw in line_lower for kw in ["call", "delegatecall", "staticcall"]):
            external_calls += 1

    if storage_ops > 5:
        analysis["optimization_suggestions"].append(
            "Reduce storage operations - consider using memory for temporary data"
        )

    if loops > 3:
        analysis["optimization_suggestions"].append(
            "Optimize loops - consider caching array lengths"
        )

    if external_calls > 2:
        analysis["optimization_suggestions"].append(
            "Minimize external calls - batch operations when possible"
        )

    analysis["estimated_total_gas"] = (
        21000 + (storage_ops * 5000) + (loops * 1000) + (external_calls * 3000)
    )

    return analysis


def suggest_gas_optimizations(contract_code: str) -> List[Dict[str, Any]]:
    suggestions = []

    if "uint256" in contract_code:
        suggestions.append(
            {
                "type": "type_optimization",
                "description": "Use uint256 for gas efficiency on EVM",
                "impact": "medium",
            }
        )

    if "for (uint i = 0" in contract_code:
        suggestions.append(
            {
                "type": "loop_optimization",
                "description": "Cache array length outside loop",
                "impact": "high",
            }
        )

    if "msg.sender" in contract_code and contract_code.count("msg.sender") > 3:
        suggestions.append(
            {
                "type": "caching",
                "description": "Cache msg.sender in local variable",
                "impact": "medium",
            }
        )

    if "require(" in contract_code:
        suggestions.append(
            {
                "type": "error_handling",
                "description": "Use custom errors instead of require with strings to save gas",
                "impact": "high",
            }
        )

    if "memory" not in contract_code and "calldata" not in contract_code:
        suggestions.append(
            {
                "type": "data_location",
                "description": "Use calldata for function parameters when possible",
                "impact": "medium",
            }
        )

    if not suggestions:
        suggestions.append(
            {
                "type": "none",
                "description": "No obvious gas optimizations found",
                "impact": "low",
            }
        )

    return suggestions


def calculate_function_gas(function_code: str) -> Dict[str, Any]:
    base_gas = 21000

    storage_read = function_code.lower().count("sload")
    storage_write = function_code.lower().count("sstore")

    gas = base_gas
    gas += storage_read * 2100
    gas += storage_write * 2900

    if "loop" in function_code.lower() or "for" in function_code.lower():
        gas += 1000

    if "call" in function_code.lower() or "delegatecall" in function_code.lower():
        gas += 9000

    return {
        "estimated_gas": gas,
        "storage_reads": storage_read,
        "storage_writes": storage_write,
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "optimize")

    try:
        if action == "optimize":
            contract_code = payload.get("contract_code", "")
            analysis = analyze_contract_gas(contract_code)
            suggestions = suggest_gas_optimizations(contract_code)

            return {
                "result": {"analysis": analysis, "suggestions": suggestions},
                "metadata": {
                    "action": "optimize",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "analyze":
            contract_code = payload.get("contract_code", "")
            result = analyze_contract_gas(contract_code)
            return {
                "result": result,
                "metadata": {
                    "action": "analyze",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "suggest":
            contract_code = payload.get("contract_code", "")
            result = suggest_gas_optimizations(contract_code)
            return {
                "result": {"suggestions": result},
                "metadata": {
                    "action": "suggest",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "calculate":
            function_code = payload.get("function_code", "")
            result = calculate_function_gas(function_code)
            return {
                "result": result,
                "metadata": {
                    "action": "calculate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in gas_optimization_techniques: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
