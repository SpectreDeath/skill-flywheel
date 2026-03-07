#!/usr/bin/env python3
"""
Simple Test Script for Enhanced MCP Server

This script tests the basic functionality of the enhanced MCP server.
"""

import pytest
import asyncio
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.core.enhanced_mcp_server import (
    discover_skills, execute_skill, validate_skill, 
    benchmark_skill, orchestrate_agents,
    get_performance_metrics, find_skill,
    PerformanceMonitor, MetricType
)

class McpFrameworkType:
    PYTEST = "pytest"
    UNITTEST = "unittest"
    CUSTOM = "custom"

class McpExecutionResult:
    def __init__(self, passed: bool, total_tests: int, passed_tests: int, 
                 failed_tests: int, coverage: float, test_cases_run: list):
        self.passed = passed
        self.total_tests = total_tests
        self.passed_tests = passed_tests
        self.failed_tests = failed_tests
        self.coverage = coverage
        self.test_cases_run = test_cases_run

def test_performance_monitor():
    """Test performance monitoring functionality."""
    monitor = PerformanceMonitor()
    
    # Test metric recording - record success rate separately
    monitor.record_metric("test_skill", MetricType.EXECUTION_TIME, 1.5)
    monitor.record_metric("test_skill", MetricType.SUCCESS_RATE, 1.0)  # Success
    monitor.record_metric("test_skill", MetricType.QUALITY_SCORE, 0.8)
    
    # Test performance retrieval
    stats = monitor.get_skill_performance("test_skill")
    assert stats["total_executions"] == 1
    assert stats["average_execution_time"] == 1.5
    assert stats["success_rate"] == 1.0
    assert stats["average_quality_score"] == 0.8

@patch('src.core.enhanced_mcp_server.load_skill_registry')
@patch('src.core.enhanced_mcp_server.filter_skills_by_domain')
def test_discover_skills_sync(mock_filter, mock_load):
    """Test skill discovery functionality."""
    mock_skills = [
        {"name": "test-skill", "domain": "test", "purpose": "test purpose", 
         "description": "test description", "path": "test/path.md"}
    ]
    mock_load.return_value = mock_skills
    mock_filter.return_value = mock_skills
    
    # Create a mock context
    class MockContext:
        pass
    
    ctx = MockContext()
    
    # Run the async function
    result = asyncio.run(discover_skills(ctx, "test", limit=5))
    
    assert "query" in result
    assert "results" in result
    assert result["query"] == "test"

@patch('src.core.enhanced_mcp_server.load_skill_registry')
@patch('src.core.enhanced_mcp_server.filter_skills_by_domain')
@patch('builtins.open')
def test_execute_skill_sync(mock_open, mock_filter, mock_load):
    """Test skill execution functionality."""
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_file.write("# Test Skill Content")
        temp_file_path = temp_file.name
    
    try:
        mock_skills = [
            {"name": "test-skill", "domain": "test", "purpose": "test purpose", 
             "description": "test description", "path": temp_file_path}
        ]
        mock_load.return_value = mock_skills
        mock_filter.return_value = mock_skills
        
        # Create a mock context
        class MockContext:
            pass
        
        ctx = MockContext()
        
        # Run the async function
        result = asyncio.run(execute_skill(ctx, "test_skill", "test request"))
        
        assert "skill_id" in result
        assert "content" in result
        assert result["skill_id"] == "test_skill"
    finally:
        # Clean up temp file
        Path(temp_file_path).unlink()

@patch('src.core.enhanced_mcp_server.load_skill_registry')
@patch('src.core.enhanced_mcp_server.filter_skills_by_domain')
@patch('builtins.open')
def test_validate_skill_sync(mock_open, mock_filter, mock_load):
    """Test skill validation functionality."""
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
        temp_file.write("# Test Skill Content")
        temp_file_path = temp_file.name
    
    try:
        mock_skills = [
            {"name": "test-skill", "domain": "test", "purpose": "test purpose", 
             "description": "test description", "path": temp_file_path}
        ]
        mock_load.return_value = mock_skills
        mock_filter.return_value = mock_skills
        
        # Create a mock context
        class MockContext:
            pass
        
        ctx = MockContext()
        
        # Run the async function
        result = asyncio.run(validate_skill(ctx, "test_skill", "format"))
        
        assert "skill_id" in result
        assert "results" in result
        assert result["skill_id"] == "test_skill"
    finally:
        # Clean up temp file
        Path(temp_file_path).unlink()

def test_benchmark_skill_sync():
    """Test skill benchmarking functionality."""
    # This would test the benchmarking functionality
    pass

def test_orchestrate_agents_sync():
    """Test agent orchestration functionality."""
    # This would test the agent orchestration functionality
    pass

def test_get_performance_metrics_sync():
    """Test performance metrics retrieval."""
    # This would test the performance metrics functionality
    pass

if __name__ == "__main__":
    # Set environment variables for local testing
    os.environ["REGISTRY_FILE"] = str(Path(__file__).parent.parent / "skill_registry.json")

    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    # Run tests
    pytest.main([__file__, "-v"])