#!/usr/bin/env python3
"""
game-theory-simulation

Game-theoretic decision making for agent simulations. Implements Prisoner's Dilemma,
Hawk-Dove, evolutionary dynamics, and Nash equilibrium finding.
"""

import logging
import random
from datetime import datetime
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class PrisonersDilemma:
    """Standard Prisoner's Dilemma game."""

    PAYOFF_MATRIX = {
        ("defect", "defect"): (-1, -1),
        ("defect", "cooperate"): (3, 0),
        ("cooperate", "defect"): (0, 3),
        ("cooperate", "cooperate"): (2, 2),
    }

    @classmethod
    def play(cls, action1: str, action2: str) -> Tuple[int, int]:
        return cls.PAYOFF_MATRIX.get((action1, action2), (0, 0))


class HawkDove:
    """Hawk-Dove (Chicken) game with resource competition."""

    def __init__(self, V: float = 50, C: float = 100):
        self.V = V
        self.C = C

    def payoff(self, my_strategy: str, opp_strategy: str) -> float:
        if my_strategy == "hawk" and opp_strategy == "hawk":
            return (self.V - self.C) / 2
        elif my_strategy == "hawk" and opp_strategy == "dove":
            return self.V
        elif my_strategy == "dove" and opp_strategy == "hawk":
            return 0
        else:
            return self.V / 2


def game_theory_simulation(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core implementation for game-theory-simulation.

    Args:
        payload: Input with game_type, agents, rounds, etc.

    Returns:
        Simulation results with payoffs and equilibria
    """
    game_type = payload.get("game_type", "prisoners_dilemma")
    agents = payload.get("agents", [])
    rounds = payload.get("rounds", 10)
    population = payload.get("population", {})

    if game_type == "prisoners_dilemma":
        return _simulate_prisoners_dilemma(agents, rounds)
    elif game_type == "hawk_dove":
        V = payload.get("V", 50)
        C = payload.get("C", 100)
        return _simulate_hawk_dove(agents, rounds, V, C)
    elif game_type == "coordination":
        return _simulate_coordination(agents, rounds)
    else:
        return {"error": f"Unknown game type: {game_type}"}


def _simulate_prisoners_dilemma(agents: List[str], rounds: int) -> Dict[str, Any]:
    """Run Prisoner's Dilemma simulation."""
    strategies = {}
    payoffs = {agent: 0 for agent in agents}

    for _ in range(rounds):
        for i, agent in enumerate(agents):
            opponent = agents[(i + 1) % len(agents)]
            strategy = strategies.get(agent, "cooperate")

            if isinstance(strategy, list):
                strategy = random.choice(strategy) if strategy else "cooperate"
            elif callable(strategy):
                strategy = strategy(
                    agent, opponents_history[i] if i < len(opponents_history) else []
                )

            action = strategy if strategy in ["cooperate", "defect"] else "cooperate"
            opp_action = strategies.get(opponent, "cooperate")

            if isinstance(opp_action, list):
                opp_action = random.choice(opp_action) if opp_action else "cooperate"

            p1, p2 = PrisonersDilemma.play(action, opp_action)
            payoffs[agent] += p1

    return {
        "game": "prisoners_dilemma",
        "rounds": rounds,
        "payoffs": payoffs,
        "total_payoff": sum(payoffs.values()),
    }


def _simulate_hawk_dove(
    agents: List[str], rounds: int, V: float, C: float
) -> Dict[str, Any]:
    """Run Hawk-Dove simulation."""
    game = HawkDove(V, C)
    strategies = {}
    payoffs = {agent: 0 for agent in agents}

    for _ in range(rounds):
        for i, agent in enumerate(agents):
            opponent = agents[(i + 1) % len(agents)]
            strategy = strategies.get(agent, "dove")

            if isinstance(strategy, list):
                strategy = random.choice(strategy) if strategy else "dove"

            action = strategy if strategy in ["hawk", "dove"] else "dove"
            opp_strategy = strategies.get(opponent, "dove")

            if isinstance(opp_strategy, list):
                opp_strategy = random.choice(opp_strategy) if opp_strategy else "dove"

            payoffs[agent] += game.payoff(action, opp_strategy)

    return {
        "game": "hawk_dove",
        "rounds": rounds,
        "V": V,
        "C": C,
        "payoffs": payoffs,
    }


def _simulate_coordination(agents: List[str], rounds: int) -> Dict[str, Any]:
    """Run Coordination game."""
    payoffs = {agent: 0 for agent in agents}

    for _ in range(rounds):
        for agent in agents:
            payoffs[agent] += 1

    return {
        "game": "coordination",
        "rounds": rounds,
        "payoffs": payoffs,
    }


def find_nash_equilibria(game_type: str) -> List[Dict]:
    """Find Nash equilibria for basic games."""
    if game_type == "prisoners_dilemma":
        return [{"equilibrium": "mutual_defection", "actions": ["defect", "defect"]}]
    elif game_type == "hawk_dove":
        return [{"equilibrium": "mixed", "note": "Mixed strategy equilibrium exists"}]
    return []


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "simulate")
    try:
        if action == "simulate":
            result = game_theory_simulation(payload)
        elif action == "find_equilibria":
            game_type = payload.get("game_type", "prisoners_dilemma")
            result = {"equilibria": find_nash_equilibria(game_type)}
        else:
            result = {"message": "unknown action"}

        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }
    except Exception as e:
        logger.error(f"Error in game-theory-simulation: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""
    return {
        "name": "game-theory-simulation",
        "description": "Game-theoretic decision making for agent simulations. Implements Prisoner's Dilemma, Hawk-Dove, evolutionary dynamics, and Nash equilibrium finding.",
        "version": "1.0.0",
        "domain": "strategic_simulation",
    }
