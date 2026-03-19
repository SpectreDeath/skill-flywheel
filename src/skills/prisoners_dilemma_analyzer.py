"""
Prisoner's Dilemma Analyzer

Analyzes classic and extended prisoner's dilemma scenarios:
- Nash equilibrium identification
- Cooperation/defection strategies
- Tit-for-tat analysis
- Evolutionary stability
"""

from typing import Any, Dict, List


def prisoners_dilemma_analyzer(
    scenario: str,
    num_rounds: int = 1,
    player1_strategy: str = "unknown",
    player2_strategy: str = "unknown",
    cooperation_reward: float = 3,
    defection_temptation: float = 5,
    sucker_payoff: float = 0,
    punishment: float = 1,
    **kwargs,
) -> Dict[str, Any]:
    """
    Analyze prisoner's dilemma scenarios.

    Args:
        scenario: Description of the dilemma scenario
        num_rounds: Number of rounds (1 = single shot, >1 = iterated)
        player1_strategy: Known strategy of player 1
        player2_strategy: Known strategy of player 2
        cooperation_reward: Payoff when both cooperate (R)
        defection_temptation: Payoff when you defect, they cooperate (T)
        sucker_payoff: Payoff when you cooperate, they defect (S)
        punishment: Payoff when both defect (P)
        **kwargs: Additional parameters

    Returns:
        Prisoner's dilemma analysis with equilibrium and recommendations
    """
    # Validate payoff matrix (T > R > P > S is standard PD)
    if not (defection_temptation > cooperation_reward > punishment > sucker_payoff):
        return {
            "status": "error",
            "error": "Invalid payoff matrix: T > R > P > S must hold",
        }

    results = {
        "status": "success",
        "scenario": scenario,
        "game_type": "iterated" if num_rounds > 1 else "single-shot",
        "num_rounds": num_rounds,
        "payoff_matrix": {
            "both_cooperate": cooperation_reward,
            "both_defect": punishment,
            "you_cooperate_they_defect": sucker_payoff,
            "you_defect_they_cooperate": defection_temptation,
        },
    }

    # Analyze single-shot game
    if num_rounds == 1:
        results["equilibrium"] = {
            "type": "pure Nash equilibrium",
            "outcome": "both_defect",
            "payoff": punishment,
            "reason": "In single-shot PD, defection is dominant strategy",
        }
        results["recommendations"] = [
            "Single-shot PD always leads to mutual defection",
            "No incentive to deviate when other defects",
            "Consider external enforcement for cooperation",
        ]
    else:
        # Analyze iterated PD
        equilibrium_analysis = _analyze_iterated_pd(
            num_rounds,
            cooperation_reward,
            defection_temptation,
            sucker_payoff,
            punishment,
        )
        results["equilibrium"] = equilibrium_analysis
        results["recommendations"] = _get_iterated_recommendations(
            num_rounds, player1_strategy, player2_strategy
        )

    # Compare known strategies
    if player1_strategy != "unknown" and player2_strategy != "unknown":
        results["strategy_comparison"] = _compare_strategies(
            player1_strategy,
            player2_strategy,
            cooperation_reward,
            defection_temptation,
            sucker_payoff,
            punishment,
            num_rounds,
        )

    return results


def _analyze_iterated_pd(
    num_rounds: int, R: float, T: float, S: float, P: float
) -> Dict[str, Any]:
    """Analyze iterated prisoner's dilemma"""

    if num_rounds == float("inf"):
        return {
            "type": "subgame perfect equilibrium with trigger strategies",
            "outcome": "depends on strategies",
            "analysis": "With infinite rounds, cooperative equilibria possible via grim trigger or tit-for-tat",
        }

    # For finite repeated games, backwards induction gives defect-defect
    if num_rounds > 1:
        return {
            "type": "subgame perfect equilibrium",
            "outcome": "mutual defection",
            "payoff_per_round": P,
            "total_payoff": P * num_rounds,
            "analysis": "Backwards induction: defect in last round, then all previous",
            "exception": "If players are sufficiently patient or rounds uncertain, cooperation possible",
        }

    return {}


def _get_iterated_recommendations(num_rounds: int, p1: str, p2: str) -> List[str]:
    """Generate recommendations for iterated PD"""

    recs = []

    if num_rounds > 10 or num_rounds == float("inf"):
        recs.append("Long horizon favors tit-for-tat or similar cooperative strategies")
        recs.append("Start with cooperation, then mirror opponent's last move")
    elif num_rounds <= 3:
        recs.append(
            "Short horizon: defection is rational (last round is single-shot PD)"
        )
        recs.append("Consider making credible commitment to cooperate")
    else:
        recs.append("Medium horizon: tit-for-tat recommended")
        recs.append("Be nice, be retaliatory, be clear, be forgiving")

    if p1 != "unknown" and p2 != "unknown":
        recs.append(f"Player 1: {p1}, Player 2: {p2}")

    return recs


def _compare_strategies(
    p1: str,
    p2: str,
    R: float,
    T: float,
    S: float,
    P: float,
    rounds: int,
) -> Dict[str, Any]:
    """Compare two known strategies"""

    strategies = {
        "cooperate": R if p2 != "defect" else S,
        "defect": T if p2 != "defect" else P,
    }

    return {
        "player1_choice": p1,
        "player2_choice": p2,
        "player1_payoff": strategies.get(p1, "unknown"),
        "recommendation": f"{p1} vs {p2} yields {strategies.get(p1, '?')}",
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "analyze")
    scenario = payload.get("scenario", "")
    num_rounds = payload.get("num_rounds", 1)
    p1_strategy = payload.get("player1_strategy", "unknown")
    p2_strategy = payload.get("player2_strategy", "unknown")

    # Payoff matrix (can customize)
    R = payload.get("cooperation_reward", 3)
    T = payload.get("defection_temptation", 5)
    S = payload.get("sucker_payoff", 0)
    P = payload.get("punishment", 1)

    if action == "analyze":
        result = prisoners_dilemma_analyzer(
            scenario=scenario,
            num_rounds=num_rounds,
            player1_strategy=p1_strategy,
            player2_strategy=p2_strategy,
            cooperation_reward=R,
            defection_temptation=T,
            sucker_payoff=S,
            punishment=P,
        )
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata"""
    return {
        "name": "prisoners-dilemma-analyzer",
        "description": "Analyze prisoner's dilemma scenarios with equilibrium analysis",
        "version": "1.0.0",
        "domain": "STRATEGY",
    }
