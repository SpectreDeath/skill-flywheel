#!/usr/bin/env python3
"""
Test script for Enhanced MCP Server

This script demonstrates the key features of the enhanced MCP server
including multi-agent orchestration, skill execution, and monitoring.
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any

# Server configuration
SERVER_URL = "http://localhost:8000"

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_result(title: str, result: Any):
    """Print a formatted result"""
    print(f"\n{title}:")
    print("-" * 40)
    if isinstance(result, dict):
        print(json.dumps(result, indent=2, default=str))
    else:
        print(result)
    print("-" * 40)

async def test_health_check():
    """Test the health check endpoint"""
    print_section("Testing Health Check")
    
    try:
        response = requests.get(f"{SERVER_URL}/health")
        result = response.json()
        print_result("Health Check Result", result)
        return result["status"] == "healthy"
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

async def test_metrics():
    """Test the metrics endpoint"""
    print_section("Testing Metrics")
    
    try:
        response = requests.get(f"{SERVER_URL}/metrics")
        result = response.json()
        print_result("Metrics Result", result)
        return True
    except Exception as e:
        print(f"Metrics test failed: {e}")
        return False

async def test_skill_discovery():
    """Test skill discovery functionality"""
    print_section("Testing Skill Discovery")
    
    try:
        response = requests.post(f"{SERVER_URL}/skills/discover")
        result = response.json()
        print_result("Skill Discovery Result", result)
        return len(result.get("discovered_skills", [])) > 0
    except Exception as e:
        print(f"Skill discovery failed: {e}")
        return False

async def test_skill_execution():
    """Test skill execution with sample data"""
    print_section("Testing Skill Execution")
    
    try:
        # Sample data for data_analyzer skill
        sample_data = [
            {"age": 25, "income": 50000, "score": 85},
            {"age": 30, "income": 60000, "score": 90},
            {"age": 35, "income": 70000, "score": 95},
            {"age": 40, "income": 80000, "score": 88},
            {"age": 45, "income": 90000, "score": 92},
        ]
        
        payload = {
            "skill_name": "data_analyzer",
            "args": [],
            "kwargs": {
                "data": sample_data,
                "analysis_type": "comprehensive",
                "output_format": "text"
            }
        }
        
        response = requests.post(f"{SERVER_URL}/skills/execute", json=payload)
        result = response.json()
        print_result("Skill Execution Result", result)
        return result.get("success", False)
    except Exception as e:
        print(f"Skill execution failed: {e}")
        return False

async def test_agent_creation():
    """Test agent creation"""
    print_section("Testing Agent Creation")
    
    try:
        payload = {
            "agent_id": "test_analyst",
            "role": "Test Data Analyst",
            "goal": "Analyze test data and provide insights",
            "backstory": "Expert in analyzing datasets and generating reports",
            "tools": [],
            "llm_config": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }
        
        response = requests.post(f"{SERVER_URL}/agents/create", json=payload)
        result = response.json()
        print_result("Agent Creation Result", result)
        return result.get("success", False)
    except Exception as e:
        print(f"Agent creation failed: {e}")
        return False

async def test_agent_task():
    """Test agent task execution"""
    print_section("Testing Agent Task Execution")
    
    try:
        payload = {
            "agent_id": "test_analyst",
            "task_description": "Analyze the following data and provide insights: [25, 30, 35, 40, 45]",
            "context": {
                "data_type": "numerical",
                "analysis_purpose": "trend_analysis"
            }
        }
        
        response = requests.post(f"{SERVER_URL}/agents/execute", json=payload)
        result = response.json()
        print_result("Agent Task Result", result)
        return result.get("success", False)
    except Exception as e:
        print(f"Agent task execution failed: {e}")
        return False

async def test_crew_creation():
    """Test crew creation"""
    print_section("Testing Crew Creation")
    
    try:
        payload = {
            "crew_id": "test_crew",
            "agents": ["test_analyst"],
            "process": "sequential"
        }
        
        response = requests.post(f"{SERVER_URL}/crews/create", json=payload)
        result = response.json()
        print_result("Crew Creation Result", result)
        return result.get("success", False)
    except Exception as e:
        print(f"Crew creation failed: {e}")
        return False

async def test_crew_task():
    """Test crew task execution"""
    print_section("Testing Crew Task Execution")
    
    try:
        payload = {
            "crew_id": "test_crew",
            "task_description": "Perform a comprehensive analysis of the provided dataset",
            "context": {
                "dataset_description": "Sample numerical data for analysis",
                "expected_output": "detailed_analysis_report"
            }
        }
        
        response = requests.post(f"{SERVER_URL}/crews/execute", json=payload)
        result = response.json()
        print_result("Crew Task Result", result)
        return result.get("success", False)
    except Exception as e:
        print(f"Crew task execution failed: {e}")
        return False

async def run_comprehensive_test():
    """Run all tests in sequence"""
    print_section("Enhanced MCP Server Comprehensive Test")
    print("This test demonstrates the key features of the enhanced MCP server")
    
    test_results = []
    
    # Test 1: Health Check
    health_ok = await test_health_check()
    test_results.append(("Health Check", health_ok))
    
    # Test 2: Metrics
    metrics_ok = await test_metrics()
    test_results.append(("Metrics", metrics_ok))
    
    # Test 3: Skill Discovery
    skills_ok = await test_skill_discovery()
    test_results.append(("Skill Discovery", skills_ok))
    
    # Test 4: Skill Execution
    if skills_ok:
        skill_ok = await test_skill_execution()
        test_results.append(("Skill Execution", skill_ok))
    else:
        test_results.append(("Skill Execution", False))
    
    # Test 5: Agent Creation
    agent_ok = await test_agent_creation()
    test_results.append(("Agent Creation", agent_ok))
    
    # Test 6: Agent Task
    if agent_ok:
        agent_task_ok = await test_agent_task()
        test_results.append(("Agent Task", agent_task_ok))
    else:
        test_results.append(("Agent Task", False))
    
    # Test 7: Crew Creation
    if agent_ok:
        crew_ok = await test_crew_creation()
        test_results.append(("Crew Creation", crew_ok))
    else:
        test_results.append(("Crew Creation", False))
    
    # Test 8: Crew Task
    if agent_ok and crew_ok:
        crew_task_ok = await test_crew_task()
        test_results.append(("Crew Task", crew_task_ok))
    else:
        test_results.append(("Crew Task", False))
    
    # Print summary
    print_section("Test Summary")
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Enhanced MCP Server is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the server configuration and dependencies.")
    
    return passed == total

def check_server_running():
    """Check if the server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

async def main():
    """Main test function"""
    print("Enhanced MCP Server Test Suite")
    print("=" * 60)
    
    # Check if server is running
    if not check_server_running():
        print("❌ Server is not running!")
        print(f"Please start the server with: python enhanced_mcp_server.py")
        print(f"Or run with Docker: docker-compose up -d")
        return
    
    print("✅ Server is running")
    
    # Run comprehensive tests
    success = await run_comprehensive_test()
    
    if success:
        print("\n🎉 Enhanced MCP Server is ready for production use!")
        print("\nNext steps:")
        print("1. Explore the API endpoints")
        print("2. Create custom skills in the skills/ directory")
        print("3. Set up monitoring with Prometheus and Grafana")
        print("4. Configure production deployment with Docker")
    else:
        print("\n⚠️  Please review the test results and fix any issues")

if __name__ == "__main__":
    asyncio.run(main())