---
name: sql-optimization-patterns
description: "Use when: optimizing SQL queries, debugging slow database operations, designing database schemas, improving database performance, or analyzing query execution plans. Triggers: 'SQL', 'query optimization', 'slow query', 'EXPLAIN', 'index', 'performance', 'database', 'optimize', 'execution plan'. NOT for: simple queries that already perform well, or when ORM handles optimization automatically."
---

# SQL Optimization Patterns

Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance and eliminate slow queries.

## When to Use This Skill

Use this skill when:
- Debugging slow queries
- Designing database schemas for performance
- Creating or reviewing indexes
- Analyzing query execution plans
- Optimizing application performance
- Performance tuning existing queries

Do NOT use when:
- Simple queries that already perform well
- Queries that run infrequently
- When ORM handles optimization automatically

## Query Analysis

### Reading EXPLAIN Output

#### PostgreSQL EXPLAIN
```sql
EXPLAIN ANALYZE 
SELECT o.id, o.created_at, c.name, p.name as product
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01'
ORDER BY o.created_at DESC
LIMIT 100;

-- Key metrics to look for:
-- - Seq Scan (bad for large tables)
-- - Index Scan (good)
-- - Nested Loop (ok for small datasets)
-- - Hash Join (good for large datasets)
-- - Actual time vs planned time
-- - Rows actually vs estimated
```

#### MySQL EXPLAIN
```sql
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE customer_id = 123;

-- Look for:
-- - type: const, eq_ref, ref, range, all (all is bad)
-- - key: which index is used
-- - rows: estimated rows to scan
-- - Extra: Using filesort, Using temporary (bad)
```

### Common Performance Problems

| Problem | Symptom | Solution |
|---------|---------|----------|
| Full Table Scan | Seq Scan in EXPLAIN | Add index |
| Missing Index | WHERE clause not using index | Create index |
| N+1 Queries | Multiple sequential scans | Join or batch |
| Unoptimized JOIN | Nested Loop on large tables | Rewrite query |
| No Pagination | Scanning entire table | Add LIMIT |
| Function on Column | Can't use index | Use generated column |

## Indexing Strategies

### Single Column Index
```sql
-- For equality queries
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- For date range queries  
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);
```

### Composite Index
```sql
-- For queries with multiple WHERE conditions
-- Column order matters: equality first, then range
CREATE INDEX idx_orders_status_created 
ON orders(status, created_at DESC);

-- DON'T create for queries that only use second column
-- This is WRONG order for: WHERE status = 'pending'
CREATE INDEX idx_orders_created_status 
ON orders(created_at DESC, status);  -- Wrong order!
```

### Partial Index
```sql
-- Index only active orders (PostgreSQL)
CREATE INDEX idx_orders_active ON orders(customer_id, created_at)
WHERE status = 'active';
```

### Covering Index
```sql
-- Include all columns needed by query
CREATE INDEX idx_orders_covering 
ON orders(customer_id, created_at) 
INCLUDE (total_amount, status);

-- Query can be satisfied entirely from index
SELECT customer_id, created_at, total_amount, status
FROM orders
WHERE customer_id = 123;
```

### When NOT to Index
- Columns with low cardinality (boolean, gender)
- Tables with infrequent queries
- Columns frequently updated
- Very small tables

## Query Patterns

### Avoid SELECT *
```sql
-- BAD: Fetches all columns
SELECT * FROM orders WHERE customer_id = 123;

-- GOOD: Only needed columns
SELECT id, created_at, total_amount 
FROM orders 
WHERE customer_id = 123;
```

### Use EXISTS Instead of IN
```sql
-- BAD: May scan large dataset
SELECT * FROM customers c
WHERE c.id IN (SELECT o.customer_id FROM orders o);

-- GOOD: Stops at first match
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.id
);
```

### Use JOIN Instead of Subquery
```sql
-- BAD: Two queries
SELECT * FROM customers c
JOIN (SELECT customer_id, SUM(amount) as total 
      FROM orders GROUP BY customer_id) o
ON c.id = o.customer_id;

-- GOOD: Single optimized query
SELECT c.*, SUM(o.amount) as total
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id;
```

### Pagination
```sql
-- BAD: Offset pagination gets slower
SELECT * FROM orders ORDER BY id LIMIT 10 OFFSET 1000;

-- GOOD: Keyset pagination (faster)
SELECT * FROM orders 
WHERE id < 1000  -- Last seen ID
ORDER BY id DESC 
LIMIT 10;
```

### Batch Operations
```sql
-- BAD: Multiple queries
for id in ids:
    execute("UPDATE orders SET status = 'processed' WHERE id = ?", id)

-- GOOD: Batch update
UPDATE orders 
SET status = 'processed' 
WHERE id IN (1, 2, 3, 4, 5);
```

## Schema Optimization

### Normalization vs Denormalization

#### Normalized Schema (OLTP)
```sql
-- Normalized for write performance
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    region_id INT REFERENCES regions(id)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    created_at TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT,
    price DECIMAL(10,2)
);
```

#### Denormalized for Read Performance
```sql
-- Add computed columns
ALTER TABLE orders ADD COLUMN customer_name VARCHAR(255);
ALTER TABLE orders ADD COLUMN total_items INT;

-- Use materialized views
CREATE MATERIALIZED VIEW order_summary AS
SELECT 
    o.id,
    o.customer_id,
    c.name as customer_name,
    SUM(oi.price * oi.quantity) as total_amount,
    COUNT(*) as item_count
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, o.customer_id, c.name;
```

### Partitioning
```sql
-- PostgreSQL Range Partitioning
CREATE TABLE orders (
    id SERIAL,
    customer_id INT,
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

CREATE TABLE orders_2024_01 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

## Database-Specific Tips

### PostgreSQL
```sql
-- Analyze query planner choice
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE customer_id = 123;

-- Force index usage (when needed)
SELECT * FROM orders USE INDEX (idx_orders_customer_id)
WHERE customer_id = 123;

-- Vacuum for performance
VACUUM ANALYZE orders;

-- Check index usage
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE relname = 'orders';
```

### MySQL
```sql
-- Force index
SELECT * FROM orders FORCE INDEX (idx_customer)
WHERE customer_id = 123;

-- Check profile
SET profiling = 1;
SELECT * FROM orders WHERE customer_id = 123;
SHOW PROFILES;

-- Analyze index cardinality
SHOW INDEX FROM orders;
```

## Caching Strategies

### Application-Level Cache
```python
import redis
from functools import wraps

redis_client = redis.Redis()

def cache_result(expiry_seconds=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from args
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute and cache
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, expiry_seconds, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(expiry_seconds=60)
def get_user_orders(user_id: int):
    return db.query(Order).filter_by(customer_id=user_id).all()
```

### Query Result Invalidation
```python
def invalidate_user_cache(user_id: int):
    pattern = f"*:user_id={user_id}:*"
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)
```

## Performance Testing

### Benchmarking Queries
```sql
-- PostgreSQL
\timing on

-- Run multiple times for consistency
SELECT * FROM orders WHERE customer_id = 123;
SELECT * FROM orders WHERE customer_id = 123;
SELECT * FROM orders WHERE customer_id = 123;

-- MySQL
SET profiling = 1;
SELECT * FROM orders WHERE customer_id = 123;
SHOW PROFILES;
```

### Load Testing
```sql
-- Simulate concurrent users
BEGIN;
SELECT * FROM orders WHERE customer_id = 1;
-- Run from multiple connections
COMMIT;
```

## Constraints

- Always measure before optimizing
- Use EXPLAIN ANALYZE, not just EXPLAIN
- Index WHERE and JOIN columns first
- Consider read vs write ratio
- Monitor query patterns in production
- Use connection pooling
- Keep statistics up to date
- Test with realistic data volumes
- Don't over-index (impacts writes)
