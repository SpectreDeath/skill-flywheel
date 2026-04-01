"""
Game Theory Negotiator

Models game theory scenarios for negotiation strategy:
- Nash equilibrium analysis
- Payoff matrix evaluation
- Strategy recommendations
- Negotiation tactics
"""

from typing import Any, Dict, List
from datetime import datetime


def analyze_payoff_matrix(payoffs: Dict) -> Dict[str, Any]:
    """Analyze payoff matrix for game theory insights"""

    players = list(payoffs.keys())
    if len(players) < 2:
        return {"error": "Need at least 2 players"}

    strategies = list(payoffs[players[0]].keys())

    # Find best responses for each player
    best_responses = {}
    for player in players:
        player_payoffs = payoffs[player]
        best = max(player_payoffs.items(), key=lambda x: x[1])
        best_responses[player] = {"strategy": best[0], "payoff": best[1]}

    # Check for dominant strategy
    dominant_strategies = {}
    for player in players:
        player_payoffs = payoffs[player]
        first_payoff = list(player_payoffs.values())[0]
        if all(p == first_payoff for p in player_payoffs.values()):
            dominant_strategies[player] = list(player_payoffs.keys())[0]

    return {
        "players": players,
        "strategies": strategies,
        "best_responses": best_responses,
        "dominant_strategies": dominant_strategies,
    }


def calculate_nash_equilibrium(payoffs: Dict) -> List[Dict]:
    """Find Nash equilibrium points"""
    equilibria = []

    players = list(payoffs.keys())
    strategies = list(payoffs[players[0]].keys())

    for strategy in strategies:
        is_equilibrium = True
        equilibrium_point = {}

        for player in players:
            current_payoff = payoffs[player][strategy]
            equilibrium_point[player] = {"strategy": strategy, "payoff": current_payoff}

            # Check if player can improve by deviating
            best_alternative = max(payoffs[player].values())
            if current_payoff < best_alternative:
                is_equilibrium = False

        if is_equilibrium:
            equilibria.append(equilibrium_point)

    return equilibria


def game_theory_negotiator(
    scenario: str,
    players: List[str],
    strategies: Dict[str, List[str]],
    payoffs: Dict[str, Dict[str, float]],
    **kwargs,
) -> Dict[str, Any]:
    """
    Model game theory scenarios for negotiation.

    Args:
        scenario: Description of the negotiation scenario
        players: List of players/parties
        strategies: Dict of available strategies per player
        payoffs: Payoff matrix
        **kwargs: Additional parameters

    Returns:
        Game theory analysis with strategy recommendations
    """
    if not players or not payoffs:
        return {"status": "error", "error": "Incomplete game data"}

    # Analyze payoff matrix
    matrix_analysis = analyze_payoff_matrix(payoffs)

    # Find Nash equilibrium
    equilibria = calculate_nash_equilibrium(payoffs)

    # Calculate expected values (assuming equal probability)
    expected_values = {}
    for player, player_payoffs in payoffs.items():
        expected_values[player] = sum(player_payoffs.values()) / len(player_payoffs)

    # Generate recommendations
    recommendations = []

    if equilibria:
        recommendations.append(f"Nash equilibrium exists: {equilibria[0]}")
    else:
        recommendations.append("No pure Nash equilibrium - consider mixed strategies")

    # Identify best/worst outcomes
    best_outcome = max(sum(payoffs[p].values()) / len(payoffs[p]) for p in players)
    worst_outcome = min(sum(payoffs[p].values()) / len(payoffs[p]) for p in players)

    recommendations.append(f"Best possible outcome: {best_outcome}")
    recommendations.append(f"Worst case scenario: {worst_outcome}")

    # Suggest tactics based on scenario type
    if "collaborative" in scenario.lower() or "cooperative" in scenario.lower():
        recommendations.append("Consider cooperative strategies for mutual gain")
    elif "competitive" in scenario.lower() or "zero-sum" in scenario.lower():
        recommendations.append(
            "Adopt competitive strategy - focus on relative advantage"
        )
    else:
        recommendations.append("Balance competitive and cooperative elements")

    return {
        "status": "success",
        "scenario": scenario,
        "players": players,
        "analysis": matrix_analysis,
        "nash_equilibria": equilibria,
        "expected_values": expected_values,
        "recommendations": recommendations,
    }


async def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "analyze")
    scenario = payload.get("scenario", "")
    players = payload.get("players", [])
    strategies = payload.get("strategies", {})
    payoffs = payload.get("payoffs", {})

    if action == "analyze":
        result = game_theory_negotiator(scenario, players, strategies, payoffs)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata"""
    return {
        "name": "game-theory-negotiator",
        "description": "Model game theory scenarios for negotiation strategy",
        "version": "1.0.0",
        "domain": "STRATEGY",
    }
