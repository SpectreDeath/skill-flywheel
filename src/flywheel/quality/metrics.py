#!/usr/bin/env python3
"""
Quality Metrics

Provides quantitative measures for assessing solution quality.
"""

import re
from typing import Any, Dict, List


class ComplexityMetric:
    """Measures code complexity."""

    @staticmethod
    def cyclomatic_complexity(code: str) -> int:
        """Approximate cyclomatic complexity."""
        decision_points = [
            r"\bif\b",
            r"\belif\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\bexcept\b",
            r"\band\b",
            r"\bor\b",
        ]

        count = 1  # Base complexity
        for pattern in decision_points:
            count += len(re.findall(pattern, code))

        return count

    @staticmethod
    def nesting_depth(code: str) -> int:
        """Maximum nesting depth."""
        max_depth = 0
        current_depth = 0

        for line in code.split("\n"):
            # Count indentation levels (assuming 4 spaces)
            indent = len(line) - len(line.lstrip())
            depth = indent // 4

            if depth > max_depth:
                max_depth = depth

        return max_depth

    @staticmethod
    def cognitive_complexity(code: str) -> int:
        """Approximate cognitive complexity."""
        # Simple approximation: count control structures
        structures = [
            r"\bif\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\btry\b",
            r"\bexcept\b",
            r"\bwith\b",
        ]

        score = 0
        for pattern in structures:
            score += len(re.findall(pattern, code))

        return score


class SurgicalMetric:
    """Measures change focus and minimality."""

    @staticmethod
    def change_ratio(original: str, modified: str) -> float:
        """Ratio of changed lines to total lines."""
        orig_lines = original.splitlines()
        mod_lines = modified.splitlines()

        if not orig_lines:
            return 0.0

        # Simple diff approximation
        changes = abs(len(orig_lines) - len(mod_lines))
        total = max(len(orig_lines), len(mod_lines))

        return changes / total

    @staticmethod
    def related_change_ratio(
        original: str, modified: str, keywords: List[str]
    ) -> float:
        """Ratio of changes related to keywords."""
        import difflib

        diff = list(
            difflib.unified_diff(
                original.splitlines(keepends=True),
                modified.splitlines(keepends=True),
                lineterm="",
            )
        )

        changed_lines = [d for d in diff if d.startswith(("+", "-"))]
        if not changed_lines:
            return 1.0

        related = sum(
            1
            for line in changed_lines
            if any(kw in line.lower() for kw in keywords)
        )

        return related / len(changed_lines)


class GoalMetric:
    """Measures goal achievement."""

    @staticmethod
    def criteria_met(
        result: Dict[str, Any], criteria: List[Dict[str, Any]]
    ) -> float:
        """Ratio of criteria met."""
        if not criteria:
            return 1.0

        met = 0
        for criterion in criteria:
            name = criterion.get("name", "")
            expected = criterion.get("target")

            if name in result:
                actual = result[name]
                if actual == expected:
                    met += 1

        return met / len(criteria)

    @staticmethod
    def success_indicator(result: Dict[str, Any]) -> float:
        """Overall success indicator (0-1)."""
        # Check common success indicators
        if result.get("status") == "success":
            return 1.0
        if result.get("passed") is True:
            return 1.0
        if result.get("satisfiable") is True:
            return 1.0
        if "error" in result or "Error" in str(result):
            return 0.0

        # Default: assume partial success
        return 0.5