import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)


def analyze_smart_contract(contract_code: str) -> Dict[str, Any]:
    findings = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": [],
        "informational": [],
    }

    code_lower = contract_code.lower()

    if "tx.origin" in code_lower:
        findings["high"].append(
            "Use of tx.origin instead of msg.sender - vulnerability to phishing"
        )

    if "selfdestruct" in code_lower:
        findings["critical"].append("Selfdestruct found - contract can be destroyed")

    if "delegatecall" in code_lower:
        findings["high"].append("Delegatecall used - ensure library code is trusted")

    if "call.value" in code_lower and " payable" not in code_lower:
        findings["critical"].append(
            "Ether sending without receive function - potential loss of funds"
        )

    if "now" in code_lower:
        findings["low"].append(
            "Use of 'now' instead of block.timestamp - timestamp manipulation possible"
        )

    if "random" in code_lower:
        findings["high"].append(
            "Random number used on-chain - can be manipulated by miners"
        )

    if "assert(" in code_lower:
        findings["informational"].append(
            "Use require instead of assert for error handling"
        )

    if ".push(" in code_lower and "length" in code_lower:
        findings["medium"].append(
            "Potential array length manipulation - validate bounds"
        )

    return findings


def check_access_control(contract_code: str) -> Dict[str, Any]:
    checks = {
        "has_owner": False,
        "has_modifiers": False,
        "missing_modifiers": [],
        "recommendations": [],
    }

    if "owner" in contract_code.lower() or " Ownable" in contract_code:
        checks["has_owner"] = True

    if "modifier " in contract_code:
        checks["has_modifiers"] = True

    critical_functions = ["withdraw", "transferOwnership", "mint", "burn", "pause"]
    for func in critical_functions:
        if (
            func in contract_code.lower()
            and "modifier"
            not in contract_code[
                contract_code.lower().find(func) : contract_code.lower().find(func)
                + 100
            ].lower()
        ):
            checks["missing_modifiers"].append(func)

    if not checks["has_owner"]:
        checks["recommendations"].append(
            "Implement access control (OpenZeppelin Ownable)"
        )

    if checks["missing_modifiers"]:
        msg = "Add access modifiers to: {}".format(
            ", ".join(checks["missing_modifiers"])
        )
        checks["recommendations"].append(msg)

    return checks


def generate_audit_report(contract_code: str) -> Dict[str, Any]:
    findings = analyze_smart_contract(contract_code)
    access_control = check_access_control(contract_code)

    critical_count = len(findings["critical"])
    high_count = len(findings["high"])
    medium_count = len(findings["medium"])

    if critical_count > 0:
        severity = "CRITICAL"
    elif high_count > 2:
        severity = "HIGH"
    elif medium_count > 3:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "severity": severity,
        "total_findings": sum(len(v) for v in findings.values()),
        "findings": findings,
        "access_control": access_control,
        "recommendations": access_control["recommendations"],
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "audit")

    try:
        if action == "audit":
            contract_code = payload.get("contract_code", "")
            report = generate_audit_report(contract_code)

            return {
                "result": report,
                "metadata": {
                    "action": "audit",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "analyze":
            contract_code = payload.get("contract_code", "")
            result = analyze_smart_contract(contract_code)
            return {
                "result": result,
                "metadata": {
                    "action": "analyze",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "access_control":
            contract_code = payload.get("contract_code", "")
            result = check_access_control(contract_code)
            return {
                "result": result,
                "metadata": {
                    "action": "access_control",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in smart_contract_audit: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
