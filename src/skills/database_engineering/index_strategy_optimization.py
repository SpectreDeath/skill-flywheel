import logging
import re
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def analyze_query_workload(queries: List[str]) -> Dict[str, Any]:
    access_patterns = {"equality": 0, "range": 0, "sort": 0, "join": 0, "full_text": 0}

    for query in queries:
        query_lower = query.lower()

        if "=" in query or "in (" in query_lower:
            access_patterns["equality"] += 1

        if any(op in query_lower for op in [">", "<", "between", "like"]):
            access_patterns["range"] += 1

        if "order by" in query_lower:
            access_patterns["sort"] += 1

        if "join" in query_lower:
            access_patterns["join"] += 1

        if "match" in query_lower or "fulltext" in query_lower:
            access_patterns["full_text"] += 1

    return access_patterns


def recommend_index_type(
    column: Dict[str, Any], access_patterns: Dict[str, Any]
) -> str:
    col_type = column.get("type", "").lower()
    cardinality = column.get("cardinality", "medium")

    if access_patterns.get("full_text", 0) > 0:
        return "GIN"

    if "timestamp" in col_type or "date" in col_type:
        if cardinality == "low":
            return "BRIN"
        return "B-tree"

    if "boolean" in col_type:
        return "B-tree"

    if "array" in col_type:
        return "GIN"

    if "json" in col_type or "jsonb" in col_type:
        return "GIN"

    return "B-tree"


def generate_index_strategy(
    schema: Dict[str, Any], queries: List[str]
) -> Dict[str, Any]:
    access_patterns = analyze_query_workload(queries)

    tables = schema.get("tables", [])
    indexes = []

    for table in tables:
        table_name = table.get("name", "unknown")
        columns = table.get("columns", [])

        for column in columns:
            col_name = column.get("name", "unknown")
            is_fk = column.get("foreign_key", False)

            if is_fk:
                indexes.append(
                    {
                        "table": table_name,
                        "columns": [col_name],
                        "index_type": "B-tree",
                        "reason": "Foreign key column - frequently joined",
                        "priority": "high",
                    }
                )

            for query in queries:
                query_lower = query.lower()
                if (
                    f"where {col_name}." in query_lower
                    or f"where {col_name}" in query_lower
                ):
                    index_type = recommend_index_type(column, access_patterns)
                    existing = False
                    for idx in indexes:
                        if idx["table"] == table_name and col_name in idx["columns"]:
                            existing = True
                            break

                    if not existing:
                        indexes.append(
                            {
                                "table": table_name,
                                "columns": [col_name],
                                "index_type": index_type,
                                "reason": "Used in WHERE clause",
                                "priority": "high"
                                if access_patterns.get("equality", 0)
                                > access_patterns.get("range", 0)
                                else "medium",
                            }
                        )

                if f"order by {col_name}" in query_lower:
                    existing = False
                    for idx in indexes:
                        if idx["table"] == table_name and col_name in idx["columns"]:
                            existing = True
                            break

                    if not existing:
                        indexes.append(
                            {
                                "table": table_name,
                                "columns": [col_name],
                                "index_type": "B-tree",
                                "reason": "Used in ORDER BY clause",
                                "priority": "medium",
                            }
                        )

    composite_indexes = []
    covered_queries = []

    for query in queries:
        query_lower = query.lower()
        where_cols = re.findall(r"where\s+(\w+)", query_lower)

        if len(where_cols) >= 2:
            table_match = re.search(r"from\s+(\w+)", query_lower)
            if table_match:
                composite_indexes.append(
                    {
                        "table": table_match.group(1),
                        "columns": where_cols,
                        "index_type": "B-tree",
                        "reason": "Composite index for query optimization",
                        "priority": "high",
                    }
                )
                covered_queries.append(query[:50])

    return {
        "single_column_indexes": indexes,
        "composite_indexes": composite_indexes,
        "total_indexes": len(indexes) + len(composite_indexes),
        "access_patterns": access_patterns,
        "recommendations": [
            "Create composite indexes for frequently queried column combinations",
            "Consider covering indexes for queries with high selectivity",
            "Monitor index usage and remove unused indexes",
        ],
    }


def analyze_existing_indexes(indexes: List[Dict[str, Any]]) -> Dict[str, Any]:
    size_mb = sum(idx.get("size_mb", 0) for idx in indexes)

    unused = [idx for idx in indexes if idx.get("usage_count", 1) == 0]
    rarely_used = [idx for idx in indexes if 0 < idx.get("usage_count", 1) < 10]
    heavily_used = [idx for idx in indexes if idx.get("usage_count", 1) > 1000]

    return {
        "total_indexes": len(indexes),
        "total_size_mb": size_mb,
        "unused_indexes": [idx["name"] for idx in unused],
        "rarely_used_indexes": [idx["name"] for idx in rarely_used],
        "heavily_used_indexes": [idx["name"] for idx in heavily_used],
        "recommendations": [
            "Drop unused indexes to reduce write overhead",
            "Review rarely used indexes for potential consolidation",
            "Consider partial indexes for partition-specific data",
        ]
        if unused
        else ["All indexes are being used"],
        "maintenance_needed": len(unused) > 0,
    }


def estimate_index_impact(
    indexes: List[Dict[str, Any]], table_stats: Dict[str, Any]
) -> Dict[str, Any]:
    write_overhead = len(indexes) * 5

    read_improvement = 0
    for idx in indexes:
        if idx.get("priority") == "high":
            read_improvement += 30
        else:
            read_improvement += 15

    storage_mb = sum(idx.get("size_mb", 10) for idx in indexes)

    return {
        "estimated_write_overhead_percent": write_overhead,
        "estimated_read_improvement_percent": min(read_improvement, 95),
        "estimated_storage_mb": storage_mb,
        "net_benefit": "positive" if read_improvement > write_overhead else "negative",
        "recommendation": "Create indexes"
        if read_improvement > write_overhead
        else "Review index necessity",
    }


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    action = payload.get("action", "strategy")

    try:
        if action == "strategy":
            schema = payload.get("schema", {})
            queries = payload.get("queries", [])
            strategy = generate_index_strategy(schema, queries)

            return {
                "result": strategy,
                "metadata": {
                    "action": "strategy",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "analyze_workload":
            queries = payload.get("queries", [])
            result = analyze_query_workload(queries)
            return {
                "result": result,
                "metadata": {
                    "action": "analyze_workload",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "recommend_type":
            column = payload.get("column", {})
            access_patterns = payload.get("access_patterns", {})
            index_type = recommend_index_type(column, access_patterns)
            return {
                "result": {"recommended_index_type": index_type},
                "metadata": {
                    "action": "recommend_type",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "analyze_existing":
            indexes = payload.get("indexes", [])
            result = analyze_existing_indexes(indexes)
            return {
                "result": result,
                "metadata": {
                    "action": "analyze_existing",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "estimate_impact":
            indexes = payload.get("indexes", [])
            table_stats = payload.get("table_stats", {})
            result = estimate_index_impact(indexes, table_stats)
            return {
                "result": result,
                "metadata": {
                    "action": "estimate_impact",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in index_strategy_optimization: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }
