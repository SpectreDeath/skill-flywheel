"""
SWOT Analysis Tool

Conducts SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis:
- Factor identification and categorization
- Strategic implications
- Action item generation
"""

from typing import Any, Dict, List
from datetime import datetime


def categorize_factors(factors: List[str], category: str) -> List[Dict]:
    """Categorize factors with descriptions"""
    categorized = []
    for factor in factors:
        categorized.append(
            {
                "factor": factor,
                "category": category,
                "impact": "high" if len(factor) > 20 else "medium",
            }
        )
    return categorized


def generate_strategic_implications(swot: Dict) -> List[str]:
    """Generate strategic implications from SWOT analysis"""
    implications = []

    strengths = swot.get("strengths", [])
    weaknesses = swot.get("weaknesses", [])
    opportunities = swot.get("opportunities", [])
    threats = swot.get("threats", [])

    # S-O strategies: Use strengths to take advantage of opportunities
    for s in strengths[:2]:
        for o in opportunities[:2]:
            implications.append(f"Use '{s}' to capitalize on '{o}'")

    # W-O strategies: Overcome weaknesses to take advantage of opportunities
    for w in weaknesses[:2]:
        for o in opportunities[:2]:
            implications.append(f"Address '{w}' to enable '{o}'")

    # S-T strategies: Use strengths to avoid threats
    for s in strengths[:2]:
        for t in threats[:2]:
            implications.append(f"Use '{s}' to mitigate '{t}'")

    # W-T strategies: Minimize weaknesses to avoid threats
    for w in weaknesses[:2]:
        for t in threats[:2]:
            implications.append(f"Reduce '{w}' to defend against '{t}'")

    return implications[:8]


def swot_analyzer(organization_data: Dict, **kwargs) -> Dict[str, Any]:
    """
    Conduct SWOT analysis from business data.

    Args:
        organization_data: Dict with strengths, weaknesses, opportunities, threats
        **kwargs: Additional parameters

    Returns:
        SWOT analysis with strategic implications
    """
    strengths = organization_data.get("strengths", [])
    weaknesses = organization_data.get("weaknesses", [])
    opportunities = organization_data.get("opportunities", [])
    threats = organization_data.get("threats", [])

    if not any([strengths, weaknesses, opportunities, threats]):
        return {"status": "error", "error": "No SWOT data provided"}

    # Categorize each factor
    categorized_swot = {
        "strengths": categorize_factors(strengths, "strength"),
        "weaknesses": categorize_factors(weaknesses, "weakness"),
        "opportunities": categorize_factors(opportunities, "opportunity"),
        "threats": categorize_factors(threats, "threat"),
    }

    # Calculate scores
    total_factors = len(strengths) + len(weaknesses) + len(opportunities) + len(threats)
    strength_ratio = len(strengths) / max(1, len(strengths) + len(weaknesses))
    opportunity_ratio = len(opportunities) / max(1, len(opportunities) + len(threats))

    # Overall health score
    health_score = (
        strength_ratio * 0.4
        + opportunity_ratio * 0.4
        + min(1, len(strengths) / 5) * 0.2
    ) * 100

    # Generate strategic implications
    implications = generate_strategic_implications(organization_data)

    # Generate action items
    actions = []
    if strengths:
        actions.append(f"Leverage: {strengths[0]}")
    if weaknesses:
        actions.append(f"Improve: {weaknesses[0]}")
    if opportunities:
        actions.append(f"Pursue: {opportunities[0]}")
    if threats:
        actions.append(f"Mitigate: {threats[0]}")

    return {
        "status": "success",
        "swot": categorized_swot,
        "summary": {
            "total_factors": total_factors,
            "strengths_count": len(strengths),
            "weaknesses_count": len(weaknesses),
            "opportunities_count": len(opportunities),
            "threats_count": len(threats),
            "health_score": round(health_score, 1),
            "health_status": "strong"
            if health_score > 70
            else "moderate"
            if health_score > 50
            else "weak",
        },
        "implications": implications,
        "recommended_actions": actions,
    }


async def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "analyze")
    organization_data = payload.get("organization_data", {})

    if action == "analyze":
        result = swot_analyzer(organization_data)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata"""

if __name__ == "__main__":
    return {
            "name": "swot-analyzer",
            "description": "Conduct SWOT analysis from business data",
            "version": "1.0.0",
            "domain": "STRATEGY",
        }