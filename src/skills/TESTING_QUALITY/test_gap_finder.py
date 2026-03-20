"""
Test Gap Finder

Identifies untested code paths in Python source code by:
- Parsing source code to extract functions and branches
- Parsing test code to understand what's is tested
- Identifying gaps in test coverage
- Prioritizing gaps by risk/importance
- Generating test suggestions
"""

import ast
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class FunctionInfo:
    name: str
    args: List[str]
    line: int
    returns: str | None
    is_async: bool
    has_self: bool
    branches: List[Dict[str, Any]] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)


@dataclass
class TestInfo:
    name: str
    test_type: str
    line: int
    targets: List[str] = field(default_factory=list)
    assertions: List[str] = field(default_factory=list)


def parse_source_code(code: str) -> Dict[str, Any]:
    """Parse source code to extract functions and branches."""
    functions = []
    branches = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"status": "error", "error": f"Syntax error in source: {e}"}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [arg.arg for arg in node.args.args]
            vararg = node.args.vararg
            kwarg = node.args.kwarg

            if vararg:
                args.append(f"*{vararg.arg}")
            if kwarg:
                args.append(f"**{kwarg.arg}")

            returns = None
            if node.returns:
                returns = ast.unparse(node.returns)

            decorators = [ast.unparse(d) for d in node.decorator_list]

            func_branches = extract_branches(node)

            exceptions = extract_exception_types(node)

            functions.append(
                FunctionInfo(
                    name=node.name,
                    args=args,
                    line=node.lineno,
                    returns=returns,
                    is_async=isinstance(node, ast.AsyncFunctionDef),
                    has_self="self" in args,
                    branches=func_branches,
                    exceptions=exceptions,
                    decorators=decorators,
                )
            )

            for branch in func_branches:
                branches.append(
                    {
                        "function": node.name,
                        "line": branch.get("line"),
                        "type": branch.get("type"),
                        "condition": branch.get("condition"),
                    }
                )

    return {
        "status": "success",
        "functions": functions,
        "branches": branches,
        "total_functions": len(functions),
        "total_branches": len(branches),
    }


def extract_branches(func_node: ast.AST) -> List[Dict[str, Any]]:
    """Extract branch points (if, elif, for, while, try, except) from function."""
    branches = []

    for node in ast.walk(func_node):
        if isinstance(node, ast.If):
            branches.append(
                {
                    "type": "if",
                    "line": node.lineno,
                    "condition": ast.unparse(node.test)
                    if hasattr(ast, "unparse")
                    else "condition",
                }
            )
        elif isinstance(node, (ast.For, ast.While)):
            branches.append(
                {"type": "loop", "line": node.lineno, "condition": "iteration"}
            )
        elif isinstance(node, ast.Try):
            branches.append(
                {
                    "type": "try_except",
                    "line": node.lineno,
                    "condition": "exception_handling",
                }
            )
        elif isinstance(node, ast.With):
            branches.append(
                {
                    "type": "with_block",
                    "line": node.lineno,
                    "condition": "context_manager",
                }
            )

    return branches


def extract_exception_types(func_node: ast.AST) -> List[str]:
    """Extract exception types that can be raised."""
    exceptions = []

    for node in ast.walk(func_node):
        if isinstance(node, ast.Raise):
            if node.exc and isinstance(node.exc, ast.Name):
                exceptions.append(node.exc.id)
            elif node.exc and isinstance(node.exc, ast.Call):
                if isinstance(node.exc.func, ast.Name):
                    exceptions.append(node.exc.func.id)
        elif isinstance(node, ast.ExceptHandler) and node.type:
            if isinstance(node.type, ast.Name):
                exceptions.append(node.type.id)
            elif isinstance(node.type, ast.Tuple):
                for ex in node.type.elts:
                    if isinstance(ex, ast.Name):
                        exceptions.append(ex.id)

    return list(set(exceptions))


def parse_test_code(test_code: str) -> Dict[str, Any]:
    """Parse test code to extract what's being tested."""
    tests = []
    tested_functions = set()
    tested_classes = set()

    try:
        tree = ast.parse(test_code)
    except SyntaxError:
        return {
            "status": "success",
            "tests": [],
            "tested_functions": [],
            "tested_classes": [],
        }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            test_name = node.name
            if test_name.startswith("test_") or test_name.endswith("_test"):
                assertions = extract_assertions(node)

                targets = find_test_targets(node)

                for target in targets:
                    tested_functions.add(target)

                if "class" in [isinstance(p, ast.Name) for p in node.args.args]:
                    pass

                tests.append(
                    TestInfo(
                        name=test_name,
                        test_type=infer_test_type(test_name),
                        line=node.lineno,
                        targets=targets,
                        assertions=assertions,
                    )
                )

    return {
        "status": "success",
        "tests": tests,
        "tested_functions": list(tested_functions),
        "tested_classes": list(tested_classes),
        "total_tests": len(tests),
    }


def extract_assertions(func_node: ast.AST) -> List[str]:
    """Extract assertion types from test function."""
    assertions = []

    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr.startswith("assert"):
                    assertions.append(node.func.attr)
            elif isinstance(node.func, ast.Name):
                if node.func.id.startswith("assert"):
                    assertions.append(node.func.id)

    return assertions


def find_test_targets(func_node: ast.AST) -> List[str]:
    """Find what functions/methods are being tested."""
    targets = []

    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                targets.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                targets.append(node.func.attr)

    return list(set(targets))


def infer_test_type(test_name: str) -> str:
    """Infer the type of test from its name."""
    name_lower = test_name.lower()

    if "unit" in name_lower:
        return "unit"
    elif "integration" in name_lower:
        return "integration"
    elif "edge" in name_lower or "boundary" in name_lower:
        return "edge_case"
    elif "error" in name_lower or "exception" in name_lower:
        return "error_case"
    elif "performance" in name_lower or "perf" in name_lower:
        return "performance"
    else:
        return "general"


def identify_gaps(
    source_info: Dict[str, Any], test_info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Identify untested functions and branches."""
    gaps = []

    source_functions = source_info.get("functions", [])
    source_info.get("branches", [])
    tested_functions = set(test_info.get("tested_functions", []))

    for func in source_functions:
        func_name = func.name

        if func_name not in tested_functions:
            gap = {
                "type": "function",
                "name": func_name,
                "line": func.line,
                "reason": "function_not_tested",
                "risk_factors": calculate_risk_factors(func),
                "suggested_priority": calculate_priority(func),
            }
            gaps.append(gap)

        if func.branches:
            for branch in func.branches:
                branch_key = f"{func_name}_{branch['line']}"
                if branch_key not in tested_functions:
                    gap = {
                        "type": "branch",
                        "name": f"{func_name}:{branch['type']}",
                        "line": branch["line"],
                        "parent_function": func_name,
                        "reason": "branch_not_tested",
                        "condition": branch.get("condition"),
                        "risk_factors": calculate_branch_risk_factors(branch),
                        "suggested_priority": calculate_branch_priority(branch),
                    }
                    gaps.append(gap)

        if func.exceptions:
            for exc in func.exceptions:
                exc_key = f"{func_name}_{exc}"
                if exc_key not in tested_functions:
                    gap = {
                        "type": "exception",
                        "name": f"{func_name}:{exc}",
                        "line": func.line,
                        "parent_function": func_name,
                        "reason": "exception_not_tested",
                        "exception_type": exc,
                        "risk_factors": {"has_exception": True},
                        "suggested_priority": "high",
                    }
                    gaps.append(gap)

    return gaps


def calculate_risk_factors(func: FunctionInfo) -> Dict[str, Any]:
    """Calculate risk factors for a function."""
    factors = {
        "has_branches": len(func.branches) > 0,
        "has_exceptions": len(func.exceptions) > 0,
        "is_public": not func.name.startswith("_"),
        "has_return": func.returns is not None,
        "is_async": func.is_async,
        "complexity": len(func.branches) + 1,
    }

    return factors


def calculate_priority(func: FunctionInfo) -> str:
    """Calculate priority based on function characteristics."""
    score = 0

    if not func.name.startswith("_"):
        score += 2

    if len(func.branches) > 0:
        score += len(func.branches)

    if len(func.exceptions) > 0:
        score += 2

    if func.is_async:
        score += 1

    if score >= 4:
        return "critical"
    elif score >= 2:
        return "high"
    elif score >= 1:
        return "medium"
    else:
        return "low"


def calculate_branch_risk_factors(branch: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate risk factors for a branch."""
    return {
        "branch_type": branch.get("type"),
        "is_critical_branch": branch.get("type") in ["if", "try_except"],
    }


def calculate_branch_priority(branch: Dict[str, Any]) -> str:
    """Calculate priority for a branch."""
    branch_type = branch.get("type")

    if branch_type in {"if", "try_except"}:
        return "high"
    elif branch_type == "loop":
        return "medium"
    else:
        return "low"


def prioritize_gaps(gaps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort gaps by priority."""
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

    def get_priority_score(gap):
        priority = gap.get("suggested_priority", "low")
        return priority_order.get(priority, 3)

    return sorted(gaps, key=get_priority_score)


def generate_test_suggestions(
    gaps: List[Dict[str, Any]], source_info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Generate test suggestions for identified gaps."""
    suggestions = []

    for gap in gaps:
        gap_type = gap.get("type")

        if gap_type == "function":
            func = find_function_by_name(source_info, gap["name"])
            if func:
                suggestion = {
                    "gap": gap["name"],
                    "gap_type": "function",
                    "test_name": f"test_{gap['name']}",
                    "test_type": "unit",
                    "description": f"Add unit test for {gap['name']}",
                    "template": generate_function_test_template(func),
                    "priority": gap.get("suggested_priority"),
                }
                suggestions.append(suggestion)

        elif gap_type == "branch":
            suggestion = {
                "gap": gap["name"],
                "gap_type": "branch",
                "test_name": f"test_{gap['parent_function']}_branch_{gap['line']}",
                "test_type": "branch",
                "description": f"Add branch test for {gap['name']}",
                "template": generate_branch_test_template(gap),
                "priority": gap.get("suggested_priority"),
            }
            suggestions.append(suggestion)

        elif gap_type == "exception":
            suggestion = {
                "gap": gap["name"],
                "gap_type": "exception",
                "test_name": f"test_{gap['parent_function']}_raises_{gap['exception_type']}",
                "test_type": "error_case",
                "description": f"Add exception test for {gap['exception_type']}",
                "template": generate_exception_test_template(gap),
                "priority": gap.get("suggested_priority"),
            }
            suggestions.append(suggestion)

    return suggestions


def find_function_by_name(
    source_info: Dict[str, Any], func_name: str
) -> FunctionInfo | None:
    """Find function info by name."""
    for func in source_info.get("functions", []):
        if func.name == func_name:
            return func
    return None


def generate_function_test_template(func: FunctionInfo) -> str:
    """Generate test template for a function."""
    args_str = ", ".join([a for a in func.args if not a.startswith("*")])

    if func.is_async:
        template = f"""async def test_{func.name}():
    # Arrange
    # Add test setup here
    pass

    # Act
    # result = await {func.name}({args_str or ''})

    # Assert
    # Add assertions here
"""
    else:
        template = f"""def test_{func.name}():
    # Arrange
    # Add test setup here
    pass

    # Act
    # result = {func.name}({args_str or ''})

    # Assert
    # Add assertions here
"""
    return template


def generate_branch_test_template(gap: Dict[str, Any]) -> str:
    """Generate test template for branch coverage."""
    parent_func = gap.get("parent_function")
    branch_type = gap.get("type")

    template = f"""def test_{parent_func}_branch_{gap['line']}():
    # Test specific branch at line {gap['line']}
    # Branch type: {branch_type}
    
    # Arrange
    # Set up conditions to trigger this branch
    
    # Act
    # result = {parent_func}(...)
    
    # Assert
    # Add assertions for expected branch behavior
"""
    return template


def generate_exception_test_template(gap: Dict[str, Any]) -> str:
    """Generate test template for exception handling."""
    parent_func = gap.get("parent_function")
    exc_type = gap.get("exception_type")

    template = f"""def test_{parent_func}_raises_{exc_type}():
    # Test {exc_type} exception handling
    
    # Arrange
    # Set up conditions to trigger {exc_type}
    
    # Act & Assert
    with pytest.raises({exc_type}):
        {parent_func}(...)
"""
    return template


def calculate_coverage_percentage(
    source_info: Dict[str, Any], test_info: Dict[str, Any]
) -> float:
    """Calculate estimated coverage percentage."""
    total_functions = source_info.get("total_functions", 0)
    tested_functions = len(set(test_info.get("tested_functions", [])))

    if total_functions == 0:
        return 100.0

    coverage = (tested_functions / total_functions) * 100
    return round(coverage, 2)


def test_gap_finder(source_code: str, test_code: str, options: dict = None) -> dict:
    """
    Main function to identify test gaps in source code.

    Args:
        source_code: The source code to find gaps in
        test_code: Existing test code
        options: Analysis options

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - coverage_percentage: Estimated coverage
        - gaps: List of untested functions/branches
        - prioritized_gaps: Gaps ranked by risk
        - test_suggestions: Suggestions for filling gaps
    """
    if options is None:
        options = {}

    if not source_code:
        return {"status": "error", "error": "No source code provided"}

    source_info = parse_source_code(source_code)
    if source_info.get("status") == "error":
        return source_info

    if not test_code:
        test_info = {
            "status": "success",
            "tests": [],
            "tested_functions": [],
            "tested_classes": [],
            "total_tests": 0,
        }
    else:
        test_info = parse_test_code(test_code)

    gaps = identify_gaps(source_info, test_info)

    prioritized_gaps = prioritize_gaps(gaps)

    suggestions = generate_test_suggestions(gaps, source_info)

    coverage_percentage = calculate_coverage_percentage(source_info, test_info)

    return {
        "status": "success",
        "coverage_percentage": coverage_percentage,
        "total_functions": source_info.get("total_functions", 0),
        "total_branches": source_info.get("total_branches", 0),
        "total_tests": test_info.get("total_tests", 0),
        "gaps": gaps,
        "prioritized_gaps": prioritized_gaps,
        "test_suggestions": suggestions,
        "summary": {
            "untested_functions": len([g for g in gaps if g["type"] == "function"]),
            "untested_branches": len([g for g in gaps if g["type"] == "branch"]),
            "untested_exceptions": len([g for g in gaps if g["type"] == "exception"]),
            "critical_gaps": len(
                [
                    g
                    for g in prioritized_gaps
                    if g.get("suggested_priority") == "critical"
                ]
            ),
            "high_priority_gaps": len(
                [
                    g
                    for g in prioritized_gaps
                    if g.get("suggested_priority") in ["critical", "high"]
                ]
            ),
        },
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    action = payload.get("action", "analyze")
    source_code = payload.get("source_code", "")
    test_code = payload.get("test_code", "")
    options = payload.get("options", {})

    if action == "analyze":
        result = test_gap_finder(source_code, test_code, options)
    elif action == "parse_source":
        result = parse_source_code(source_code)
    elif action == "parse_tests":
        result = parse_test_code(test_code)
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata."""
    return {
        "name": "test-gap-finder",
        "description": "Identifies untested code paths in Python source code",
        "version": "1.0.0",
        "domain": "TESTING_QUALITY",
    }
