---
Domain: strategic_simulation
Version: 1.0.0
Complexity: Advanced
Type: Tool
Category: Integration
Estimated Execution Time: 100ms - 1 second
name: prolog-agent-reasoning
---

## Description

Python-Prolog bridge for agent behavioral reasoning. Provides seamless integration between Python agent systems and Prolog logic engines, with automatic fallback to pure Python when Prolog is unavailable.

## Purpose

To enable agents to use declarative Prolog logic for decision-making while maintaining Python compatibility and graceful degradation.

## When to Use

- Building agents that need game-theoretic or logical reasoning
- Connecting Python simulation frameworks with Prolog knowledge bases
- Creating explainable AI systems with transparent reasoning
- Implementing complex behavioral logic that benefits from Prolog

## When NOT to Use

- Simple decision logic that doesn't need logical inference
- When Prolog dependencies cannot be installed
- Real-time systems requiring sub-millisecond latency

## Input Format

```yaml
bridge_request:
  action: "decide|query|consult|explain"
  profile: object           # AgentProfile with traits and resources
  opponent_history: array   # List of opponent actions
  prolog_file: string      # Optional custom Prolog file
```

## Output Format

```yaml
bridge_result:
  action: string            # Chosen action
  reasoning: string         # Explanation
  trace: array              # Decision trace
  prolog_used: boolean      # Whether Prolog was available
```

## Capabilities

### 1. Prolog Engine Initialization

```python
class PrologBridge:
    def __init__(self, prolog_file: Path | None = None):
        self.prolog_file = prolog_file or self._default_traits_file()
        self._prolog = None
        self._loaded = False
        self._init_prolog()
    
    def _init_prolog(self):
        try:
            from pyswip import Prolog
            self._prolog = Prolog()
            self._prolog.consult(str(self.prolog_file))
            self._loaded = True
        except ImportError:
            logger.warning("pyswip not available, using Python fallback")
```

### 2. Decision Making

```python
def decide(self, profile: AgentProfile, opponent_history: list) -> DecisionResult:
    prolog_history = self._to_prolog_history(opponent_history)
    
    if self._loaded and self._prolog is not None:
        return self._prolog_decide(profile, prolog_history)
    else:
        return self._python_fallback_decide(profile, opponent_history)

def _prolog_decide(self, profile, history):
    query = f"decide({profile.to_prolog()}, {history}, Action)"
    for solution in self._prolog.query(query):
        return DecisionResult(
            action=solution['Action'],
            reasoning=self._get_reasoning_trace(profile, history),
            trace=[]
        )
```

### 3. Python Fallback

```python
def _python_fallback_decide(self, profile, history):
    """Pure Python implementation when Prolog unavailable."""
    
    if 'aggression' in profile.traits and profile.resources > 5:
        return DecisionResult(action='escalate', reasoning='aggression trait')
    
    if 'pacifist' in profile.traits:
        return DecisionResult(action='deescalate', reasoning='pacifist trait')
    
    if history:
        last_action = history[-1]
        if 'reciprocity' in profile.traits:
            return DecisionResult(action=last_action, reasoning='reciprocity')
        
        if 'tit_for_tat' in profile.traits:
            return DecisionResult(action=last_action, reasoning='tit_for_tat')
    
    # Default: majority vote
    cooperations = history.count('deescalate')
    escalations = history.count('escalate')
    action = 'deescalate' if cooperations >= escalations else 'escalate'
    return DecisionResult(action=action, reasoning='default majority')
```

### 4. Query Interface

```python
def query(self, goal: str) -> list[dict]:
    """Query Prolog knowledge base directly."""
    if not self._loaded:
        return []
    
    results = []
    for solution in self._prolog.query(goal):
        results.append(dict(solution))
    return results
```

### 5. Explain Decision

```python
def explain(self, profile: AgentProfile, history: list) -> str:
    """Get human-readable explanation of decision."""
    if self._loaded:
        result = self._prolog.query(
            f"trace_decide({profile.to_prolog()}, {history}, Action, Trace)"
        )
        return f"Matched rule: {result[0]['Trace']}"
    else:
        return "Python fallback: rule-based decision"
```

### 6. Dynamic Fact Assertion

```python
def assert_fact(self, fact: str):
    """Assert new fact into Prolog knowledge base."""
    if self._loaded:
        self._prolog.assertz(fact)

def retract_fact(self, fact: str):
    """Retract fact from Prolog knowledge base."""
    if self._loaded:
        self._prolog.retract(fact)
```

## Implementation Notes

- Always check `PYSWIP_AVAILABLE` before using Prolog
- Provide meaningful fallback behavior
- Log Prolog loading failures for debugging
- Use `to_prolog()` method for profile serialization

## Configuration Options

```yaml
prolog_bridge_config:
  prolog_file: string       # Path to .pl file
  strict: boolean           # Raise if Prolog unavailable
  fallback_enabled: boolean
  trace_enabled: boolean    # Return decision trace
```

## Best Practices

1. **Always Provide Fallback**: Never crash if Prolog unavailable
2. **Log Decisions**: Record decisions for analysis
3. **Validate Profile**: Ensure traits are in allowed list
4. **Test Both Paths**: Test both Prolog and Python implementations
5. **Version Prolog Files**: Track changes to .pl files

## Error Handling

- Prolog file not found → raise with helpful message
- Invalid query → return empty results, log warning
- Prolog crash → fall back to Python

## Dependencies

- pyswip (optional): `pip install pyswip`
- Prolog files in package data

## Version History

- **1.0.0**: Initial Prolog bridge implementation

## Constraints

- MUST have fallback when Prolog unavailable
- ALWAYS validate Prolog query syntax
- STOP if Prolog query times out (>5s)