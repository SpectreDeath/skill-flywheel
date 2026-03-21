---
name: decision-tree-analysis
description: Map out decision paths systematically to explore options, outcomes, and consequences
metadata:
  updated-on: "2026-03-18"
  source: community
  tags: "decision-tree,branching,scenarios,choice,analysis"
---

# Decision Tree Analysis

Map choices and consequences to make informed decisions.

## Tree Structure

```
                    ┌──────────────┐
                    │  Decision    │
                    │   Point A    │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
      ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐
      │ Option1 │    │  Option2  │   │ Option3  │
      └────┬────┘    └─────┬─────┘   └─────┬─────┘
           │               │               │
      ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐
      │Outcome A│    │ Outcome B │   │ Outcome C │
      └─────────┘    └───────────┘   └───────────┘
```

## Example: Build vs. Buy

```
Decision: Build custom payment system or buy Stripe?

                        ┌────────────────────┐
                        │  Payment Solution  │
                        └─────────┬──────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
    ┌────▼────────┐          ┌─────▼──────┐         ┌──────▼──────┐
    │    Build    │          │    Buy     │         │   Hybrid    │
    │  (Custom)   │          │  (Stripe)  │         │  (Partial)  │
    └──────┬──────┘          └──────┬──────┘         └──────┬──────┘
           │                         │                      │
      ┌────▼────┐               ┌────▼─────┐           ┌────▼─────┐
      │ Complete│               │ $2k/mo   │           │ $1k/mo   │
      │Control  │               │ +dev     │           │ +partial │
      │ 12 weeks│               │ time     │           │ dev      │
      └─────────┘               └──────────┘          └──────────┘

Evaluation Criteria (weighted):
├── Time to market: 30%
├── Cost (1yr): 25%
├── Control/Flex: 25%
└── Maintenance: 20%

Scoring:
Build:   3×0.3 + 2×0.25 + 5×0.25 + 2×0.20 = 3.05
Buy:     5×0.3 + 4×0.25 + 3×0.25 + 5×0.20 = 4.25
Hybrid:  4×0.3 + 3×0.25 + 4×0.25 + 4×0.20 = 3.70

Decision: BUY (highest score)
```

## Example: Bug Prioritization

```
                    ┌──────────────┐
                    │  Bug Found   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │                         │
         ┌────▼────┐              ┌─────▼─────┐
         │ Critical│              │  Non-Crit │
         │ (P0)    │              │ (P1-P3)   │
         └────┬────┘              └─────┬─────┘
              │                         │
    ┌─────────┼─────────┐      ┌────────┼────────┐
    │         │         │      │        │        │
┌───▼───┐ ┌──▼──┐ ┌───▼───┐┌──▼──┐┌──▼──┐┌──▼──┐
│Revenue│ │Data │ │Security││Fix  ││Later││Docs │
│Impact │ │Loss │ │ Breach ││Next ││Sprint││ Only│
└───────┘ └─────┘ └───────┘└─────┘└─────┘└─────┘

Fix now: Critical bugs affecting revenue, data, or security
Plan: Non-critical bugs that block features  
Backlog: Minor issues, improvements, documentation
```

## Decision Tree Template

```
DECISION: [What needs to be decided]

OPTIONS:
1. [Option A]
2. [Option B]  
3. [Option C]

CRITERIA (with weights):
- [Criterion 1]: [Weight]%
- [Criterion 2]: [Weight]%
- [Criterion 3]: [Weight]%

SCORING (1-5):
Option A: [scores]
Option B: [scores]
Option C: [scores]

WEIGHTED SCORES:
Option A: [total]
Option B: [total]
Option C: [total]

DECISION: [Winner with reasoning]

RISKS:
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]
```

## Code: Simple Decision Tree

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DecisionNode:
    question: str
    yes_branch: Optional['DecisionNode'] = None
    no_branch: Optional['DecisionNode'] = None
    outcome: Optional[str] = None
    
    def decide(self, answers: dict) -> str:
        answer = answers.get(self.question, "")
        
        if self.outcome:
            return self.outcome
        
        if answer.lower() in ["yes", "y", "true"]:
            return self.yes_branch.decide(answers) if self.yes_branch else self.outcome
        else:
            return self.no_branch.decide(answers) if self.no_branch else self.outcome


# Build a tree
root = DecisionNode(
    question="Is it a security issue?",
    yes_branch=DecisionNode(
        outcome="Fix immediately - P0"
    ),
    no_branch=DecisionNode(
        question="Does it block users?",
        yes_branch=DecisionNode(
            outcome="Fix this sprint - P1"
        ),
        no_branch=DecisionNode(
            question="Is it a new feature bug?",
            yes_branch=DecisionNode(
                outcome="Next sprint - P2"
            ),
            no_branch=DecisionNode(
                outcome="Backlog - P3"
            )
        )
    )
)

# Use it
result = root.decide({
    "Is it a security issue?": "No",
    "Does it block users?": "Yes"
})
# Result: "Fix this sprint - P1"
```

## Best Practices

- Start with the decision, work backward
- Branch on binary choices where possible
- Consider "do nothing" as an option
- Assign probabilities to uncertain outcomes
- Calculate expected value for numeric decisions
- Document assumptions at each node

## Anti-Patterns

- Incomplete options list
- Missing "none of the above"
- Ignoring probabilities
- Not considering time horizon
- Confusing symptoms with decisions
