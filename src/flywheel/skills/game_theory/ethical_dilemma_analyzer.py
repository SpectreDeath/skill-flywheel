"
Ethical Dilemma Analyzer

Analyzes ethical dilemmas and applies moral frameworks:
- Utilitarianism, Deontology, Virtue Ethics
- Provides multi-perspective analysis
- Identifies stakeholders and impacts
"

from typing import Any, Dict, List
from datetime import datetime

MORAL_FRAMEWORKS = {
    "utilitarianism": {
        "principle": "Maximize overall happiness/wellbeing",
        "question": "What action produces the greatest good for the greatest number?",
        "focus": "Outcomes and consequences",
    },
    "deontology": {
        "principle": "Follow moral rules and duties",
        "question": "Is this action respecting universal moral laws?",
        "focus": "Duties and rights",
    },
    "virtue_ethics": {
        "principle": "Cultivate good character traits",
        "question": "What would a virtuous person do?",
        "focus": "Character and virtues",
    },
    "care_ethics": {
        "principle": "Maintain relationships and care",
        "question": "How does this action affect those we care for?",
        "focus": "Relationships and context",
    },
    "rights_based": {
        "principle": "Respect individual rights",
        "question": "Does this action violate any fundamental rights?",
        "focus": "Individual freedoms",
    },
    "contractarianism": {
        "principle": "Fairness through mutual agreement",
        "question": "Would rational parties agree to this?",
        "focus": "Social contract",
    },
}


def identify_stakeholders(scenario: str) -> List[Dict[str, Any]]:
    "Identify stakeholders in the ethical dilemma"
    stakeholders = []

    # Common stakeholder patterns
    common = [
        "people",
        "individuals",
        "employees",
        "customers",
        "society",
        "family",
        "community",
        "company",
        "organization",
        "environment",
    ]

    scenario_lower = scenario.lower()
    for stakeholder in common:
        if stakeholder in scenario_lower:
            stakeholders.append(
                {
                    "type": stakeholder,
                    "impact": "potential",
                    "description": f"Those affected by {stakeholder}",
                }
            )

    return stakeholders[:5]


def analyze_from_framework(
    framework: str, scenario: str, stakeholders: List[Dict]
) -> Dict[str, Any]:
    "Analyze dilemma from a specific moral framework"

    if framework not in MORAL_FRAMEWORKS:
        return {"error": f"Unknown framework: {framework}"}

    principles = MORAL_FRAMEWORKS[framework]

    # Generate analysis based on framework
    analysis = {
        "framework": framework,
        "principle": principles["principle"],
        "key_question": principles["question"],
        "perspective": principles["focus"],
        "analysis": ",
        "recommendation": ",
        "strengths": [],
        "weaknesses": [],
    }

    # Framework-specific analysis
    if framework == "utilitarianism":
        analysis["analysis"] = (
            f"From a utilitarian perspective, evaluate the net consequences for all {len(stakeholders)} stakeholder groups."
        )
        analysis["recommendation"] = (
            "Choose the action that maximizes overall wellbeing"
        )
        analysis["strengths"] = [
            "Considers all affected parties",
            "Focuses on outcomes",
        ]
        analysis["weaknesses"] = [
            "May justify harming minorities",
            "Difficult to measure happiness",
        ]

    elif framework == "deontology":
        analysis["analysis"] = (
            "From a deontological perspective, determine if the action respects moral duties and rights."
        )
        analysis["recommendation"] = (
            "Choose the action that respects universal moral principles"
        )
        analysis["strengths"] = ["Respects individual rights", "Provides clear rules"]
        analysis["weaknesses"] = [
            "May produce suboptimal outcomes",
            "Rules can conflict",
        ]

    elif framework == "virtue_ethics":
        analysis["analysis"] = (
            "From a virtue ethics perspective, consider what a virtuous person would do."
        )
        analysis["recommendation"] = (
            "Cultivate and demonstrate virtues like honesty, courage, compassion"
        )
        analysis["strengths"] = ["Emphasizes character", "Flexible to context"]
        analysis["weaknesses"] = ["Subjective", "No clear decision procedure"]

    return analysis


def ethical_dilemma_analyzer(
    scenario: str, frameworks: List[str] | None = None, **kwargs
) -> Dict[str, Any]:
    "
    Analyze ethical dilemmas using multiple moral frameworks.

    Args:
        scenario: Description of the ethical dilemma
        frameworks: List of frameworks to apply (default: all)
        **kwargs: Additional parameters

    Returns:
        Multi-perspective ethical analysis
    "
    if not scenario:
        return {"status": "error", "error": "No scenario provided"}

    frameworks = frameworks or list(MORAL_FRAMEWORKS.keys())
    stakeholders = identify_stakeholders(scenario)

    # Analyze from each framework
    analyses = []
    for framework in frameworks:
        if framework in MORAL_FRAMEWORKS:
            analysis = analyze_from_framework(framework, scenario, stakeholders)
            analyses.append(analysis)

    # Synthesize conclusions
    recommendations = [a.get("recommendation", ") for a in analyses]

    return {
        "status": "success",
        "scenario": scenario[:200] + "..." if len(scenario) > 200 else scenario,
        "stakeholders": stakeholders,
        "frameworks_analyzed": frameworks,
        "analyses": analyses,
        "summary": {
            "frameworks_count": len(analyses),
            "recommendations": recommendations,
            "note": "Different frameworks may suggest different actions - consider all perspectives",
        },
    }


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    action = payload.get("action", "analyze")
    scenario = payload.get("scenario", ")
    frameworks = payload.get("frameworks")

    if action == "analyze":
        result = ethical_dilemma_analyzer(scenario, frameworks)
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
        "name": "ethical-dilemma-analyzer",
        "description": "Analyze ethical dilemmas using moral frameworks",
        "version": "1.0.0",
        "domain": "PHILOSOPHY",
    }
