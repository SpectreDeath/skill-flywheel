"""
Coverage Optimizer

Suggests tests to maximize code coverage by:
- Analyzing current coverage data
- Identifying uncovered lines and branches
- Suggesting specific test cases
- Prioritizing by impact and value
- Generating ready-to-complete test stubs
"""

import ast
from dataclasses import dataclass
from typing import Any, List, Set
from datetime import datetime


@dataclass
class CoverageMetrics:
    line_coverage: float
    branch_coverage: float
    function_coverage: float
    total_lines: int
    covered_lines: int
    total_branches: int
    covered_branches: int
    total_functions: int
    covered_functions: int


@dataclass
class GapInfo:
    gap_type: str
    line: int
    code: str
    context: str
    branch_condition: str | None = None
    uncovered_values: List[Any] | None = None
    priority: str = "medium"
    impact_score: float = 0.0


def analyze_coverage(source_code: str, coverage_data: dict) -> CoverageMetrics:
    """Analyze coverage data and compute metrics."""
    total_lines = coverage_data.get("total_lines", 0)
    covered_lines = coverage_data.get("covered_lines", 0)
    total_branches = coverage_data.get("total_branches", 0)
    covered_branches = coverage_data.get("covered_branches", 0)
    total_functions = coverage_data.get("total_functions", 0)
    covered_functions = coverage_data.get("covered_functions", 0)

    line_coverage = (covered_lines / total_lines * 100) if total_lines > 0 else 0.0
    branch_coverage = (
        (covered_branches / total_branches * 100) if total_branches > 0 else 0.0
    )
    function_coverage = (
        (covered_functions / total_functions * 100) if total_functions > 0 else 0.0
    )

    return CoverageMetrics(
        line_coverage=round(line_coverage, 2),
        branch_coverage=round(branch_coverage, 2),
        function_coverage=round(function_coverage, 2),
        total_lines=total_lines,
        covered_lines=covered_lines,
        total_branches=total_branches,
        covered_branches=covered_branches,
        total_functions=total_functions,
        covered_functions=covered_functions,
    )


def parse_coverage_report(source_code: str, coverage_report: dict) -> dict:
    """Parse coverage report to extract uncovered lines and branches."""
    uncovered_lines = coverage_report.get("uncovered_lines", [])
    uncovered_branches = coverage_report.get("uncovered_branches", [])
    covered_lines = coverage_report.get("covered_lines", [])

    lines = source_code.split("\n")
    line_map = {}
    for i, line in enumerate(lines, start=1):
        line_map[i] = line

    gaps = []

    for line_num in uncovered_lines:
        if 1 <= line_num <= len(line_map):
            gaps.append(
                {
                    "type": "line",
                    "line": line_num,
                    "code": line_map.get(line_num, "").strip(),
                    "context": _get_line_context(lines, line_num),
                }
            )

    for branch in uncovered_branches:
        branch_line = branch.get("line")
        condition = branch.get("condition", "")
        gaps.append(
            {
                "type": "branch",
                "line": branch_line,
                "code": line_map.get(branch_line, "").strip(),
                "context": _get_line_context(lines, branch_line),
                "branch_condition": condition,
                "uncovered_values": branch.get("uncovered_values", []),
            }
        )

    return {
        "status": "success",
        "uncovered_lines": uncovered_lines,
        "uncovered_branches": uncovered_branches,
        "covered_lines": covered_lines,
        "gaps": gaps,
    }


def _get_line_context(lines: List[str], line_num: int, context: int = 3) -> str:
    """Get surrounding context for a line."""
    start = max(0, line_num - context - 1)
    end = min(len(lines), line_num + context)
    context_lines = lines[start:end]
    return "\n".join(context_lines)


def identify_uncovered_paths(source_code: str, coverage_data: dict) -> List[GapInfo]:
    """Identify uncovered code paths from source and coverage data."""
    gaps = []

    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return gaps

    uncovered_lines = set(coverage_data.get("uncovered_lines", []))
    uncovered_branches = coverage_data.get("uncovered_branches", [])

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            gaps.extend(
                _analyze_function_coverage(
                    node, uncovered_lines, uncovered_branches, source_code
                )
            )

    return gaps


def _analyze_function_coverage(
    node: ast.FunctionDef,
    uncovered_lines: Set[int],
    uncovered_branches: List[dict],
    source_code: str,
) -> List[GapInfo]:
    """Analyze coverage for a single function."""
    gaps = []
    func_name = node.name
    range(node.lineno, node.end_lineno + 1)

    for child in ast.walk(node):
        if isinstance(child, ast.If):
            if child.lineno in uncovered_lines:
                gaps.append(
                    GapInfo(
                        gap_type="branch",
                        line=child.lineno,
                        code=_get_line_code(source_code, child.lineno),
                        context=f"in function {func_name}",
                        branch_condition=ast.unparse(child.test)
                        if child.test
                        else None,
                        priority="high",
                        impact_score=_calculate_impact(child),
                    )
                )

        elif isinstance(child, (ast.For, ast.While)):
            if child.lineno in uncovered_lines:
                gaps.append(
                    GapInfo(
                        gap_type="loop",
                        line=child.lineno,
                        code=_get_line_code(source_code, child.lineno),
                        context=f"in function {func_name}",
                        priority="medium",
                        impact_score=0.5,
                    )
                )

        elif isinstance(child, ast.ExceptHandler):
            if child.type and hasattr(child.type, "lineno"):
                if child.type.lineno in uncovered_lines:
                    gaps.append(
                        GapInfo(
                            gap_type="exception",
                            line=child.lineno,
                            code=f"except {ast.unparse(child.type) if child.type else ''}",
                            context=f"in function {func_name}",
                            uncovered_values=[ast.unparse(child.type)]
                            if child.type
                            else [],
                            priority="medium",
                            impact_score=0.6,
                        )
                    )

        elif isinstance(child, ast.BoolOp) and child.lineno in uncovered_lines:
            gaps.append(
                GapInfo(
                    gap_type="boolean",
                    line=child.lineno,
                    code=_get_line_code(source_code, child.lineno),
                    context=f"in function {func_name}",
                    branch_condition=ast.unparse(child),
                    priority="medium",
                    impact_score=0.4,
                )
            )

    return gaps


def _get_line_code(source_code: str, line_num: int) -> str:
    """Get the code at a specific line number."""
    lines = source_code.split("\n")
    if 0 < line_num <= len(lines):
        return lines[line_num - 1].strip()
    return ""


def _calculate_impact(node: ast.AST) -> float:
    """Calculate impact score for a node."""
    score = 0.7

    for child in ast.walk(node):
        if isinstance(child, (ast.Call, ast.Attribute)):
            score += 0.1

    return min(score, 1.0)


def suggest_test_cases(gaps: List[GapInfo], source_code: str) -> List[dict]:
    """Generate test case suggestions for uncovered code."""
    suggestions = []

    for gap in gaps:
        if gap.gap_type == "branch":
            suggestion = _suggest_branch_test(gap, source_code)
        elif gap.gap_type == "loop":
            suggestion = _suggest_loop_test(gap, source_code)
        elif gap.gap_type == "exception":
            suggestion = _suggest_exception_test(gap)
        elif gap.gap_type == "boolean":
            suggestion = _suggest_boolean_test(gap, source_code)
        else:
            suggestion = _suggest_line_test(gap, source_code)

        suggestions.append(suggestion)

    return suggestions


def _suggest_branch_test(gap: GapInfo, source_code: str) -> dict:
    """Suggest test for an uncovered branch."""
    condition = gap.branch_condition or "condition"

    return {
        "type": "branch",
        "line": gap.line,
        "description": f"Test uncovered branch at line {gap.line}",
        "test_inputs": {
            "true_case": _generate_true_case_inputs(condition),
            "false_case": _generate_false_case_inputs(condition),
        },
        "expected_behavior": "Exercise both true and false paths of the condition",
        "priority": gap.priority,
        "impact": gap.impact_score,
    }


def _generate_true_case_inputs(condition: str) -> List[dict]:
    """Generate inputs that make the condition evaluate to True."""
    return [{"condition": condition, "should_be": True}]


def _generate_false_case_inputs(condition: str) -> List[dict]:
    """Generate inputs that make the condition evaluate to False."""
    return [{"condition": condition, "should_be": False}]


def _suggest_loop_test(gap: GapInfo, source_code: str) -> dict:
    """Suggest test for uncovered loop."""
    return {
        "type": "loop",
        "line": gap.line,
        "description": f"Test uncovered loop at line {gap.line}",
        "test_inputs": {
            "empty_iterable": [],
            "single_item": [1],
            "multiple_items": [1, 2, 3],
            "edge_case": None,
        },
        "expected_behavior": "Test loop with empty, single, and multiple iterations",
        "priority": gap.priority,
        "impact": gap.impact_score,
    }


def _suggest_exception_test(gap: GapInfo) -> dict:
    """Suggest test for uncovered exception handling."""
    exc_type = gap.uncovered_values[0] if gap.uncovered_values else "Exception"

    return {
        "type": "exception",
        "line": gap.line,
        "description": f"Test exception handling for {exc_type}",
        "test_inputs": {
            "trigger_exception": {
                "method": "raise",
                "exception_type": exc_type,
            },
            "no_exception": {
                "method": "normal",
            },
        },
        "expected_behavior": f"Verify {exc_type} is caught and handled correctly",
        "priority": gap.priority,
        "impact": gap.impact_score,
    }


def _suggest_boolean_test(gap: GapInfo, source_code: str) -> dict:
    """Suggest test for uncovered boolean operations."""
    return {
        "type": "boolean",
        "line": gap.line,
        "description": f"Test boolean operation at line {gap.line}",
        "test_inputs": {
            "all_true": [True, True],
            "all_false": [False, False],
            "mixed": [True, False],
        },
        "expected_behavior": "Cover all boolean operation outcomes",
        "priority": gap.priority,
        "impact": gap.impact_score,
    }


def _suggest_line_test(gap: GapInfo, source_code: str) -> dict:
    """Suggest test for uncovered line."""
    return {
        "type": "line",
        "line": gap.line,
        "description": f"Test uncovered line {gap.line}",
        "test_inputs": {},
        "expected_behavior": "Execute the uncovered line",
        "priority": gap.priority,
        "impact": gap.impact_score,
    }


def prioritize_by_impact(
    suggestions: List[dict], target_coverage: float, current_coverage: float
) -> List[dict]:
    """Prioritize test suggestions by impact and coverage gain potential."""
    gap = target_coverage - current_coverage

    for suggestion in suggestions:
        base_priority = suggestion.get("priority", "medium")
        impact = suggestion.get("impact", 0.5)

        if base_priority == "high":
            priority_score = 3.0
        elif base_priority == "medium":
            priority_score = 2.0
        else:
            priority_score = 1.0

        suggestion["priority_score"] = priority_score * impact

        if gap > 20 and suggestion["type"] in ["branch", "exception"]:
            suggestion["priority_score"] *= 1.5

    return sorted(suggestions, key=lambda x: x.get("priority_score", 0), reverse=True)


def generate_test_stubs(
    suggestions: List[dict], source_code: str, test_framework: str = "pytest"
) -> List[dict]:
    """Generate ready-to-complete test stubs."""
    stubs = []

    tree = ast.parse(source_code)
    functions = {
        node.name: node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    }

    for suggestion in suggestions:
        stub = _generate_single_stub(suggestion, functions, test_framework)
        stubs.append(stub)

    return stubs


def _generate_single_stub(
    suggestion: dict, functions: dict, test_framework: str
) -> dict:
    """Generate a single test stub."""
    suggestion.get("type", "line")
    suggestion.get("line", 0)

    if test_framework == "pytest":
        return _generate_pytest_stub(suggestion, functions)
    elif test_framework == "unittest":
        return _generate_unittest_stub(suggestion, functions)
    else:
        return _generate_generic_stub(suggestion, functions)


def _generate_pytest_stub(suggestion: dict, functions: dict) -> dict:
    """Generate pytest test stub."""
    test_type = suggestion.get("type", "line")
    line = suggestion.get("line", 0)
    desc = suggestion.get("description", "")

    if test_type == "branch":
        template = f'''def test_branch_at_line_{line}():
    """
    {desc}
    
    Test inputs for true case: {suggestion.get("test_inputs", {}).get("true_case", [])}
    Test inputs for false case: {suggestion.get("test_inputs", {}).get("false_case", [])}
    """
    # Arrange
    # TODO: Set up test data for branch condition
    
    # Act
    # TODO: Call the function with test inputs
    
    # Assert
    # TODO: Verify both branch paths are exercised
    pass

def test_branch_at_line_{line}_true():
    """Test true branch path."""
    # TODO: Implement true path test
    pass

def test_branch_at_line_{line}_false():
    """Test false branch path."""
    # TODO: Implement false path test
    pass
'''
    elif test_type == "exception":
        template = f'''def test_exception_at_line_{line}():
    """
    {desc}
    
    Exception type: {suggestion.get("test_inputs", {}).get("trigger_exception", {}).get("exception_type")}
    """
    # TODO: Implement exception test
    pass
'''
    elif test_type == "loop":
        template = f'''def test_loop_at_line_{line}():
    """
    {desc}
    """
    # Test with empty iterable
    # TODO: Call function with empty iterable
    
    # Test with single item
    # TODO: Call function with single item
    
    # Test with multiple items
    # TODO: Call function with multiple items
    pass
'''
    else:
        template = f'''def test_line_{line}():
    """
    {desc}
    """
    # TODO: Implement test for line {line}
    pass
'''

    return {
        "test_name": f"test_{test_type}_at_line_{line}",
        "line": line,
        "type": test_type,
        "template": template,
        "framework": "pytest",
    }


def _generate_unittest_stub(suggestion: dict, functions: dict) -> dict:
    """Generate unittest test stub."""
    test_type = suggestion.get("type", "line")
    line = suggestion.get("line", 0)

    template = f'''class TestLine{line}(unittest.TestCase):
    """Tests for uncovered line {line}."""

    def test_{test_type}_at_line_{line}(self):
        """{suggestion.get("description", "")}"""
        # TODO: Implement test
        pass
'''

    return {
        "test_name": f"TestLine{line}.test_{test_type}_at_line_{line}",
        "line": line,
        "type": test_type,
        "template": template,
        "framework": "unittest",
    }


def _generate_generic_stub(suggestion: dict, functions: dict) -> dict:
    """Generate generic test stub."""
    test_type = suggestion.get("type", "line")
    line = suggestion.get("line", 0)

    template = f'''def test_{test_type}_at_line_{line}():
    """
    {suggestion.get("description", "")}
    
    Expected behavior: {suggestion.get("expected_behavior", "")}
    Priority: {suggestion.get("priority", "medium")}
    """
    # TODO: Complete this test
    pass
'''

    return {
        "test_name": f"test_{test_type}_at_line_{line}",
        "line": line,
        "type": test_type,
        "template": template,
        "framework": "generic",
    }


def estimate_coverage_gain(suggestion: dict, coverage_data: dict) -> float:
    """Estimate coverage percentage gain from implementing a suggestion."""
    test_type = suggestion.get("type", "line")
    impact = suggestion.get("impact", 0.5)

    total_lines = coverage_data.get("total_lines", 100)
    estimated_lines_per_test = {
        "branch": 2,
        "exception": 2,
        "loop": 3,
        "boolean": 2,
        "line": 1,
    }

    lines_covered = estimated_lines_per_test.get(test_type, 1)
    gain = (lines_covered / total_lines) * 100 * impact

    return round(gain, 2)


def coverage_optimizer(
    source_code: str, coverage_data: dict, options: dict = None
) -> dict:
    """
    Main function to optimize test coverage.

    Args:
        source_code: The source code to analyze
        coverage_data: Coverage information (line numbers, branches)
        options: Target coverage percentage, test framework, etc.

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - current_coverage: Current coverage metrics
        - gaps: Uncovered lines/branches
        - suggestions: Prioritized test suggestions
        - test_stubs: Generated test stubs
    """
    if options is None:
        options = {}

    if not source_code:
        return {"status": "error", "error": "No source code provided"}

    target_coverage = options.get("target_coverage", 90.0)
    test_framework = options.get("test_framework", "pytest")

    metrics = analyze_coverage(source_code, coverage_data)

    gaps_result = parse_coverage_report(source_code, coverage_data)
    if gaps_result.get("status") == "error":
        gaps_result = {"gaps": []}

    uncovered_paths = identify_uncovered_paths(source_code, coverage_data)

    all_gaps = gaps_result.get("gaps", [])
    for path in uncovered_paths:
        all_gaps.append(
            {
                "gap_type": path.gap_type,
                "line": path.line,
                "code": path.code,
                "context": path.context,
                "branch_condition": path.branch_condition,
                "priority": path.priority,
                "impact": path.impact_score,
            }
        )

    suggestions = suggest_test_cases(
        [
            GapInfo(
                gap_type=gap.get("gap_type") or gap.get("type", "line"),
                line=gap.get("line", 0),
                code=gap.get("code", ""),
                context=gap.get("context", ""),
                branch_condition=gap.get("branch_condition"),
                uncovered_values=gap.get("uncovered_values"),
                priority=gap.get("priority", "medium"),
                impact_score=gap.get("impact", 0.5),
            )
            if isinstance(gap, dict)
            else gap
            for gap in all_gaps
        ],
        source_code,
    )

    prioritized = prioritize_by_impact(
        suggestions, target_coverage, metrics.line_coverage
    )

    stubs = generate_test_stubs(prioritized, source_code, test_framework)

    estimated_total_gain = sum(
        estimate_coverage_gain(s, coverage_data) for s in prioritized
    )

    return {
        "status": "success",
        "current_coverage": {
            "line_coverage": metrics.line_coverage,
            "branch_coverage": metrics.branch_coverage,
            "function_coverage": metrics.function_coverage,
            "total_lines": metrics.total_lines,
            "covered_lines": metrics.covered_lines,
            "total_branches": metrics.total_branches,
            "covered_branches": metrics.covered_branches,
        },
        "target_coverage": target_coverage,
        "gap_to_target": round(target_coverage - metrics.line_coverage, 2),
        "gaps": all_gaps,
        "suggestions": prioritized,
        "test_stubs": stubs,
        "estimated_coverage_gain": round(estimated_total_gain, 2),
        "summary": {
            "total_gaps": len(all_gaps),
            "branch_gaps": len([g for g in all_gaps if g.get("type") == "branch"]),
            "exception_gaps": len(
                [g for g in all_gaps if g.get("type") == "exception"]
            ),
            "loop_gaps": len([g for g in all_gaps if g.get("type") == "loop"]),
            "line_gaps": len([g for g in all_gaps if g.get("type") == "line"]),
            "high_priority": len(
                [g for g in prioritized if g.get("priority") == "high"]
            ),
            "tests_to_write": len(stubs),
        },
    }


async def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    action = payload.get("action", "optimize")
    source_code = payload.get("source_code", "")
    coverage_data = payload.get("coverage_data", {})
    options = payload.get("options", {})

    if action == "optimize":
        result = coverage_optimizer(source_code, coverage_data, options)
    elif action == "analyze_coverage":
        result = analyze_coverage(source_code, coverage_data)
    elif action == "identify_gaps":
        result = parse_coverage_report(source_code, coverage_data)
    elif action == "suggest_tests":
        gaps = payload.get("gaps", [])
        result = {"suggestions": suggest_test_cases(gaps, source_code)}
    elif action == "generate_stubs":
        suggestions = payload.get("suggestions", [])
        test_framework = options.get("test_framework", "pytest")
        result = {
            "stubs": generate_test_stubs(suggestions, source_code, test_framework)
        }
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata."""
    return {
        "name": "coverage-optimizer",
        "description": "Suggests tests to maximize code coverage with prioritized test cases and ready-to-complete stubs",
        "version": "1.0.0",
        "domain": "TESTING_QUALITY",
        "capabilities": [
            "coverage_analysis",
            "gap_identification",
            "test_suggestion",
            "impact_prioritization",
            "test_stub_generation",
        ],
    }
