---
name: iterative-refinement
description: Progressive improvement through feedback loops - refine solutions by cycling through generate, evaluate, and improve phases
metadata:
  updated-on: "2026-03-18"
  source: community
  tags: "iteration,refinement,feedback,improvement,loop"
---

# Iterative Refinement

Improve solutions through progressive cycles of feedback and enhancement.

## The Iteration Cycle

```
┌─────────────────────────────────────┐
│         ITERATION LOOP              │
├─────────────────────────────────────┤
│  1. GENERATE → 2. EVALUATE         │
│        ↗                      ↘    │
│        └──────────────────────┘    │
│           3. IMPROVE               │
└─────────────────────────────────────┘
```

## Template

```
Iteration N:
- Current state: [description]
- Evaluation criteria: [how to measure]
- Gap from goal: [what's wrong]
- Improvement action: [specific change]
- Expected outcome: [what happens next]
```

## Example: Code Refinement

```
Iteration 1 - Initial:
```python
def find_max(arr):
    max_val = 0
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val
```
Evaluation: Fails for negative numbers [-5, -2, -10]
Gap: Returns 0 instead of -2

Iteration 2 - Fixed negatives:
```python
def find_max(arr):
    max_val = arr[0]
    for x in arr[1:]:
        if x > max_val:
            max_val = x
    return max_val
```
Evaluation: Works but crashes on empty array
Gap: IndexError when arr is empty

Iteration 3 - Handle empty:
```python
def find_max(arr):
    if not arr:
        raise ValueError("Empty array")
    max_val = arr[0]
    for x in arr[1:]:
        if x > max_val:
            max_val = x
    return max_val
```
Evaluation: ✓ Correct for all cases
```

## Example: Algorithm Optimization

```
Problem: Sort 1M integers

Iteration 1 - Bubble Sort (baseline):
- Time: O(n²) = 10¹² operations
- Memory: O(1)
- Evaluation: Too slow

Iteration 2 - Quick Sort:
- Time: O(n log n) = 20M operations
- Memory: O(log n) stack
- Evaluation: Fast enough but unstable

Iteration 3 - Timsort (Python built-in):
- Time: O(n log n) worst case
- Memory: O(n)
- Evaluation: ✓ Production ready
```

## Convergence Criteria

| Criterion | Example | Threshold |
|-----------|---------|-----------|
| Performance | Execution time | < 100ms |
| Accuracy | Test pass rate | > 99% |
| Coverage | Lines tested | > 90% |
| Quality | Lint score | 0 errors |
| Stability | Crash rate | 0% |

## When to Stop Iterating

- Solution meets all requirements
- Diminishing returns (effort >> improvement)
- Time budget exhausted
- Found fundamental limitation
- Premature optimization warning

## Anti-Patterns

- **Premature optimization**: Optimize before correct
- **Scope creep**: Keep adding features
- **Perfectionism**: Endless refinements
- **Ignoring feedback**: Dismiss valid criticism
- **No baseline**: Don't know where you started
