#!/usr/bin/env python3
r"""
Tests for skills generated from D:/GitHub/claude-code repository.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from flywheel.skills.modern_backend.tool_definition_builder import invoke as tool_def_invoke
from flywheel.skills.modern_backend.cost_tracker import invoke as cost_invoke


class TestToolDefinitionBuilderSkill(unittest.IsolatedAsyncioTestCase):
    """Test tool definition builder skill."""

    async def test_build_tool_basic(self):
        result = await tool_def_invoke({
            "action": "build_tool",
            "name": "BashTool",
            "description": "Execute shell commands",
            "is_destructive": True,
            "is_concurrency_safe": False,
            "input_schema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command"}
                },
                "required": ["command"]
            }
        })
        self.assertEqual(result["result"]["name"], "BashTool")
        self.assertTrue(result["result"]["is_destructive"])
        self.assertFalse(result["result"]["is_concurrency_safe"])
        self.assertIn("command", result["result"]["input_schema"])

    async def test_build_tool_defaults(self):
        result = await tool_def_invoke({
            "action": "build_tool",
            "name": "FileReadTool",
            "description": "Read files"
        })
        self.assertFalse(result["result"]["is_destructive"])
        self.assertFalse(result["result"]["is_concurrency_safe"])
        self.assertFalse(result["result"]["is_read_only"])

    async def test_list_tools(self):
        await tool_def_invoke({
            "action": "build_tool",
            "name": "TestTool1",
            "description": "Test tool 1"
        })
        result = await tool_def_invoke({"action": "list_tools"})
        self.assertGreater(result["result"]["tool_count"], 0)

    async def test_get_tool(self):
        await tool_def_invoke({
            "action": "build_tool",
            "name": "SpecificTool",
            "description": "A specific test tool"
        })
        result = await tool_def_invoke({
            "action": "get_tool",
            "name": "SpecificTool"
        })
        self.assertEqual(result["result"]["name"], "SpecificTool")

    async def test_get_tool_not_found(self):
        result = await tool_def_invoke({
            "action": "get_tool",
            "name": "NonExistentTool"
        })
        self.assertEqual(result["result"], {"error": "Tool not found: NonExistentTool"})

    async def test_validate_input_success(self):
        await tool_def_invoke({
            "action": "build_tool",
            "name": "ValidatedTool",
            "description": "Tool with required fields",
            "input_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        })
        result = await tool_def_invoke({
            "action": "validate_input",
            "name": "ValidatedTool",
            "args": {"name": "test"}
        })
        self.assertTrue(result["result"]["result"])

    async def test_validate_input_missing_field(self):
        await tool_def_invoke({
            "action": "build_tool",
            "name": "RequiredFieldTool",
            "description": "Tool with required field",
            "input_schema": {
                "type": "object",
                "properties": {
                    "required_field": {"type": "string"}
                },
                "required": ["required_field"]
            }
        })
        result = await tool_def_invoke({
            "action": "validate_input",
            "name": "RequiredFieldTool",
            "args": {}
        })
        self.assertFalse(result["result"]["result"])
        self.assertIn("Missing required field", result["result"]["message"])


class TestCostTrackerSkill(unittest.IsolatedAsyncioTestCase):
    """Test cost tracker skill."""

    async def test_add_usage(self):
        await cost_invoke({"action": "reset"})
        result = await cost_invoke({
            "action": "add_usage",
            "model": "claude-sonnet-4-20250514",
            "input_tokens": 1500,
            "output_tokens": 2500,
            "cache_read": 500,
            "cache_write": 200,
            "cost_usd": 0.045
        })
        self.assertEqual(result["result"]["status"], "added")

    async def test_add_duration(self):
        await cost_invoke({"action": "reset"})
        result = await cost_invoke({
            "action": "add_duration",
            "type": "api",
            "seconds": 12.5
        })
        self.assertEqual(result["result"]["status"], "added")

    async def test_add_code_changes(self):
        await cost_invoke({"action": "reset"})
        result = await cost_invoke({
            "action": "add_code_changes",
            "lines_added": 42,
            "lines_removed": 15
        })
        self.assertEqual(result["result"]["status"], "added")

    async def test_summary(self):
        await cost_invoke({"action": "reset"})
        await cost_invoke({
            "action": "add_usage",
            "model": "test-model",
            "input_tokens": 100,
            "output_tokens": 200,
            "cost_usd": 0.01
        })
        result = await cost_invoke({"action": "summary"})
        self.assertEqual(result["result"]["total_input_tokens"], 100)
        self.assertEqual(result["result"]["total_output_tokens"], 200)
        self.assertEqual(result["result"]["total_cost_usd"], 0.01)

    async def test_reset(self):
        await cost_invoke({
            "action": "add_usage",
            "model": "model1",
            "input_tokens": 999,
            "cost_usd": 9.99
        })
        result = await cost_invoke({"action": "reset"})
        self.assertEqual(result["result"]["status"], "reset")

        # Verify reset
        summary = await cost_invoke({"action": "summary"})
        self.assertEqual(summary["result"]["total_input_tokens"], 0)
        self.assertEqual(summary["result"]["total_cost_usd"], 0.0)

    async def test_format_cost_low_value(self):
        result = await cost_invoke({
            "action": "format_cost",
            "cost": 0.0045
        })
        self.assertIn("$", result["result"]["formatted"])

    async def test_format_cost_high_value(self):
        result = await cost_invoke({
            "action": "format_cost",
            "cost": 1.25
        })
        self.assertEqual(result["result"]["formatted"], "$1.25")

    async def test_full_workflow(self):
        """Test a complete workflow: reset, add usage, add duration, summary."""
        await cost_invoke({"action": "reset"})

        # Add usage
        await cost_invoke({
            "action": "add_usage",
            "model": "claude-sonnet-4",
            "input_tokens": 5000,
            "output_tokens": 3000,
            "cost_usd": 0.06
        })

        # Add durations
        await cost_invoke({"action": "add_duration", "type": "api", "seconds": 8.2})
        await cost_invoke({"action": "add_duration", "type": "tool", "seconds": 1.5})

        # Add code changes
        await cost_invoke({"action": "add_code_changes", "lines_added": 100, "lines_removed": 25})

        # Get summary
        result = await cost_invoke({"action": "summary"})
        summary = result["result"]

        self.assertEqual(summary["total_input_tokens"], 5000)
        self.assertEqual(summary["total_output_tokens"], 3000)
        self.assertEqual(summary["total_cost_usd"], 0.06)
        self.assertEqual(summary["lines_added"], 100)
        self.assertEqual(summary["lines_removed"], 25)
        self.assertIn("claude-sonnet-4", summary["model_usage"])


if __name__ == "__main__":
    unittest.main()