---
name: writer-sql
description: >
  Writes production-quality SQL queries, DDL statements, stored procedures, views, and transactions
  for OLTP databases (PostgreSQL, MySQL, MSSQL, SQLite, Oracle). Use this skill whenever the user wants
  to write a SQL query, SELECT statement, INSERT/UPDATE/DELETE, JOIN query, CTE, stored procedure,
  trigger, view, index, or any transactional SQL. Also trigger for "optimize this query", "write SQL for X",
  "how do I query Y in SQL", "write a migration query", or "generate SQL". Distinct from writer-sql-analytics
  (which targets warehouse dialects: Snowflake, BigQuery, ClickHouse) and design-schema (which designs
  the structure, not the queries).
---

# writer-sql

Write **production-quality SQL** for OLTP databases: queries, DDL, stored procedures, views, transactions, and optimization.

## Variant detection

Identify the dialect from context. Check in this order:

1. Explicit mention ("postgres", "mysql", "sqlite", etc.)
2. File extensions or migration tool conventions (`.sql`, Flyway prefix `V1__`, Liquibase)
3. Code imports (`pg`, `mysql2`, `sqlite3`, `pyodbc`)
4. Infrastructure mentions ("RDS Postgres", "Azure SQL", etc.)
5. If genuinely ambiguous: ask once — "Which database are you using? (PostgreSQL, MySQL, MSSQL, SQLite, Oracle)"

Once identified, load the dialect-specific reference for syntax details:

- **PostgreSQL** → read `references/postgres.md`
- **MySQL / MariaDB** → read `references/mysql.md`
- **MSSQL / SQL Server** → read `references/mssql.md`
- **SQLite** → read `references/sqlite.md`
- **Oracle** → read `references/oracle.md`

## Output format

Always produce:

1. **The SQL** — formatted, readable, with comments
2. **Explanation** — what it does and why the approach was chosen (1–3 sentences per non-trivial decision)
3. **Performance notes** — indexes this query benefits from, or will create
4. **Edge cases** — NULLs, empty sets, concurrent modification

## SQL quality standards

### Formatting

```sql
-- Use uppercase for SQL keywords
-- Align columns in SELECT lists
SELECT
    u.id,
    u.email,
    u.created_at,
    COUNT(o.id)  AS order_count,
    SUM(o.total) AS lifetime_value
FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
WHERE
    u.deleted_at IS NULL
    AND u.created_at >= '2024-01-01'
GROUP BY
    u.id,
    u.email,
    u.created_at
ORDER BY
    lifetime_value DESC NULLS LAST
LIMIT 100;
```

### CTEs over subqueries

Prefer CTEs for readability. Use subqueries only when a CTE would be materially slower.

```sql
WITH active_users AS (
    SELECT id, email
    FROM users
    WHERE deleted_at IS NULL
),
recent_orders AS (
    SELECT user_id, COUNT(*) AS count
    FROM orders
    WHERE created_at >= NOW() - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT
    u.email,
    COALESCE(ro.count, 0) AS orders_last_30_days
FROM active_users u
    LEFT JOIN recent_orders ro ON ro.user_id = u.id;
```

### NULL handling

- Use `IS NULL` / `IS NOT NULL`, never `= NULL`
- Use `COALESCE` for defaults, explain the semantic choice
- Document nullable columns in comments

### Transactions

Wrap multi-statement mutations in explicit transactions with rollback on error:

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = :from_id;
UPDATE accounts SET balance = balance + 100 WHERE id = :to_id;

-- Verify no negative balances
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM accounts WHERE balance < 0 AND id IN (:from_id, :to_id)) THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;
END $$;

COMMIT;
```

### Parameterized queries

Always use parameters (`$1`, `:name`, `?`) instead of string interpolation. Note which style applies to the dialect.

### Index awareness

After writing a query, note which indexes it relies on:

```sql
-- This query benefits from: idx_orders_user_id, idx_orders_created_at
-- If these don't exist: CREATE INDEX idx_orders_user_id ON orders(user_id);
```

## Common patterns by dialect

Read the relevant `references/<dialect>.md` file for:

- Type system quirks (e.g., Postgres JSONB, MySQL ENUM pitfalls, SQLite type affinity)
- Pagination idioms (OFFSET vs keyset)
- EXPLAIN / execution plan syntax
- Full-text search capabilities
- Date/time functions
- Upsert syntax (`ON CONFLICT`, `ON DUPLICATE KEY UPDATE`, `MERGE`)

## Query optimization checklist

When asked to optimize a query, check:

- [ ] Are all JOIN columns indexed?
- [ ] Is there an index on all WHERE clause columns used for filtering (not full-table-scan)?
- [ ] Are there unnecessary subqueries that could be CTEs or JOINs?
- [ ] Is `SELECT *` used where specific columns would suffice?
- [ ] For pagination: is OFFSET used on large tables? (switch to keyset if so)
- [ ] Is `LIKE '%value%'` used? (leading wildcard prevents index use — consider full-text search)
- [ ] Are there implicit type casts in WHERE clauses causing index skips?
