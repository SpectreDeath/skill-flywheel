---
name: belief-revision
description: "Use when: updating beliefs based on evidence, implementing belief revision systems, handling contradictory information, or building epistemic agents. Triggers: 'belief revision', 'update beliefs', 'Bayesian update', 'evidence-based', 'epistemic', 'belief update'. NOT for: when beliefs are fixed, simple rule-based systems, or when no evidence handling needed."
---

# Belief Revision

Implements belief revision mechanisms for updating knowledge based on new evidence. This skill applies Bayesian inference, handles contradictory information, and maintains coherent belief states.

## When to Use This Skill

Use this skill when:
- Updating beliefs based on evidence
- Implementing belief revision systems
- Handling contradictory information
- Building epistemic agents
- Making evidence-based decisions

Do NOT use this skill when:
- Beliefs are fixed
- Simple rule-based systems
- No evidence handling needed
- Deterministic logic sufficient

## Input Format

```yaml
revision_request:
  current_beliefs: object        # Current belief state
  new_evidence: object          # New evidence to incorporate
  revision_method: string       # How to revise (Bayesian, AGM, etc.)
  confidence: object           # Confidence levels
```

## Output Format

```yaml
revision_result:
  updated_beliefs: object        # Revised belief state
  revision_explanation: string # Why beliefs changed
  confidence_changes: object   # How confidence shifted
  contradictions: array         # Any contradictions found
```

## Capabilities

### 1. Belief Representation (10 min)

- Define belief states
- Represent confidence levels
- Model uncertainty
- Structure knowledge

### 2. Evidence Processing (15 min)

- Evaluate evidence quality
- Calculate likelihood ratios
- Assess evidence relevance
- Handle conflicting evidence

### 3. Revision Application (15 min)

- Apply Bayesian updates
- Use AGM postulates
- Handle belief contraction
- Manage expansion vs revision

### 4. Consistency Maintenance (10 min)

- Detect contradictions
- Resolve conflicts
- Maintain logical consistency
- Handle paradoxes

### 5. Explanation Generation (10 min)

- Explain belief changes
- Show evidence impact
- Justify revisions
- Track belief history

## Usage Examples

### Basic Usage

"Update my beliefs based on this new evidence."

### Advanced Usage

"Apply Bayesian revision with conflict resolution."

## Configuration Options

- `revision_method`: Bayesian, AGM, Pearl, etc.
- `consistency_check`: How rigorous
- `explanation_level`: Detail of explanations
- `history_tracking`: Keep belief timeline

## Constraints

- MUST maintain consistency
- SHOULD explain changes
- MUST handle contradictions
- SHOULD quantify uncertainty

## Integration Examples

- AI agents: Epistemic reasoning
- Decision systems: Evidence-based choices
- Knowledge bases: Dynamic updates
- Expert systems: Evidence handling

## Dependencies

- Python 3.10+
- Probability libraries
- Logic systems
- Bayesian inference
