---
name: tla-plus-specification
description: "Use when: writing TLA+ specifications, modeling concurrent systems, verifying system properties, or performing formal verification with TLA+. Triggers: 'TLA+', 'formal specification', 'model checking', 'temporal logic', 'formal verification', 'PlusCal'. NOT for: when formal methods not needed, simple systems easily tested, or when TLA+ expertise unavailable."
---

# TLA+ Specification

Writes TLA+ specifications for formal modeling and verification of systems. This skill helps create PlusCal algorithms, define invariants, and run model checking.

## When to Use This Skill

Use this skill when:
- Writing TLA+ specifications
- Modeling concurrent systems
- Verifying system properties
- Performing formal verification
- Debugging with model checking

Do NOT use this skill when:
- Formal methods not needed
- Simple systems easily tested
- TLA+ expertise unavailable
- Time constraints prohibit formal methods

## Input Format

```yaml
spec_request:
  system_description: string    # System to model
  properties_to_verify: array   # Invariants/liveness
  language: string              # TLA+ or PlusCal
  model_check: boolean         # Run model checker
```

## Output Format

```yaml
spec_result:
  specification: string         # Generated TLA+ code
  invariants: array             # Defined invariants
  properties_verified: object   # Model checking results
  counter_examples: array      # Any violations found
```

## Capabilities

### 1. System Modeling (15 min)

- Capture system behavior
- Define system states
- Model transitions
- Represent concurrency

### 2. Property Definition (15 min)

- Define invariants
- Specify liveness properties
- Define safety properties
- Express temporal logic

### 3. Specification Writing (20 min)

- Write TLA+ modules
- Create PlusCal algorithms
- Define constants and variables
- Structure specifications

### 4. Model Checking (15 min)

- Configure model checker
- Run TLC model checker
- Analyze counterexamples
- Verify properties

### 5. Debugging (10 min)

- Interpret errors
- Fix specification issues
- Refine models
- Verify fixes

## Usage Examples

### Basic Usage

"Write a TLA+ spec for this concurrent system."

### Advanced Usage

"Full spec with invariants and model checking."

## Configuration Options

- `language`: TLA+ or PlusCal
- `model_check`: Run TLC checker
- `depth`: Model checking depth
- `parallelism`: TLC workers

## Constraints

- MUST produce valid TLA+
- SHOULD verify properties
- MUST explain model checking results
- SHOULD provide examples

## Integration Examples

- Critical systems: Verify correctness
- Concurrent code: Find race conditions
- Protocols: Verify behavior
- Formal methods: Teach TLA+

## Dependencies

- TLA+ tools (TLC model checker)
- PlusCal parser
- Python 3.10+ for utilities
