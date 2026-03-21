import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def scan_repo(path: str) -> Dict[str, Any]:
    findings = []
    if "package.json" in path or "requirements.txt" in path:
        findings.append(
            {"type": "dependencies", "issue": "Check for vulnerable dependencies"}
        )
    if ".env" in path:
        findings.append(
            {"type": "secrets", "issue": "Environment files may contain secrets"}
        )
    if "docker-compose.yml" in path:
        findings.append(
            {"type": "infrastructure", "issue": "Review container security"}
        )
    return {"findings": findings, "status": "scanned", "path": path}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        action = payload.get("action", "scan")
        if action == "scan":
            path = payload.get("path", "")
            result = scan_repo(path)
        else:
            result = {"error": "Unknown action"}
        return {"result": result, "metadata": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        return {
            "result": {"error": str(e)},
            "metadata": {"timestamp": datetime.now().isoformat()},
        }
