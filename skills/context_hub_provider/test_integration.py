#!/usr/bin/env python3
"""
Integration tests for Context Hub Provider Skill.

This test suite validates the skill's integration with the actual chub CLI.
"""

import unittest
import json
import sys
import os

# Add the skill directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skill import ContextHubProvider, execute_function


class TestContextHubIntegration(unittest.TestCase):
    """Integration tests for ContextHubProvider with actual chub CLI."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.provider = ContextHubProvider()
    
    def test_chub_cli_integration(self):
        """Test that the skill can integrate with the actual chub CLI."""
        # This test verifies that the skill can find and use the chub CLI
        self.assertTrue(self.provider.is_available(), 
                       "chub CLI should be available for integration tests")
    
    def test_get_context_hub_info_integration(self):
        """Test getting context hub info through the actual CLI."""
        if not self.provider.is_available():
            self.skipTest("chub CLI not available")
        
        result = self.provider.get_context_hub_info()
        
        self.assertEqual(result["status"], "success")
        self.assertIn("info", result)
        self.assertIn("domain", result)
        self.assertEqual(result["domain"], "strategy_analysis")
    
    def test_mcp_function_integration(self):
        """Test MCP function execution with actual CLI."""
        if not self.provider.is_available():
            self.skipTest("chub CLI not available")
        
        # Test get_context_hub_info through MCP interface
        result = execute_function("get_context_hub_info", {})
        
        self.assertEqual(result["status"], "success")
        self.assertIn("info", result)
        self.assertIn("domain", result)
    
    def test_error_handling_with_real_cli(self):
        """Test error handling with the actual CLI."""
        if not self.provider.is_available():
            self.skipTest("chub CLI not available")
        
        # Test with invalid domain
        result = self.provider.list_skills("nonexistent_domain")
        
        # Should handle gracefully - either success with empty list or error
        self.assertIn("status", result)
        self.assertIn(result["status"], ["success", "error"])
    
    def test_skill_registration(self):
        """Test that the skill registers correctly with MCP."""
        from skill import register_skill
        
        registration = register_skill()
        
        self.assertEqual(registration["name"], "context_hub_provider")
        self.assertEqual(registration["version"], "1.0.0")
        self.assertEqual(registration["domain"], "strategy_analysis")
        self.assertIn("functions", registration)
        
        # Check that all expected functions are registered
        function_names = [f["name"] for f in registration["functions"]]
        expected_functions = [
            "get_context_hub_info",
            "list_skills", 
            "create_skill",
            "analyze_context",
            "synthesize_skills"
        ]
        
        for func in expected_functions:
            self.assertIn(func, function_names)


if __name__ == '__main__':
    # Run the integration tests
    unittest.main(verbosity=2)