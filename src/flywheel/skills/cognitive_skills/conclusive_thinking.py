"""
Conclusive Thinking Module

Reach definitive, unambiguous answers that resolve questions completely.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List


class ConclusionType(Enum):
    DEFINITIVE = "definitive"
    PROBABLE = "probable"
    INCONCLUSIVE = "inconclusive"
    IMPOSSIBLE = "impossible"


@dataclass
class Evidence:
    """Evidence for a conclusion."""

    statement: str
    strength: float  # 0-1
    source: str


class ConclusiveThinker:
    """
    Reaches definitive conclusions.

    Framework:
    1. Assess Sufficiency
    2. Evaluate Evidence
    3. Determine Answer
    4. State Conclusion
    5. Resolve
    """

    def __init__(self):
        self.evidence: List[Evidence] = []

    def add_evidence(self, statement: str, strength: float, source: str) -> Evidence:
        """Add evidence for consideration."""
        evidence = Evidence(
            statement=statement, strength=max(0, min(1, strength)), source=source
        )
        self.evidence.append(evidence)
        return evidence

    def assess_sufficiency(self) -> Dict:
        """Assess if enough information exists."""
        total_strength = sum(e.strength for e in self.evidence)
        avg_strength = total_strength / len(self.evidence) if self.evidence else 0

        return {
            "evidence_count": len(self.evidence),
            "average_strength": avg_strength,
            "sufficient": len(self.evidence) >= 3 and avg_strength >= 0.5,
            "gaps": self._identify_gaps(),
        }

    def _identify_gaps(self) -> List[str]:
        """Identify information gaps."""
        gaps = []
        if len(self.evidence) < 3:
            gaps.append("Need more evidence points")
        if (
            sum(e.strength for e in self.evidence) / len(self.evidence) < 0.5
            if self.evidence
            else True
        ):
            gaps.append("Evidence too weak")
        return gaps

    def evaluate_evidence(self) -> Dict:
        """Evaluate the strength of evidence."""
        if not self.evidence:
            return {"error": "No evidence to evaluate"}

        return {
            "total_evidence": len(self.evidence),
            "strong_count": len([e for e in self.evidence if e.strength >= 0.7]),
            "medium_count": len([e for e in self.evidence if 0.4 <= e.strength < 0.7]),
            "weak_count": len([e for e in self.evidence if e.strength < 0.4]),
            "overall_strength": sum(e.strength for e in self.evidence)
            / len(self.evidence),
        }

    def determine_conclusion(self, question: str) -> Dict:
        """
        Determine the conclusion.

        Args:
            question: The question to answer

        Returns:
            Conclusion with confidence
        """
        sufficiency = self.assess_sufficiency()
        evaluation = self.evaluation()

        # Determine conclusion type
        if not sufficiency["sufficient"]:
            if not self.evidence:
                conclusion_type = ConclusionType.IMPOSSIBLE
            else:
                conclusion_type = ConclusionType.INCONCLUSIVE
        elif evaluation["overall_strength"] >= 0.7:
            conclusion_type = ConclusionType.DEFINITIVE
        else:
            conclusion_type = ConclusionType.PROBABLE

        return {
            "question": question,
            "conclusion_type": conclusion_type.value,
            "confidence": self._get_confidence(conclusion_type),
            "sufficiency": sufficiency,
            "evidence_evaluation": evaluation,
            "requires_more_info": conclusion_type
            in [ConclusionType.INCONCLUSIVE, ConclusionType.IMPOSSIBLE],
        }

    def _get_confidence(self, conclusion_type: ConclusionType) -> str:
        """Get confidence level string."""
        mapping = {
            ConclusionType.DEFINITIVE: "HIGH",
            ConclusionType.PROBABLE: "MEDIUM",
            ConclusionType.INCONCLUSIVE: "LOW",
            ConclusionType.IMPOSSIBLE: "N/A",
        }
        return mapping.get(conclusion_type, "UNKNOWN")

    def state_conclusion(
        self, question: str, answer: str, caveats: List[str] = None
    ) -> Dict:
        """State the final conclusion."""
        determination = self.determine_conclusion(question)

        return {
            "question": question,
            "answer": answer,
            "type": determination["conclusion_type"],
            "confidence": determination["confidence"],
            "caveats": caveats or [],
            "resolved": determination["conclusion_type"]
            in [ConclusionType.DEFINITIVE, ConclusionType.PROBABLE],
        }

    def root_cause_analysis(self, symptoms: List[str], evidence: List[Dict]) -> Dict:
        """Perform root cause analysis."""
        causes = []

        for e in evidence:
            if e.get("type") == "cause":
                causes.append(
                    {"cause": e.get("statement"), "strength": e.get("strength", 0.5)}
                )

        causes.sort(key=lambda x: x["strength"], reverse=True)

        return {
            "symptoms": symptoms,
            "likely_root_cause": causes[0] if causes else None,
            "confidence": "HIGH"
            if causes and causes[0]["strength"] >= 0.7
            else "MEDIUM",
            "conclusion": f"Root cause: {causes[0]['cause']}"
            if causes
            else "Inconclusive",
        }


# Convenience function
def conclude(question: str, evidence: List[Dict]) -> Dict:
    """Quick conclusive thinking."""
    thinker = ConclusiveThinker()
    for e in evidence:
        thinker.add_evidence(
            e.get("statement", ""), e.get("strength", 0.5), e.get("source", "unknown")
        )
    return thinker.determine_conclusion(question)


# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "evaluate_evidence")
    timestamp = _dt.datetime.now().isoformat()
    kwargs = {k: v for k, v in payload.items() if k != "action"}

    instance = ConclusiveThinker()

    if action == "get_info":
        return {"result": {"name": "conclusive_thinking", "actions": ['add_evidence', 'assess_sufficiency', 'determine_conclusion', 'evaluate_evidence', 'state_conclusion'] }, "metadata": {"action": action, "timestamp": timestamp}}

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    result = method(**kwargs)
    if _inspect.isawaitable(result):
        result = await result
    return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
