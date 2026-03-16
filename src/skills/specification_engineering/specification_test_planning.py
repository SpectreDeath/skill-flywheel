import time
import logging
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def generate_test_plan(spec: Dict[str, Any]) -> Dict[str, Any]:
    plan = {
        "plan_id": "test-plan-{}".format(
            hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        ),
        "title": spec.get("title", "Test Plan"),
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
    }

    plan["scope"] = {
        "in_scope": ["Unit tests", "Integration tests", "System tests"],
        "out_of_scope": ["Performance testing", "Security testing"],
    }

    test_types = ["unit", "integration", "system", "acceptance"]
    plan["test_types"] = []

    for test_type in test_types:
        plan["test_types"].append(
            {
                "type": test_type,
                "description": "{} tests".format(test_type.title()),
                "coverage": "70%",
                "tools": ["pytest", "unittest"]
                if test_type == "unit"
                else ["Postman", "Selenium"],
            }
        )

    test_scenarios = []
    requirements = spec.get("requirements", [])
    for i, req in enumerate(requirements):
        test_scenarios.append(
            {
                "id": "TS-{:03d}".format(i + 1),
                "requirement": req,
                "test_cases": [
                    {
                        "id": "TC-{:03d}".format(i * 2 + 1),
                        "description": "Verify {}".format(req),
                        "priority": "High",
                    },
                    {
                        "id": "TC-{:03d}".format(i * 2 + 2),
                        "description": "Verify edge case for {}".format(req),
                        "priority": "Medium",
                    },
                ],
            }
        )

    if not test_scenarios:
        test_scenarios.append(
            {
                "id": "TS-001",
                "requirement": "Core functionality",
                "test_cases": [
                    {
                        "id": "TC-001",
                        "description": "Verify basic functionality",
                        "priority": "High",
                    },
                    {
                        "id": "TC-002",
                        "description": "Verify error handling",
                        "priority": "Medium",
                    },
                ],
            }
        )

    plan["test_scenarios"] = test_scenarios

    plan["test_environment"] = {
        "development": {"url": "dev.example.com", "database": "dev_db"},
        "staging": {"url": "staging.example.com", "database": "staging_db"},
        "production": {"url": "example.com", "database": "prod_db"},
    }

    plan["schedule"] = {
        "unit_testing": {"start": "Week 1", "duration": "2 weeks"},
        "integration_testing": {"start": "Week 2", "duration": "2 weeks"},
        "system_testing": {"start": "Week 3", "duration": "1 week"},
        "user_acceptance_testing": {"start": "Week 4", "duration": "1 week"},
    }

    plan["resources"] = {
        "testers": 2,
        "automation_engineers": 1,
        "tools": ["Selenium", "Postman", "Jenkins", "Jira"],
    }

    plan["entry_criteria"] = [
        "Test environment is ready",
        "Test data is prepared",
        "Test cases are reviewed",
    ]

    plan["exit_criteria"] = [
        "All critical test cases pass",
        "Test coverage exceeds 80%",
        "No high-priority defects open",
    ]

    return plan


def calculate_test_coverage(
    plan: Dict[str, Any], requirements: List[str]
) -> Dict[str, Any]:
    total_requirements = len(requirements)

    scenarios = plan.get("test_scenarios", [])
    covered_requirements = len(scenarios)

    coverage = (
        (covered_requirements / total_requirements * 100)
        if total_requirements > 0
        else 0
    )

    return {
        "total_requirements": total_requirements,
        "covered_requirements": covered_requirements,
        "coverage_percentage": round(coverage, 2),
        "gaps": requirements[covered_requirements:]
        if covered_requirements < total_requirements
        else [],
    }


def estimate_test_effort(plan: Dict[str, Any]) -> Dict[str, Any]:
    scenarios = len(plan.get("test_scenarios", []))

    test_cases = sum(
        len(s.get("test_cases", [])) for s in plan.get("test_scenarios", [])
    )

    hours_per_test_case = 2
    total_hours = test_cases * hours_per_test_case

    buffer = total_hours * 0.2

    return {
        "total_test_cases": test_cases,
        "estimated_hours": round(total_hours, 2),
        "buffer_hours": round(buffer, 2),
        "total_with_buffer": round(total_hours + buffer, 2),
    }


def validate_test_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    issues = []

    if not plan.get("title"):
        issues.append({"type": "error", "message": "Test plan title is required"})

    if not plan.get("test_scenarios"):
        issues.append(
            {"type": "error", "message": "At least one test scenario is required"}
        )

    if not plan.get("schedule"):
        issues.append({"type": "warning", "message": "Test schedule not defined"})

    if not plan.get("resources"):
        issues.append({"type": "warning", "message": "Resources not specified"})

    return {
        "valid": len([i for i in issues if i["type"] == "error"]) == 0,
        "issues": issues,
        "score": 100 - len([i for i in issues if i["type"] == "error"]) * 20,
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "plan")

    try:
        if action == "plan":
            spec = payload.get("spec", {})
            plan = generate_test_plan(spec)

            return {
                "result": plan,
                "metadata": {"action": "plan", "timestamp": datetime.now().isoformat()},
            }

        elif action == "generate":
            spec = payload.get("spec", {})
            plan = generate_test_plan(spec)
            return {
                "result": plan,
                "metadata": {
                    "action": "generate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "coverage":
            plan = payload.get("plan", {})
            requirements = payload.get("requirements", [])
            result = calculate_test_coverage(plan, requirements)
            return {
                "result": result,
                "metadata": {
                    "action": "coverage",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "estimate":
            plan = payload.get("plan", {})
            result = estimate_test_effort(plan)
            return {
                "result": result,
                "metadata": {
                    "action": "estimate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "validate":
            plan = payload.get("plan", {})
            result = validate_test_plan(plan)
            return {
                "result": result,
                "metadata": {
                    "action": "validate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in specification_test_planning: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
