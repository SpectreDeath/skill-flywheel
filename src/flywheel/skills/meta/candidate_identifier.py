#!/usr/bin/env python3
"""
Architecture Candidate Identifier Skill
Domain: META

Identifies existing skills that would benefit from the "Collective-Mind"
(Python-Prolog-Hy) architecture.
"""

import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)




def candidate_identifier(
    payload: Dict[str, Any], surfaces: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyzes the skill registry to find candidates for the new architecture.
    """
    limit = payload.get("limit", 10)

    # 1. Fetch skills from database
    db_path = Path("data/skill_registry.db")
    if not db_path.exists():
        return {"error": "Skill database not found"}

    candidates = []
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name, domain, description FROM skills")
        all_skills = cursor.fetchall()
        conn.close()
    except Exception as e:
        return {"error": f"Database error: {e}"}

    # 2. Process each skill using surfaces
    import hy
    import types

    hy_mod = None
    if surfaces and "hy" in surfaces:
        try:
            hy_mod = types.ModuleType("hy_mod")
            # Using hy.read_many and passing the module object for Hy 1.0+
            hy.eval(hy.read_many(surfaces["hy"]), hy_mod.__dict__, hy_mod)
        except Exception as e:
            logger.error(f"Failed to init Hy for identifier: {e}")

    for name, domain, description in all_skills:
        # Prolog Surface check
        prio = "Consider for Enhancement"
        if surfaces and "prolog" in surfaces:
            prolog = surfaces["prolog"]
            # Clean up name for Prolog (ensure it's an atom)
            clean_name = name.replace("-", "_").lower()
            prolog.assertz(f"domain('{clean_name}', '{domain.lower()}')")
            results = list(prolog.query(f"recommendation('{clean_name}', R)"))
            if results:
                val = results[0]["R"]
                # Decode if it's bytes (pyswip sometimes returns bytes)
                if isinstance(val, bytes):
                    prio = val.decode("utf-8")
                else:
                    prio = str(val)

        # Hy Surface check
        score = 0.1
        if hy_mod and hasattr(hy_mod, "calculate_suitability_score"):
            try:
                score = hy_mod.calculate_suitability_score(description or "")
            except Exception as e:
                logger.error(f"Hy eval failed for {name}: {e}")

        # Final collation
        candidates.append(
            {
                "name": name,
                "domain": domain,
                "description": description[:100] + "..." if description else "",
                "priority": prio,
                "suitability_score": round(float(score), 2),
            }
        )

    # Sort by suitability score and then priority
    candidates.sort(
        key=lambda x: (x["suitability_score"], x["priority"] == "Highly Recommended"),
        reverse=True,
    )

    return {
        "top_candidates": candidates[:limit],
        "total_analyzed": len(all_skills),
        "surfaces_used": ["prolog", "hy", "python"],
        "architecture_applied": "Collective-Mind",
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP entry point."""
    from datetime import datetime

    return {
        "result": candidate_identifier(payload),
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "skill": "architecture-candidate-identifier",
        },
    }


def register_skill():
    return {
        "name": "architecture-candidate-identifier",
        "description": "Identifies best skills for Collective-Mind architecture upgrade.",
        "version": "1.0.0",
        "domain": "META",
    }


# --- SURFACE 1: PROLOG (Hard Rules) ---
PROLOG_SURFACE = """
% Tier 1 domains (Hard Rules)
is_tier1_domain(epistemology).
is_tier1_domain(logic).
is_tier1_domain(logic_programming).
is_tier1_domain(game_theory).
is_tier1_domain(formal_methods).
is_tier1_domain(reasoning).

% Rule: Recommended if it's a Tier 1 domain
recommendation(Skill, "Highly Recommended") :- 
    domain(Skill, Domain), 
    is_tier1_domain(Domain).

% Default recommendation
recommendation(Skill, "Consider for Enhancement") :- 
    not(recommendation(Skill, "Highly Recommended")).
"""

# --- SURFACE 2: HY (Soft Heuristics) ---
HY_SURFACE = """
(defn calculate-suitability-score [description]
  (let [keywords ["logic" "heuristic" "rules" "reliability" "trust" 
                  "verification" "optimization" "orchestration" 
                  "reasoning" "epistemic" "validation" "consensus"
                  "formal" "mathematical" "truth" "inference" "engine"]
        score 0.1
        desc-lower (.lower description)]
    (for [kw keywords]
      (if (> (.count desc-lower kw) 0)
          (setv score (+ score 0.15))))
    (min 1.0 score)))
"""
