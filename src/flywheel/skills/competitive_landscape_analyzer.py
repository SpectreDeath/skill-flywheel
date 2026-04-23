"""
Competitive Landscape Analyzer

Analyzes competitive landscape and identifies market positioning:
- Competitor identification and profiling
- Market share analysis
- Positioning mapping
- Competitive advantage assessment
"""

from typing import Any, Dict, List
from datetime import datetime


def parse_competitors(competitor_data: List[Dict]) -> List[Dict]:
    """Parse and validate competitor data"""
    competitors = []
    for comp in competitor_data:
        competitors.append(
            {
                "name": comp.get("name", "Unknown"),
                "market_share": comp.get("market_share", 0),
                "strengths": comp.get("strengths", []),
                "weaknesses": comp.get("weaknesses", []),
                "products": comp.get("products", []),
                "position": comp.get("position", "unknown"),
            }
        )
    return competitors


def analyze_market_position(
    competitors: List[Dict], your_company: Dict
) -> Dict[str, Any]:
    """Analyze market position relative to competitors"""

    # Calculate market position metrics
    total_share = sum(c["market_share"] for c in competitors)
    your_share = your_company.get("market_share", 0)

    # Find closest competitors
    share_diff = [(c["name"], abs(c["market_share"] - your_share)) for c in competitors]
    share_diff.sort(key=lambda x: x[1])
    closest = share_diff[:3]

    # Identify competitive advantages
    your_strengths = set(your_company.get("strengths", []))
    competitor_gaps = []

    for comp in competitors:
        comp_strengths = set(comp.get("strengths", []))
        gaps = your_strengths - comp_strengths
        if gaps:
            competitor_gaps.append(
                {"competitor": comp["name"], "advantages": list(gaps)}
            )

    return {
        "your_market_share": your_share,
        "total_market_share": total_share + your_share,
        "closest_competitors": closest,
        "competitive_advantages": competitor_gaps,
        "market_ranking": sorted(
            competitors + [your_company],
            key=lambda x: x.get("market_share", 0),
            reverse=True,
        ),
    }


def identify_opportunities(
    competitors: List[Dict], market_gaps: List[str]
) -> List[Dict]:
    """Identify market opportunities"""
    opportunities = []

    # Analyze competitor weaknesses
    for comp in competitors:
        for weakness in comp.get("weaknesses", []):
            opportunities.append(
                {
                    "type": "competitor_weakness",
                    "description": f"Exploit {comp['name']}'s weakness: {weakness}",
                    "competitor": comp["name"],
                    "potential_impact": "high",
                }
            )

    # Analyze market gaps
    for gap in market_gaps:
        opportunities.append(
            {
                "type": "market_gap",
                "description": f"Address unmet need: {gap}",
                "potential_impact": "high",
            }
        )

    return opportunities[:5]


def competitive_landscape_analyzer(
    competitor_data: List[Dict],
    your_company: Dict,
    market_gaps: List[str] | None = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Analyze competitive landscape and identify positioning.

    Args:
        competitor_data: List of competitor information
        your_company: Your company's data
        market_gaps: Known market gaps
        **kwargs: Additional parameters

    Returns:
        Competitive analysis results
    """
    if not competitor_data:
        return {"status": "error", "error": "No competitor data provided"}

    market_gaps = market_gaps or []

    competitors = parse_competitors(competitor_data)
    position_analysis = analyze_market_position(competitors, your_company)
    opportunities = identify_opportunities(competitors, market_gaps)

    return {
        "status": "success",
        "competitors_analyzed": len(competitors),
        "market_position": position_analysis,
        "opportunities": opportunities,
        "recommendations": [
            f"Leverage advantages over {opp['competitor']}"
            for opp in opportunities[:2]
            if opp.get("competitor")
        ],
    }


async def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "analyze")
    competitor_data = payload.get("competitor_data", [])
    your_company = payload.get("your_company", {})
    market_gaps = payload.get("market_gaps", [])

    if action == "analyze":
        result = competitive_landscape_analyzer(
            competitor_data, your_company, market_gaps
        )
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
            "name": "competitive-landscape-analyzer",
            "description": "Analyze competitive landscape and identify market positioning",
            "version": "1.0.0",
            "domain": "STRATEGY",
        }