---
Domain: COGNITIVE_SKILLS
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Thinking Skills
Estimated Execution Time: 5-20 minutes
name: sequential-problem-solving
Source: community
---

## Purpose

Move from problem statement to solution through logical, ordered steps with verification at each stage.

## Description

Sequential problem-solving is a methodical approach that breaks down problem resolution into discrete, ordered steps. Each step builds on the previous, with verification before proceeding. This reduces errors and ensures logical flow from problem to solution.

## Examples

### Mathematical Problem

```
Problem: Solve 2x + 5 = 17

Step 1: Identify goal - find x
        Constraint - equation must remain balanced

Step 2: Plan - isolate x by inverse operations
        First: subtract 5 from both sides
        Second: divide by 2

Step 3: Execute:
        2x + 5 = 17 → 2x = 12 → x = 6

Step 4: Verify: 2(6) + 5 = 17 ✓
```

## Implementation Notes

- Break problems into manageable steps
- Verify each step before proceeding
- Track dependencies between steps

## Capabilities

- Problem decomposition
- Step planning
- Execution verification
- Solution validation

## Input Format

```yaml
problem:
  statement: "problem description"
  constraints: []
  knowns: []
  unknowns: []
```

## Output Format

```yaml
solution:
  steps: []
  verification: "passed/failed"
  final_answer: ""
```

## Constraints

- MUST verify each step before proceeding
- MUST document intermediate results
- SHOULD handle dependencies explicitly
