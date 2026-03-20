"""
Complexity Analyzer Skill

This module provides skills for analyzing code complexity:
- Cyclomatic complexity calculation
- Cognitive complexity measurement
- Nesting depth analysis
- Function length metrics
- Maintainability index calculation
"""

import ast
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class FunctionMetrics:
    """Metrics for a single function"""

    name: str
    line_start: int
    line_end: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    nesting_depth: int
    lines_of_code: int
    num_decisions: int = 0
    num_loops: int = 0
    num_exceptions: int = 0
    num_returns: int = 0
    is_method: bool = False
    class_name: str | None = None


@dataclass
class ClassMetrics:
    """Metrics for a single class"""

    name: str
    line_start: int
    line_end: int
    num_methods: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    nesting_depth: int
    lines_of_code: int
    method_metrics: List[FunctionMetrics] = field(default_factory=list)


class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor to calculate complexity metrics"""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.functions: List[FunctionMetrics] = []
        self.classes: List[ClassMetrics] = []
        self.current_class: str | None = None
        self.current_function: str | None = None
        self.current_nesting = 0
        self.max_nesting_global = 0

        self._cyclomatic_complexity = 1
        self._cognitive_complexity = 0
        self._max_nesting = 0
        self._num_decisions = 0
        self._num_loops = 0
        self._num_exceptions = 0
        self._num_returns = 0

        self._function_start_line = 0
        self._function_end_line = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        old_class = self.current_class
        self.current_class = node.name
        class_start = node.lineno
        class_end = node.end_lineno if hasattr(node, "end_lineno") else node.lineno

        method_metrics = []
        class_cyclomatic = 1
        class_cognitive = 0
        class_nesting = 0
        class_loc = 0

        self.generic_visit(node)

        for child in ast.walk(node):
            if isinstance(child, ast.FunctionDef):
                func_metric = self._extract_function_metrics(child)
                if func_metric:
                    method_metrics.append(func_metric)
                    class_cyclomatic += func_metric.cyclomatic_complexity
                    class_cognitive += func_metric.cognitive_complexity
                    class_nesting = max(class_nesting, func_metric.nesting_depth)
                    class_loc += func_metric.lines_of_code

        if not method_metrics:
            class_loc = len(self.source_lines[class_start - 1 : class_end])

        class_metrics = ClassMetrics(
            name=node.name,
            line_start=class_start,
            line_end=class_end,
            num_methods=len(method_metrics),
            cyclomatic_complexity=class_cyclomatic,
            cognitive_complexity=class_cognitive,
            nesting_depth=class_nesting,
            lines_of_code=class_loc,
            method_metrics=method_metrics,
        )
        self.classes.append(class_metrics)

        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._enter_function(node)
        self.generic_visit(node)
        self._exit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._enter_function(node)
        self.generic_visit(node)
        self._exit_function(node)

    def _enter_function(self, node: ast.FunctionDef) -> None:
        old_cognitive = self._cognitive_complexity
        old_cyclomatic = self._cyclomatic_complexity
        old_nesting = self._max_nesting
        old_decisions = self._num_decisions
        old_loops = self._num_loops
        old_exceptions = self._num_exceptions
        old_returns = self._num_returns
        old_func = self.current_function
        old_start = self._function_start_line

        self._cyclomatic_complexity = 1
        self._cognitive_complexity = 0
        self._max_nesting = 0
        self._num_decisions = 0
        self._num_loops = 0
        self._num_exceptions = 0
        self._num_returns = 0
        self.current_function = node.name
        self._function_start_line = node.lineno

        self._visit_with_complexity(node)

        self._function_end_line = (
            node.end_lineno if hasattr(node, "end_lineno") else node.lineno
        )

        is_method = self.current_class is not None

        func_metric = FunctionMetrics(
            name=node.name,
            line_start=node.lineno,
            line_end=self._function_end_line,
            cyclomatic_complexity=self._cyclomatic_complexity,
            cognitive_complexity=self._cognitive_complexity,
            nesting_depth=self._max_nesting,
            lines_of_code=max(1, self._function_end_line - node.lineno + 1),
            num_decisions=self._num_decisions,
            num_loops=self._num_loops,
            num_exceptions=self._num_exceptions,
            num_returns=self._num_returns,
            is_method=is_method,
            class_name=self.current_class,
        )
        self.functions.append(func_metric)

        self.max_nesting_global = max(self.max_nesting_global, self._max_nesting)

        self._cognitive_complexity = old_cognitive
        self._cyclomatic_complexity = old_cyclomatic
        self._max_nesting = old_nesting
        self._num_decisions = old_decisions
        self._num_loops = old_loops
        self._num_exceptions = old_exceptions
        self._num_returns = old_returns
        self.current_function = old_func
        self._function_start_line = old_start

    def _exit_function(self, node: ast.FunctionDef) -> None:
        pass

    def _visit_with_complexity(self, node: ast.AST) -> None:
        for child in ast.iter_child_nodes(node):
            self._process_node(child)
            self._visit_with_complexity(child)

    def _process_node(self, node: ast.AST) -> None:
        if isinstance(node, (ast.If, ast.IfExp)):
            self._cyclomatic_complexity += 1
            self._num_decisions += 1
            self._cognitive_complexity += 1 + self._max_nesting
        elif isinstance(node, (ast.For, ast.While, ast.AsyncFor)):
            self._cyclomatic_complexity += 1
            self._num_loops += 1
            self._cognitive_complexity += 1 + self._max_nesting
        elif isinstance(node, ast.BoolOp):
            if isinstance(node.op, (ast.And, ast.Or)):
                self._cyclomatic_complexity += len(node.values) - 1
                self._num_decisions += len(node.values) - 1
        elif isinstance(node, ast.ExceptHandler):
            self._cyclomatic_complexity += 1
            self._num_exceptions += 1
            self._cognitive_complexity += 1 + self._max_nesting
        elif isinstance(node, ast.With):
            for item in node.items:
                if item.optional_vars:
                    self._cyclomatic_complexity += 1
        elif isinstance(node, ast.Assert):
            self._cyclomatic_complexity += 1
        elif isinstance(node, (ast.Return, ast.Yield, ast.YieldFrom)):
            self._num_returns += 1
            if isinstance(node.value, ast.IfExp):
                self._cyclomatic_complexity += 1

        if isinstance(
            node,
            (
                ast.If,
                ast.For,
                ast.While,
                ast.AsyncFor,
                ast.With,
                ast.Try,
                ast.ExceptHandler,
                ast.ListComp,
                ast.SetComp,
                ast.DictComp,
                ast.GeneratorExp,
                ast.Lambda,
            ),
        ):
            self._max_nesting += 1


def calculate_cyclomatic_complexity(code: str) -> int:
    """Calculate overall cyclomatic complexity of the code"""
    try:
        tree = ast.parse(code)
        lines = code.splitlines()
        visitor = ComplexityVisitor(lines)
        visitor.visit(tree)

        total = 1
        for func in visitor.functions:
            total += func.cyclomatic_complexity - 1

        return max(1, total)
    except SyntaxError:
        return 1


def calculate_cognitive_complexity(code: str) -> int:
    """Calculate overall cognitive complexity of the code"""
    try:
        tree = ast.parse(code)
        lines = code.splitlines()
        visitor = ComplexityVisitor(lines)
        visitor.visit(tree)

        total = 0
        for func in visitor.functions:
            total += func.cognitive_complexity

        return total
    except SyntaxError:
        return 0


def calculate_nesting_depth(code: str) -> int:
    """Calculate maximum nesting depth in the code"""
    try:
        tree = ast.parse(code)
        lines = code.splitlines()
        visitor = ComplexityVisitor(lines)
        visitor.visit(tree)

        return visitor.max_nesting_global
    except SyntaxError:
        return 0


def calculate_maintainability_index(
    cyclomatic_complexity: float, lines_of_code: int, comment_lines: int = 0
) -> float:
    """Calculate maintainability index (0-100)

    Formula based on Microsoft Visual Studio metrics:
    MI = 171 - 5.2 * ln(Halstead Volume) - 0.23 * (Cyclomatic Complexity) - 16.2 * ln(LOC)

    Simplified version:
    MI = 171 - 5.2 * ln(estimated_volume) - 0.23 * cyclomatic - 16.2 * ln(loc)
    """
    if lines_of_code <= 0:
        return 100.0

    import math

    loc = float(lines_of_code)
    cc = float(cyclomatic_complexity)

    mi = 171.0 - 5.2 * math.log(loc + 1) - 0.23 * cc - 16.2 * math.log(loc + 1)
    mi = mi - 0.23 * (comment_lines / (loc + 1)) * 100

    mi = max(0, min(100, mi))

    mi = mi * 100 / 171

    return round(mi, 2)


def count_lines_of_code(code: str) -> Tuple[int, int, int]:
    """Count total, code, and comment lines"""
    lines = code.splitlines()

    total_lines = len(lines)
    code_lines = 0
    comment_lines = 0
    in_multiline_string = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith('"""') or stripped.startswith("'''"):
            if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                continue
            in_multiline_string = not in_multiline_string
            comment_lines += 1
            continue

        if in_multiline_string:
            comment_lines += 1
            continue

        if stripped.startswith("#"):
            comment_lines += 1
        else:
            code_lines += 1

    return total_lines, code_lines, comment_lines


def get_complexity_rating(complexity: int) -> str:
    """Get rating string for complexity value"""
    if complexity <= 10:
        return "low"
    elif complexity <= 20:
        return "moderate"
    elif complexity <= 40:
        return "high"
    else:
        return "very_high"


def get_maintainability_rating(mi: float) -> str:
    """Get rating string for maintainability index"""
    if mi >= 80:
        return "good"
    elif mi >= 60:
        return "moderate"
    elif mi >= 40:
        return "poor"
    else:
        return "very_poor"


def complexity_analyzer(code: str, options: dict = None) -> dict:
    """
    Analyze code complexity with various metrics

    Args:
        code: Python source code to analyze
        options: Dictionary with thresholds and options:
            - max_cyclomatic: Max cyclomatic complexity threshold (default: 20)
            - max_cognitive: Max cognitive complexity threshold (default: 30)
            - max_nesting: Max nesting depth threshold (default: 5)
            - max_function_length: Max lines per function (default: 50)
            - include_classes: Include class metrics (default: True)
            - include_functions: Include function metrics (default: True)
            - max_hotspots: Number of hotspots to return (default: 10)

    Returns:
        dict with:
            - status: "success" or "error"
            - overall_complexity: Aggregate complexity score
            - functions: Per-function complexity metrics
            - classes: Per-class complexity metrics
            - hotspots: Most complex areas
            - maintainability_index: 0-100 score
    """
    if options is None:
        options = {}

    max_cyclomatic = options.get("max_cyclomatic", 20)
    max_cognitive = options.get("max_cognitive", 30)
    max_nesting = options.get("max_nesting", 5)
    max_function_length = options.get("max_function_length", 50)
    include_classes = options.get("include_classes", True)
    include_functions = options.get("include_functions", True)
    max_hotspots = options.get("max_hotspots", 10)

    try:
        tree = ast.parse(code)
        lines = code.splitlines()

        total_lines, code_lines, comment_lines = count_lines_of_code(code)

        visitor = ComplexityVisitor(lines)
        visitor.visit(tree)

        total_cyclomatic = 1
        total_cognitive = 0
        for func in visitor.functions:
            total_cyclomatic += func.cyclomatic_complexity - 1
            total_cognitive += func.cognitive_complexity

        overall_complexity = (
            total_cyclomatic * 2
            + total_cognitive
            + visitor.max_nesting_global * 5
            + (total_lines / 10)
        )

        maintainability_index = calculate_maintainability_index(
            total_cyclomatic, code_lines, comment_lines
        )

        function_metrics = []
        if include_functions:
            for func in visitor.functions:
                func_data = {
                    "name": func.name,
                    "line_start": func.line_start,
                    "line_end": func.line_end,
                    "lines_of_code": func.lines_of_code,
                    "cyclomatic_complexity": func.cyclomatic_complexity,
                    "cognitive_complexity": func.cognitive_complexity,
                    "nesting_depth": func.nesting_depth,
                    "num_decisions": func.num_decisions,
                    "num_loops": func.num_loops,
                    "num_exceptions": func.num_exceptions,
                    "num_returns": func.num_returns,
                    "is_method": func.is_method,
                    "class_name": func.class_name,
                    "rating": get_complexity_rating(func.cyclomatic_complexity),
                    "violations": _get_violations(
                        func,
                        max_cyclomatic,
                        max_cognitive,
                        max_nesting,
                        max_function_length,
                    ),
                }
                function_metrics.append(func_data)

        class_metrics = []
        if include_classes:
            for cls in visitor.classes:
                cls_data = {
                    "name": cls.name,
                    "line_start": cls.line_start,
                    "line_end": cls.line_end,
                    "lines_of_code": cls.lines_of_code,
                    "num_methods": cls.num_methods,
                    "cyclomatic_complexity": cls.cyclomatic_complexity,
                    "cognitive_complexity": cls.cognitive_complexity,
                    "nesting_depth": cls.nesting_depth,
                    "rating": get_complexity_rating(cls.cyclomatic_complexity),
                    "methods": [
                        {
                            "name": m.name,
                            "cyclomatic_complexity": m.cyclomatic_complexity,
                            "cognitive_complexity": m.cognitive_complexity,
                        }
                        for m in cls.method_metrics
                    ],
                }
                class_metrics.append(cls_data)

        hotspots = _identify_hotspots(
            visitor.functions,
            visitor.classes,
            max_cyclomatic,
            max_cognitive,
            max_nesting,
            max_hotspots,
        )

        return {
            "status": "success",
            "overall_complexity": round(overall_complexity, 2),
            "metrics_summary": {
                "total_lines": total_lines,
                "code_lines": code_lines,
                "comment_lines": comment_lines,
                "total_cyclomatic_complexity": max(1, total_cyclomatic),
                "total_cognitive_complexity": total_cognitive,
                "max_nesting_depth": visitor.max_nesting_global,
                "num_functions": len(visitor.functions),
                "num_classes": len(visitor.classes),
            },
            "functions": function_metrics,
            "classes": class_metrics,
            "hotspots": hotspots,
            "maintainability_index": maintainability_index,
            "maintainability_rating": get_maintainability_rating(maintainability_index),
            "thresholds": {
                "cyclomatic": max_cyclomatic,
                "cognitive": max_cognitive,
                "nesting": max_nesting,
                "function_length": max_function_length,
            },
        }

    except SyntaxError as e:
        return {
            "status": "error",
            "message": f"Syntax error in code: {str(e)}",
            "overall_complexity": 0,
            "functions": [],
            "classes": [],
            "hotspots": [],
            "maintainability_index": 0,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error analyzing complexity: {str(e)}",
            "overall_complexity": 0,
            "functions": [],
            "classes": [],
            "hotspots": [],
            "maintainability_index": 0,
        }


def _get_violations(
    func: FunctionMetrics, max_cc: int, max_cog: int, max_nest: int, max_len: int
) -> List[str]:
    """Get list of threshold violations for a function"""
    violations = []

    if func.cyclomatic_complexity > max_cc:
        violations.append(
            f"Cyclomatic complexity {func.cyclomatic_complexity} exceeds threshold {max_cc}"
        )

    if func.cognitive_complexity > max_cog:
        violations.append(
            f"Cognitive complexity {func.cognitive_complexity} exceeds threshold {max_cog}"
        )

    if func.nesting_depth > max_nest:
        violations.append(
            f"Nesting depth {func.nesting_depth} exceeds threshold {max_nest}"
        )

    if func.lines_of_code > max_len:
        violations.append(
            f"Function length {func.lines_of_code} exceeds threshold {max_len}"
        )

    return violations


def _identify_hotspots(
    functions: List[FunctionMetrics],
    classes: List[ClassMetrics],
    max_cc: int,
    max_cog: int,
    max_nest: int,
    limit: int,
) -> List[dict]:
    """Identify the most complex areas (hotspots)"""
    hotspots = []

    for func in functions:
        score = 0
        if func.cyclomatic_complexity > max_cc:
            score += (func.cyclomatic_complexity - max_cc) * 3
        if func.cognitive_complexity > max_cog:
            score += (func.cognitive_complexity - max_cog) * 2
        if func.nesting_depth > max_nest:
            score += (func.nesting_depth - max_nest) * 5

        if score > 0:
            hotspots.append(
                {
                    "type": "method" if func.is_method else "function",
                    "name": func.name,
                    "class_name": func.class_name,
                    "line_start": func.line_start,
                    "line_end": func.line_end,
                    "complexity_score": score,
                    "cyclomatic_complexity": func.cyclomatic_complexity,
                    "cognitive_complexity": func.cognitive_complexity,
                    "nesting_depth": func.nesting_depth,
                    "issues": _get_violations(func, max_cc, max_cog, max_nest, 50),
                }
            )

    for cls in classes:
        for method in cls.method_metrics:
            if method.cyclomatic_complexity > max_cc * 2:
                hotspots.append(
                    {
                        "type": "method",
                        "name": method.name,
                        "class_name": cls.name,
                        "line_start": method.line_start,
                        "line_end": method.line_end,
                        "complexity_score": method.cyclomatic_complexity,
                        "cyclomatic_complexity": method.cyclomatic_complexity,
                        "cognitive_complexity": method.cognitive_complexity,
                        "nesting_depth": method.nesting_depth,
                        "issues": [
                            f"Very high cyclomatic complexity: {method.cyclomatic_complexity}"
                        ],
                    }
                )

    hotspots.sort(key=lambda x: x["complexity_score"], reverse=True)

    return hotspots[:limit]


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation

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
        return {"result": {"status": "error", "message": "No code provided"}}

    result = complexity_analyzer(code, options)
    return {"result": result}


def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "complexity-analyzer",
        "description": "Analyze Python code complexity - measures cyclomatic complexity, cognitive complexity, nesting depth, function length, and maintainability index to identify code hotspots and quality issues",
        "version": "1.0.0",
        "domain": "CODEBASE_INTELLIGENCE",
    }


if __name__ == "__main__":
    test_code = """
def simple_function(x, y):
    return x + y


def moderate_function(items):
    result = 0
    for item in items:
        if item > 10:
            result += item
        elif item > 5:
            result += item * 2
        else:
            result += 1
    return result


def complex_function(data, config):
    results = []
    for item in data:
        if config.get('enabled'):
            if item.get('active'):
                if item.get('value', 0) > 100:
                    results.append(process_high(item))
                elif item.get('value', 0) > 50:
                    results.append(process_medium(item))
                else:
                    results.append(process_low(item))
            else:
                results.append(handle_inactive(item))
        else:
            results.append(handle_disabled(item))
    
    if config.get('validate'):
        for r in results:
            if not validate(r):
                raise ValueError("Invalid result")
    
    return sorted(results)


def very_complex(a, b, c, d, e):
    x = 1
    if a:
        if b:
            if c:
                if d:
                    if e:
                        x = 10
                    else:
                        x = 9
                else:
                    x = 8
            else:
                x = 7
        else:
            x = 6
    else:
        x = 5
    
    for i in range(10):
        for j in range(10):
            if i == j:
                continue
            x += 1
    
    try:
        result = risky_operation(x)
        if result and (result > 0 or x > 10):
            return process(result)
    except Exception as e:
        return handle_error(e)
    
    return x


class MyClass:
    def method_one(self):
        return 1
    
    def method_two(self, x):
        if x > 10:
            return x * 2
        return x
    
    def complex_method(self, data):
        results = []
        for item in data:
            if item.active:
                if item.value > 50:
                    results.append(self._process_high(item))
                elif item.value > 25:
                    results.append(self._process_med(item))
                else:
                    results.append(self._process_low(item))
        return results
"""

    options = {
        "max_cyclomatic": 10,
        "max_cognitive": 15,
        "max_nesting": 4,
        "max_function_length": 30,
        "max_hotspots": 5,
    }

    result = complexity_analyzer(test_code, options)
    import json

    print(json.dumps(result, indent=2))
