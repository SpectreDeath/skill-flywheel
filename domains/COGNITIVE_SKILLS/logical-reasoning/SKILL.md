---
Domain: COGNITIVE_SKILLS
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Thinking Skills
Estimated Execution Time: 2-10 minutes
name: logical-reasoning
Source: community
---

## Purpose

Apply rational assessment to draw correct inferences from premises to conclusions using formal logical rules.

## Description

Logical reasoning is the foundation of convergent thinking. It involves applying established logical rules (syllogisms, implications, deductions) to evaluate arguments, draw inferences, and reach valid conclusions. This skill enables systematic evaluation of claims based on evidence and logical structure.

## Examples

### Syllogism Example

```
Premise 1: All mammals are warm-blooded
Premise 2: Whales are mammals
Conclusion: Therefore, whales are warm-blooded
```

### Modus Ponens

```
If it rains (P), then the ground gets wet (Q)
It rains (P)
Therefore, the ground gets wet (Q)
```

## Implementation Notes

- Uses formal logic patterns: syllogisms, modus ponens, modus tollens
- Distinguishes between validity (structure) and truth (content)
- Identifies logical fallacies and hidden assumptions

## Capabilities

- Deductive reasoning application
- Inductive reasoning evaluation
- Argument structure analysis
- Fallacy detection
- Logical inference drawing

## Usage Examples

### Argument Evaluation

```
ARGUMENT: [Statement to evaluate]

STEP 1: Identify Premises
        - Premise A
        - Premise B

STEP 2: Identify Conclusion

STEP 3: Check Validity
        - Are premises true?
        - Does conclusion follow logically?

STEP 4: Assess Strength
        - Strong: Conclusion follows necessarily
        - Weak: Conclusion follows probabilistically
```

## Input Format

```yaml
reasoning_task:
  premises:
    - "premise 1"
    - "premise 2"
  conclusion: "proposed conclusion"
  reasoning_type: "deductive|inductive"
```

## Output Format

```yaml
reasoning_result:
  is_valid: true/false
  is_sound: true/false
  strength: "strong|moderate|weak"
  fallacies: []
  explanation: "detailed explanation"
```

## Best Practices

- Identify premises first before drawing conclusions
- Check for hidden assumptions
- Distinguish validity from truth
- Use formal logic rules

## Constraints

- MUST identify all premises before evaluating
- MUST check assumptions
- SHOULD use formal logic patterns
- MUST NOT assume correlation implies causation
