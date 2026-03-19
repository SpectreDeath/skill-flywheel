#!/usr/bin/env python3
"""
Unit tests for Context Hub Provider Skill.

This test suite validates the functionality of the context_hub_provider skill
including CLI integration, error handling, and MCP compatibility.
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Add the skill directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skill import ContextHubProvider, execute_function, register_skill


class TestContextHubProvider(unittest.TestCase):
    """Test cases for ContextHubProvider class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.provider = ContextHubProvider()
    
    @patch('subprocess.run')
    def test_find_chub_cli_success(self, mock_run):
        """Test successful chub CLI discovery."""
        # Mock successful version check
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "chub version 1.0.0"
        mock_run.return_value = mock_result
        
        # Test the _find_chub_cli method
        result = self.provider._find_chub_cli()
        
        self.assertIsNotNone(result)
        self.assertEqual(result, "chub")
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_find_chub_cli_failure(self, mock_run):
        """Test chub CLI discovery failure."""
        # Mock failed version check
        mock_run.side_effect = FileNotFoundError("chub not found")
        
        result = self.provider._find_chub_cli()
        
        self.assertIsNone(result)
    
    def test_is_available_true(self):
        """Test is_available when chub CLI is found."""
        self.provider.chub_path = "chub"
        self.assertTrue(self.provider.is_available())
    
    def test_is_available_false(self):
        """Test is_available when chub CLI is not found."""
        self.provider.chub_path = None
        self.assertFalse(self.provider.is_available())
    
    @patch('subprocess.run')
    def test_get_context_hub_info_success(self, mock_run):
        """Test successful context hub info retrieval."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Version: 1.0.0\nStatus: Active\nDomain: strategy_analysis"
        mock_run.return_value = mock_result
        
        self.provider.chub_path = "chub"
        result = self.provider.get_context_hub_info()
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["domain"], "strategy_analysis")
        self.assertIn("info", result)
    
    @patch('subprocess.run')
    def test_get_context_hub_info_failure(self, mock_run):
        """Test failed context hub info retrieval."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Command failed"
        mock_run.return_value = mock_result
        
        self.provider.chub_path = "chub"
        result = self.provider.get_context_hub_info()
        
        self.assertEqual(result["status"], "error")
        self.assertIn("Failed to get context hub info", result["message"])
    
    @patch('subprocess.run')
    def test_list_skills_success(self, mock_run):
        """Test successful skills listing."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "skill1\tDescription 1\tanalysis\nskill2\tDescription 2\tstrategy"
        mock_run.return_value = mock_result
        
        self.provider.chub_path = "chub"
        result = self.provider.list_skills("strategy_analysis")
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["domain"], "strategy_analysis")
        self.assertEqual(result["count"], 2)
        self.assertEqual(len(result["skills"]), 2)
    
    @patch('subprocess.run')
    def test_create_skill_success(self, mock_run):
        """Test successful skill creation."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Skill created successfully"
        mock_run.return_value = mock_result
        
        self.provider.chub_path = "chub"
        result = self.provider.create_skill(
            "test_skill", 
            "Test skill description", 
            "analysis"
        )
        
        self.assertEqual(result["status"], "success")
        self.assertIn("Skill 'test_skill' created successfully", result["message"])
    
    @patch('subprocess.run')
    def test_analyze_context_success(self, mock_run):
        """Test successful context analysis."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"analysis": {"insights": ["insight1", "insight2"]}}'
        mock_run.return_value = mock_result
        
        self.provider.chub_path = "chub"
        context_data = {"test": "data"}
        result = self.provider.analyze_context(context_data)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("analysis", result)
    
    @patch('subprocess.run')
    def test_synthesize_skills_success(self, mock_run):
        """Test successful skill synthesis."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = '{"synthesized": ["skill1", "skill2"]}'
        mock_run.return_value = mock_result
        
        self.provider.chub_path = "chub"
        requirements = ["requirement1", "requirement2"]
        result = self.provider.synthesize_skills(requirements)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("synthesis", result)


class TestMCPIntegration(unittest.TestCase):
    """Test cases for MCP integration functions."""
    
    def test_register_skill(self):
        """Test skill registration for MCP."""
        result = register_skill()
        
        self.assertEqual(result["name"], "context_hub_provider")
        self.assertEqual(result["version"], "1.0.0")
        self.assertEqual(result["domain"], "strategy_analysis")
        self.assertIn("functions", result)
        
        # Check that all expected functions are registered
        function_names = [f["name"] for f in result["functions"]]
        expected_functions = [
            "get_context_hub_info",
            "list_skills", 
            "create_skill",
            "analyze_context",
            "synthesize_skills"
        ]
        
        for func in expected_functions:
            self.assertIn(func, function_names)
    
    @patch('skill.ContextHubProvider')
    def test_execute_function_get_context_hub_info(self, mock_provider_class):
        """Test execute_function for get_context_hub_info."""
        mock_provider = Mock()
        mock_provider.get_context_hub_info.return_value = {"status": "success"}
        mock_provider_class.return_value = mock_provider
        
        result = execute_function("get_context_hub_info", {})
        
        self.assertEqual(result["status"], "success")
        mock_provider.get_context_hub_info.assert_called_once()
    
    @patch('skill.ContextHubProvider')
    def test_execute_function_list_skills(self, mock_provider_class):
        """Test execute_function for list_skills."""
        mock_provider = Mock()
        mock_provider.list_skills.return_value = {"status": "success", "count": 5}
        mock_provider_class.return_value = mock_provider
        
        result = execute_function("list_skills", {"domain": "strategy_analysis"})
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["count"], 5)
        mock_provider.list_skills.assert_called_once_with("strategy_analysis")
    
    @patch('skill.ContextHubProvider')
    def test_execute_function_create_skill(self, mock_provider_class):
        """Test execute_function for create_skill."""
        mock_provider = Mock()
        mock_provider.create_skill.return_value = {"status": "success"}
        mock_provider_class.return_value = mock_provider
        
        result = execute_function("create_skill", {
            "skill_name": "test_skill",
            "skill_description": "Test description",
            "skill_type": "analysis"
        })
        
        self.assertEqual(result["status"], "success")
        mock_provider.create_skill.assert_called_once_with(
            "test_skill", "Test description", "analysis"
        )
    
    @patch('skill.ContextHubProvider')
    def test_execute_function_analyze_context(self, mock_provider_class):
        """Test execute_function for analyze_context."""
        mock_provider = Mock()
        mock_provider.analyze_context.return_value = {"status": "success"}
        mock_provider_class.return_value = mock_provider
        
        context_data = {"test": "data"}
        result = execute_function("analyze_context", {"context_data": context_data})
        
        self.assertEqual(result["status"], "success")
        mock_provider.analyze_context.assert_called_once_with(context_data)
    
    @patch('skill.ContextHubProvider')
    def test_execute_function_synthesize_skills(self, mock_provider_class):
        """Test execute_function for synthesize_skills."""
        mock_provider = Mock()
        mock_provider.synthesize_skills.return_value = {"status": "success"}
        mock_provider_class.return_value = mock_provider
        
        requirements = ["req1", "req2"]
        result = execute_function("synthesize_skills", {"requirements": requirements})
        
        self.assertEqual(result["status"], "success")
        mock_provider.synthesize_skills.assert_called_once_with(requirements)
    
    def test_execute_function_unknown(self):
        """Test execute_function with unknown function name."""
        result = execute_function("unknown_function", {})
        
        self.assertEqual(result["error"], "Unknown function: unknown_function")


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling."""
    
    @patch('subprocess.run')
    def test_timeout_handling(self, mock_run):
        """Test timeout handling in subprocess calls."""
        mock_run.side_effect = subprocess.TimeoutExpired("chub", 10)
        
        self.provider = ContextHubProvider()
        self.provider.chub_path = "chub"
        
        result = self.provider.get_context_hub_info()
        
        self.assertEqual(result["error"], "Timeout while getting context hub info")
    
    def test_parse_skills_output(self):
        """Test parsing of skills output."""
        self.provider = ContextHubProvider()
        
        output = "skill1\tDescription 1\tanalysis\nskill2\tDescription 2\tstrategy"
        result = self.provider._parse_skills_output(output)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "skill1")
        self.assertEqual(result[0]["description"], "Description 1")
        self.assertEqual(result[0]["type"], "analysis")
    
    def test_parse_analysis_output_json(self):
        """Test parsing of analysis output as JSON."""
        self.provider = ContextHubProvider()
        
        output = '{"analysis": {"insights": ["insight1"]}}'
        result = self.provider._parse_analysis_output(output)
        
        self.assertIn("analysis", result)
        self.assertIn("insights", result["analysis"])
    
    def test_parse_analysis_output_fallback(self):
        """Test fallback parsing of analysis output."""
        self.provider = ContextHubProvider()
        
        output = "Raw analysis output"
        result = self.provider._parse_analysis_output(output)
        
        self.assertEqual(result["raw_output"], "Raw analysis output")


class TestConfiguration(unittest.TestCase):
    """Test cases for configuration handling."""
    
    def test_config_file_exists(self):
        """Test that config file exists and is valid JSON."""
        config_path = Path(__file__).parent / "config.json"
        
        self.assertTrue(config_path.exists())
        
        with open(config_path) as f:
            config = json.load(f)
        
        self.assertIn("name", config)
        self.assertEqual(config["name"], "context_hub_provider")
        self.assertIn("domain", config)
        self.assertEqual(config["domain"], "strategy_analysis")
        self.assertIn("mcp_integration", config)
        self.assertTrue(config["mcp_integration"]["enabled"])


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
