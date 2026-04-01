"""
Global Feature Importance

Skill: global-feature-importance
Domain: generated_skills
Description: Aggregates local SHAP-IQ explanations across multiple samples
for global importance.

Actions:
- aggregate: Accumulate main effects and pair matrices across N samples
- get_global_ranking: Return sorted global feature importance
- get_global_interactions: Return global interaction submatrix for top-K features
- reset: Clear accumulated data
"""

from datetime import datetime
from typing import Any, Dict, List

import numpy as np


class GlobalFeatureImportance:
    """Accumulates local explanations into global feature importance."""

    def __init__(self) -> None:
        self.main_effects_sum: np.ndarray = np.zeros(0)
        self.pair_matrix_sum: np.ndarray = np.zeros((0, 0))
        self.n_samples: int = 0

    def aggregate(
        self, main_effects: List[float], pair_matrix: List[List[float]]
    ) -> Dict[str, int]:
        """Accumulate one sample's main effects and pair matrix."""
        me = np.array(main_effects, dtype=float)
        pm = np.array(pair_matrix, dtype=float)

        if self.n_samples == 0:
            self.main_effects_sum = me.copy()
            self.pair_matrix_sum = pm.copy()
        else:
            n_me = min(len(self.main_effects_sum), len(me))
            n_pm = min(self.pair_matrix_sum.shape[0], pm.shape[0])
            self.main_effects_sum[:n_me] += me[:n_me]
            self.pair_matrix_sum[:n_pm, :n_pm] += pm[:n_pm, :n_pm]

        self.n_samples += 1
        return {"samples_aggregated": self.n_samples}

    def get_global_ranking(self) -> List[Dict[str, Any]]:
        """Return features sorted by absolute global main effect."""
        if self.n_samples == 0:
            return []
        means = self.main_effects_sum / self.n_samples
        ranking = [
            {
                "index": i,
                "mean_effect": float(means[i]),
                "abs_effect": float(abs(means[i])),
            }
            for i in range(len(means))
        ]
        ranking.sort(key=lambda x: x["abs_effect"], reverse=True)
        return ranking

    def get_global_interactions(self, k: int = 5) -> Dict[str, Any]:
        """Return submatrix of top-K features by global interaction magnitude."""
        if self.n_samples == 0:
            return {"indices": [], "submatrix": []}
        means = self.pair_matrix_sum / self.n_samples
        abs_means = np.abs(means)
        np.fill_diagonal(abs_means, 0)
        sums = abs_means.sum(axis=1)
        top_k = np.argsort(sums)[-k:][::-1].tolist()
        submatrix = means[np.ix_(top_k, top_k)].tolist()
        return {"indices": top_k, "submatrix": submatrix}

    def reset(self) -> Dict[str, int]:
        """Clear all accumulated data."""
        self.main_effects_sum = np.zeros(0)
        self.pair_matrix_sum = np.zeros((0, 0))
        prev = self.n_samples
        self.n_samples = 0
        return {"cleared_samples": prev}


_instance = GlobalFeatureImportance()


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Entry point for global-feature-importance skill."""
    action = payload.get("action", "get_global_ranking")

    if action == "aggregate":
        result = _instance.aggregate(
            payload.get("main_effects", []),
            payload.get("pair_matrix", []),
        )
    elif action == "get_global_ranking":
        result = {"ranking": _instance.get_global_ranking()}
    elif action == "get_global_interactions":
        result = _instance.get_global_interactions(payload.get("k", 5))
    elif action == "reset":
        result = _instance.reset()
    else:
        result = {"error": f"Unknown action: {action}"}

    return {
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }


if __name__ == "__main__":
    import asyncio

    asyncio.run(invoke({"action": "reset"}))
    for _ in range(3):
        asyncio.run(
            invoke(
                {
                    "action": "aggregate",
                    "main_effects": [0.5, -0.3, 0.1],
                    "pair_matrix": [[0, 0.2, -0.1], [0.2, 0, 0.05], [-0.1, 0.05, 0]],
                }
            )
        )
    print(asyncio.run(invoke({"action": "get_global_ranking"})))
    print(asyncio.run(invoke({"action": "get_global_interactions", "k": 2})))
