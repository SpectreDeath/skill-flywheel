"""
Refactoring Recommender Skill

This module provides skills for analyzing Python code and suggesting refactorings:
- Detect code smells (long functions, large classes, duplicate code)
- Analyze complexity (cyclomatic complexity, nesting depth)
- Identify SOLID principle violations
- Generate prioritized refactoring recommendations
- Estimate implementation effort
"""

import ast
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Set


@dataclass
class CodeSmell:
    """Detected code smell"""

    type: str
    severity: str
    location: str
    line_start: int
    line_end: int
    description: str
    metric_value: Any = None
    threshold: Any = None


@dataclass
class ComplexityIssue:
    """Function or class exceeding complexity thresholds"""

    name: str
    type: str
    line_start: int
    line_end: int
    complexity_score: int
    threshold: int
    nesting_depth: int = 0
    line_count: int = 0


@dataclass
class SOLIDViolation:
    """SOLID principle violation"""

    principle: str
    class_name: str
    method_name: str | None
    line: int
    description: str
    severity: str


@dataclass
class Recommendation:
    """Refactoring recommendation"""

    title: str
    description: str
    priority: int
    confidence: float
    effort: str
    location: str
    line_start: int
    line_end: int
    smell_type: str | None = None
    principle_violated: str | None = None


DEFAULT_OPTIONS = {
    "max_function_lines": 50,
    "max_class_lines": 300,
    "max_function_params": 5,
    "max_nesting_depth": 4,
    "max_cyclomatic_complexity": 10,
    "check_solid": True,
    "check_duplicates": True,
    "min_duplicate_length": 5,
    "threshold_complexity": 10,
}


def calculate_cyclomatic_complexity(node: ast.AST) -> int:
    """Calculate cyclomatic complexity for a function"""
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += len(child.values) - 1
    return complexity


def calculate_nesting_depth(node: ast.AST, current_depth: int = 0) -> int:
    """Calculate maximum nesting depth"""
    max_depth = current_depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
            child_depth = calculate_nesting_depth(child, current_depth + 1)
            max_depth = max(max_depth, child_depth)
        else:
            child_depth = calculate_nesting_depth(child, current_depth)
            max_depth = max(max_depth, child_depth)
    return max_depth


def get_function_lines(node: ast.FunctionDef) -> int:
    """Get the number of lines in a function"""
    if hasattr(node, "end_lineno") and node.end_lineno and node.lineno:
        return node.end_lineno - node.lineno + 1
    return 0


def get_class_lines(node: ast.ClassDef) -> int:
    """Get the number of lines in a class"""
    if hasattr(node, "end_lineno") and node.end_lineno and node.lineno:
        return node.end_lineno - node.lineno + 1
    return 0


def detect_long_functions(tree: ast.AST, threshold: int) -> List[CodeSmell]:
    """Detect functions that exceed line count threshold"""
    smells = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            line_count = get_function_lines(node)
            if line_count > threshold:
                smells.append(
                    CodeSmell(
                        type="Long Function",
                        severity="high" if line_count > threshold * 2 else "medium",
                        location=f"{node.name}()",
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        description=f"Function has {line_count} lines (threshold: {threshold})",
                        metric_value=line_count,
                        threshold=threshold,
                    )
                )
    return smells


def detect_long_classes(tree: ast.AST, threshold: int) -> List[CodeSmell]:
    """Detect classes that exceed line count threshold"""
    smells = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            line_count = get_class_lines(node)
            if line_count > threshold:
                smells.append(
                    CodeSmell(
                        type="Large Class",
                        severity="high" if line_count > threshold * 2 else "medium",
                        location=node.name,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        description=f"Class has {line_count} lines (threshold: {threshold})",
                        metric_value=line_count,
                        threshold=threshold,
                    )
                )
    return smells


def detect_too_many_parameters(tree: ast.AST, threshold: int) -> List[CodeSmell]:
    """Detect functions with too many parameters"""
    smells = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            param_count = len(node.args.args)
            if param_count > threshold:
                smells.append(
                    CodeSmell(
                        type="Too Many Parameters",
                        severity="medium",
                        location=f"{node.name}()",
                        line_start=node.lineno,
                        line_end=node.lineno,
                        description=f"Function has {param_count} parameters (threshold: {threshold})",
                        metric_value=param_count,
                        threshold=threshold,
                    )
                )
    return smells


def detect_deep_nesting(tree: ast.AST, threshold: int) -> List[CodeSmell]:
    """Detect excessive nesting depth"""
    smells = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            depth = calculate_nesting_depth(node)
            if depth > threshold:
                smells.append(
                    CodeSmell(
                        type="Deep Nesting",
                        severity="medium" if depth <= threshold + 1 else "high",
                        location=node.name,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        description=f"Nesting depth is {depth} (threshold: {threshold})",
                        metric_value=depth,
                        threshold=threshold,
                    )
                )
    return smells


def detect_duplicate_code(tree: ast.AST, min_length: int) -> List[CodeSmell]:
    """Detect potential duplicate code patterns"""
    defaultdict(list)
    smells = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.If, ast.For, ast.While)):
            source_lines = []
            if hasattr(node, "end_lineno") and node.lineno:
                for n in ast.walk(node):
                    if isinstance(n, ast.stmt):
                        source_lines.append(
                            ast.unparse(n) if hasattr(ast, "unparse") else ""
                        )

    return smells


def detect_complex_functions(tree: ast.AST, threshold: int) -> List[ComplexityIssue]:
    """Detect functions with high cyclomatic complexity"""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            complexity = calculate_cyclomatic_complexity(node)
            nesting = calculate_nesting_depth(node)
            line_count = get_function_lines(node)
            if complexity > threshold:
                issues.append(
                    ComplexityIssue(
                        name=node.name,
                        type="function",
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        complexity_score=complexity,
                        threshold=threshold,
                        nesting_depth=nesting,
                        line_count=line_count,
                    )
                )
    return issues


def detect_complex_classes(tree: ast.AST, threshold: int) -> List[ComplexityIssue]:
    """Detect classes with many methods and high complexity"""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            total_complexity = sum(calculate_cyclomatic_complexity(m) for m in methods)
            line_count = get_class_lines(node)
            if len(methods) > 10 or total_complexity > threshold * 2:
                issues.append(
                    ComplexityIssue(
                        name=node.name,
                        type="class",
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        complexity_score=total_complexity,
                        threshold=threshold,
                        nesting_depth=0,
                        line_count=line_count,
                    )
                )
    return issues


def check_srp_violations(tree: ast.AST) -> List[SOLIDViolation]:
    """Check Single Responsibility Principle violations"""
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
            has_data_manipulation = False
            has_io = False
            has_business_logic = False

            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    method_source = (
                        ast.unparse(method) if hasattr(ast, "unparse") else ""
                    )
                    if any(
                        kw in method_source.lower()
                        for kw in [
                            "save",
                            "load",
                            "read",
                            "write",
                            "file",
                            "db",
                            "database",
                        ]
                    ):
                        has_io = True
                    if any(
                        kw in method_source.lower()
                        for kw in ["calc", "compute", "process", "validate", "check"]
                    ):
                        has_business_logic = True
                    if any(
                        kw in method_source.lower()
                        for kw in ["set", "get", "add", "remove", "update", "delete"]
                    ):
                        has_data_manipulation = True

            responsibility_count = sum(
                [has_io, has_business_logic, has_data_manipulation]
            )
            if method_count > 15 or responsibility_count > 2:
                violations.append(
                    SOLIDViolation(
                        principle="SRP",
                        class_name=node.name,
                        method_name=None,
                        line=node.lineno,
                        description=f"Class has {method_count} methods and {responsibility_count} responsibilities",
                        severity="high" if responsibility_count > 2 else "medium",
                    )
                )
    return violations


def check_ocp_violations(tree: ast.AST) -> List[SOLIDViolation]:
    """Check Open/Closed Principle violations"""
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            has_modification = False
            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    method_source = (
                        ast.unparse(method) if hasattr(ast, "unparse") else ""
                    )
                    if "if" in method_source and any(
                        x in method_source.lower()
                        for x in ["type", "kind", "mode", "action"]
                    ):
                        has_modification = True
                        break

            if has_modification:
                violations.append(
                    SOLIDViolation(
                        principle="OCP",
                        class_name=node.name,
                        method_name=None,
                        line=node.lineno,
                        description="Class appears to use type-checking conditionals instead of polymorphism",
                        severity="medium",
                    )
                )
    return violations


def check_lsp_violations(tree: ast.AST) -> List[SOLIDViolation]:
    """Check Liskov Substitution Principle violations"""
    violations = []
    class_methods: Dict[str, Set[str]] = defaultdict(set)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_methods[node.name] = {
                n.name for n in node.body if isinstance(n, ast.FunctionDef)
            }

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and len(node.bases) > 0:
            parent_methods = set()
            for base in node.bases:
                if isinstance(base, ast.Name):
                    parent_methods = class_methods.get(base.id, set())

            override_methods = class_methods.get(node.name, set()) & parent_methods
            for method_name in override_methods:
                for method in node.body:
                    if (
                        isinstance(method, ast.FunctionDef)
                        and method.name == method_name
                    ):
                        if len(method.args.args) > 0:
                            violations.append(
                                SOLIDViolation(
                                    principle="LSP",
                                    class_name=node.name,
                                    method_name=method_name,
                                    line=method.lineno,
                                    description=f"Method {method_name} may violate LSP (parameter type changes)",
                                    severity="low",
                                )
                            )
    return violations


def check_isp_violations(tree: ast.AST) -> List[SOLIDViolation]:
    """Check Interface Segregation Principle violations"""
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            public_methods = [m for m in methods if not m.name.startswith("_")]
            if len(public_methods) > 10:
                violations.append(
                    SOLIDViolation(
                        principle="ISP",
                        class_name=node.name,
                        method_name=None,
                        line=node.lineno,
                        description=f"Class has {len(public_methods)} public methods - consider splitting interface",
                        severity="medium",
                    )
                )
    return violations


def check_dip_violations(tree: ast.AST) -> List[SOLIDViolation]:
    """Check Dependency Inversion Principle violations"""
    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    for arg in method.args.args:
                        if isinstance(arg, ast.arg):
                            arg_type = arg.annotation
                            if arg_type and isinstance(arg_type, ast.Name):
                                if arg_type.id[0].isupper() and arg_type.id not in [
                                    "str",
                                    "int",
                                    "float",
                                    "bool",
                                    "list",
                                    "dict",
                                    "tuple",
                                    "set",
                                ]:
                                    violations.append(
                                        SOLIDViolation(
                                            principle="DIP",
                                            class_name=node.name,
                                            method_name=method.name,
                                            line=method.lineno,
                                            description=f"Method depends on concrete class {arg_type.id} instead of abstraction",
                                            severity="low",
                                        )
                                    )
    return violations


def generate_recommendations(
    code_smells: List[CodeSmell],
    complexity_issues: List[ComplexityIssue],
    solid_violations: List[SOLIDViolation],
) -> List[Recommendation]:
    """Generate prioritized refactoring recommendations"""

    recommendations = []

    for smell in code_smells:
        if smell.type == "Long Function":
            recommendations.append(
                Recommendation(
                    title="Extract Method",
                    description=f"Break down '{smell.location}' into smaller, focused functions. Consider the Single Responsibility Principle.",
                    priority=1 if smell.severity == "high" else 2,
                    confidence=0.85,
                    effort="medium",
                    location=smell.location,
                    line_start=smell.line_start,
                    line_end=smell.line_end,
                    smell_type=smell.type,
                )
            )
        elif smell.type == "Large Class":
            recommendations.append(
                Recommendation(
                    title="Extract Class / Split Responsibility",
                    description=f"Break down '{smell.location}' into smaller, focused classes. Consider what each class should do.",
                    priority=1,
                    confidence=0.8,
                    effort="high",
                    location=smell.location,
                    line_start=smell.line_start,
                    line_end=smell.line_end,
                    smell_type=smell.type,
                )
            )
        elif smell.type == "Too Many Parameters":
            recommendations.append(
                Recommendation(
                    title="Introduce Parameter Object",
                    description="Group related parameters into a data class or object to reduce parameter count.",
                    priority=2,
                    confidence=0.75,
                    effort="low",
                    location=smell.location,
                    line_start=smell.line_start,
                    line_end=smell.line_end,
                    smell_type=smell.type,
                )
            )
        elif smell.type == "Deep Nesting":
            recommendations.append(
                Recommendation(
                    title="Reduce Nesting / Use Guard Clauses",
                    description="Reduce nesting depth by using early returns, guard clauses, or extracting logic.",
                    priority=2,
                    confidence=0.7,
                    effort="medium",
                    location=smell.location,
                    line_start=smell.line_start,
                    line_end=smell.line_end,
                    smell_type=smell.type,
                )
            )

    for issue in complexity_issues:
        if issue.type == "function":
            recommendations.append(
                Recommendation(
                    title="Reduce Cyclomatic Complexity",
                    description=f"Simplify '{issue.name}' - current complexity: {issue.complexity_score}. Consider extracting branches or using strategy pattern.",
                    priority=1 if issue.complexity_score > issue.threshold * 1.5 else 2,
                    confidence=0.8,
                    effort="medium",
                    location=issue.name,
                    line_start=issue.line_start,
                    line_end=issue.line_end,
                    smell_type="High Complexity",
                )
            )

    for violation in solid_violations:
        if violation.principle == "SRP":
            recommendations.append(
                Recommendation(
                    title="Apply Single Responsibility Principle",
                    description=f"Class '{violation.class_name}' has multiple responsibilities. Consider splitting into separate classes.",
                    priority=1,
                    confidence=0.75,
                    effort="high",
                    location=violation.class_name,
                    line_start=violation.line,
                    line_end=violation.line,
                    principle_violated="SRP",
                )
            )
        elif violation.principle == "OCP":
            recommendations.append(
                Recommendation(
                    title="Apply Open/Closed Principle",
                    description=f"Use polymorphism and extension points instead of modification in '{violation.class_name}'.",
                    priority=2,
                    confidence=0.65,
                    effort="medium",
                    location=violation.class_name,
                    line_start=violation.line,
                    line_end=violation.line,
                    principle_violated="OCP",
                )
            )
        elif violation.principle == "ISP":
            recommendations.append(
                Recommendation(
                    title="Apply Interface Segregation Principle",
                    description=f"Class '{violation.class_name}' has too many methods. Split into focused interfaces.",
                    priority=2,
                    confidence=0.7,
                    effort="medium",
                    location=violation.class_name,
                    line_start=violation.line,
                    line_end=violation.line,
                    principle_violated="ISP",
                )
            )
        elif violation.principle == "DIP":
            recommendations.append(
                Recommendation(
                    title="Apply Dependency Inversion Principle",
                    description="Depend on abstractions (protocols/interfaces) instead of concrete classes.",
                    priority=3,
                    confidence=0.6,
                    effort="medium",
                    location=f"{violation.class_name}.{violation.method_name}"
                    if violation.method_name
                    else violation.class_name,
                    line_start=violation.line,
                    line_end=violation.line,
                    principle_violated="DIP",
                )
            )

    recommendations.sort(key=lambda x: (x.priority, -x.confidence))
    return recommendations


def calculate_impact_metrics(
    code_smells: List[CodeSmell],
    complexity_issues: List[ComplexityIssue],
    solid_violations: List[SOLIDViolation],
    recommendations: List[Recommendation],
) -> Dict[str, Any]:
    """Calculate estimated impact of implementing recommendations"""

    high_severity_smells = sum(1 for s in code_smells if s.severity == "high")
    medium_severity_smells = sum(1 for s in code_smells if s.severity == "medium")

    total_complexity = sum(i.complexity_score for i in complexity_issues)

    critical_violations = sum(1 for v in solid_violations if v.severity == "high")

    estimated_improvement = (
        high_severity_smells * 15
        + medium_severity_smells * 10
        + len(complexity_issues) * 20
        + critical_violations * 25
    )

    return {
        "code_smells_count": len(code_smells),
        "high_severity_count": high_severity_smells,
        "medium_severity_count": medium_severity_smells,
        "complexity_issues_count": len(complexity_issues),
        "total_complexity_score": total_complexity,
        "solid_violations_count": len(solid_violations),
        "critical_violations": critical_violations,
        "recommendations_count": len(recommendations),
        "estimated_improvement_percentage": min(estimated_improvement, 100),
        "maintainability_score": max(0, 100 - estimated_improvement),
    }


def refactoring_recommender(code: str, options: dict = None) -> dict:
    """
    Analyze code and generate refactoring recommendations.

    Args:
        code: Python source code to analyze
        options: Analysis options including:
            - max_function_lines: Maximum lines in a function (default: 50)
            - max_class_lines: Maximum lines in a class (default: 300)
            - max_function_params: Maximum parameters (default: 5)
            - max_nesting_depth: Maximum nesting depth (default: 4)
            - max_cyclomatic_complexity: Maximum complexity (default: 10)
            - check_solid: Whether to check SOLID principles (default: True)
            - check_duplicates: Whether to check for duplicates (default: True)
            - min_duplicate_length: Minimum duplicate block length (default: 5)
            - threshold_complexity: Complexity threshold (default: 10)

    Returns:
        Dictionary containing:
            - status: "success" or "error"
            - code_smells: List of detected smells
            - complexity_issues: Functions/classes exceeding complexity
            - solid_violations: SOLID principle violations
            - recommendations: Prioritized refactoring suggestions
            - estimated_impact: Potential improvement metrics
    """
    if options is None:
        options = {}

    opts = {**DEFAULT_OPTIONS, **options}

    try:
        tree = ast.parse(code)

        code_smells = []
        code_smells.extend(detect_long_functions(tree, opts["max_function_lines"]))
        code_smells.extend(detect_long_classes(tree, opts["max_class_lines"]))
        code_smells.extend(
            detect_too_many_parameters(tree, opts["max_function_params"])
        )
        code_smells.extend(detect_deep_nesting(tree, opts["max_nesting_depth"]))

        if opts.get("check_duplicates", True):
            code_smells.extend(
                detect_duplicate_code(tree, opts.get("min_duplicate_length", 5))
            )

        complexity_issues = []
        complexity_issues.extend(
            detect_complex_functions(tree, opts["threshold_complexity"])
        )
        complexity_issues.extend(
            detect_complex_classes(tree, opts["threshold_complexity"])
        )

        solid_violations = []
        if opts.get("check_solid", True):
            solid_violations.extend(check_srp_violations(tree))
            solid_violations.extend(check_ocp_violations(tree))
            solid_violations.extend(check_lsp_violations(tree))
            solid_violations.extend(check_isp_violations(tree))
            solid_violations.extend(check_dip_violations(tree))

        recommendations = generate_recommendations(
            code_smells, complexity_issues, solid_violations
        )

        estimated_impact = calculate_impact_metrics(
            code_smells, complexity_issues, solid_violations, recommendations
        )

        return {
            "status": "success",
            "code_smells": [
                {
                    "type": s.type,
                    "severity": s.severity,
                    "location": s.location,
                    "line_start": s.line_start,
                    "line_end": s.line_end,
                    "description": s.description,
                    "metric_value": s.metric_value,
                    "threshold": s.threshold,
                }
                for s in code_smells
            ],
            "complexity_issues": [
                {
                    "name": i.name,
                    "type": i.type,
                    "line_start": i.line_start,
                    "line_end": i.line_end,
                    "complexity_score": i.complexity_score,
                    "threshold": i.threshold,
                    "nesting_depth": i.nesting_depth,
                    "line_count": i.line_count,
                }
                for i in complexity_issues
            ],
            "solid_violations": [
                {
                    "principle": v.principle,
                    "class_name": v.class_name,
                    "method_name": v.method_name,
                    "line": v.line,
                    "description": v.description,
                    "severity": v.severity,
                }
                for v in solid_violations
            ],
            "recommendations": [
                {
                    "title": r.title,
                    "description": r.description,
                    "priority": r.priority,
                    "confidence": r.confidence,
                    "effort": r.effort,
                    "location": r.location,
                    "line_start": r.line_start,
                    "line_end": r.line_end,
                    "smell_type": r.smell_type,
                    "principle_violated": r.principle_violated,
                }
                for r in recommendations
            ],
            "estimated_impact": estimated_impact,
        }

    except SyntaxError as e:
        return {
            "status": "error",
            "error": f"Syntax error in code: {str(e)}",
            "message": "Failed to parse the provided Python code",
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze code for refactoring opportunities",
        }


def invoke(payload: dict) -> dict:
    """Main entry point for MCP skill invocation"""
    code = payload.get("code", "")
    options = payload.get("options", {})

    if not code:
        return {"result": {"status": "error", "message": "No code provided"}}

    result = refactoring_recommender(code, options)
    return {"result": result}


def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "refactoring-recommender",
        "description": "Analyze Python code for refactoring opportunities - detect code smells, analyze complexity, identify SOLID violations, and generate prioritized recommendations with effort estimates",
        "version": "1.0.0",
        "domain": "CODEBASE_INTELLIGENCE",
    }


if __name__ == "__main__":
    test_code = """
class UserManager:
    def __init__(self):
        self.users = []
    
    def process_user(self, user_id, name, email, phone, address, city, state, zipcode, country, age, gender, occupation, company, salary, department, manager_id, start_date, end_date=None):
        user = {"id": user_id, "name": name, "email": email, "phone": phone, "address": address}
        if age > 18:
            if gender == "male":
                if occupation == "engineer":
                    if company:
                        if salary > 50000:
                            if department:
                                if manager_id:
                                    self.users.append(user)
        return user
    
    def save_to_database(self):
        pass
    
    def send_email(self):
        pass
    
    def validate_input(self):
        pass
    
    def calculate_salary(self):
        pass
    
    def generate_report(self):
        pass
    
    def export_data(self):
        pass
    
    def import_data(self):
        pass
    
    def backup_data(self):
        pass
    
    def restore_data(self):
        pass
    
    def process_payment(self):
        pass
    
    def update_profile(self):
        pass
    
    def delete_user(self):
        pass
"""

    result = refactoring_recommender(test_code)
    print(result)
