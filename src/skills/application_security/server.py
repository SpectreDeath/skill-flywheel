import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def check_server_security(headers: Dict[str, str]) -> Dict[str, Any]:
    issues = []
    if headers.get("X-Powered-By"):
        issues.append({"type": "server_info_exposed", "severity": "low"})
    if headers.get("Server", "").startswith("Apache"):
        issues.append({"type": "server_version_exposed", "severity": "medium"})
    if headers.get("X-Content-Type-Options", "") != "nosniff":
        issues.append({"type": "missing_content_type_options", "severity": "medium"})
    if headers.get("Strict-Transport-Security", "") == "":
        issues.append({"type": "no_hsts", "severity": "high"})
    return {"issues": issues, "secure": len(issues) == 0}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "check")
    try:
        headers = payload.get("headers", {})
        result = check_server_security(headers)
        return {
            "result": result,
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
