"""
Focused Selection Module

Filter out irrelevant information to work within the relevant frame of reference.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field


@dataclass
class Frame:
    """Defines the relevant scope/frame."""

    goal: str
    scope: str
    constraints: List[str] = field(default_factory=list)


@dataclass
class FilteredItem:
    """Item after filtering."""

    content: str
    relevance_score: float
    category: str  # relevant, marginal, irrelevant


class FocusedSelector:
    """
    Filters information to maintain focus.

    Framework:
    1. Define Frame
    2. Identify Noise
    3. Filter
    4. Verify Focus
    5. Proceed
    """

    def __init__(self):
        self.current_frame: Optional[Frame] = None

    def define_frame(
        self, goal: str, scope: str, constraints: List[str] = None
    ) -> Frame:
        """Define the relevant frame."""
        self.current_frame = Frame(
            goal=goal, scope=scope, constraints=constraints or []
        )
        return self.current_frame

    def identify_noise(self, items: List[str]) -> List[str]:
        """Identify likely noise items."""
        if not self.current_frame:
            return []

        noise_indicators = {"unrelated", "irrelevant", "old", "deprecated", "unused"}
        noise = []

        for item in items:
            item_lower = item.lower()
            if any(ind in item_lower for ind in noise_indicators):
                noise.append(item)

        return noise

    def calculate_relevance(self, item: str, criteria: Set[str]) -> float:
        """
        Calculate relevance score for an item.

        Args:
            item: Item to score
            criteria: Relevance criteria

        Returns:
            Score 0-1
        """
        item_words = set(item.lower().split())
        matches = item_words & criteria

        if not criteria:
            return 0.5

        return len(matches) / len(criteria)

    def filter_items(
        self, items: List[str], criteria: List[str]
    ) -> Dict[str, List[FilteredItem]]:
        """
        Filter items based on relevance.

        Args:
            items: Items to filter
            criteria: Relevance criteria

        Returns:
            Categorized items
        """
        criteria_set = set(criteria)

        relevant = []
        marginal = []
        irrelevant = []

        for item in items:
            score = self.calculate_relevance(item, criteria_set)

            if score >= 0.5:
                relevant.append(
                    FilteredItem(
                        content=item, relevance_score=score, category="relevant"
                    )
                )
            elif score >= 0.2:
                marginal.append(
                    FilteredItem(
                        content=item, relevance_score=score, category="marginal"
                    )
                )
            else:
                irrelevant.append(
                    FilteredItem(
                        content=item, relevance_score=score, category="irrelevant"
                    )
                )

        # Sort by score
        relevant.sort(key=lambda x: x.relevance_score, reverse=True)

        return {"relevant": relevant, "marginal": marginal, "irrelevant": irrelevant}

    def verify_focus(self, filtered: Dict[str, List[FilteredItem]]) -> Dict:
        """Verify focus is maintained."""
        relevant_count = len(filtered.get("relevant", []))

        return {
            "has_relevant": relevant_count > 0,
            "relevant_count": relevant_count,
            "focus_maintained": relevant_count >= 3,
            "recommendation": "Proceed" if relevant_count >= 3 else "Expand criteria",
        }

    def select_best(self, items: List[str], criteria: List[str]) -> Optional[str]:
        """Select the best item from a list."""
        filtered = self.filter_items(items, criteria)

        if filtered["relevant"]:
            return filtered["relevant"][0].content

        if filtered["marginal"]:
            return filtered["marginal"][0].content

        return None


# Convenience function
def filter_information(items: List[str], criteria: List[str]) -> Dict:
    """Quick information filtering."""
    selector = FocusedSelector()
    filtered = selector.filter_items(items, criteria)
    verification = selector.verify_focus(filtered)

    return {
        "filtered": {
            "relevant": [i.content for i in filtered["relevant"]],
            "marginal": [i.content for i in filtered["marginal"]],
            "irrelevant": [i.content for i in filtered["irrelevant"]],
        },
        "verification": verification,
    }
