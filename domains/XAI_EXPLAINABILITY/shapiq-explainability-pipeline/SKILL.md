---
name: shapiq-explainability-pipeline
description: "Use when: building explainable AI pipelines with SHAP-IQ to compute theoretically grounded Shapley interaction indices for model predictions. Triggers: 'SHAP-IQ', 'Shapley interactions', 'feature interactions', 'pairwise effects', 'explainability pipeline', 'XAI'. NOT for: basic SHAP values only (use standard SHAP), or when model doesn't support SHAP."
---

# SHAP-IQ Explainability Pipeline Setup

## Overview

End-to-end setup pattern for SHAP-IQ-based explainability. Installs dependencies, loads data, trains a model, and initializes the SHAP-IQ `TabularExplainer` with configurable interaction order, computation budget, and interaction index type.

## Dependencies

```python
import sys, subprocess

def _pip(*pkgs):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *pkgs], check=False)

_pip("shapiq", "plotly", "pandas", "numpy", "scikit-learn")
```

## Configuration Constants

```python
RANDOM_STATE = 42
INDEX = "SII"            # Shapley Interaction Index (alternatives: "k-SII", "FSII", "FBII")
MAX_ORDER = 2            # 1=main effects only, 2=main+pairwise interactions
BUDGET_LOCAL = 512       # Computation budget per local explanation
TOP_K = 10               # Number of top features to display
INSTANCE_I = 24          # Test instance index for local explanation
GLOBAL_ON = True         # Enable global analysis
GLOBAL_N = 40            # Number of samples for global aggregation
BUDGET_GLOBAL = 256      # Computation budget per global sample
```

## Model Training

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import shapiq

X, y = shapiq.load_california_housing()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

feature_names = list(X_train.columns)
n_features = len(feature_names)

model = RandomForestRegressor(
    n_estimators=400,
    max_depth=max(3, n_features),
    max_features=2/3,
    max_samples=2/3,
    random_state=RANDOM_STATE,
    n_jobs=-1
)
model.fit(X_train.values, y_train.values)
```

## Explainer Initialization

```python
explainer = shapiq.TabularExplainer(
    model=model.predict,
    data=X_train.values,
    index=INDEX,           # "SII" = Shapley Interaction Index
    max_order=int(MAX_ORDER),  # 2 = compute up to pairwise interactions
)
```

## Local Explanation

```python
INSTANCE_I = int(np.clip(INSTANCE_I, 0, len(X_test)-1))
x = X_test.iloc[INSTANCE_I].values
y_true = float(y_test.iloc[INSTANCE_I])
pred = float(model.predict([x])[0])

# Compute explanation with budget constraint
iv = explainer.explain(x, budget=int(BUDGET_LOCAL), random_state=0)
baseline = float(getattr(iv, "baseline_value", 0.0))
```

## InteractionValues Object Structure

```python
# iv.dict_values is a dict mapping tuples to float values:
#   (i,)      -> main effect of feature i
#   (i, j)    -> pairwise interaction between features i and j
#   baseline  -> average model prediction over background data
```

## Index Types

| Index | Key | Description |
|-------|-----|-------------|
| SII | `"SII"` | Shapley Interaction Index -- signed values, sums to prediction |
| k-SII | `"k-SII"` | k-Shapley Interaction Index -- truncated interactions |
| FSII | `"FSII"` | Faithful Shapley Interaction Index |
| FBII | `"FBII"` | Fictitious Banzhaf Interaction Index |

## Constraints

- MUST set `max_order=2` to capture pairwise interactions (1 = main effects only)
- MUST provide `data` parameter for background distribution (training data)
- MUST use `model.predict` (callable), not the model object directly
- BUDGET controls accuracy vs speed tradeoff -- higher = more accurate but slower
- SHOULD use `random_state` for reproducible explanations
- SHOULD use `np.clip` on instance index to prevent out-of-bounds
- `index="SII"` provides signed interaction values that sum to the prediction minus baseline
