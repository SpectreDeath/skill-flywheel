---
name: terminal-xai-reporting
description: "Use when: generating terminal-friendly ASCII reports for explainable AI analysis without graphical output, including bar visualizations and structured tables. Triggers: 'terminal XAI', 'ASCII report', 'CLI visualization', 'feature importance table', 'text-based charts'. NOT for: interactive visualizations (use xai-plotly-visualization), or when rich output is required."
---

# Terminal-Based XAI Reporting

## Overview

ASCII visualization and terminal reporting pattern for explainable AI outputs. Produces readable feature importance bars, structured tables, and formatted summaries directly in the terminal without requiring GUI or browser access.

## ASCII Bar Chart

```python
def ascii_bar(series, width=28, top_k=10):
    """Render horizontal ASCII bar chart in terminal."""
    s = series.abs().sort_values(ascending=False).head(top_k)
    m = float(s.max()) if len(s) else 1.0
    lines = []
    for name, val in s.items():
        n = int((abs(val) / m) * width) if m > 0 else 0
        lines.append(f"{name:>18} | {'█'*n}{' '*(width-n)} | {val:+.6f}")
    return "\n".join(lines)
```

**Output:**
```
       MedInc       | ████████████████████████████ | +0.452318
       Latitude     | ████████████████             | -0.258934
       HouseAge     | ████████████                 | +0.194521
       AveRooms     | ████████                     | +0.128453
```

## Local Explanation Report

```python
def print_local_report(iv, main_effects, pair_df, feature_names, pred, y_true, baseline, top_k=10):
    print("\n" + "="*90)
    print("LOCAL EXPLANATION (single test instance)")
    print("="*90)
    print(f"Prediction: {pred:.6f} | True: {y_true:.6f} | Baseline: {baseline:.6f}")

    # Signed main effects table
    print("\nTop main effects (signed):")
    top = main_effects.reindex(
        main_effects.abs().sort_values(ascending=False).head(top_k).index
    )
    print(top.to_frame().to_string())

    # ASCII visualization
    print("\nASCII view (signed main effects, top-k):")
    print(ascii_bar(main_effects, top_k=top_k))

    # Top interactions table
    print("\nTop pairwise interactions by |value|:")
    n = len(feature_names)
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            v = float(pair_df.iat[i, j])
            pairs.append((feature_names[i], feature_names[j], v, abs(v)))
    pairs_df = pd.DataFrame(
        pairs, columns=["feature_i", "feature_j", "interaction", "abs_interaction"]
    ).sort_values("abs_interaction", ascending=False).head(25)
    print(pairs_df.to_string(index=False))
```

## Global Report

```python
def print_global_report(global_main, global_pair, feature_names, n_samples, budget, top_k=10):
    print("\n" + "="*90)
    print("GLOBAL SUMMARIES (sampled over multiple test points)")
    print("="*90)
    print(f"Samples={n_samples} | budget/sample={budget}")

    print("\nGlobal feature importance (mean |main effect|):")
    print(global_main.head(top_k).to_string(index=False))

    print("\nGlobal interaction heatmap (top features):")
    top_feats = list(global_main["feature"].head(top_k).values)
    sub = global_pair.loc[top_feats, top_feats]
    print(sub.to_string())
```

## Separator Helpers

```python
def section_header(title, width=90):
    print("\n" + "="*width)
    print(title)
    print("="*width)

def subsection(title):
    print(f"\n{title}:")
```

## Constraints

- MUST use `abs()` for ranking but display signed values for directionality
- ASCII bar width should be 20-40 characters for readability
- SHOULD use `>18` right-align for feature names (adjust for longest name)
- MUST format floats with `+.6f` to show sign and precision
- SHOULD use `to_string(index=False)` for clean table output
- SHOULD use Unicode block character `█` for bars (works in most modern terminals)
- MUST separate sections with `=` dividers for visual scanning
