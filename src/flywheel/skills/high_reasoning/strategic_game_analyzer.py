#!/usr/bin/env python3
"""
Strategic Game Theory Analyzer with Datalog + Prolog Surfaces

Uses Datalog for modeling player relationships, payoffs, and strategies
and Prolog for analyzing game equilibria and optimal strategies.

This skill demonstrates how relational knowledge (Datalog) can inform
logical game theory analysis (Prolog) for complex strategic scenarios.
"""

from pathlib import Path
from typing import Dict, Any, List

# Surface definitions
_base_path = Path(__file__).parent

# Datalog surface for relational game modeling
DATALOG_SURFACE = (_base_path / "strategic_game_analyzer.dl").read_text()

# Prolog surface for game theory logic and equilibrium analysis
PROLOG_SURFACE = (_base_path / "strategic_game_analyzer.pl").read_text()


def strategic_game_analyzer(game_type: str, players: List[str], **params) -> Dict[str, Any]:
    """
    Analyze strategic games using relational and logical reasoning.

    Args:
        game_type: Type of game ('prisoners_dilemma', 'chicken', 'staghunt', etc.)
        players: List of players/agents
        **params: Game parameters (payoffs, strategies, etc.)

    Returns:
        Strategic analysis with equilibria and recommendations
    """
    try:
        from pyDatalog import pyDatalog
    except ImportError:
        return {"error": "pyDatalog not available", "analysis": {}}

    try:
        from pyswip import Prolog
    except ImportError:
        return {"error": "SWI-Prolog not available", "analysis": {}}

    # Initialize Datalog for relational game modeling
    pyDatalog.clear()
    pyDatalog.create_terms('player, strategy, payoff, relationship, dominates, nash_equilibrium')
    pyDatalog.create_terms('X, Y, Z, P1, P2, S1, S2')

    # Load Datalog knowledge base
    try:
        pyDatalog.load(DATALOG_SURFACE)
    except Exception as e:
        return {"error": f"Failed to load Datalog surface: {e}", "analysis": {}}

    # Add game-specific facts
    for player in players:
        pyDatalog.assert_fact('player', player)

    # Add game type and parameters
    pyDatalog.assert_fact('game_type', game_type)

    # Query relational aspects (player relationships, strategy sets)
    relational_analysis = _analyze_relational_aspects(pyDatalog, players, game_type)

    # Initialize Prolog for logical game analysis
    prolog = Prolog()
    temp_pl = Path(f"data/temp_strategic_{hash(str(players))}.pl")
    temp_pl.parent.mkdir(exist_ok=True)
    temp_pl.write_text(PROLOG_SURFACE)
    prolog.consult(str(temp_pl))

    # Add game facts to Prolog
    for player in players:
        prolog.assertz(f"player('{player}')")
    prolog.assertz(f"game_type('{game_type}')")

    # Query logical aspects (equilibria, optimal strategies)
    logical_analysis = _analyze_logical_aspects(prolog, players, game_type)

    # Synthesize results
    return {
        "game_type": game_type,
        "players": players,
        "relational_analysis": relational_analysis,
        "logical_analysis": logical_analysis,
        "strategic_recommendations": _synthesize_strategic_recommendations(
            relational_analysis, logical_analysis
        )
    }


def _analyze_relational_aspects(datalog_engine, players: List[str], game_type: str) -> Dict[str, Any]:
    """Use Datalog to analyze relational aspects of the game"""
    try:
        # Query strategy relationships
        strategy_query = datalog_engine.ask("strategy_relationship(X, Y, Relation)")
        strategy_relationships = [{"from": r[0], "to": r[1], "relation": r[2]}
                                 for r in strategy_query.answers] if strategy_query else []

        # Query payoff structures
        payoff_query = datalog_engine.ask("payoff_structure(Player, Strategy, Payoff)")
        payoff_structure = [{"player": r[0], "strategy": r[1], "payoff": r[2]}
                           for r in payoff_query.answers] if payoff_query else []

        # Query dominant strategies
        dominant_query = datalog_engine.ask("dominant_strategy(Player, Strategy)")
        dominant_strategies = [{"player": r[0], "strategy": r[1]}
                              for r in dominant_query.answers] if dominant_query else []

        return {
            "strategy_relationships": strategy_relationships,
            "payoff_structure": payoff_structure,
            "dominant_strategies": dominant_strategies,
            "player_network": _build_player_network(players)
        }
    except Exception as e:
        return {"error": str(e), "relationships": []}


def _analyze_logical_aspects(prolog_engine, players: List[str], game_type: str) -> Dict[str, Any]:
    """Use Prolog to analyze logical aspects of game theory"""
    try:
        # Query Nash equilibria
        nash_solutions = list(prolog_engine.query("nash_equilibrium(Equilibrium)"))
        nash_equilibria = [str(sol['Equilibrium']) for sol in nash_solutions if sol]

        # Query Pareto optimal outcomes
        pareto_solutions = list(prolog_engine.query("pareto_optimal(Outcome)"))
        pareto_optimal = [str(sol['Outcome']) for sol in pareto_solutions if sol]

        # Query cooperative vs competitive analysis
        coop_query = list(prolog_engine.query("cooperative_advantage(Advantage)"))
        cooperative_advantages = [str(sol['Advantage']) for sol in coop_query if sol]

        return {
            "nash_equilibria": nash_equilibria,
            "pareto_optimal": pareto_optimal,
            "cooperative_advantages": cooperative_advantages,
            "game_classification": _classify_game_type(game_type)
        }
    except Exception as e:
        return {"error": str(e), "equilibria": []}


def _build_player_network(players: List[str]) -> Dict[str, List[str]]:
    """Build a simple player relationship network"""
    # This would be more sophisticated in a real implementation
    network = {}
    for player in players:
        network[player] = [p for p in players if p != player]
    return network


def _classify_game_type(game_type: str) -> Dict[str, Any]:
    """Classify game characteristics"""
    classifications = {
        "prisoners_dilemma": {
            "type": "non-cooperative",
            "equilibria": "single dominant",
            "social_optimum": "not achievable",
            "cooperation_challenge": "high"
        },
        "chicken": {
            "type": "non-cooperative",
            "equilibria": "multiple asymmetric",
            "social_optimum": "achievable",
            "cooperation_challenge": "medium"
        },
        "staghunt": {
            "type": "coordination",
            "equilibria": "multiple symmetric",
            "social_optimum": "achievable",
            "cooperation_challenge": "low"
        }
    }
    return classifications.get(game_type, {"type": "unknown"})


def _synthesize_strategic_recommendations(relational: Dict, logical: Dict) -> List[str]:
    """Synthesize strategic recommendations from multi-surface analysis"""
    recommendations = []

    # Nash equilibrium recommendations
    if logical.get("nash_equilibria"):
        recommendations.append(f"Consider Nash equilibrium strategies: {', '.join(logical['nash_equilibria'])}")

    # Cooperative advantage analysis
    if logical.get("cooperative_advantages"):
        recommendations.append(f"Cooperative advantages identified: {', '.join(logical['cooperative_advantages'])}")

    # Dominant strategy considerations
    if relational.get("dominant_strategies"):
        dom_strats = [f"{ds['player']}->{ds['strategy']}" for ds in relational["dominant_strategies"]]
        recommendations.append(f"Dominant strategies: {', '.join(dom_strats)}")

    # Game type specific advice
    game_class = logical.get("game_classification", {})
    if game_class.get("cooperation_challenge") == "high":
        recommendations.append("High cooperation challenge - consider incentive alignment")
    elif game_class.get("cooperation_challenge") == "low":
        recommendations.append("Low cooperation challenge - focus on coordination mechanisms")

    return recommendations if recommendations else ["No specific recommendations - analyze game structure further"]


def register_skill():
    """Register this skill with metadata"""
    return {
        "name": "strategic_game_analyzer",
        "description": "Multi-surface strategic game theory analysis combining relational modeling with logical equilibrium analysis",
        "version": "1.0.0",
        "domain": "HIGH_REASONING",
        "surfaces": ["datalog", "prolog"],
        "capabilities": [
            "game_equilibrium_analysis",
            "strategy_relationship_modeling",
            "cooperative_vs_competitive_analysis",
            "payoff_structure_reasoning",
            "multi_player_network_analysis"
        ]
    }