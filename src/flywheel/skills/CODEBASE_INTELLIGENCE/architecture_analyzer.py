"""
Architecture Analyzer Skill

This module provides skills for analyzing Python code architecture:
- Extract module structure and hierarchy
- Map import dependencies
- Identify design patterns
- Analyze module coupling
- Generate improvement recommendations
"""

import ast
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime


@dataclass
class ModuleInfo:
    """Information about a Python module"""

    name: str
    path: str
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    imported_by: List[str] = field(default_factory=list)
    docstring: str | None = None
    line_count: int = 0


PATTERNS = {
    "Singleton": {
        "indicators": [
            r"_instance\s*=\s*None",
            r"_instance\s*=\s*None\s*,\s*None",
            r"if\s+\w+\s+is\s+None:",
            r"__new__\s*\(",
        ],
        "class_indicators": ["_instance", "__new__"],
    },
    "Factory": {
        "indicators": [
            r"def\s+create\w+\s*\(",
            r"def\s+make\w+\s*\(",
            r"def\s+build\w+\s*\(",
            r"Factory",
            r"def\s+\w*factory\w*\s*\(",
        ],
        "class_indicators": ["Factory", "create_", "make_"],
    },
    "Adapter": {
        "indicators": [
            r"class\s+\w*Adapter\w*",
            r"def\s+adapt\s*\(",
            r"def\s+convert\s*\(",
            r"wrap",
            r"wrapper",
        ],
        "class_indicators": ["Adapter", "Wrapper"],
    },
    "Observer": {
        "indicators": [
            r"def\s+notify\s*\(",
            r"def\s+subscribe\s*\(",
            r"def\s+add_observer\s*\(",
            r"def\s+register\s*\(",
            r"_observers",
            r"_listeners",
        ],
        "class_indicators": ["Observer", "_observers", "_listeners"],
    },
    "Strategy": {
        "indicators": [
            r"def\s+execute\s*\(",
            r"def\s+run\s*\(",
            r"Strategy",
            r"def\s+set_strategy\s*\(",
            r"def\s+use_strategy\s*\(",
        ],
        "class_indicators": ["Strategy", "execute", "set_strategy"],
    },
    "Decorator": {
        "indicators": [
            r"@staticmethod",
            r"@classmethod",
            r"@property",
            r"def\s+\w+\s*\(\s*self",
            r"wrappee",
            r"decorator",
        ],
        "class_indicators": ["decorator", "@"],
    },
    "Facade": {
        "indicators": [
            r"class\s+\w*Facade\w*",
            r"def\s+init\s*\(self\):\s*\n\s*self\._",
            r"def\s+\w+\s*\([^)]*\):\s*\n\s*[^ ]+self\.\w+\.\w+",
        ],
        "class_indicators": ["Facade"],
    },
    "Command": {
        "indicators": [
            r"class\s+\w*Command\w*",
            r"def\s+execute\s*\(",
            r"def\s+undo\s*\(",
            r"def\s+redo\s*\(",
        ],
        "class_indicators": ["Command", "execute", "undo"],
    },
    "Builder": {
        "indicators": [
            r"def\s+set\w+\s*\(",
            r"def\s+with\w+\s*\(",
            r"def\s+build\s*\(\s*\)",
            r"Builder",
        ],
        "class_indicators": ["Builder", "set_", "with_", "build"],
    },
    "Repository": {
        "indicators": [
            r"class\s+\w*Repository\w*",
            r"def\s+get\s*\(",
            r"def\s+add\s*\(",
            r"def\s+delete\s*\(",
            r"def\s+find\s*\(",
        ],
        "class_indicators": ["Repository", "get", "add", "find"],
    },
}


def parse_python_file(file_path: str) -> ModuleInfo | None:
    """Parse a Python file and extract module information"""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=file_path)

        module_name = os.path.splitext(os.path.basename(file_path))[0]

        module_info = ModuleInfo(
            name=module_name,
            path=file_path,
            line_count=len(content.splitlines()),
        )

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                module_info.classes.append(node.name)
                if ast.get_docstring(node):
                    module_info.docstring = ast.get_docstring(node)
            elif isinstance(node, ast.FunctionDef):
                module_info.functions.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module_info.imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_info.imports.append(node.module)

        return module_info

    except (SyntaxError, FileNotFoundError, UnicodeDecodeError):
        return None


def extract_module_structure(code: str, options: dict) -> Dict[str, Any]:
    """Extract module structure from Python code or file path"""
    modules = []
    root_path = None

    if os.path.isfile(code):
        if code.endswith(".py"):
            module = parse_python_file(code)
            if module:
                modules.append(
                    {
                        "name": module.name,
                        "path": module.path,
                        "classes": module.classes,
                        "functions": module.functions,
                        "line_count": module.line_count,
                        "docstring": module.docstring,
                    }
                )
                root_path = os.path.dirname(code)
        return {"modules": modules, "root_path": root_path}

    if os.path.isdir(code):
        root_path = code
        for root, dirs, files in os.walk(code):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]

            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    file_path = os.path.join(root, file)
                    module = parse_python_file(file_path)

                    if module:
                        rel_path = os.path.relpath(file_path, code)
                        modules.append(
                            {
                                "name": module.name,
                                "path": rel_path,
                                "classes": module.classes,
                                "functions": module.functions,
                                "imports": module.imports,
                                "line_count": module.line_count,
                                "docstring": module.docstring,
                            }
                        )

    return {"modules": modules, "root_path": root_path}


def build_dependency_graph(modules: List[Dict]) -> Dict[str, List[str]]:
    """Build import dependency graph"""
    dependencies = defaultdict(list)
    module_names = {m["name"] for m in modules}
    module_paths = {m["path"] for m in modules}

    for module in modules:
        module_name = module["name"]

        for imp in module.get("imports", []):
            imp_base = imp.split(".")[0]

            if imp_base in module_names:
                dependencies[module_name].append(imp_base)
            elif any(
                imp.startswith(p.replace(".py", "").replace("\\", "/").split("/")[-1])
                for p in module_paths
            ):
                for p in module_paths:
                    if imp.startswith(
                        p.replace(".py", "").replace("\\", "/").split("/")[-1]
                    ):
                        target = p.replace(".py", "").split("/")[-1]
                        if target in module_names:
                            dependencies[module_name].append(target)

    return dict(dependencies)


def detect_patterns(modules: List[Dict]) -> List[Dict[str, Any]]:
    """Detect design patterns in the code"""
    detected_patterns = []

    for module in modules:
        module_path = module.get("path", "")

        if not os.path.isabs(module_path) or not os.path.exists(module_path):
            continue

        try:
            with open(module_path, encoding="utf-8") as f:
                content = f.read()

            for pattern_name, pattern_info in PATTERNS.items():
                matches = 0
                total_indicators = len(pattern_info["indicators"])

                for indicator in pattern_info["indicators"]:
                    if re.search(indicator, content, re.IGNORECASE):
                        matches += 1

                confidence = (
                    (matches / total_indicators) * 100 if total_indicators > 0 else 0
                )

                if confidence >= 30:
                    detected_patterns.append(
                        {
                            "pattern": pattern_name,
                            "module": module["name"],
                            "confidence": round(confidence, 2),
                            "indicators_found": matches,
                        }
                    )

        except (FileNotFoundError, UnicodeDecodeError):
            continue

    detected_patterns.sort(key=lambda x: x["confidence"], reverse=True)
    return detected_patterns


def analyze_coupling(
    modules: List[Dict], dependencies: Dict[str, List[str]]
) -> Dict[str, Any]:
    """Analyze coupling between modules"""
    if not modules:
        return {"metrics": {}, "high_coupling": [], "low_coupling": []}

    module_names = [m["name"] for m in modules]

    afferent_coupling = defaultdict(int)
    efferent_coupling = defaultdict(int)

    for source, targets in dependencies.items():
        if source in module_names:
            efferent_coupling[source] = len(targets)

            for target in targets:
                if target in module_names:
                    afferent_coupling[target] += 1

    instability = {}
    for module in module_names:
        ca = afferent_coupling.get(module, 0)
        ce = efferent_coupling.get(module, 0)

        if ca + ce > 0:
            instability[module] = round(ce / (ca + ce), 3)
        else:
            instability[module] = 0.0

    high_coupling = sorted(
        [
            {
                "module": m,
                "efferent": efferent_coupling.get(m, 0),
                "afferent": afferent_coupling.get(m, 0),
            }
            for m in module_names
            if efferent_coupling.get(m, 0) > 3
        ],
        key=lambda x: x["efferent"],
        reverse=True,
    )

    low_coupling = sorted(
        [
            {"module": m, "instability": instability.get(m, 0)}
            for m in module_names
            if instability.get(m, 0) < 0.3 and efferent_coupling.get(m, 0) > 0
        ],
        key=lambda x: x["instability"],
    )

    return {
        "metrics": {
            "afferent_coupling": dict(afferent_coupling),
            "efferent_coupling": dict(efferent_coupling),
            "instability": instability,
            "total_dependencies": sum(len(v) for v in dependencies.values()),
        },
        "high_coupling": high_coupling,
        "low_coupling": low_coupling,
    }


def generate_recommendations(
    modules: List[Dict],
    dependencies: Dict[str, List[str]],
    coupling: Dict[str, Any],
    patterns: List[Dict[str, Any]],
) -> List[Dict[str, str]]:
    """Generate architecture improvement recommendations"""
    recommendations = []

    high_coupling = coupling.get("high_coupling", [])
    if high_coupling:
        recommendations.append(
            {
                "type": "HIGH_COUPLING",
                "priority": "HIGH",
                "message": f"Modules with high coupling detected: {', '.join([m['module'] for m in high_coupling[:3]])}. Consider extracting interfaces or using dependency injection.",
            }
        )

    low_coupling = coupling.get("low_coupling", [])
    if low_coupling:
        recommendations.append(
            {
                "type": "GOOD_DESIGN",
                "priority": "INFO",
                "message": f"Well-decoupled modules found: {', '.join([m['module'] for m in low_coupling[:3]])}. These modules follow good isolation principles.",
            }
        )

    if not patterns:
        recommendations.append(
            {
                "type": "NO_PATTERNS",
                "priority": "MEDIUM",
                "message": "No common design patterns detected. Consider implementing standard patterns like Factory, Repository, or Strategy for better maintainability.",
            }
        )

    large_modules = [m for m in modules if m.get("line_count", 0) > 500]
    if large_modules:
        recommendations.append(
            {
                "type": "LARGE_MODULES",
                "priority": "MEDIUM",
                "message": f"Large modules detected (>500 lines): {', '.join([m['name'] for m in large_modules[:3]])}. Consider splitting into smaller, focused modules.",
            }
        )

    modules_without_tests = [
        m for m in modules if not any(x in m.get("path", "") for x in ["test", "tests"])
    ]
    if len(modules_without_tests) > len(modules) * 0.7 and len(modules) > 3:
        recommendations.append(
            {
                "type": "TEST_COVERAGE",
                "priority": "MEDIUM",
                "message": f"{len(modules_without_tests)} modules may lack tests. Consider adding unit tests to improve maintainability.",
            }
        )

    circular_deps = detect_circular_dependencies(dependencies)
    if circular_deps:
        recommendations.append(
            {
                "type": "CIRCULAR_DEPENDENCIES",
                "priority": "HIGH",
                "message": f"Circular dependencies detected: {circular_deps}. Break cycles by introducing abstraction layers.",
            }
        )

    if len(modules) > 20:
        recommendations.append(
            {
                "type": "MODULARIZATION",
                "priority": "INFO",
                "message": f"Large codebase with {len(modules)} modules. Consider organizing into packages with clear separation of concerns.",
            }
        )

    return recommendations


def detect_circular_dependencies(dependencies: Dict[str, List[str]]) -> List[List[str]]:
    """Detect circular dependencies in the dependency graph"""
    circular = []
    visited = set()
    rec_stack = set()

    def has_cycle(node: str, path: List[str]) -> List[str] | None:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in dependencies.get(node, []):
            if neighbor not in visited:
                cycle = has_cycle(neighbor, path + [neighbor])
                if cycle:
                    return cycle
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor) if neighbor in path else 0
                return path[cycle_start:] + [neighbor]

        rec_stack.remove(node)
        return None

    for node in dependencies:
        if node not in visited:
            cycle = has_cycle(node, [node])
            if cycle:
                circular.append(cycle)
                visited.add(node)

    return circular[:5]


def architecture_analyzer(code: str, options: dict = None) -> dict:
    """
    Analyze Python code architecture.

    Args:
        code: Python source code or file/directory path
        options: Analysis options (include_tests, max_depth, etc.)

    Returns:
        Dictionary with analysis results
    """
    options = options or {}

    try:
        include_tests = options.get("include_tests", True)
        max_depth = options.get("max_depth", 10)

        structure = extract_module_structure(code, options)
        modules = structure["modules"]

        if not include_tests:
            modules = [m for m in modules if "test" not in m.get("path", "").lower()]

        if max_depth and structure["root_path"]:
            modules = modules[: max_depth * 10]

        dependencies = build_dependency_graph(modules)

        patterns = detect_patterns(modules)

        coupling = analyze_coupling(modules, dependencies)

        recommendations = generate_recommendations(
            modules, dependencies, coupling, patterns
        )

        return {
            "status": "success",
            "modules": modules,
            "dependencies": dependencies,
            "patterns": patterns,
            "coupling_analysis": coupling,
            "recommendations": recommendations,
            "summary": {
                "total_modules": len(modules),
                "total_dependencies": sum(len(v) for v in dependencies.values()),
                "patterns_detected": len(patterns),
                "recommendations_count": len(recommendations),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze architecture",
        }


async def invoke(payload: dict) -> dict:
    """Main entry point for MCP skill invocation"""
    code = payload.get("code", "")
    options = payload.get("options", {})

    if not code:
        return{
        "result": {"status": "error", "message": "No code or path provided"},
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
    result = architecture_analyzer(code, options)
    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata for MCP registration"""

if __name__ == "__main__":
    return {
            "name": "architecture-analyzer",
            "description": "Analyze Python code architecture - extract module structure, map dependencies, identify patterns, analyze coupling, and generate improvement recommendations",
            "version": "1.0.0",
            "domain": "CODEBASE_INTELLIGENCE",
        }