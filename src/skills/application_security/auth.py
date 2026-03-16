import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def check_auth_patterns(code: str) -> List[Dict[str, Any]]:
    issues = []
    if "password" in code.lower() and "=" in code and '"' in code:
        issues.append({"type": "hardcoded_password", "severity": "high"})
    if "jwt" in code.lower() and "verify" not in code.lower():
        issues.append({"type": "jwt_not_verified", "severity": "high"})
    if "session" in code.lower() and "secure" not in code.lower():
        issues.append({"type": "insecure_session", "severity": "medium"})
    return issues


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "analyze")
    try:
        if action == "analyze":
            code = payload.get("code", "")
            issues = check_auth_patterns(code)
            return {
                "result": {"issues": issues},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }
        return {
            "result": {"error": "Unknown action"},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
