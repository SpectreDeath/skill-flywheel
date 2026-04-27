#!/usr/bin/env python3
"""
Test script to verify behavioral orchestrator works with high reasoning skills
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_behavioral_orchestrator_with_sat_solver():
    """Test the behavioral orchestrator with SAT solver skill"""
    try:
        from flywheel.core.skills import EnhancedSkillManager
        from flywheel.behavioral.orchestrator import BehavioralOrchestrator
        import asyncio
        
        # Initialize managers
        skill_manager = EnhancedSkillManager(skills_dir='src/flywheel/skills')
        orchestrator = BehavioralOrchestrator(skill_manager)
        
        print("Testing behavioral orchestrator with SAT solver...")
        
        # First, let's see what skills are discovered
        skills = asyncio.run(skill_manager.discover_skills())
        print(f"Discovered {len(skills)} skills total")
        
        # Look for our specific skills
        high_reasoning_skills = [s for s in skills if 'high_reasoning' in s]
        print(f"High reasoning skills discovered: {high_reasoning_skills}")
        
        sat_solver_skills = [s for s in skills if 'sat_solver' in s]
        print(f"SAT solver skills discovered: {sat_solver_skills}")
        
        if not sat_solver_skills:
            print("ERROR: SAT solver skill not found in discovered skills!")
            return False
        
        # Test payload
        payload = {
            "clauses": [["P", "Q"], ["-P", "R"], ["-Q", "-R"]],
            "variables": ["P", "Q", "R"]
        }
        
        # Execute with behavioral guidelines - use the exact skill name as discovered
        skill_name = sat_solver_skills[0]  # Use the first match
        print(f"Using skill name: {skill_name}")
        
        result = orchestrator.invoke(
            skill_name=skill_name,
            payload=payload,
            profile="karpathy_balanced"
        )
        
        print(f"Execution result:")
        print(f"  Success: {result.get('result', {}).get('solution_found', False)}")
        print(f"  Status: {result.get('result', {}).get('status', 'unknown')}")
        
        quality_report = result.get('quality_report', {})
        print(f"  Quality Score: {quality_report.get('overall_score', 0):.2f}")
        print(f"  Grade: {quality_report.get('grade', 'F')}")
        print(f"  Checks Passed: {quality_report.get('checks_passed', 0)}/{quality_report.get('checks_total', 0)}")
        
        # Verify we got a proper result
        assert 'result' in result
        assert 'quality_report' in result
        assert result['result'].get('solution_found') is not False  # Should find a solution
        
        print("PASS: Behavioral orchestrator test passed")
        return True
        
    except Exception as e:
        print(f"FAIL: Behavioral orchestrator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Skill Flywheel Behavioral Orchestrator Integration")
    print("=" * 60)
    
    if test_behavioral_orchestrator_with_sat_solver():
        print("\nPASS: All tests passed!")
        sys.exit(0)
    else:
        print("\nFAIL: Tests failed")
        sys.exit(1)