#!/usr/bin/env python3
"""
Test script for the Behavioral Layer integration
"""

import sys
sys.path.insert(0, 'src')

from flywheel.behavioral.orchestrator import BehavioralOrchestrator
from flywheel.behavioral.profiles import (
    get_profile,
    list_profiles,
    KARPATHY_BALANCED,
    KARPATHY_STRICT,
    PRODUCTION_CRITICAL
)
from flywheel.quality.reporter import QualityReporter


def test_profiles():
    """Test behavioral profile management."""
    print("Testing Behavioral Profiles...")
    print("-" * 50)
    
    # List profiles
    profiles = list_profiles()
    print(f"Available profiles: {profiles}")
    
    # Get specific profiles
    balanced = get_profile("karpathy_balanced")
    strict = get_profile("karpathy_strict")
    critical = get_profile("production_critical")
    
    print(f"\nBalanced profile:")
    print(f"  Name: {balanced.name}")
    print(f"  Constraints: {balanced.constraints}")
    print(f"  Min score: {balanced.min_score}")
    
    print(f"\nStrict profile:")
    print(f"  Name: {strict.name}")
    print(f"  Max complexity: {strict.settings['max_complexity']}")
    print(f"  Require assumptions: {strict.settings['require_assumptions']}")
    
    print(f"\nProduction critical profile:")
    print(f"  Name: {critical.name}")
    print(f"  Max complexity: {critical.settings['max_complexity']}")
    print(f"  Max change ratio: {critical.settings['max_change_ratio']}")
    
    print("\n[PASS] Profile tests completed\n")


def test_quality_reporter():
    """Test quality reporting."""
    print("Testing Quality Reporter...")
    print("-" * 50)
    
    reporter = QualityReporter()
    
    # Test score calculation
    checks = {
        "simplicity": {"passed": True},
        "assumptions": {"passed": True},
        "surgical": {"passed": False, "issues": ["Unrelated changes"]},
        "goals": {"passed": True},
    }
    
    score = reporter.calculate_overall_score(checks)
    grade = reporter.get_grade(score)
    
    print(f"Checks: {len(checks)} total, {reporter.count_passed(checks)} passed")
    print(f"Overall score: {score:.2f}")
    print(f"Grade: {grade}")
    
    # Test report generation
    pre_results = {"checks": {"simplicity": {"passed": True}}}
    post_results = {
        "checks": {
            "simplicity": {"passed": False, "violation": "Too complex"},
            "goals": {"passed": True},
        }
    }
    
    profile_config = {
        "name": "karpathy_balanced",
        "min_score": 0.7,
    }
    
    report = reporter.generate_report(pre_results, post_results, profile_config)
    
    print(f"\nReport:")
    print(f"  Score: {report.overall_score:.2f}")
    print(f"  Grade: {report.grade}")
    print(f"  Passed: {report.passed}")
    print(f"  Checks: {report.checks_passed}/{report.checks_total}")
    
    recommendations = reporter.generate_recommendations(checks, score)
    print(f"\nRecommendations:")
    for rec in recommendations:
        print(f"  • {rec}")
    
    print("\n[PASS] Quality reporter tests completed\n")


def test_constraints():
    """Test individual constraint implementations."""
    print("Testing Constraints...")
    print("-" * 50)
    
    from flywheel.behavioral.constraints import (
        SimplicityConstraint,
        AssumptionsConstraint,
        SurgicalConstraint,
        GoalsConstraint,
    )
    
    # Test SimplicityConstraint
    print("\n1. SimplicityConstraint:")
    simp = SimplicityConstraint(max_complexity=10)
    
    simple_result = {
        "generated_code": "def add(a, b):\n    return a + b\n",
        "reasoning_steps": ["Parse input", "Add numbers", "Return result"],
    }
    
    complex_result = {
        "generated_code": "x" * 500,  # Long code
        "reasoning_steps": list(range(20)),
    }
    
    simple_check = simp.post_check(simple_result, {})
    complex_check = simp.post_check(complex_result, {})
    
    print(f"  Simple solution: passed={simple_check.passed}")
    print(f"  Complex solution: passed={complex_check.passed}")
    
    # Test AssumptionsConstraint
    print("\n2. AssumptionsConstraint:")
    assump = AssumptionsConstraint()
    
    payload = {
        "description": "Probably works for most cases",
        "assumptions": ["Input is valid"],
    }
    
    pre_check = assump.pre_check(payload, {})
    print(f"  Assumptions identified: {len(pre_check.assumptions_identified)}")
    print(f"  Requires clarification: {pre_check.requires_clarification}")
    
    # Test SurgicalConstraint
    print("\n3. SurgicalConstraint:")
    surg = SurgicalConstraint()
    
    original = "def add(a, b):\n    return a + b\n"
    modified = "def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n"
    
    validation = surg.validate(original, modified, "Add subtraction function")
    print(f"  Changes related to request: {validation.related_changes}")
    print(f"  Unrelated changes: {validation.unrelated_changes}")
    print(f"  Surgical: {validation.passed}")
    
    # Test GoalsConstraint
    print("\n4. GoalsConstraint:")
    goals = GoalsConstraint()
    
    criteria = [
        {"name": "tests_pass", "description": "Tests pass", "type": "unit_test", "target": True},
        {"name": "performance", "description": "Performance improved", "type": "performance", "target": "improved"},
    ]
    
    extracted = goals.extract_criteria({"success_criteria": criteria})
    print(f"  Extracted criteria: {len(extracted)}")
    
    result = {
        "tests_passed": 5,
        "tests_total": 5,
        "performance": "improved",
    }
    
    verification = goals.verify(result, extracted)
    print(f"  Goals met: {verification.passed}")
    print(f"  Unmet criteria: {len(verification.unmet_criteria)}")
    
    print("\n[PASS] Constraint tests completed\n")


def test_integration():
    """Test behavioral layer integration."""
    print("Testing Behavioral Layer Integration...")
    print("-" * 50)
    
    # Create orchestrator (without skill manager for this test)
    orchestrator = BehavioralOrchestrator(skill_manager=None)
    
    # Test SAT solver simulation with behavioral layer
    payload = {
        "clauses": [["P", "Q"], ["-P", "R"], ["-Q", "-R"]],
        "variables": ["P", "Q", "R"],
        "success_criteria": [
            {"name": "satisfiable", "type": "property_check", "target": True}
        ],
    }
    
    result = orchestrator.invoke(
        skill_name="sat-solver-optimization",
        payload=payload,
        profile="karpathy_balanced",
    )
    
    print(f"Skill: {result['metadata']['skill']}")
    print(f"Profile: {result['metadata']['profile']}")
    print(f"Behavioral gates passed: {result['metadata']['behavioral_gates_passed']}/{result['metadata']['behavioral_gates_total']}")
    print(f"Quality score: {result['quality_report']['overall_score']:.2f}")
    print(f"Grade: {result['quality_report']['grade']}")
    
    if result['quality_report']['recommendations']:
        print("\nRecommendations:")
        for rec in result['quality_report']['recommendations']:
            print(f"  • {rec}")
    
    print("\n[PASS] Integration test completed\n")


def test_claude_md_generation():
    """Test CLAUDE.md generation."""
    print("Testing CLAUDE.md Generation...")
    print("-" * 50)
    
    from flywheel.docs.generator import ClaudeMDGenerator
    
    generator = ClaudeMDGenerator()
    
    skills = [
        {
            "name": "sat-solver-optimization",
            "domain": "LOGIC",
            "description": "Enhanced SAT solver using Collective-Mind architecture",
            "version": "2.0.0",
        },
        {
            "name": "belief-revision",
            "domain": "EPISTEMOLOGY",
            "description": "Enhanced belief revision using Prolog and Hy surfaces",
            "version": "2.0.0",
        },
        {
            "name": "bayesian-networks",
            "domain": "PROBABILISTIC_MODELS",
            "description": "Bayesian network inference with behavioral constraints",
            "version": "2.0.0",
        },
    ]
    
    content = generator.generate(
        profile_name="karpathy_balanced",
        skills=skills,
        project_name="Test Project",
    )
    
    print(f"Generated CLAUDE.md ({len(content)} characters):")
    print("\n" + "=" * 50)
    print(content[:2000] + "...")
    print("=" * 50)
    
    print("\n[PASS] CLAUDE.md generation test completed\n")


def main():
    """Run all tests."""
    print("=" * 50)
    print("BEHAVIORAL LAYER TEST SUITE")
    print("=" * 50 + "\n")
    
    try:
        test_profiles()
        test_quality_reporter()
        test_constraints()
        test_integration()
        test_claude_md_generation()
        
        print("=" * 50)
        print("ALL TESTS PASSED")
        print("=" * 50)
        return 0
        
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
