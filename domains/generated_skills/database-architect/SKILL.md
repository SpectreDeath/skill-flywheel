---
name: database-architect
description: "Use when: designing database schemas, writing SQL queries, optimizing database performance, implementing connection pooling, managing migrations, or working with PostgreSQL/MongoDB/cloud databases. Triggers: 'database', 'SQL', 'schema', 'PostgreSQL', 'MongoDB', 'query', 'migration', 'index', 'connection pool', 'repository pattern', 'ORM', 'EF Core', 'postgres'. NOT for: infrastructure (use devops skills), or analytics (use data analysis skills)."
---

# Database Architect

Complete database development and administration skill covering schema design, query optimization, migrations, and cloud databases.

## Supported Databases

- PostgreSQL (relational, JSON, vector)
- MongoDB (document, Atlas)
- SQLite (embedded)
- Cloud: Azure SQL, Snowflake, BigQuery

## Schema Design

```python
class SchemaDesigner:
    """Design database schemas."""
    
    def design_relational(self, entities: List[Entity]) -> Schema:
        """Design PostgreSQL schema."""
        
        tables = []
        for entity in entities:
            columns = []
            for attr in entity.attributes:
                col = Column(
                    name=attr.name,
                    type=self.map_type(attr.type),
                    nullable=attr.nullable,
                    primary_key=attr.primary_key,
                    references=attr.references
                )
                columns.append(col)
                
            tables.append(Table(name=entity.name, columns=columns))
            
        # Add indexes
        for entity in entities:
            for idx in entity.indexes:
                tables[idx.table].add_index(idx.columns, unique=idx.unique)
                
        return Schema(tables=tables)
        
    def design_document(self, collections: List[Collection]) -> Schema:
        """Design MongoDB schema."""
        
        schemas = {}
        for coll in collections:
            schemas[coll.name] = {
                "_id": "ObjectId",
                "_createdAt": "datetime",
                "_updatedAt": "datetime"
            }
            for field in coll.fields:
                schemas[coll.name][field.name] = self.map_mongo_type(field.type)
                
        return Schema(collections=schemas)
        
    @staticmethod
    def map_type(attr_type: str) -> str:
        """Map Python type to SQL type."""
        mappings = {
            "str": "VARCHAR(255)",
            "int": "INTEGER",
            "float": "REAL",
            "bool": "BOOLEAN",
            "datetime": "TIMESTAMP",
            "uuid": "UUID",
            "json": "JSONB",
            "text": "TEXT"
        }
        return mappings.get(attr_type, "TEXT")
```

## SQL Query Patterns

```python
class SQLPatterns:
    """Common SQL patterns."""
    
    @staticmethod
    def pagination(query: str, page: int, page_size: int) -> str:
        """Add pagination to query."""
        offset = (page - 1) * page_size
        return f"""
            {query}
            LIMIT {page_size} OFFSET {offset}
        """
        
    @staticmethod
    def upsert(table: str, data: dict) -> str:
        """Generate upsert statement."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f"${i+1}" for i in range(len(data))])
        return f"""
            INSERT INTO {table} ({columns})
            VALUES ({placeholders})
            ON CONFLICT (id) DO UPDATE SET
            {", ".join([f"{k} = EXCLUDED.{k}" for k in data.keys()])}
        """
        
    @staticmethod
    def bulk_insert(table: str, rows: List[dict]) -> str:
        """Generate bulk insert."""
        if not rows:
            return ""
        columns = ", ".join(rows[0].keys())
        placeholders = ", ".join([f"${i+1}" for i in range(len(rows[0]))])
        values = ", ".join([f"({placeholders})" for _ in rows])
        return f"INSERT INTO {table} ({columns}) VALUES {values}"
        
    @staticmethod
    def recursive_cte(base_table: str, id_col: str, parent_col: str) -> str:
        """Generate recursive CTE for tree traversal."""
        return f"""
            WITH RECURSIVE tree AS (
                SELECT *, 0 as depth
                FROM {base_table}
                WHERE {parent_col} IS NULL
                
                UNION ALL
                
                SELECT t.*, tree.depth + 1
                FROM {base_table} t
                JOIN tree ON t.{parent_col} = tree.{id_col}
            )
            SELECT * FROM tree
        """
```

## Connection Pooling

```python
import asyncpg
from contextlib import asynccontextmanager

class ConnectionPool:
    """Manage database connections."""
    
    def __init__(self, dsn: str, min_size=5, max_size=20):
        self.pool = None
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        
    async def init(self):
        """Initialize pool."""
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size
        )
        
    @asynccontextmanager
    async def acquire(self):
        """Acquire connection."""
        async with self.pool.acquire() as conn:
            yield conn
            
    async def close(self):
        """Close pool."""
        await self.pool.close()
        
# Usage
pool = ConnectionPool("postgresql://user:pass@localhost/db")
await pool.init()

async with pool.acquire() as conn:
    await conn.fetch("SELECT * FROM users")
```

## Migration Management

```python
class MigrationManager:
    """Handle database migrations."""
    
    def __init__(self, pool: ConnectionPool):
        self.pool = pool
        
    async def create_migration(self, name: str) -> str:
        """Create new migration file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.sql"
        
        template = f"""
-- Migration: {name}
-- Created: {datetime.now()}

-- Forward
BEGIN;

-- TODO: Add your changes here

COMMIT;

-- Rollback
-- BEGIN;
-- TODO: Add rollback steps
-- ROLLBACK;
"""
        return filename, template
        
    async def run_migrations(self):
        """Run pending migrations."""
        async with self.pool.acquire() as conn:
            # Create migrations table if not exists
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS _migrations (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    applied_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Get applied migrations
            applied = await conn.fetch("SELECT name FROM _migrations")
            applied_names = {row["name"] for row in applied}
            
            # Run pending
            for migration in self.get_pending_migrations(applied_names):
                await conn.execute(migration.sql)
                await conn.execute(
                    "INSERT INTO _migrations (name) VALUES ($1)",
                    migration.name
                )
```

## Query Optimization

```python
class QueryOptimizer:
    """Optimize SQL queries."""
    
    def analyze(self, query: str) -> OptimizationReport:
        """Analyze query for optimization opportunities."""
        
        issues = []
        
        # Check for missing indexes
        if "WHERE" in query and "JOIN" in query:
            issues.append("Consider adding index on filter columns")
            
        # Check for N+1 patterns
        if query.count("SELECT") > 1:
            issues.append("Potential N+1 query detected")
            
        # Check for missing LIMIT
        if "ORDER BY" in query and "LIMIT" not in query:
            issues.append("Consider adding LIMIT to avoid full sort")
            
        return OptimizationReport(issues=issues)
        
    def explain(self, conn, query: str) -> dict:
        """Get query plan."""
        return conn.fetchrow(f"EXPLAIN (ANALYZE, BUFFERS) {query}")
        
    def suggest_indexes(self, query: str) -> List[str]:
        """Suggest indexes for query."""
        # Analyze WHERE clauses
        # Analyze JOIN conditions
        # Analyze ORDER BY columns
        pass
```

## MongoDB Patterns

```python
class MongoDBPatterns:
    """MongoDB-specific patterns."""
    
    @staticmethod
    def aggregation_pipeline(stages: List[dict]) -> list:
        """Build aggregation pipeline."""
        return stages
        
    @staticmethod
    def lookup_join(from_col: str, local_field: str, 
                    foreign_field: str, as_field: str) -> dict:
        """Perform lookup join."""
        return {
            "$lookup": {
                "from": from_col,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_field
            }
        }
        
    @staticmethod
    def transaction(operations: List[dict]) -> dict:
        """Execute transaction."""
        return {"$transact": operations}
```

## Repository Pattern

```python
class UserRepository:
    """Repository pattern implementation."""
    
    def __init__(self, pool: ConnectionPool):
        self.pool = pool
        
    async def get_by_id(self, id: int) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", id
            )
            return User(**row) if row else None
            
    async def create(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO users (name, email)
                VALUES ($1, $2)
                RETURNING *
            """, user.name, user.email)
            return User(**row)
            
    async def update(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                UPDATE users SET name = $1, email = $2
                WHERE id = $3
                RETURNING *
            """, user.name, user.email, user.id)
            return User(**row)
            
    async def delete(self, id: int) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM users WHERE id = $1", id
            )
            return result != "DELETE 0"
```

## Constraints

- MUST use parameterized queries to prevent SQL injection
- SHOULD use connection pooling for production workloads
- MUST implement proper error handling and retries
- SHOULD use transactions for multi-step operations
- MUST handle migration rollbacks
- SHOULD monitor query performance with EXPLAIN
- MUST back up before schema changes