---
name: writer-sql-analytics
description: >
  Writes complex analytical SQL queries for data warehouses (Snowflake, BigQuery, ClickHouse, Redshift).
  Use this skill whenever the user wants to write an analytical query, use window functions, calculate
  retention, perform cohort analysis, write a pivoting query, or asks to "write a BigQuery query",
  "calculate monthly active users in SQL", "write a Snowflake query for X", "how do I do cohort
  analysis in SQL", or "write an analytical SQL query". Distinct from writer-sql (which focuses on
  OLTP transactional databases like Postgres/MySQL) and model-dbt (which focuses on dbt project structure).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-sql-analytics

Produce **analytical SQL queries** optimized for data warehouses (BigQuery, Snowflake, etc.).

## Output format

```sql
-- Target dialect: [BigQuery / Snowflake / ClickHouse / Redshift]
-- Description: [Brief explanation of what the query calculates]

WITH cohort_users AS (
    -- 1. Identify the user's first action (cohort definition)
    SELECT 
        user_id,
        DATE_TRUNC('month', MIN(event_timestamp)) AS cohort_month
    FROM `project.dataset.events`
    WHERE event_name = 'sign_up'
    GROUP BY 1
),

active_months AS (
    -- 2. Identify all months the user was active
    SELECT DISTINCT
        user_id,
        DATE_TRUNC('month', event_timestamp) AS activity_month
    FROM `project.dataset.events`
    WHERE event_name = 'purchase'
)

-- 3. Calculate retention matrix
SELECT 
    c.cohort_month,
    COUNT(DISTINCT c.user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN DATE_DIFF(a.activity_month, c.cohort_month, MONTH) = 1 THEN c.user_id END) AS month_1_retained,
    COUNT(DISTINCT CASE WHEN DATE_DIFF(a.activity_month, c.cohort_month, MONTH) = 2 THEN c.user_id END) AS month_2_retained,
    COUNT(DISTINCT CASE WHEN DATE_DIFF(a.activity_month, c.cohort_month, MONTH) = 3 THEN c.user_id END) AS month_3_retained
FROM cohort_users c
LEFT JOIN active_months a ON c.user_id = a.user_id
GROUP BY 1
ORDER BY 1 DESC;
```

## Analytical SQL Guidelines

- **Use CTEs (WITH clauses)** heavily. Break complex logic into readable, sequential steps. Do not use nested subqueries in the FROM clause.
- **Dialect awareness**: Be precise with date functions (e.g., BigQuery `DATE_DIFF` vs Snowflake `DATEDIFF`).
- **Window functions**: Use `ROW_NUMBER()`, `LAG()`, `LEAD()`, and `SUM() OVER (...)` for running totals and sessionization.
- **Comments**: Comment each CTE to explain its purpose.
- **Formatting**: Capitalize SQL keywords. Indent consistently.
