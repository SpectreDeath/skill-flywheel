"""
Decision Making Module

Weigh alternatives systematically and select the best solution
based on defined criteria.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class DecisionStatus(Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    DECIDED = "decided"
    IMPLEMENTED = "implemented"


@dataclass
class Criterion:
    """Represents a decision criterion."""

    name: str
    weight: float
    description: str = ""


@dataclass
class Option:
    """Represents a decision option."""

    name: str
    scores: Dict[str, float] = field(default_factory=dict)
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)


@dataclass
class Decision:
    """Represents a decision to be made."""

    question: str
    criteria: List[Criterion] = field(default_factory=list)
    options: List[Option] = field(default_factory=list)
    status: DecisionStatus = DecisionStatus.PENDING
    selected: Optional[str] = None
    rationale: str = ""


class DecisionMaker:
    """
    Weighs alternatives and selects best solution.

    Framework:
    1. Define the Decision
    2. Identify Alternatives
    3. Establish Criteria
    4. Evaluate Each Option
    5. Make the Decision
    6. Plan Implementation
    """

    def __init__(self):
        self.current_decision: Optional[Decision] = None

    def create_decision(self, question: str) -> Decision:
        """Create a new decision."""
        decision = Decision(question=question)
        self.current_decision = decision
        return decision

    def add_criterion(
        self, name: str, weight: float, description: str = ""
    ) -> Criterion:
        """Add a criterion to the current decision."""
        if not self.current_decision:
            raise ValueError("No current decision. Create one first.")

        criterion = Criterion(name=name, weight=weight, description=description)
        self.current_decision.criteria.append(criterion)
        return criterion

    def add_option(self, name: str) -> Option:
        """Add an option to the current decision."""
        if not self.current_decision:
            raise ValueError("No current decision. Create one first.")

        option = Option(name=name)
        self.current_decision.options.append(option)
        return option

    def score_option(self, option_name: str, criterion_name: str, score: float) -> bool:
        """Score an option on a criterion (1-5 scale)."""
        if not self.current_decision:
            return False

        for option in self.current_decision.options:
            if option.name == option_name:
                option.scores[criterion_name] = max(1, min(5, score))
                return True
        return False

    def add_pros_cons(
        self, option_name: str, pros: List[str] = None, cons: List[str] = None
    ):
        """Add pros and cons for an option."""
        if not self.current_decision:
            return

        for option in self.current_decision.options:
            if option.name == option_name:
                if pros:
                    option.pros.extend(pros)
                if cons:
                    option.cons.extend(cons)

    def evaluate(self) -> Dict:
        """Evaluate all options using weighted decision matrix."""
        if not self.current_decision:
            return {"error": "No current decision"}

        decision = self.current_decision
        total_weight = sum(c.weight for c in decision.criteria)

        results = {}

        for option in decision.options:
            weighted_score = 0
            for criterion in decision.criteria:
                score = option.scores.get(criterion.name, 0)
                weight = criterion.weight / total_weight
                weighted_score += score * weight

            results[option.name] = {
                "weighted_score": round(weighted_score, 2),
                "max_possible": 5.0,
                "percentage": round(weighted_score / 5.0 * 100, 1),
                "pros": option.pros,
                "cons": option.cons,
            }

        # Find winner
        winner = max(results.items(), key=lambda x: x[1]["weighted_score"])

        return {
            "decision": decision.question,
            "criteria": [(c.name, c.weight) for c in decision.criteria],
            "results": results,
            "winner": winner[0],
            "winner_score": winner[1]["weighted_score"],
        }

    def decide(self, rationale: str = "") -> Dict:
        """Make the final decision."""
        if not self.current_decision:
            return {"error": "No current decision"}

        evaluation = self.evaluate()
        winner = evaluation["winner"]

        self.current_decision.selected = winner
        self.current_decision.rationale = rationale
        self.current_decision.status = DecisionStatus.DECIDED

        return {
            "decision": self.current_decision.question,
            "selected": winner,
            "score": evaluation["winner_score"],
            "rationale": rationale,
            "all_scores": evaluation["results"],
        }

    def create_decision_tree(self, root_decision: str, branches: Dict) -> Dict:
        """
        Create a simple decision tree.

        Args:
            root_decision: The root decision question
            branches: Dictionary of decision branches

        Returns:
            Decision tree structure
        """
        tree = {"decision": root_decision, "branches": {}}

        for branch_name, branch_data in branches.items():
            tree["branches"][branch_name] = {
                "condition": branch_data.get("condition", ""),
                "outcome": branch_data.get("outcome", ""),
                "next_steps": branch_data.get("next_steps", []),
            }

        return tree


# Convenience function
def make_decision(
    question: str, criteria: Dict[str, float], options: Dict[str, Dict[str, float]]
) -> Dict:
    """Quick decision making."""
    maker = DecisionMaker()
    maker.create_decision(question)

    for name, weight in criteria.items():
        maker.add_criterion(name, weight)

    for opt_name, scores in options.items():
        maker.add_option(opt_name)
        for crit_name, score in scores.items():
            maker.score_option(opt_name, crit_name, score)

    return maker.decide()
