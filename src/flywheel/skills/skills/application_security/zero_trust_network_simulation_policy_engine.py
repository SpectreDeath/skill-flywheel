import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def analyze_zero_trust(architecture: Dict[str, Any]) -> Dict[str, Any]:
    issues = []
    if not architecture.get("identity_provider"):
        issues.append(
            {"component": "identity", "issue": "No identity provider configured"}
        )
    if not architecture.get("mfa_enabled"):
        issues.append({"component": "authentication", "issue": "MFA not enabled"})
    if not architecture.get("encryption_at_rest"):
        issues.append({"component": "data", "issue": "Data not encrypted at rest"})
    return {
        "issues": issues,
        "compliant": len(issues) == 0,
        "score": 100 - len(issues) * 30,
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        architecture = payload.get("architecture", {})
        result = analyze_zero_trust(architecture)
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
