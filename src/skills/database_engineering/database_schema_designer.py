#!/usr/bin/env python3
"""
Skill: database-schema-designer
Domain: database_engineering
Description: Database schema design and optimization system for relational databases
"""

import asyncio
import logging
import re
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class DatabaseType(Enum):
    """Types of databases"""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"
    ELASTICSEARCH = "elasticsearch"

class IndexType(Enum):
    """Types of database indexes"""
    BTREE = "btree"
    HASH = "hash"
    GIN = "gin"
    GIST = "gist"
    BRIN = "brin"

class ConstraintType(Enum):
    """Types of database constraints"""
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"
    UNIQUE = "unique"
    CHECK = "check"
    NOT_NULL = "not_null"

class NormalizationLevel(Enum):
    """Database normalization levels"""
    FIRST_NORMAL = "1nf"
    SECOND_NORMAL = "2nf"
    THIRD_NORMAL = "3nf"
    BOYCE_CODD = "bcnf"
    FOURTH_NORMAL = "4nf"
    FIFTH_NORMAL = "5nf"

@dataclass
class DatabaseField:
    """Represents a database field"""
    field_id: str
    name: str
    data_type: str
    length: Optional[int]
    precision: Optional[int]
    scale: Optional[int]
    nullable: bool
    default_value: Optional[str]
    auto_increment: bool
    description: str
    created_at: float

@dataclass
class DatabaseTable:
    """Represents a database table"""
    table_id: str
    name: str
    schema_name: str
    fields: List[DatabaseField]
    indexes: List[Dict[str, Any]]
    constraints: List[Dict[str, Any]]
    description: str
    created_at: float

@dataclass
class DatabaseRelationship:
    """Represents a relationship between tables"""
    relationship_id: str
    source_table: str
    source_field: str
    target_table: str
    target_field: str
    relationship_type: str  # one-to-one, one-to-many, many-to-many
    cardinality: str
    created_at: float

@dataclass
class DatabaseSchema:
    """Represents a complete database schema"""
    schema_id: str
    name: str
    database_type: DatabaseType
    tables: List[DatabaseTable]
    relationships: List[DatabaseRelationship]
    version: str
    description: str
    created_at: float
    last_modified: float

@dataclass
class QueryPlan:
    """Represents a query execution plan"""
    plan_id: str
    query: str
    estimated_cost: float
    actual_cost: Optional[float]
    execution_time: Optional[float]
    indexes_used: List[str]
    bottlenecks: List[str]
    recommendations: List[str]
    analyzed_at: float

class DatabaseSchemaDesigner:
    """Database schema design and optimization system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the database schema designer
        
        Args:
            config: Configuration dictionary with:
                - default_database_type: Default database type
                - max_table_fields: Maximum fields per table
                - enable_normalization: Whether to enforce normalization
        """
        self.default_database_type = config.get("default_database_type", "postgresql")
        self.max_table_fields = config.get("max_table_fields", 50)
        self.enable_normalization = config.get("enable_normalization", True)
        
        self.schemas: Dict[str, DatabaseSchema] = {}
        self.query_plans: Dict[str, QueryPlan] = {}
        
        self.design_stats = {
            "total_schemas": 0,
            "total_tables": 0,
            "total_relationships": 0,
            "normalized_schemas": 0,
            "optimized_queries": 0
        }
        
        self.logger = logging.getLogger(__name__)
    
    def create_schema(self,
                     name: str,
                     database_type: DatabaseType,
                     description: str = "") -> str:
        """
        Create a new database schema
        
        Args:
            name: Schema name
            database_type: Type of database
            description: Schema description
            
        Returns:
            Schema ID
        """
        schema_id = str(uuid.uuid4())
        
        schema = DatabaseSchema(
            schema_id=schema_id,
            name=name,
            database_type=database_type,
            tables=[],
            relationships=[],
            version="1.0.0",
            description=description,
            created_at=time.time(),
            last_modified=time.time()
        )
        
        self.schemas[schema_id] = schema
        self.design_stats["total_schemas"] += 1
        
        self.logger.info(f"Created database schema: {schema_id}")
        return schema_id
    
    def add_table(self,
                 schema_id: str,
                 name: str,
                 fields: List[Dict[str, Any]],
                 description: str = "") -> str:
        """
        Add a table to a schema
        
        Args:
            schema_id: Schema ID
            name: Table name
            fields: List of field configurations
            description: Table description
            
        Returns:
            Table ID
        """
        if schema_id not in self.schemas:
            raise ValueError(f"Schema {schema_id} not found")
        
        if len(fields) > self.max_table_fields:
            raise ValueError(f"Table cannot have more than {self.max_table_fields} fields")
        
        schema = self.schemas[schema_id]
        
        # Create fields
        table_fields = []
        for field_config in fields:
            field_id = str(uuid.uuid4())
            
            field = DatabaseField(
                field_id=field_id,
                name=field_config.get("name", ""),
                data_type=field_config.get("data_type", "varchar"),
                length=field_config.get("length"),
                precision=field_config.get("precision"),
                scale=field_config.get("scale"),
                nullable=field_config.get("nullable", True),
                default_value=field_config.get("default_value"),
                auto_increment=field_config.get("auto_increment", False),
                description=field_config.get("description", ""),
                created_at=time.time()
            )
            
            table_fields.append(field)
        
        # Create indexes and constraints
        indexes = self._generate_indexes(table_fields)
        constraints = self._generate_constraints(table_fields)
        
        table = DatabaseTable(
            table_id=str(uuid.uuid4()),
            name=name,
            schema_name=schema.name,
            fields=table_fields,
            indexes=indexes,
            constraints=constraints,
            description=description,
            created_at=time.time()
        )
        
        schema.tables.append(table)
        schema.last_modified = time.time()
        self.design_stats["total_tables"] += 1
        
        self.logger.info(f"Added table {name} to schema {schema_id}")
        return table.table_id
    
    def add_relationship(self,
                        schema_id: str,
                        source_table: str,
                        source_field: str,
                        target_table: str,
                        target_field: str,
                        relationship_type: str) -> str:
        """
        Add a relationship between tables
        
        Args:
            schema_id: Schema ID
            source_table: Source table name
            source_field: Source field name
            target_table: Target table name
            target_field: Target field name
            relationship_type: Type of relationship
            
        Returns:
            Relationship ID
        """
        if schema_id not in self.schemas:
            raise ValueError(f"Schema {schema_id} not found")
        
        schema = self.schemas[schema_id]
        
        # Validate tables exist
        source_table_obj = next((t for t in schema.tables if t.name == source_table), None)
        target_table_obj = next((t for t in schema.tables if t.name == target_table), None)
        
        if not source_table_obj:
            raise ValueError(f"Source table {source_table} not found")
        if not target_table_obj:
            raise ValueError(f"Target table {target_table} not found")
        
        # Validate fields exist
        source_field_obj = next((f for f in source_table_obj.fields if f.name == source_field), None)
        target_field_obj = next((f for f in target_table_obj.fields if f.name == target_field), None)
        
        if not source_field_obj:
            raise ValueError(f"Source field {source_field} not found in {source_table}")
        if not target_field_obj:
            raise ValueError(f"Target field {target_field} not found in {target_table}")
        
        relationship_id = str(uuid.uuid4())
        
        relationship = DatabaseRelationship(
            relationship_id=relationship_id,
            source_table=source_table,
            source_field=source_field,
            target_table=target_table,
            target_field=target_field,
            relationship_type=relationship_type,
            cardinality=self._determine_cardinality(relationship_type),
            created_at=time.time()
        )
        
        schema.relationships.append(relationship)
        schema.last_modified = time.time()
        self.design_stats["total_relationships"] += 1
        
        self.logger.info(f"Added relationship {relationship_id} between {source_table}.{source_field} and {target_table}.{target_field}")
        return relationship_id
    
    def analyze_schema(self, schema_id: str) -> Dict[str, Any]:
        """
        Analyze a schema for design issues and optimization opportunities
        
        Args:
            schema_id: Schema ID
            
        Returns:
            Analysis results
        """
        if schema_id not in self.schemas:
            raise ValueError(f"Schema {schema_id} not found")
        
        schema = self.schemas[schema_id]
        
        issues = []
        recommendations = []
        
        # Check for normalization violations
        if self.enable_normalization:
            normalization_issues = self._check_normalization(schema)
            issues.extend(normalization_issues)
        
        # Check for indexing issues
        indexing_issues = self._check_indexing(schema)
        issues.extend(indexing_issues)
        
        # Check for relationship issues
        relationship_issues = self._check_relationships(schema)
        issues.extend(relationship_issues)
        
        # Check for field design issues
        field_issues = self._check_field_design(schema)
        issues.extend(field_issues)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(schema, issues)
        
        return {
            "schema_id": schema_id,
            "schema_name": schema.name,
            "database_type": schema.database_type.value,
            "total_tables": len(schema.tables),
            "total_relationships": len(schema.relationships),
            "issues": issues,
            "recommendations": recommendations,
            "normalization_level": self._assess_normalization(schema),
            "complexity_score": self._calculate_complexity_score(schema),
            "analyzed_at": time.time()
        }
    
    def optimize_query(self, schema_id: str, query: str) -> Dict[str, Any]:
        """
        Optimize a SQL query for the given schema
        
        Args:
            schema_id: Schema ID
            query: SQL query to optimize
            
        Returns:
            Optimization results
        """
        if schema_id not in self.schemas:
            raise ValueError(f"Schema {schema_id} not found")
        
        schema = self.schemas[schema_id]
        
        # Parse query to identify tables and fields
        tables_used = self._extract_tables_from_query(query)
        fields_used = self._extract_fields_from_query(query)
        
        # Generate execution plan
        plan = self._generate_execution_plan(query, schema, tables_used, fields_used)
        
        # Generate optimization recommendations
        optimizations = self._generate_query_optimizations(query, schema, plan)
        
        plan_id = str(uuid.uuid4())
        query_plan = QueryPlan(
            plan_id=plan_id,
            query=query,
            estimated_cost=plan.get("estimated_cost", 0.0),
            actual_cost=None,
            execution_time=None,
            indexes_used=plan.get("indexes_used", []),
            bottlenecks=plan.get("bottlenecks", []),
            recommendations=optimizations,
            analyzed_at=time.time()
        )
        
        self.query_plans[plan_id] = query_plan
        self.design_stats["optimized_queries"] += 1
        
        return {
            "plan_id": plan_id,
            "original_query": query,
            "optimized_query": self._apply_optimizations(query, optimizations),
            "execution_plan": plan,
            "optimizations": optimizations,
            "estimated_improvement": self._calculate_improvement(plan, optimizations),
            "optimized_at": time.time()
        }
    
    def generate_ddl(self, schema_id: str) -> Dict[str, str]:
        """
        Generate DDL statements for the schema
        
        Args:
            schema_id: Schema ID
            
        Returns:
            DDL statements by object type
        """
        if schema_id not in self.schemas:
            raise ValueError(f"Schema {schema_id} not found")
        
        schema = self.schemas[schema_id]
        
        ddl_statements = {
            "schema": [],
            "tables": [],
            "indexes": [],
            "constraints": [],
            "relationships": []
        }
        
        # Generate schema statement
        if schema.database_type == DatabaseType.POSTGRESQL:
            ddl_statements["schema"].append(f"CREATE SCHEMA IF NOT EXISTS {schema.name};")
        elif schema.database_type == DatabaseType.MYSQL:
            ddl_statements["schema"].append(f"CREATE DATABASE IF NOT EXISTS {schema.name};")
        
        # Generate table statements
        for table in schema.tables:
            table_ddl = self._generate_table_ddl(table, schema.database_type)
            ddl_statements["tables"].append(table_ddl)
            
            # Generate index statements
            for index in table.indexes:
                index_ddl = self._generate_index_ddl(index, table.name, schema.database_type)
                ddl_statements["indexes"].append(index_ddl)
            
            # Generate constraint statements
            for constraint in table.constraints:
                constraint_ddl = self._generate_constraint_ddl(constraint, table.name, schema.database_type)
                ddl_statements["constraints"].append(constraint_ddl)
        
        # Generate relationship statements (foreign keys)
        for relationship in schema.relationships:
            fk_ddl = self._generate_foreign_key_ddl(relationship, schema.database_type)
            ddl_statements["relationships"].append(fk_ddl)
        
        return ddl_statements
    
    def get_design_stats(self) -> Dict[str, Any]:
        """Get schema design statistics"""
        return {
            "total_schemas": self.design_stats["total_schemas"],
            "total_tables": self.design_stats["total_tables"],
            "total_relationships": self.design_stats["total_relationships"],
            "normalized_schemas": self.design_stats["normalized_schemas"],
            "optimized_queries": self.design_stats["optimized_queries"],
            "average_tables_per_schema": self.design_stats["total_tables"] / max(1, self.design_stats["total_schemas"]),
            "average_relationships_per_schema": self.design_stats["total_relationships"] / max(1, self.design_stats["total_schemas"])
        }
    
    def _generate_indexes(self, fields: List[DatabaseField]) -> List[Dict[str, Any]]:
        """Generate appropriate indexes for fields"""
        indexes = []
        
        for field in fields:
            # Primary key index
            if any(c.get("type") == "primary_key" for c in field.__dict__.get("constraints", [])):
                indexes.append({
                    "name": f"idx_{field.name}_pk",
                    "fields": [field.name],
                    "type": IndexType.BTREE.value,
                    "unique": True
                })
            
            # Foreign key index
            elif field.name.endswith("_id"):
                indexes.append({
                    "name": f"idx_{field.name}_fk",
                    "fields": [field.name],
                    "type": IndexType.BTREE.value,
                    "unique": False
                })
            
            # Text search index for text fields
            elif field.data_type in ["text", "varchar", "char"]:
                indexes.append({
                    "name": f"idx_{field.name}_text",
                    "fields": [field.name],
                    "type": IndexType.GIN.value if field.data_type == "text" else IndexType.BTREE.value,
                    "unique": False
                })
        
        return indexes
    
    def _generate_constraints(self, fields: List[DatabaseField]) -> List[Dict[str, Any]]:
        """Generate appropriate constraints for fields"""
        constraints = []
        
        for field in fields:
            # NOT NULL constraint
            if not field.nullable:
                constraints.append({
                    "name": f"nn_{field.name}",
                    "type": ConstraintType.NOT_NULL.value,
                    "fields": [field.name],
                    "condition": None
                })
            
            # UNIQUE constraint
            if field.name in ["email", "username", "code"]:
                constraints.append({
                    "name": f"uk_{field.name}",
                    "type": ConstraintType.UNIQUE.value,
                    "fields": [field.name],
                    "condition": None
                })
        
        return constraints
    
    def _determine_cardinality(self, relationship_type: str) -> str:
        """Determine cardinality based on relationship type"""
        if relationship_type == "one-to-one":
            return "1:1"
        elif relationship_type == "one-to-many":
            return "1:N"
        elif relationship_type == "many-to-many":
            return "M:N"
        else:
            return "N:1"
    
    def _check_normalization(self, schema: DatabaseSchema) -> List[Dict[str, Any]]:
        """Check for normalization violations"""
        issues = []
        
        for table in schema.tables:
            # Check for repeating groups (1NF)
            repeating_groups = self._check_repeating_groups(table)
            if repeating_groups:
                issues.append({
                    "type": "normalization",
                    "level": "1NF",
                    "table": table.name,
                    "issue": "Repeating groups detected",
                    "fields": repeating_groups,
                    "severity": "high"
                })
            
            # Check for partial dependencies (2NF)
            partial_deps = self._check_partial_dependencies(table)
            if partial_deps:
                issues.append({
                    "type": "normalization",
                    "level": "2NF",
                    "table": table.name,
                    "issue": "Partial dependencies detected",
                    "fields": partial_deps,
                    "severity": "medium"
                })
        
        return issues
    
    def _check_repeating_groups(self, table: DatabaseTable) -> List[str]:
        """Check for repeating groups in a table"""
        repeating_fields = []
        
        for field in table.fields:
            # Check for fields with array-like names
            if re.search(r'(_\d+|_list|_array)$', field.name):
                repeating_fields.append(field.name)
        
        return repeating_fields
    
    def _check_partial_dependencies(self, table: DatabaseTable) -> List[str]:
        """Check for partial dependencies in a table"""
        partial_deps = []
        
        # Look for composite primary keys
        pk_fields = [f for f in table.fields if any(c.get("type") == "primary_key" for c in f.__dict__.get("constraints", []))]
        
        if len(pk_fields) > 1:
            # Check for fields that depend on only part of the primary key
            for field in table.fields:
                if field not in pk_fields:
                    # Simplified check - in reality this would require dependency analysis
                    if field.name.startswith(pk_fields[0].name):
                        partial_deps.append(field.name)
        
        return partial_deps
    
    def _check_indexing(self, schema: DatabaseSchema) -> List[Dict[str, Any]]:
        """Check for indexing issues"""
        issues = []
        
        for table in schema.tables:
            # Check for tables without primary keys
            pk_fields = [f for f in table.fields if any(c.get("type") == "primary_key" for c in f.__dict__.get("constraints", []))]
            if not pk_fields:
                issues.append({
                    "type": "indexing",
                    "table": table.name,
                    "issue": "No primary key defined",
                    "severity": "high"
                })
            
            # Check for foreign key fields without indexes
            for field in table.fields:
                if field.name.endswith("_id"):
                    has_index = any(field.name in idx.get("fields", []) for idx in table.indexes)
                    if not has_index:
                        issues.append({
                            "type": "indexing",
                            "table": table.name,
                            "field": field.name,
                            "issue": "Foreign key field without index",
                            "severity": "medium"
                        })
        
        return issues
    
    def _check_relationships(self, schema: DatabaseSchema) -> List[Dict[str, Any]]:
        """Check for relationship issues"""
        issues = []
        
        # Check for many-to-many relationships without junction tables
        many_to_many = [r for r in schema.relationships if r.relationship_type == "many-to-many"]
        
        for relationship in many_to_many:
            # Check if junction table exists
            junction_table = next((t for t in schema.tables if t.name.lower() in [
                f"{relationship.source_table}_{relationship.target_table}",
                f"{relationship.target_table}_{relationship.source_table}"
            ]), None)
            
            if not junction_table:
                issues.append({
                    "type": "relationships",
                    "relationship": f"{relationship.source_table}.{relationship.source_field} -> {relationship.target_table}.{relationship.target_field}",
                    "issue": "Many-to-many relationship without junction table",
                    "severity": "medium"
                })
        
        return issues
    
    def _check_field_design(self, schema: DatabaseSchema) -> List[Dict[str, Any]]:
        """Check for field design issues"""
        issues = []
        
        for table in schema.tables:
            for field in table.fields:
                # Check for overly long field names
                if len(field.name) > 30:
                    issues.append({
                        "type": "field_design",
                        "table": table.name,
                        "field": field.name,
                        "issue": "Field name too long (>30 characters)",
                        "severity": "low"
                    })
                
                # Check for inappropriate data types
                if field.data_type == "text" and field.length:
                    issues.append({
                        "type": "field_design",
                        "table": table.name,
                        "field": field.name,
                        "issue": "Text field with length constraint",
                        "severity": "medium"
                    })
        
        return issues
    
    def _generate_recommendations(self, schema: DatabaseSchema, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on identified issues"""
        recommendations = []
        
        issue_types = [issue["type"] for issue in issues]
        
        if "normalization" in issue_types:
            recommendations.append("Consider normalizing the schema to 3NF to eliminate data redundancy")
        
        if "indexing" in issue_types:
            recommendations.append("Add appropriate indexes for foreign key fields and frequently queried columns")
        
        if "relationships" in issue_types:
            recommendations.append("Create junction tables for many-to-many relationships")
        
        if "field_design" in issue_types:
            recommendations.append("Review field naming conventions and data types")
        
        # General recommendations
        recommendations.append("Implement proper backup and recovery procedures")
        recommendations.append("Consider partitioning large tables for better performance")
        recommendations.append("Use appropriate data types to optimize storage and performance")
        
        return recommendations
    
    def _assess_normalization(self, schema: DatabaseSchema) -> str:
        """Assess the normalization level of a schema"""
        # Simplified assessment
        has_repeating_groups = any(
            self._check_repeating_groups(table) for table in schema.tables
        )
        
        if has_repeating_groups:
            return "0NF"
        
        has_partial_deps = any(
            self._check_partial_dependencies(table) for table in schema.tables
        )
        
        if has_partial_deps:
            return "1NF"
        
        # Assume 2NF if no partial dependencies
        return "3NF"
    
    def _calculate_complexity_score(self, schema: DatabaseSchema) -> float:
        """Calculate a complexity score for the schema"""
        table_count = len(schema.tables)
        relationship_count = len(schema.relationships)
        total_fields = sum(len(table.fields) for table in schema.tables)
        
        # Complexity formula: (tables * 0.3) + (relationships * 0.4) + (fields * 0.01)
        complexity = (table_count * 0.3) + (relationship_count * 0.4) + (total_fields * 0.01)
        
        return round(complexity, 2)
    
    def _extract_tables_from_query(self, query: str) -> List[str]:
        """Extract table names from SQL query"""
        # Simplified extraction - in reality would need proper SQL parsing
        tables = []
        query_upper = query.upper()
        
        # Look for FROM and JOIN clauses
        from_match = re.search(r'FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_upper)
        if from_match:
            tables.append(from_match.group(1))
        
        join_matches = re.findall(r'JOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_upper)
        tables.extend(join_matches)
        
        return list(set(tables))
    
    def _extract_fields_from_query(self, query: str) -> List[str]:
        """Extract field names from SQL query"""
        # Simplified extraction
        fields = []
        query_upper = query.upper()
        
        # Look for SELECT fields
        select_match = re.search(r'SELECT\s+(.*?)\s+FROM', query_upper)
        if select_match:
            select_part = select_match.group(1)
            # Extract field names (simplified)
            field_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)', select_part)
            fields.extend(field_matches)
        
        return list(set(fields))
    
    def _generate_execution_plan(self, query: str, schema: DatabaseSchema, 
                                tables_used: List[str], fields_used: List[str]) -> Dict[str, Any]:
        """Generate an execution plan for a query"""
        # Simplified execution plan generation
        estimated_cost = len(tables_used) * 100 + len(fields_used) * 10
        
        indexes_used = []
        bottlenecks = []
        
        # Check which indexes would be used
        for table_name in tables_used:
            table = next((t for t in schema.tables if t.name == table_name), None)
            if table:
                for index in table.indexes:
                    if any(field in index.get("fields", []) for field in fields_used):
                        indexes_used.append(f"{table_name}.{index['name']}")
        
        # Identify potential bottlenecks
        if len(tables_used) > 3:
            bottlenecks.append("Multiple table joins may impact performance")
        
        if not indexes_used:
            bottlenecks.append("No indexes available for query fields")
        
        return {
            "estimated_cost": estimated_cost,
            "indexes_used": indexes_used,
            "bottlenecks": bottlenecks,
            "execution_steps": self._generate_execution_steps(query, tables_used)
        }
    
    def _generate_execution_steps(self, query: str, tables_used: List[str]) -> List[str]:
        """Generate execution steps for a query"""
        steps = []
        
        if "SELECT" in query.upper():
            steps.append("Parse query and validate syntax")
            steps.append("Identify tables and fields")
            steps.append("Check for available indexes")
            steps.append("Generate execution plan")
            steps.append("Execute query")
            steps.append("Return results")
        
        return steps
    
    def _generate_query_optimizations(self, query: str, schema: DatabaseSchema, 
                                    plan: Dict[str, Any]) -> List[str]:
        """Generate query optimization recommendations"""
        optimizations = []
        
        # Check for missing indexes
        if not plan.get("indexes_used"):
            optimizations.append("Add indexes on frequently queried fields")
        
        # Check for unnecessary joins
        if len(plan.get("execution_steps", [])) > 5:
            optimizations.append("Consider reducing the number of table joins")
        
        # Check for SELECT *
        if "SELECT *" in query.upper():
            optimizations.append("Specify only required columns instead of using SELECT *")
        
        # Check for ORDER BY without LIMIT
        if "ORDER BY" in query.upper() and "LIMIT" not in query.upper():
            optimizations.append("Add LIMIT clause when using ORDER BY on large datasets")
        
        return optimizations
    
    def _apply_optimizations(self, query: str, optimizations: List[str]) -> str:
        """Apply optimizations to a query"""
        optimized_query = query
        
        # Apply specific optimizations
        if "Specify only required columns instead of using SELECT *" in optimizations:
            optimized_query = optimized_query.replace("SELECT *", "SELECT id, name, created_at")
        
        return optimized_query
    
    def _calculate_improvement(self, plan: Dict[str, Any], optimizations: List[str]) -> str:
        """Calculate estimated improvement from optimizations"""
        base_cost = plan.get("estimated_cost", 100)
        improvement_factor = len(optimizations) * 0.1  # 10% improvement per optimization
        
        estimated_improvement = min(improvement_factor, 0.8)  # Max 80% improvement
        
        return f"~{int(estimated_improvement * 100)}% performance improvement expected"
    
    def _generate_table_ddl(self, table: DatabaseTable, db_type: DatabaseType) -> str:
        """Generate DDL for a table"""
        field_defs = []
        
        for field in table.fields:
            field_def = f"{field.name} {self._map_data_type(field.data_type, db_type, field.length)}"
            
            if not field.nullable:
                field_def += " NOT NULL"
            
            if field.default_value:
                field_def += f" DEFAULT {field.default_value}"
            
            if field.auto_increment:
                if db_type == DatabaseType.POSTGRESQL:
                    field_def += " SERIAL"
                elif db_type == DatabaseType.MYSQL:
                    field_def += " AUTO_INCREMENT"
            
            field_defs.append(field_def)
        
        return f"CREATE TABLE {table.name} (\n  " + ",\n  ".join(field_defs) + "\n);"
    
    def _map_data_type(self, data_type: str, db_type: DatabaseType, length: Optional[int]) -> str:
        """Map generic data types to database-specific types"""
        if db_type == DatabaseType.POSTGRESQL:
            type_mapping = {
                "varchar": f"VARCHAR({length or 255})",
                "text": "TEXT",
                "integer": "INTEGER",
                "bigint": "BIGINT",
                "decimal": "DECIMAL",
                "boolean": "BOOLEAN",
                "timestamp": "TIMESTAMP",
                "date": "DATE"
            }
        elif db_type == DatabaseType.MYSQL:
            type_mapping = {
                "varchar": f"VARCHAR({length or 255})",
                "text": "TEXT",
                "integer": "INT",
                "bigint": "BIGINT",
                "decimal": "DECIMAL",
                "boolean": "BOOLEAN",
                "timestamp": "TIMESTAMP",
                "date": "DATE"
            }
        else:
            type_mapping = {
                "varchar": f"VARCHAR({length or 255})",
                "text": "TEXT",
                "integer": "INTEGER",
                "bigint": "BIGINT",
                "decimal": "DECIMAL",
                "boolean": "BOOLEAN",
                "timestamp": "TIMESTAMP",
                "date": "DATE"
            }
        
        return type_mapping.get(data_type, "TEXT")
    
    def _generate_index_ddl(self, index: Dict[str, Any], table_name: str, db_type: DatabaseType) -> str:
        """Generate DDL for an index"""
        unique_clause = "UNIQUE " if index.get("unique", False) else ""
        fields_clause = ", ".join(index.get("fields", []))
        
        return f"CREATE {unique_clause}INDEX {index['name']} ON {table_name} ({fields_clause});"
    
    def _generate_constraint_ddl(self, constraint: Dict[str, Any], table_name: str, db_type: DatabaseType) -> str:
        """Generate DDL for a constraint"""
        if constraint["type"] == "primary_key":
            fields_clause = ", ".join(constraint.get("fields", []))
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint['name']} PRIMARY KEY ({fields_clause});"
        elif constraint["type"] == "unique":
            fields_clause = ", ".join(constraint.get("fields", []))
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint['name']} UNIQUE ({fields_clause});"
        else:
            return f"-- Constraint {constraint['name']} type {constraint['type']} not implemented"
    
    def _generate_foreign_key_ddl(self, relationship: DatabaseRelationship, db_type: DatabaseType) -> str:
        """Generate DDL for a foreign key relationship"""
        return (f"ALTER TABLE {relationship.source_table} "
                f"ADD CONSTRAINT fk_{relationship.source_table}_{relationship.target_table} "
                f"FOREIGN KEY ({relationship.source_field}) "
                f"REFERENCES {relationship.target_table} ({relationship.target_field});")

# Global schema designer instance
_schema_designer = DatabaseSchemaDesigner({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "create_schema", "add_table", "add_relationship", 
                     "analyze_schema", "optimize_query", "generate_ddl", "get_stats"
            - schema_data: Schema configuration
            - table_data: Table configuration
            - relationship_data: Relationship configuration
            - query_data: Query optimization parameters
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "create_schema":
            schema_data = payload.get("schema_data", {})
            
            schema_id = _schema_designer.create_schema(
                name=schema_data.get("name", "Database Schema"),
                database_type=DatabaseType(schema_data.get("database_type", "postgresql")),
                description=schema_data.get("description", "")
            )
            
            return {
                "result": {
                    "schema_id": schema_id,
                    "message": f"Created database schema: {schema_id}"
                },
                "metadata": {
                    "action": "create_schema",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "add_table":
            table_data = payload.get("table_data", {})
            
            table_id = _schema_designer.add_table(
                schema_id=table_data.get("schema_id", ""),
                name=table_data.get("name", "Table"),
                fields=table_data.get("fields", []),
                description=table_data.get("description", "")
            )
            
            return {
                "result": {
                    "table_id": table_id,
                    "message": "Added table to schema"
                },
                "metadata": {
                    "action": "add_table",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "add_relationship":
            relationship_data = payload.get("relationship_data", {})
            
            relationship_id = _schema_designer.add_relationship(
                schema_id=relationship_data.get("schema_id", ""),
                source_table=relationship_data.get("source_table", ""),
                source_field=relationship_data.get("source_field", ""),
                target_table=relationship_data.get("target_table", ""),
                target_field=relationship_data.get("target_field", ""),
                relationship_type=relationship_data.get("relationship_type", "one-to-many")
            )
            
            return {
                "result": {
                    "relationship_id": relationship_id,
                    "message": "Added relationship to schema"
                },
                "metadata": {
                    "action": "add_relationship",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "analyze_schema":
            schema_id = payload.get("schema_id", "")
            analysis = _schema_designer.analyze_schema(schema_id)
            
            return {
                "result": analysis,
                "metadata": {
                    "action": "analyze_schema",
                    "timestamp": datetime.now().isoformat(),
                    "schema_id": schema_id
                }
            }
        
        elif action == "optimize_query":
            query_data = payload.get("query_data", {})
            
            optimization = _schema_designer.optimize_query(
                schema_id=query_data.get("schema_id", ""),
                query=query_data.get("query", "")
            )
            
            return {
                "result": optimization,
                "metadata": {
                    "action": "optimize_query",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "generate_ddl":
            schema_id = payload.get("schema_id", "")
            ddl = _schema_designer.generate_ddl(schema_id)
            
            return {
                "result": ddl,
                "metadata": {
                    "action": "generate_ddl",
                    "timestamp": datetime.now().isoformat(),
                    "schema_id": schema_id
                }
            }
        
        elif action == "get_stats":
            stats = _schema_designer.get_design_stats()
            
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
        logger.error(f"Error in database_schema_designer: {e}")
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
    """Example of how to use the database schema designer skill"""
    
    # Create a schema
    schema_id = await invoke({
        "action": "create_schema",
        "schema_data": {
            "name": "ECommerce",
            "database_type": "postgresql",
            "description": "E-commerce platform database schema"
        }
    })
    
    print(f"Created schema: {schema_id['result']['schema_id']}")
    
    # Add tables
    users_table_id = await invoke({
        "action": "add_table",
        "table_data": {
            "schema_id": schema_id['result']['schema_id'],
            "name": "users",
            "fields": [
                {"name": "id", "data_type": "integer", "nullable": False, "auto_increment": True},
                {"name": "email", "data_type": "varchar", "length": 255, "nullable": False},
                {"name": "name", "data_type": "varchar", "length": 100, "nullable": False},
                {"name": "created_at", "data_type": "timestamp", "nullable": False}
            ],
            "description": "User accounts"
        }
    })
    
    products_table_id = await invoke({
        "action": "add_table",
        "table_data": {
            "schema_id": schema_id['result']['schema_id'],
            "name": "products",
            "fields": [
                {"name": "id", "data_type": "integer", "nullable": False, "auto_increment": True},
                {"name": "name", "data_type": "varchar", "length": 200, "nullable": False},
                {"name": "price", "data_type": "decimal", "precision": 10, "scale": 2, "nullable": False},
                {"name": "stock", "data_type": "integer", "nullable": False},
                {"name": "created_at", "data_type": "timestamp", "nullable": False}
            ],
            "description": "Product catalog"
        }
    })
    
    orders_table_id = await invoke({
        "action": "add_table",
        "table_data": {
            "schema_id": schema_id['result']['schema_id'],
            "name": "orders",
            "fields": [
                {"name": "id", "data_type": "integer", "nullable": False, "auto_increment": True},
                {"name": "user_id", "data_type": "integer", "nullable": False},
                {"name": "total_amount", "data_type": "decimal", "precision": 10, "scale": 2, "nullable": False},
                {"name": "status", "data_type": "varchar", "length": 50, "nullable": False},
                {"name": "created_at", "data_type": "timestamp", "nullable": False}
            ],
            "description": "Customer orders"
        }
    })
    
    print(f"Added tables: {users_table_id['result']['table_id']}, {products_table_id['result']['table_id']}, {orders_table_id['result']['table_id']}")
    
    # Add relationships
    await invoke({
        "action": "add_relationship",
        "relationship_data": {
            "schema_id": schema_id['result']['schema_id'],
            "source_table": "orders",
            "source_field": "user_id",
            "target_table": "users",
            "target_field": "id",
            "relationship_type": "one-to-many"
        }
    })
    
    # Analyze schema
    analysis = await invoke({
        "action": "analyze_schema",
        "schema_id": schema_id['result']['schema_id']
    })
    
    print(f"Schema analysis: {analysis['result']}")
    
    # Optimize a query
    optimization = await invoke({
        "action": "optimize_query",
        "query_data": {
            "schema_id": schema_id['result']['schema_id'],
            "query": "SELECT u.name, COUNT(o.id) as order_count FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.name ORDER BY order_count DESC"
        }
    })
    
    print(f"Query optimization: {optimization['result']}")
    
    # Generate DDL
    ddl = await invoke({
        "action": "generate_ddl",
        "schema_id": schema_id['result']['schema_id']
    })
    
    print(f"Generated DDL: {ddl['result']}")

if __name__ == "__main__":
    asyncio.run(example_usage())
