"""
SHAP-IQ Explainability Pipeline

Domain: generated_skills
Description: Setup pattern for SHAP-IQ explainability. Provides utilities for
configuring explainers, extracting interaction values, and running mock
explanations on feature data.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

VALID_INDICES = ("k-SII", "SII", "STII", "FSII", "BZF")


class ExplainerConfig:
    def __init__(
        self,
        index_type: str = "k-SII",
        max_order: int = 2,
        budget: int = 2000,
        random_state: int = 42,
    ):
        if index_type not in VALID_INDICES:
            raise ValueError(f"index_type must be one of {VALID_INDICES}")
        if max_order < 1:
            raise ValueError("max_order must be >= 1")
        self.index_type = index_type
        self.max_order = max_order
        self.budget = budget
        self.random_state = random_state

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index_type": self.index_type,
            "max_order": self.max_order,
            "budget": self.budget,
            "random_state": self.random_state,
        }


def extract_main_effects(
    interaction_values: Dict[str, float], n_features: int = 0
) -> Dict[str, float]:
    main = {}
    for key, val in interaction_values.items():
        parts = key.split("_")
        if len(parts) == 1:
            main[key] = val
    return dict(sorted(main.items(), key=lambda x: -abs(x[1])))


def extract_pair_matrix(
    interaction_values: Dict[str, float], n_features: int = 5
) -> List[List[float]]:
    matrix = [[0.0] * n_features for _ in range(n_features)]
    for key, val in interaction_values.items():
        parts = key.split("_")
        if len(parts) == 2:
            try:
                i, j = int(parts[0]), int(parts[1])
                if 0 <= i < n_features and 0 <= j < n_features:
                    matrix[i][j] = val
                    matrix[j][i] = val
            except ValueError:
                continue
    return matrix


def explain_sample(
    features: Dict[str, float],
    config: Optional[ExplainerConfig] = None,
) -> Dict[str, Any]:
    cfg = config or ExplainerConfig()
    sorted_feats = sorted(features.items(), key=lambda x: -abs(x[1]))
    main_effects = {k: round(v, 6) for k, v in sorted_feats}
    pairs: Dict[str, float] = {}
    names = list(features.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            val = round(features[names[i]] * features[names[j]] * 0.1, 6)
            pairs[f"{names[i]}_{names[j]}"] = val
    return {
        "index_type": cfg.index_type,
        "main_effects": main_effects,
        "interactions": dict(sorted(pairs.items(), key=lambda x: -abs(x[1]))),
        "top_feature": sorted_feats[0][0] if sorted_feats else None,
        "feature_count": len(features),
    }


_config = ExplainerConfig()


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    global _config
    action = payload.get("action", "get_config")

    if action == "configure":
        _config = ExplainerConfig(
            index_type=payload.get("index_type", "k-SII"),
            max_order=payload.get("max_order", 2),
            budget=payload.get("budget", 2000),
            random_state=payload.get("random_state", 42),
        )
        result = _config.to_dict()
    elif action == "extract_main_effects":
        result = extract_main_effects(
            interaction_values=payload["interaction_values"],
            n_features=payload.get("n_features", 0),
        )
    elif action == "extract_pair_matrix":
        result = extract_pair_matrix(
            interaction_values=payload["interaction_values"],
            n_features=payload.get("n_features", 5),
        )
    elif action == "explain_sample":
        result = explain_sample(
            features=payload["features"],
            config=_config,
        )
    elif action == "get_config":
        result = _config.to_dict()
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

    async def demo():
        print(
            await invoke({"action": "configure", "index_type": "SII", "max_order": 3})
        )
        print(
            await invoke(
                {
                    "action": "explain_sample",
                    "features": {"age": 0.45, "income": 0.72, "score": -0.3},
                }
            )
        )
        print(await invoke({"action": "get_config"}))

    asyncio.run(demo())
