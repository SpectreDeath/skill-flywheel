"""
SHAP-IQ Interaction Extraction

Skill: shapiq-interaction-extraction
Domain: generated_skills
Description: Extracts structured data from SHAP-IQ InteractionValues.
Converts raw dict mapping tuples to floats into Pandas-style structures.

Actions:
- extract_main_effects: Get main (first-order) effects from a dict {(i,): value}
- extract_pair_matrix: Get symmetric NxN matrix from {(i,j): value} pairs
- get_top_interactions: Sort and return top-K interaction pairs
- compute_interaction_stats: Compute mean, max, sum of absolute interactions
"""

from datetime import datetime
from typing import Any, Dict, List, Tuple

import numpy as np


def extract_main_effects(
    interactions: Dict[Tuple[int, ...], float],
) -> Dict[int, float]:
    """Extract main (first-order) effects from interaction dict where keys are (i,)."""
    main_effects = {}
    for key, value in interactions.items():
        if len(key) == 1:
            main_effects[key[0]] = value
    return main_effects


def extract_pair_matrix(
    interactions: Dict[Tuple[int, ...], float],
    n_features: int,
) -> np.ndarray:
    """Build symmetric NxN matrix from {(i,j): value} second-order pairs."""
    matrix = np.zeros((n_features, n_features))
    for key, value in interactions.items():
        if len(key) == 2:
            i, j = key
            matrix[i][j] = value
            matrix[j][i] = value
    return matrix


def get_top_interactions(
    interactions: Dict[Tuple[int, ...], float],
    k: int = 10,
) -> List[Dict[str, Any]]:
    """Sort interactions by absolute value and return top-K pairs."""
    pairs = []
    for key, value in interactions.items():
        if len(key) == 2:
            pairs.append({"pair": list(key), "value": value, "abs_value": abs(value)})
    pairs.sort(key=lambda x: x["abs_value"], reverse=True)
    return pairs[:k]


def compute_interaction_stats(
    interactions: Dict[Tuple[int, ...], float],
) -> Dict[str, float]:
    """Compute mean, max, and sum of absolute interaction values (second-order only)."""
    values = [v for k, v in interactions.items() if len(k) == 2]
    if not values:
        return {"mean_abs": 0.0, "max_abs": 0.0, "sum_abs": 0.0, "count": 0}
    abs_values = [abs(v) for v in values]
    return {
        "mean_abs": float(np.mean(abs_values)),
        "max_abs": float(np.max(abs_values)),
        "sum_abs": float(np.sum(abs_values)),
        "count": len(values),
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Entry point for shapiq-interaction-extraction skill."""
    action = payload.get("action", "extract_main_effects")
    raw = payload.get("interactions", {})
    interactions = {tuple(k) if isinstance(k, list) else k: v for k, v in raw.items()}

    if action == "extract_main_effects":
        result = extract_main_effects(interactions)
    elif action == "extract_pair_matrix":
        n = payload.get("n_features", 0)
        matrix = extract_pair_matrix(interactions, n)
        result = {"matrix": matrix.tolist()}
    elif action == "get_top_interactions":
        k = payload.get("k", 10)
        result = {"top_interactions": get_top_interactions(interactions, k)}
    elif action == "compute_interaction_stats":
        result = compute_interaction_stats(interactions)
    else:
        result = {"error": f"Unknown action: {action}"}

    return {
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }


singleton = "shapiq-interaction-extraction"

if __name__ == "__main__":
    import asyncio

    sample = {
        (0, 1): 0.12,
        (0, 2): -0.05,
        (1, 2): 0.33,
        (0,): 0.7,
        (1,): -0.2,
        (2,): 0.4,
    }
    print(
        asyncio.run(invoke({"action": "extract_main_effects", "interactions": sample}))
    )
    print(
        asyncio.run(
            invoke(
                {
                    "action": "extract_pair_matrix",
                    "interactions": sample,
                    "n_features": 3,
                }
            )
        )
    )
    print(
        asyncio.run(
            invoke({"action": "get_top_interactions", "interactions": sample, "k": 2})
        )
    )
    print(
        asyncio.run(
            invoke({"action": "compute_interaction_stats", "interactions": sample})
        )
    )
