#!/usr/bin/env python3
"""
Test script to verify behavioral layer integration with high reasoning skills
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_behavioral_imports():
    """Test that behavioral components can be imported"""
    try:
        from flywheel.behavioral.orchestrator import BehavioralOrchestrator
        from flywheel.behavioral.profiles import BehavioralProfile, get_profile
        from flywheel.behavioral.constraints.assumptions import AssumptionsConstraint
        from flywheel.behavioral.constraints.goals import GoalsConstraint
        from flywheel.behavioral.constraints.simplicity import SimplicityConstraint
        from flywheel.behavioral.constraints.surgical import SurgicalConstraint
        print("PASS: All behavioral components imported successfully")
        return True
    except Exception as e:
        print(f"FAIL: Failed to import behavioral components: {e}")
        return False

def test_high_reasoning_skills_import():
    """Test that high reasoning skills can be imported"""
    try:
        from flywheel.skills.high_reasoning.sat_solver_optimization import sat_solver_optimization
        from flywheel.skills.high_reasoning.belief_revision import belief_revision
        from flywheel.skills.high_reasoning.bayesian_networks import bayesian_networks
        print("PASS: All high reasoning skills imported successfully")
        return True
    except Exception as e:
        print(f"FAIL: Failed to import high reasoning skills: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of a high reasoning skill"""
    try:
        from flywheel.skills.high_reasoning.sat_solver_optimization import sat_solver_optimization
        
        # Simple test payload
        payload = {
            "clauses": [["P", "Q"], ["-P", "R"], ["-Q", "-R"]],
            "variables": ["P", "Q", "R"]
        }
        
        result = sat_solver_optimization(payload)
        
        # Basic checks
        assert "solution_found" in result
        assert "status" in result
        assert "surfaces_used" in result
        assert "python" in result["surfaces_used"]
        
        print("PASS: Basic SAT solver functionality works")
        print(f"  Result: {result['status']}, Solution found: {result['solution_found']}")
        return True
    except Exception as e:
        print(f"FAIL: Basic functionality test failed: {e}")
        return False

def test_enhanced_skill_manager():
    """Test the enhanced skill manager with behavioral layer"""
    try:
        from flywheel.core.skills import EnhancedSkillManager
        from flywheel.behavioral.orchestrator import BehavioralOrchestrator
        import asyncio
        
        # Initialize managers
        skill_manager = EnhancedSkillManager(skills_dir='src/flywheel/skills')
        orchestrator = BehavioralOrchestrator(skill_manager)
        
        print("PASS: EnhancedSkillManager and BehavioralOrchestrator initialized")
        
        # Test skill discovery
        skills = asyncio.run(skill_manager.discover_skills())
        high_reasoning_skills = [s for s in skills if 'high_reasoning' in s]
        print(f"PASS: Discovered {len(high_reasoning_skills)} high reasoning skills: {high_reasoning_skills}")
        
        return True
    except Exception as e:
        print(f"FAIL: Enhanced skill manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Skill Flywheel Behavioral Layer Integration")
    print("=" * 50)
    
    tests = [
        test_behavioral_imports,
        test_high_reasoning_skills_import,
        test_basic_functionality,
        test_enhanced_skill_manager
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("PASS: All integration tests passed!")
        sys.exit(0)
    else:
        print("FAIL: Some tests failed")
        sys.exit(1)