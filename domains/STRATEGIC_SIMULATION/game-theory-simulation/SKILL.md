---
Domain: strategic_simulation
Version: 1.0.0
Complexity: Advanced
Type: Process
Category: Simulation
Estimated Execution Time: 100ms - 5 minutes
name: game-theory-simulation
---

## Description

Game-theoretic decision making framework for agent-based simulations. Provides implementation of strategic interactions including Prisoner's Dilemma, Hawk-Dove, coordination games, and evolutionary game theory with fitness calculations.

## Purpose

To create agent simulations where strategic decision-making emerges from mathematical game theory rather than hard-coded rules. Supports multiple equilibria concepts, evolutionary stability, and mixed strategy sampling.

## When to Use

- Building agent simulations with strategic interactions
- Implementing evolutionary dynamics where agent behaviors evolve
- Creating multi-agent systems with competitive/cooperative behaviors
- Modeling negotiation, conflict, or resource allocation scenarios

## When NOT to Use

- Simple rule-based agent behaviors without strategic interaction
- Single-agent planning without opponent modeling
- When game theory is not appropriate (e.g., deterministic environments)

## Input Format

```yaml
simulation_request:
  game_type: string        # "prisoners_dilemma", "hawk_dove", "coordination"
  agents: array            # List of agent configurations
  rounds: number           # Number of interaction rounds
  population: object       # For evolutionary simulations
```

## Output Format

```yaml
simulation_result:
  actions: array           # Chosen actions per agent
  payoffs: object          # Payoff results
  equilibria: array        # Found Nash equilibria
  trajectories: array      # Evolutionary trajectories
```

## Capabilities

### 1. Prisoner's Dilemma Implementation

```python
class PrisonersDilemma:
    PAYOFF_MATRIX = {
        ("defect", "defect"): (-1, -1),
        ("defect", "cooperate"): (3, 0),
        ("cooperate", "defect"): (0, 3),
        ("cooperate", "cooperate"): (2, 2),
    }
    
    def play(self, action1, action2):
        return self.PAYOFF_MATRIX[(action1, action2)]
```

### 2. Hawk-Dove (Chicken) Game

```python
class HawkDove:
    """Resource competition with escalating costs."""
    
    def __init__(self, V=50, C=100):
        self.V = V  # Value of resource
        self.C = C  # Cost of fighting
    
    def payoff(self, my_strategy, opp_strategy):
        if my_strategy == "hawk" and opp_strategy == "hawk":
            return (self.V - self.C) / 2
        elif my_strategy == "hawk" and opp_strategy == "dove":
            return self.V
        elif my_strategy == "dove" and opp_strategy == "hawk":
            return 0
        else:  # both dove
            return self.V / 2
```

### 3. Evolutionary Stability

```python
def is_evolutionarily_stable(strategy, mutant_payoff, resident_payoff):
    """Check if strategy is evolutionarily stable."""
    return mutant_payoff < resident_payoff

def replicator_dynamics(population, payoffs):
    """Replicator equation for evolutionary dynamics."""
    new_pop = []
    avg_fitness = sum(p * f for p, f in zip(population, payoffs))
    for p, f in zip(population, payoffs):
        new_pop.append(p * (f - avg_fitness))
    return normalize(new_pop)
```

### 4. Nash Equilibrium Finding

```python
def find_nash_equilibria(game):
    """Find mixed strategy Nash equilibria."""
    # For 2x2 games, analytical solutions exist
    # For larger games, use linear programming or iterative methods
    pass
```

### 5. Multi-Agent Tournament

```python
class Tournament:
    def run(self, strategies, rounds=100):
        results = {}
        for s1 in strategies:
            for s2 in strategies:
                # Play round robin
                pass
        return self.rank_strategies(results)
```

## Implementation Notes

- Start with 2x2 games before scaling
- Track population dynamics over time for evolutionary analysis
- Use Monte Carlo for stochastic策略 selection
- Consider repeated games for reputation effects

## Configuration Options

```yaml
game_theory_config:
  game_type: "prisoners_dilemma|hawk_dove|coordination|stag_hunt"
  rounds: number
  noise: number                    # Mutation probability
  population_size: number
  selection_method: "replicator|fitness_proportional|tournament"
```

## Best Practices

1. **Start Simple**: Implement 2x2 games first
2. **Verify Payoffs**: Ensure matrix represents intended incentives
3. **Track Dynamics**: Record population changes over time
4. **Multiple Equilibria**: Consider both pure and mixed strategies
5. **Evolutionary Analysis**: Study long-term stability of strategies

## Error Handling

- Invalid strategy combinations → return (0, 0) payoffs
- Convergence failure → return last stable state
- Empty agent list → return empty results

## Version History

- **1.0.0**: Initial game theory simulation framework

## Constraints

- MUST validate payoff matrix symmetry
- ALWAYS normalize population after replicator dynamics
- STOP if simulation diverges (population goes negative)