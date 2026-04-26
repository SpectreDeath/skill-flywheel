# Agent Guidelines - Karpathy-Inspired Principles

This directory contains skills enhanced with behavioral guidelines derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

## Overview

Skills in this directory implement the **Collective-Mind Architecture** (Python + Prolog + Hy/Lisp) with **behavioral guardrails** that enforce:

1. **Think Before Coding** - State assumptions explicitly, surface confusion, push back when warranted
2. **Simplicity First** - Minimum code that solves the problem, no speculative features
3. **Surgical Changes** - Touch only what's necessary, clean up only your own mess
4. **Goal-Driven Execution** - Define and verify success criteria before implementation

## Available Skills

| Skill | Domain | Description |
|-------|--------|-------------|
| [sat_solver_optimization](sat_solver_optimization.py) | LOGIC | Enhanced SAT solver using Prolog (constraints), Hy (heuristics), Python (orchestration) |
| [belief_revision](belief_revision.py) | EPISTEMOLOGY | Belief revision with logical consistency checking and assumption tracking |
| [bayesian_networks](bayesian_networks.py) | PROBABILISTIC_MODELS | Bayesian inference combining probabilistic logic, heuristics, and inference algorithms |

## Behavioral Profiles

Skills can be invoked with different behavioral strictness levels:

- **`karpathy_strict`** - All principles enforced strictly (production-critical work)
- **`karpathy_balanced`** - Recommended for most engineering work (default)
- **`karpathy_minimal`** - Core principles only (rapid prototyping)
- **`production_critical`** - Maximum quality enforcement (safety-sensitive systems)
- **`rapid_prototype`** - Goals only (quick experiments)

## Usage

### With Behavioral Orchestrator

```python
from flywheel.behavioral.orchestrator import BehavioralOrchestrator
from flywheel.core.skills import EnhancedSkillManager

# Initialize
skill_manager = EnhancedSkillManager(skills_dir='src/flywheel/skills')
orchestrator = BehavioralOrchestrator(skill_manager)

# Invoke with behavioral guidelines
result = orchestrator.invoke(
    skill_name="sat-solver-optimization",
    payload={
        "clauses": [["P", "Q"], ["-P", "R"]],
        "variables": ["P", "Q", "R"]
    },
    profile="karpathy_balanced"  # Behavioral strictness
)

print(f"Quality Score: {result['quality_report']['overall_score']:.2f}")
print(f"Grade: {result['quality_report']['grade']}")
```

### Direct Invocation (without behavioral layer)

```python
from flywheel.skills.high_reasoning.sat_solver_optimization import sat_solver_optimization

result = sat_solver_optimization({
    "clauses": [["P", "Q"], ["-P", "R"]],
    "variables": ["P", "Q", "R"]
})
```

## What the Behavioral Layer Does

### Pre-Execution
- **Simplicity Check** - Warns if problem seems simple but solution might overcomplicate
- **Assumption Tracking** - Identifies implicit assumptions that should be explicit

### Post-Execution
- **Complexity Validation** - Ensures solution isn't over-engineered
- **Surgical Change Verification** - Confirms changes are minimal and focused
- **Goal Verification** - Checks all success criteria are met

### Quality Scoring
Each skill execution receives an A-F grade based on:
- Simplicity (25% weight)
- Assumption clarity (20% weight)
- Change focus/surgical precision (25% weight)
- Goal achievement (30% weight)

## Architecture

Each skill implements three surfaces:

1. **Prolog Surface** (`.pl`) - Symbolic logic, constraints, reasoning
2. **Hy Surface** (`.hy`) - Heuristic strategies, pattern matching, adaptive scoring
3. **Python Surface** (`.py`) - Orchestration, I/O, result formatting

The behavioral guidelines cross-cut all three surfaces, ensuring disciplined reasoning regardless of the computational approach.

## Configuration

Behavioral profiles are defined in `src/flywheel/behavioral/profiles.py`. Each profile specifies:

- Which principles to enforce
- Complexity thresholds
- Assumption tracking requirements
- Change magnitude limits
- Minimum quality score to pass

## Examples

See [test_behavioral_layer.py](https://github.com/SpectreDeath/skill-flywheel/blob/main/test_behavioral_layer.py) for comprehensive examples.

## Adding New Skills

1. Create skill in `high_reasoning/` with `.py`, `.pl`, and `.hy` files
2. Register in `high_reasoning/__init__.py`
3. Invoke through `BehavioralOrchestrator` for guideline enforcement
4. Profile will be auto-detected from skill metadata

## Benefits

- **Fewer Mistakes**: Explicit assumptions surface before they cause errors
- **Simpler Code**: Hard constraints on complexity prevent over-engineering
- **Focused Changes**: Surgical checks ensure minimal touch
- **Clear Success**: Goal-driven execution means you know when you're done
- **Measurable Quality**: A-F grades make quality objective, not subjective

## License

MIT - See repository root for details.