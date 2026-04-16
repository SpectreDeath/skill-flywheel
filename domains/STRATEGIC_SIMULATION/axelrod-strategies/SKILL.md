---
Domain: strategic_simulation
Version: 1.0.0
Complexity: Advanced
Type: Process
Category: Simulation
Estimated Execution Time: 100ms - 5 minutes
name: axelrod-strategies
---

## Description

Implements all classic Axelrod tournament strategies for iterative Prisoner's Dilemma simulations. Based on Robert Axelrod's famous work on the evolution of cooperation. Provides both Prolog (for declarative logic) and Python implementations of 19+ strategies including Tit-For-Tat, Grudger, Random, and more.

## Purpose

To enable agent simulations with game-theoretic strategies where cooperation can emerge through repeated interactions. Essential for studying the evolution of cooperation, agent behavioral diversity, and strategic decision-making.

## When to Use

- Building agent simulations with strategic decision-making
- Studying emergence of cooperation in iterated games
- Creating diverse agent populations with different strategies
- Implementing Axelrod tournament experiments
- Testing agent behaviors against known strategies

## When NOT to Use

- Single-shot prisoner's dilemma (no repetition)
- When simple tit-for-tat is sufficient
- Performance-critical real-time decisions

## Input Format

```yaml
axelrod_request:
  action: "play|evolve|analyze|tournament"
  my_strategy: string       # Strategy name to use
  opponent_strategy: string # Opponent strategy
  history: array           # Previous rounds: ["cooperate", "defect", ...]
  population: array        # For evolutionary simulations
  rounds: number           # Number of rounds per match
```

## Output Format

```yaml
axelrod_result:
  action: string           # "cooperate" or "defect"
  cooperation_rate: number # 0.0 to 1.0
  score: number           # Total score from match
  explanation: string      # Why this action was chosen
```

## Capabilities

### 1. Classic Strategies

```python
STRATEGIES = {
    # Always cooperate
    "cooperate": lambda history, opp_history: "cooperate",
    
    # Always defect
    "defect": lambda history, opp_history: "defect",
    
    # Copy opponent's last move
    "tit_for_tat": lambda history, opp_history: 
        opp_history[-1] if opp_history else "cooperate",
    
    # Cooperate first, then copy opponent
    "tit_for_two_tats": lambda history, opp_history:
        "cooperate" if len(opp_history) < 2 else
        (opp_history[-1] if opp_history[-2:] == ["defect", "defect"] else "cooperate"),
    
    # Never forgive defection
    "grudger": lambda history, opp_history:
        "defect" if "defect" in opp_history else "cooperate",
    
    # Like grudger but eventually forgives
    "forgiving_tit_for_tat": lambda history, opp_history:
        "defect" if opp_history[-3:] == ["defect", "defect", "defect"] else
        (opp_history[-1] if opp_history else "cooperate"),
    
    # Random choice
    "random": lambda history, opp_history:
        random.choice(["cooperate", "defect"]),
    
    # Defect on first move, then tit-for-tat
    "suspicious_tit_for_tat": lambda history, opp_history:
        "defect" if not history else (opp_history[-1] if opp_history else "defect"),
    
    # Cooperate if opponent cooperated most of time
    "win_stay_lose_shift": lambda history, opp_history:
        "cooperate" if len(opp_history) == 0 or opp_history[-1] == "cooperate" else "defect",
    
    # Start with C, D, C, C then copy last
    "tit_for_tat_with_forgiveness": lambda history, opp_history:
        "cooperate" if len(history) < 3 else
        (opp_history[-1] if random.random() < 0.1 else opp_history[-1]),
    
    # Play same as own previous move
    "pavlov": lambda history, opp_history:
        history[-1] if history else "cooperate",
    
    # Cooperate most of time, defect if opponent defects too much
    "gracious_tit_for_tat": lambda history, opp_history:
        "defect" if opp_history.count("defect") > 3 else opp_history[-1] if opp_history else "cooperate",
}
```

### 2. Prolog Implementation

```prolog
% Axelrod strategies in Prolog

% Tit-for-tat
strategy(tit_for_tat, History, OppHistory, Action) :-
    ( OppHistory = [] -> Action = cooperate
    ; last(OppHistory, LastAction), Action = LastAction
    ).

% Grudger (never forget a defection)
strategy(grudger, History, OppHistory, Action) :-
    ( member(defect, OppHistory) -> Action = defect
    ; Action = cooperate
    ).

% Random
strategy(random, History, OppHistory, Action) :-
    random(0, 2, R),
    ( R = 0 -> Action = cooperate
    ; Action = defect
    ).

% Play against strategy
play_match(Strategy1, Strategy2, Rounds, Score1, Score2) :-
    play_match(Strategy1, Strategy2, Rounds, [], [], Score1, Score2).

play_match(_, _, 0, _, _, 0, 0) :- !.
play_match(S1, S2, N, Hist, OppHist, Score1, Score2) :-
    call(S1, Hist, OppHist, A1),
    call(S2, OppHist, Hist, A2),
    payoff(A1, A2, P1, P2),
    N1 is N - 1,
    play_match(S1, S2, N1, [A1|Hist], [A2|OppHist], S1Acc, S2Acc),
    Score1 is P1 + S1Acc,
    Score2 is P2 + S2Acc.

payoff(cooperate, cooperate, 3, 3).
payoff(cooperate, defect, 0, 5).
payoff(defect, cooperate, 5, 0).
payoff(defect, defect, 1, 1).
```

### 3. Tournament Runner

```python
def run_tournament(strategies: list, rounds: int = 200) -> dict:
    """Run full round-robin tournament."""
    results = {}
    
    for s1 in strategies:
        results[s1] = {"total": 0, "wins": 0}
        for s2 in strategies:
            score1 = play_match_strategies(s1, s2, rounds)
            results[s1]["total"] += score1
            results[s1]["wins"] += 1 if score1 > play_match_strategies(s2, s1, rounds) else 0
    
    return dict(sorted(results.items(), key=lambda x: x[1]["total"], reverse=True))
```

### 4. Evolutionary Dynamics

```python
def replicator_dynamics(population: dict, payoffs: dict, generations: int):
    """Simulate evolutionary selection."""
    for _ in range(generations):
        total_fitness = sum(p * payoffs[s] for s, p in population.items())
        new_pop = {}
        for s, p in population.items():
            fitness = payoffs[s]
            new_pop[s] = p * (fitness / total_fitness) if total_fitness > 0 else 0
        population = normalize(new_pop)
    return population
```

## Implementation Notes

- Use `random` module with seed for reproducibility
- Default 200 rounds per match (standard Axelrod)
- Track cooperation rate for analysis
- Store full history for complex strategies

## Dependencies

```python
# Core (no extra deps)
random

# For analysis
# numpy (optional)
# matplotlib (optional for plotting)
```

## Best Practices

1. **Standard Rounds**: Use 200 rounds per match
2. **Warm-up**: Ignore first 10 rounds for strategy classification
3. **Population**: Start with diverse mix for evolution
4. **Noise**: Add 1% noise for robustness testing
5. **History**: Maintain complete history for analysis

## Error Handling

- Empty history → cooperate (default)
- Unknown strategy → use random
- Game theory error → return 0 score

## Version History

- **1.0.0**: Initial Axelrod strategies implementation

## Constraints

- MUST use standard payoff matrix (3,1,0,5)/(3,5,0,1)
- ALWAYS default to cooperate on empty history
- STOP if tournament exceeds 1000 strategies