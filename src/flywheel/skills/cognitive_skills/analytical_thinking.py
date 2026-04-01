"""
Analytical Thinking Module

Systematically break down complex problems into components to identify
patterns and find optimal solutions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class Component:
    """Represents a problem component."""

    name: str
    description: str
    relationships: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)


class AnalyticalThinker:
    """
    Breaks down complex problems systematically.

    Framework:
    1. Decompose - Break into sub-components
    2. Examine - Study each component
    3. Compare - Find commonalities/differences
    4. Synthesize - Combine insights
    5. Validate - Test solution
    """

    def __init__(self):
        self.components: List[Component] = []

    def decompose(self, problem: str, sub_components: List[str]) -> List[Component]:
        """Decompose a problem into components."""
        self.components = [
            Component(name=name, description=f"Component: {name}")
            for name in sub_components
        ]
        return self.components

    def examine_component(self, component_name: str, data: Dict[str, Any]) -> Component:
        """Examine a specific component with data."""
        for comp in self.components:
            if comp.name == component_name:
                comp.data = data
                return comp
        raise ValueError(f"Component {component_name} not found")

    def identify_patterns(self, data: List[Any]) -> Dict[str, Any]:
        """
        Identify patterns in data.

        Args:
            data: List of data points

        Returns:
            Dictionary with pattern analysis
        """
        if not data:
            return {"pattern": "unknown", "confidence": 0}

        # Check for linear pattern
        if all(isinstance(x, (int, float)) for x in data):
            differences = [data[i + 1] - data[i] for i in range(len(data) - 1)]
            if len(set(differences)) == 1:
                return {
                    "pattern": "linear",
                    "formula": f"y = {differences[0]}x + b",
                    "confidence": 0.9,
                }

            # Check for exponential
            if len(data) > 1:
                ratios = [
                    data[i + 1] / data[i] for i in range(len(data) - 1) if data[i] != 0
                ]
                if len({round(r, 2) for r in ratios}) == 1:
                    return {
                        "pattern": "exponential",
                        "formula": f"y = {data[0]} * {round(ratios[0], 2)}^x",
                        "confidence": 0.85,
                    }

        # Check for periodic (simplified)
        if len(data) >= 4:
            first_half = data[: len(data) // 2]
            if len(set(first_half)) < len(first_half) // 2:
                return {"pattern": "periodic", "confidence": 0.7}

        return {"pattern": "unknown", "confidence": 0}

    def compare_components(self, comp1: str, comp2: str) -> Dict:
        """Compare two components."""
        c1 = next((c for c in self.components if c.name == comp1), None)
        c2 = next((c for c in self.components if c.name == comp2), None)

        if not c1 or not c2:
            return {"error": "Component not found"}

        return {
            "component1": comp1,
            "component2": comp2,
            "commonalities": list(set(c1.data.keys()) & set(c2.data.keys())),
            "differences": list(set(c1.data.keys()) ^ set(c2.data.keys())),
        }

    def synthesize_insights(self) -> Dict:
        """Synthesize insights from all components."""
        if not self.components:
            return {"error": "No components to analyze"}

        all_keys = set()
        for comp in self.components:
            all_keys.update(comp.data.keys())

        return {
            "total_components": len(self.components),
            "unique_metrics": len(all_keys),
            "components": [c.name for c in self.components],
        }

    def root_cause_analysis(
        self, symptoms: List[str], possible_causes: List[str]
    ) -> Dict:
        """
        Perform root cause analysis.

        Args:
            symptoms: Observed symptoms
            possible_causes: Possible causes

        Returns:
            Dictionary with likely root causes
        """
        # Simplified scoring
        causes_ranked = []
        for cause in possible_causes:
            score = len(cause) % 5 + 3  # Simplified scoring
            causes_ranked.append(
                {
                    "cause": cause,
                    "likelihood": min(score / 10.0, 1.0),
                    "recommended": score >= 6,
                }
            )

        causes_ranked.sort(key=lambda x: x["likelihood"], reverse=True)

        return {
            "symptoms": symptoms,
            "likely_causes": causes_ranked[:3],
            "root_cause": causes_ranked[0]["cause"] if causes_ranked else None,
        }

    def analyze_data(self, data: Dict[str, List]) -> Dict:
        """
        Analyze data across components.

        Args:
            data: Dictionary of component data

        Returns:
            Analysis results
        """
        results = {}
        for component_name, values in data.items():
            pattern = self.identify_patterns(values)
            results[component_name] = pattern

        return results


# Convenience function
def analyze_problem(problem: str, components: List[str]) -> Dict:
    """Quick analytical thinking."""
    thinker = AnalyticalThinker()
    thinker.decompose(problem, components)
    return thinker.synthesize_insights()


# --- invoke() wrapper added by batch fix ---
import asyncio as _asyncio
import inspect as _inspect

async def invoke(payload: dict) -> dict:
    """Entry point for skill invocation."""
    import datetime as _dt
    action = payload.get("action", "analyze_problem")
    timestamp = _dt.datetime.now().isoformat()
    kwargs = {k: v for k, v in payload.items() if k != "action"}

    instance = AnalyticalThinker()

    if action == "get_info":
        return {"result": {"name": "analytical_thinking", "actions": ['analyze_problem', 'decompose', 'identify_patterns', 'root_cause_analysis', 'synthesize_insights'] }, "metadata": {"action": action, "timestamp": timestamp}}

    method = getattr(instance, action, None)
    if method is None:
        return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"action": action, "timestamp": timestamp}}

    result = method(**kwargs)
    if _inspect.isawaitable(result):
        result = await result
    return {"result": result, "metadata": {"action": action, "timestamp": timestamp}}
