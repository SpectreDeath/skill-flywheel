---
name: problem-decomposition
description: Break complex problems into manageable sub-problems using hierarchical and functional decomposition
metadata:
  updated-on: "2026-03-18"
  source: community
  tags: "decomposition,breakdown,sub-problems,hierarchical,thinking"
---

# Problem Decomposition

Transform overwhelming problems into solvable pieces.

## Hierarchical Decomposition

```
Complex Problem
    ├── Level 1: Major Components
    │   ├── Component A
    │   │   ├── Sub-component A1
    │   │   └── Sub-component A2
    │   └── Component B
    │       ├── Sub-component B1
    │       └── Sub-component B2
    │
    └── Level 2: Dependencies
        - Which components depend on others?
        - What can be parallelized?
        - What is sequential?
```

## Functional Decomposition

```
Problem: Build an e-commerce checkout system

分解 (Decompose):
├── User Authentication
│   ├── Login
│   ├── Registration
│   └── Password reset
├── Product Catalog
│   ├── Browse
│   ├── Search
│   └── Filter
├── Shopping Cart
│   ├── Add/remove items
│   ├── Update quantities
│   └── Calculate totals
├── Checkout
│   ├── Shipping address
│   ├── Payment processing
│   └── Order confirmation
└── Order Management
    ├── Order history
    ├── Tracking
    └── Returns
```

## Algorithm Design: Divide and Conquer

```python
def merge_sort(arr):
    """Decompose: split → sort → merge"""
    
    # Base case: single element is sorted
    if len(arr) <= 1:
        return arr
    
    # DECOMPOSE: Split into halves
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # CONQUER: Sort each half recursively
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    
    # COMBINE: Merge sorted halves
    return merge(left_sorted, right_sorted)


def merge(left, right):
    """Combine two sorted arrays"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

## Data Decomposition

```
Task: Process 1M records

Decomposition strategies:

1. By Record:
   - Split into 10 batches of 100K
   - Process each independently
   - Aggregate results

2. By Field:
   - Extract common fields separately
   - Transform in parallel
   - Join back together

3. By Time Window:
   - Partition by date/hour
   - Process each time slice
   - Merge temporal results
```

## Dependency Analysis

```
Task: Build a web application

Step 1 - Identify all tasks:
├── Design UI
├── Setup database
├── Create API endpoints
├── Write frontend code
├── Write backend logic
├── Write tests
└── Deploy

Step 2 - Map dependencies:
- Design UI → Write frontend code
- Setup database → Create API endpoints
- Setup database → Write backend logic
- Write frontend code → Deploy
- Write backend logic → Deploy
- Write tests → Deploy

Step 3 - Determine execution order:
Phase 1: Design UI, Setup database
Phase 2: Write frontend, Write backend, Create API
Phase 3: Write tests  
Phase 4: Deploy
```

## Decision: Decompose or Not

| Problem Type | Decompose? | Reason |
|--------------|------------|--------|
| Algorithm design | Yes | Reduce complexity |
| Bug investigation | Yes | Isolate causes |
| Large refactor | Yes | Manage risk |
| Simple CRUD | No | Overhead not worth it |
| Single file fix | No | Already atomic |

## Red Flags

- More than 7 items at one level → sub-divide
- Circular dependencies → redesign
- Uneven workload → rebalance
- Can't explain a sub-problem → too coarse
