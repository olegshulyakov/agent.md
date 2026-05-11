---
name: model-dbt
description: >
  Generates dbt model SQL files, schema.yml definitions, tests, and documentation for data transformation
  pipelines. Use this skill whenever the user wants to create dbt models, write dbt SQL transformations,
  define dbt schema and tests, document dbt models, build a dbt project structure, or asks to "write a
  dbt model", "create a dbt transformation", "generate schema.yml for dbt", "add dbt tests to this model",
  "write a staging/intermediate/mart model", "model this data in dbt", or "create dbt documentation".
  Also trigger for "dbt source definition", "dbt snapshot", "dbt seed", "dbt materialization", and
  "incremental model". Distinct from writer-sql (general SQL queries) and setup-pipeline-etl
  (broader ETL pipeline scaffolding).
---

# model-dbt

Produce **dbt model files** including the SQL transformation, `schema.yml`, tests, and documentation.

## dbt Model Layers

Identify which layer the model belongs to and apply appropriate conventions:

| Layer | Prefix | Purpose | Materialization | Source |
|-------|--------|---------|----------------|--------|
| **Staging** | `stg_` | Clean raw source data; 1:1 with source tables | `view` | `source()` |
| **Intermediate** | `int_` | Business logic, joins; consumed only by marts | `view` or `ephemeral` | `ref()` |
| **Marts** | `fct_`, `dim_` | Wide, analytics-ready facts and dimensions | `table` or `incremental` | `ref()` |

## Information gathering

From context, identify:
- **Data source**: Source table names, schema, raw columns
- **Transformation goal**: What business entity or metric is being modeled?
- **Layer**: Staging, intermediate, or mart?
- **Grain**: What does one row represent?
- **Tests needed**: uniqueness, not-null, accepted values, relationships?
- **Incremental?**: Large fact table needing incremental loading?

## Output structure

Generate these files:

```
models/
├── staging/
│   └── [source_name]/
│       ├── stg_[source]__[entity].sql
│       └── _stg_[source]__[entity].yml
├── intermediate/
│   └── int_[entity]_[transformation].sql
└── marts/
    └── [domain]/
        ├── fct_[entity].sql
        ├── dim_[entity].sql
        └── _[domain].yml
```

## SQL templates

### Staging model (`stg_source__entity.sql`)

```sql
-- stg_orders__orders.sql
-- Grain: one row per order
-- Source: raw.orders

with source as (
    select * from {{ source('orders', 'orders') }}
),

renamed as (
    select
        -- Primary key
        order_id,
        
        -- Foreign keys
        customer_id,
        store_id,
        
        -- Dimensions
        status                                     as order_status,
        
        -- Cleaned fields
        {{ dbt_utils.generate_surrogate_key(['order_id']) }} as order_key,
        
        -- Timestamps
        created_at                                 as order_created_at,
        updated_at                                 as order_updated_at,
        
        -- Metadata
        _loaded_at
        
    from source
)

select * from renamed
```

### Intermediate model (`int_entity_transformation.sql`)

```sql
-- int_orders_pivoted.sql
-- Grain: one row per order with aggregated line items

with orders as (
    select * from {{ ref('stg_orders__orders') }}
),

order_items as (
    select * from {{ ref('stg_orders__order_items') }}
),

agg_items as (
    select
        order_id,
        count(*)            as item_count,
        sum(quantity)       as total_quantity,
        sum(unit_price * quantity) as gross_revenue
    from order_items
    group by 1
),

joined as (
    select
        o.*,
        i.item_count,
        i.total_quantity,
        i.gross_revenue
    from orders o
    left join agg_items i using (order_id)
)

select * from joined
```

### Fact model (`fct_entity.sql`)

```sql
-- fct_orders.sql
-- Grain: one row per order
-- Materialization: table (or incremental for large volumes)

{{
    config(
        materialized='incremental',
        unique_key='order_id',
        on_schema_change='sync_all_columns',
        incremental_strategy='merge'
    )
}}

with orders as (
    select * from {{ ref('int_orders_pivoted') }}
    {% if is_incremental() %}
        where order_updated_at > (select max(order_updated_at) from {{ this }})
    {% endif %}
),

final as (
    select
        -- Surrogate key
        {{ dbt_utils.generate_surrogate_key(['order_id']) }} as order_key,
        
        -- Natural key
        order_id,
        
        -- Dimensions
        customer_id,
        order_status,
        
        -- Measures
        item_count,
        total_quantity,
        gross_revenue,
        
        -- Derived measures
        gross_revenue - (gross_revenue * 0.1) as net_revenue,
        
        -- Dates
        order_created_at::date                  as order_date,
        order_created_at,
        order_updated_at,
        
        -- Metadata
        current_timestamp                       as dbt_updated_at
        
    from orders
)

select * from final
```

### Dimension model (`dim_entity.sql`)

```sql
-- dim_customers.sql
-- Grain: one row per current customer (SCD Type 1)

with customers as (
    select * from {{ ref('stg_customers__customers') }}
),

final as (
    select
        -- Surrogate key
        {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_key,
        
        customer_id,
        full_name,
        email,
        country_code,
        customer_segment,
        first_order_date,
        current_timestamp as dbt_updated_at
        
    from customers
)

select * from final
```

## Schema YAML (`_domain.yml`)

```yaml
version: 2

sources:
  - name: orders
    database: raw
    schema: public
    tables:
      - name: orders
        description: "Raw orders from the OLTP database"
        loaded_at_field: _loaded_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
        columns:
          - name: order_id
            description: "Primary key"
            tests:
              - unique
              - not_null

models:
  - name: fct_orders
    description: >
      One row per order. Central fact table for order analytics.
      Join to dim_customers and dim_products for full context.
    config:
      tags: ['daily', 'finance']
    columns:
      - name: order_key
        description: "Surrogate key (SHA256 of order_id)"
        tests:
          - unique
          - not_null
      - name: order_id
        description: "Natural key from source system"
        tests:
          - not_null
          - relationships:
              to: ref('stg_orders__orders')
              field: order_id
      - name: order_status
        description: "Current order status"
        tests:
          - not_null
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled', 'refunded']
      - name: gross_revenue
        description: "Sum of (unit_price × quantity) before discounts and taxes"
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
```

## Calibration

- **Staging model only**: Clean rename of source; minimal transformations
- **With incremental**: Use `is_incremental()` block; document the unique key and update strategy
- **Snapshot / SCD Type 2**: Use `dbt snapshot` syntax with `strategy`, `unique_key`, `updated_at`
- **Custom test**: Define as a `.sql` file in `tests/` returning rows that fail the test
- **Documentation-only request**: Generate `schema.yml` for existing models without writing SQL
