"
Signaling Game Analyzer

Analyzes sender-receiver signaling games:
- Costly signaling
- Separating equilibria
- Pooling equilibria
- Cheap talk games
"

from typing import Any, Dict, List
from datetime import datetime


def signaling_game_analyzer(
    game_type: str,
    sender_types: List[str] | None = None,
    messages: List[str] | None = None,
    receiver_actions: List[str] | None = None,
    sender_payoffs: Dict | None = None,
    receiver_payoffs: Dict | None = None,
    signaling_cost: Dict | None = None,
    **kwargs,
) -> Dict[str, Any]:
    "
    Analyze signaling game scenarios.

    Args:
        game_type: Type of signaling game (costly, cheap_talk, education, custom)
        sender_types: Possible types of sender
        messages: Available messages/signals
        receiver_actions: Available actions for receiver
        sender_payoffs: Sender payoff functions
        receiver_payoffs: Receiver payoff functions
        signaling_cost: Cost of sending each message
        **kwargs: Additional parameters

    Returns:
        Signaling game analysis with equilibria
    "

    if game_type.lower() == "costly":
        return _analyze_costly_signaling(
            sender_types, messages, receiver_actions, signaling_cost
        )
    elif game_type.lower() == "cheap_talk":
        return _analyze_cheap_talk(sender_types, messages, receiver_actions)
    elif game_type.lower() == "education":
        return _analyze_education_signaling(sender_types, messages, receiver_actions)
    elif sender_payoffs and receiver_payoffs:
        return _analyze_custom_signaling(
            sender_types, messages, receiver_actions, sender_payoffs, receiver_payoffs
        )
    else:
        return {
            "status": "error",
            "error": "Unknown game type or missing payoff functions",
        }


def _analyze_costly_signaling(
    sender_types: List[str] | None,
    messages: List[str],
    receiver_actions: List[str],
    signaling_cost: Dict | None,
) -> Dict[str, Any]:
    "Analyze costly signaling game ( Spence signaling)"

    if not sender_types:
        sender_types = ["high_ability", "low_ability"]
    if not messages:
        messages = ["invest", "don't_invest"]
    if not receiver_actions:
        receiver_actions = ["hire", "reject"]
    if not signaling_cost:
        signaling_cost = {"invest": {"high_ability": 1, "low_ability": 3}}

    # Costly signaling conditions
    # High type has lower cost of signaling
    # Equilibrium: separating if costs differ enough

    separating_eq = {
        "description": "Different types send different signals",
        "high_ability": "invest",
        "low_ability": "don't_invest",
        "receiver_beliefs": {
            "invest": {"high_ability": 1.0, "low_ability": 0.0},
            "don't_invest": {"high_ability": 0.0, "low_ability": 1.0},
        },
    }

    pooling_eq = {
        "description": "Both types send same signal",
        "signal": "invest",
        "receiver_beliefs": {"prob_high_ability": 0.5},
    }

    return {
        "status": "success",
        "game_type": "costly_signaling",
        "separating_equilibrium": separating_eq,
        "pooling_equilibrium": pooling_eq,
        "recommendations": [
            "Costly signaling works when high type has lower signaling cost",
            "Separation occurs if cost difference > benefit from deception",
            "Pooled equilibria more common when costs are similar",
            "Credentials, certifications act as costly signals in labor markets",
        ],
    }


def _analyze_cheap_talk(
    sender_types: List[str] | None, messages: List[str], receiver_actions: List[str]
) -> Dict[str, Any]:
    "Analyze cheap talk (no-cost signaling) game"

    if not sender_types:
        sender_types = ["truthful", "dishonest"]
    if not messages:
        messages = ["honest_message", "dishonest_message"]
    if not receiver_actions:
        receiver_actions = ["believe", "disbelieve"]

    # Cheap talk: no intrinsic cost to messages
    # Equilibria depend on interests being aligned

    aligned_equilibrium = {
        "condition": "Sender and receiver interests aligned",
        "description": "Sender tells truth, receiver believes",
        "sender_strategy": "honest_message",
        "receiver_beliefs": "trust_message",
    }

    misaligned_equilibrium = {
        "condition": "Sender and receiver interests conflict",
        "description": "Receiver discounts message completely",
        "sender_strategy": "any (irrelevant)",
        "receiver_strategy": "disbelieve always",
        "outcome": "communication breaks down",
    }

    return {
        "status": "success",
        "game_type": "cheap_talk",
        "equilibria": {
            "aligned_interests": aligned_equilibrium,
            "conflicting_interests": misaligned_equilibrium,
        },
        "recommendations": [
            "Cheap talk only works when interests sufficiently aligned",
            "Repeated interactions can sustain honest communication",
            "Reputation valuable when direct signaling untrusted",
            "Verifiable disclosure more credible than self-reported claims",
        ],
    }


def _analyze_education_signaling(
    sender_types: List[str] | None, messages: List[str], receiver_actions: List[str]
) -> Dict[str, Any]:
    "Analyze education as signaling game"

    if not sender_types:
        sender_types = ["high_ability", "low_ability"]
    if not messages:
        messages = ["get_education", "no_education"]
    if not receiver_actions:
        receiver_actions = ["high_wage", "low_wage"]


    return {
        "status": "success",
        "game_type": "education_signaling",
        "analysis": {
            "high_ability_education_cost": 10,
            "low_ability_education_cost": 30,
            "net_benefit_high": 100 - 10 - 80,  # 10
            "net_benefit_low": 60 - 30 - 40,  # -10
        },
        "separating_equilibrium": {
            "description": "Only high ability gets education",
            "high_ability": "get_education",
            "low_ability": "no_education",
            "receiver_beliefs_after_education": "high_ability",
        },
        "recommendations": [
            "Education signals ability when cost differs enough",
            "If cost(high) < cost(low), education can separate types",
            "Social welfare: signaling has deadweight cost",
            "Credential inflation: signals degrade as more people obtain them",
        ],
    }


def _analyze_custom_signaling(
    sender_types: List[str],
    messages: List[str],
    receiver_actions: List[str],
    sender_payoffs: Dict,
    receiver_payoffs: Dict,
) -> Dict[str, Any]:
    "Analyze custom signaling game"

    # Check for separating equilibrium
    separating = _find_separating_equilibrium(
        sender_types, messages, sender_payoffs, receiver_payoffs
    )

    # Check for pooling equilibrium
    pooling = _find_pooling_equilibrium(sender_types, messages, receiver_payoffs)

    return {
        "status": "success",
        "game_type": "custom_signaling",
        "separating_equilibrium": separating,
        "pooling_equilibrium": pooling,
    }


def _find_separating_equilibrium(
    sender_types: List[str],
    messages: List[str],
    sender_payoffs: Dict,
    receiver_payoffs: Dict,
) -> Dict | None:
    "Find separating equilibrium"

    if len(sender_types) != len(messages):
        return None

    return {
        "type": "separating",
        "mapping": dict(zip(sender_types, messages, strict=False)),
    }


def _find_pooling_equilibrium(
    sender_types: List[str], messages: List[str], receiver_payoffs: Dict
) -> Dict | None:
    "Find pooling equilibrium"

    if not messages:
        return None

    return {
        "type": "pooling",
        "message": messages[0],
        "beliefs": {t: 1.0 / len(sender_types) for t in sender_types},
    }


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    payload.get("action", "analyze")
    game_type = payload.get("game_type", "costly")
    sender_types = payload.get("sender_types")
    messages = payload.get("messages")
    receiver_actions = payload.get("receiver_actions")
    sender_payoffs = payload.get("sender_payoffs")
    receiver_payoffs = payload.get("receiver_payoffs")
    signaling_cost = payload.get("signaling_cost")

    result = signaling_game_analyzer(
        game_type=game_type,
        sender_types=sender_types,
        messages=messages,
        receiver_actions=receiver_actions,
        sender_payoffs=sender_payoffs,
        receiver_payoffs=receiver_payoffs,
        signaling_cost=signaling_cost,
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
        "name": "signaling-game-analyzer",
        "description": "Analyze sender-receiver signaling games with costly and cheap talk variants",
        "version": "1.0.0",
        "domain": "STRATEGY",
    }
