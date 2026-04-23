#!/usr/bin/env python3
"""
prolog-agent-reasoning

Python-Prolog bridge for agent behavioral reasoning. Provides integration
between Python agents and Prolog logic engines with fallback to Python.
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Try to import pyswip
try:
    from pyswip import Prolog as PyswipProlog

    PYSWIP_AVAILABLE = True
except ImportError:
    PYSWIP_AVAILABLE = False
    PyswipProlog = None


DEFAULT_TRAITS_PL = """
% Behavioral DNA for agents
trait(reciprocity).
trait(forgiveness).
trait(aggression).
trait(tit_for_tat).
trait(grudger).
trait(pacifist).

% Decision rules
decide(profile(Traits,_,_), History, Action) :-
    member(trait(aggression), Traits), Resources > 5.0, !, Action = escalate.
decide(profile(Traits,_,_), _, deescalate) :- member(trait(pacifist), Traits), !.
decide(profile(Traits,_), History, Action) :- member(trait(reciprocity), Traits), last(History, Action), !.
decide(profile(Traits,_), History, Action) :- member(trait(tit_for_tat), Traits), (length(History,0) -> Action = deescalate; last(History, Action)), !.
decide(profile(_,_), History, Action) :- (length(History,0) -> Action = deescalate; last(History, Action)).
"""


class PrologAgentBridge:
    """Bridge between Python agents and Prolog logic."""

    def __init__(self, prolog_file: Optional[Path] = None, strict: bool = False):
        self.prolog_file = prolog_file
        self.strict = strict
        self._prolog = None
        self._loaded = False
        self._init_prolog()

    def _init_prolog(self):
        if not PYSWIP_AVAILABLE:
            if self.strict:
                raise ImportError("pyswip required. Install: pip install pyswip")
            logger.warning("pyswip not available, using Python fallback")
            return

        try:
            self._prolog = PyswipProlog()

            if self.prolog_file and self.prolog_file.exists():
                self._prolog.consult(str(self.prolog_file))
            else:
                # Write to temp file and consult
                import tempfile

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".pl", delete=False
                ) as f:
                    f.write(DEFAULT_TRAITS_PL)
                    temp_file = f.name
                self._prolog.consult(temp_file)

            self._loaded = True
            logger.info("Prolog agent bridge initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Prolog: {e}")
            self._loaded = False

    def is_available(self) -> bool:
        """Check if Prolog is available."""
        return self._loaded and self._prolog is not None

    def decide(
        self, traits: List[str], history: List[str], resources: float = 5.0
    ) -> Dict[str, Any]:
        """Make decision using Prolog or fallback."""
        if self.is_available():
            return self._prolog_decide(traits, history, resources)
        return self._python_fallback_decide(traits, history, resources)

    def _prolog_decide(
        self, traits: List[str], history: List[str], resources: float
    ) -> Dict[str, Any]:
        try:
            traits_prolog = f"[{','.join(f'trait({t})' for t in traits)}]"
            history_prolog = (
                f"[{','.join(f'{h}' for h in history)}]" if history else "[]"
            )
            query = f"decide(profile({traits_prolog},{resources},0), {history_prolog}, Action)"

            for solution in self._prolog.query(query):
                return {
                    "action": str(solution["Action"]),
                    "reasoning": f"Prolog decision with traits: {traits}",
                    "prolog_used": True,
                    "source": "prolog",
                }
        except Exception as e:
            logger.warning(f"Prolog decision failed: {e}")

        return self._python_fallback_decide(traits, history, resources)

    def _python_fallback_decide(
        self, traits: List[str], history: List[str], resources: float
    ) -> Dict[str, Any]:
        """Pure Python fallback when Prolog unavailable."""

        if "aggression" in traits and resources > 5:
            return {
                "action": "escalate",
                "reasoning": "aggression with high resources",
                "prolog_used": False,
                "source": "python_fallback",
            }

        if "pacifist" in traits:
            return {
                "action": "deescalate",
                "reasoning": "pacifist always cooperates",
                "prolog_used": False,
                "source": "python_fallback",
            }

        if "grudger" in traits and "escalate" in history:
            return {
                "action": "escalate",
                "reasoning": "grudger never forgives",
                "prolog_used": False,
                "source": "python_fallback",
            }

        if "tit_for_tat" in traits and history:
            return {
                "action": history[-1],
                "reasoning": "tit for tat",
                "prolog_used": False,
                "source": "python_fallback",
            }

        if "reciprocity" in traits and history:
            return {
                "action": history[-1],
                "reasoning": "reciprocal",
                "prolog_used": False,
                "source": "python_fallback",
            }

        if history:
            cooperations = history.count("deescalate")
            defections = history.count("escalate")
            action = "deescalate" if cooperations >= defections else "escalate"
        else:
            action = "deescalate"

        return {
            "action": action,
            "reasoning": "default fallback",
            "prolog_used": False,
            "source": "python_fallback",
        }

    def query(self, goal: str) -> List[Dict]:
        """Query Prolog knowledge base."""
        if not self.is_available():
            return []

        try:
            results = []
            for solution in self._prolog.query(goal):
                results.append(dict(solution))
            return results
        except Exception as e:
            logger.warning(f"Query failed: {e}")
            return []

    def assert_fact(self, fact: str):
        """Assert new fact into knowledge base."""
        if self.is_available():
            try:
                self._prolog.assertz(fact)
            except Exception as e:
                logger.warning(f"Failed to assert fact: {e}")

    def explain(self, traits: List[str], history: List[str]) -> str:
        """Explain decision in human-readable form."""
        result = self.decide(traits, history)
        return f"Decision: {result['action']}. Reasoning: {result['reasoning']}"


def prolog_agent_reasoning(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core implementation for prolog-agent-reasoning.

    Args:
        payload: Input with action, traits, history, resources

    Returns:
        Decision result with action, reasoning, trace
    """
    action = payload.get("action", "decide")

    if action == "decide":
        traits = payload.get("traits", [])
        history = payload.get("history", [])
        resources = payload.get("resources", 5.0)

        bridge = PrologAgentBridge(
            prolog_file=payload.get("prolog_file"),
            strict=payload.get("strict", False),
        )

        return bridge.decide(traits, history, resources)

    elif action == "query":
        goal = payload.get("goal", "")
        bridge = PrologAgentBridge()
        return {"results": bridge.query(goal)}

    elif action == "explain":
        traits = payload.get("traits", [])
        history = payload.get("history", [])
        bridge = PrologAgentBridge()
        return {"explanation": bridge.explain(traits, history)}

    else:
        return {"error": f"Unknown action: {action}"}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "decide")
    try:
        result = prolog_agent_reasoning(payload)
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }
    except Exception as e:
        logger.error(f"Error in prolog-agent-reasoning: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""

if __name__ == "__main__":
    return {
            "name": "prolog-agent-reasoning",
            "description": "Python-Prolog bridge for agent behavioral reasoning with fallback to pure Python.",
            "version": "1.0.0",
            "domain": "strategic_simulation",
        }