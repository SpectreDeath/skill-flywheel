"""
Unit Test Generator

Generates unit tests from Python code snippets using:
- AST analysis to understand function signatures
- Pattern recognition for common test cases
- Template-based test generation
"""

import ast
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


def extract_functions(code: str) -> List[Dict[str, Any]]:
    """Extract function definitions from code"""
    functions = []

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                defaults = node.args.defaults

                # Handle *args and **kwargs
                if node.args.vararg:
                    args.append(f"*{node.args.vararg.arg}")
                if node.args.kwarg:
                    args.append(f"**{node.args.kwarg.arg}")

                # Return type hints
                returns = None
                if node.returns:
                    returns = ast.unparse(node.returns)

                functions.append(
                    {
                        "name": node.name,
                        "args": args,
                        "line": node.lineno,
                        "returns": returns,
                        "has_self": "self" in args,
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                    }
                )
    except SyntaxError:
        pass

    return functions


def infer_test_type(func_name: str) -> str:
    """Infer appropriate test type from function name"""
    name_lower = func_name.lower()

    if "validate" in name_lower or "check" in name_lower:
        return "assertTrue"
    elif "get" in name_lower or "fetch" in name_lower:
        return "assertIsNotNone"
    elif "create" in name_lower or "add" in name_lower:
        return "assertIsNotNone"
    elif "delete" in name_lower or "remove" in name_lower:
        return "assertTrue"
    else:
        return "assertEqual"


def generate_tests(code: str, framework: str = "pytest") -> Dict[str, Any]:
    """
    Generate unit tests from code.

    Args:
        code: Python source code
        framework: Test framework (pytest, unittest)

    Returns:
        Generated test code
    """
    functions = extract_functions(code)

    if not functions:
        return {"status": "error", "error": "No functions found in code"}

    test_code = []

    # Import statements
    if framework == "pytest":
        test_code.append("import pytest")
    else:
        test_code.append("import unittest")

    test_code.append("from your_module import *\n")

    # Generate test class
    test_code.append("class TestFunctions(unittest.TestCase):")

    for func in functions:
        if func["has_self"]:
            continue  # Skip methods for now

        func_name = func["name"]
        args = [a for a in func["args"] if not a.startswith("*")]
        test_type = infer_test_type(func_name)

        # Generate test method
        test_code.append(f"\n    def test_{func_name}(self):")

        if args:
            # Generate sample arguments based on type hints
            sample_args = []
            for arg in args:
                if func["returns"] and "int" in func["returns"]:
                    sample_args.append("1")
                elif func["returns"] and "str" in func["returns"]:
                    sample_args.append('"test"')
                elif func["returns"] and "bool" in func["returns"]:
                    sample_args.append("True")
                elif func["returns"] and "list" in func["returns"]:
                    sample_args.append("[]")
                elif func["returns"] and "dict" in func["returns"]:
                    sample_args.append("{}")
                else:
                    sample_args.append("None")

            call_args = ", ".join(sample_args)
            if func["is_async"]:
                test_code.append(f"        # Note: Requires pytest-asyncio")
                test_code.append(f"        result = await {func_name}({call_args})")
            else:
                test_code.append(f"        result = {func_name}({call_args})")
        else:
            if func["is_async"]:
                test_code.append(f"        # Note: Requires pytest-asyncio")
                test_code.append(f"        result = await {func_name}()")
            else:
                test_code.append(f"        result = {func_name}()")

        # Add assertion
        if test_type == "assertIsNotNone":
            test_code.append(f"        self.assertIsNotNone(result)")
        elif test_type == "assertTrue":
            test_code.append(f"        self.assertTrue(result)")
        elif test_type == "assertEqual":
            test_code.append(f"        # Add your expected result")
            test_code.append(f"        self.assertEqual(result, expected)")

    # Add main block for unittest
    if framework == "unittest":
        test_code.append("\n\nif __name__ == '__main__':")
        test_code.append("    unittest.main()")

    return {
        "status": "success",
        "functions_found": len(functions),
        "functions": [f["name"] for f in functions],
        "test_code": "\n".join(test_code),
        "framework": framework,
    }


def unit_test_generator(
    code: str, framework: str = "pytest", **kwargs
) -> Dict[str, Any]:
    """
    Main entry point for unit test generation.

    Args:
        code: Python source code
        framework: Test framework (pytest, unittest)
        **kwargs: Additional parameters

    Returns:
        Generated test code
    """
    if not code:
        return {"status": "error", "error": "No code provided"}

    return generate_tests(code, framework)


def invoke(payload: dict) -> dict:
    """MCP skill invocation"""
    action = payload.get("action", "generate")
    code = payload.get("code", "")
    framework = payload.get("framework", "pytest")

    if action == "generate":
        result = unit_test_generator(code, framework)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata"""
    return {
        "name": "unit-test-generator",
        "description": "Generate unit tests from Python code snippets",
        "version": "1.0.0",
        "domain": "AI_AGENT_DEVELOPMENT",
    }
