import time
import logging
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def generate_test_cases(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    test_cases = []

    fields = spec.get("fields", [])

    happy_path = {
        "test_id": "test-happy-path-001",
        "name": "Happy Path Test",
        "type": "positive",
        "description": "Test with valid inputs",
        "inputs": {},
        "expected_result": "success",
    }
    for field in fields:
        if field.get("type") == "string":
            happy_path["inputs"][field["name"]] = "test_value"
        elif field.get("type") == "number":
            happy_path["inputs"][field["name"]] = 1
        elif field.get("type") == "boolean":
            happy_path["inputs"][field["name"]] = True
    test_cases.append(happy_path)

    edge_case = {
        "test_id": "test-edge-case-001",
        "name": "Edge Case Test",
        "type": "edge",
        "description": "Test boundary conditions",
        "inputs": {},
        "expected_result": "varies",
    }
    for field in fields:
        if field.get("type") == "string":
            edge_case["inputs"][field["name"]] = ""
        elif field.get("type") == "number":
            edge_case["inputs"][field["name"]] = 0
    test_cases.append(edge_case)

    null_case = {
        "test_id": "test-null-001",
        "name": "Null Input Test",
        "type": "negative",
        "description": "Test with null/empty inputs",
        "inputs": {},
        "expected_result": "error",
    }
    test_cases.append(null_case)

    invalid_case = {
        "test_id": "test-invalid-001",
        "name": "Invalid Input Test",
        "type": "negative",
        "description": "Test with invalid inputs",
        "inputs": {},
        "expected_result": "error",
    }
    for field in fields:
        if field.get("type") == "number":
            invalid_case["inputs"][field["name"]] = "invalid"
    test_cases.append(invalid_case)

    return test_cases


def execute_spec_test(
    test_case: Dict[str, Any], spec: Dict[str, Any]
) -> Dict[str, Any]:
    test_type = test_case.get("type", "positive")
    inputs = test_case.get("inputs", {})

    result = {
        "test_id": test_case.get("test_id"),
        "status": "passed",
        "execution_time_ms": 0,
        "output": None,
        "errors": [],
    }

    execution_start = time.time()

    required_fields = [f["name"] for f in spec.get("fields", []) if f.get("required")]
    for field in required_fields:
        if field not in inputs or inputs[field] in ["", None]:
            result["status"] = "failed"
            err_msg = "Missing required field: {}".format(field)
            result["errors"].append(err_msg)

    for field_name, value in inputs.items():
        field_spec = next(
            (f for f in spec.get("fields", []) if f["name"] == field_name), None
        )
        if not field_spec:
            continue

        expected_type = field_spec.get("type")

        if expected_type == "number" and isinstance(value, str):
            try:
                float(value)
            except:
                result["status"] = "failed"
                err_msg = "Invalid type for field {}: expected {}".format(
                    field_name, expected_type
                )
                result["errors"].append(err_msg)

        if expected_type == "string" and isinstance(value, str):
            if value == "" and field_spec.get("required"):
                result["status"] = "failed"
                err_msg = "Empty string for required field {}".format(field_name)
                result["errors"].append(err_msg)

    result["execution_time_ms"] = round((time.time() - execution_start) * 1000, 2)

    if test_type == "negative" and result["status"] == "failed":
        result["status"] = "passed"
        result["errors"] = []

    return result


def generate_test_report(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "passed")
    failed = sum(1 for r in results if r.get("status") == "failed")

    pass_rate = (passed / total * 100) if total > 0 else 0

    avg_time = (
        sum(r.get("execution_time_ms", 0) for r in results) / total if total > 0 else 0
    )

    return {
        "summary": {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(pass_rate, 2),
            "average_execution_time_ms": round(avg_time, 2),
        },
        "results": results,
    }


def validate_spec_executable(spec: Dict[str, Any]) -> Dict[str, Any]:
    issues = []

    if not spec.get("name"):
        issues.append({"type": "error", "message": "Specification name is required"})

    if not spec.get("version"):
        issues.append(
            {"type": "warning", "message": "Specification version not provided"}
        )

    fields = spec.get("fields", [])
    if not fields:
        issues.append(
            {"type": "warning", "message": "No fields defined in specification"}
        )

    for field in fields:
        if "name" not in field:
            issues.append({"type": "error", "message": "Field missing name attribute"})
        if "type" not in field:
            field_name = field.get("name", "unknown")
            msg = "Field '{}' missing type attribute".format(field_name)
            issues.append({"type": "error", "message": msg})

    is_executable = len([i for i in issues if i["type"] == "error"]) == 0

    return {
        "executable": is_executable,
        "issues": issues,
        "validation_score": 100
        - len([i for i in issues if i["type"] == "error"]) * 20
        - len([i for i in issues if i["type"] == "warning"]) * 5,
    }


def create_test_harness(spec: Dict[str, Any]) -> Dict[str, Any]:
    harness_id = "harness-{}".format(
        hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    )
    harness = {
        "harness_id": harness_id,
        "spec_name": spec.get("name", "Unknown"),
        "spec_version": spec.get("version", "1.0.0"),
        "created_at": datetime.now().isoformat(),
        "test_cases": [],
        "execution_mode": "sequential",
        "reporting": {"format": "json", "verbosity": "standard"},
    }

    harness["test_cases"] = generate_test_cases(spec)

    return harness


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "harness")

    try:
        if action == "harness":
            spec = payload.get("spec", {})
            harness = create_test_harness(spec)

            return {
                "result": harness,
                "metadata": {
                    "action": "harness",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "generate_tests":
            spec = payload.get("spec", {})
            test_cases = generate_test_cases(spec)
            return {
                "result": {"test_cases": test_cases},
                "metadata": {
                    "action": "generate_tests",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "execute":
            test_case = payload.get("test_case", {})
            spec = payload.get("spec", {})
            result = execute_spec_test(test_case, spec)
            return {
                "result": result,
                "metadata": {
                    "action": "execute",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "execute_all":
            test_cases = payload.get("test_cases", [])
            spec = payload.get("spec", {})
            results = [execute_spec_test(tc, spec) for tc in test_cases]
            report = generate_test_report(results)
            return {
                "result": report,
                "metadata": {
                    "action": "execute_all",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "validate":
            spec = payload.get("spec", {})
            result = validate_spec_executable(spec)
            return {
                "result": result,
                "metadata": {
                    "action": "validate",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "create_harness":
            spec = payload.get("spec", {})
            harness = create_test_harness(spec)
            return {
                "result": harness,
                "metadata": {
                    "action": "create_harness",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": "Unknown action: {}".format(action)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error("Error in executable_spec_harness: {}".format(e))
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
