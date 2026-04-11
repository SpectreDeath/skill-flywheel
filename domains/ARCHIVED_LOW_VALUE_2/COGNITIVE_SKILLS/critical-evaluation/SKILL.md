---
Domain: COGNITIVE_SKILLS
Version: 1.0.0
Complexity: High
Type: Process
Category: Thinking Skills
Estimated Execution Time: 10-30 minutes
name: critical-evaluation
Source: community
---
origin: manual
triggers:
  - agent
  - ai
  - development
quality:
  applied_count: 0
  success_count: 0
  completion_rate: 0.0
  token_savings_avg: 0.0
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T10:00:00Z"


## Purpose

Apply standards and probabilities to assess the quality and validity of information, arguments, and solutions.

## Description

Critical evaluation involves systematically assessing information quality using defined criteria, probability assessment, and evidence strength. It goes beyond surface-level checking to evaluate credibility, logic, and practical applicability.

## Examples

### Research Claim Evaluation

```
CLAIM: "New drug reduces heart disease by 50%"

EVALUATION:
1. Source: Peer-reviewed journal ✓
2. Evidence: Sample size 10,000, p<0.001 ✓
3. Logic: Conclusion follows from data ✓
4. Probability: HIGH confidence

CONCLUSION: HIGHLY PROBABLE
```

## Implementation Notes

- Use multiple evaluation criteria
- Quantify where possible
- Consider alternatives explicitly

## Capabilities

- Source credibility assessment
- Evidence quality evaluation
- Probability assessment
- Bias detection

## Constraints

- MUST use multiple criteria
- MUST state confidence levels
- SHOULD quantify when possible
