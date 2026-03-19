"""
Fact-Based Assessment Module

Evaluate situations and make decisions using observable evidence
rather than intuition or assumptions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Tuple


class FactType(Enum):
    OBSERVABLE = "observable"
    MEASURED = "measured"
    RECORDED = "recorded"
    DERIVED = "derived"


class OpinionType(Enum):
    INTERPRETATION = "interpretation"
    JUDGMENT = "judgment"
    PREDICTION = "prediction"
    PREFERENCE = "preference"


@dataclass
class Fact:
    """Represents a factual statement."""

    statement: str
    fact_type: FactType
    source: str
    verified: bool = False
    confidence: float = 1.0


@dataclass
class Opinion:
    """Represents an opinion statement."""

    statement: str
    opinion_type: OpinionType
    basis: str = ""


class FactBasedAssessor:
    """
    Assesses situations using evidence.

    Framework:
    1. Gather Facts
    2. Separate from Opinions
    3. Verify Sources
    4. Analyze
    5. Conclude
    """

    def __init__(self):
        self.facts: List[Fact] = []
        self.opinions: List[Opinion] = []

    def add_fact(self, statement: str, fact_type: FactType, source: str) -> Fact:
        """Add a factual statement."""
        fact = Fact(statement=statement, fact_type=fact_type, source=source)
        self.facts.append(fact)
        return fact

    def add_opinion(
        self, statement: str, opinion_type: OpinionType, basis: str = ""
    ) -> Opinion:
        """Add an opinion statement."""
        opinion = Opinion(statement=statement, opinion_type=opinion_type, basis=basis)
        self.opinions.append(opinion)
        return opinion

    def separate_facts_from_opinions(
        self, statements: List[str]
    ) -> Tuple[List[Fact], List[Opinion]]:
        """
        Separate factual from opinion statements.

        Args:
            statements: List of statements to categorize

        Returns:
            Tuple of (facts, opinions)
        """
        facts = []
        opinions = []

        # Simple heuristic: statements with numbers, dates, specific names are facts
        # Statements with subjective words are opinions
        subjective_indicators = {
            "believe",
            "think",
            "feel",
            "probably",
            "might",
            "could be",
            "seems",
        }

        for stmt in statements:
            stmt_lower = stmt.lower()
            has_numbers = any(c.isdigit() for c in stmt)
            has_subjective = any(ind in stmt_lower for ind in subjective_indicators)

            if has_numbers or not has_subjective:
                fact = Fact(
                    statement=stmt, fact_type=FactType.OBSERVABLE, source="user_input"
                )
                facts.append(fact)
            else:
                opinion = Opinion(
                    statement=stmt, opinion_type=OpinionType.INTERPRETATION
                )
                opinions.append(opinion)

        return facts, opinions

    def verify_source(self, source: str) -> Dict:
        """Verify a source's credibility."""
        # Simplified source verification
        source_trust = {
            "official": 5,
            "peer-reviewed": 5,
            "expert": 4,
            "documented": 3,
            "reported": 2,
            "hearsay": 1,
        }

        trust_level = source_trust.get(source.lower(), 2)

        return {
            "source": source,
            "trust_score": trust_level,
            "verified": trust_level >= 3,
        }

    def analyze_facts(self) -> Dict:
        """Analyze gathered facts."""
        if not self.facts:
            return {"error": "No facts to analyze"}

        type_counts = {}
        for fact in self.facts:
            type_counts[fact.fact_type.value] = (
                type_counts.get(fact.fact_type.value, 0) + 1
            )

        return {
            "total_facts": len(self.facts),
            "by_type": type_counts,
            "all_verified": all(f.verified for f in self.facts),
            "average_confidence": sum(f.confidence for f in self.facts)
            / len(self.facts),
        }

    def draw_conclusion(self) -> Dict:
        """Draw evidence-based conclusion."""
        analysis = self.analyze_facts()

        if self.facts:
            conclusion = f"Based on {len(self.facts)} factual statements"
            if self.opinions:
                conclusion += f" and {len(self.opinions)} opinion statements"
            conclusion += "."

            return {
                "conclusion": conclusion,
                "evidence_strength": "HIGH"
                if len(self.facts) >= 5
                else "MEDIUM"
                if len(self.facts) >= 2
                else "LOW",
                "facts_count": len(self.facts),
                "opinions_count": len(self.opinions),
                "recommendation": "Proceed with confidence"
                if len(self.facts) >= 3
                else "Gather more evidence",
            }

        return {"error": "Insufficient information"}

    def assess_data(self, data: Dict[str, Any]) -> Dict:
        """
        Assess data for fact-based decision making.

        Args:
            data: Data dictionary to assess

        Returns:
            Assessment results
        """
        facts_extracted = []

        for key, value in data.items():
            if isinstance(value, (int, float, bool)):
                fact = Fact(
                    statement=f"{key}: {value}",
                    fact_type=FactType.MEASURED,
                    source="data_input",
                )
                facts_extracted.append(fact)

        self.facts.extend(facts_extracted)

        return {
            "data_points": len(data),
            "facts_extracted": len(facts_extracted),
            "assessment": self.analyze_facts(),
        }


# Convenience function
def assess_facts(statements: List[str]) -> Dict:
    """Quick fact-based assessment."""
    assessor = FactBasedAssessor()
    facts, opinions = assessor.separate_facts_from_opinions(statements)
    assessor.facts.extend(facts)
    assessor.opinions.extend(opinions)
    return assessor.draw_conclusion()
