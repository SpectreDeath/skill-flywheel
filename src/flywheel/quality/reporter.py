#!/usr/bin/env python3
"""
Quality Reporter

Generates structured quality reports from audit results.
"""

import logging
from typing import Any, Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class QualityReport:
    """Structured quality report."""

    overall_score: float
    grade: str
    passed: bool
    checks_passed: int
    checks_total: int
    profile: str
    checks: Dict[str, Any]
    recommendations: List[str]


class QualityReporter:
    """Generates comprehensive quality reports."""

    GRADE_THRESHOLDS = {
        "A+": 0.95,
        "A": 0.90,
        "A-": 0.85,
        "B+": 0.80,
        "B": 0.75,
        "B-": 0.70,
        "C+": 0.65,
        "C": 0.60,
        "C-": 0.55,
        "D": 0.50,
        "F": 0.0,
    }

    def generate_report(
        self,
        pre_results: Dict[str, Any],
        post_results: Dict[str, Any],
        profile_config: Dict[str, Any],
    ) -> QualityReport:
        """
        Generate comprehensive quality report.

        Args:
            pre_results: Pre-execution audit results
            post_results: Post-execution audit results
            profile_config: Behavioral profile configuration

        Returns:
            QualityReport with overall assessment
        """
        all_checks = {**pre_results.get("checks", {}), **post_results.get("checks", {})}

        overall_score = self.calculate_overall_score(all_checks)
        grade = self.get_grade(overall_score)
        passed = overall_score >= profile_config.get("min_score", 0.7)

        recommendations = self.generate_recommendations(
            all_checks, overall_score
        )

        return QualityReport(
            overall_score=overall_score,
            grade=grade,
            passed=passed,
            checks_passed=self.count_passed(all_checks),
            checks_total=len(all_checks),
            profile=profile_config.get("name", "default"),
            checks=all_checks,
            recommendations=recommendations,
        )

    def calculate_overall_score(self, checks: Dict[str, Any]) -> float:
        """
        Calculate weighted overall quality score.

        Args:
            checks: Individual check results

        Returns:
            Score between 0 and 1
        """
        if not checks:
            return 1.0

        # Weight checks by importance
        weights = {
            "simplicity": 0.25,
            "assumptions": 0.20,
            "surgical": 0.25,
            "goals": 0.30,
        }

        total_score = 0
        total_weight = 0

        for check_type, weight in weights.items():
            if check_type in checks:
                check = checks[check_type]
                # Extract score from check (may be nested)
                score = self._extract_score(check)
                total_score += score * weight
                total_weight += weight

        return total_score / total_weight if total_weight > 0 else 0.0

    def _extract_score(self, check: Any) -> float:
        """Extract numeric score from check result."""
        if isinstance(check, dict):
            # Look for passed/score fields
            if "passed" in check:
                return 1.0 if check["passed"] else 0.0
            if "score" in check:
                return float(check["score"])
            # Check nested structure
            for v in check.values():
                score = self._extract_score(v)
                if score >= 0:
                    return score
        elif isinstance(check, (int, float, bool)):
            return 1.0 if check else 0.0

        return 0.0

    def count_passed(self, checks: Dict[str, Any]) -> int:
        """Count number of passed checks."""
        passed = 0
        for check in checks.values():
            if self._is_passed(check):
                passed += 1
        return passed

    def _is_passed(self, check: Any) -> bool:
        """Determine if a check passed."""
        if isinstance(check, dict):
            if "passed" in check:
                return check["passed"]
            # Check if any nested check passed
            # Check if any nested check passed\n            return all(self._is_passed(v) for v in check.values())\n
    def get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        for grade, threshold in self.GRADE_THRESHOLDS.items():
            if score >= threshold:
                return grade
        return "F"

    def generate_summary(self, report: QualityReport) -> str:
        """
        Generate human-readable summary.

        Args:
            report: Quality report

        Returns:
            Formatted summary string
        """
        lines = []
        lines.append(f"Quality Score: {report.overall_score:.2f} ({report.grade})")
        lines.append(f"Checks: {report.checks_passed}/{report.checks_total}")
        lines.append(f"Status: {'PASS' if report.passed else 'FAIL'}")

        if report.checks:
            lines.append("\nIndividual Checks:")
            for name, check in report.checks.items():
                status = "✓" if self._is_passed(check) else "✗"
                lines.append(f"  {status} {name}")

        if report.recommendations:
            lines.append("\nRecommendations:")
            for rec in report.recommendations:
                lines.append(f"  • {rec}")

        return "\n".join(lines)

    def generate_recommendations(
        self, checks: Dict[str, Any], score: float
    ) -> List[str]:
        """
        Generate improvement recommendations.

        Args:
            checks: Individual check results
            score: Overall score

        Returns:
            List of recommendations
        """
        recommendations = []

        if score < 0.7:
            recommendations.append(
                "Review failed checks and address quality issues"
            )

        # Check-specific recommendations
        if "simplicity" in checks:
            sim = checks["simplicity"]
            if not self._is_passed(sim):
                recommendations.append(
                    "Simplify solution - reduce complexity and remove unnecessary code"
                )

        if "assumptions" in checks:
            ass = checks["assumptions"]
            if not self._is_passed(ass):
                recommendations.append(
                    "Make assumptions explicit and testable"
                )

        if "surgical" in checks:
            surg = checks["surgical"]
            if not self._is_passed(surg):
                recommendations.append(
                    "Ensure changes are minimal and focused on the request"
                )

        if "goals" in checks:
            goals = checks["goals"]
            if not self._is_passed(goals):
                recommendations.append(
                    "Define clear success criteria and verify against them"
                )

        if score >= 0.9:
            recommendations.append(
                "Excellent quality - solution meets all behavioral criteria"
            )

        return recommendations

    def to_dict(self, report: QualityReport) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "overall_score": report.overall_score,
            "grade": report.grade,
            "passed": report.passed,
            "checks_passed": report.checks_passed,
            "checks_total": report.checks_total,
            "profile": report.profile,
            "checks": report.checks,
            "recommendations": report.recommendations,
        }
