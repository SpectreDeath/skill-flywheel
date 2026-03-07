#!/usr/bin/env python3
"""
Test and Validation Script for Enhanced MCP Server

This script tests all the new capabilities of the enhanced MCP server,
including skill discovery, agent orchestration, validation, testing,
and performance monitoring.
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
import os

# Set environment variables for local testing
os.environ["REGISTRY_FILE"] = str(Path(__file__).parent.parent / "skill_registry.json")
os.environ["TELEMETRY_LOG"] = str(Path(__file__).parent.parent / "telemetry_test_log.jsonl")

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.enhanced_mcp_server import (
    discover_skills, execute_skill, validate_skill, test_skill as mcp_test_skill, 
    benchmark_skill, orchestrate_agents, get_performance_metrics
)
from src.core.agent_orchestration import (
    AgentOrchestrator, AgentConfig, AgentFramework,
    create_workflow_builder
)
from src.core.validation_testing import (
    validate_skill_comprehensive as verify_skill_comprehensive, 
    test_skill_comprehensive as run_skill_test_comprehensive,
    ValidationType, ValidationTestFramework
)
from src.core.performance_monitoring import (
    record_performance_metric, get_skill_performance_stats,
    generate_performance_report, MetricType
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedMCPServerTester:
    """Comprehensive tester for the enhanced MCP server."""
    
    def __init__(self):
        self.test_results = []
        self.test_skill_path = Path("domains/agent_evolution/SKILL.self-improvement-loop/SKILL.md")
        
    async def run_all_tests(self):
        """Run all test suites."""
        logger.info("Starting Enhanced MCP Server Test Suite")
        
        # Test 1: Skill Discovery
        await self.test_skill_discovery()
        
        # Test 2: Skill Execution
        await self.test_skill_execution()
        
        # Test 3: Skill Validation
        await self.test_skill_validation()
        
        # Test 4: Skill Testing
        await self.test_skill_testing()
        
        # Test 5: Skill Benchmarking
        await self.test_skill_benchmarking()
        
        # Test 6: Agent Orchestration
        await self.test_agent_orchestration()
        
        # Test 7: Performance Monitoring
        await self.test_performance_monitoring()
        
        # Test 8: Integration Tests
        await self.test_integration_scenarios()
        
        # Generate test report
        success = self.generate_test_report()
        
        logger.info("Enhanced MCP Server Test Suite Completed")
        return success
    
    async def test_skill_discovery(self):
        """Test skill discovery functionality."""
        logger.info("Testing Skill Discovery...")
        
        try:
            # Test basic discovery
            result = await discover_skills(None, query="agent", limit=5)
            self._record_test_result("Skill Discovery - Basic", result.get("results", []) is not None)
            
            # Test domain filtering
            result = await discover_skills(None, query="security", domain="APPLICATION_SECURITY", limit=3)
            self._record_test_result("Skill Discovery - Domain Filter", result.get("results", []) is not None)
            
            # Test detailed discovery
            result = await discover_skills(None, query="validation", include_details=True, limit=2)
            self._record_test_result("Skill Discovery - Detailed", result.get("results", []) is not None)
            
        except Exception as e:
            logger.error(f"Skill Discovery test failed: {e}")
            self._record_test_result("Skill Discovery - Error", False, str(e))
    
    async def test_skill_execution(self):
        """Test skill execution functionality."""
        logger.info("Testing Skill Execution...")
        
        try:
            # Test basic execution
            result = await execute_skill(None, skill_id="self-improvement-loop", request="Test execution")
            self._record_test_result("Skill Execution - Basic", result.get("execution_context") is not None)
            
            # Test execution with context
            context = {"test_mode": True, "user_id": "test_user"}
            result = await execute_skill(None, skill_id="self-improvement-loop", request="Test with context", context=context)
            self._record_test_result("Skill Execution - With Context", result.get("execution_context") is not None)
            
        except Exception as e:
            logger.error(f"Skill Execution test failed: {e}")
            self._record_test_result("Skill Execution - Error", False, str(e))
    
    async def test_skill_validation(self):
        """Test skill validation functionality."""
        logger.info("Testing Skill Validation...")
        
        try:
            # Test comprehensive validation
            result = await validate_skill(None, skill_id="self-improvement-loop", validation_type="all")
            self._record_test_result("Skill Validation - Comprehensive", result.get("overall_status") is not None)
            
            # Test specific validation types
            for validation_type in ["format", "dependencies", "security"]:
                result = await validate_skill(None, skill_id="self-improvement-loop", validation_type=validation_type)
                self._record_test_result(f"Skill Validation - {validation_type.title()}", result.get("results") is not None)
            
        except Exception as e:
            logger.error(f"Skill Validation test failed: {e}")
            self._record_test_result("Skill Validation - Error", False, str(e))
    
    async def test_skill_testing(self):
        """Test skill testing functionality."""
        logger.info("Testing Skill Testing...")
        
        try:
            # Test pytest framework
            test_cases = [
                {"description": "Test basic functionality", "input": "test", "expected": "success"},
                {"description": "Test error handling", "input": "error", "expected": "handled"}
            ]
            
            result = await mcp_test_skill(None, skill_id="self-improvement-loop", test_framework="pytest", test_cases=test_cases)
            self._record_test_result("Skill Testing - Pytest", result.get("test_framework") == "pytest")
            
            # Test unittest framework
            result = await mcp_test_skill(None, skill_id="self-improvement-loop", test_framework="unittest", test_cases=test_cases)
            self._record_test_result("Skill Testing - Unittest", result.get("test_framework") == "unittest")
            
        except Exception as e:
            logger.error(f"Skill Testing test failed: {e}")
            self._record_test_result("Skill Testing - Error", False, str(e))
    
    async def test_skill_benchmarking(self):
        """Test skill benchmarking functionality."""
        logger.info("Testing Skill Benchmarking...")
        
        try:
            # Test benchmarking
            result = await benchmark_skill(None, skill_id="self-improvement-loop", iterations=3)
            self._record_test_result("Skill Benchmarking - Basic", result.get("metrics") is not None)
            
            # Test with test data
            test_data = ["test1", "test2", "test3"]
            result = await benchmark_skill(None, skill_id="self-improvement-loop", iterations=2, test_data=test_data)
            self._record_test_result("Skill Benchmarking - With Data", result.get("metrics") is not None)
            
        except Exception as e:
            logger.error(f"Skill Benchmarking test failed: {e}")
            self._record_test_result("Skill Benchmarking - Error", False, str(e))
    
    async def test_agent_orchestration(self):
        """Test agent orchestration functionality."""
        logger.info("Testing Agent Orchestration...")
        
        try:
            # Test single framework orchestration
            orchestrator = AgentOrchestrator()
            
            # Register agents
            orchestrator.register_agent(AgentConfig(
                name="researcher",
                role="Researcher",
                goal="Research complex topics",
                backstory="Expert researcher",
                framework=AgentFramework.AUTOGEN
            ))
            
            orchestrator.register_agent(AgentConfig(
                name="analyst",
                role="Analyst", 
                goal="Analyze research findings",
                backstory="Data analysis specialist",
                framework=AgentFramework.AUTOGEN
            ))
            
            # Test orchestration
            result = await orchestrator.orchestrate_task(
                task_id="test_task_001",
                agents=["researcher", "analyst"],
                task_description="Research and analyze AI agent orchestration"
            )
            
            self._record_test_result("Agent Orchestration - Single Framework", result.success)
            
            # Test multi-framework orchestration
            orchestrator.register_agent(AgentConfig(
                name="langchain_writer",
                role="Writer",
                goal="Write reports",
                backstory="Content specialist",
                framework=AgentFramework.LANGCHAIN
            ))
            
            result = await orchestrator.orchestrate_task(
                task_id="test_task_002",
                agents=["researcher", "langchain_writer"],
                task_description="Multi-framework task"
            )
            
            self._record_test_result("Agent Orchestration - Multi-Framework", result.success)
            
            # Test workflow builder
            builder = create_workflow_builder()
            builder.add_agent(
                name="workflow_researcher",
                role="Researcher",
                goal="Research topics",
                backstory="Research expert",
                framework=AgentFramework.AUTOGEN
            ).add_step(
                step_name="research_step",
                agents=["workflow_researcher"],
                task="Research the topic"
            )
            
            results = await builder.execute_workflow()
            self._record_test_result("Agent Orchestration - Workflow Builder", len(results) > 0)
            
        except Exception as e:
            logger.error(f"Agent Orchestration test failed: {e}")
            self._record_test_result("Agent Orchestration - Error", False, str(e))
    
    async def test_performance_monitoring(self):
        """Test performance monitoring functionality."""
        logger.info("Testing Performance Monitoring...")
        
        try:
            # Test metric recording
            record_performance_metric(
                "test_skill",
                MetricType.EXECUTION_TIME,
                2.5,
                {"test": "performance"},
                "autogen"
            )
            
            self._record_test_result("Performance Monitoring - Record Metric", True)
            
            # Test performance stats
            stats = get_skill_performance_stats("test_skill")
            self._record_test_result("Performance Monitoring - Get Stats", stats is not None)
            
            # Test report generation
            report = generate_performance_report(1)  # Last 1 day
            self._record_test_result("Performance Monitoring - Generate Report", report is not None)
            
        except Exception as e:
            logger.error(f"Performance Monitoring test failed: {e}")
            self._record_test_result("Performance Monitoring - Error", False, str(e))
    
    async def test_integration_scenarios(self):
        """Test integration scenarios combining multiple features."""
        logger.info("Testing Integration Scenarios...")
        
        try:
            # Scenario 1: Complete skill lifecycle
            skill_id = "self-improvement-loop"
            
            # 1. Discover skill
            discovery_result = await discover_skills(None, query="self-improvement", limit=1)
            self._record_test_result("Integration - Skill Discovery", discovery_result.get("results") is not None)
            
            # 2. Validate skill
            validation_result = await validate_skill(None, skill_id=skill_id, validation_type="all")
            self._record_test_result("Integration - Skill Validation", validation_result.get("overall_status") is not None)
            
            # 3. Execute skill
            execution_result = await execute_skill(None, skill_id=skill_id, request="Test integration scenario")
            self._record_test_result("Integration - Skill Execution", execution_result.get("execution_context") is not None)
            
            # 4. Benchmark skill
            benchmark_result = await benchmark_skill(None, skill_id=skill_id, iterations=2)
            self._record_test_result("Integration - Skill Benchmarking", benchmark_result.get("metrics") is not None)
            
            # 5. Monitor performance
            record_performance_metric(
                skill_id,
                MetricType.EXECUTION_TIME,
                3.2,
                {"integration_test": True},
                "autogen"
            )
            
            stats = get_skill_performance_stats(skill_id)
            self._record_test_result("Integration - Performance Monitoring", stats is not None)
            
            # Scenario 2: Multi-agent workflow
            orchestrator = AgentOrchestrator()
            
            # Register multiple agents
            for i in range(3):
                orchestrator.register_agent(AgentConfig(
                    name=f"agent_{i}",
                    role=f"Agent {i}",
                    goal=f"Perform task {i}",
                    backstory=f"Agent {i} specialist",
                    framework=AgentFramework.AUTOGEN
                ))
            
            # Execute multi-agent task
            result = await orchestrator.orchestrate_task(
                task_id="integration_test_001",
                agents=["agent_0", "agent_1", "agent_2"],
                task_description="Integration test with multiple agents"
            )
            
            self._record_test_result("Integration - Multi-Agent Workflow", result.success)
            
        except Exception as e:
            logger.error(f"Integration Scenarios test failed: {e}")
            self._record_test_result("Integration - Error", False, str(e))
    
    def _record_test_result(self, test_name: str, success: bool, error_message: str = None):
        """Record a test result."""
        result = {
            "test_name": test_name,
            "success": success,
            "error_message": error_message,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        
        status = "PASS" if success else "FAIL"
        logger.info(f"Test '{test_name}': {status}")
        if error_message:
            logger.error(f"  Error: {error_message}")
    
    def generate_test_report(self):
        """Generate a comprehensive test report."""
        logger.info("\n" + "="*60)
        logger.info("ENHANCED MCP SERVER TEST REPORT")
        logger.info("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "N/A")
        
        logger.info("\nDetailed Results:")
        logger.info("-" * 40)
        
        for result in self.test_results:
            status = "✓ PASS" if result["success"] else "✗ FAIL"
            logger.info(f"{status} {result['test_name']}")
            if result["error_message"]:
                logger.info(f"     Error: {result['error_message']}")
        
        # Save report to file
        report_data = {
            "timestamp": time.time(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0
            },
            "test_results": self.test_results
        }
        
        report_file = Path("test_report.json")
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"\nDetailed report saved to: {report_file}")
        
        # Return success status
        return failed_tests == 0

async def main():
    """Main test execution."""
    logger.info("Enhanced MCP Server Test Suite Starting...")
    
    tester = EnhancedMCPServerTester()
    success = await tester.run_all_tests()
    
    if success:
        logger.info("🎉 All tests passed! Enhanced MCP Server is working correctly.")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed. Please check the implementation.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())