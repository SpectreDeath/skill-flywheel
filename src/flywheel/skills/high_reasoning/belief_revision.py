#!/usr/bin/env python3
"""
Belief Revision Skill (Enhanced with Collective-Mind Architecture)

Domain: EPISTEMOLOGY
Description: Enhanced belief revision system using Prolog for logical consistency checking,
Hy for heuristic belief selection strategies, and Python for orchestration.

Enhanced with Collective-Mind Architecture (Prolog + Hy + Python)
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

def belief_revision(
    payload: Dict[str, Any], surfaces: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Enhanced belief revision using three-surface Collective-Mind architecture:
    - Prolog: Logical consistency checking and constraint validation
    - Hy: Heuristic belief selection and revision strategies
    - Python: Orchestration, belief update logic, and result formatting
    
    Args:
        payload: Input parameters containing:
            - beliefs: Dictionary of current beliefs with confidence scores
            - new_evidence: New evidence to incorporate
            - revision_strategy: Strategy for belief revision
        surfaces: Optional dict containing Prolog and Hy surfaces
        
    Returns:
        Result dictionary with revised beliefs, status, and execution details
    """
    beliefs = payload.get("beliefs", {})
    new_evidence = payload.get("new_evidence", {})
    revision_strategy = payload.get("revision_strategy", "conservative")
    
    logger.info(f"Revising beliefs with {len(beliefs)} current beliefs and {len(new_evidence)} new evidence items")
    
    # 1. Prolog Surface: Logical consistency validation
    consistency_check = {"consistent": True, "conflicts": []}
    
    if surfaces and "prolog" in surfaces:
        prolog = surfaces["prolog"]
        try:
            # Convert beliefs to Prolog facts for consistency checking
            belief_facts = []
            for belief, confidence in beliefs.items():
                if isinstance(confidence, (int, float)) and 0 <= confidence <= 1:
                    belief_facts.append(f"belief('{belief}', {confidence}).")
            
            evidence_facts = []
            for evidence, strength in new_evidence.items():
                if isinstance(strength, (int, float)) and 0 <= strength <= 1:
                    evidence_facts.append(f"evidence('{evidence}', {strength}).")
            
            # Check for logical conflicts
            query = f"check_consistency([{','.join(belief_facts + evidence_facts)}], Conflicts)"
            results = list(prolog.query(query))
            
            if results:
                consistency_check["consistent"] = len(results[0].get("Conflicts", [])) == 0
                consistency_check["conflicts"] = results[0].get("Conflicts", [])
                consistency_check["details"] = results[0]
            else:
                consistency_check["details"] = "No consistency results returned"
        except Exception as e:
            logger.warning(f"Prolog consistency check failed: {e}")
            consistency_check["error"] = str(e)
    
    # 2. Hy Surface: Heuristic guidance for belief revision strategy
    heuristic_guidance = {
        "strategy": revision_strategy,
        "confidence_threshold": 0.5,
        "belief_updates": {},
        "evidence_weight": 0.3
    }
    
    if surfaces and "hy" in surfaces:
        try:
            import hy
            import types
            
            hy_code = surfaces["hy"]
            # Create a dedicated module for Hy logic
            hy_mod = types.ModuleType("hy_mod")
            # In Hy 1.0+, hy.eval needs a module object for declarations like defn
            hy.eval(hy.read_many(hy_code), hy_mod.__dict__, hy_mod)
            
            # Get heuristic recommendations for belief revision
            heuristic_guidance = hy_mod.revise_beliefs(
                beliefs=beliefs,
                new_evidence=new_evidence,
                current_strategy=revision_strategy
            )
        except Exception as e:
            logger.error(f"Hy surface execution failed: {e}")
            # Fallback to basic heuristic
            heuristic_guidance = {
                "strategy": revision_strategy,
                "confidence_threshold": 0.5,
                "belief_updates": {k: min(1.0, v + 0.1) for k, v in beliefs.items() if k in new_evidence},
                "evidence_weight": 0.3,
                "fallback_used": True
            }
    
    # 3. Python Surface: Orchestration and belief revision execution
    # Apply belief revision based on Prolog consistency and Hy heuristics
    
    revised_beliefs = beliefs.copy()
    updates_applied = []
    
    # Apply evidence-based updates from Hy guidance
    belief_updates = heuristic_guidance.get("belief_updates", {})
    for belief, new_confidence in belief_updates.items():
        if belief in revised_beliefs:
            old_confidence = revised_beliefs[belief]
            # Blend old belief with new evidence based on strategy
            if heuristic_guidance.get("strategy") == "conservative":
                revised_confidence = old_confidence * 0.7 + new_confidence * 0.3
            elif heuristic_guidance.get("strategy") == "aggressive":
                revised_confidence = old_confidence * 0.3 + new_confidence * 0.7
            else:  # balanced or default
                revised_confidence = (old_confidence + new_confidence) / 2
            
            revised_beliefs[belief] = max(0.0, min(1.0, revised_confidence))
            updates_applied.append({
                "belief": belief,
                "old_confidence": old_confidence,
                "new_confidence": revised_beliefs[belief],
                "change": revised_beliefs[belief] - old_confidence
            })
    
    # Add new evidence as beliefs if not already present
    for evidence, strength in new_evidence.items():
        if evidence not in revised_beliefs:
            revised_beliefs[evidence] = strength * heuristic_guidance.get("evidence_weight", 0.3)
            updates_applied.append({
                "belief": evidence,
                "old_confidence": 0.0,
                "new_confidence": revised_beliefs[evidence],
                "change": revised_beliefs[evidence],
                "type": "new_evidence"
            })
    
    # Apply consistency constraints from Prolog if inconsistencies were found
    consistency_adjustments = []
    if not consistency_check.get("consistent", True):
        # In a real implementation, we would use Prolog to suggest minimally inconsistent subsets to remove
        # For now, we'll lower confidence of conflicting beliefs
        conflicts = consistency_check.get("conflicts", [])
        for conflict in conflicts:
            # Simple approach: reduce confidence of mentioned beliefs
            for belief in conflict:
                if belief in revised_beliefs and revised_beliefs[belief] > 0.1:
                    old_conf = revised_beliefs[belief]
                    revised_beliefs[belief] *= 0.8  # Reduce confidence by 20%
                    consistency_adjustments.append({
                        "belief": belief,
                        "old_confidence": old_conf,
                        "new_confidence": revised_beliefs[belief],
                        "reason": "resolved_consistency_conflict"
                    })
    
    result = {
        "original_beliefs_count": len(beliefs),
        "new_evidence_count": len(new_evidence),
        "revised_beliefs_count": len(revised_beliefs),
        "beliefs_revised": len(updates_applied),
        "consistency_check": consistency_check,
        "heuristic_guidance": heuristic_guidance,
        "revised_beliefs": revised_beliefs,
        "updates_applied": updates_applied,
        "consistency_adjustments": consistency_adjustments,
        "status": "success",
        "surfaces_used": [],
        "logic_summary": "",
        "revision_summary": ""
    }
    
    # Track which surfaces were successfully used
    if surfaces:
        if "prolog" in surfaces:
            result["surfaces_used"].append("prolog")
        if "hy" in surfaces:
            result["surfaces_used"].append("hy")
    result["surfaces_used"].append("python")
    
    # Create summary
    summary_parts = []
    if "prolog" in result["surfaces_used"]:
        consistent = consistency_check.get("consistent", True)
        conflict_count = len(consistency_check.get('conflicts', []))
        status_text = 'PASS' if consistent else f'FAIL ({conflict_count} conflicts)'
        summary_parts.append(f"Prolog consistency check: {status_text}")
    if "hy" in result["surfaces_used"]:
        strategy = heuristic_guidance.get("strategy", "unknown")
        summary_parts.append(f"Hy recommended strategy: {strategy} ({len(updates_applied)} belief updates)")
    if "python" in result["surfaces_used"]:
        summary_parts.append(f"Python orchestrated belief revision ({len(revised_beliefs)} total beliefs)")
        
    result["logic_summary"] = "; ".join(summary_parts)
    
    # Create human-readable summary
    belief_changes = len([u for u in updates_applied if abs(u["change"]) > 0.01])
    result["revision_summary"] = f"Revised {belief_changes} beliefs based on {len(new_evidence)} new evidence items"
    
    return result


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP entry point for the enhanced belief revision system."""
    from datetime import datetime
    
    # Note: In production, the EnhancedSkillManager would pass surfaces
    # For standalone/testing, we'll call without surfaces
    result = belief_revision(payload)
    
    return {
        "result": result,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "skill": "belief-revision",
            "version": "2.0.0-enhanced"
        }
    }


def register_skill():
    """Return skill metadata for MCP registration."""
    return {
        "name": "belief-revision",
        "description": "Enhanced belief revision using Collective-Mind architecture (Prolog+Hy+Python)",
        "version": "2.0.0",
        "domain": "EPISTEMOLOGY",
    }


# --- SURFACE DEFINITIONS ---
# These are loaded by the EnhancedSkillManager at runtime
_base_path = Path(__file__).parent

# Prolog Surface: Logical consistency and belief constraints
PROLOG_SURFACE = (_base_path / "belief_revision.pl").read_text()

# Hy Surface: Heuristic belief revision strategies
HY_SURFACE = (_base_path / "belief_revision.hy").read_text()
