---
name: global-feature-importance
description: "Use when: computing global feature importance and interaction patterns by aggregating SHAP-IQ local explanations across samples. Triggers: 'global importance', 'aggregated SHAP', 'model behavior', 'feature ranking', 'overall importance'. NOT for: single prediction explanation (use local SHAP), or when SHAP-IQ isn't available."
---

# Global Feature Importance Aggregation

## Overview

Aggregation pattern that computes local SHAP-IQ explanations across multiple samples and averages them to produce global feature importance rankings and interaction heatmaps. Identifies which features and feature pairs matter most to the model overall.

## Aggregation Function

```python
import numpy as np
import pandas as pd

def global_summaries(explainer, X_samples, feature_names, budget, seed=123):
    main_abs = np.zeros(len(feature_names), dtype=float)
    pair_abs = np.zeros((len(feature_names), len(feature_names)), dtype=float)

    for t, x in enumerate(X_samples):
        # Compute local explanation with unique seed per sample
        iv = explainer.explain(x, budget=int(budget), random_state=int(seed + t))

        # Extract structured effects
        main = extract_main_effects(iv, feature_names).values
        pair = extract_pair_matrix(iv, feature_names).values

        # Accumulate absolute values (magnitude matters for importance)
        main_abs += np.abs(main)
        pair_abs += np.abs(pair)

    # Average across samples
    main_abs /= max(1, len(X_samples))
    pair_abs /= max(1, len(X_samples))

    # Create output DataFrames
    main_df = pd.DataFrame({
        "feature": feature_names,
        "mean_abs_main_effect": main_abs
    }).sort_values("mean_abs_main_effect", ascending=False)

    pair_df = pd.DataFrame(pair_abs, index=feature_names, columns=feature_names)

    return main_df, pair_df
```

## Sampling Strategy

```python
# Sample subset of test data for global analysis
GLOBAL_N = 40  # Balance between coverage and computation cost
sample = X_test.sample(n=GLOBAL_N, random_state=1).values

global_main, global_pair = global_summaries(
    explainer=explainer,
    X_samples=sample,
    feature_names=feature_names,
    budget=256,     # Lower budget OK for global (averaging smooths noise)
    seed=123,
)
```

## Interpretation

```python
# Top global features
print(global_main.head(10))

# Top global interactions
top_feats = list(global_main["feature"].head(10).values)
sub = global_pair.loc[top_feats, top_feats]
print(sub)  # 10x10 interaction submatrix
```

## Budget Tradeoffs

| Budget | Accuracy | Speed | Use Case |
|--------|----------|-------|----------|
| 128 | Low | Fast | Quick screening |
| 256 | Medium | Moderate | Global analysis (recommended) |
| 512 | High | Slow | Local single-instance |
| 1024+ | Very high | Very slow | Publication-quality |

## Per-Sample Seed Strategy

Using `seed + t` (where t is sample index) ensures:
- Different samples get different random permutations
- Same sample always gets same explanation (reproducibility)
- No correlation between seed and sample content

## Constraints

- MUST use `np.abs()` before averaging (signed values cancel out across samples)
- MUST use unique `random_state` per sample for unbiased aggregation
- SHOULD use lower budget for global than local (averaging compensates noise)
- MUST ensure `GLOBAL_N >= 5` for meaningful averages
- MUST use `max(1, len(X_samples))` to prevent division by zero
- SHOULD use `X_test.sample()` not `X_test.head()` to avoid selection bias
- Pairwise interaction matrix at global level shows co-importance patterns
