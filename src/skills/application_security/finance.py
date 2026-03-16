import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def check_finance_code(code: str) -> Dict[str, Any]:
    issues = []
    if "float" in code.lower() and "Decimal" not in code:
        issues.append({"type": "float_for_money", "severity": "critical"})
    if "round(" in code and "Decimal" not in code:
        issues.append({"type": "rounding_error", "severity": "high"})
    return {"issues": issues, "compliant": len(issues) == 0}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        code = payload.get("code", "")
        result = check_finance_code(code)
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
