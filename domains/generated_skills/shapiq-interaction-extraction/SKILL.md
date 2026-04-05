---
name: shapiq-interaction-extraction
description: "Use when: extracting main effects and pairwise interaction matrices from SHAP-IQ InteractionValues objects for analysis. Triggers: 'SHAP-IQ extraction', 'interaction matrix', 'main effects', 'pairwise interactions', 'DataFrame conversion'. NOT for: raw SHAP values (use standard SHAP), or when visualization is needed (use xai-plotly-visualization)."
---

# SHAP-IQ Interaction Effect Extraction

## Overview

Utility functions for extracting structured data from SHAP-IQ `InteractionValues` objects. Converts the raw `(tuple) -> float` dictionary into Pandas Series (main effects) and DataFrames (pairwise interaction matrices).

## Main Effects Extraction

```python
import pandas as pd
import numpy as np

def extract_main_effects(iv, feature_names):
    """Extract main (first-order) effects from InteractionValues."""
    d = iv.dict_values
    vals = [float(d.get((i,), 0.0)) for i in range(len(feature_names))]
    return pd.Series(vals, index=list(feature_names), name="main_effect")
```

**Output:** `pd.Series` indexed by feature names, containing signed main effect values. Positive = pushes prediction above baseline, negative = pushes below.

## Pairwise Interaction Matrix

```python
def extract_pair_matrix(iv, feature_names):
    """Extract symmetric pairwise interaction matrix from InteractionValues."""
    d = iv.dict_values
    n = len(feature_names)
    M = np.zeros((n, n), dtype=float)
    for k, v in d.items():
        if isinstance(k, tuple) and len(k) == 2:
            i, j = k
            M[i, j] = float(v)
            M[j, i] = float(v)  # Symmetric: interaction(i,j) == interaction(j,i)
    return pd.DataFrame(M, index=list(feature_names), columns=list(feature_names))
```

**Output:** `pd.DataFrame` (n x n) symmetric matrix. Diagonal is zero (self-interactions are main effects). Off-diagonal values represent how much the combined effect of features i and j deviates from the sum of their individual effects.

## Interaction Value Semantics

```
prediction ≈ baseline + Σ main_effects + Σ pairwise_interactions

For a single prediction:
  f(x) ≈ baseline + Σᵢ φᵢ + Σᵢ<ⱼ φᵢⱼ

Where:
  baseline        = average model output over background data
  φᵢ (i,)        = main effect of feature i
  φᵢⱼ (i,j)      = interaction between features i and j
```

## Extracting Top Interactions as List

```python
def get_top_interactions(pair_df, feature_names, top_k=25):
    """Convert interaction matrix to sorted list of top-k pairs."""
    n = len(feature_names)
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            v = float(pair_df.iat[i, j])
            pairs.append({
                'feature_i': feature_names[i],
                'feature_j': feature_names[j],
                'interaction': v,
                'abs_interaction': abs(v)
            })
    return pd.DataFrame(pairs).sort_values('abs_interaction', ascending=False).head(top_k)
```

## Usage Pattern

```python
# After explainer.explain(x, budget=512, random_state=0)
main_effects = extract_main_effects(iv, feature_names)
pair_df = extract_pair_matrix(iv, feature_names)

# Top main effects
top_main = main_effects.reindex(
    main_effects.abs().sort_values(ascending=False).head(10).index
)

# Top interactions
top_pairs = get_top_interactions(pair_df, feature_names, top_k=25)
```

## Constraints

- MUST check `isinstance(k, tuple) and len(k) == 2` when extracting interactions (skip main effects and higher-order terms)
- MUST handle missing keys with `.get((i,), 0.0)` (not all features may have non-zero effects)
- Interaction matrix is always symmetric -- fill both (i,j) and (j,i)
- Diagonal of interaction matrix should remain zero (self-interactions stored as main effects)
- Budget affects which interactions are computed -- low budget may skip some pairs
