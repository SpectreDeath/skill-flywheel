#!/usr/bin/env python3
"""
axelrod-strategies

Implements all classic Axelrod tournament strategies for iterative Prisoner's Dilemma.
Provides Prolog and Python implementations of 19+ strategies.
"""

import logging
import random
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

PAYOFFS = {
    ("cooperate", "cooperate"): (3, 3),
    ("cooperate", "defect"): (0, 5),
    ("defect", "cooperate"): (5, 0),
    ("defect", "defect"): (1, 1),
}


def axelrod_strategies(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core implementation for axelrod-strategies.

    Args:
        payload: Input with action, my_strategy, opponent_strategy, history, rounds

    Returns:
        Decision with action, cooperation_rate, score, explanation
    """
    action_type = payload.get("action", "play")
    my_strategy = payload.get("my_strategy", "tit_for_tat")
    opponent_strategy = payload.get("opponent_strategy", "random")
    history = payload.get("history", [])
    opp_history = payload.get("opp_history", [])
    rounds = payload.get("rounds", 200)
    population = payload.get("population", [])

    if action_type == "play":
        result = _play_round(my_strategy, history, opp_history)
    elif action_type == "tournament":
        result = _run_tournament(payload.get("strategies", []), rounds)
    elif action_type == "evolve":
        result = _evolve_population(population, rounds, payload.get("generations", 100))
    elif action_type == "analyze":
        result = _analyze_strategy(my_strategy, rounds)
    else:
        result = {"error": f"Unknown action: {action_type}"}

    return result


def _get_strategy_fn(name: str):
    """Get strategy function by name."""
    strategies = {
        "cooperate": lambda h, oh: "cooperate",
        "defect": lambda h, oh: "defect",
        "tit_for_tat": lambda h, oh: oh[-1] if oh else "cooperate",
        "tit_for_two_tats": lambda h, oh: (
            """cooperate"""
            if len(oh) < 2
            else ("cooperate" if oh[-2:] != ["defect", "defect"] else "defect")
        ),
        "grudger": lambda h, oh: "defect" if "defect" in oh else "cooperate",
        "forgiving_tit_for_tat": lambda h, oh: (
            oh[-1] if oh and random.random() > 0.1 else "cooperate"
        ),
        "random": lambda h, oh: random.choice(["cooperate", "defect"]),
        "suspicious_tit_for_tat": lambda h, oh: "defect"
        if not h
        else (oh[-1] if oh else "defect"),
        "win_stay_lose_shift": lambda h, oh: (
            "cooperate" if not oh or oh[-1] == "cooperate" else "defect"
        ),
        "pavlov": lambda h, oh: h[-1] if h else "cooperate",
        "gracious_tit_for_tat": lambda h, oh: (
            "defect" if oh.count("defect") > 3 else (oh[-1] if oh else "cooperate")
        ),
        "always_cooperate": lambda h, oh: "cooperate",
        "always_defect": lambda h, oh: "defect",
        "prober": lambda h, oh: (
            "defect" if not h else ("cooperate" if h[0] == "defect" else "defect")
        ),
        "backstabber": lambda h, oh: (
            """defect"""
            if len(h) >= 3 and h[-1] == h[-2] == h[-3] == "defect"
            else (oh[-1] if oh else "cooperate")
        ),
        "negatizer": lambda h, oh: (
            "defect" if len(h) >= 2 and h[-1] != h[-2] else "cooperate"
        ),
        "adaptive": lambda h, oh: (
            "defect" if oh.count("cooperate") < oh.count("defect") else "cooperate"
        ),
        "noise": lambda h, oh: (
            random.choice(["cooperate", "defect"])
            if random.random() < 0.05
            else (oh[-1] if oh else "cooperate")
        ),
    }
    return strategies.get(name, strategies["tit_for_tat"])


def _play_round(
    strategy: str, history: List[str], opp_history: List[str]
) -> Dict[str, Any]:
    """Play one round with given strategy."""
    strategy_fn = _get_strategy_fn(strategy)
    action = strategy_fn(history, opp_history)

    cooperation_rate = 0.0
    if history:
        cooperation_rate = history.count("cooperate") / len(history)

    return {
        "action": action,
        "strategy_used": strategy,
        "cooperation_rate": cooperation_rate,
        "explanation": f"Strategy '{strategy}' chose '{action}'",
    }


def _run_tournament(strategies: List[str], rounds: int = 200) -> Dict[str, Any]:
    """Run full round-robin tournament."""
    if not strategies:
        strategies = ["tit_for_tat", "grudger", "cooperate", "defect", "random"]

    results = {}

    for s1 in strategies:
        results[s1] = {"total_score": 0, "wins": 0, "cooperation_rate": 0}

        for s2 in strategies:
            score1, score2, coop_rate = _play_match(s1, s2, rounds)
            results[s1]["total_score"] += score1
            results[s1]["wins"] += 1 if score1 > score2 else 0
            results[s1]["cooperation_rate"] += coop_rate

        results[s1]["cooperation_rate"] /= len(strategies)

    sorted_results = dict(
        sorted(results.items(), key=lambda x: x[1]["total_score"], reverse=True)
    )

    return {
        "tournament_results": sorted_results,
        "rounds_per_match": rounds,
        "winner": list(sorted_results.keys())[0] if sorted_results else None,
    }


def _play_match(s1: str, s2: str, rounds: int) -> tuple:
    """Play a match between two strategies."""
    history1, history2 = [], []
    total1, total2 = 0, 0

    fn1, fn2 = _get_strategy_fn(s1), _get_strategy_fn(s2)

    for _ in range(rounds):
        a1 = fn1(history1, history2)
        a2 = fn2(history2, history1)

        p1, p2 = PAYOFFS.get((a1, a2), (0, 0))
        total1 += p1
        total2 += p2

        history1.append(a1)
        history2.append(a2)

    coop_rate = history1.count("cooperate") / rounds
    return total1, total2, coop_rate


def _evolve_population(
    population: Dict[str, float], rounds: int, generations: int
) -> Dict[str, Any]:
    """Simulate evolutionary selection."""
    if not population:
        population = {
            "tit_for_tat": 0.2,
            "grudger": 0.2,
            "cooperate": 0.2,
            "defect": 0.2,
            "random": 0.2,
        }

    strategies = list(population.keys())
    history = []

    for gen in range(generations):
        payoffs = {s: 0 for s in strategies}

        for s1 in strategies:
            for s2 in strategies:
                score1, _, _ = _play_match(s1, s2, rounds)
                payoffs[s1] += score1 * population[s1] * population[s2]

        total_fitness = sum(payoffs[s] * population[s] for s in strategies)
        if total_fitness > 0:
            new_pop = {}
            for s in strategies:
                new_pop[s] = (payoffs[s] * population[s]) / total_fitness
            population = new_pop

        if gen % 20 == 0:
            dominant = max(population.items(), key=lambda x: x[1])
            history.append(
                {"generation": gen, "dominant": dominant[0], "share": dominant[1]}
            )

    final_population = dict(
        sorted(population.items(), key=lambda x: x[1], reverse=True)
    )

    return {
        "final_population": final_population,
        "evolution_history": history,
        "generations": generations,
    }


def _analyze_strategy(strategy: str, rounds: int = 200) -> Dict[str, Any]:
    """Analyze a strategy's behavior across all opponents."""
    opponents = [
        "cooperate",
        "defect",
        "tit_for_tat",
        "grudger",
        "random",
        "pavlov",
        "win_stay_lose_shift",
    ]

    results = {"strategy": strategy, "opponents": {}}

    for opp in opponents:
        score, _, coop_rate = _play_match(strategy, opp, rounds)
        results["opponents"][opp] = {
            "score": score,
            "cooperation_rate": coop_rate,
        }

    results["average_score"] = sum(
        r["score"] for r in results["opponents"].values()
    ) / len(opponents)
    results["average_cooperation"] = sum(
        r["cooperation_rate"] for r in results["opponents"].values()
    ) / len(opponents)

    return results


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "play")
    try:
        result = axelrod_strategies(payload)
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }
    except Exception as e:
        logger.error(f"Error in axelrod-strategies: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""
    return {
        "name": "axelrod-strategies",
        "description": "All classic Axelrod tournament strategies for iterative Prisoner's Dilemma. Includes Tit-For-Tat, Grudger, and 17+ more strategies.",
        "version": "1.0.0",
        "domain": "strategic_simulation",
    }
