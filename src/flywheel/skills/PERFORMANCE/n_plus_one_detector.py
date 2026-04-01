"""
N+1 Query Detector: Detects N+1 query patterns in ORM code

This module provides N+1 query detection capabilities:
- Parse ORM code (SQLAlchemy, Django, Prisma)
- Detect N+1 patterns (loop + query anti-patterns)
- Find lazy loading issues
- Suggest fixes (eager loading, selectinload)
- Estimate query count reduction
"""

import ast
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List
from datetime import datetime


class ORMType(Enum):
    SQLALCHEMY = "sqlalchemy"
    DJANGO = "django"
    PRISMA = "prisma"
    SQLALCHEMY2 = "sqlalchemy2"


@dataclass
class NPlusOnePattern:
    type: str
    severity: str
    description: str
    location: str
    loop_variable: str
    query_pattern: str
    model_name: str
    relationship: str | None
    line_number: int
    estimated_queries: int
    suggested_fix: str


@dataclass
class LazyLoadingIssue:
    severity: str
    description: str
    location: str
    relationship: str
    model: str
    suggested_fix: str
    line_number: int


@dataclass
class FixSuggestion:
    priority: str
    category: str
    description: str
    code_example: str
    expected_improvement: str
    related_pattern: str | None


def n_plus_one_detector(code: str, options: dict) -> dict:
    """
    Detect N+1 query patterns in ORM code.

    Args:
        code: Python code with ORM queries
        options: Configuration options including:
            - orm_type: "sqlalchemy", "django", or "prisma" (default: "sqlalchemy")
            - detect_lazy_loading: Whether to detect lazy loading issues (default: True)
            - min_loop_size: Minimum loop size to flag (default: 2)
            - detect_relationship_access: Whether to detect relationship access patterns (default: True)

    Returns:
        Dictionary with detection results containing:
            - status: "success" or "error"
            - n_plus_one_queries: Detected N+1 patterns
            - lazy_loading_issues: Lazy loading problems
            - fixes: Suggested fixes
            - estimated_savings: Query reduction estimates
    """
    try:
        options = _normalize_options(options)
        orm_type = options.get("orm_type", "sqlalchemy").lower()

        n_plus_one_patterns = _detect_n_plus_one_patterns(code, options, orm_type)

        lazy_loading_issues = []
        if options.get("detect_lazy_loading", True):
            lazy_loading_issues = _detect_lazy_loading_issues(code, options, orm_type)

        fixes = _generate_fixes(n_plus_one_patterns, lazy_loading_issues, orm_type)

        estimated_savings = _estimate_savings(n_plus_one_patterns, lazy_loading_issues)

        return {
            "status": "success",
            "orm_type": orm_type,
            "n_plus_one_queries": [vars(p) for p in n_plus_one_patterns],
            "lazy_loading_issues": [vars(i) for i in lazy_loading_issues],
            "fixes": [vars(f) for f in fixes],
            "estimated_savings": estimated_savings,
            "summary": {
                "total_n_plus_one": len(n_plus_one_patterns),
                "total_lazy_loading": len(lazy_loading_issues),
                "total_queries_before": sum(
                    p.estimated_queries for p in n_plus_one_patterns
                ),
                "total_queries_after": len(n_plus_one_patterns)
                + sum(p.estimated_queries for p in n_plus_one_patterns)
                // max(1, options.get("min_loop_size", 2)),
                "lines_analyzed": len(code.splitlines()),
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze code for N+1 patterns",
        }


def _normalize_options(options: dict) -> dict:
    defaults = {
        "orm_type": "sqlalchemy",
        "detect_lazy_loading": True,
        "min_loop_size": 2,
        "detect_relationship_access": True,
    }
    return {**defaults, **options}


def _detect_n_plus_one_patterns(
    code: str, options: dict, orm_type: str
) -> List[NPlusOnePattern]:
    patterns = []
    lines = code.splitlines()
    min_loop_size = options.get("min_loop_size", 2)

    if orm_type in ["sqlalchemy", "sqlalchemy2"]:
        patterns.extend(_detect_sqlalchemy_n_plus_one(code, lines, min_loop_size))
    elif orm_type == "django":
        patterns.extend(_detect_django_n_plus_one(code, lines, min_loop_size))
    elif orm_type == "prisma":
        patterns.extend(_detect_prisma_n_plus_one(code, lines, min_loop_size))

    return patterns


def _detect_sqlalchemy_n_plus_one(
    code: str, lines: List[str], min_loop_size: int
) -> List[NPlusOnePattern]:
    patterns = []
    query_patterns = [
        r"\.query\(",
        r"\.select\(|\.select_from\(",
        r"\.execute\(.*select",
        r"session\.query\(",
        r"\.all\(\)|\.first\(\)|\.filter\(",
    ]
    loop_patterns = [
        r"for\s+(\w+)\s+in\s+(\w+)\s*:",
        r"for\s+(\w+)\s*,\s*(\w+)\s+in\s+",
    ]

    try:
        tree = ast.parse(code)
        patterns.extend(
            _analyze_ast_for_n_plus_one(tree, code, lines, min_loop_size, "sqlalchemy")
        )
    except SyntaxError:
        pass

    for i, line in enumerate(lines, 1):
        for loop_pattern in loop_patterns:
            loop_match = re.search(loop_pattern, line)
            if loop_match:
                loop_var = loop_match.group(1) if loop_match.lastindex >= 1 else None
                if loop_var:
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 10)
                    context = "\n".join(lines[context_start:context_end])

                    for qp in query_patterns:
                        if re.search(qp, context):
                            inner_loop = False
                            for j in range(i, min(len(lines), i + 5)):
                                if re.search(r"for\s+\w+\s+in\s+", lines[j]):
                                    inner_loop = True
                                    break

                            if inner_loop or re.search(rf"{loop_var}\.\w+", context):
                                patterns.append(
                                    NPlusOnePattern(
                                        type="loop_query",
                                        severity="high",
                                        description=f"Potential N+1: Query inside loop over '{loop_var}'",
                                        location=f"Line {i}",
                                        loop_variable=loop_var,
                                        query_pattern=qp,
                                        model_name=_infer_model_name(loop_var),
                                        relationship=_find_relationship_access(
                                            context, loop_var
                                        ),
                                        line_number=i,
                                        estimated_queries=min_loop_size,
                                        suggested_fix=_sqlalchemy_fix_suggestion(
                                            loop_var
                                        ),
                                    )
                                )
                            break

    return patterns


def _detect_django_n_plus_one(
    code: str, lines: List[str], min_loop_size: int
) -> List[NPlusOnePattern]:
    patterns = []
    query_patterns = [
        r"\.filter\(",
        r"\.all\(\)",
        r"\.get\(",
        r"Model\.objects\.",
        r"\.values\(\)|\.values_list\(",
    ]
    loop_patterns = [
        r"for\s+(\w+)\s+in\s+(\w+)\s*:",
    ]

    for i, line in enumerate(lines, 1):
        for loop_pattern in loop_patterns:
            loop_match = re.search(loop_pattern, line)
            if loop_match:
                loop_var = loop_match.group(1)
                (
                    loop_match.group(2) if loop_match.lastindex >= 2 else None
                )
                if loop_var:
                    context_start = max(0, i - 2)
                    context_end = min(len(lines), i + 10)
                    context = "\n".join(lines[context_start:context_end])

                    for qp in query_patterns:
                        if re.search(qp, context) and re.search(
                            rf"{loop_var}\.\w+", context
                        ):
                            patterns.append(
                                NPlusOnePattern(
                                    type="loop_query",
                                    severity="high",
                                    description=f"Django N+1: Accessing related objects in loop over '{loop_var}'",
                                    location=f"Line {i}",
                                    loop_variable=loop_var,
                                    query_pattern=qp,
                                    model_name=_infer_model_name(loop_var),
                                    relationship=_find_django_relationship_access(
                                        context, loop_var
                                    ),
                                    line_number=i,
                                    estimated_queries=min_loop_size,
                                    suggested_fix=_django_fix_suggestion(loop_var),
                                )
                            )
                            break

    return patterns


def _detect_prisma_n_plus_one(
    code: str, lines: List[str], min_loop_size: int
) -> List[NPlusOnePattern]:
    patterns = []
    loop_patterns = [
        r"for\s+\w+\s+in\s+\w+",
        r"\.forEach\(",
    ]

    for i, line in enumerate(lines, 1):
        for loop_pattern in loop_patterns:
            if re.search(loop_pattern, line):
                context_start = max(0, i - 1)
                context_end = min(len(lines), i + 10)
                context = "\n".join(lines[context_start:context_end])

                if re.search(r"\.findUnique\(|\.findFirst\(|\.findMany\(", context):
                    prisma_relations = re.findall(r"(\w+)\s*:\s*\{", context)
                    if prisma_relations:
                        patterns.append(
                            NPlusOnePattern(
                                type="loop_query",
                                severity="high",
                                description="Prisma N+1: Fetching related data in loop",
                                location=f"Line {i}",
                                loop_variable="item",
                                query_pattern="prisma.*find",
                                model_name=prisma_relations[0]
                                if prisma_relations
                                else "unknown",
                                relationship=",".join(prisma_relations),
                                line_number=i,
                                estimated_queries=min_loop_size,
                                suggested_fix=_prisma_fix_suggestion(),
                            )
                        )

    return patterns


def _analyze_ast_for_n_plus_one(
    tree: ast.AST, code: str, lines: List[str], min_loop_size: int, orm_type: str
) -> List[NPlusOnePattern]:
    patterns = []

    class NPlusOneVisitor(ast.NodeVisitor):
        def __init__(self):
            self.loops = []
            self.query_calls = []
            self.patterns_found = []

        def visit_For(self, node):
            if isinstance(node.iter, ast.Name):
                self.loops.append(
                    {
                        "var": node.target.id
                        if isinstance(node.target, ast.Name)
                        else "",
                        "iter": node.iter.id if isinstance(node.iter, ast.Name) else "",
                        "line": node.lineno,
                    }
                )
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
                if method_name in ["query", "filter", "all", "first", "execute"]:
                    self.query_calls.append(
                        {
                            "method": method_name,
                            "line": node.lineno,
                        }
                    )
            self.generic_visit(node)

    visitor = NPlusOneVisitor()
    visitor.visit(tree)

    for loop in visitor.loops:
        loop_line = loop["line"]
        for query in visitor.query_calls:
            if abs(query["line"] - loop_line) < 5:
                patterns.append(
                    NPlusOnePattern(
                        type="loop_query",
                        severity="high",
                        description=f"N+1: Query call '{query['method']}' near loop over '{loop.get('iter', 'data')}'",
                        location=f"Line {loop_line}",
                        loop_variable=loop.get("iter", "item"),
                        query_pattern=query["method"],
                        model_name=_infer_model_name(loop.get("iter", "data")),
                        relationship=None,
                        line_number=loop_line,
                        estimated_queries=min_loop_size,
                        suggested_fix="Use eager loading: query.options(joinedload(Model.relationship))",
                    )
                )

    return patterns


def _detect_lazy_loading_issues(
    code: str, options: dict, orm_type: str
) -> List[LazyLoadingIssue]:
    issues = []

    if orm_type in ["sqlalchemy", "sqlalchemy2"]:
        issues.extend(_detect_sqlalchemy_lazy_loading(code))
    elif orm_type == "django":
        issues.extend(_detect_django_lazy_loading(code))
    elif orm_type == "prisma":
        issues.extend(_detect_prisma_lazy_loading(code))

    return issues


def _detect_sqlalchemy_lazy_loading(code: str) -> List[LazyLoadingIssue]:
    issues = []
    lines = code.splitlines()

    lazy_indicators = [
        (r"relationship\([^)]+\)", "SQLAlchemy relationship without eager loading"),
        (r"backref\([^)]+\)", "Backref without eager loading"),
        (r'lazy=["\']select["\']', 'Explicit lazy="select" - triggers separate query'),
    ]

    for i, line in enumerate(lines, 1):
        for pattern, description in lazy_indicators:
            if re.search(pattern, line, re.IGNORECASE):
                rel_match = re.search(r'relationship\(["\'](\w+)["\']', line)
                rel_name = rel_match.group(1) if rel_match else "unknown"

                issues.append(
                    LazyLoadingIssue(
                        severity="medium",
                        description=f"Lazy loading: {description} on relationship '{rel_name}'",
                        location=f"Line {i}",
                        relationship=rel_name,
                        model=_infer_model_from_relationship(line),
                        suggested_fix=_sqlalchemy_eager_load_fix(rel_name),
                        line_number=i,
                    )
                )

    return issues


def _detect_django_lazy_loading(code: str) -> List[LazyLoadingIssue]:
    issues = []
    lines = code.splitlines()

    foreign_key_pattern = r"ForeignKey\([^)]+\)|models\.ForeignKey\("

    for i, line in enumerate(lines, 1):
        if re.search(foreign_key_pattern, line):
            model_match = re.search(r'ForeignKey\(["\'](\w+)["\']', line)
            if model_match:
                related_model = model_match.group(1)
                issues.append(
                    LazyLoadingIssue(
                        severity="medium",
                        description=f"Django ForeignKey to '{related_model}' - accessed lazily by default",
                        location=f"Line {i}",
                        relationship=related_model,
                        model="current_model",
                        suggested_fix=_django_eager_load_fix(related_model),
                        line_number=i,
                    )
                )

    many_to_many_pattern = r"ManyToManyField\("

    for i, line in enumerate(lines, 1):
        if re.search(many_to_many_pattern, line):
            model_match = re.search(r'ManyToManyField\(["\'](\w+)["\']', line)
            if model_match:
                related_model = model_match.group(1)
                issues.append(
                    LazyLoadingIssue(
                        severity="medium",
                        description=f"Django ManyToManyField to '{related_model}' - accessed lazily by default",
                        location=f"Line {i}",
                        relationship=related_model,
                        model="current_model",
                        suggested_fix=_django_eager_load_fix(related_model),
                        line_number=i,
                    )
                )

    return issues


def _detect_prisma_lazy_loading(code: str) -> List[LazyLoadingIssue]:
    issues = []
    lines = code.splitlines()

    relation_pattern = r"@relation\([^)]*fields:\s*\[[^\]]+\][^)]*\)"

    for i, line in enumerate(lines, 1):
        if re.search(relation_pattern, line):
            issues.append(
                LazyLoadingIssue(
                    severity="low",
                    description="Prisma relation without include - will be lazy loaded",
                    location=f"Line {i}",
                    relationship="inferred",
                    model="inferred",
                    suggested_fix=_prisma_fix_suggestion(),
                    line_number=i,
                )
            )

    return issues


def _generate_fixes(
    n_plus_one_patterns: List[NPlusOnePattern],
    lazy_loading_issues: List[LazyLoadingIssue],
    orm_type: str,
) -> List[FixSuggestion]:
    fixes = []

    for pattern in n_plus_one_patterns:
        if orm_type in ["sqlalchemy", "sqlalchemy2"]:
            fixes.append(
                FixSuggestion(
                    priority="high",
                    category="Eager Loading",
                    description=f"Use selectinload or joinedload for '{pattern.loop_variable}' relationship",
                    code_example=_sqlalchemy_fix_code_example(pattern),
                    expected_improvement=f"Reduce {pattern.estimated_queries} queries to 1-2 queries",
                    related_pattern=f"Line {pattern.line_number}",
                )
            )
        elif orm_type == "django":
            fixes.append(
                FixSuggestion(
                    priority="high",
                    category="Prefetch Related",
                    description=f"Use prefetch_related or select_related for '{pattern.loop_variable}'",
                    code_example=_django_fix_code_example(pattern),
                    expected_improvement=f"Reduce {pattern.estimated_queries} queries to 1-2 queries",
                    related_pattern=f"Line {pattern.line_number}",
                )
            )
        elif orm_type == "prisma":
            fixes.append(
                FixSuggestion(
                    priority="high",
                    category="Include",
                    description="Use Prisma's include to fetch related data",
                    code_example=_prisma_fix_code_example(pattern),
                    expected_improvement=f"Reduce {pattern.estimated_queries} queries to 1 query",
                    related_pattern=f"Line {pattern.line_number}",
                )
            )

    for issue in lazy_loading_issues:
        if orm_type in ["sqlalchemy", "sqlalchemy2"]:
            fixes.append(
                FixSuggestion(
                    priority="medium",
                    category="Lazy to Eager",
                    description=f"Change lazy loading for '{issue.relationship}' to eager loading",
                    code_example=f"relationship('{issue.relationship}', lazy='selectin')",
                    expected_improvement="Eliminate lazy load on access",
                    related_pattern=f"Line {issue.line_number}",
                )
            )
        elif orm_type == "django":
            fixes.append(
                FixSuggestion(
                    priority="medium",
                    category="QuerySet Optimization",
                    description=f"Use prefetch_related for '{issue.relationship}'",
                    code_example=f"Model.objects.prefetch_related('{issue.relationship}')",
                    expected_improvement="Single query instead of lazy loads",
                    related_pattern=f"Line {issue.line_number}",
                )
            )

    return fixes


def _estimate_savings(
    n_plus_one_patterns: List[NPlusOnePattern],
    lazy_loading_issues: List[LazyLoadingIssue],
) -> Dict:
    total_queries_before = 0
    total_queries_after = 0

    for pattern in n_plus_one_patterns:
        total_queries_before += pattern.estimated_queries + 1
        total_queries_after += 2

    for _issue in lazy_loading_issues:
        total_queries_before += 1

    queries_saved = total_queries_before - total_queries_after
    reduction_percentage = (
        (queries_saved / total_queries_before * 100) if total_queries_before > 0 else 0
    )

    return {
        "queries_before": total_queries_before,
        "queries_after": total_queries_after,
        "queries_saved": queries_saved,
        "reduction_percentage": round(reduction_percentage, 1),
        "estimated_speedup": f"{total_queries_before / max(1, total_queries_after):.1f}x"
        if total_queries_after > 0
        else "N/A",
        "impact": "high"
        if reduction_percentage > 50
        else "medium"
        if reduction_percentage > 20
        else "low",
    }


def _infer_model_name(var_name: str) -> str:
    singular = var_name.rstrip("s")
    return singular.capitalize()


def _infer_model_from_relationship(line: str) -> str:
    match = re.search(r"class\s+(\w+)\s*\(", line)
    if match:
        return match.group(1)
    return "Model"


def _find_relationship_access(context: str, loop_var: str) -> str | None:
    matches = re.findall(rf"{loop_var}\.(\w+)", context)
    return ",".join(matches[:3]) if matches else None


def _find_django_relationship_access(context: str, loop_var: str) -> str | None:
    matches = re.findall(rf"{loop_var}\.(\w+)\.(all|filter|get)", context)
    return ",".join([m[0] for m in matches[:3]]) if matches else None


def _sqlalchemy_fix_suggestion(loop_var: str) -> str:
    return (
        f"Use: query.options(selectinload({_infer_model_name(loop_var)}.relationship))"
    )


def _django_fix_suggestion(loop_var: str) -> str:
    return "Use: Model.objects.prefetch_related('related_field')"


def _prisma_fix_suggestion() -> str:
    return "Use: prisma.model.findMany({ include: { relation: true } })"


def _sqlalchemy_eager_load_fix(relationship: str) -> str:
    return f"relationship('{relationship}', lazy='selectin') or use query.options(selectinload(Model.{relationship}))"


def _django_eager_load_fix(related_model: str) -> str:
    return f"Model.objects.select_related('{related_model}') or prefetch_related('{related_model}')"


def _sqlalchemy_fix_code_example(pattern: NPlusOnePattern) -> str:
    model = pattern.model_name
    rel = pattern.relationship or "relationship_name"
    return f"""# Before
results = session.query({model}).all()
for item in results:
    print(item.{rel}.name)  # N+1 query!

# After
results = session.query({model}).options(selectinload({model}.{rel})).all()
for item in results:
    print(item.{rel}.name)  # Single query with JOIN"""


def _django_fix_code_example(pattern: NPlusOnePattern) -> str:
    model = pattern.model_name
    rel = pattern.relationship or "related_field"
    return f"""# Before
items = {model}.objects.all()
for item in items:
    print(item.{rel}.name)  # N+1 query!

# After
items = {model}.objects.prefetch_related('{rel}')
for item in items:
    print(item.{rel}.name)  # Two queries with prefetch"""


def _prisma_fix_code_example(pattern: NPlusOnePattern) -> str:
    return """// Before
const users = await prisma.user.findMany()
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { authorId: user.id } })
}

// After  
const users = await prisma.user.findMany({
  include: { posts: true }
})"""


async def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation.

    Expected payload format:
    {
        "code": "def get_users():\n    users = session.query(User).all()\n    for user in users:\n        print(user.orders)",
        "options": {
            "orm_type": "sqlalchemy" | "django" | "prisma",
            "detect_lazy_loading": true,
            "min_loop_size": 2,
            "detect_relationship_access": true,
        },
    }
    """
    code = payload.get("code", "")

    if not code:
        return {"status": "error", "error": "No code provided"}

    options = payload.get("options", {})
    result = n_plus_one_detector(code, options)

    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def generate_report(analysis: dict) -> str:
    """Generate human-readable N+1 detection report."""
    lines = []
    lines.append("=" * 60)
    lines.append("N+1 QUERY DETECTION REPORT")
    lines.append("=" * 60)
    lines.append(f"ORM Type: {analysis.get('orm_type', 'Unknown')}")
    lines.append("")

    summary = analysis.get("summary", {})
    lines.append("SUMMARY:")
    lines.append("-" * 40)
    lines.append(f"  N+1 Patterns Found: {summary.get('total_n_plus_one', 0)}")
    lines.append(f"  Lazy Loading Issues: {summary.get('total_lazy_loading', 0)}")
    lines.append(f"  Queries Before: {summary.get('total_queries_before', 0)}")
    lines.append(f"  Queries After Fix: {summary.get('total_queries_after', 0)}")
    lines.append("")

    n_plus_one_queries = analysis.get("n_plus_one_queries", [])
    if n_plus_one_queries:
        lines.append("DETECTED N+1 PATTERNS:")
        lines.append("-" * 40)
        for i, pattern in enumerate(n_plus_one_queries[:10], 1):
            lines.append(f"{i}. {pattern.get('description', 'N/A')}")
            lines.append(f"   Location: {pattern.get('location', 'N/A')}")
            lines.append(f"   Severity: {pattern.get('severity', 'N/A').upper()}")
            lines.append("")

    lazy_loading = analysis.get("lazy_loading_issues", [])
    if lazy_loading:
        lines.append("LAZY LOADING ISSUES:")
        lines.append("-" * 40)
        for i, issue in enumerate(lazy_loading[:10], 1):
            lines.append(f"{i}. {issue.get('description', 'N/A')}")
            lines.append(f"   Location: {issue.get('location', 'N/A')}")
            lines.append("")

    fixes = analysis.get("fixes", [])
    if fixes:
        lines.append("SUGGESTED FIXES:")
        lines.append("-" * 40)
        for i, fix in enumerate(fixes[:5], 1):
            lines.append(
                f"{i}. [{fix.get('priority', 'low').upper()}] {fix.get('description', 'N/A')}"
            )
            lines.append(f"   Example: {fix.get('code_example', 'N/A')[:60]}...")
            lines.append(f"   Expected: {fix.get('expected_improvement', 'N/A')}")
            lines.append("")

    savings = analysis.get("estimated_savings", {})
    if savings:
        lines.append("ESTIMATED SAVINGS:")
        lines.append("-" * 40)
        lines.append(f"  Queries Saved: {savings.get('queries_saved', 0)}")
        lines.append(f"  Reduction: {savings.get('reduction_percentage', 0)}%")
        lines.append(f"  Speedup: {savings.get('estimated_speedup', 'N/A')}")

    return "\n".join(lines)


def register_skill():
    """Return skill metadata for MCP registration."""
    return {
        "name": "n-plus-one-detector",
        "description": "Detect N+1 query patterns in ORM code (SQLAlchemy, Django, Prisma) - finds loop+query anti-patterns, lazy loading issues, suggests eager loading fixes, and estimates query reduction",
        "version": "1.0.0",
        "domain": "PERFORMANCE",
        "capabilities": [
            "Parse ORM code (SQLAlchemy, Django, Prisma)",
            "Detect N+1 query patterns",
            "Find lazy loading issues",
            "Suggest eager loading fixes",
            "Estimate query count reduction",
            "Generate code fix examples",
        ],
        "options": {
            "orm_type": "ORM type (sqlalchemy, django, prisma)",
            "detect_lazy_loading": "Whether to detect lazy loading issues (default: True)",
            "min_loop_size": "Minimum loop size to flag (default: 2)",
            "detect_relationship_access": "Whether to detect relationship access patterns (default: True)",
        },
    }


if __name__ == "__main__":
    test_codes = [
        {
            "name": "SQLAlchemy N+1",
            "code": """
def get_users_with_orders():
    session = Session()
    users = session.query(User).all()
    for user in users:
        for order in user.orders:
            print(order.total)
""",
            "options": {"orm_type": "sqlalchemy"},
        },
        {
            "name": "Django N+1",
            "code": """
def get_articles():
    articles = Article.objects.all()
    for article in articles:
        print(article.author.name)
        print(article.category.title)
""",
            "options": {"orm_type": "django"},
        },
    ]

    for test in test_codes:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print("=" * 60)
        result = n_plus_one_detector(test["code"], test["options"])
        print(f"Status: {result.get('status')}")
        print(f"N+1 Patterns: {len(result.get('n_plus_one_queries', []))}")
        print(f"Lazy Loading Issues: {len(result.get('lazy_loading_issues', []))}")
        print(f"Savings: {result.get('estimated_savings', {})}")
