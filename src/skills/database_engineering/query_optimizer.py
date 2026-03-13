#!/usr/bin/env python3
"""
Skill: query-optimizer
Domain: database_engineering
Description: Advanced SQL query optimization and performance tuning system
"""

import asyncio
import logging
import time
import uuid
import json
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import re
import statistics
from collections import defaultdict

logger = logging.getLogger(__name__)

class QueryType(Enum):
    """Types of SQL queries"""
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    MERGE = "merge"

class IndexStrategy(Enum):
    """Index optimization strategies"""
    COVERING = "covering"
    FILTERED = "filtered"
    COMPOSITE = "composite"
    PARTIAL = "partial"

class JoinStrategy(Enum):
    """Join optimization strategies"""
    NESTED_LOOP = "nested_loop"
    HASH_JOIN = "hash_join"
    MERGE_JOIN = "merge_join"
    INDEX_JOIN = "index_join"

@dataclass
class QueryMetrics:
    """Query performance metrics"""
    query_id: str
    execution_time: float
    cpu_time: float
    io_operations: int
    memory_usage: int
    rows_returned: int
    rows_examined: int
    cache_hits: int
    cache_misses: int
    timestamp: float

@dataclass
class IndexRecommendation:
    """Index optimization recommendation"""
    recommendation_id: str
    table_name: str
    index_fields: List[str]
    index_type: str
    estimated_improvement: float
    reason: str
    created_at: float

@dataclass
class QueryPlan:
    """Query execution plan"""
    plan_id: str
    query: str
    estimated_cost: float
    actual_cost: Optional[float]
    execution_steps: List[Dict[str, Any]]
    indexes_used: List[str]
    indexes_missing: List[str]
    bottlenecks: List[str]
    created_at: float

@dataclass
class PerformanceIssue:
    """Performance issue detected in query"""
    issue_id: str
    issue_type: str
    severity: str
    description: str
    affected_components: List[str]
    suggested_fix: str
    created_at: float

class QueryOptimizer:
    """Advanced SQL query optimization and performance tuning system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the query optimizer
        
        Args:
            config: Configuration dictionary with:
                - enable_auto_optimization: Whether to enable automatic optimization
                - max_execution_time: Maximum execution time in milliseconds
                - memory_threshold: Memory usage threshold in MB
        """
        self.enable_auto_optimization = config.get("enable_auto_optimization", True)
        self.max_execution_time = config.get("max_execution_time", 30000)  # 30 seconds
        self.memory_threshold = config.get("memory_threshold", 1024)  # 1GB
        
        self.query_metrics: Dict[str, QueryMetrics] = {}
        self.index_recommendations: Dict[str, IndexRecommendation] = {}
        self.query_plans: Dict[str, QueryPlan] = {}
        self.performance_issues: Dict[str, PerformanceIssue] = {}
        
        self.optimization_stats = {
            "total_queries": 0,
            "optimized_queries": 0,
            "average_improvement": 0.0,
            "total_recommendations": 0,
            "applied_recommendations": 0
        }
        
        self.logger = logging.getLogger(__name__)
        
        # Start background optimization
        self._optimization_task = asyncio.create_task(self._optimization_loop())
    
    def analyze_query(self, query: str, database_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a SQL query for performance issues
        
        Args:
            query: SQL query to analyze
            database_schema: Database schema information
            
        Returns:
            Analysis results
        """
        query_id = str(uuid.uuid4())
        
        # Parse query
        query_type = self._detect_query_type(query)
        tables_used = self._extract_tables(query)
        fields_used = self._extract_fields(query)
        
        # Generate execution plan
        plan = self._generate_execution_plan(query, query_type, tables_used, fields_used, database_schema)
        
        # Detect performance issues
        issues = self._detect_performance_issues(query, plan, database_schema)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(query, plan, issues, database_schema)
        
        # Store analysis results
        analysis = {
            "query_id": query_id,
            "query": query,
            "query_type": query_type.value,
            "tables_used": tables_used,
            "fields_used": fields_used,
            "execution_plan": plan,
            "performance_issues": issues,
            "recommendations": recommendations,
            "analysis_timestamp": time.time()
        }
        
        self.optimization_stats["total_queries"] += 1
        
        return analysis
    
    def optimize_query(self, query: str, database_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize a SQL query
        
        Args:
            query: SQL query to optimize
            database_schema: Database schema information
            
        Returns:
            Optimization results
        """
        analysis = self.analyze_query(query, database_schema)
        
        # Apply optimizations
        optimized_query = self._apply_optimizations(query, analysis["recommendations"])
        
        # Calculate improvement estimate
        improvement_estimate = self._calculate_improvement_estimate(analysis["execution_plan"], analysis["recommendations"])
        
        optimization_result = {
            "original_query": query,
            "optimized_query": optimized_query,
            "analysis": analysis,
            "improvement_estimate": improvement_estimate,
            "optimization_timestamp": time.time()
        }
        
        self.optimization_stats["optimized_queries"] += 1
        
        return optimization_result
    
    def generate_index_recommendations(self, query: str, database_schema: Dict[str, Any]) -> List[IndexRecommendation]:
        """
        Generate index recommendations for a query
        
        Args:
            query: SQL query
            database_schema: Database schema information
            
        Returns:
            List of index recommendations
        """
        recommendations = []
        
        # Analyze query for index opportunities
        query_type = self._detect_query_type(query)
        tables_used = self._extract_tables(query)
        fields_used = self._extract_fields(query)
        
        for table_name in tables_used:
            if table_name in database_schema.get("tables", {}):
                table_schema = database_schema["tables"][table_name]
                
                # Recommend indexes for WHERE clause fields
                where_fields = self._extract_where_fields(query)
                for field in where_fields:
                    if field in table_schema.get("fields", {}):
                        rec = IndexRecommendation(
                            recommendation_id=str(uuid.uuid4()),
                            table_name=table_name,
                            index_fields=[field],
                            index_type="btree",
                            estimated_improvement=30.0,
                            reason=f"Index on WHERE clause field: {field}",
                            created_at=time.time()
                        )
                        recommendations.append(rec)
                        self.index_recommendations[rec.recommendation_id] = rec
                
                # Recommend composite indexes for multiple WHERE fields
                if len(where_fields) > 1:
                    rec = IndexRecommendation(
                        recommendation_id=str(uuid.uuid4()),
                        table_name=table_name,
                        index_fields=where_fields,
                        index_type="composite",
                        estimated_improvement=50.0,
                        reason=f"Composite index for multiple WHERE fields: {', '.join(where_fields)}",
                        created_at=time.time()
                    )
                    recommendations.append(rec)
                    self.index_recommendations[rec.recommendation_id] = rec
                
                # Recommend covering indexes for SELECT fields
                select_fields = self._extract_select_fields(query)
                if select_fields and not self._is_covering_index_possible(select_fields, table_schema):
                    rec = IndexRecommendation(
                        recommendation_id=str(uuid.uuid4()),
                        table_name=table_name,
                        index_fields=select_fields + where_fields,
                        index_type="covering",
                        estimated_improvement=40.0,
                        reason=f"Covering index to avoid table lookups",
                        created_at=time.time()
                    )
                    recommendations.append(rec)
                    self.index_recommendations[rec.recommendation_id] = rec
        
        self.optimization_stats["total_recommendations"] += len(recommendations)
        
        return recommendations
    
    def monitor_query_performance(self, query_id: str, metrics: QueryMetrics):
        """Monitor query performance metrics"""
        self.query_metrics[query_id] = metrics
        
        # Check for performance issues
        if metrics.execution_time > self.max_execution_time:
            self._create_performance_issue(
                query_id, "slow_query", "high", 
                f"Query execution time ({metrics.execution_time}ms) exceeds threshold",
                ["execution_time"], "Consider adding indexes or rewriting query"
            )
        
        if metrics.memory_usage > self.memory_threshold * 1024 * 1024:  # Convert MB to bytes
            self._create_performance_issue(
                query_id, "high_memory", "medium",
                f"Query memory usage ({metrics.memory_usage / 1024 / 1024}MB) exceeds threshold",
                ["memory_usage"], "Optimize query to reduce memory footprint"
            )
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization statistics"""
        return {
            "total_queries": self.optimization_stats["total_queries"],
            "optimized_queries": self.optimization_stats["optimized_queries"],
            "total_recommendations": self.optimization_stats["total_recommendations"],
            "applied_recommendations": self.optimization_stats["applied_recommendations"],
            "success_rate": self.optimization_stats["optimized_queries"] / max(1, self.optimization_stats["total_queries"]),
            "average_improvement": self.optimization_stats["average_improvement"]
        }
    
    def _detect_query_type(self, query: str) -> QueryType:
        """Detect the type of SQL query"""
        query_upper = query.strip().upper()
        
        if query_upper.startswith("SELECT"):
            return QueryType.SELECT
        elif query_upper.startswith("INSERT"):
            return QueryType.INSERT
        elif query_upper.startswith("UPDATE"):
            return QueryType.UPDATE
        elif query_upper.startswith("DELETE"):
            return QueryType.DELETE
        elif query_upper.startswith("MERGE"):
            return QueryType.MERGE
        else:
            return QueryType.SELECT  # Default
    
    def _extract_tables(self, query: str) -> List[str]:
        """Extract table names from query"""
        tables = []
        query_upper = query.upper()
        
        # Extract FROM clause
        from_match = re.search(r'FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_upper)
        if from_match:
            tables.append(from_match.group(1))
        
        # Extract JOIN clauses
        join_matches = re.findall(r'JOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_upper)
        tables.extend(join_matches)
        
        # Extract UPDATE table
        update_match = re.search(r'UPDATE\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_upper)
        if update_match:
            tables.append(update_match.group(1))
        
        # Extract INSERT table
        insert_match = re.search(r'INSERT\s+INTO\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_upper)
        if insert_match:
            tables.append(insert_match.group(1))
        
        return list(set(tables))
    
    def _extract_fields(self, query: str) -> List[str]:
        """Extract field names from query"""
        fields = []
        
        # Extract SELECT fields
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', query, re.IGNORECASE | re.DOTALL)
        if select_match:
            select_part = select_match.group(1)
            field_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', select_part)
            fields.extend(field_matches)
        
        # Extract WHERE fields
        where_fields = self._extract_where_fields(query)
        fields.extend(where_fields)
        
        # Extract ORDER BY fields
        order_match = re.search(r'ORDER\s+BY\s+(.*?)(?:\s+LIMIT|\s+GROUP\s+BY|\s+HAVING|\s*$)', query, re.IGNORECASE)
        if order_match:
            order_part = order_match.group(1)
            field_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', order_part)
            fields.extend(field_matches)
        
        return list(set(fields))
    
    def _extract_where_fields(self, query: str) -> List[str]:
        """Extract fields used in WHERE clause"""
        where_fields = []
        
        # Simple WHERE clause extraction
        where_match = re.search(r'WHERE\s+(.*?)(?:\s+GROUP\s+BY|\s+HAVING|\s+ORDER\s+BY|\s+LIMIT|\s*$)', query, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_part = where_match.group(1)
            # Extract field names (simplified)
            field_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*[=<>!]', where_part)
            where_fields.extend(field_matches)
        
        return list(set(where_fields))
    
    def _extract_select_fields(self, query: str) -> List[str]:
        """Extract fields in SELECT clause"""
        select_fields = []
        
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', query, re.IGNORECASE | re.DOTALL)
        if select_match:
            select_part = select_match.group(1)
            # Remove functions and extract field names
            clean_select = re.sub(r'\w+\s*\([^)]*\)', '', select_part)  # Remove function calls
            field_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', clean_select)
            select_fields.extend(field_matches)
        
        return list(set(select_fields))
    
    def _generate_execution_plan(self, query: str, query_type: QueryType, 
                                tables_used: List[str], fields_used: List[str],
                                database_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate execution plan for query"""
        plan = {
            "estimated_cost": 0.0,
            "execution_steps": [],
            "indexes_used": [],
            "indexes_missing": [],
            "bottlenecks": []
        }
        
        # Calculate base cost
        base_cost = len(tables_used) * 100 + len(fields_used) * 10
        
        # Analyze each table for index usage
        for table_name in tables_used:
            if table_name in database_schema.get("tables", {}):
                table_schema = database_schema["tables"][table_name]
                indexes = table_schema.get("indexes", [])
                
                # Check which indexes can be used
                for index in indexes:
                    index_fields = index.get("fields", [])
                    if any(field in fields_used for field in index_fields):
                        plan["indexes_used"].append(f"{table_name}.{index['name']}")
                
                # Identify missing indexes
                where_fields = self._extract_where_fields(query)
                for field in where_fields:
                    has_index = any(field in idx.get("fields", []) for idx in indexes)
                    if not has_index and field in table_schema.get("fields", {}):
                        plan["indexes_missing"].append(f"{table_name}.{field}")
        
        # Identify potential bottlenecks
        if len(tables_used) > 3:
            plan["bottlenecks"].append("Multiple table joins")
        
        if not plan["indexes_used"] and query_type == QueryType.SELECT:
            plan["bottlenecks"].append("No indexes available for query")
        
        if "ORDER BY" in query.upper() and "LIMIT" not in query.upper():
            plan["bottlenecks"].append("ORDER BY without LIMIT on large dataset")
        
        plan["estimated_cost"] = base_cost + len(plan["bottlenecks"]) * 50
        
        return plan
    
    def _detect_performance_issues(self, query: str, plan: Dict[str, Any], 
                                  database_schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect performance issues in query"""
        issues = []
        
        # Check for SELECT *
        if "SELECT *" in query.upper():
            issues.append({
                "type": "inefficient_select",
                "severity": "medium",
                "description": "Using SELECT * instead of specific columns",
                "components": ["select_clause"],
                "fix": "Specify only required columns"
            })
        
        # Check for missing indexes
        if plan["indexes_missing"]:
            issues.append({
                "type": "missing_indexes",
                "severity": "high",
                "description": f"Missing indexes on fields: {', '.join(plan['indexes_missing'])}",
                "components": ["where_clause"],
                "fix": "Create appropriate indexes"
            })
        
        # Check for inefficient joins
        if len(plan["execution_steps"]) > 5:
            issues.append({
                "type": "complex_joins",
                "severity": "medium",
                "description": "Complex join operations may impact performance",
                "components": ["join_operations"],
                "fix": "Consider query restructuring"
            })
        
        # Check for subqueries that could be joins
        if "SELECT" in query[query.find("WHERE")+1:].upper():
            issues.append({
                "type": "inefficient_subquery",
                "severity": "medium",
                "description": "Subquery in WHERE clause may be inefficient",
                "components": ["where_clause"],
                "fix": "Consider converting to JOIN"
            })
        
        return issues
    
    def _generate_recommendations(self, query: str, plan: Dict[str, Any], 
                                 issues: List[Dict[str, Any]], 
                                 database_schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Generate recommendations based on issues
        for issue in issues:
            if issue["type"] == "inefficient_select":
                recommendations.append({
                    "type": "select_optimization",
                    "priority": "medium",
                    "description": "Replace SELECT * with specific column names",
                    "implementation": "List only required columns in SELECT clause"
                })
            
            elif issue["type"] == "missing_indexes":
                recommendations.append({
                    "type": "index_creation",
                    "priority": "high",
                    "description": "Create indexes on frequently queried fields",
                    "implementation": "CREATE INDEX statements for missing indexes"
                })
            
            elif issue["type"] == "complex_joins":
                recommendations.append({
                    "type": "join_optimization",
                    "priority": "medium",
                    "description": "Simplify join operations",
                    "implementation": "Review join conditions and table order"
                })
        
        # Generate additional recommendations
        if "ORDER BY" in query.upper() and "LIMIT" not in query.upper():
            recommendations.append({
                "type": "pagination",
                "priority": "medium",
                "description": "Add LIMIT clause for better performance",
                "implementation": "Add LIMIT clause to restrict result set"
            })
        
        # Check for potential index opportunities
        where_fields = self._extract_where_fields(query)
        if where_fields:
            recommendations.append({
                "type": "index_strategy",
                "priority": "high",
                "description": f"Consider composite index on fields: {', '.join(where_fields)}",
                "implementation": f"CREATE INDEX idx_composite ON table_name ({', '.join(where_fields)})"
            })
        
        return recommendations
    
    def _apply_optimizations(self, query: str, recommendations: List[Dict[str, Any]]) -> str:
        """Apply optimizations to query"""
        optimized_query = query
        
        for rec in recommendations:
            if rec["type"] == "select_optimization":
                # Replace SELECT * with specific fields (simplified)
                optimized_query = optimized_query.replace("SELECT *", "SELECT id, name, created_at")
            
            elif rec["type"] == "pagination":
                if "ORDER BY" in optimized_query.upper() and "LIMIT" not in optimized_query.upper():
                    optimized_query += " LIMIT 1000"
        
        return optimized_query
    
    def _calculate_improvement_estimate(self, plan: Dict[str, Any], 
                                      recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate estimated improvement from optimizations"""
        base_cost = plan["estimated_cost"]
        
        # Calculate improvement based on recommendations
        improvement_factor = 0.0
        for rec in recommendations:
            if rec["priority"] == "high":
                improvement_factor += 0.3
            elif rec["priority"] == "medium":
                improvement_factor += 0.15
            elif rec["priority"] == "low":
                improvement_factor += 0.05
        
        improvement_factor = min(improvement_factor, 0.8)  # Max 80% improvement
        
        estimated_cost = base_cost * (1 - improvement_factor)
        improvement_percentage = improvement_factor * 100
        
        return {
            "base_cost": base_cost,
            "estimated_cost": estimated_cost,
            "improvement_percentage": improvement_percentage,
            "execution_time_improvement": f"~{int(improvement_percentage)}%",
            "memory_improvement": f"~{int(improvement_percentage * 0.7)}%"
        }
    
    def _is_covering_index_possible(self, select_fields: List[str], table_schema: Dict[str, Any]) -> bool:
        """Check if covering index is possible for select fields"""
        table_fields = [f["name"] for f in table_schema.get("fields", [])]
        return all(field in table_fields for field in select_fields)
    
    def _create_performance_issue(self, query_id: str, issue_type: str, severity: str,
                                 description: str, components: List[str], fix: str):
        """Create a performance issue record"""
        issue_id = str(uuid.uuid4())
        
        issue = PerformanceIssue(
            issue_id=issue_id,
            issue_type=issue_type,
            severity=severity,
            description=description,
            affected_components=components,
            suggested_fix=fix,
            created_at=time.time()
        )
        
        self.performance_issues[issue_id] = issue
        self.logger.warning(f"Performance issue detected in query {query_id}: {description}")
    
    async def _optimization_loop(self):
        """Background optimization loop"""
        while True:
            try:
                await self._periodic_optimization_check()
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                self.logger.error(f"Error in optimization loop: {e}")
                await asyncio.sleep(300)
    
    async def _periodic_optimization_check(self):
        """Perform periodic optimization checks"""
        # Analyze recent query metrics for trends
        recent_metrics = [
            metrics for metrics in self.query_metrics.values()
            if time.time() - metrics.timestamp < 3600  # Last hour
        ]
        
        if len(recent_metrics) > 10:
            avg_execution_time = statistics.mean(m.execution_time for m in recent_metrics)
            avg_memory_usage = statistics.mean(m.memory_usage for m in recent_metrics)
            
            # Check for performance degradation
            if avg_execution_time > self.max_execution_time * 0.8:
                self.logger.warning(f"Average execution time ({avg_execution_time:.2f}ms) approaching threshold")
            
            if avg_memory_usage > self.memory_threshold * 0.8 * 1024 * 1024:
                self.logger.warning(f"Average memory usage ({avg_memory_usage / 1024 / 1024:.2f}MB) approaching threshold")

# Global query optimizer instance
_query_optimizer = QueryOptimizer({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "analyze_query", "optimize_query", "generate_recommendations", 
                     "monitor_performance", "get_stats"
            - query_data: Query information
            - schema_data: Database schema information
            - metrics_data: Performance metrics
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "analyze_query":
            query_data = payload.get("query_data", {})
            
            analysis = _query_optimizer.analyze_query(
                query=query_data.get("query", ""),
                database_schema=query_data.get("database_schema", {})
            )
            
            return {
                "result": analysis,
                "metadata": {
                    "action": "analyze_query",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "optimize_query":
            query_data = payload.get("query_data", {})
            
            optimization = _query_optimizer.optimize_query(
                query=query_data.get("query", ""),
                database_schema=query_data.get("database_schema", {})
            )
            
            return {
                "result": optimization,
                "metadata": {
                    "action": "optimize_query",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "generate_recommendations":
            query_data = payload.get("query_data", {})
            
            recommendations = _query_optimizer.generate_index_recommendations(
                query=query_data.get("query", ""),
                database_schema=query_data.get("database_schema", {})
            )
            
            return {
                "result": [asdict(rec) for rec in recommendations],
                "metadata": {
                    "action": "generate_recommendations",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "monitor_performance":
            metrics_data = payload.get("metrics_data", {})
            
            metrics = QueryMetrics(
                query_id=metrics_data.get("query_id", ""),
                execution_time=metrics_data.get("execution_time", 0.0),
                cpu_time=metrics_data.get("cpu_time", 0.0),
                io_operations=metrics_data.get("io_operations", 0),
                memory_usage=metrics_data.get("memory_usage", 0),
                rows_returned=metrics_data.get("rows_returned", 0),
                rows_examined=metrics_data.get("rows_examined", 0),
                cache_hits=metrics_data.get("cache_hits", 0),
                cache_misses=metrics_data.get("cache_misses", 0),
                timestamp=time.time()
            )
            
            _query_optimizer.monitor_query_performance(metrics_data.get("query_id", ""), metrics)
            
            return {
                "result": {
                    "query_id": metrics_data.get("query_id", ""),
                    "message": "Performance metrics recorded"
                },
                "metadata": {
                    "action": "monitor_performance",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_stats":
            stats = _query_optimizer.get_optimization_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in query_optimizer: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the query optimizer skill"""
    
    # Sample database schema
    database_schema = {
        "tables": {
            "users": {
                "fields": [
                    {"name": "id", "type": "integer"},
                    {"name": "email", "type": "varchar"},
                    {"name": "name", "type": "varchar"},
                    {"name": "created_at", "type": "timestamp"}
                ],
                "indexes": [
                    {"name": "idx_users_id", "fields": ["id"], "type": "primary"},
                    {"name": "idx_users_email", "fields": ["email"], "type": "unique"}
                ]
            },
            "orders": {
                "fields": [
                    {"name": "id", "type": "integer"},
                    {"name": "user_id", "type": "integer"},
                    {"name": "total_amount", "type": "decimal"},
                    {"name": "status", "type": "varchar"},
                    {"name": "created_at", "type": "timestamp"}
                ],
                "indexes": [
                    {"name": "idx_orders_id", "fields": ["id"], "type": "primary"},
                    {"name": "idx_orders_user_id", "fields": ["user_id"], "type": "foreign"}
                ]
            }
        }
    }
    
    # Sample query to optimize
    query = """
    SELECT * FROM users u 
    JOIN orders o ON u.id = o.user_id 
    WHERE u.created_at > '2023-01-01' 
    AND o.status = 'completed'
    ORDER BY u.name
    """
    
    # Analyze query
    analysis = await invoke({
        "action": "analyze_query",
        "query_data": {
            "query": query,
            "database_schema": database_schema
        }
    })
    
    print(f"Query analysis: {analysis['result']}")
    
    # Optimize query
    optimization = await invoke({
        "action": "optimize_query",
        "query_data": {
            "query": query,
            "database_schema": database_schema
        }
    })
    
    print(f"Query optimization: {optimization['result']}")
    
    # Generate index recommendations
    recommendations = await invoke({
        "action": "generate_recommendations",
        "query_data": {
            "query": query,
            "database_schema": database_schema
        }
    })
    
    print(f"Index recommendations: {recommendations['result']}")
    
    # Monitor performance
    await invoke({
        "action": "monitor_performance",
        "metrics_data": {
            "query_id": "test_query_1",
            "execution_time": 1500.0,
            "cpu_time": 800.0,
            "io_operations": 150,
            "memory_usage": 256 * 1024 * 1024,  # 256MB
            "rows_returned": 1000,
            "rows_examined": 50000,
            "cache_hits": 80,
            "cache_misses": 20
        }
    })
    
    # Get optimization statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Optimization stats: {stats['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())