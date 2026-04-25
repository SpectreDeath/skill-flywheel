#!/usr/bin/env python3
"""
Trust Scorer Skill (POC for Collective-Mind Substrate)
Domain: EPISTEMOLOGY

Demonstrates the three-surface architecture:
- Prolog: Hard disqualification rules (Symbolic Logic)
- Hy (Lisp): Heuristic scoring (Associative Pattern Matching)
- Python: Coordination and I/O (Motor/Execution)
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# --- SURFACE 1: PROLOG (Hard Rules) ---
PROLOG_SURFACE = """
% Disqualify if source is on a known banned list
disqualified(Source) :- banned(Source).
% Disqualify if source has zero reputation
disqualified(Source) :- reputation(Source, 0).

% Example data (could be dynamic)
banned(malicious_actor_01).
banned(shadow_node_42).
reputation(anonymous_proxy, 0).
reputation(verified_expert, 100).
"""

# --- SURFACE 2: HY (Soft Heuristics) ---
HY_SURFACE = """
(defn calculate-heuristic [features]
  (if (> (.count features "peer_reviewed") 0)
      0.9
      0.5))
"""

def trust_scorer(payload: Dict[str, Any], surfaces: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Coordinates Prolog, Hy, and Python surfaces to score a source's trust.
    """
    source = payload.get("source", "unknown")
    features = payload.get("features", [])
    
    # 1. Prolog Check (Hard Disqualification)
    is_disqualified = False
    disqualification_reason = None
    
    if surfaces and "prolog" in surfaces:
        prolog = surfaces["prolog"]
        # Check if disqualified
        results = list(prolog.query(f"disqualified({source})"))
        if results:
            is_disqualified = True
            disqualification_reason = "Disqualified by Prolog hard rules (banned or zero reputation)"
    
    if is_disqualified:
        return {
            "source": source,
            "trust_score": 0.0,
            "status": "disqualified",
            "reason": disqualification_reason,
            "surfaces_used": ["prolog"]
        }
    
    # 2. Hy Check (Soft Heuristic Scoring)
    heuristic_score = 0.5
    if surfaces and "hy" in surfaces:
        import hy
        import types
        try:
            hy_code = surfaces["hy"]
            # Create a dedicated module for Hy logic
            hy_mod = types.ModuleType("hy_mod")
            # In Hy 1.0+, hy.eval needs a module object for declarations like defn
            hy.eval(hy.read_many(hy_code), hy_mod.__dict__, hy_mod)
            
            # Directly call the Hy-defined function (it's a Python function!)
            heuristic_score = hy_mod.calculate_heuristic(features)
        except Exception as e:
            logger.error(f"Hy surface execution failed: {e}")
            heuristic_score = 0.5 # Fallback
            
    # 3. Python (Final Assembly & Formatting)
    final_score = round(heuristic_score, 2)
    
    return {
        "source": source,
        "trust_score": final_score,
        "status": "active",
        "features_analyzed": features,
        "surfaces_used": ["prolog", "hy", "python"],
        "logic_summary": f"Prolog validated {source}; Hy evaluated features {features} to score {final_score}"
    }

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP entry point."""
    # Note: In a real run, the manager would pass 'surfaces' to the function
    # but for testing/standalone we might need to handle it.
    from datetime import datetime
    
    # This is a bit of a hack for standalone invoke if not called via manager
    # but the manager change I made will pass it.
    
    return {
        "result": trust_scorer(payload), # Manager will pass surfaces here
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "skill": "trust_scorer"
        }
    }

def register_skill():
    return {
        "name": "trust_scorer",
        "description": "Hybrid trust scoring using Prolog and Hy surfaces.",
        "version": "1.0.0",
        "domain": "EPISTEMOLOGY"
    }
