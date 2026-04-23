"""
Uncertainty Quantification

Calculates confidence levels and uncertainty from evidence:
- Bayesian probability updates
- Evidence weighting
- Confidence intervals
"""

import math
from typing import Any, Dict, List
from datetime import datetime


def bayesian_update(prior: float, likelihood: float, evidence: float) -> float:
    "Perform Bayesian update on probability"
    if evidence == 0:
        return prior

    posterior = (likelihood * prior) / evidence
    return min(1.0, max(0.0, posterior))


def calculate_confidence_from_evidence(
    evidence: List[Dict[str, Any]],
) -> Dict[str, Any]:
    "
    Calculate confidence from multiple evidence items.

    Each evidence item should have:
    - strength: 0-1 (how strong the evidence is)
    - reliability: 0-1 (how reliable the source is)
    - relevance: 0-1 (how relevant to the question)
    "
    if not evidence:
        return {
            "status": "success",
            "confidence": 0.0,
            "uncertainty": 1.0,
            "evidence_count": 0,
            "method": "no_evidence",
        }

    # Weighted average of evidence strength
    total_weight = 0
    weighted_sum = 0

    for item in evidence:
        strength = item.get("strength", 0.5)
        reliability = item.get("reliability", 0.5)
        relevance = item.get("relevance", 0.5)

        weight = reliability * relevance
        weighted_sum += strength * weight
        total_weight += weight

    base_confidence = weighted_sum / total_weight if total_weight > 0 else 0.5

    # Adjust for evidence count
    count_factor = min(1.0, len(evidence) / 10.0)  # Diminishing returns after 10

    # Bayesian adjustment with evidence count
    prior = 0.5
    likelihood = base_confidence
    evidence_strength = count_factor

    final_confidence = bayesian_update(prior, likelihood, evidence_strength)

    return {
        "status": "success",
        "confidence": round(final_confidence, 3),
        "uncertainty": round(1.0 - final_confidence, 3),
        "evidence_count": len(evidence),
        "base_confidence": round(base_confidence, 3),
        "count_factor": round(count_factor, 3),
        "method": "bayesian_weighted",
    }


def calculate_confidence_interval(
    n_successes: int, n_trials: int, confidence: float = 0.95
) -> Dict[str, Any]:
    "Calculate confidence interval for binomial proportion"
    if n_trials == 0:
        return {"error": "No trials"}

    p_hat = n_successes / n_trials

    # Wilson score interval (more accurate for small samples)
    z = 1.96 if confidence == 0.95 else 2.576  # 95% or 99%

    denominator = 1 + z**2 / n_trials
    center = p_hat + z**2 / (2 * n_trials)
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z**2 / (4 * n_trials)) / n_trials)

    lower = max(0, (center - spread) / denominator)
    upper = min(1, (center + spread) / denominator)

    return {
        "proportion": round(p_hat, 3),
        "confidence_level": confidence,
        "lower_bound": round(lower, 3),
        "upper_bound": round(upper, 3),
        "interval_width": round(upper - lower, 3),
    }


def uncertainty_quantifier(
    evidence: List[Dict] | None = None,
    n_successes: int = 0,
    n_trials: int = 0,
    method: str = "evidence",
    **kwargs,
) -> Dict[str, Any]:
    "
    Quantify uncertainty from evidence or trial data.

    Args:
        evidence: List of evidence items with strength, reliability, relevance
        n_successes: Number of successful trials (for binomial)
        n_trials: Total number of trials
        method: Calculation method ("evidence" or "binomial")
        **kwargs: Additional parameters

    Returns:
        Uncertainty quantification results
    "
    if method == "evidence" or (evidence and method != "binomial"):
        if not evidence:
            evidence = []
        return calculate_confidence_from_evidence(evidence)

    elif method == "binomial":
        confidence = kwargs.get("confidence", 0.95)
        result = calculate_confidence_interval(n_successes, n_trials, confidence)
        result["uncertainty"] = result.get("interval_width", 0)
        result["method"] = "binomial"
        return result

    else:
        return {"status": "error", "error": f"Unknown method: {method}"}


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    action = payload.get("action", "quantify")
    evidence = payload.get("evidence")
    n_successes = payload.get("n_successes", 0)
    n_trials = payload.get("n_trials", 0)
    method = payload.get("method", "evidence")

    if action == "quantify":
        result = uncertainty_quantifier(evidence, n_successes, n_trials, method)
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
    """ Return skill metadata """

if __name__ == "__main__":
    return {
            "name": "uncertainty-quantifier",
            "description": "Quantify uncertainty and calculate confidence levels from evidence",
            "version": "1.0.0",
            "domain": "EPISTEMOLOGY",
        }