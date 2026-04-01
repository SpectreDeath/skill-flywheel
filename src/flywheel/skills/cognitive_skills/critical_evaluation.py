"""
Critical Evaluation Module

Apply standards and probabilities to assess the quality and validity of
information, arguments, and solutions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class EvidenceQuality(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SourceCredibility(Enum):
    PEER_REVIEWED = "peer_reviewed"
    OFFICIAL_DOCS = "official_documentation"
    EXPERT_OPINION = "expert_opinion"
    NEWS_ARTICLE = "news_article"
    SOCIAL_MEDIA = "social_media"
    UNKNOWN = "unknown"


@dataclass
class EvaluationCriteria:
    """Criteria for evaluating information."""

    name: str
    weight: float
    score: float | None = None


@dataclass
class Source:
    """Represents an information source."""

    name: str
    credibility: SourceCredibility
    url: str | None = None
    date: str | None = None


class CriticalEvaluator:
    """
    Applies standards and probabilities to assess quality.

    Framework:
    1. Source Credibility
    2. Evidence Quality
    3. Logical Coherence
    4. Practicality
    5. Probability Assessment
    """

    def __init__(self):
        self.credibility_scores = {
            SourceCredibility.PEER_REVIEWED: 5.0,
            SourceCredibility.OFFICIAL_DOCS: 4.0,
            SourceCredibility.EXPERT_OPINION: 3.0,
            SourceCredibility.NEWS_ARTICLE: 2.0,
            SourceCredibility.SOCIAL_MEDIA: 1.0,
            SourceCredibility.UNKNOWN: 0.5,
        }

    def evaluate_source(self, source: Source) -> Dict:
        """Evaluate the credibility of a source."""
        base_score = self.credibility_scores.get(source.credibility, 0.5)

        # Adjust for recency if date available
        # (simplified - would normally parse dates)

        return {
            "source": source.name,
            "credibility": source.credibility.value,
            "quality_score": base_score,
            "assessment": "HIGH"
            if base_score >= 4
            else "MEDIUM"
            if base_score >= 2
            else "LOW",
        }

    def evaluate_claim(
        self, claim: str, sources: List[Source], evidence: List[str]
    ) -> Dict:
        """
        Evaluate a claim against sources and evidence.

        Args:
            claim: The claim to evaluate
            sources: List of sources supporting the claim
            evidence: List of evidence statements

        Returns:
            Dictionary with evaluation results
        """
        # Evaluate sources
        source_scores = [self.evaluate_source(s)["quality_score"] for s in sources]
        avg_source_score = (
            sum(source_scores) / len(source_scores) if source_scores else 0
        )

        # Evaluate evidence
        evidence_count = len(evidence)
        evidence_quality = self._assess_evidence_quality(evidence)

        # Calculate overall probability
        probability = self._calculate_probability(
            avg_source_score, evidence_quality, evidence_count
        )

        return {
            "claim": claim,
            "source_evaluation": {
                "count": len(sources),
                "average_score": avg_source_score,
                "assessment": "HIGH"
                if avg_source_score >= 4
                else "MEDIUM"
                if avg_source_score >= 2
                else "LOW",
            },
            "evidence_evaluation": {
                "count": evidence_count,
                "quality": evidence_quality.value,
            },
            "probability": probability,
            "conclusion": self._get_conclusion(probability),
        }

    def _assess_evidence_quality(self, evidence: List[str]) -> EvidenceQuality:
        """Assess the quality of evidence."""
        if len(evidence) >= 5:
            return EvidenceQuality.HIGH
        elif len(evidence) >= 2:
            return EvidenceQuality.MEDIUM
        else:
            return EvidenceQuality.LOW

    def _calculate_probability(
        self,
        source_score: float,
        evidence_quality: EvidenceQuality,
        evidence_count: int,
    ) -> float:
        """Calculate overall probability score."""
        quality_weight = {"high": 1.0, "medium": 0.6, "low": 0.3}

        base = source_score / 5.0 * 0.4
        quality = quality_weight[evidence_quality.value] * 0.4
        count = min(evidence_count / 5.0, 1.0) * 0.2

        return round((base + quality + count) * 100, 1)

    def _get_conclusion(self, probability: float) -> str:
        """Get conclusion based on probability."""
        if probability >= 75:
            return "HIGHLY PROBABLE"
        elif probability >= 50:
            return "PROBABLE"
        elif probability >= 25:
            return "UNLIKELY"
        else:
            return "HIGHLY UNLIKELY"

    def create_weighted_evaluation(
        self,
        criteria: List[EvaluationCriteria],
        option_scores: Dict[str, Dict[str, float]],
    ) -> Dict:
        """
        Create a weighted decision matrix evaluation.

        Args:
            criteria: List of evaluation criteria with weights
            option_scores: Scores for each option on each criterion

        Returns:
            Dictionary with weighted scores
        """
        results = {}
        total_weight = sum(c.weight for c in criteria)

        for option_name, scores in option_scores.items():
            weighted_score = 0
            for criterion in criteria:
                score = scores.get(criterion.name, 0)
                weight = criterion.weight / total_weight
                weighted_score += score * weight

            results[option_name] = {
                "weighted_score": round(weighted_score, 2),
                "normalized_score": round(weighted_score / 5.0 * 100, 1),
            }

        # Determine winner
        winner = max(results.items(), key=lambda x: x[1]["weighted_score"])

        return {
            "results": results,
            "winner": winner[0],
            "score": winner[1]["weighted_score"],
        }


# Convenience function
def evaluate_claim(claim: str, sources: List[Dict], evidence: List[str]) -> Dict:
    """Quick claim evaluation."""
    evaluator = CriticalEvaluator()
    source_objects = [
        Source(
            name=s.get("name", "Unknown"),
            credibility=SourceCredibility[
                s.get("credibility", "UNKNOWN").upper().replace(" ", "_")
            ],
        )
        for s in sources
    ]
    return evaluator.evaluate_claim(claim, source_objects, evidence)


# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "evaluate_claim")
    timestamp = _dt.datetime.now().isoformat()
    kwargs = {k: v for k, v in payload.items() if k != "action"}

    instance = CriticalEvaluator()

    if action == "get_info":
        return {"result": {"name": "critical_evaluation", "actions": ['create_weighted_evaluation', 'evaluate_claim', 'evaluate_source'] }, "metadata": {"action": action, "timestamp": timestamp}}

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    result = method(**kwargs)
    if _inspect.isawaitable(result):
        result = await result
    return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
