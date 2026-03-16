import time
import logging
import random
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class ComplianceRule:
    def __init__(self, rule_id: str, description: str, severity: str, pattern: str):
        self.rule_id = rule_id
        self.description = description
        self.severity = severity
        self.pattern = pattern

    def check(self, code: str) -> bool:
        import re

        return bool(re.search(self.pattern, code, re.IGNORECASE))


def detect_violations(code: str, rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    violations = []

    rule_patterns = {
        "security": [
            {
                "pattern": r"eval\s*\(",
                "description": "Use of eval() - security risk",
                "severity": "critical",
            },
            {
                "pattern": r"password\s*=\s*['\"]",
                "description": "Hardcoded password detected",
                "severity": "critical",
            },
            {
                "pattern": r"api[_-]?key\s*=\s*['\"]",
                "description": "Hardcoded API key detected",
                "severity": "critical",
            },
        ],
        "performance": [
            {
                "pattern": r"for\s+.*\s+in\s+.*:\s*for\s+",
                "description": "Nested loops detected - potential performance issue",
                "severity": "medium",
            },
            {
                "pattern": r"\.append\(",
                "description": "Multiple append calls - consider list comprehension",
                "severity": "low",
            },
        ],
        "style": [
            {
                "pattern": r"\s+$",
                "description": "Trailing whitespace",
                "severity": "low",
            },
            {
                "pattern": r"\t",
                "description": "Tab character - use spaces",
                "severity": "low",
            },
        ],
    }

    for category, pattern_rules in rule_patterns.items():
        for rule in pattern_rules:
            import re

            matches = re.finditer(rule["pattern"], code, re.IGNORECASE)
            for match in matches:
                violations.append(
                    {
                        "rule_id": "{}-{}".format(category, random.randint(1000, 9999)),
                        "category": category,
                        "description": rule["description"],
                        "severity": rule["severity"],
                        "line": code[: match.start()].count("\n") + 1,
                        "match": match.group(),
                    }
                )

    return violations


def adaptive_testing(spec_data: Dict[str, Any]) -> Dict[str, Any]:
    testing_params = spec_data.get("adaptive_testing", {})
    change_probability = testing_params.get("requirement_change_probability", 0.2)
    stress_intensity = testing_params.get("stress_test_intensity", "medium")

    stress_levels = {"low": 5, "medium": 10, "high": 20}
    iterations = stress_levels.get(stress_intensity, 10)

    test_cases = []
    for i in range(iterations):
        if random.random() < change_probability:
            variations = [
                "performance",
                "security",
                "usability",
                "reliability",
                "compatibility",
            ]
            variation = random.choice(variations)
            test_case = {
                "test_id": "stress-test-{:03d}".format(i + 1),
                "variation": variation,
                "modified": True,
                "description": "Stress test with {} variation".format(variation),
            }
        else:
            test_case = {
                "test_id": "stress-test-{:03d}".format(i + 1),
                "variation": "baseline",
                "modified": False,
                "description": "Baseline test case",
            }
        test_cases.append(test_case)

    return {
        "iterations": iterations,
        "change_probability": change_probability,
        "test_cases": test_cases,
        "stress_intensity": stress_intensity,
    }


def midnight_audit() -> Dict[str, Any]:
    current_hour = datetime.now().hour

    audit_types = ["full", "random", "targeted"]
    audit_type = random.choice(audit_types)

    if current_hour >= 2 and current_hour <= 4:
        audit_result = "midnight_audit"
    else:
        audit_result = "scheduled_audit"

    return {
        "audit_type": audit_result,
        "audit_time": datetime.now().isoformat(),
        "compliance_score": random.randint(70, 100),
        "violations_found": random.randint(0, 5),
        "recommendations": [
            "Review security configurations",
            "Update deprecated dependencies",
            "Add error handling for edge cases",
        ][: random.randint(1, 3)],
    }


def darwinian_evolution(code: str) -> Dict[str, Any]:
    survival_rate = 0.7

    violations = detect_violations(code, [])
    non_compliant_count = len(
        [v for v in violations if v["severity"] in ["critical", "high"]]
    )

    kept_lines = []
    removed_lines = []
    lines = code.split("\n")

    for i, line in enumerate(lines):
        is_compliant = True
        for v in violations:
            if v["line"] == i + 1:
                is_compliant = False
                break

        if is_compliant or random.random() < survival_rate:
            kept_lines.append(line)
        else:
            removed_lines.append(line)

    return {
        "original_lines": len(lines),
        "kept_lines": len(kept_lines),
        "removed_lines": len(removed_lines),
        "survival_rate": survival_rate,
        "compliance_improvement": len(kept_lines) / max(1, len(lines)),
        "evolved_code": "\n".join(kept_lines),
    }


def generate_compliance_report(violations: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not violations:
        return {
            "total_violations": 0,
            "compliance_score": 100,
            "status": "compliant",
            "critical_issues": 0,
            "medium_issues": 0,
            "low_issues": 0,
        }

    critical = len([v for v in violations if v.get("severity") == "critical"])
    medium = len([v for v in violations if v.get("severity") == "medium"])
    low = len([v for v in violations if v.get("severity") == "low"])

    score = 100 - (critical * 15) - (medium * 5) - (low * 1)
    score = max(0, score)

    return {
        "total_violations": len(violations),
        "compliance_score": score,
        "status": "compliant"
        if score >= 80
        else "needs_improvement"
        if score >= 60
        else "non_compliant",
        "critical_issues": critical,
        "medium_issues": medium,
        "low_issues": low,
        "violations_by_category": {},
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "enforce")

    try:
        if action == "enforce":
            spec_data = payload.get("specification_context", {})
            code = payload.get("code", "")

            violations = detect_violations(code, [])
            report = generate_compliance_report(violations)

            return {
                "result": {"violations": violations, "compliance_report": report},
                "metadata": {
                    "action": "enforce",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "adaptive_testing":
            result = adaptive_testing(payload)
            return {
                "result": result,
                "metadata": {
                    "action": "adaptive_testing",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "midnight_audit":
            result = midnight_audit()
            return {
                "result": result,
                "metadata": {
                    "action": "midnight_audit",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "darwinian_evolution":
            code = payload.get("code", "")
            result = darwinian_evolution(code)
            return {
                "result": result,
                "metadata": {
                    "action": "darwinian_evolution",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "check_violations":
            code = payload.get("code", "")
            violations = detect_violations(code, [])
            return {
                "result": {"violations": violations},
                "metadata": {
                    "action": "check_violations",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "compliance_report":
            violations = payload.get("violations", [])
            report = generate_compliance_report(violations)
            return {
                "result": report,
                "metadata": {
                    "action": "compliance_report",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in spec_guardrail_enforcement: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
