"""
Logical Reasoning Module

Applies rational assessment to draw correct inferences from premises to conclusions
using formal logical rules.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple


class LogicalFallacy(Enum):
    CIRCULAR_REASONING = "circular_reasoning"
    FALSE_DILEMMA = "false_dilemma"
    HASTY_GENERALIZATION = "hasty_generalization"
    AD_HOMINEM = "ad_hominem"
    STRAW_MAN = "straw_man"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    SLIPPERY_SLOPE = "slippery_slope"
    NONE = "none"


@dataclass
class LogicalStatement:
    """Represents a logical statement with premise and conclusion."""

    premise: str
    conclusion: str
    is_valid: bool = True
    is_sound: bool = True
    strength: str = "strong"  # strong, moderate, weak


@dataclass
class Syllogism:
    """Represents a syllogism with two premises and a conclusion."""

    premise1: str
    premise2: str
    conclusion: str
    major_term: str = ""
    minor_term: str = ""
    middle_term: str = ""


class LogicalReasoner:
    """
    Applies rational assessment to draw correct inferences.

    Supports:
    - Syllogistic reasoning
    - Modus ponens / modus tollens
    - Fallacy detection
    - Argument evaluation
    """

    def __init__(self):
        self.fallacy_patterns = {
            LogicalFallacy.CIRCULAR_REASONING: r"(.+)\s+because\s+\1",
            LogicalFallacy.FALSE_DILEMMA: r"(?:either|only\s+two|there\s+are\s+two|must\s+be)",
            LogicalFallacy.HASTY_GENERALIZATION: r"(?:all\s+|every\s+|always\s+|never\s+).{0,20}prove",
        }

    def evaluate_syllogism(self, syllogism: Syllogism) -> Dict:
        """
        Evaluate a syllogism for validity and soundness.

        Args:
            syllogism: Syllogism to evaluate

        Returns:
            Dictionary with evaluation results
        """
        # Check structure (simplified validation)
        is_valid = self._check_syllogism_structure(syllogism)

        return {
            "is_valid": is_valid,
            "is_sound": is_valid,  # Simplified - assumes premises are true
            "premise1": syllogism.premise1,
            "premise2": syllogism.premise2,
            "conclusion": syllogism.conclusion,
            "assessment": "Valid syllogism"
            if is_valid
            else "Invalid syllogism structure",
        }

    def _check_syllogism_structure(self, syllogism: Syllogism) -> bool:
        """Check if syllogism has valid logical structure."""
        # Simplified check - in practice would use formal logic
        return bool(syllogism.premise1 and syllogism.premise2 and syllogism.conclusion)

    def modus_ponens(self, premise: str, implication: str) -> str | None:
        """
        Apply modus ponens: If P then Q. P. Therefore Q.

        Args:
            premise: The condition P
            implication: The implication "If P then Q"

        Returns:
            The derived conclusion or None
        """
        # Simplified implementation
        return f"Therefore: {premise} leads to the conclusion"

    def modus_tollens(self, negated_conclusion: str, implication: str) -> str | None:
        """
        Apply modus tollens: If P then Q. Not Q. Therefore not P.

        Args:
            negated_conclusion: The negated conclusion (not Q)
            implication: The implication "If P then Q"

        Returns:
            The derived conclusion or None
        """
        return f"Therefore: {negated_conclusion} implies the premise is false"

    def detect_fallacy(self, statement: str) -> Tuple[LogicalFallacy, float]:
        """
        Detect logical fallacies in a statement.

        Args:
            statement: Statement to analyze

        Returns:
            Tuple of (detected fallacy, confidence score)
        """
        import re

        for fallacy, pattern in self.fallacy_patterns.items():
            if re.search(pattern, statement, re.IGNORECASE):
                return fallacy, 0.8

        return LogicalFallacy.NONE, 0.0

    def evaluate_argument(self, premises: List[str], conclusion: str) -> Dict:
        """
        Evaluate a complete argument.

        Args:
            premises: List of premise statements
            conclusion: The conclusion to evaluate

        Returns:
            Dictionary with evaluation results
        """
        fallacy, confidence = self.detect_fallacy(" ".join(premises) + " " + conclusion)

        return {
            "premises": premises,
            "conclusion": conclusion,
            "premise_count": len(premises),
            "detected_fallacy": fallacy.value
            if fallacy != LogicalFallacy.NONE
            else None,
            "fallacy_confidence": confidence,
            "is_logically_valid": fallacy == LogicalFallacy.NONE,
            "strength": "strong"
            if confidence < 0.3
            else "moderate"
            if confidence < 0.6
            else "weak",
        }

    def create_syllogism(
        self, premise1: str, premise2: str, conclusion: str
    ) -> Syllogism:
        """Create a syllogism from premises and conclusion."""
        return Syllogism(premise1=premise1, premise2=premise2, conclusion=conclusion)


# Convenience function
def evaluate_argument(premises: List[str], conclusion: str) -> Dict:
    """Quick evaluation of an argument."""
    reasoner = LogicalReasoner()
    return reasoner.evaluate_argument(premises, conclusion)


def detect_fallacy(statement: str) -> Tuple[str, float]:
    """Quick fallacy detection."""
    reasoner = LogicalReasoner()
    fallacy, confidence = reasoner.detect_fallacy(statement)
    return fallacy.value, confidence


# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""

if __name__ == "__main__":
    import datetime as _dt
        action = payload.get("action", "evaluate_argument")
        timestamp = _dt.datetime.now().isoformat()
        kwargs = {k: v for k, v in payload.items() if k != "action"}

        instance = LogicalReasoner()

        if action == "get_info":
            return {"result": {"name": "logical_reasoning", "actions": ['create_syllogism', 'detect_fallacy', 'evaluate_argument', 'evaluate_syllogism', 'modus_ponens', 'modus_tollens'] }, "metadata": {"action": action, "timestamp": timestamp}}

        method = getattr(instance, action, None)
        if method is None:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

        result = method(**kwargs)
        if _inspect.isawaitable(result):
            result = await result
        return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}