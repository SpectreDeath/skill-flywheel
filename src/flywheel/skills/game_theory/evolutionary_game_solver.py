"""
Evolutionary Game Solver

Analyzes evolutionary stable strategies and dynamics:
- Replicator dynamics
- Evolutionary stability
- Population games
- Hawk-Dove / Chicken game analysis
"""

from typing import Any, Dict, List
from datetime import datetime


def evolutionary_game_solver(
    game_type: str,
    population: Dict[str, float] | None = None,
    payoff_matrix: Dict[str, Dict[str, float]] | None = None,
    generations: int = 50,
    mutation_rate: float = 0.01,
    **kwargs,
) -> Dict[str, Any]:
    "
    Solve evolutionary game theory scenarios.

    Args:
        game_type: Type of evolutionary game (hawk_dove, coordination, prisoner, custom)
        population: Initial population frequencies (strategy -> proportion)
        payoff_matrix: Payoff matrix (strategy -> opponent_strategy -> payoff)
        generations: Number of generations to simulate
        mutation_rate: Probability of random strategy change
        **kwargs: Additional parameters

    Returns:
        Evolutionary stable strategies and dynamics
    "

    # Set up game
    if game_type.lower() == "hawk_dove":
        payoff_matrix = payoff_matrix or {
            "hawk": {"hawk": -10, "dove": 15},
            "dove": {"dove": 0, "hawk": -10},
        }
        population = population or {"hawk": 0.5, "dove": 0.5}
    elif game_type.lower() == "coordination":
        payoff_matrix = payoff_matrix or {
            "a": {"a": 10, "b": 0},
            "b": {"a": 0, "b": 10},
        }
        population = population or {"a": 0.5, "b": 0.5}
    elif game_type.lower() == "prisoner":
        payoff_matrix = payoff_matrix or {
            "cooperate": {"cooperate": 3, "defect": 0},
            "defect": {"cooperate": 5, "defect": 1},
        }
        population = population or {"cooperate": 0.5, "defect": 0.5}
    elif not payoff_matrix:
        return {
            "status": "error",
            "error": "Must provide payoff_matrix for custom games",
        }

    # Normalize population
    strategies = list(payoff_matrix.keys())
    if not population:
        population = {s: 1.0 / len(strategies) for s in strategies}

    # Check valid population
    total = sum(population.values())
    if abs(total - 1.0) > 0.001:
        population = {k: v / total for k, v in population.items()}

    # Run replicator dynamics
    trajectory = _replicator_dynamics(
        population, payoff_matrix, generations, mutation_rate
    )

    # Find ESS
    ess = _find_evolutionary_stable_strategies(payoff_matrix)

    return {
        "status": "success",
        "game_type": game_type,
        "initial_population": population,
        "final_population": trajectory[-1] if trajectory else population,
        "trajectory": trajectory[:10],  # First 10 generations
        "equilibrium": ess,
        "generations": generations,
    }


def _replicator_dynamics(
    initial_pop: Dict[str, float],
    payoff_matrix: Dict[str, Dict[str, float]],
    generations: int,
    mutation_rate: float,
) -> List[Dict[str, float]]:
    "Run replicator dynamics simulation"

    population = initial_pop.copy()
    trajectory = [population.copy()]
    strategies = list(population.keys())

    for _gen in range(generations):
        # Calculate fitness for each strategy
        fitness = {}
        for strategy in strategies:
            fit = 0
            for opponent in strategies:
                fit += population[opponent] * payoff_matrix[strategy][opponent]
            fitness[strategy] = fit

        # Average fitness
        avg_fitness = sum(population[s] * fitness[s] for s in strategies)

        # Replicator equation: x'_i = x_i * (f_i - avg_fitness)
        new_pop = {}
        for strategy in strategies:
            if avg_fitness != 0:
                growth_rate = fitness[strategy] / avg_fitness
                new_pop[strategy] = population[strategy] * growth_rate
            else:
                new_pop[strategy] = population[strategy]

        # Apply mutation after all strategies are initialized
        if mutation_rate > 0:
            mutation_total = dict.fromkeys(strategies, 0.0)
            for strategy in strategies:
                for other in strategies:
                    if other != strategy:
                        mutation_amount = population[strategy] * mutation_rate
                        mutation_total[other] = (
                            mutation_total.get(other, 0) + mutation_amount
                        )
                        mutation_total[strategy] = (
                            mutation_total.get(strategy, 0) - mutation_amount
                        )

            for strategy in strategies:
                new_pop[strategy] += mutation_total.get(strategy, 0)

        # Ensure non-negative
        for strategy in strategies:
            new_pop[strategy] = max(0, new_pop[strategy])

        # Normalize
        total = sum(new_pop.values())
        if total > 0:
            population = {k: v / total for k, v in new_pop.items()}

        trajectory.append(population.copy())

    return trajectory


def _find_evolutionary_stable_strategies(
    payoff_matrix: Dict[str, Dict[str, float]],
) -> Dict[str, Any]:
    "Find evolutionary stable strategies"

    strategies = list(payoff_matrix.keys())

    # Check pure strategy ESS
    pure_ess = []
    for strategy in strategies:
        is_ess = True

        # Check against each mutant strategy
        for mutant in strategies:
            if mutant == strategy:
                continue

            # ESS condition: either
            # 1. Payoff(strategy, strategy) > Payoff(mutant, strategy), OR
            # 2. Payoff(strategy, strategy) = Payoff(mutant, strategy) AND
            #    Payoff(strategy, mutant) > Payoff(mutant, mutant)

            v_ss = payoff_matrix[strategy][strategy]
            v_ms = payoff_matrix[mutant][strategy]
            v_sm = payoff_matrix[strategy][mutant]
            v_mm = payoff_matrix[mutant][mutant]

            if v_ss <= v_ms and (v_ss != v_sm or v_sm <= v_mm):
                is_ess = False
                break

        if is_ess:
            pure_ess.append(strategy)

    # Check for mixed ESS (simplified)
    mixed_ess = _find_mixed_equilibrium(payoff_matrix)

    return {
        "pure_ess": pure_ess,
        "mixed_ess": mixed_ess,
    }


def _find_mixed_equilibrium(
    payoff_matrix: Dict[str, Dict[str, float]],
) -> Dict[str, float] | None:
    "Find symmetric mixed equilibrium (simplified 2-strategy case)"

    strategies = list(payoff_matrix.keys())
    if len(strategies) != 2:
        return None

    s1, s2 = strategies

    # For two strategies, find mixing that equalizes fitness
    # v1(s1) + (1-p)*v1(s2) = v2(s1) + (1-p)*v2(s2)
    # where p is freq of s1

    v1_s1 = payoff_matrix[s1][s1]
    v1_s2 = payoff_matrix[s1][s2]
    v2_s1 = payoff_matrix[s2][s1]
    v2_s2 = payoff_matrix[s2][s2]

    # Solve for p
    if v1_s1 - v2_s1 - v1_s2 + v2_s2 != 0:
        p = (v2_s2 - v2_s1) / (v1_s1 - v2_s1 - v1_s2 + v2_s2)
        p = max(0, min(1, p))  # Clamp to [0, 1]
        return {s1: p, s2: 1 - p}

    return None


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    payload.get("action", "solve")
    game_type = payload.get("game_type", "hawk_dove")
    population = payload.get("population")
    payoff_matrix = payload.get("payoff_matrix")
    generations = payload.get("generations", 50)
    mutation_rate = payload.get("mutation_rate", 0.01)

    result = evolutionary_game_solver(
        game_type=game_type,
        population=population,
        payoff_matrix=payoff_matrix,
        generations=generations,
        mutation_rate=mutation_rate,
    )

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """ Return skill metadata """

if __name__ == "__main__":
    return {
            "name": "evolutionary-game-solver",
            "description": "Analyze evolutionary stable strategies and replicator dynamics",
            "version": "1.0.0",
            "domain": "STRATEGY",
        }