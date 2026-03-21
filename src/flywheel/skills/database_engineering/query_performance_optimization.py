import logging
import re
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def analyze_query_patterns(queries: List[str]) -> List[Dict[str, Any]]:
    analysis = []

    for i, query in enumerate(queries):
        issues = []
        recommendations = []

        query_lower = query.lower()

        if "select *" in query_lower:
            issues.append("Using SELECT * instead of specific columns")
            recommendations.append(
                "Specify only required columns to reduce data transfer"
            )

        if re.search(r'where\s+.*\s+like\s+["\']%', query_lower):
            issues.append("Leading wildcard in LIKE pattern prevents index usage")
            recommendations.append("Avoid leading wildcards or use full-text search")

        if query_lower.count("join") > 3:
            issues.append("Multiple joins may indicate denormalized schema")
            recommendations.append("Review schema design or use materialized views")

        if re.search(r"where\s+.*\s+is\s+null", query_lower):
            issues.append("IS NULL conditions may not use indexes efficiently")
            recommendations.append(
                "Consider using a placeholder value or partial index"
            )

        if "order by rand()" in query_lower:
            issues.append("ORDER BY RAND() is extremely slow on large tables")
            recommendations.append(
                "Use application-side randomization or reservoir sampling"
            )

        if not re.search(r"\bwhere\b", query_lower):
            issues.append("Query without WHERE clause scans entire table")
            recommendations.append("Add appropriate WHERE conditions or pagination")

        if re.search(r"select\s+.*\s+from\s+.*\s+where\s+.*\s+in\s*\(", query_lower):
            issues.append("IN clause with subquery may be slow")
            recommendations.append("Consider JOIN or EXISTS alternatives")

        analysis.append(
            {
                "query_id": f"query-{i + 1:03d}",
                "query": query[:100] + "..." if len(query) > 100 else query,
                "issues": issues if issues else ["No major issues detected"],
                "recommendations": recommendations
                if recommendations
                else ["Query appears optimized"],
                "risk_level": "high"
                if len(issues) >= 3
                else "medium"
                if issues
                else "low",
            }
        )

    return analysis


def analyze_explain_plan(explain_output: Dict[str, Any]) -> Dict[str, Any]:
    findings = []
    total_cost = 0

    plan = explain_output.get("plan", {})

    if "Seq Scan" in str(plan) or "seqscan" in str(plan).lower():
        findings.append(
            {
                "type": "seq_scan",
                "severity": "high",
                "description": "Sequential scan detected - consider adding index",
            }
        )

    if "Nested Loop" in str(plan) or "nestedloop" in str(plan).lower():
        findings.append(
            {
                "type": "nested_loop",
                "severity": "medium",
                "description": "Nested loop join detected - verify join order and indexes",
            }
        )

    if "Hash Join" in str(plan) or "hashjoin" in str(plan).lower():
        findings.append(
            {
                "type": "hash_join",
                "severity": "low",
                "description": "Hash join used - generally efficient",
            }
        )

    cost = explain_output.get("cost", {})
    if cost:
        total_cost = cost.get("total", cost.get("startup", 0))

    return {
        "findings": findings,
        "estimated_cost": total_cost,
        "recommendations": [
            "Add indexes on frequently filtered columns",
            "Review join order and ensure proper indexing",
            "Consider partitioning large tables",
        ]
        if findings
        else ["Query plan looks optimal"],
        "needs_optimization": len([f for f in findings if f["severity"] == "high"]) > 0,
    }


def suggest_indexes(queries: List[str]) -> List[Dict[str, Any]]:
    index_candidates = []

    for _i, query in enumerate(queries):
        query_lower = query.lower()

        where_match = re.search(r"where\s+(\w+)", query_lower)
        if where_match:
            column = where_match.group(1)
            table_match = re.search(r"from\s+(\w+)", query_lower)
            table = table_match.group(1) if table_match else "unknown"

            existing = False
            for candidate in index_candidates:
                if candidate["table"] == table and column in candidate["columns"]:
                    existing = True
                    break

            if not existing:
                index_candidates.append(
                    {
                        "table": table,
                        "columns": [column],
                        "query": query[:50] + "..." if len(query) > 50 else query,
                        "index_type": "btree",
                        "priority": "high"
                        if "where" in query_lower and "join" in query_lower
                        else "medium",
                    }
                )

        join_match = re.search(r"join\s+(\w+)\s+on\s+(\w+)\.(\w+)", query_lower)
        if join_match:
            table = join_match.group(1)
            column = join_match.group(3)
            existing = False
            for candidate in index_candidates:
                if candidate["table"] == table and column in candidate["columns"]:
                    existing = True
                    break
            if not existing:
                index_candidates.append(
                    {
                        "table": table,
                        "columns": [column],
                        "query": "JOIN condition",
                        "index_type": "btree",
                        "priority": "high",
                    }
                )

    return index_candidates


def detect_n_plus_one(queries: List[str]) -> Dict[str, Any]:
    has_loop_pattern = False
    potential_issues = []

    for query in queries:
        if "for" in query.lower() and "in" in query.lower():
            has_loop_pattern = True
            potential_issues.append(
                {
                    "type": "potential_n_plus_one",
                    "query": query[:50],
                    "description": "Loop with IN clause detected - may cause N+1 queries",
                }
            )

    return {
        "detected": has_loop_pattern,
        "issues": potential_issues,
        "recommendations": [
            "Use JOIN or batch query instead of loop with IN",
            "Consider eager loading or prefetching",
            "Implement query batching at application level",
        ]
        if has_loop_pattern
        else [],
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "analyze")

    try:
        if action == "analyze":
            queries = payload.get("queries", [])
            analysis = analyze_query_patterns(queries)

            return {
                "result": {"query_analysis": analysis},
                "metadata": {
                    "action": "analyze",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "explain":
            explain_output = payload.get("explain_output", {})
            result = analyze_explain_plan(explain_output)
            return {
                "result": result,
                "metadata": {
                    "action": "explain",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "suggest_indexes":
            queries = payload.get("queries", [])
            indexes = suggest_indexes(queries)
            return {
                "result": {"index_candidates": indexes},
                "metadata": {
                    "action": "suggest_indexes",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "detect_n_plus_one":
            queries = payload.get("queries", [])
            result = detect_n_plus_one(queries)
            return {
                "result": result,
                "metadata": {
                    "action": "detect_n_plus_one",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "optimize":
            queries = payload.get("queries", [])
            explain_output = payload.get("explain_output", {})

            analysis = analyze_query_patterns(queries)
            indexes = suggest_indexes(queries)
            n_plus_one = detect_n_plus_one(queries)
            explain = analyze_explain_plan(explain_output) if explain_output else {}

            return {
                "result": {
                    "query_analysis": analysis,
                    "index_candidates": indexes,
                    "n_plus_one": n_plus_one,
                    "explain_analysis": explain,
                },
                "metadata": {
                    "action": "optimize",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in query_performance_optimization: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
