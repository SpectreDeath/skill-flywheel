"""
Query Optimizer: Database query optimization skill

This module provides SQL query optimization capabilities:
- Parse and analyze SQL query structure
- Detect common performance issues (N+1, missing indexes, full table scans)
- Suggest optimization improvements
- Generate simulated execution plans
- Estimate performance impact
"""

import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class DatabaseType(Enum):
    POSTGRESQL = "PostgreSQL"
    MYSQL = "MySQL"
    SQLITE = "SQLite"


@dataclass
class QueryComponents:
    query_type: str
    tables: List[str]
    columns: List[str]
    joins: List[Dict[str, str]]
    where_clauses: List[str]
    order_by: List[str]
    group_by: List[str]
    having: List[str]
    limit_value: Optional[int]
    subqueries: List[str]
    indexes_used: List[str]


@dataclass
class QueryIssue:
    severity: str
    category: str
    description: str
    location: str
    impact: str
    recommendation: str


@dataclass
class OptimizationSuggestion:
    priority: str
    category: str
    description: str
    sql_example: str
    expected_improvement: str


@dataclass
class ExecutionPlanStep:
    operation: str
    table: str
    condition: str
    estimated_rows: int
    cost_estimate: float
    details: str


def query_optimizer(query: str, options: dict) -> dict:
    """
    Analyze and optimize SQL queries.

    Args:
        query: SQL query to optimize
        options: Configuration options including:
            - db_type: "PostgreSQL", "MySQL", or "SQLite" (default: "PostgreSQL")
            - analyze_indexes: Whether to analyze index usage (default: True)
            - detect_n_plus_one: Whether to detect N+1 patterns (default: True)
            - check_full_scans: Whether to check for full table scans (default: True)

    Returns:
        Dictionary with optimization results containing:
            - status: "success" or "error"
            - issues: Detected query issues
            - suggestions: Optimization suggestions
            - execution_plan: Query execution plan
            - estimated_improvement: Expected performance gain
    """
    try:
        options = _normalize_options(options)
        db_type = options.get("db_type", "PostgreSQL")

        components = _parse_query(query)

        issues = _detect_issues(query, components, options, db_type)

        suggestions = _generate_suggestions(query, components, issues, db_type)

        execution_plan = _generate_execution_plan(query, components, options, db_type)

        estimated_improvement = _estimate_improvement(issues, suggestions)

        return {
            "status": "success",
            "query_type": components.query_type,
            "tables": components.tables,
            "db_type": db_type,
            "issues": issues,
            "suggestions": suggestions,
            "execution_plan": execution_plan,
            "estimated_improvement": estimated_improvement,
            "complexity_score": _calculate_complexity(components),
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze query",
        }


def _normalize_options(options: dict) -> dict:
    defaults = {
        "db_type": "PostgreSQL",
        "analyze_indexes": True,
        "detect_n_plus_one": True,
        "check_full_scans": True,
    }
    return {**defaults, **options}


def _parse_query(query: str) -> QueryComponents:
    query = query.strip()
    query_upper = query.upper()

    query_type = "SELECT"
    if query_upper.startswith("SELECT"):
        query_type = "SELECT"
    elif query_upper.startswith("INSERT"):
        query_type = "INSERT"
    elif query_upper.startswith("UPDATE"):
        query_type = "UPDATE"
    elif query_upper.startswith("DELETE"):
        query_type = "DELETE"

    tables = _extract_tables(query)

    columns = _extract_columns(query)

    joins = _extract_joins(query)

    where_clauses = _extract_where_clauses(query)

    order_by = _extract_order_by(query)

    group_by = _extract_group_by(query)

    having = _extract_having(query)

    limit_value = _extract_limit(query)

    subqueries = _extract_subqueries(query)

    indexes_used = _identify_potential_indexes(tables, where_clauses, order_by)

    return QueryComponents(
        query_type=query_type,
        tables=tables,
        columns=columns,
        joins=joins,
        where_clauses=where_clauses,
        order_by=order_by,
        group_by=group_by,
        having=having,
        limit_value=limit_value,
        subqueries=subqueries,
        indexes_used=indexes_used,
    )


def _extract_tables(query: str) -> List[str]:
    tables = []

    from_pattern = r"FROM\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)"
    for match in re.finditer(from_pattern, query, re.IGNORECASE):
        table = match.group(1).split(".")[-1].strip()
        if table not in tables:
            tables.append(table)

    join_pattern = r"(?:INNER|LEFT|RIGHT|OUTER)?\s*JOIN\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)?)"
    for match in re.finditer(join_pattern, query, re.IGNORECASE):
        table = match.group(1).split(".")[-1].strip()
        if table not in tables:
            tables.append(table)

    into_pattern = r"INTO\s+([a-zA-Z_][a-zA-Z0-9_]*)"
    for match in re.finditer(into_pattern, query, re.IGNORECASE):
        table = match.group(1).strip()
        if table not in tables:
            tables.append(table)

    update_pattern = r"UPDATE\s+([a-zA-Z_][a-zA-Z0-9_]*)"
    for match in re.finditer(update_pattern, query, re.IGNORECASE):
        table = match.group(1).strip()
        if table not in tables:
            tables.append(table)

    return tables


def _extract_columns(query: str) -> List[str]:
    columns = []

    select_pattern = r"SELECT\s+(.+?)\s+FROM"
    match = re.search(select_pattern, query, re.IGNORECASE | re.DOTALL)
    if match:
        cols_str = match.group(1).strip()
        if cols_str != "*":
            for col in re.split(r",\s*", cols_str):
                col = col.strip()
                col = re.sub(r"^\w+\.", "", col)
                col = re.sub(r"\s+AS\s+\w+", "", col, flags=re.IGNORECASE)
                col = col.strip()
                if col and col not in columns:
                    columns.append(col)

    return columns


def _extract_joins(query: str) -> List[Dict[str, str]]:
    joins = []

    join_pattern = r"(?:(INNER|LEFT|RIGHT|OUTER|FULL)\s+)?JOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+(?:AS\s+)?(\w+)?\s+ON\s+(.+?)(?=\s+(?:INNER|LEFT|RIGHT|OUTER|FULL|WHERE|GROUP|ORDER|LIMIT)|$)"
    for match in re.finditer(join_pattern, query, re.IGNORECASE | re.DOTALL):
        join_type = match.group(1) or "INNER"
        table = match.group(2)
        alias = match.group(3) or table
        condition = match.group(4).strip()

        joins.append(
            {
                "type": join_type.upper(),
                "table": table,
                "alias": alias,
                "condition": condition,
            }
        )

    return joins


def _extract_where_clauses(query: str) -> List[str]:
    where_clauses = []

    where_pattern = r"WHERE\s+(.+?)(?:\s+(?:GROUP|ORDER|HAVING|LIMIT)|$)"
    match = re.search(where_pattern, query, re.IGNORECASE | re.DOTALL)
    if match:
        where_str = match.group(1).strip()
        conditions = re.split(r"\s+AND\s+", where_str, flags=re.IGNORECASE)
        for cond in conditions:
            cond = cond.strip()
            if cond:
                where_clauses.append(cond)

    return where_clauses


def _extract_order_by(query: str) -> List[str]:
    order_by = []

    order_pattern = r"ORDER\s+BY\s+(.+?)(?:\s+(?:LIMIT|HAVING)|$)"
    match = re.search(order_pattern, query, re.IGNORECASE | re.DOTALL)
    if match:
        order_str = match.group(1).strip()
        for col in re.split(r",\s*", order_str):
            col = col.strip()
            if col:
                order_by.append(col)

    return order_by


def _extract_group_by(query: str) -> List[str]:
    group_by = []

    group_pattern = r"GROUP\s+BY\s+(.+?)(?:\s+(?:HAVING|ORDER|LIMIT)|$)"
    match = re.search(group_pattern, query, re.IGNORECASE | re.DOTALL)
    if match:
        group_str = match.group(1).strip()
        for col in re.split(r",\s*", group_str):
            col = col.strip()
            if col:
                group_by.append(col)

    return group_by


def _extract_having(query: str) -> List[str]:
    having = []

    having_pattern = r"HAVING\s+(.+?)(?:\s+(?:ORDER|LIMIT)|$)"
    match = re.search(having_pattern, query, re.IGNORECASE | re.DOTALL)
    if match:
        having_str = match.group(1).strip()
        conditions = re.split(r"\s+AND\s+", having_str, flags=re.IGNORECASE)
        for cond in conditions:
            cond = cond.strip()
            if cond:
                having.append(cond)

    return having


def _extract_limit(query: str) -> Optional[int]:
    limit_pattern = r"LIMIT\s+(\d+)"
    match = re.search(limit_pattern, query, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def _extract_subqueries(query: str) -> List[str]:
    subqueries = []

    subquery_pattern = r"\((SELECT\s+.+?)\)"
    for match in re.finditer(subquery_pattern, query, re.IGNORECASE | re.DOTALL):
        subquery = match.group(1).strip()
        if subquery not in subqueries:
            subqueries.append(subquery)

    return subqueries


def _identify_potential_indexes(
    tables: List[str], where_clauses: List[str], order_by: List[str]
) -> List[str]:
    indexes = []

    for clause in where_clauses:
        col_pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=|>|<|>=|<=|LIKE|IN|\bass\b)"
        for match in re.finditer(col_pattern, clause, re.IGNORECASE):
            col = match.group(1)
            if col.lower() not in ["and", "or", "not", "is", "null", "true", "false"]:
                indexes.append(col)

    for col in order_by:
        col_clean = re.sub(r"\s+(ASC|DESC)", "", col, flags=re.IGNORECASE).strip()
        if col_clean not in indexes:
            indexes.append(col_clean)

    return list(dict.fromkeys(indexes))


def _detect_issues(
    query: str, components: QueryComponents, options: dict, db_type: str
) -> List[Dict]:
    issues = []

    if options.get("detect_n_plus_one"):
        issues.extend(_detect_n_plus_one(query, components))

    if options.get("check_full_scans"):
        issues.extend(_detect_full_scans(query, components, options))

    issues.extend(_detect_missing_indexes(components, options))

    issues.extend(_detect_subquery_issues(components))

    issues.extend(_detect_join_issues(components))

    issues.extend(_detect_order_by_issues(components))

    issues.extend(_detect_select_star_issues(query, components))

    return sorted(
        issues,
        key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(
            x.get("severity", "low"), 3
        ),
    )


def _detect_n_plus_one(query: str, components: QueryComponents) -> List[Dict]:
    issues = []

    if len(components.tables) > 1 and not components.joins:
        issues.append(
            {
                "severity": "high",
                "category": "N+1 Query",
                "description": "Potential N+1 query pattern detected - multiple tables without explicit JOINs",
                "location": f"Tables: {', '.join(components.tables)}",
                "impact": "Each row in the outer query triggers additional queries for related tables",
                "recommendation": "Use JOINs to fetch related data in a single query instead of multiple queries",
            }
        )

    if components.subqueries:
        for i, subquery in enumerate(components.subqueries):
            if re.search(r"^\s*SELECT\s+.+\s+FROM", subquery, re.IGNORECASE):
                if "JOIN" not in subquery.upper():
                    issues.append(
                        {
                            "severity": "medium",
                            "category": "N+1 Query",
                            "description": "Subquery may cause N+1 behavior",
                            "location": f"Subquery {i+1}",
                            "impact": "Subquery executes for each row of the outer query",
                            "recommendation": "Consider converting subquery to JOIN or using a CTE",
                        }
                    )

    return issues


def _detect_full_scans(
    query: str, components: QueryComponents, options: dict
) -> List[Dict]:
    issues = []

    for clause in components.where_clauses:
        if re.search(r'^\s*\w+\s*LIKE\s+[\'"]%', clause, re.IGNORECASE):
            issues.append(
                {
                    "severity": "high",
                    "category": "Full Table Scan",
                    "description": "Leading wildcard in LIKE pattern forces full table scan",
                    "location": clause,
                    "impact": "Cannot use index due to leading wildcard - scans all rows",
                    "recommendation": "Use full-text search indexes or consider reversing the pattern",
                }
            )

        if re.search(r"NOT\s+(=|LIKE|IN\b)", clause, re.IGNORECASE):
            issues.append(
                {
                    "severity": "medium",
                    "category": "Full Table Scan",
                    "description": "NOT operator may prevent index usage",
                    "location": clause,
                    "impact": "Database must scan all rows to find non-matching records",
                    "recommendation": "Consider using positive conditions with OR or restructuring the query",
                }
            )

        if re.search(r"OR\s+", clause, re.IGNORECASE):
            issues.append(
                {
                    "severity": "low",
                    "category": "Potential Full Scan",
                    "description": "OR condition may prevent index usage on some databases",
                    "location": clause,
                    "impact": "May require scanning multiple index trees",
                    "recommendation": "Consider using UNION ALL for better index utilization",
                }
            )

        if re.search(r"IS\s+NOT\s+NULL", clause, re.IGNORECASE):
            issues.append(
                {
                    "severity": "low",
                    "category": "Potential Full Scan",
                    "description": "IS NOT NULL condition may not use indexes efficiently",
                    "location": clause,
                    "impact": "Many databases cannot use B-tree indexes for NULL checks efficiently",
                    "recommendation": "Consider using a covering index or restructuring",
                }
            )

        if re.search(r"FUNC\(\w+\)", clause, re.IGNORECASE):
            func_match = re.search(r"(\w+)\s*\(\s*(\w+)", clause, re.IGNORECASE)
            if func_match:
                issues.append(
                    {
                        "severity": "high",
                        "category": "Function on Column",
                        "description": f"Function '{func_match.group(1)}' on column '{func_match.group(2)}' prevents index usage",
                        "location": clause,
                        "impact": "Database must evaluate function on every row before comparison",
                        "recommendation": "Move the function call to the other side of the comparison or use expression indexes",
                    }
                )

    for order_col in components.order_by:
        if re.search(r"\w+\s*\(\s*", order_col, re.IGNORECASE):
            issues.append(
                {
                    "severity": "medium",
                    "category": "Full Index Scan",
                    "description": "Function in ORDER BY prevents index usage",
                    "location": order_col,
                    "impact": "Must evaluate function on all rows before sorting",
                    "recommendation": "Use expression index or pre-compute the value",
                }
            )

    if not components.where_clauses and not components.limit_value:
        issues.append(
            {
                "severity": "medium",
                "category": "Full Table Scan",
                "description": "Query without WHERE clause and no LIMIT will scan entire table",
                "location": "Query level",
                "impact": "Scans all rows in the table - no filtering applied",
                "recommendation": "Add WHERE clause to filter results or add LIMIT",
            }
        )

    return issues


def _detect_missing_indexes(components: QueryComponents, options: dict) -> List[Dict]:
    issues = []

    if not options.get("analyze_indexes"):
        return issues

    for table in components.tables:
        if not components.where_clauses:
            issues.append(
                {
                    "severity": "medium",
                    "category": "Missing Index",
                    "description": f"No WHERE clause for table '{table}' - full table scan likely",
                    "location": f"Table: {table}",
                    "impact": "No index available for filtering - full table scan required",
                    "recommendation": f"Consider creating an index on frequently queried columns in '{table}'",
                }
            )

    for i, clause in enumerate(components.where_clauses):
        col_match = re.match(r"^(\w+)", clause.strip())
        if col_match:
            col = col_match.group(1)
            if col.lower() not in ["and", "or", "not"]:
                pass

    for col in components.group_by:
        issues.append(
            {
                "severity": "low",
                "category": "Consider Index",
                "description": f"GROUP BY column '{col}' could benefit from an index",
                "location": f"GROUP BY {col}",
                "impact": "Index can speed up GROUP BY operations significantly",
                "recommendation": f"Create index on column '{col}' for better GROUP BY performance",
            }
        )

    return issues


def _detect_subquery_issues(components: QueryComponents) -> List[Dict]:
    issues = []

    if len(components.subqueries) > 3:
        issues.append(
            {
                "severity": "medium",
                "category": "Subquery Complexity",
                "description": f"Multiple subqueries detected ({len(components.subqueries)}) - may impact performance",
                "location": "Query level",
                "impact": "Each subquery adds complexity and potential for inefficient execution",
                "recommendation": "Consider using CTEs (WITH clause) or joining subqueries for better optimization",
            }
        )

    for i, subquery in enumerate(components.subqueries):
        if subquery.upper().startswith("SELECT") and "FROM" in subquery.upper():
            if re.search(r"WHERE\s+\w+\s*=\s*\$", subquery, re.IGNORECASE):
                issues.append(
                    {
                        "severity": "high",
                        "category": "Correlated Subquery",
                        "description": "Correlated subquery detected - executes for each outer row",
                        "location": f"Subquery {i+1}",
                        "impact": "Performance degrades significantly with large datasets",
                        "recommendation": "Convert to JOIN or use EXISTS with proper indexing",
                    }
                )

    return issues


def _detect_join_issues(components: QueryComponents) -> List[Dict]:
    issues = []

    for join in components.joins:
        if join["type"] == "LEFT" and components.where_clauses:
            where_str = " ".join(components.where_clauses)
            if (
                join["table"].lower() in where_str.lower()
                and "is not null" in where_str.lower()
            ):
                issues.append(
                    {
                        "severity": "low",
                        "category": "Unnecessary Join Type",
                        "description": "LEFT JOIN with NULL check could be INNER JOIN",
                        "location": f"JOIN {join['table']}",
                        "impact": "LEFT JOIN is slower than INNER JOIN when NULL is filtered",
                        "recommendation": "Change LEFT JOIN to INNER JOIN if NULL values are filtered",
                    }
                )

    if len(components.joins) > 5:
        issues.append(
            {
                "severity": "medium",
                "category": "Join Complexity",
                "description": f"Multiple joins detected ({len(components.joins)}) - query complexity is high",
                "location": "Query level",
                "impact": "Each join multiplies complexity and potential for poor performance",
                "recommendation": "Consider denormalizing data or using materialized views",
            }
        )

    return issues


def _detect_order_by_issues(components: QueryComponents) -> List[Dict]:
    issues = []

    if components.order_by and not components.where_clauses:
        issues.append(
            {
                "severity": "low",
                "category": "Sort Performance",
                "description": "ORDER BY without WHERE clause - full table sort required",
                "location": "ORDER BY clause",
                "impact": "Must sort entire result set in memory - slow for large tables",
                "recommendation": "Add WHERE clause to reduce result set before sorting",
            }
        )

    if len(components.order_by) > 3:
        issues.append(
            {
                "severity": "low",
                "category": "Sort Performance",
                "description": f"Multiple columns in ORDER BY ({len(components.order_by)}) - complex sort",
                "location": "ORDER BY clause",
                "impact": "Multi-column sorts are more expensive and may not use indexes efficiently",
                "recommendation": "Create composite index matching ORDER BY column order",
            }
        )

    return issues


def _detect_select_star_issues(query: str, components: QueryComponents) -> List[Dict]:
    issues = []

    if re.search(r"SELECT\s+\*", query, re.IGNORECASE):
        issues.append(
            {
                "severity": "low",
                "category": "Select Star",
                "description": "SELECT * fetches unnecessary columns - increases data transfer and memory",
                "location": "SELECT clause",
                "impact": "Fetches all columns including unused ones - wastes bandwidth and memory",
                "recommendation": "Specify only required columns explicitly",
            }
        )

    return issues


def _generate_suggestions(
    query: str, components: QueryComponents, issues: List[Dict], db_type: str
) -> List[Dict]:
    suggestions = []

    issue_categories = {issue["category"] for issue in issues}

    if "N+1 Query" in issue_categories:
        if len(components.tables) > 1 and not components.joins:
            tables_str = ", ".join(components.tables)
            suggestions.append(
                {
                    "priority": "high",
                    "category": "Query Restructuring",
                    "description": "Use explicit JOINs instead of multiple queries or implicit joins",
                    "sql_example": f"SELECT * FROM {components.tables[0]} t1 JOIN {components.tables[1]} t2 ON t1.id = t2.{_singularize(components.tables[0])}_id",
                    "expected_improvement": "50-90% reduction in query execution time",
                }
            )

    if (
        "Full Table Scan" in issue_categories
        or "Function on Column" in issue_categories
    ):
        suggestions.append(
            {
                "priority": "high",
                "category": "Index Creation",
                "description": "Create indexes on filtered and sorted columns",
                "sql_example": f"CREATE INDEX idx_{components.tables[0]}_column ON {components.tables[0]}(column_name) WHERE column_name IS NOT NULL"
                if db_type == "PostgreSQL"
                else f"CREATE INDEX idx_{components.tables[0]}_column ON {components.tables[0]}(column_name)",
                "expected_improvement": "10-100x improvement for filtered queries",
            }
        )

    if "Subquery Complexity" in issue_categories:
        suggestions.append(
            {
                "priority": "medium",
                "category": "Query Restructuring",
                "description": "Replace multiple subqueries with CTEs for better optimization",
                "sql_example": "WITH cte1 AS (SELECT ...), cte2 AS (SELECT ...) SELECT * FROM cte1 JOIN cte2",
                "expected_improvement": "20-40% improvement in query planning",
            }
        )

    if "Correlated Subquery" in issue_categories:
        suggestions.append(
            {
                "priority": "high",
                "category": "Query Restructuring",
                "description": "Convert correlated subquery to JOIN or EXISTS",
                "sql_example": "SELECT * FROM t1 WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.id = t1.t2_id)",
                "expected_improvement": "50-95% improvement for large datasets",
            }
        )

    if "Select Star" in issue_categories:
        suggestions.append(
            {
                "priority": "low",
                "category": "Query Optimization",
                "description": "Replace SELECT * with specific column list",
                "sql_example": f"SELECT {', '.join(components.columns[:5]) if components.columns else 'id, name'} FROM {components.tables[0]}",
                "expected_improvement": "10-30% reduction in data transfer",
            }
        )

    if "GROUP BY" in str(components.group_by) and "Consider Index" in issue_categories:
        suggestions.append(
            {
                "priority": "medium",
                "category": "Index Creation",
                "description": "Create composite index for GROUP BY columns",
                "sql_example": f"CREATE INDEX idx_{components.tables[0]}_group ON {components.tables[0]}({', '.join(components.group_by)})",
                "expected_improvement": "30-70% improvement for GROUP BY queries",
            }
        )

    if not suggestions:
        suggestions.append(
            {
                "priority": "low",
                "category": "General",
                "description": "Query appears well-structured. Consider adding LIMIT for pagination",
                "sql_example": f"{query.rstrip(';')} LIMIT 100",
                "expected_improvement": "Prevents large result sets and improves response time",
            }
        )

    return suggestions


def _generate_execution_plan(
    query: str, components: QueryComponents, options: dict, db_type: str
) -> List[Dict]:
    plan = []

    plan.append(
        {
            "step": 1,
            "operation": "Parse and Analyze",
            "table": components.tables[0] if components.tables else "N/A",
            "condition": "Query syntax validation",
            "estimated_rows": 1,
            "cost_estimate": 0.1,
            "details": "Query is parsed and validated for syntax",
        }
    )

    if components.tables:
        has_where = len(components.where_clauses) > 0
        has_join = len(components.joins) > 0
        has_order = len(components.order_by) > 0
        has_group = len(components.group_by) > 0

        if has_where:
            estimated_cost = 10.0 if components.indexes_used else 100.0
            plan.append(
                {
                    "step": 2,
                    "operation": "Filter",
                    "table": components.tables[0],
                    "condition": " AND ".join(components.where_clauses[:2]),
                    "estimated_rows": max(
                        1, 1000 // (len(components.where_clauses) * 10)
                    ),
                    "cost_estimate": estimated_cost,
                    "details": f"{'Index Scan' if components.indexes_used else 'Seq Scan'} - filtering rows based on WHERE conditions",
                }
            )

        if has_join:
            for i, join in enumerate(components.joins, 1):
                plan.append(
                    {
                        "step": 2 + i,
                        "operation": f"{join['type']} Join",
                        "table": join["table"],
                        "condition": join["condition"],
                        "estimated_rows": max(1, 500 // (i + 1)),
                        "cost_estimate": 50.0 * (i + 1),
                        "details": f"Hash {'Merge'} Join - joining {join['table']} with result set",
                    }
                )

        if has_group:
            plan.append(
                {
                    "step": len(plan) + 1,
                    "operation": "Group",
                    "table": components.tables[0] if components.tables else "N/A",
                    "condition": ", ".join(components.group_by),
                    "estimated_rows": max(1, 100 // len(components.group_by)),
                    "cost_estimate": 30.0,
                    "details": "Hash Aggregate - grouping rows by specified columns",
                }
            )

        if has_order:
            plan.append(
                {
                    "step": len(plan) + 1,
                    "operation": "Sort",
                    "table": components.tables[0] if components.tables else "N/A",
                    "condition": ", ".join(components.order_by),
                    "estimated_rows": max(
                        1, 500 // (len(components.where_clauses) + 1)
                    ),
                    "cost_estimate": 20.0,
                    "details": "External Sort - sorting result set in memory or disk",
                }
            )

        if components.limit_value:
            plan.append(
                {
                    "step": len(plan) + 1,
                    "operation": "Limit",
                    "table": "N/A",
                    "condition": f"LIMIT {components.limit_value}",
                    "estimated_rows": components.limit_value,
                    "cost_estimate": 0.5,
                    "details": "Limiting result to specified number of rows",
                }
            )

        if not has_where and not has_join and not has_order and not has_group:
            plan.append(
                {
                    "step": 2,
                    "operation": "Seq Scan",
                    "table": components.tables[0],
                    "condition": "No filter",
                    "estimated_rows": 10000,
                    "cost_estimate": 500.0,
                    "details": "Full table scan - reading all rows from table",
                }
            )

    total_cost = sum(step["cost_estimate"] for step in plan)
    plan.append(
        {
            "step": len(plan) + 1,
            "operation": "Total Cost",
            "table": "N/A",
            "condition": f"db_type: {db_type}",
            "estimated_rows": 0,
            "cost_estimate": round(total_cost, 2),
            "details": f"Estimated total query cost: {total_cost:.2f} (relative units)",
        }
    )

    return plan


def _estimate_improvement(issues: List[Dict], suggestions: List[Dict]) -> Dict:
    severity_weights = {
        "critical": 80,
        "high": 60,
        "medium": 40,
        "low": 20,
    }

    total_potential = 0
    for issue in issues:
        severity = issue.get("severity", "low")
        total_potential += severity_weights.get(severity, 20)

    for suggestion in suggestions:
        priority = suggestion.get("priority", "low")
        if priority == "high":
            total_potential += 30
        elif priority == "medium":
            total_potential += 20
        else:
            total_potential += 10

    max_improvement = min(95, max(10, total_potential // 2))

    critical_count = sum(1 for i in issues if i.get("severity") == "critical")
    high_count = sum(1 for i in issues if i.get("severity") == "high")

    if critical_count > 0:
        estimated = f"{max_improvement - 20}% - {max_improvement}%"
    elif high_count > 0:
        estimated = f"{max_improvement - 30}% - {max_improvement - 10}%"
    else:
        estimated = f"{max_improvement - 40}% - {max_improvement - 20}%"

    return {
        "potential_improvement": estimated,
        "estimated_speedup": f"{max_improvement / 100 + 1:.1f}x"
        if max_improvement > 0
        else "1.0x",
        "risk_level": "high"
        if critical_count > 0
        else "medium"
        if high_count > 0
        else "low",
        "priority_fixes": min(
            5, len([s for s in suggestions if s.get("priority") == "high"])
        ),
    }


def _calculate_complexity(components: QueryComponents) -> Dict:
    score = 0

    score += len(components.tables) * 5

    score += len(components.joins) * 10

    score += len(components.where_clauses) * 3

    score += len(components.order_by) * 2

    score += len(components.group_by) * 4

    score += len(components.subqueries) * 15

    score += len(components.columns) if components.columns else 0

    if not components.where_clauses:
        score += 10

    if len(components.order_by) > 3:
        score += 10

    if score < 20:
        complexity = "simple"
    elif score < 50:
        complexity = "moderate"
    elif score < 80:
        complexity = "complex"
    else:
        complexity = "very_complex"

    return {
        "score": score,
        "level": complexity,
        "description": _get_complexity_description(complexity),
    }


def _get_complexity_description(complexity: str) -> str:
    descriptions = {
        "simple": "Query is straightforward with minimal performance concerns",
        "moderate": "Query has some complexity but should perform reasonably",
        "complex": "Query is complex - consider optimization and indexing",
        "very_complex": "Query is very complex - significant performance issues likely",
    }
    return descriptions.get(complexity, "Unknown complexity")


def _singularize(word: str) -> str:
    """Convert plural word to singular form."""
    if word.endswith("ies"):
        return word[:-3] + "y"
    elif word.endswith("es"):
        return word[:-2]
    elif word.endswith("s") and len(word) > 1:
        return word[:-1]
    return word


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation.

    Expected payload format:
    {
        "query": "SELECT * FROM users WHERE...",
        "options": {
            "db_type": "PostgreSQL" | "MySQL" | "SQLite",
            "analyze_indexes": true,
            "detect_n_plus_one": true,
            "check_full_scans": true,
        },
        "generate_report": false  // optional, generates text report
    }
    """
    query = payload.get("query", "")

    if not query:
        return {"status": "error", "error": "No query provided"}

    options = payload.get("options", {})
    result = query_optimizer(query, options)

    if payload.get("generate_report", False):
        result["report"] = generate_report(result)

    return {"result": result}


def generate_report(analysis: dict) -> str:
    """Generate human-readable query optimization report."""
    lines = []
    lines.append("=" * 60)
    lines.append("QUERY OPTIMIZATION REPORT")
    lines.append("=" * 60)
    lines.append(f"Database Type: {analysis.get('db_type', 'Unknown')}")
    lines.append(f"Query Type: {analysis.get('query_type', 'Unknown')}")
    lines.append(f"Tables: {', '.join(analysis.get('tables', []))}")
    complexity = analysis.get("complexity_score", {})
    lines.append(
        f"Complexity: {complexity.get('level', 'unknown')} (score: {complexity.get('score', 0)})"
    )
    lines.append("")

    issues = analysis.get("issues", [])
    if issues:
        lines.append("DETECTED ISSUES:")
        lines.append("-" * 40)
        for i, issue in enumerate(issues[:10], 1):
            lines.append(
                f"{i}. [{issue.get('severity', 'unknown').upper()}] {issue.get('category', 'Unknown')}"
            )
            lines.append(f"   {issue.get('description', '')}")
            lines.append(f"   Location: {issue.get('location', 'N/A')}")
            lines.append(f"   Fix: {issue.get('recommendation', 'N/A')}")
            lines.append("")

    suggestions = analysis.get("suggestions", [])
    if suggestions:
        lines.append("OPTIMIZATION SUGGESTIONS:")
        lines.append("-" * 40)
        for i, suggestion in enumerate(suggestions[:5], 1):
            lines.append(
                f"{i}. [{suggestion.get('priority', 'low').upper()}] {suggestion.get('category', 'Unknown')}"
            )
            lines.append(f"   {suggestion.get('description', '')}")
            lines.append(f"   Example: {suggestion.get('sql_example', 'N/A')[:80]}...")
            lines.append(
                f"   Expected: {suggestion.get('expected_improvement', 'N/A')}"
            )
            lines.append("")

    execution_plan = analysis.get("execution_plan", [])
    if execution_plan:
        lines.append("EXECUTION PLAN:")
        lines.append("-" * 40)
        for step in execution_plan[:-1]:
            lines.append(f"  {step.get('step', '')}. {step.get('operation', '')}")
            lines.append(f"     Table: {step.get('table', 'N/A')}")
            lines.append(f"     Cost: {step.get('cost_estimate', 0)}")
        lines.append("")

    improvement = analysis.get("estimated_improvement", {})
    if improvement:
        lines.append("ESTIMATED IMPROVEMENT:")
        lines.append("-" * 40)
        lines.append(f"  Potential: {improvement.get('potential_improvement', 'N/A')}")
        lines.append(f"  Speedup: {improvement.get('estimated_speedup', 'N/A')}")
        lines.append(f"  Risk Level: {improvement.get('risk_level', 'unknown')}")

    return "\n".join(lines)


def register_skill():
    """Return skill metadata for MCP registration."""
    return {
        "name": "query-optimizer",
        "description": "Analyze and optimize SQL queries - detects N+1 queries, missing indexes, full table scans, suggests improvements, generates execution plans, and estimates performance gains",
        "version": "1.0.0",
        "domain": "PERFORMANCE",
        "capabilities": [
            "Parse SQL query structure",
            "Detect N+1 query patterns",
            "Identify missing indexes",
            "Detect full table scans",
            "Find function usage that prevents index usage",
            "Suggest query restructuring",
            "Suggest index creation",
            "Generate simulated execution plans",
            "Estimate performance improvement",
            "Calculate query complexity",
        ],
        "options": {
            "db_type": "Database type (PostgreSQL, MySQL, SQLite)",
            "analyze_indexes": "Whether to analyze index usage (default: True)",
            "detect_n_plus_one": "Whether to detect N+1 patterns (default: True)",
            "check_full_scans": "Whether to check for full table scans (default: True)",
        },
    }


if __name__ == "__main__":
    test_queries = [
        "SELECT * FROM users WHERE id = 1",
        "SELECT u.name, o.total FROM users u LEFT JOIN orders o ON u.id = o.user_id WHERE o.status = 'pending'",
        "SELECT * FROM products WHERE name LIKE '%test%'",
        "SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE status = 'active')",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print("=" * 60)
        result = query_optimizer(query, {"db_type": "PostgreSQL"})
        print(json.dumps(result, indent=2))
