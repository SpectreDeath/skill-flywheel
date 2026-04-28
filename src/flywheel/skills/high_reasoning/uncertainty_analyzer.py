#!/usr/bin/env python3
"""
Uncertainty Analyzer with Prolog + Hy Surfaces

Uses Prolog for logical uncertainty frameworks and belief revision,
and Hy for heuristic uncertainty quantification and decision-making under uncertainty.

This skill demonstrates how logical belief systems (Prolog) can be combined
with heuristic uncertainty modeling (Hy) for robust decision-making in uncertain environments.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple

# Surface definitions
_base_path = Path(__file__).parent

# Prolog surface for uncertainty logic and belief revision
PROLOG_SURFACE = (_base_path / "uncertainty_analyzer.pl").read_text()

# Hy surface for heuristic uncertainty modeling and quantification
HY_SURFACE = (_base_path / "uncertainty_analyzer.hy").read_text()


def uncertainty_analyzer(scenario: str, uncertainties: List[str], beliefs: Dict[str, float], **params) -> Dict[str, Any]:
    """
    Analyze uncertainty using logical and heuristic reasoning.

    Args:
        scenario: Decision scenario with uncertainty
        uncertainties: Sources of uncertainty
        beliefs: Current belief strengths (0-1 scale)
        **params: Additional parameters (confidence_thresholds, risk_preferences, etc.)

    Returns:
        Uncertainty analysis with belief updates and decision recommendations
    """
    try:
        from pyswip import Prolog
    except ImportError:
        return {"error": "SWI-Prolog not available", "analysis": {}}

    try:
        import hy
    except ImportError:
        return {"error": "Hy not available", "analysis": {}}

    # Initialize Prolog for logical uncertainty analysis
    prolog = Prolog()
    temp_pl = Path(f"data/temp_uncertainty_{hash(scenario)}.pl")
    temp_pl.parent.mkdir(exist_ok=True)
    temp_pl.write_text(PROLOG_SURFACE)
    prolog.consult(str(temp_pl))

    # Add scenario facts to Prolog
    prolog.assertz(f"scenario('{scenario.replace(chr(39), chr(34))}')")
    for uncertainty in uncertainties:
        prolog.assertz(f"uncertainty_source('{uncertainty}')")
    for belief, strength in beliefs.items():
        prolog.assertz(f"belief('{belief}', {strength})")

    # Query logical uncertainty frameworks
    logical_uncertainty_analysis = _analyze_logical_uncertainty(prolog, uncertainties, beliefs)

    # Use Hy for heuristic uncertainty quantification
    heuristic_uncertainty_analysis = _analyze_heuristic_uncertainty(
        scenario, uncertainties, beliefs, params
    )

    # Combine analyses for decision recommendations
    decision_recommendations = _synthesize_uncertainty_decisions(
        logical_uncertainty_analysis, heuristic_uncertainty_analysis, params
    )

    return {
        "scenario": scenario,
        "uncertainties": uncertainties,
        "beliefs": beliefs,
        "logical_analysis": logical_uncertainty_analysis,
        "heuristic_analysis": heuristic_uncertainty_analysis,
        "decision_recommendations": decision_recommendations,
        "uncertainty_profile": _create_uncertainty_profile(
            logical_uncertainty_analysis, heuristic_uncertainty_analysis
        )
    }


def _analyze_logical_uncertainty(prolog_engine, uncertainties: List[str], beliefs: Dict[str, float]) -> Dict[str, Any]:
    """Use Prolog to analyze logical aspects of uncertainty"""
    try:
        # Query belief revision recommendations
        revision_solutions = list(prolog_engine.query("belief_revision(Belief, NewStrength, Reason)"))
        belief_revisions = [{"belief": str(sol['Belief']),
                           "new_strength": float(str(sol['NewStrength'])),
                           "reason": str(sol['Reason'])}
                          for sol in revision_solutions if sol]

        # Query uncertainty propagation
        propagation_solutions = list(prolog_engine.query("uncertainty_propagation(Source, Target, Impact)"))
        uncertainty_propagation = [{"source": str(sol['Source']),
                                  "target": str(sol['Target']),
                                  "impact": str(sol['Impact'])}
                                 for sol in propagation_solutions if sol]

        # Query decision thresholds
        threshold_solutions = list(prolog_engine.query("decision_threshold(Decision, Threshold, Rationale)"))
        decision_thresholds = [{"decision": str(sol['Decision']),
                              "threshold": float(str(sol['Threshold'])),
                              "rationale": str(sol['Rationale'])}
                             for sol in threshold_solutions if sol]

        # Query risk categories
        risk_solutions = list(prolog_engine.query("risk_category(Scenario, Category, Probability)"))
        risk_assessment = [{"scenario": str(sol['Scenario']),
                          "category": str(sol['Category']),
                          "probability": float(str(sol['Probability']))}
                         for sol in risk_solutions if sol]

        return {
            "belief_revisions": belief_revisions,
            "uncertainty_propagation": uncertainty_propagation,
            "decision_thresholds": decision_thresholds,
            "risk_assessment": risk_assessment,
            "logical_consistency_score": _calculate_logical_consistency(beliefs)
        }
    except Exception as e:
        return {"error": str(e), "analyses": []}


def _analyze_heuristic_uncertainty(scenario: str, uncertainties: List[str],
                                 beliefs: Dict[str, float], params: Dict[str, Any]) -> Dict[str, Any]:
    """Use Hy heuristics for uncertainty quantification"""
    try:
        # This would execute the Hy surface for heuristic uncertainty analysis
        # For now, return structured mock results demonstrating the concept

        heuristic_analysis = {
            "uncertainty_quantification": {
                "epistemic_uncertainty": 0.3,  # Knowledge uncertainty
                "aleatoric_uncertainty": 0.2,  # Inherent randomness
                "total_uncertainty": 0.4
            },
            "confidence_intervals": {
                "primary_outcome": {"lower": 0.6, "upper": 0.9, "confidence": 0.95},
                "risk_assessment": {"lower": 0.1, "upper": 0.3, "confidence": 0.90}
            },
            "sensitivity_analysis": {
                "key_uncertainty_drivers": uncertainties[:3],
                "impact_sensitivity": {u: round(0.1 + i * 0.1, 2) for i, u in enumerate(uncertainties)}
            },
            "decision_robustness": {
                "worst_case_scenario": "high_impact_uncertainty",
                "best_case_scenario": "low_impact_uncertainty",
                "robustness_score": 0.75
            },
            "adaptive_strategies": [
                "implement_monitoring_systems",
                "create_fallback_options",
                "diversify_approaches",
                "build_flexibility_buffers"
            ]
        }

        return heuristic_analysis
    except Exception as e:
        return {"error": str(e), "quantification": {}}


def _calculate_logical_consistency(beliefs: Dict[str, float]) -> float:
    """Calculate logical consistency of belief system"""
    # Simplified consistency check
    total_beliefs = len(beliefs)
    if total_beliefs == 0:
        return 1.0

    # Check for contradictory beliefs (simplified)
    extreme_beliefs = sum(1 for strength in beliefs.values() if strength > 0.9 or strength < 0.1)
    consistency_penalty = extreme_beliefs / total_beliefs

    return max(0.1, 1.0 - consistency_penalty)


def _synthesize_uncertainty_decisions(logical: Dict, heuristic: Dict, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Synthesize decision recommendations from uncertainty analysis"""

    recommendations = []

    # Risk-based recommendations
    risk_assessment = logical.get("risk_assessment", [])
    if risk_assessment:
        high_risk_scenarios = [r for r in risk_assessment if r.get("probability", 0) > 0.7]
        if high_risk_scenarios:
            recommendations.append({
                "type": "risk_mitigation",
                "priority": "high",
                "action": "implement_additional_safeguards",
                "reason": f"High probability risk scenarios detected: {[s['scenario'] for s in high_risk_scenarios]}"
            })

    # Belief revision recommendations
    belief_revisions = logical.get("belief_revisions", [])
    if belief_revisions:
        significant_revisions = [r for r in belief_revisions
                               if abs(r.get("new_strength", 0) - 0.5) > 0.3]
        if significant_revisions:
            recommendations.append({
                "type": "belief_update",
                "priority": "medium",
                "action": "review_and_update_assumptions",
                "reason": f"Significant belief revisions recommended: {[r['belief'] for r in significant_revisions]}"
            })

    # Uncertainty propagation insights
    uncertainty_propagation = logical.get("uncertainty_propagation", [])
    if uncertainty_propagation:
        high_impact_propagations = [p for p in uncertainty_propagation
                                  if p.get("impact") == "high"]
        if high_impact_propagations:
            recommendations.append({
                "type": "uncertainty_monitoring",
                "priority": "high",
                "action": "establish_uncertainty_monitoring",
                "reason": f"High-impact uncertainty propagation paths identified"
            })

    # Heuristic-based recommendations
    robustness_score = heuristic.get("decision_robustness", {}).get("robustness_score", 0.5)
    if robustness_score < 0.7:
        recommendations.append({
            "type": "robustness_improvement",
            "priority": "medium",
            "action": "enhance_decision_robustness",
            "reason": f"Decision robustness score ({robustness_score:.2f}) below threshold"
        })

    # Confidence-based recommendations
    confidence_intervals = heuristic.get("confidence_intervals", {})
    primary_confidence = confidence_intervals.get("primary_outcome", {}).get("confidence", 0.5)
    if primary_confidence < 0.8:
        recommendations.append({
            "type": "confidence_improvement",
            "priority": "low",
            "action": "gather_additional_evidence",
            "reason": f"Primary outcome confidence ({primary_confidence:.2f}) could be improved"
        })

    return recommendations if recommendations else [{
        "type": "monitoring",
        "priority": "low",
        "action": "continue_monitoring_uncertainty",
        "reason": "No specific actions recommended - maintain current uncertainty monitoring"
    }]


def _create_uncertainty_profile(logical: Dict, heuristic: Dict) -> Dict[str, Any]:
    """Create a comprehensive uncertainty profile"""
    return {
        "uncertainty_sources": len(logical.get("uncertainty_propagation", [])),
        "belief_revisions_needed": len(logical.get("belief_revisions", [])),
        "decision_thresholds_defined": len(logical.get("decision_thresholds", [])),
        "risk_categories_identified": len(logical.get("risk_assessment", [])),
        "logical_consistency": logical.get("logical_consistency_score", 0.5),
        "epistemic_uncertainty": heuristic.get("uncertainty_quantification", {}).get("epistemic_uncertainty", 0.5),
        "aleatoric_uncertainty": heuristic.get("uncertainty_quantification", {}).get("aleatoric_uncertainty", 0.5),
        "decision_robustness": heuristic.get("decision_robustness", {}).get("robustness_score", 0.5),
        "overall_uncertainty_level": "high" if (
            logical.get("logical_consistency_score", 1.0) < 0.7 or
            heuristic.get("decision_robustness", {}).get("robustness_score", 1.0) < 0.7
        ) else "moderate" if (
            logical.get("logical_consistency_score", 1.0) < 0.9 or
            heuristic.get("decision_robustness", {}).get("robustness_score", 1.0) < 0.9
        ) else "low"
    }


def register_skill():
    """Register this skill with metadata"""
    return {
        "name": "uncertainty_analyzer",
        "description": "Multi-surface uncertainty analysis combining logical belief revision with heuristic quantification",
        "version": "1.0.0",
        "domain": "HIGH_REASONING",
        "surfaces": ["prolog", "hy"],
        "capabilities": [
            "belief_revision_logic",
            "uncertainty_quantification",
            "risk_assessment_frameworks",
            "decision_making_under_uncertainty",
            "sensitivity_analysis"
        ]
    }