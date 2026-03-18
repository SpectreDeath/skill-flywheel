"""
Coordination Game Solver

Helps resolve coordination problems:
- Pure coordination games
- Battle of the Sexes
- Stag Hunt
- Network effects
- Focal points (Schelling points)
"""

from typing import Dict, List, Any, Optional, Tuple


def coordination_game_solver(
    game_type: str,
    players: List[str],
    options: Optional[List[str]] = None,
    payoffs: Optional[Dict[str, Dict[str, float]]] = None,
    preferences: Optional[Dict[str, List[str]]] = None,
    communication: bool = False,
    **kwargs,
) -> Dict[str, Any]:
    """
    Solve coordination game scenarios.

    Args:
        game_type: Type of coordination game (pure, battle_sexes, stag_hunt, network, custom)
        players: List of players
        options: Available coordination options
        payoffs: Custom payoff matrix
        preferences: Player preference rankings over options
        communication: Whether players can communicate
        **kwargs: Additional parameters

    Returns:
        Coordination solutions and recommendations
    """

    if game_type.lower() == "pure":
        return _solve_pure_coordination(players, options, payoffs)
    elif game_type.lower() == "battle_sexes" or game_type.lower() == "battleofthesexes":
        return _solve_battle_sexes(players, options, preferences)
    elif game_type.lower() == "stag_hunt":
        return _solve_stag_hunt(players, options)
    elif game_type.lower() == "network":
        return _solve_network_effects(players, options)
    elif payoffs:
        return _solve_custom_coordination(players, options, payoffs, communication)
    else:
        return {
            "status": "error",
            "error": "Unknown game type or no payoff matrix provided",
        }


def _solve_pure_coordination(
    players: List[str], options: Optional[List[str]], payoffs: Optional[Dict]
) -> Dict[str, Any]:
    """Pure coordination game - multiple equilibria with equal payoffs"""

    if not options:
        options = ["A", "B"]
    elif isinstance(options, list) and len(options) == 1:
        options = options + [f"alt_{options[0]}"]

    # Pure coordination: both prefer same outcome
    if not payoffs:
        payoffs = {}
        for opt in options:
            payoffs[opt] = {o: 10 if o == opt else 0 for o in options}

    equilibria = _find_pure_equilibria(payoffs)
    focal_points = _find_focal_points(options)

    return {
        "status": "success",
        "game_type": "pure_coordination",
        "equilibria": equilibria,
        "focal_points": focal_points,
        "recommendations": [
            f"Any of {equilibria} are stable equilibria",
            f"Use focal point: {focal_points[0] if focal_points else options[0]}",
            "Communication helps select preferred equilibrium",
        ],
    }


def _solve_battle_sexes(
    players: List[str], options: Optional[List[str]], preferences: Optional[Dict]
) -> Dict[str, Any]:
    """Battle of the Sexes - misaligned preferences"""

    if not options:
        options = ["opera", "football"]

    if not preferences and len(players) >= 2:
        preferences = {
            players[0]: [options[0], options[1]],  # Player 1 prefers opera
            players[1]: [options[1], options[0]],  # Player 2 prefers football
        }

    # Payoff matrix for BoS
    if not preferences:
        payoffs = {
            options[0]: {options[0]: (10, 5), options[1]: (0, 0)},
            options[1]: {options[0]: (0, 0), options[1]: (5, 10)},
        }
    else:
        payoffs = _build_payoffs_from_preferences(players, options, preferences)

    equilibria = _find_pure_equilibria(payoffs)
    mixed = _calculate_battle_sexes_mixed(players, options, payoffs)

    return {
        "status": "success",
        "game_type": "battle_sexes",
        "equilibria": equilibria,
        "mixed_equilibrium": mixed,
        "recommendations": [
            "Two pure Nash equilibria: (opera, opera) or (football, football)",
            "Mixed equilibrium: each player plays favorite 2/3 of time",
            "Communication or convention can select efficient outcome",
            "One player may sacrifice to follow the other (leadership)",
        ],
    }


def _solve_stag_hunt(
    players: List[str], options: Optional[List[str]]
) -> Dict[str, Any]:
    """Stag Hunt - safety vs. cooperation dilemma"""

    if not options:
        options = ["stag", "hare"]

    # Stag Hunt payoffs (security dominant vs. cooperative)
    payoffs = {
        "stag": {"stag": (10, 10), "hare": (0, 8)},
        "hare": {"stag": (8, 0), "hare": (8, 8)},
    }

    equilibria = ["stag_stag", "hare_hare"]

    return {
        "status": "success",
        "game_type": "stag_hunt",
        "equilibria": equilibria,
        "recommendations": [
            "Two equilibria: mutual stag (Pareto dominant) or mutual hare (safe)",
            "Stag is better but riskier - requires trust",
            "Once stag hunt succeeds, path dependence makes it stable",
            "Building trust increases chances of cooperative outcome",
        ],
        "risk_analysis": {
            "stag_stag": {"risk": "high", "reward": "high"},
            "hare_hare": {"risk": "low", "reward": "medium"},
        },
    }


def _solve_network_effects(
    players: List[str], options: Optional[List[str]]
) -> Dict[str, Any]:
    """Network effects coordination"""

    if not options:
        options = ["platform_a", "platform_b", "platform_c"]

    # Network effects create tipping dynamics
    return {
        "status": "success",
        "game_type": "network_effects",
        "analysis": {
            "phenomena": ["tipping", "lock_in", "network_externalities"],
            "expected_outcome": "single_platform_dominance",
        },
        "recommendations": [
            "Network effects cause winner-take-all dynamics",
            "Early adopters have outsized influence",
            "Consider compatibility with existing standards",
            "Look for platforms reaching critical mass",
            "Tipping point typically around 20-30% market share",
        ],
        "strategic_advice": {
            "for_platforms": [
                "First-mover advantage",
                "Subsidize early adopters",
                "Open APIs for ecosystem",
            ],
            "for_users": {
                "early": "Join growing network",
                "late": "Join dominant network",
            },
        },
    }


def _solve_custom_coordination(
    players: List[str], options: Optional[List[str]], payoffs: Dict, communication: bool
) -> Dict[str, Any]:
    """Solve custom coordination game"""

    equilibria = _find_pure_equilibria(payoffs)
    focal_points = _find_focal_points(options) if options else []

    recommendations = []
    if communication:
        recommendations.append(
            "Communication allows equilibrium selection through agreement"
        )
    if focal_points:
        recommendations.append(f"Focal points help: {focal_points}")

    return {
        "status": "success",
        "game_type": "custom",
        "equilibria": equilibria,
        "focal_points": focal_points,
        "recommendations": recommendations,
    }


def _build_payoffs_from_preferences(
    players: List[str], options: List[str], preferences: Dict
) -> Dict:
    """Build payoff matrix from preference rankings"""
    payoffs = {}
    for opt1 in options:
        payoffs[opt1] = {}
        for opt2 in options:
            player_payoffs = []
            for player in players:
                rank = (
                    preferences.get(player, []).index(opt2)
                    if opt2 in preferences.get(player, [])
                    else len(options)
                )
                payoff = len(options) - rank
                player_payoffs.append(payoff)
            payoffs[opt1][opt2] = tuple(player_payoffs)
    return payoffs


def _find_pure_equilibria(payoffs: Dict) -> List[str]:
    """Find pure Nash equilibria"""
    equilibria = []
    options = list(payoffs.keys())

    for opt1 in options:
        for opt2 in options:
            # Check if (opt1, opt2) is Nash equilibrium
            # Neither player can improve by deviating
            is_equilibrium = True

            # Get payoffs
            if isinstance(payoffs[opt1][opt2], tuple):
                p1_payoff, p2_payoff = payoffs[opt1][opt2]
            else:
                continue  # Need 2-player game

            # Check player 1 deviation
            for alt in options:
                if isinstance(payoffs[alt][opt2], tuple):
                    if payoffs[alt][opt2][0] > p1_payoff:
                        is_equilibrium = False
                        break
                elif isinstance(payoffs[alt][opt2], (int, float)):
                    if (
                        payoffs[alt][opt2] > p1_payoff
                        if isinstance(p1_payoff, (int, float))
                        else False
                    ):
                        is_equilibrium = False
                        break

            # Check player 2 deviation
            if is_equilibrium:
                for alt in options:
                    if isinstance(payoffs[opt1][alt], tuple):
                        if payoffs[opt1][alt][1] > p2_payoff:
                            is_equilibrium = False
                            break

            if is_equilibrium:
                equilibria.append(f"{opt1}_{opt2}")

    return equilibria


def _find_focal_points(options: List[str]) -> List[str]:
    """Schelling focal points - salient options"""
    focal = []

    # Check for common/standard options
    common_terms = ["standard", "default", "a", "1", "first"]
    for opt in options:
        opt_lower = opt.lower()
        if any(term in opt_lower for term in common_terms):
            focal.append(opt)

    # If no common terms, suggest first option
    if not focal and options:
        focal.append(options[0])

    return focal


def _calculate_battle_sexes_mixed(
    players: List[str], options: List[str], payoffs: Dict
) -> Dict:
    """Calculate mixed equilibrium for battle of the sexes"""

    # For BoS with payoffs (10,5) and (5,10)
    # Mixed equilibrium: P1 plays O 2/3, P2 plays F 2/3
    if len(options) >= 2:
        return {
            players[0]: {options[0]: 2 / 3, options[1]: 1 / 3},
            players[1]: {options[1]: 2 / 3, options[0]: 1 / 3},
        }
    return {}


def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "solve")
    game_type = payload.get("game_type", "pure")
    players = payload.get("players", ["player1", "player2"])
    options = payload.get("options")
    payoffs = payload.get("payoffs")
    preferences = payload.get("preferences")
    communication = payload.get("communication", False)

    result = coordination_game_solver(
        game_type=game_type,
        players=players,
        options=options,
        payoffs=payoffs,
        preferences=preferences,
        communication=communication,
    )

    return {"result": result}


def register_skill():
    """Return skill metadata"""
    return {
        "name": "coordination-game-solver",
        "description": "Solve coordination problems including pure coordination, battle of the sexes, and stag hunt",
        "version": "1.0.0",
        "domain": "STRATEGY",
    }
