#!/usr/bin/env python3
r"""
Tests for skills generated from D:/GitHub/claw-code repository.
"""
import asyncio
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from flywheel.skills.modern_backend.cli_argument_parser import invoke as cli_invoke
from flywheel.skills.modern_backend.tool_execution_engine import invoke as tool_invoke
from flywheel.skills.modern_backend.session_manager import invoke as session_invoke
from flywheel.skills.modern_backend.parity_auditor import invoke as parity_invoke


class TestCLIArgumentParserSkill(unittest.IsolatedAsyncioTestCase):
    """Test CLI argument parser skill."""

    async def test_build_parser(self):
        result = await cli_invoke({
            "action": "build_parser",
            "title": "Test CLI",
            "subcommands": [
                {"name": "summary", "help": "Show summary"},
                {"name": "detail", "help": "Show detail"}
            ]
        })
        self.assertEqual(result["result"]["subcommand_count"], 2)
        self.assertIn("summary", result["result"]["subcommands"])
        self.assertIn("detail", result["result"]["subcommands"])

    async def test_validate_args_valid(self):
        result = await cli_invoke({
            "action": "validate_args",
            "required": ["name", "path"],
            "provided": {"name": "test", "path": "/tmp", "extra": True}
        })
        self.assertTrue(result["result"]["valid"])
        self.assertEqual(result["result"]["missing_args"], [])

    async def test_validate_args_missing(self):
        result = await cli_invoke({
            "action": "validate_args",
            "required": ["name", "path", "config"],
            "provided": {"name": "test"}
        })
        self.assertFalse(result["result"]["valid"])
        self.assertEqual(len(result["result"]["missing_args"]), 2)
        self.assertIn("path", result["result"]["missing_args"])
        self.assertIn("config", result["result"]["missing_args"])

    async def test_metadata_present(self):
        result = await cli_invoke({"action": "build_parser", "title": "Test"})
        self.assertIn("metadata", result)
        self.assertIn("timestamp", result["metadata"])
        self.assertEqual(result["metadata"]["action"], "build_parser")


class TestToolExecutionEngineSkill(unittest.IsolatedAsyncioTestCase):
    """Test tool execution engine skill."""

    async def test_register_tools(self):
        result = await tool_invoke({
            "action": "register_tools",
            "tools": [
                {"name": "BashTool", "responsibility": "Shell execution", "source_hint": "runtime"},
                {"name": "FileReadTool", "responsibility": "Read files", "source_hint": "fs"},
            ]
        })
        self.assertEqual(result["result"]["registered_count"], 2)
        self.assertGreaterEqual(result["result"]["total_in_registry"], 2)

    async def test_find_tools(self):
        await tool_invoke({
            "action": "register_tools",
            "tools": [
                {"name": "BashTool", "responsibility": "Shell execution", "source_hint": "runtime"},
                {"name": "FileReadTool", "responsibility": "Read files", "source_hint": "fs"},
            ]
        })
        result = await tool_invoke({
            "action": "find_tools",
            "query": "Bash"
        })
        self.assertEqual(result["result"]["match_count"], 1)
        self.assertEqual(result["result"]["matches"][0]["name"], "BashTool")

    async def test_execute_tool(self):
        await tool_invoke({
            "action": "register_tools",
            "tools": [
                {"name": "TestTool", "responsibility": "Test", "source_hint": "test"},
            ]
        })
        result = await tool_invoke({
            "action": "execute",
            "tool_name": "TestTool",
            "payload": "command=echo hello"
        })
        self.assertTrue(result["result"]["handled"])
        self.assertIn("TestTool", result["result"]["message"])

    async def test_execute_unknown_tool(self):
        result = await tool_invoke({
            "action": "execute",
            "tool_name": "NonExistentTool",
            "payload": ""
        })
        self.assertFalse(result["result"]["handled"])
        self.assertIn("Unknown tool", result["result"]["message"])


class TestSessionManagerSkill(unittest.IsolatedAsyncioTestCase):
    """Test session management skill."""

    async def test_create_session(self):
        result = await session_invoke({
            "action": "create",
            "metadata": {"purpose": "test"}
        })
        self.assertIn("session_id", result["result"])
        self.assertEqual(result["result"]["message_count"], 0)

    async def test_submit_message(self):
        create_result = await session_invoke({
            "action": "create",
            "metadata": {"test": True}
        })
        session_id = create_result["result"]["session_id"]

        result = await session_invoke({
            "action": "submit",
            "session_id": session_id,
            "content": "Hello, this is a test message"
        })
        self.assertEqual(result["result"]["message_count"], 1)

    async def test_persist_and_load(self):
        create_result = await session_invoke({
            "action": "create",
            "metadata": {"persist_test": True}
        })
        session_id = create_result["result"]["session_id"]

        persist_result = await session_invoke({
            "action": "persist",
            "session_id": session_id,
            "directory": ".test_sessions"
        })
        self.assertIn("path", persist_result["result"])

    async def test_list_sessions(self):
        result = await session_invoke({
            "action": "list",
            "directory": ".test_sessions"
        })
        self.assertIn("sessions", result["result"])
        self.assertIsInstance(result["result"]["sessions"], list)


class TestParityAuditorSkill(unittest.IsolatedAsyncioTestCase):
    """Test parity auditor skill."""

    async def test_list_subsystems(self):
        result = await parity_invoke({
            "action": "list_subsystems",
            "directory": "src/flywheel/skills"
        })
        self.assertIn("subsystems", result["result"])
        self.assertGreater(result["result"]["subsystem_count"], 0)

    async def test_count_files(self):
        result = await parity_invoke({
            "action": "count_files",
            "directory": "src/flywheel/skills"
        })
        self.assertIn("file_count", result["result"])
        self.assertGreater(result["result"]["file_count"], 0)

    async def test_audit_same_directory(self):
        """Audit comparing a directory to itself should show 100% coverage."""
        result = await parity_invoke({
            "action": "audit",
            "source_dir": "src/flywheel/skills",
            "target_dir": "src/flywheel/skills"
        })
        self.assertEqual(result["result"]["file_coverage_pct"], 100.0)
        self.assertEqual(result["result"]["subsystem_coverage_pct"], 100.0)
        self.assertEqual(result["result"]["critical_gaps"], 0)


if __name__ == "__main__":
    unittest.main()