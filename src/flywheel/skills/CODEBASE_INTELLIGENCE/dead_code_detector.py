"""
Dead Code Detector Skill

This module provides skills for detecting dead code in Python:
- Detect unused functions
- Detect unused imports
- Detect unused variables
- Detect unreachable code
- Detect duplicate code
"""

import ast
import hashlib
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any, Dict, List, Set, Tuple


@dataclass
class UnusedFunction:
    """Function that is never called"""

    name: str
    line_start: int
    line_end: int
    is_method: bool = False
    class_name: str | None = None


@dataclass
class UnusedImport:
    """Import that is never used"""

    name: str
    line: int
    module: str | None = None
    is_alias: bool = False


@dataclass
class UnusedVariable:
    """Variable that is assigned but never read"""

    name: str
    line: int
    scope: str = "local"


@dataclass
class UnreachableCode:
    """Code that can never be executed"""

    line_start: int
    line_end: int
    trigger: str


@dataclass
class DuplicateCode:
    """Potential duplicate code block"""

    block_1_line_start: int
    block_1_line_end: int
    block_2_line_start: int
    block_2_line_end: int
    similarity: float


def normalize_code_for_comparison(code: str) -> str:
    """Normalize code by removing whitespace and comments for comparison"""
    normalized = re.sub(r"#.*$", "", code, flags=re.MULTILINE)
    normalized = re.sub(r'""".*?"""', "", normalized, flags=re.DOTALL)
    normalized = re.sub(r"'''.*?'''", "", normalized, flags=re.DOTALL)
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.strip()
    return normalized


def get_code_hash(code: str) -> str:
    """Get a hash of the normalized code"""
    normalized = normalize_code_for_comparison(code)
    return hashlib.md5(normalized.encode()).hexdigest()


def get_lines(code: str) -> List[str]:
    """Split code into lines"""
    return code.splitlines()


class DeadCodeVisitor(ast.NodeVisitor):
    """AST visitor to detect various types of dead code"""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.functions: List[ast.FunctionDef] = []
        self.methods: List[ast.FunctionDef] = []
        self.function_names: Set[str] = set()
        self.method_names: Set[str] = set()
        self.called_names: Set[str] = set()
        self.imports: Dict[str, int] = {}
        self.import_from: Dict[str, Tuple[str, int]] = {}
        self.used_names: Set[str] = set()
        self.variables: Dict[str, int] = {}
        self.read_variables: Set[str] = set()
        self.unreachable_ranges: List[Tuple[int, int]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions.append(node)
        self.function_names.add(node.name)

        for arg in node.args.args:
            self.used_names.add(arg.arg)

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.methods.append(item)
                self.method_names.add(item.name)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self.called_names.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.used_names.add(node.func.attr)

        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.asname:
                self.imports[alias.asname] = node.lineno
            else:
                self.imports[alias.name.split(".")[0]] = node.lineno

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            if alias.asname:
                self.import_from[alias.asname] = (node.module or "", node.lineno)
            else:
                self.import_from[alias.name] = (node.module or "", node.lineno)

        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        elif isinstance(node.ctx, ast.Store):
            self.variables[node.id] = node.lineno

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.attr)

        self.generic_visit(node)


def detect_unused_functions(
    tree: ast.Module, code_lines: List[str]
) -> List[Dict[str, Any]]:
    """Detect functions that are defined but never called"""
    visitor = DeadCodeVisitor(code_lines)
    visitor.visit(tree)

    unused = []

    for func in visitor.functions:
        if func.name.startswith("_") and func.name != "__init__":
            continue

        if func.name not in visitor.called_names:
            unused.append(
                {
                    "name": func.name,
                    "line_start": func.lineno,
                    "line_end": func.end_lineno or func.lineno,
                    "is_method": False,
                }
            )

    for method in visitor.methods:
        if method.name.startswith("_") and method.name != "__init__":
            continue

        if method.name not in visitor.called_names:
            class_name = None
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if item is method:
                            class_name = node.name
                            break

            unused.append(
                {
                    "name": method.name,
                    "line_start": method.lineno,
                    "line_end": method.end_lineno or method.lineno,
                    "is_method": True,
                    "class_name": class_name,
                }
            )

    return unused


def detect_unused_imports(
    tree: ast.Module, code_lines: List[str]
) -> List[Dict[str, Any]]:
    """Detect imports that are never used"""
    visitor = DeadCodeVisitor(code_lines)
    visitor.visit(tree)

    unused = []

    for name, line in visitor.imports.items():
        if name not in visitor.used_names:
            unused.append(
                {
                    "name": name,
                    "line": line,
                    "module": None,
                    "is_alias": name in visitor.imports,
                }
            )

    for name, (module, line) in visitor.import_from.items():
        if name not in visitor.used_names:
            unused.append(
                {
                    "name": name,
                    "line": line,
                    "module": module,
                    "is_alias": name in visitor.import_from,
                }
            )

    return unused


def detect_unused_variables(
    tree: ast.Module, code_lines: List[str]
) -> List[Dict[str, Any]]:
    """Detect variables that are assigned but never used"""
    visitor = DeadCodeVisitor(code_lines)
    visitor.visit(tree)

    unused = []

    for var_name, line in visitor.variables.items():
        if var_name not in visitor.read_variables and not var_name.startswith("_"):
            unused.append({"name": var_name, "line": line, "scope": "local"})

    return unused


def detect_unreachable_code(code_lines: List[str]) -> List[Dict[str, Any]]:
    """Detect code that follows unconditional return/raise"""
    unreachable = []

    for i, line in enumerate(code_lines):
        stripped = line.strip()

        if stripped.startswith("return") and "# unreachable after return" not in line:
            code_after = code_lines[i + 1 :] if i + 1 < len(code_lines) else []
            meaningful_lines = [
                l for l in code_after if l.strip() and not l.strip().startswith("#")
            ]

            if meaningful_lines:
                i + 2
                (
                    i + 1 + len(code_after) - len(code_after) + len(meaningful_lines)
                )

                for j, l in enumerate(code_after):
                    if l.strip() and not l.strip().startswith("#"):
                        i + 2 + j
                        break

                last_meaningful = i
                for j in range(i + 1, len(code_lines)):
                    if code_lines[j].strip() and not code_lines[j].strip().startswith(
                        """#"""
                    ):
                        last_meaningful = j

                if last_meaningful > i:
                    unreachable.append(
                        {
                            "line_start": i + 1,
                            "line_end": last_meaningful + 1,
                            "trigger": "return",
                        }
                    )
                break

        if stripped.startswith("raise") and "# unreachable after raise" not in line:
            code_after = code_lines[i + 1 :] if i + 1 < len(code_lines) else []
            meaningful_lines = [
                l for l in code_after if l.strip() and not l.strip().startswith("#")
            ]

            if meaningful_lines:
                last_meaningful = i
                for j in range(i + 1, len(code_lines)):
                    if code_lines[j].strip() and not code_lines[j].strip().startswith(
                        """#"""
                    ):
                        last_meaningful = j

                if last_meaningful > i:
                    unreachable.append(
                        {
                            "line_start": i + 1,
                            "line_end": last_meaningful + 1,
                            "trigger": "raise",
                        }
                    )
                break

        if (
            "raise" in stripped
            and "Exception" in stripped
            and "from" not in stripped.split("raise")[-1]
        ):
            pass

    [l.lower() for l in code_lines]

    for i, line in enumerate(code_lines):
        stripped = line.strip()

        if stripped.startswith("return ") or stripped == "return":
            if i + 1 < len(code_lines):
                j = i + 1
                while j < len(code_lines):
                    if code_lines[j].strip() and not code_lines[j].strip().startswith(
                        """#"""
                    ):
                        unreachable.append(
                            {
                                "line_start": j + 1,
                                "line_end": j + 1,
                                "trigger": "return",
                            }
                        )
                        break
                    j += 1

        if stripped.startswith("raise ") or stripped == "raise":
            if i + 1 < len(code_lines):
                j = i + 1
                while j < len(code_lines):
                    if code_lines[j].strip() and not code_lines[j].strip().startswith(
                        """#"""
                    ):
                        unreachable.append(
                            {"line_start": j + 1, "line_end": j + 1, "trigger": "raise"}
                        )
                        break
                    j += 1

    return unreachable


def extract_code_blocks(
    tree: ast.Module, code_lines: List[str]
) -> List[Tuple[int, int, str]]:
    """Extract code blocks for duplicate detection"""
    blocks = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.end_lineno:
                start = node.lineno - 1
                end = node.end_lineno
                code = "\n".join(code_lines[start:end])
                blocks.append((node.lineno, node.end_lineno, code))

        elif isinstance(node, ast.If):
            if hasattr(node, "body") and node.body and hasattr(node.body[0], "lineno"):
                if node.end_lineno and node.lineno:
                    start = node.lineno - 1
                    end = node.end_lineno
                    code = "\n".join(code_lines[start:end])
                    if len(code) > 100:
                        blocks.append((node.lineno, node.end_lineno, code))

    return blocks


def detect_duplicate_code(
    code_lines: List[str], threshold: float = 0.8
) -> List[Dict[str, Any]]:
    """Detect similar code blocks that might be duplicated"""
    try:
        tree = ast.parse("\n".join(code_lines))
    except:
        return []

    blocks = extract_code_blocks(tree, code_lines)

    duplicates = []

    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            start1, end1, code1 = blocks[i]
            start2, end2, code2 = blocks[j]

            if end1 - start1 < 3 or end2 - start2 < 3:
                continue

            norm1 = normalize_code_for_comparison(code1)
            norm2 = normalize_code_for_comparison(code2)

            if len(norm1) < 20 or len(norm2) < 20:
                continue

            similarity = SequenceMatcher(None, norm1, norm2).ratio()

            if similarity >= threshold:
                duplicates.append(
                    {
                        "block_1_line_start": start1 + 1,
                        "block_1_line_end": end1,
                        "block_2_line_start": start2 + 1,
                        "block_2_line_end": end2,
                        "similarity": round(similarity, 2),
                    }
                )

    return duplicates


def dead_code_detector(code: str, options: dict = None) -> dict:
    """
    Analyze Python code for dead code patterns

    Args:
        code: Python source code to analyze
        options: Analysis options
            - check_unreachable: Detect unreachable code (default: True)
            - check_duplicates: Detect duplicate code (default: True)
            - check_unused_functions: Detect unused functions (default: True)
            - check_unused_imports: Detect unused imports (default: True)
            - check_unused_variables: Detect unused variables (default: True)
            - duplicate_threshold: Similarity threshold for duplicates (default: 0.8)

    Returns:
        dict with analysis results:
            - status: "success" or "error"
            - unused_functions: List of unused functions
            - unused_imports: List of unused imports
            - unused_variables: List of unused variables
            - unreachable_code: List of unreachable code blocks
            - duplicate_code: List of potential duplicates
    """
    if options is None:
        options = {}

    check_unreachable = options.get("check_unreachable", True)
    check_duplicates = options.get("check_duplicates", True)
    check_unused_functions = options.get("check_unused_functions", True)
    check_unused_imports = options.get("check_unused_imports", True)
    check_unused_variables = options.get("check_unused_variables", True)
    duplicate_threshold = options.get("duplicate_threshold", 0.8)

    result = {
        "status": "success",
        "unused_functions": [],
        "unused_imports": [],
        "unused_variables": [],
        "unreachable_code": [],
        "duplicate_code": [],
    }

    if not code or not code.strip():
        result["status"] = "error"
        result["error"] = "No code provided"
        return result

    code_lines = get_lines(code)

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        result["status"] = "error"
        result["error"] = f"Syntax error: {str(e)}"
        return result

    if check_unused_functions:
        result["unused_functions"] = detect_unused_functions(tree, code_lines)

    if check_unused_imports:
        result["unused_imports"] = detect_unused_imports(tree, code_lines)

    if check_unused_variables:
        result["unused_variables"] = detect_unused_variables(tree, code_lines)

    if check_unreachable:
        result["unreachable_code"] = detect_unreachable_code(code_lines)

    if check_duplicates:
        result["duplicate_code"] = detect_duplicate_code(
            code_lines, duplicate_threshold
        )

    return result


async def invoke(payload: dict) -> dict:
    """
    Invoke the dead code detector skill

    Args:
        payload: Dictionary with:
            - code: Python source code (required)
            - options: Analysis options (optional)

    Returns:
        dict with analysis result
    """
    code = payload.get("code")
    options = payload.get("options", {})

    if not code:
        return{
        "result": {"status": "error", "message": "No code provided"},
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
    result = dead_code_detector(code, options)
    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "dead-code-detector",
        "description": "Analyze Python code to detect dead code - find unused functions, unused imports, unused variables, unreachable code, and duplicate code blocks",
        "version": "1.0.0",
        "domain": "CODEBASE_INTELLIGENCE",
    }


if __name__ == "__main__":
    test_code = """
import os
import sys
import json

def unused_function():
    print("This function is never called")
    return "dead code"

def used_function():
    result = calculate_value()
    return result

def calculate_value():
    x = 10
    y = 20
    return x + y

def unreachable_after_return():
    x = 1
    return x
    y = 2
    z = 3

class MyClass:
    def unused_method(self):
        pass
    
    def used_method(self):
        return True

def another_unused():
    pass

result = used_function()
print(result)
"""


if __name__ == "__main__":
    options = {
        "check_unreachable": True,
        "check_duplicates": True,
        "check_unused_functions": True,
        "check_unused_imports": True,
        "check_unused_variables": True,
        "duplicate_threshold": 0.8,
    }

    result = dead_code_detector(test_code, options)
    import json
    from datetime import datetime

    print(json.dumps(result, indent=2))
