"""
Impact Analyzer - Predicts what breaks if code changes

Analyzes code changes to:
- Parse code changes and understand functions/classes
- Build call graphs (who calls whom)
- Find dependents (all code that uses the changed element)
- Assess risk based on dependents and usage patterns
- Suggest tests to run
"""

import re
import ast
import os
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class CodeElement:
    name: str
    type: str
    line_start: int
    line_end: int
    params: List[str] = field(default_factory=list)
    calls: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)


class CallGraphBuilder(ast.NodeVisitor):
    def __init__(self, source: str, filename: str = "<unknown>"):
        self.source = source
        self.filename = filename
        self.tree = ast.parse(source)
        self.elements: Dict[str, CodeElement] = {}
        self.current_class: Optional[str] = None
        self.call_graph: Dict[str, Set[str]] = defaultdict(set)
        self.imports: Set[str] = set()
        self.from_imports: Dict[str, Set[str]] = defaultdict(set)

    def build(self) -> Dict[str, CodeElement]:
        self._extract_imports()
        self.visit(self.tree)
        return self.elements

    def _extract_imports(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports.add(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    self.from_imports[node.module or ""].add(alias.asname or alias.name)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        element = self._create_element_from_function(node)
        self._add_element(node.name, element)
        self._process_function_body(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        element = self._create_element_from_function(node)
        self._add_element(node.name, element)
        self._process_function_body(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        old_class = self.current_class
        self.current_class = node.name
        element = CodeElement(
            name=node.name,
            type="class",
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
        )
        self._add_element(node.name, element)

        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_name = f"{node.name}.{item.name}"
                method_element = self._create_element_from_function(item)
                self._add_element(method_name, method_element)

        self.generic_visit(node)
        self.current_class = old_class

    def _create_element_from_function(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> CodeElement:
        params = []
        for arg in node.args.args:
            params.append(arg.arg)
        if node.args.vararg:
            params.append(f"*{node.args.vararg.arg}")
        if node.args.kwarg:
            params.append(f"**{node.args.kwarg.arg}")

        return CodeElement(
            name=node.name,
            type="function",
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            params=params,
            decorators=[self._get_decorator_name(d) for d in node.decorator_list],
        )

    def _add_element(self, name: str, element: CodeElement):
        self.elements[name] = element
        self.call_graph[name] = set()

    def _process_function_body(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ):
        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)
        element = self.elements.get(node.name)
        if element:
            element.calls = calls
            for call in calls:
                self.call_graph[node.name].add(call)

    def _get_decorator_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id
            elif isinstance(node.func, ast.Attribute):
                return node.func.attr
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ""


def parse_code(code: str, filename: str = "<unknown>") -> Dict[str, CodeElement]:
    try:
        builder = CallGraphBuilder(code, filename)
        return builder.build()
    except SyntaxError:
        return {}


def find_callers(elements: Dict[str, CodeElement], target: str) -> List[str]:
    callers = []
    target_base = target.split(".")[-1] if "." in target else target

    for name, element in elements.items():
        if target in element.calls or target_base in element.calls:
            if name != target:
                callers.append(name)

    return list(set(callers))


def find_indirect_callers(
    elements: Dict[str, CodeElement], target: str, max_depth: int = 5
) -> Dict[str, List[str]]:
    visited = set()
    call_chains = {}

    def find_recursive(current: str, path: List[str], depth: int):
        if depth > max_depth or current in visited:
            return

        visited.add(current)
        callers = find_callers(elements, current)

        for caller in callers:
            new_path = path + [caller]
            if caller not in call_chains:
                call_chains[caller] = new_path
            find_recursive(caller, new_path, depth + 1)

    find_recursive(target, [target], 0)
    return call_chains


def analyze_usage_patterns(
    target: str, elements: Dict[str, CodeElement]
) -> Dict[str, Any]:
    target_element = elements.get(target)
    if not target_element:
        return {"pattern": "unknown", "severity": "unknown", "details": []}

    details = []
    severity = "low"

    if target_element.decorators:
        details.append(f"Has decorators: {', '.join(target_element.decorators)}")
        severity = "high"

    if target_element.type == "class":
        details.append("Is a class - may affect all instances and subclasses")
        severity = "high"

    if target.startswith("_") and not target.startswith("__"):
        details.append("Private function - lower risk of external usage")
        severity = "low"
    elif target.startswith("__"):
        details.append("Name-mangled - lower risk of external usage")
        severity = "medium"
    else:
        details.append("Public API - high risk of external usage")
        severity = "high"

    if target_element.params:
        details.append(f"Parameters: {', '.join(target_element.params)}")

    return {
        "pattern": "public" if severity == "high" else "internal",
        "severity": severity,
        "details": details,
        "is_async": target_element.type == "function"
        and "async" in str(type(target_element)),
        "has_return": True,
    }


def calculate_risk_score(
    target: str,
    direct_callers: List[str],
    indirect_callers: Dict[str, List[str]],
    usage_pattern: Dict[str, Any],
    options: Dict[str, Any],
) -> Tuple[int, List[str]]:
    score = 0
    breaking_changes = []

    base_severity = {"high": 40, "medium": 20, "low": 5}
    score += base_severity.get(usage_pattern.get("severity", "low"), 10)

    direct_count = len(direct_callers)
    if direct_count > 10:
        score += 30
    elif direct_count > 5:
        score += 20
    elif direct_count > 0:
        score += direct_count * 3

    indirect_count = len(indirect_callers)
    if indirect_count > 20:
        score += 25
    elif indirect_count > 10:
        score += 15
    elif indirect_count > 0:
        score += indirect_count

    target_element_name = target.split(".")[-1] if "." in target else target
    for caller in direct_callers:
        if target not in breaking_changes:
            breaking_changes.append(f"Direct caller affected: {caller}")

    for indirect in indirect_callers:
        if len(breaking_changes) < 10:
            chain = " -> ".join(indirect_callers[indirect])
            breaking_changes.append(f"Indirect chain: {chain}")

    if usage_pattern.get("severity") == "high":
        breaking_changes.append(f"Public API change - may break external consumers")

    if usage_pattern.get("decorators"):
        for dec in usage_pattern["decorators"]:
            if dec in ["property", "classmethod", "staticmethod"]:
                breaking_changes.append(
                    f"Decorator '{dec}' change affects class behavior"
                )

    if options.get("breaking_changes_only", False):
        breaking_changes = [
            bc
            for bc in breaking_changes
            if "affected" in bc.lower() or "public" in bc.lower()
        ]

    return min(100, score), breaking_changes[:20]


def find_affected_modules(
    target: str,
    direct_callers: List[str],
    indirect_callers: Dict[str, List[str]],
    code: str,
    options: Dict[str, Any],
) -> List[str]:
    modules = set()
    modules.add("<local>")

    if not options.get("include_external", False):
        return list(modules)

    all_callers = direct_callers + list(indirect_callers.keys())
    for caller in all_callers:
        if "." in caller:
            module = caller.rsplit(".", 1)[0]
            modules.add(module)

    return sorted(list(modules))


def suggest_tests(
    target: str,
    direct_callers: List[str],
    indirect_callers: Dict[str, List[str]],
    options: Dict[str, Any],
) -> List[Dict[str, Any]]:
    recommended = []

    test_patterns = {
        "test_": "Unit test file",
        "test_": "Integration test file",
        "test_": "E2E test file",
    }

    for caller in direct_callers[:5]:
        test_name = f"test_{caller}"
        if "." in caller:
            method_name = caller.split(".")[-1]
            test_name = f"test_{caller.replace('.', '_')}"

        recommended.append(
            {"name": test_name, "type": "unit", "target": caller, "priority": "high"}
        )

    for caller in list(indirect_callers.keys())[:3]:
        test_name = f"test_{caller.replace('.', '_')}"
        recommended.append(
            {
                "name": test_name,
                "type": "integration",
                "target": caller,
                "priority": "medium",
            }
        )

    recommended.append(
        {
            "name": f"test_{target.replace('.', '_')}_signature",
            "type": "regression",
            "target": target,
            "priority": "high",
            "description": "Verify function/class signature compatibility",
        }
    )

    return recommended


def impact_analyzer(code: str, change_target: str, options: dict = None) -> dict:
    if options is None:
        options = {}

    if not code:
        return {"status": "error", "error": "No code provided"}

    if not change_target:
        return {"status": "error", "error": "No change target provided"}

    max_depth = options.get("max_depth", 5)
    include_external = options.get("include_external", False)

    elements = parse_code(code)

    if not elements:
        return {"status": "error", "error": "Could not parse code - syntax error"}

    if change_target not in elements:
        similar = [
            name for name in elements.keys() if change_target.lower() in name.lower()
        ]
        return {
            "status": "error",
            "error": f"Target '{change_target}' not found in code",
            "suggestions": similar[:5] if similar else [],
        }

    direct_callers = find_callers(elements, change_target)
    indirect_callers = find_indirect_callers(elements, change_target, max_depth)
    usage_pattern = analyze_usage_patterns(change_target, elements)
    risk_score, breaking_changes = calculate_risk_score(
        change_target, direct_callers, indirect_callers, usage_pattern, options
    )
    affected_modules = find_affected_modules(
        change_target, direct_callers, indirect_callers, code, options
    )
    recommended_tests = suggest_tests(
        change_target, direct_callers, indirect_callers, options
    )

    return {
        "status": "success",
        "target": change_target,
        "target_type": elements[change_target].type,
        "target_details": {
            "line_start": elements[change_target].line_start,
            "line_end": elements[change_target].line_end,
            "params": elements[change_target].params,
            "decorators": elements[change_target].decorators,
        },
        "callers": direct_callers,
        "indirect_callers": {k: v for k, v in indirect_callers.items()},
        "risk_score": risk_score,
        "risk_level": "high"
        if risk_score >= 70
        else "medium"
        if risk_score >= 40
        else "low",
        "affected_modules": affected_modules,
        "recommended_tests": recommended_tests,
        "breaking_changes": breaking_changes,
        "usage_pattern": usage_pattern,
        "analysis_options": options,
    }


def invoke(payload: dict) -> dict:
    action = payload.get("action", "analyze")

    if action == "analyze":
        code = payload.get("code", "")
        change_target = payload.get("change_target", "")
        options = payload.get("options", {})

        result = impact_analyzer(code, change_target, options)
        return {"result": result}

    elif action == "batch":
        results = []
        analyses = payload.get("analyses", [])

        for analysis in analyses:
            code = analysis.get("code", "")
            change_target = analysis.get("change_target", "")
            options = analysis.get("options", {})
            results.append(impact_analyzer(code, change_target, options))

        return {"result": results}

    elif action == "full_analysis":
        target = payload.get("change_target", "")
        base_path = payload.get("base_path", ".")
        options = payload.get("options", {})

        all_results = {"status": "success", "target": target, "file_analyses": []}

        return all_results

    else:
        return {"status": "error", "error": f"Unknown action: {action}"}


def register_skill():
    return {
        "name": "impact-analyzer",
        "description": "Predicts what breaks if code changes - analyzes call graphs, finds dependents, assesses risk, and suggests tests",
        "version": "1.0.0",
        "domain": "CODEBASE_INTELLIGENCE",
        "capabilities": [
            "parse_code",
            "build_call_graph",
            "find_dependents",
            "assess_risk",
            "suggest_tests",
        ],
        "parameters": {
            "code": "Python source code string",
            "change_target": "Function/class name that will change",
            "options": {
                "include_external": "Include external module analysis",
                "max_depth": "Maximum call chain depth (default: 5)",
                "breaking_changes_only": "Only report breaking changes",
            },
        },
        "returns": {
            "status": "success or error",
            "target": "The analyzed element",
            "callers": "Direct callers",
            "indirect_callers": "Callers through call chain",
            "risk_score": "0-100 impact score",
            "affected_modules": "List of affected modules",
            "recommended_tests": "Tests to run",
            "breaking_changes": "Potential breaking changes",
        },
    }


if __name__ == "__main__":
    sample_code = """
class DataProcessor:
    def __init__(self):
        self.data = []
    
    def process(self, items):
        return [self.transform(i) for i in items]
    
    def transform(self, item):
        return item.upper() if isinstance(item, str) else item
    
    def save(self):
        return self.data

def main():
    processor = DataProcessor()
    result = processor.process(["hello", "world"])
    processor.save()

class Validator:
    def validate(self, data):
        return processor.transform(data)
"""

    result = impact_analyzer(sample_code, "DataProcessor.transform")
    import json

    print(json.dumps(result, indent=2))
