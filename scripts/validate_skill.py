#!/usr/bin/env python3
"""
Skill Module Validator

Validates that a skill module follows the correct format:
- Has async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]
- Returns dict with "result" and "metadata" keys
- Has "from datetime import datetime" or "import datetime"
- Has proper error handling (try/except in invoke)

Usage:
    python scripts/validate_skill.py <path/to/skill.py>
    python scripts/validate_skill.py --recursive src/flywheel/skills
"""

import ast
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SkillValidator:
    """Validate skill module format."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.content = ""
        self.tree: Optional[ast.AST] = None

    def load(self) -> bool:
        """Load and parse the file."""
        if not self.filepath.exists():
            self.errors.append(f"File not found: {self.filepath}")
            return False

        try:
            self.content = self.filepath.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(f"Cannot read file: {e}")
            return False

        try:
            self.tree = ast.parse(self.content)
        except SyntaxError as e:
            self.errors.append(f"Syntax error: {e}")
            return False

        return True

    def validate(self) -> Dict[str, Any]:
        """Run all validations."""
        if not self.load():
            return self._result()

        self._check_invoke_exists()
        self._check_invoke_is_async()
        self._check_invoke_signature()
        self._check_datetime_import()
        self._check_return_format()
        self._check_error_handling()
        self._check_register_skill()

        return self._result()

    def _check_invoke_exists(self):
        """Check that invoke function exists."""
        has_invoke = False
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                if node.name == "invoke":
                    has_invoke = True
                    break
        if not has_invoke:
            self.errors.append("Missing invoke function")

    def _check_invoke_is_async(self):
        """Check that invoke is async."""
        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.FunctionDef) and node.name == "invoke":
                self.errors.append("invoke must be async (use 'async def invoke')")
                return

    def _check_invoke_signature(self):
        """Check invoke has correct signature."""
        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "invoke":
                args = [a.arg for a in node.args.args]
                if "payload" not in args:
                    self.warnings.append("invoke should have 'payload' parameter")
                if node.returns is None:
                    self.warnings.append("invoke should have return type annotation")
                return

    def _check_datetime_import(self):
        """Check datetime import exists."""
        has_import = False
        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == "datetime":
                    for alias in node.names:
                        if alias.name == "datetime":
                            has_import = True
                            break
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "datetime":
                        has_import = True
                        break
        if not has_import:
            self.errors.append("Missing 'from datetime import datetime'")

    def _check_return_format(self):
        """Check that invoke returns proper format."""
        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "invoke":
                has_result = False
                has_metadata = False
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Return) and sub_node.value:
                        if isinstance(sub_node.value, ast.Dict):
                            keys = [
                                k.value if isinstance(k, ast.Constant) else None
                                for k in sub_node.value.keys
                            ]
                            if "result" in keys:
                                has_result = True
                            if "metadata" in keys:
                                has_metadata = True

                if has_result and has_metadata:
                    return  # Good
                if has_result and not has_metadata:
                    self.errors.append("invoke returns 'result' but missing 'metadata' key")
                elif not has_result:
                    self.warnings.append("invoke should return dict with 'result' key")
                return

    def _check_error_handling(self):
        """Check that invoke has error handling."""
        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, ast.AsyncFunctionDef) and node.name == "invoke":
                has_try = False
                for sub_node in ast.walk(node):
                    if isinstance(sub_node, ast.Try):
                        has_try = True
                        break
                if not has_try:
                    self.warnings.append("invoke should have try/except error handling")
                return

    def _check_register_skill(self):
        """Check that register_skill function exists."""
        has_register = False
        for node in ast.iter_child_nodes(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == "register_skill":
                    has_register = True
                    break
        if not has_register:
            self.warnings.append("Missing register_skill() function")

    def _result(self) -> Dict[str, Any]:
        return {
            "file": str(self.filepath),
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_single(filepath: Path) -> Dict[str, Any]:
    """Validate a single skill file."""
    validator = SkillValidator(filepath)
    return validator.validate()


def validate_recursive(dirpath: Path) -> List[Dict[str, Any]]:
    """Validate all Python files in directory."""
    results = []
    for f in dirpath.rglob("*.py"):
        if f.name.startswith("__"):
            continue
        result = validate_single(f)
        results.append(result)
    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate skill modules")
    parser.add_argument("path", type=Path, help="File or directory to validate")
    parser.add_argument("--recursive", action="store_true", help="Scan directory recursively")
    parser.add_argument("--quiet", action="store_true", help="Only show failures")

    args = parser.parse_args()

    if args.path.is_file():
        results = [validate_single(args.path)]
    else:
        if args.recursive:
            results = validate_recursive(args.path)
        else:
            results = [validate_single(f) for f in args.path.glob("*.py") if not f.name.startswith("__")]

    passed = 0
    failed = 0

    for r in results:
        if r["valid"]:
            passed += 1
            if not args.quiet:
                print(f"PASS: {r['file']}")
        else:
            failed += 1
            print(f"FAIL: {r['file']}")
            for e in r["errors"]:
                print(f"  ERROR: {e}")
            for w in r["warnings"]:
                print(f"  WARN: {w}")

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()