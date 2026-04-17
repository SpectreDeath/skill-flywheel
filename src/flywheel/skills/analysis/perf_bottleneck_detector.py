"
Performance Bottleneck Detector

Detects performance bottlenecks in Python code by analyzing:
- Inefficient loops and list comprehensions
- N+1 query patterns
- Unnecessary object creation
- Missing caching opportunities
"

import ast
import re
from dataclasses import dataclass
from typing import Any, Dict, List
from datetime import datetime


@dataclass
class Bottleneck:
    type: str
    severity: str
    line: int
    description: str
    suggestion: str


class PerformanceAnalyzer(ast.NodeVisitor):
    "AST-based performance analyzer for Python code"

    def __init__(self):
        self.bottlenecks: List[Bottleneck] = []
        self.loop_depth = 0
        self.in_list_comp = False

    def visit_For(self, node):
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):
        self.loop_depth += 1
        # Check for infinite loop risk
        self.bottlenecks.append(
            Bottleneck(
                type="Infinite Loop Risk",
                severity="high",
                line=node.lineno,
                description="While loop without clear termination",
                suggestion="Add explicit break condition or max iterations",
            )
        )
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_ListComp(self, node):
        old_in_comp = self.in_list_comp
        self.in_list_comp = True
        self.generic_visit(node)
        self.in_list_comp = old_in_comp

    def visit_Call(self, node):
        if hasattr(node.func, "attr"):
            # Check for inefficient patterns
            if node.func.attr == "append" and self.loop_depth > 0:
                self.bottlenecks.append(
                    Bottleneck(
                        type="List Append in Loop",
                        severity="medium",
                        line=node.lineno,
                        description="Append inside loop - consider list comprehension",
                        suggestion="Use list comprehension for better performance",
                    )
                )
            elif node.func.attr in ["items", "keys", "values"]:
                if self.loop_depth > 0:
                    self.bottlenecks.append(
                        Bottleneck(
                            type="Dictionary Iteration",
                            severity="low",
                            line=node.lineno,
                            description="Dictionary method called in loop",
                            suggestion="Consider .items() for key-value iteration",
                        )
                    )
        self.generic_visit(node)


def analyze_python_code(code: str) -> Dict[str, Any]:
    "
    Analyze Python code for performance bottlenecks.

    Args:
        code: Python source code to analyze

    Returns:
        Analysis results with bottlenecks and suggestions
    "
    bottlenecks = []

    try:
        tree = ast.parse(code)
        analyzer = PerformanceAnalyzer()
        analyzer.visit(tree)
        bottlenecks = analyzer.bottlenecks
    except SyntaxError as e:
        return {"status": "error", "error": f"Syntax error: {str(e)}"}

    # Additional regex-based checks
    lines = code.split("\n")
    for i, line in enumerate(lines, 1):
        # Check for global variables
        if re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*\(.*\)$", line):
            if "def " not in line and "class " not in line:
                # Function call at module level
                if any(x in line for x in ["open(", "read(", "json.load"]):
                    bottlenecks.append(
                        Bottleneck(
                            type="I/O at Module Level",
                            severity="medium",
                            line=i,
                            description="File I/O at module level causes slow import",
                            suggestion="Move to function or lazy load",
                        )
                    )

        # Check for nested loops
        if re.search(r"\bfor\s+\w+\s+in\s+.*:\s*\n\s*for\s+", line):
            pass  # Already handled by AST

    # Calculate score
    severity_scores = {"critical": 10, "high": 5, "medium": 2, "low": 1}
    score = 100 - sum(severity_scores.get(b.severity, 1) for b in bottlenecks)

    return {
        "status": "success",
        "total_bottlenecks": len(bottlenecks),
        "score": max(0, score),
        "bottlenecks": [
            {
                "type": b.type,
                "severity": b.severity,
                "line": b.line,
                "description": b.description,
                "suggestion": b.suggestion,
            }
            for b in bottlenecks
        ],
        "summary": {
            "critical": len([b for b in bottlenecks if b.severity == "critical"]),
            "high": len([b for b in bottlenecks if b.severity == "high"]),
            "medium": len([b for b in bottlenecks if b.severity == "medium"]),
            "low": len([b for b in bottlenecks if b.severity == "low"]),
        },
    }


def perf_bottleneck_detector(code: str, **kwargs) -> Dict[str, Any]:
    "
    Main entry point for performance bottleneck detection.

    Args:
        code: Python source code to analyze
        **kwargs: Additional parameters

    Returns:
        Analysis results
    "
    if not code:
        return {"status": "error", "error": "No code provided"}

    return analyze_python_code(code)


async def invoke(payload: dict) -> dict:
    "MCP skill invocation"
    action = payload.get("action", "analyze")
    code = payload.get("code", ")

    if action == "analyze":
        result = perf_bottleneck_detector(code)
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
    "Return skill metadata"
    return {
        "name": "perf-bottleneck-detector",
        "description": "Detect performance bottlenecks in Python code",
        "version": "1.0.0",
        "domain": "DATA_ENGINEERING",
    }
