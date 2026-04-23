"
Strategic Decision Matrix

Evaluates strategic options using multi-criteria decision analysis:
- Weighted decision matrices
- Pros/cons analysis
- Risk/reward scoring
- Recommendation generation
"

from typing import Any, Dict, List
from datetime import datetime


def calculate_weighted_score(option: Dict, criteria: List[Dict]) -> float:
    "Calculate weighted score for an option"
    total_score = 0
    total_weight = 0

    for criterion in criteria:
        weight = criterion.get("weight", 1)
        criterion_name = criterion.get("name", ")

        # Get score for this criterion
        score = option.get("scores", {}).get(criterion_name, 5)

        total_score += score * weight
        total_weight += weight

    return total_score / total_weight if total_weight > 0 else 0


def analyze_risk_reward(option: Dict) -> Dict[str, Any]:
    "Analyze risk/reward for an option"
    risks = option.get("risks", [])
    rewards = option.get("rewards", [])

    # Calculate risk score (0-10)
    risk_score = min(10, len(risks) * 2)

    # Calculate reward score (0-10)
    reward_score = min(10, len(rewards) * 2 + option.get("potential_impact", 5))

    # Determine ratio
    ratio = reward_score / risk_score if risk_score > 0 else reward_score

    return {
        "risk_score": risk_score,
        "reward_score": reward_score,
        "ratio": round(ratio, 2),
        "assessment": "favorable"
        if ratio > 1.5
        else "risky"
        if ratio < 0.8
        else "balanced",
    }


def strategic_decision_matrix(
    options: List[Dict], criteria: List[Dict], **kwargs
) -> Dict[str, Any]:
    "
    Evaluate strategic options using decision matrix.

    Args:
        options: List of strategic options to evaluate
        criteria: List of evaluation criteria with weights
        **kwargs: Additional parameters

    Returns:
        Decision matrix analysis with recommendations
    "
    if not options:
        return {"status": "error", "error": "No options provided"}

    if not criteria:
        criteria = [{"name": "default", "weight": 1}]

    results = []

    for option in options:
        weighted_score = calculate_weighted_score(option, criteria)
        risk_analysis = analyze_risk_reward(option)

        results.append(
            {
                "option": option.get("name", "Unnamed"),
                "weighted_score": round(weighted_score, 2),
                "risk_analysis": risk_analysis,
                "pros": option.get("pros", []),
                "cons": option.get("cons", []),
            }
        )

    # Sort by weighted score
    results.sort(key=lambda x: x["weighted_score"], reverse=True)

    # Generate recommendation
    best = results[0] if results else None
    recommendation = "
    if best:
        if best["risk_analysis"]["assessment"] == "favorable":
            recommendation = f"Strong recommendation: {best['option']}"
        elif best["risk_analysis"]["assessment"] == "risky":
            recommendation = f"Caution: {best['option']} has high risk"
        else:
            recommendation = f"Recommended with monitoring: {best['option']}"

    return {
        "status": "success",
        "options_analyzed": len(options),
        "criteria_used": len(criteria),
        "rankings": results,
        "best_option": best["option"] if best else None,
        "recommendation": recommendation,
    }


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    action = payload.get("action", "evaluate")
    options = payload.get("options", [])
    criteria = payload.get("criteria", [])

    if action == "evaluate":
        result = strategic_decision_matrix(options, criteria)
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
    "Return skill metadata"
    return {
        "name": "strategic-decision-matrix",
        "description": "Evaluate strategic options using decision matrices",
        "version": "1.0.0",
        "domain": "STRATEGY",
    }
