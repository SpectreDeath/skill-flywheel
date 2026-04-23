#!/usr/bin/env python3
"""
behavioral-trait-logic

Prolog-based behavioral traits for agent decision-making. Implements reciprocity,
tit_for_tat, forgiveness, grudger, pacifist, and aggression strategies.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AgentProfile:
    """Agent behavioral profile."""

    traits: List[str]
    resources: float = 5.0
    tom_level: int = 0

    def to_prolog(self) -> str:
        traits_str = ",".join(f"trait({t})" for t in self.traits)
        return f"profile([{traits_str}],{self.resources},{self.tom_level})"


# Try to import pyswip
try:
    from pyswip import Prolog

    PYSWIP_AVAILABLE = True
except ImportError:
    PYSWIP_AVAILABLE = False
    Prolog = None


TRAITS_PL = """
% Behavioral traits
trait(reciprocity).
trait(forgiveness).
trait(aggression).
trait(tit_for_tat).
trait(grudger).
trait(pacifist).

action(escalate).
action(deescalate).

% Rule: RECIPROCITY
rule(profile(Traits,_), History, Action) :-
    member(trait(reciprocity), Traits),
    last(History, LastAction), !,
    Action = LastAction.

% Rule: TIT_FOR_TAT
rule(profile(Traits,_), History, Action) :-
    member(trait(tit_for_tat), Traits), !,
    ( length(History, 0) -> Action = deescalate
    ; last(History, LastAction), Action = LastAction
    ).

% Rule: FORGIVENESS
rule(profile(Traits,_), History, Action) :-
    member(trait(forgiveness), Traits), !,
    ( length(History, L), L < 3 -> Action = deescalate
    ; count_cooperations(History, Coop),
      count_defections(History, Def),
      ( Def = 1, Coop >= 2 -> Action = deescalate
      ; last(History, Action)
      )
    ).

% Rule: GRUDGER
rule(profile(Traits,_), History, Action) :-
    member(trait(grudger), Traits), !,
    ( has_defected(History) -> Action = escalate
    ; Action = deescalate
    ).

% Rule: AGGRESSION
rule(profile(Traits, Resources, _), _, escalate) :-
    member(trait(aggression), Traits),
    Resources > 5.0, !.

% Rule: PACIFIST
rule(profile(Traits,_,_), _, deescalate) :-
    member(trait(pacifist), Traits), !.

% Default: majority vote
rule(profile(_,_,_), History, Action) :-
    ( length(History, 0) -> Action = deescalate
    ; count_cooperations(History, Coop),
      count_defections(History, Def),
      ( Coop >= Def -> Action = deescalate
      ; Action = escalate
      )
    ).

% Helper predicates
count_cooperations([], 0).
count_cooperations([H|T], Count) :-
    ( H = deescalate -> count_cooperations(T, C), Count is C + 1
    ; count_cooperations(T, Count)
    ).

count_defections([], 0).
count_defections([H|T], Count) :-
    ( H = escalate -> count_defections(T, C), Count is C + 1
    ; count_defections(T, Count)
    ).

has_defected([escalate|_]) :- !.
has_defected([_|T]) :- has_defected(T).

decide(Profile, History, Action) :- rule(Profile, History, Action).
"""


class TraitLogic:
    """Behavioral trait logic engine."""

    def __init__(self):
        self._prolog = None
        self._loaded = False
        self._init_prolog()

    def _init_prolog(self):
        if not PYSWIP_AVAILABLE:
            logger.warning("pyswip not available")
            return

        try:
            self._prolog = Prolog()
            # Use consult with the full rules as a string
            from io import StringIO
            import tempfile

            # Write to temp file and consult
            with tempfile.NamedTemporaryFile(mode="w", suffix=".pl", delete=False) as f:
                f.write(TRAITS_PL)
                temp_file = f.name

            self._prolog.consult(temp_file)
            self._loaded = True
            logger.info("Prolog trait logic loaded")
        except Exception as e:
            logger.warning(f"Failed to load Prolog: {e}")

    def decide(self, profile: AgentProfile, history: List[str]) -> Dict[str, Any]:
        """Make decision based on traits and history."""
        if self._loaded and self._prolog:
            return self._prolog_decide(profile, history)
        else:
            return self._python_fallback_decide(profile, history)

    def _prolog_decide(
        self, profile: AgentProfile, history: List[str]
    ) -> Dict[str, Any]:
        try:
            profile_str = profile.to_prolog()
            history_str = f"[{','.join(history)}]" if history else "[]"
            query = f"decide({profile_str}, {history_str}, Action)"

            for solution in self._prolog.query(query):
                return {
                    "action": str(solution["Action"]),
                    "rule_used": "prolog_matched",
                    "reasoning": f"Used traits: {profile.traits}",
                    "prolog_used": True,
                }
        except Exception as e:
            logger.warning(f"Prolog query failed: {e}")

        return self._python_fallback_decide(profile, history)

    def _python_fallback_decide(
        self, profile: AgentProfile, history: List[str]
    ) -> Dict[str, Any]:
        """Pure Python fallback implementation."""
        traits = profile.traits

        if "aggression" in traits and profile.resources > 5:
            return {
                "action": "escalate",
                "rule_used": "aggression",
                "reasoning": "Resources > 5",
                "prolog_used": False,
            }

        if "pacifist" in traits:
            return {
                "action": "deescalate",
                "rule_used": "pacifist",
                "reasoning": "Always peaceful",
                "prolog_used": False,
            }

        if "grudger" in traits and history and "escalate" in history:
            return {
                "action": "escalate",
                "rule_used": "grudger",
                "reasoning": "Opponent defected",
                "prolog_used": False,
            }

        if "tit_for_tat" in traits and history:
            return {
                "action": history[-1],
                "rule_used": "tit_for_tat",
                "reasoning": "Mirror last move",
                "prolog_used": False,
            }

        if "reciprocity" in traits and history:
            return {
                "action": history[-1],
                "rule_used": "reciprocity",
                "reasoning": "Reciprocate",
                "prolog_used": False,
            }

        if "forgiveness" in traits and history:
            cooperations = history.count("deescalate")
            defections = history.count("escalate")
            if defections == 1 and cooperations >= 2:
                return {
                    "action": "deescalate",
                    "rule_used": "forgiveness",
                    "reasoning": "Forgiven",
                    "prolog_used": False,
                }

        # Default: majority vote
        if history:
            cooperations = history.count("deescalate")
            defections = history.count("escalate")
            action = "deescalate" if cooperations >= defections else "escalate"
        else:
            action = "deescalate"

        return {
            "action": action,
            "rule_used": "default",
            "reasoning": "Majority vote",
            "prolog_used": False,
        }


def behavioral_trait_logic(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core implementation for behavioral-trait-logic.

    Args:
        payload: Input with traits, history, resources

    Returns:
        Decision with action, reasoning, trace
    """
    traits = payload.get("traits", [])
    history = payload.get("history", [])
    resources = payload.get("resources", 5.0)
    tom_level = payload.get("tom_level", 0)

    profile = AgentProfile(traits=traits, resources=resources, tom_level=tom_level)
    engine = TraitLogic()

    return engine.decide(profile, history)


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "decide")
    try:
        result = behavioral_trait_logic(payload)
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }
    except Exception as e:
        logger.error(f"Error in behavioral-trait-logic: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""

if __name__ == "__main__":
    return {
            "name": "behavioral-trait-logic",
            "description": "Prolog-based behavioral traits for agent decision-making. Implements reciprocity, tit_for_tat, forgiveness, grudger, pacifist, and aggression.",
            "version": "1.0.0",
            "domain": "strategic_simulation",
        }