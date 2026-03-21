import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def scan_for_vulnerabilities(
    code: str, language: str = "python"
) -> List[Dict[str, Any]]:
    vulnerabilities = []

    dangerous_patterns = [
        {
            "pattern": "eval(",
            "severity": "critical",
            "issue": "Use of eval() - code injection risk",
        },
        {
            "pattern": "exec(",
            "severity": "critical",
            "issue": "Use of exec() - code injection risk",
        },
        {
            "pattern": "pickle.loads",
            "severity": "high",
            "issue": "Pickle deserialization vulnerability",
        },
        {
            "pattern": "subprocess.call",
            "severity": "high",
            "issue": "Shell command injection risk",
        },
        {
            "pattern": "os.system",
            "severity": "high",
            "issue": "Shell command injection risk",
        },
        {
            "pattern": "password =",
            "severity": "high",
            "issue": "Hardcoded password detected",
        },
        {
            "pattern": "api_key =",
            "severity": "critical",
            "issue": "Hardcoded API key detected",
        },
        {
            "pattern": "secret =",
            "severity": "high",
            "issue": "Hardcoded secret detected",
        },
        {
            "pattern": "sql = ",
            "severity": "critical",
            "issue": "SQL injection risk - use parameterized queries",
        },
        {
            "pattern": ".format(",
            "severity": "medium",
            "issue": "String format - potential injection",
        },
    ]

    for item in dangerous_patterns:
        if item["pattern"] in code:
            vulnerabilities.append(
                {
                    "type": item["issue"],
                    "severity": item["severity"],
                    "pattern": item["pattern"],
                    "recommendation": "Refactor to avoid security risk",
                }
            )

    return vulnerabilities


def check_owasp_compliance(code: str) -> Dict[str, Any]:
    issues = []

    owasp_checks = [
        {"id": "A01", "name": "Broken Access Control", "pattern": "if user.is_admin"},
        {"id": "A02", "name": "Cryptographic Failures", "pattern": "md5("},
        {"id": "A03", "name": "Injection", "pattern": "cursor.execute"},
        {"id": "A04", "name": "Insecure Design", "pattern": "random("},
        {"id": "A05", "name": "Security Misconfiguration", "pattern": "debug=True"},
        {"id": "A06", "name": "Vulnerable Components", "pattern": "import"},
    ]

    for check in owasp_checks:
        if check["pattern"].lower() in code.lower():
            issues.append({"category": check["id"], "name": check["name"]})

    return {"owasp_categories_found": issues, "compliant": len(issues) >= 3}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "scan")

    try:
        if action == "scan":
            code = payload.get("code", "")
            language = payload.get("language", "python")
            vulnerabilities = scan_for_vulnerabilities(code, language)

            return {
                "result": {"vulnerabilities": vulnerabilities},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        elif action == "owasp":
            code = payload.get("code", "")
            result = check_owasp_compliance(code)
            return {
                "result": result,
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in security_scan: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
