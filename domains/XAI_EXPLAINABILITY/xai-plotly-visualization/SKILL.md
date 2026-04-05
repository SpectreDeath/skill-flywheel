---
name: xai-plotly-visualization
description: "Use when: creating interactive Plotly visualizations for explainable AI outputs including feature importance bar charts, interaction heatmaps, and decision breakdown waterfall plots. Triggers: 'SHAP plot', 'feature importance', 'interaction heatmap', 'waterfall plot', 'explainability', 'XAI visualization'. NOT for: static reports (use terminal-xai-reporting), or when Plotly is unavailable."
---

# XAI Visualization Pipeline (Plotly)

## Overview

Three-visualization pattern for presenting explainable AI results: bar charts for feature importance, heatmaps for pairwise interactions, and waterfall plots for decision breakdowns. Uses Plotly for interactive exploration.

## Local Feature Importance Bar Chart

```python
import plotly.express as px

def plot_local_feature_bar(main_effects, top_k):
    df = main_effects.abs().sort_values(ascending=False).head(top_k).reset_index()
    df.columns = ["feature", "abs_main_effect"]
    fig = px.bar(
        df, x="abs_main_effect", y="feature", orientation="h",
        title="Local Feature Importance (|Main Effects|)"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig
```

## Interaction Heatmap

```python
def plot_local_interaction_heatmap(pair_df, top_features):
    sub = pair_df.loc[top_features, top_features]
    fig = px.imshow(
        sub.values, x=sub.columns, y=sub.index, aspect="auto",
        title="Local Pairwise Interaction Importance"
    )
    return fig
```

## Decision Breakdown Waterfall

```python
import plotly.graph_objects as go

def plot_waterfall(baseline, main_effects, top_k):
    contrib = main_effects.copy()
    top = contrib.reindex(contrib.abs().sort_values(ascending=False).head(top_k).index)
    remainder = float(contrib.sum() - top.sum())

    labels = ["baseline"] + list(top.index)
    measures = ["absolute"] + ["relative"] * len(top)
    y = [0.0] + [float(v) for v in top.values]

    if abs(remainder) > 1e-12:
        labels += ["others"]
        measures += ["relative"]
        y += [float(remainder)]

    labels += ["prediction"]
    measures += ["total"]
    y += [0.0]

    fig = go.Figure(go.Waterfall(
        x=labels, y=y, measure=measures, orientation="v",
        connector={"line": {"width": 1}}
    ))
    fig.update_layout(
        title="Decision Breakdown (Baseline -> Prediction via Main Effects)",
        showlegend=False
    )
    return fig
```

## Global Visualizations

```python
# Global feature importance bar
def plot_global_feature_bar(global_main, top_k):
    fig = px.bar(
        global_main.head(top_k), x="mean_abs_main_effect", y="feature",
        orientation="h", title="Global Feature Importance (mean |main effect|)"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    return fig

# Global interaction heatmap
def plot_global_interaction_heatmap(global_pair, top_features):
    sub = global_pair.loc[top_features, top_features]
    fig = px.imshow(
        sub.values, x=sub.columns, y=sub.index, aspect="auto",
        title="Global Pairwise Interaction Importance (mean |interaction|)"
    )
    return fig
```

## Render Configuration

```python
import plotly.io as pio

# Auto-detect environment
try:
    pio.renderers.default = "colab"  # Google Colab
except Exception:
    pio.renderers.default = "browser"  # Local fallback

# Usage
fig = plot_local_feature_bar(main_effects, top_k=10)
fig.show()
```

## Constraints

- MUST use `main_effects.abs()` for importance ranking (signed values for waterfall)
- Waterfall plot uses signed values (positive = pushes up, negative = pushes down)
- Heatmap requires symmetric square DataFrame from `extract_pair_matrix()`
- SHOULD use `"categoryorder": "total ascending"` for horizontal bars (largest on top)
- MUST handle `"others"` remainder category in waterfall when `abs(remainder) > 1e-12`
- `aspect="auto"` allows non-square heatmaps; use `aspect="equal"` for square feature sets
