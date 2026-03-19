"""
Dependency Analyzer Skill

This module provides skills for analyzing Python import dependencies:
- Build import graph between modules
- Detect circular dependencies
- Analyze dependency direction (afferent vs efferent)
- Calculate instability metric (Ce/Ca+Ce)
- Identify problematic dependencies (tight coupling, god modules)
"""

import ast
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class Import:
    """Represents an import statement"""

    module: str
    name: str
    alias: Optional[str] = None
    line: int = 0
    is_from: bool = False
    is_relative: bool = False


@dataclass
class ModuleInfo:
    """Information about a module"""

    path: str
    name: str
    imports: List[Import] = field(default_factory=list)
    imported_by: List[str] = field(default_factory=list)
    afferent_coupling: int = 0
    efferent_coupling: int = 0
    instability: float = 0.0


class ImportGraphBuilder(ast.NodeVisitor):
    """AST visitor to build import graph"""

    def __init__(self, source_lines: List[str], module_name: str = "__main__"):
        self.source_lines = source_lines
        self.module_name = module_name
        self.imports: List[Import] = []
        self.current_line = 0

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(
                Import(
                    module=alias.name,
                    name=alias.name.split(".")[0],
                    alias=alias.asname,
                    line=node.lineno,
                    is_from=False,
                    is_relative=any(
                        part.startswith("_") for part in alias.name.split(".")
                    ),
                )
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        is_relative = node.level > 0

        for alias in node.names:
            if alias.name == "*":
                continue

            imported_name = alias.name
            if is_relative:
                module = "." * node.level + module

            self.imports.append(
                Import(
                    module=module,
                    name=imported_name,
                    alias=alias.asname,
                    line=node.lineno,
                    is_from=True,
                    is_relative=is_relative,
                )
            )
        self.generic_visit(node)


def parse_imports(code: str, module_name: str = "__main__") -> List[Import]:
    """Parse imports from Python code"""
    try:
        tree = ast.parse(code)
        source_lines = code.splitlines()
        visitor = ImportGraphBuilder(source_lines, module_name)
        visitor.visit(tree)
        return visitor.imports
    except SyntaxError:
        return []


def build_import_graph(files: Dict[str, str]) -> Dict[str, ModuleInfo]:
    """Build import graph from multiple files"""
    graph: Dict[str, ModuleInfo] = {}

    for file_path, code in files.items():
        module_name = Path(file_path).stem
        if module_name.startswith("__"):
            continue

        imports = parse_imports(code, module_name)

        graph[module_name] = ModuleInfo(
            path=file_path, name=module_name, imports=imports
        )

    for module_name, info in graph.items():
        for imp in info.imports:
            target_module = imp.name.split(".")[0]
            if target_module in graph and target_module != module_name:
                graph[target_module].imported_by.append(module_name)

    for module_name, info in graph.items():
        unique_imports = set()
        for imp in info.imports:
            target = imp.name.split(".")[0]
            if target in graph and target != module_name:
                unique_imports.add(target)

        info.efferent_coupling = len(unique_imports)

        unique_imported_by = set(info.imported_by)
        info.afferent_coupling = len(unique_imported_by)

        total = info.afferent_coupling + info.efferent_coupling
        if total > 0:
            info.instability = info.efferent_coupling / total
        else:
            info.instability = 0.0

    return graph


def detect_circular_dependencies(graph: Dict[str, ModuleInfo]) -> List[List[str]]:
    """Detect circular dependencies using DFS"""
    cycles: List[List[str]] = []
    visited: Set[str] = set()
    rec_stack: Set[str] = set()
    path: List[str] = []

    def dfs(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        if node in graph:
            for imp in graph[node].imports:
                target = imp.name.split(".")[0]
                if target not in graph:
                    continue

                if target not in visited:
                    if dfs(target):
                        return True
                elif target in rec_stack:
                    cycle_start = path.index(target)
                    cycle = path[cycle_start:] + [target]
                    if cycle not in cycles:
                        cycles.append(cycle)
                    return True

        path.pop()
        rec_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            dfs(node)

    return cycles


def analyze_dependency_direction(
    graph: Dict[str, ModuleInfo],
) -> Dict[str, Dict[str, Any]]:
    """Analyze afferent (incoming) vs efferent (outgoing) dependencies"""
    analysis = {}

    for module_name, info in graph.items():
        afferent = [
            m
            for m in graph
            if module_name in [i.name.split(".")[0] for i in graph[m].imports]
            and m != module_name
        ]
        efferent = [
            i.name.split(".")[0]
            for i in info.imports
            if i.name.split(".")[0] in graph and i.name.split(".")[0] != module_name
        ]

        analysis[module_name] = {
            "afferent": list(set(afferent)),
            "efferent": list(set(efferent)),
            "afferent_count": len(set(afferent)),
            "efferent_count": len(set(efferent)),
            "stable": info.afferent_coupling > info.efferent_coupling,
            "unstable": info.efferent_coupling > info.afferent_coupling,
            "abstract": info.afferent_coupling == 0 and info.efferent_coupling > 0,
        }

    return analysis


def calculate_instability(graph: Dict[str, ModuleInfo]) -> Dict[str, float]:
    """Calculate instability for each module: Ce / (Ca + Ce)"""
    instability = {}

    for module_name, info in graph.items():
        instability[module_name] = info.instability

    return instability


def identify_problematic_dependencies(
    graph: Dict[str, ModuleInfo],
) -> Dict[str, List[Dict[str, Any]]]:
    """Identify problematic coupling patterns"""
    issues = {
        "god_modules": [],
        "tight_coupling": [],
        "hub_modules": [],
        "instable_modules": [],
        "orphan_modules": [],
    }

    avg_efferent = (
        sum(m.efferent_coupling for m in graph.values()) / len(graph) if graph else 0
    )
    avg_afferent = (
        sum(m.afferent_coupling for m in graph.values()) / len(graph) if graph else 0
    )

    for module_name, info in graph.items():
        if info.efferent_coupling > avg_efferent * 3 and info.efferent_coupling > 5:
            issues["god_modules"].append(
                {
                    "module": module_name,
                    "efferent_coupling": info.efferent_coupling,
                    "reason": f"Excessive outgoing dependencies ({info.efferent_coupling} > {avg_efferent * 3:.1f} avg)",
                }
            )

        if info.afferent_coupling > avg_afferent * 3 and info.afferent_coupling > 5:
            issues["hub_modules"].append(
                {
                    "module": module_name,
                    "afferent_coupling": info.afferent_coupling,
                    "reason": f"Excessive incoming dependencies ({info.afferent_coupling} > {avg_afferent * 3:.1f} avg)",
                }
            )

        if info.instability > 0.8:
            issues["instable_modules"].append(
                {
                    "module": module_name,
                    "instability": info.instability,
                    "reason": f"High instability ({info.instability:.2f} > 0.8)",
                }
            )

        if info.afferent_coupling == 0 and info.efferent_coupling > 0:
            issues["orphan_modules"].append(
                {
                    "module": module_name,
                    "reason": "No other modules depend on this module",
                }
            )

    return issues


def generate_recommendations(
    graph: Dict[str, ModuleInfo],
    circular_deps: List[List[str]],
    issues: Dict[str, List[Dict[str, Any]]],
) -> List[str]:
    """Generate recommendations for improving dependency structure"""
    recommendations = []

    for cycle in circular_deps:
        recommendations.append(f"Break circular dependency: {' -> '.join(cycle)}")

    for god in issues.get("god_modules", []):
        recommendations.append(
            f"Refactor '{god['module']}' - consider splitting to reduce outgoing dependencies"
        )

    for hub in issues.get("hub_modules", []):
        recommendations.append(
            f"Review '{hub['module']}' - consider extracting interface to reduce incoming dependencies"
        )

    for instable in issues.get("instable_modules", []):
        recommendations.append(
            f"Make '{instable['module']}' more stable - reduce efferent dependencies"
        )

    for orphan in issues.get("orphan_modules", []):
        recommendations.append(
            f"Review '{orphan['module']}' - consider if it should be part of the codebase"
        )

    unstable_modules = [m for m, i in graph.items() if i.instability > 0.5]
    if unstable_modules:
        recommendations.append(
            f"Consider adding abstractions for: {', '.join(unstable_modules)}"
        )

    return recommendations


def read_file_or_code(code: str) -> Tuple[Optional[Dict[str, str]], str]:
    """Read code from file path or use directly as code"""
    if isinstance(code, dict):
        return code, "multi_file"

    if os.path.isfile(code):
        try:
            with open(code, encoding="utf-8") as f:
                return {code: f.read()}, os.path.basename(code)
        except Exception:
            return None, "file_error"

    if "\n" in code or "import" in code:
        return {"__main__.py": code}, "__main__"

    return None, "invalid_input"


def dependency_analyzer(code: str, options: dict = None) -> dict:
    """
    Analyze import dependencies in Python code

    Args:
        code: Python source code or file path
        options: Analysis options:
            - detect_circular: Detect circular dependencies (default: True)
            - analyze_coupling: Analyze afferent/efferent coupling (default: True)
            - calculate_instability: Calculate instability metric (default: True)
            - identify_issues: Identify problematic patterns (default: True)

    Returns:
        dict with:
            - status: "success" or "error"
            - imports: List of imports with source and targets
            - circular_dependencies: List of circular dependency chains
            - instability_score: Module instability metric
            - coupling_issues: Problematic coupling patterns
            - recommendations: Suggestions for improving dependency structure
    """
    if options is None:
        options = {}

    result = {
        "status": "success",
        "imports": [],
        "circular_dependencies": [],
        "instability_score": {},
        "coupling_issues": {},
        "recommendations": [],
        "module_analysis": {},
    }

    detect_circular = options.get("detect_circular", True)
    analyze_coupling = options.get("analyze_coupling", True)
    do_calc_instability = options.get("calculate_instability", True)
    identify_issues = options.get("identify_issues", True)

    files, module_name = read_file_or_code(code)

    if files is None:
        result["status"] = "error"
        result["error"] = f"Could not read code from: {module_name}"
        return result

    is_single_module = len(files) == 1 and any("__main__" in k for k in files)

    if is_single_module:
        imports = parse_imports(code, module_name)
        imports_data = []
        for imp in imports:
            imports_data.append(
                {
                    "module": imp.module,
                    "name": imp.name,
                    "alias": imp.alias,
                    "line": imp.line,
                    "is_from": imp.is_from,
                    "is_relative": imp.is_relative,
                }
            )
        result["imports"] = [{"source": module_name, "imports": imports_data}]
        result["recommendations"] = [
            "For full dependency analysis, provide multiple Python files as a dictionary",
            f"Found {len(imports)} imports in single module analysis",
        ]

        external_imports = [
            i
            for i in imports
            if not i.is_relative
            and i.name
            not in (
                "os",
                "sys",
                "collections",
                "typing",
                "dataclasses",
                "pathlib",
                "re",
                "ast",
                "json",
                "hashlib",
                "defaultdict",
            )
        ]
        if external_imports:
            result["recommendations"].append(
                f"External dependencies detected: {[i.name for i in external_imports]}"
            )

        return result

    graph = build_import_graph(files)

    for mod_name, info in graph.items():
        imports_data = []
        for imp in info.imports:
            imports_data.append(
                {
                    "module": imp.module,
                    "name": imp.name,
                    "alias": imp.alias,
                    "line": imp.line,
                    "is_from": imp.is_from,
                    "is_relative": imp.is_relative,
                }
            )
        result["imports"].append({"source": mod_name, "imports": imports_data})

    if detect_circular:
        result["circular_dependencies"] = detect_circular_dependencies(graph)

    if analyze_coupling:
        result["module_analysis"] = analyze_dependency_direction(graph)

    if do_calc_instability:
        result["instability_score"] = calculate_instability(graph)

    if identify_issues:
        result["coupling_issues"] = identify_problematic_dependencies(graph)

    result["recommendations"] = generate_recommendations(
        graph, result["circular_dependencies"], result["coupling_issues"]
    )

    return result


def invoke(payload: dict) -> dict:
    """
    Invoke the dependency analyzer skill

    Args:
        payload: Dictionary with:
            - code: Python source code or file path (required)
            - options: Analysis options (optional)

    Returns:
        dict with analysis result
    """
    code = payload.get("code")
    options = payload.get("options", {})

    if not code:
        return {"result": {"status": "error", "message": "No code provided"}}

    result = dependency_analyzer(code, options)
    return {"result": result}


def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "dependency-analyzer",
        "description": "Analyze Python import dependencies - build import graph, detect circular dependencies, calculate instability metrics, and identify problematic coupling patterns",
        "version": "1.0.0",
        "domain": "CODEBASE_INTELLIGENCE",
    }


if __name__ == "__main__":
    test_code = """
import os
import sys
from collections import defaultdict
from typing import Dict, List

class ModuleA:
    def process(self):
        return "processed"

class ModuleB:
    def __init__(self):
        self.a = ModuleA()
    
    def run(self):
        return self.a.process()

class ModuleC:
    def __init__(self):
        self.b = ModuleB()
    
    def execute(self):
        return self.b.run()
"""

    options = {
        "detect_circular": True,
        "analyze_coupling": True,
        "calculate_instability": True,
        "identify_issues": True,
    }

    result = dependency_analyzer(test_code, options)
    print(f"Status: {result['status']}")
    print(f"Imports found: {len(result['imports'])}")
    print(f"Circular dependencies: {result['circular_dependencies']}")
    print(f"Instability scores: {result['instability_score']}")
    print(f"Coupling issues: {result['coupling_issues']}")
    print(f"Recommendations: {result['recommendations']}")
