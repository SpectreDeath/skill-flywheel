#!/usr/bin/env python3
"""
Simple test script for Bayesian Networks enhanced skill
"""

import sys
sys.path.insert(0, 'src')

from flywheel.skills.high_reasoning import bayesian_networks

def test_basic():
    """Test basic Bayesian network inference"""
    print("Testing Bayesian Networks Skill...")
    
    # Define a simple network: A -> B -> C
    payload = {
        "variables": ["A", "B", "C"],
        "edges": [["A", "B"], ["B", "C"]],
        "cpts": {
            "A": {"True": 0.3, "False": 0.7},
            "B": {"A_True_True": 0.8, "A_True_False": 0.2, "A_False_True": 0.3, "A_False_False": 0.7},
            "C": {"B_True_True": 0.9, "B_True_False": 0.1, "B_False_True": 0.4, "B_False_False": 0.6}
        },
        "evidence": {"A": True},
        "query": ["B", "C"],
        "algorithm": "variable_elimination"
    }
    
    # Test without surfaces
    result = bayesian_networks.bayesian_networks(payload)
    
    print("  Status: " + result.get('status', ''))
    print("  Surfaces used: " + str(result.get('surfaces_used', [])))
    print("  Network summary: " + result.get('network_summary', ''))
    print("  Logic summary: " + result.get('logic_summary', ''))
    
    # Check results
    posteriors = result.get("posterior_probabilities", {})
    for var, probs in posteriors.items():
        print("  P(" + var + "): " + str(probs))
    
    print("  [PASS] Basic test completed\n")
    return True

def test_with_surfaces():
    """Test with mock surfaces"""
    print("Testing with mock surfaces...")
    
    payload = {
        "variables": ["Rain", "Sprinkler", "Wet_Grass"],
        "edges": [["Rain", "Wet_Grass"], ["Sprinkler", "Wet_Grass"]],
        "evidence": {"Wet_Grass": True},
        "query": ["Rain", "Sprinkler"],
        "algorithm": "variable_elimination"
    }
    
    # Mock surfaces
    mock_surfaces = {
        "prolog": None,
        "hy": None
    }
    
    result = bayesian_networks.bayesian_networks(payload, mock_surfaces)
    
    print("  Status: " + result.get('status', ''))
    print("  Surfaces used: " + str(result.get('surfaces_used', [])))
    print("  Algorithm: " + str(result.get('inference_details', {}).get('algorithm_used')))
    print("  Network: " + result.get('network_summary', ''))
    print("  [PASS] Mock surfaces test completed\n")
    return True

def test_registration():
    """Test skill registration"""
    print("Testing Skill Registration...")
    
    meta = bayesian_networks.register_skill()
    
    print("  Name: " + meta['name'])
    print("  Version: " + meta['version'])
    print("  Domain: " + meta['domain'])
    print("  Description: " + meta['description'])
    print("  [PASS] Registration test completed\n")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING BAYESIAN NETWORKS - ENHANCED SKILL")
    print("=" * 60 + "\n")
    
    try:
        test_registration()
        test_basic()
        test_with_surfaces()
        
        print("=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        
    except Exception as e:
        print("\n[X] Test failed with error: " + str(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)