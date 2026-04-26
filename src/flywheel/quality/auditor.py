#!/usr/bin/env python3
"""
Quality Auditor

Performs pre and post execution validation of skill outputs
against behavioral and functional criteria.
"""

import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AuditResult:
    passed: bool
    category: str
    score: float
    message: str = ""
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


class QualityAuditor:
    """Validates skill outputs against quality criteria."""

    def __init__(self):
        self.metrics = []

    def audit_pre_execution(
        self, skill_name: str, payload: Dict[str, Any], config: Dict[str, Any]
    ) -> Dict[str, AuditResult]:
        """Audit before execution."""
        results = {}

        # Check input validity
        results["input_validity"] = self._check_input_validity(payload)

        # Check if task is well-defined
        results["task_clarity"] = self._check_task_clarity(payload)

        return results

    def audit_post_execution(
        self,
        skill_name: str,
        result: Dict[str, Any],
        payload: Dict[str, Any],
        config: Dict[str, Any],
    ) -> Dict[str, AuditResult]:
        """Audit after execution."""
        results = {}

        # Check output quality
        results["output_quality"] = self._check_output_quality(result)

        # Check completeness
        results["completeness"] = self._check_completeness(result, payload)

        # Check for errors
        results["error_check"] = self._check_errors(result)

        return results

    def _check_input_validity(self, payload: Dict[str, Any]) -> AuditResult:
        """Check if input is valid and complete."""
        required_fields = self._detect_required_fields(payload)
        missing = [f for f in required_fields if f not in payload]

        if missing:
            return AuditResult(
                passed=False,
                category="input_validity",
                score=0.0,
                message=f"Missing required fields: {missing}",
            )

        return AuditResult(
            passed=True,
            category="input_validity",
            score=1.0,
            message="All required fields present",
        )

    def _check_task_clarity(self, payload: Dict[str, Any]) -> AuditResult:
        """Check if task is well-defined."""
        # Heuristic: task is clear if it has specific goals
        has_goals = "success_criteria" in payload or "verify" in str(payload)

        if has_goals:
            return AuditResult(
                passed=True,
                category="task_clarity",
                score=1.0,
                message="Task has clear success criteria",
            )

        return AuditResult(
            passed=False,
            category="task_clarity",
            score=0.5,
            message="Task lacks explicit success criteria",
            details={"suggestion": "Add success_criteria to payload"},
        )

    def _check_output_quality(self, result: Dict[str, Any]) -> AuditResult:
        """Check if output is of high quality."""
        # Check for errors
        has_error = "error" in result or "Error" in str(result)
        if has_error:
            return AuditResult(
                passed=False,
                category="output_quality",
                score=0.0,
                message="Output contains errors",
            )

        # Check for completeness
        has_result = "result" in result or bool(result)
        if not has_result:
            return AuditResult(
                passed=False,
                category="output_quality",
                score=0.0,
                message="No result produced",
            )

        return AuditResult(
            passed=True,
            category="output_quality",
            score=1.0,
            message="Output is complete and error-free",
        )

    def _check_completeness(
        self, result: Dict[str, Any], payload: Dict[str, Any]
    ) -> AuditResult:
        """Check if result addresses all aspects of the request."""
        # Heuristic: more detailed requests should produce more detailed results
        payload_size = len(str(payload))
        result_size = len(str(result))

        if result_size < payload_size * 0.1:
            return AuditResult(
                passed=False,
                category="completeness",
                score=0.3,
                message="Result seems incomplete relative to request",
            )

        return AuditResult(
            passed=True,
            category="completeness",
            score=1.0,
            message="Result appears complete",
        )

    def _check_errors(self, result: Dict[str, Any]) -> AuditResult:
        """Check for any errors in the result."""
        def find_errors(obj, path=""):
            errors = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k.lower() in ["error", "exception", "traceback"]:
                        errors.append(f"{path}.{k}" if path else k)
                    else:
                        errors.extend(find_errors(v, f"{path}.{k}" if path else k))
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    errors.extend(find_errors(v, f"{path}[{i}]"))
            return errors

        errors = find_errors(result)

        if errors:
            return AuditResult(
                passed=False,
                category="error_check",
                score=0.0,
                message=f"Found errors: {errors}",
            )

        return AuditResult(
            passed=True,
            category="error_check",
            score=1.0,
            message="No errors found",
        )

    def _detect_required_fields(self, payload: Dict[str, Any]) -> List[str]:
        """Detect which fields are required for this type of task."""
        # This would be more sophisticated in production
        return []

    def compile_report(
        self, pre_results: Dict[str, AuditResult], post_results: Dict[str, AuditResult]
    ) -> Dict[str, Any]:
        """Compile overall quality report."""
        all_results = {**pre_results, **post_results}
        passed = sum(1 for r in all_results.values() if r.passed)
        total = len(all_results)

        return {
            "passed": passed == total,
            "score": passed / total if total > 0 else 0,
            "checks_passed": passed,
            "checks_total": total,
            "results": all_results,
        }
