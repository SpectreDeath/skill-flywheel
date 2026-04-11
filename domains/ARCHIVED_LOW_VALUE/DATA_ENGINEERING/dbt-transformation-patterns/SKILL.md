---
name: dbt-transformation-patterns
description: "Use when: building data transformations with dbt (data build tool), creating analytics models, implementing incremental strategies, writing dbt tests, or documenting data models. Triggers: 'dbt', 'data build tool', 'analytics engineering', 'dbt model', 'dbt test', 'dbt run', 'dbt docs', 'transformation', 'warehouse'. NOT for: real-time streaming pipelines, or when using other ETL tools like Airflow directly."
---

# dbt Transformation Patterns

Master dbt (data build tool) for analytics engineering with model organization, testing, documentation, and incremental strategies.

## When to Use This Skill

Use this skill when:
- Building data transformations in a data warehouse
- Creating analytics models and business logic
- Implementing incremental processing for large datasets
- Writing and running dbt tests
- Documenting data models and lineage
- Setting up dbt for a new project

Do NOT use when:
- Real-time streaming pipelines (use Kafka/Flink)
- Complex orchestrations beyond dbt (use Airflow)
- Data sources outside the warehouse
- Batch processing without SQL transformations

## Project Structure

```
my_dbt_project/
├── models/
│   ├── staging/
│   │   ├── stg_orders.sql
│   │   └── stg_customers.sql
│   ├── intermediate/
│   │   └── int_order_metrics.sql
│   └── marts/
│       ├── dim_customers.sql
│       └── fct_orders.sql
├── macros/
│   ├── macros/
│   │   └── get_payment_type.sql
│   └── utils/
│       └── dates.sql
├── tests/
│   └── assert_positive_amounts.sql
├── seeds/
│   └── payment_types.csv
├── snapshots/
│   └── snap_orders.sql
├── analysis/
│   └── ad_hoc_analysis.sql
├── dbt_project.yml
└── profiles.yml
```

## Model Organization

### Staging Layer
```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

select
    order_id,
    customer_id,
    order_date,
    status,
    total_amount,
    created_at
from {{ source('ecom', 'orders') }}
```

### Intermediate Layer
```sql
-- models/intermediate/int_order_metrics.sql
{{ config(materialized='table') }}

with order_items as (
    select * from {{ ref('stg_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

enriched as (
    select
        o.order_id,
        o.customer_id,
        o.order_date,
        sum(oi.amount) as total_item_amount
    from orders o
    join order_items oi on o.order_id = oi.order_id
    group by 1, 2, 3
)

select * from enriched
```

### Marts Layer (Fact & Dimension)
```sql
-- models/marts/fct_orders.sql
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select
    order_id,
    customer_id,
    order_date,
    total_amount,
    status,
    _loaded_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
where _loaded_at > (select max(_loaded_at) from {{ this }})
{% endif %}
```

## Incremental Strategies

### Append-Only Strategy
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='append'
) }}

select ...
from {{ source('ecom', 'orders') }}
```

### Merge Strategy (Snowflake/BigQuery)
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge'
) }}

select
    order_id,
    customer_id,
    order_date,
    total_amount
from {{ source('ecom', 'orders') }}

{% if is_incremental() %}
where order_date > (select max(order_date) from {{ this }})
{% endif %}
```

### Delete+Insert Strategy (Redshift)
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='delete+insert'
) }}
```

## Testing Patterns

### Generic Tests
```yaml
# dbt_project.yml
tests:
  my_dbt_project:
    assert_positive_amounts:
      - assert: positive_value
        column_name: amount
    assert_valid_status:
      - assert: accepted_values
        column_name: status
        values: ['pending', 'completed', 'cancelled']
```

### Singular Tests
```sql
-- tests/assert_no_duplicate_orders.sql
select order_id, count(*)
from {{ ref('fct_orders') }}
group by order_id
having count(*) > 1
```

### Schema Tests
```yaml
# models/schema.yml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: total_amount
        tests:
          - not_null
```

## Documentation

### Model Documentation
```sql
-- models/marts/fct_orders.sql
{{ config(
    meta={
        'model_owner': 'analytics_team',
        'cost_center': 'engineering'
    }
) }}

/*
    Business Purpose: Track order performance and revenue metrics
    
    Data Sources:
    - Source: ecom.orders (production database)
    - Refresh: Daily at 6 AM UTC
    
    Key Metrics:
    - Total Revenue
    - Order Count
    - Average Order Value
*/
```

### Column Descriptions
```yaml
# models/schema.yml
models:
  - name: fct_orders
    description: Order fact table capturing all order transactions
    columns:
      - name: order_id
        description: Primary key, unique order identifier
        tests: [unique, not_null]
      - name: total_amount
        description: Total order amount in USD
        meta:
          metric: revenue
```

## Macros

### Reusable Macro
```sql
-- macros/get_payment_type.sql
{% macro get_payment_type(payment_id) %}
    case
        when payment_id like '%CARD%' then 'credit_card'
        when payment_id like '%PAYPAL%' then 'paypal'
        when payment_id like '%BANK%' then 'bank_transfer'
        else 'other'
    end
{% endmacro %}
```

### Macro Usage
```sql
select
    order_id,
    {{ get_payment_type(payment_id) }} as payment_type
from {{ ref('stg_orders') }}
```

## Seeds and Snapshots

### Seeds (Static Data)
```bash
dbt seed --select payment_types
```

```csv
# data/payment_types.csv
payment_type_id,payment_type_name
1,Credit Card
2,PayPal
3,Bank Transfer
```

### Snapshots (Slowly Changing Dimensions)
```sql
-- snapshots/snap_customers.sql
{% snapshot snap_customers %}
    {{
        config(
            strategy='check',
            unique_key='customer_id',
            invalidate_hard_deletes=True,
            check_cols=['email', 'name', 'status']
        )
    }}
    select
        customer_id,
        email,
        name,
        status,
        updated_at
    from {{ source('ecom', 'customers') }}
{% endsnapshot %}
```

## Running dbt

### Common Commands
```bash
# Run all models
dbt run

# Run specific model and its dependencies
dbt run --select dim_customers+

# Run tests
dbt test

# Generate docs
dbt docs generate

# Serve docs locally
dbt docs serve

# Debug
dbt debug

# Compile only (validate SQL)
dbt compile
```

### Selection Syntax
```bash
# By tag
dbt run --select tag:daily

# By source
dbt run --select source:ecom+

# By path
dbt run --select models/marts/

# By config
dbt run --select config(materialized=table)
```

## Constraints

- Always use sources instead of raw tables
- Document all models and columns
- Test critical business logic
- Use incremental models for large datasets
- Keep staging models simple (1:1 with source)
- Use generic tests for reusability
- Version control your dbt project
- Use packages for shared macros
