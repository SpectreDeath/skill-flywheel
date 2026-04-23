"
Repeated Game Analyzer

Analyzes repeated/iterated strategic interactions:
- Finite horizon effects
- Infinite horizon / folk theorems
- Trigger strategies
- Tit-for-tat analysis
- Collusion in oligopoly
"

from typing import Any, Dict, List
from datetime import datetime


def repeated_game_analyzer(
    base_game: str,
    players: List[str],
    horizon: int,
    discount_factor: float = 0.9,
    strategies: Dict[str, str] | None = None,
    **kwargs,
) -> Dict[str, Any]:
    "
    Analyze repeated game scenarios.

    Args:
        base_game: Underlying one-shot game (prisoner, oligopoly, etc.)
        players: List of players
        horizon: Number of repetitions (1 = single shot, inf = infinite)
        discount_factor: Future payoffs discounted by this factor
        strategies: Named strategies for each player
        **kwargs: Additional parameters

    Returns:
        Repeated game analysis with equilibria and recommendations
    "

    base_game = base_game.lower().replace("-", "_").replace(" ", "_")

    if base_game in {"prisoner", "prisoners_dilemma"}:
        return _analyze_repeated_prisoners(
            players, horizon, discount_factor, strategies
        )
    elif base_game in {"oligopoly", "cournot"}:
        return _analyze_repeated_oligopoly(players, horizon, discount_factor)
    elif base_game == "coordination":
        return _analyze_repeated_coordination(players, horizon, discount_factor)
    elif base_game in {"chicken", "hawk_dove"}:
        return _analyze_repeated_chicken(players, horizon, discount_factor)
    else:
        return {"status": "error", "error": f"Unknown base game: {base_game}"}


def _analyze_repeated_prisoners(
    players: List[str], horizon: int, discount: float, strategies: Dict | None
) -> Dict[str, Any]:
    "Analyze repeated prisoner's dilemma"

    results = {
        "status": "success",
        "game": "repeated_prisoners_dilemma",
        "horizon": horizon,
        "discount_factor": discount,
    }

    # Finite horizon analysis
    if horizon < float("inf"):
        results["finite_horizon"] = {
            "equilibrium": "Subgame perfect: defect in every period",
            "reason": "Backward induction: last period = single-shot PD",
            "all_periods": "Defect in period T, then T-1, etc.",
            "outcome": "Mutual defection (P, P) each round",
        }

        if horizon <= 3:
            results["recommendations"] = [
                "Short horizon: defection is rational",
                "No room for cooperation in finite repeated game",
                "Consider making credible commitment to cooperate",
            ]
        else:
            results["recommendations"] = [
                f"Medium horizon ({horizon} rounds): tit-for-tat works",
                "Start cooperative, reciprocate defection",
                "Forgive after one defection if opponent cooperates",
            ]
    else:
        # Infinite horizon - folk theorems apply
        min_equilibrium_payoff = 1  # Mutual defection payoff
        max_payoff = horizon if horizon == float("inf") else 5 * horizon

        results["infinite_horizon"] = {
            "folk_theorem": "Any payoff above min-max is sustainable",
            "min_max_payoff": min_equilibrium_payoff,
            "feasible_payoffs": f"({min_equilibrium_payoff}, {max_payoff})",
        }

        results["equilibria"] = {
            "grim_trigger": {
                "description": "Cooperate until defection, then defect forever",
                "sustains": "Full cooperation if discount high enough",
                "condition": f"discount >= R/(R+P) where R=3, P=1: {3 / 4}",
            },
            "tit_for_tat": {
                "description": "Copy opponent's last move",
                "sustains": "Cooperation in deterministic environments",
                "robustness": "Responds to mistakes",
            },
            "grudge": {
                "description": "Cooperate for n rounds, then defect forever",
                "forgiving": "Not as forgiving as TFT",
            },
            "randomized": {
                "description": "Random cooperation/defection",
                "payoff": "Expected payoff with probability adjustment",
            },
        }

        results["recommendations"] = [
            "Infinite horizon: many equilibria possible (folk theorems)",
            f"With discount {discount}, cooperation sustainable if sufficiently patient",
            "Tit-for-tat recommended: nice, retaliatory, clear, forgiving",
            "Start with cooperation - establishes good equilibrium",
        ]

    return results


def _analyze_repeated_oligopoly(
    players: List[str], horizon: int, discount: float
) -> Dict[str, Any]:
    "Analyze repeated oligopoly (collusion)"

    n = len(players)

    # Cournot payoffs (simplified)
    monopoly_payoff = 100 / n  # If all produce less
    competitive_payoff = 10  # If all produce at competitive level
    deviation_payoff = 50  # If others collude, you deviate

    return {
        "status": "success",
        "game": "repeated_oligopoly",
        "horizon": horizon,
        "discount_factor": discount,
        "payoffs": {
            "monopoly": monopoly_payoff,
            "competitive": competitive_payoff,
            "deviation": deviation_payoff,
        },
        "collusion_analysis": {
            "sustainable": horizon == float("inf")
            or discount > competitive_payoff / deviation_payoff,
            "trigger_strategy": "Deviate triggers price war forever",
            "simple_collusion": "All produce less, share monopoly profits",
        },
        "recommendations": [
            f"With {n} firms, collusion more difficult but more profitable per firm",
            "Use trigger strategies to sustain collusion",
            "Frequent interactions (high discount) support collusion",
            "Watch for leniency programs that break collusion",
        ],
    }


def _analyze_repeated_coordination(
    players: List[str], horizon: int, discount: float
) -> Dict[str, Any]:
    "Analyze repeated coordination game"

    return {
        "status": "success",
        "game": "repeated_coordination",
        "horizon": horizon,
        "discount_factor": discount,
        "equilibrium_selection": {
            "risk_dominant": "Battle of the sexes: safer option",
            "payoff_dominant": "Pareto superior option",
        },
        "focal_points": {
            "description": "History or convention can select equilibrium",
            "examples": ["same location", "alphabetically first", "prior precedent"],
        },
        "recommendations": [
            "Repeated play helps coordinate on efficient outcome",
            "Communication before play aids coordination",
            "Establish precedent in early rounds",
            "Pure coordination games easier than incomplete info",
        ],
    }


def _analyze_repeated_chicken(
    players: List[str], horizon: int, discount: float
) -> Dict[str, Any]:
    "Analyze repeated chicken (hawk-dove) game"

    return {
        "status": "success",
        "game": "repeated_chicken",
        "horizon": horizon,
        "discount_factor": discount,
        "equilibria": {
            "alternation": {
                "description": "Players take turns yielding",
                "sustains": "Cooperative outcome",
            },
            "stalemate": {
                "description": "Both refuse to yield",
                "outcome": "Repeated (hawk, hawk) - mutual destruction",
            },
            "deterrence": {
                "description": "Credible threat to not yield",
                "wins": "Whoever is more committed wins",
            },
        },
        "recommendations": [
            "Chicken has no pure cooperative equilibrium",
            "Consider alternating: you yield next if I yield now",
            "Build reputation for being crazy (unpredictable)",
            "Make credible commitments to extract concessions",
        ],
    }


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    payload.get("action", "analyze")
    base_game = payload.get("base_game", "prisoner")
    players = payload.get("players", ["player1", "player2"])
    horizon = payload.get("horizon", 10)
    discount_factor = payload.get("discount_factor", 0.9)
    strategies = payload.get("strategies")

    result = repeated_game_analyzer(
        base_game=base_game,
        players=players,
        horizon=horizon,
        discount_factor=discount_factor,
        strategies=strategies,
    )

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    "Return skill metadata"
    return {
        "name": "repeated-game-analyzer",
        "description": "Analyze repeated/iterated games with trigger strategies and folk theorems",
        "version": "1.0.0",
        "domain": "STRATEGY",
    }
