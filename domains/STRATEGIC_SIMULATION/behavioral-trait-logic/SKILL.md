---
Domain: strategic_simulation
Version: 1.0.0
Complexity: Advanced
Type: Process
Category: Logic Programming
Estimated Execution Time: 50ms - 2 minutes
name: behavioral-trait-logic
---

## Description

Prolog-based behavioral trait system for agent decision-making. Implements game-theoretic behavioral strategies including reciprocity, tit-for-tat, forgiveness, grudger, pacifist, and aggression. Provides full decision logic with history tracking and theory of mind capabilities.

## Purpose

To create declarative behavioral logic that can be queried and reasoned about, enabling transparent agent decision-making where the reasoning trace can be examined and verified.

## When to Use

- Building agents with complex behavioral strategies
- Implementing game-theoretic strategies in Prolog
- Creating interpretable AI systems where decisions can be explained
- Modeling opponent modeling and theory of mind

## When NOT to Use

- Simple rule-based behaviors without history dependency
- When Prolog is not available (use pure Python fallback)
- Performance-critical real-time decisions (use compiled code)

## Input Format

```yaml
trait_request:
  traits: array              # [reciprocity, forgiveness, aggression, tit_for_tat, grudger, pacifist]
  history: array            # List of opponent actions: [escalate, deescalate, ...]
  resources: number         # Agent resource level (affects aggression)
  tom_level: number         # Theory of Mind depth (0-2)
```

## Output Format

```yaml
trait_result:
  action: "escalate" | "deescalate"
  rule_used: string         # Which rule matched
  reasoning: string         # Human-readable explanation
  trace: array              # Decision trace
```

## Capabilities

### 1. Core Behavioral Rules

```prolog
% RECIPROCITY - Mirror opponent's last move
rule(profile(Traits,_), History, Action) :-
    member(trait(reciprocity), Traits),
    last(History, LastAction), !,
    Action = LastAction.

% TIT_FOR_TAT - Copy first move, then reciprocate
rule(profile(Traits,_), History, Action) :-
    member(trait(tit_for_tat), Traits), !,
    ( length(History, 0) -> Action = deescalate
    ; last(History, LastAction), Action = LastAction
    ).

% FORGIVENESS - Forgive after 2 cooperations
rule(profile(Traits,_), History, Action) :-
    member(trait(forgiveness), Traits), !,
    ( length(History, L), L < 3 -> Action = deescalate
    ; count_cooperations(History, Coop),
      count_defections(History, Def),
      ( Def = 1, Coop >= 2 -> Action = deescalate
      ; last(History, Action)
      )
    ).

% GRUDGER - Never cooperate after defection
rule(profile(Traits,_), History, Action) :-
    member(trait(grudger), Traits), !,
    ( has_defected(History) -> Action = escalate
    ; Action = deescalate
    ).

% AGGRESSION - Escalate if resources > 5
rule(profile(Traits, Resources, _), _, escalate) :-
    member(trait(aggression), Traits),
    Resources > 5.0, !.

% PACIFIST - Always deescalate
rule(profile(Traits,_,_), _, deescalate) :-
    member(trait(pacifist), Traits), !.
```

### 2. Helper Predicates

```prolog
% Count cooperations in history
count_cooperations([], 0).
count_cooperations([H|T], Count) :-
    ( H = deescalate -> count_cooperations(T, C), Count is C + 1
    ; count_cooperations(T, Count)
    ).

% Check if history contains defection
has_defected([escalate|_]) :- !.
has_defected([_|T]) :- has_defected(T).
```

### 3. Theory of Mind

```prolog
% Level 0: Direct knowledge
believes(Agent, Fact) :- Fact =.. [P|_], call(P, _).

% Level 1: Agent models another's beliefs
believes(Agent, believes(OtherAgent, Fact)) :-
    not(Agent = OtherAgent),
    can_reason_about(Agent, OtherAgent).

% Level 2: Detect deception
believes(Agent, deceptive(OtherAgent, Fact)) :-
    believes(Agent, believes(OtherAgent, HiddenFact)),
    HiddenFact \= Fact,
    has_theory_of_mind(Agent, 2).
```

### 4. Payoff Matrix

```prolog
% Prisoner's Dilemma payoff matrix
payoff(escalate, escalate, 0, -1).
payoff(escalate, deescalate, 3, -2).
payoff(deescalate, escalate, -2, 3).
payoff(deescalate, deescalate, 1, 1).
```

### 5. Decision Entry Point

```prolog
decide(Profile, History, Action) :- rule(Profile, History, Action).

trace_decide(Profile, History, Action, Trace) :-
    findall(RuleUsed, (rule(Profile, History, Action), RuleUsed = Action), Rules),
    ( Rules = [Action|_] -> Trace = matched(Action)
    ; Trace = default_fallback
    ).
```

## Implementation Notes

- Use pyswip for Python-Prolog bridge
- Fall back to pure Python when Prolog unavailable
- Track reasoning trace for explainability
- Use cut (!) strategically to prevent backtracking

## Best Practices

1. **Test Each Rule**: Verify each trait rule independently
2. **Track History**: Maintain action history per opponent
3. **Explain Decisions**: Return reasoning trace with each decision
4. **Handle Edge Cases**: Empty history, unknown traits
5. **Evolutionary Fitness**: Calculate fitness against trait pools

## Error Handling

- Unknown trait → use default behavior
- Empty history → start cooperative (deescalate)
- Prolog unavailable → fall back to Python implementation

## Version History

- **1.0.0**: Initial behavioral trait logic based on Strategify traits.pl

## Constraints

- MUST validate traits against known trait list
- ALWAYS return reasoning trace for transparency
- STOP if infinite loop detected in rule chaining