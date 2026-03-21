---
name: hypothesis-testing
description: Form and test hypotheses systematically using deductive reasoning and evidence-based validation
metadata:
  updated-on: "2026-03-18"
  source: community
  tags: "hypothesis,testing,deduction,experiments,validation"
---

# Hypothesis Testing

Form educated guesses and validate them with evidence.

## Hypothesis Structure

```
Hypothesis Template:
┌─────────────────────────────────────────┐
│ IF [condition/action]                  │
│ THEN [expected outcome]                │
│ BECAUSE [reasoning]                    │
└─────────────────────────────────────────┘

Example:
IF we add caching to the API
THEN response time will decrease by 50%
BECAUSE cached responses skip database queries
```

## Hypothesis Template

```
Hypothesis: [Specific, testable statement]

Evidence Needed:
- [Metric to measure]
- [Acceptance threshold]

Test Method:
- [How to run the test]
- [Control vs. treatment]

Success Criteria:
- [Quantitative result needed]
- [When to accept/reject]
```

## Example: Performance Hypothesis

```
Hypothesis: 
IF we add Redis caching layer
THEN average API response time will decrease from 500ms to 100ms
BECAUSE Redis is in-memory and avoids database round-trips

Test Design:
├── Control: Current production (500ms baseline)
├── Treatment: New version with Redis
├── Metric: p99 response time
├── Duration: 7 days
└── Traffic: 10% of users (canary)

Execution:
├── Day 1-2: Deploy to 1% traffic
├── Day 3-4: Deploy to 10% traffic  
├── Day 5-7: Full evaluation
└── Then: Full rollout if successful

Results Analysis:
├── Treatment avg: 95ms
├── Control avg: 505ms
├── Improvement: 81%
├── Statistical significance: p < 0.001
└── Decision: ACCEPT - deploy to 100%
```

## Scientific Method Steps

```
1. OBSERVE: API is slow (500ms avg)
2. QUESTION: Why is the API slow?
3. HYPOTHESIZE: Database queries are the bottleneck
4. PREDICT: Adding caching will reduce latency
5. TEST: Implement cache, measure latency
6. ANALYZE: Compare before/after metrics
7. CONCLUDE: Hypothesis supported or refuted
```

## Hypothesis Prioritization Matrix

| Feasibility | Impact | Priority |
|-------------|--------|----------|
| High | High | **Do First** |
| High | Low | Do Later |
| Low | High | **Do First** (find easier way) |
| Low | Low | Skip |

## Anti-Patterns

- **Hypothesis without test**: "I think X is wrong" without way to verify
- **A/B confusion**: Changing multiple things at once
- **Ignoring null**: Not considering "no effect" possibility
- **Sample size too small**: One test run isn't evidence
- **Confirmation bias**: Only looking for supporting data

## Code: A/B Test Framework

```python
from dataclasses import dataclass
from typing import Callable, List
import random

@dataclass
class Experiment:
    name: str
    control_fn: Callable
    treatment_fn: Callable
    metric_fn: Callable
    success_threshold: float
    
    def run(self, n_samples: int) -> dict:
        control_results = []
        treatment_results = []
        
        for _ in range(n_samples):
            # Random assignment
            if random.random() < 0.5:
                result = self.control_fn()
                control_results.append(self.metric_fn(result))
            else:
                result = self.treatment_fn()
                treatment_results.append(self.metric_fn(result))
        
        control_mean = sum(control_results) / len(control_results)
        treatment_mean = sum(treatment_results) / len(treatment_results)
        
        improvement = (treatment_mean - control_mean) / control_mean
        
        return {
            "experiment": self.name,
            "control_mean": control_mean,
            "treatment_mean": treatment_mean,
            "improvement": improvement,
            "success": improvement >= self.success_threshold
        }
```

## Validation Checklist

- [ ] Clear hypothesis statement
- [ ] Measurable outcome
- [ ] Control group defined
- [ ] Sample size adequate
- [ ] Duration sufficient
- [ ] Metrics collected
- [ ] Statistical significance checked
- [ ] Results documented
