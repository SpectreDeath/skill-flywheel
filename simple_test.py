#!/usr/bin/env python3
"""
Simple test script to verify the enhanced Collective-Mind skills work correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_sat_solver():
    """Test the enhanced SAT solver skill"""
    print("Testing Enhanced SAT Solver...")
    
    # Import the enhanced skill
    from flywheel.skills.high_reasoning import sat_solver_optimization
    
    # Test payload
    payload = {
        "clauses": [["P", "Q"], ["-P", "R"], ["-Q", "-R"]],
        "variables": ["P", "Q", "R"],
        "strategy": "dpll"
    }
    
    # Test without surfaces (should still work)
    result = sat_solver_optimization.sat_solver_optimization(payload)
    print("  Result without surfaces:", result.get('status', 'unknown'))
    print("  Surfaces used:", result.get('surfaces_used', []))
    print("  Logic summary:", result.get('logic_summary', 'none'))
    
    print("  SAT Solver test completed\n")

def test_belief_revision():
    """Test the enhanced belief revision skill"""
    print("Testing Enhanced Belief Revision...")
    
    # Import the enhanced skill
    from flywheel.skills.high_reasoning import belief_revision
    
    # Test payload
    payload = {
        "beliefs": {
            "BEL-001": 0.8,  # High confidence belief
            "BEL-002": 0.3,  # Low confidence belief
            "BEL-003": 0.6   # Medium confidence belief
        },
        "new_evidence": {
            "EVID-001": 0.9,  # Strong new evidence
            "EVID-002": 0.2   # Weak contradictory evidence
        },
        "revision_strategy": "balanced"
    }
    
    # Test without surfaces
    result = belief_revision.belief_revision(payload)
    print("  Result without surfaces:", result.get('status', 'unknown'))
    print("  Beliefs revised:", result.get('beliefs_revised', 0))
    print("  Surfaces used:", result.get('surfaces_used', []))
    print("  Logic summary:", result.get('logic_summary', 'none'))
    print("  Revision summary:", result.get('revision_summary', 'none'))
    
    print("  Belief Revision test completed\n")

def test_registration():
    """Test that skills can be registered"""
    print("Testing Skill Registration...")
    
    from flywheel.skills.high_reasoning.sat_solver_optimization import register_skill as sat_register
    from flywheel.skills.high_reasoning.belief_revision import register_skill as belief_register
    
    sat_meta = sat_register()
    belief_meta = belief_register()
    
    print("  SAT Solver:", sat_meta['name'], "v{}".format(sat_meta['version']), "({})".format(sat_meta['domain']))
    print("  Belief Revision:", belief_meta['name'], "v{}".format(belief_meta['version']), "({})".format(belief_meta['domain']))
    print("  Registration test completed\n")

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING ENHANCED COLLECTIVE-MIND SKILLS")
    print("=" * 60)
    
    try:
        test_registration()
        test_sat_solver()
        test_belief_revision()
        
        print("=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print("Test failed with error:", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)