#!/usr/bin/env python3
"""
Simple test runner for the MCP Server tests
"""

import subprocess
import sys
import os

def run_test_file(test_file):
    """Run a specific test file"""
    print(f"Running {test_file}...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def main():
    """Run all test files"""
    test_dir = "tests"
    test_files = [
        "test_mcp_server_fix.py",
        "test_enhanced_server.py",
        "test_dynamic_lazy_loading.py",
        "test_performance_improvements.py",
        "test_watchdog.py",
        "test_ux_mobile_idle_wake.py"
    ]
    
    results = {}
    
    for test_file_name in test_files:
        test_file = os.path.join(test_dir, test_file_name)
        if os.path.exists(test_file):
            print(f"\n{'='*60}")
            print(f"Testing: {test_file}")
            print(f"{'='*60}")
            
            success = run_test_file(test_file)
            results[test_file] = success
            
            if success:
                print(f"✅ {test_file} PASSED")
            else:
                print(f"❌ {test_file} FAILED")
        else:
            print(f"⚠️  {test_file} not found, skipping")
            results[test_file] = None
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for result in results.values() if result is True)
    failed = sum(1 for result in results.values() if result is False)
    skipped = sum(1 for result in results.values() if result is None)
    
    print(f"Total files: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    
    if failed > 0:
        print(f"\n❌ Some tests failed!")
        sys.exit(1)
    else:
        print(f"\n✅ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()