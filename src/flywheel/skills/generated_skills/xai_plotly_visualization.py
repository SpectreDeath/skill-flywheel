"""
XAI Plotly Visualization

Domain: generated_skills
Description: Creates visualization specs (as JSON-serializable dicts) for feature
importance bars, interaction heatmaps, and waterfall plots. Returns Plotly-compatible
figure specifications without requiring plotly to be installed.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


def feature_bar_chart(
    features: List[str],
    importance: List[float],
    title: str = "Feature Importance",
    orientation: str = "h",
) -> Dict[str, Any]:
    sorted_pairs = sorted(zip(features, importance), key=lambda x: abs(x[1]))
    sf, si = zip(*sorted_pairs) if sorted_pairs else ([], [])
    return {
        "data": [
            {
                "type": "bar",
                "x": list(si),
                "y": list(sf),
                "orientation": orientation,
                "marker": {"color": list(si), "colorscale": "Viridis"},
            }
        ],
        "layout": {
            "title": title,
            "xaxis": {"title": "Importance"},
            "yaxis": {"title": "Feature"},
            "margin": {"l": 120},
        },
    }


def interaction_heatmap(
    matrix: List[List[float]],
    labels: Optional[List[str]] = None,
    title: str = "Feature Interaction Heatmap",
) -> Dict[str, Any]:
    n = len(matrix)
    if labels is None:
        labels = [f"F{i}" for i in range(n)]
    return {
        "data": [
            {
                "type": "heatmap",
                "z": matrix,
                "x": labels,
                "y": labels,
                "colorscale": "RdBu",
                "zmid": 0,
            }
        ],
        "layout": {
            "title": title,
            "xaxis": {"title": "Feature"},
            "yaxis": {"title": "Feature", "autorange": "reversed"},
            "margin": {"l": 80, "b": 80},
        },
    }


def waterfall_plot(
    baseline: float,
    contributions: Dict[str, float],
    title: str = "SHAP Waterfall Plot",
) -> Dict[str, Any]:
    features = list(contributions.keys())
    values = list(contributions.values())
    cumulative = []
    running = baseline
    measures = ["absolute"] + ["relative"] * len(values) + ["total"]
    x_vals = ["Baseline"] + features + ["Prediction"]
    y_vals = [baseline] + values + [baseline + sum(values)]

    return {
        "data": [
            {
                "type": "waterfall",
                "orientation": "v",
                "x": x_vals,
                "y": y_vals,
                "measure": measures,
                "connector": {"line": {"color": "rgb(63,63,63)"}},
                "increasing": {"marker": {"color": "#EF553B"}},
                "decreasing": {"marker": {"color": "#636EFA"}},
                "totals": {"marker": {"color": "#00CC96"}},
            }
        ],
        "layout": {
            "title": title,
            "xaxis": {"title": "Feature"},
            "yaxis": {"title": "Contribution"},
            "showlegend": False,
        },
    }


def global_feature_bar(
    features: List[str],
    importance: List[float],
    title: str = "Global Feature Importance",
) -> Dict[str, Any]:
    sorted_pairs = sorted(zip(features, importance), key=lambda x: -abs(x[1]))
    sf, si = zip(*sorted_pairs) if sorted_pairs else ([], [])
    return {
        "data": [
            {
                "type": "bar",
                "x": list(sf),
                "y": [abs(v) for v in si],
                "marker": {"color": [abs(v) for v in si], "colorscale": "Bluered"},
            }
        ],
        "layout": {
            "title": title,
            "xaxis": {"title": "Feature", "tickangle": -45},
            "yaxis": {"title": "|SHAP value|"},
            "margin": {"b": 100},
        },
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "feature_bar_chart")

    if action == "feature_bar_chart":
        features = payload.get("features", {})
        importance = payload.get(
            "importance", list(features.values()) if features else []
        )
        if not importance and features:
            importance = list(features.values())
        result = feature_bar_chart(
            features=list(features.keys()) if isinstance(features, dict) else features,
            importance=importance,
            title=payload.get("title", "Feature Importance"),
            orientation=payload.get("orientation", "h"),
        )
    elif action == "interaction_heatmap":
        result = interaction_heatmap(
            matrix=payload["matrix"],
            labels=payload.get("labels"),
            title=payload.get("title", "Feature Interaction Heatmap"),
        )
    elif action == "waterfall_plot":
        result = waterfall_plot(
            baseline=payload["baseline"],
            contributions=payload["contributions"],
            title=payload.get("title", "SHAP Waterfall Plot"),
        )
    elif action == "global_feature_bar":
        features = payload.get("features", {})
        importance = payload.get(
            "importance", list(features.values()) if features else []
        )
        if not importance and features:
            importance = list(features.values())
        result = global_feature_bar(
            features=list(features.keys()) if isinstance(features, dict) else features,
            importance=importance,
            title=payload.get("title", "Global Feature Importance"),
        )
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
            await invoke(
                {
                    "action": "feature_bar_chart",
                    "features": ["age", "income", "score"],
                    "importance": [0.45, 0.72, -0.3],
                }
            )
        )
        print(
            await invoke(
                {
                    "action": "waterfall_plot",
                    "baseline": 0.5,
                    "contributions": {"age": 0.12, "income": -0.08, "score": 0.25},
                }
            )
        )
        print(
            await invoke(
                {
                    "action": "interaction_heatmap",
                    "matrix": [[0, 0.1, 0.2], [0.1, 0, 0.3], [0.2, 0.3, 0]],
                    "labels": ["A", "B", "C"],
                }
            )
        )

    asyncio.run(demo())
