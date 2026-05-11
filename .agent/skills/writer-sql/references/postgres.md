# PostgreSQL Reference

## Key types

- `UUID` — primary/foreign keys (use `uuid_generate_v4()` or `gen_random_uuid()` in PG 13+)
- `TEXT` — variable-length strings (no arbitrary VARCHAR limits)
- `NUMERIC(p,s)` — exact decimal (money, quantities)
- `TIMESTAMPTZ` — always use timezone-aware timestamps
- `JSONB` — structured JSON data with indexing support
- `BOOLEAN` — true/false (not 0/1)
- `BIGINT` — for counts and large IDs when UUID overhead matters

## Upsert

```sql
INSERT INTO users (email, name)
VALUES ($1, $2)
ON CONFLICT (email)
DO UPDATE SET
    name = EXCLUDED.name,
    updated_at = NOW()
RETURNING *;
```

## CTEs with modification

```sql
WITH inserted AS (
    INSERT INTO audit_log (action, table_name, record_id)
    VALUES ('create', 'users', $1)
    RETURNING id
)
SELECT u.*, al.id AS audit_id
FROM users u
JOIN inserted al ON true
WHERE u.id = $1;
```

## JSONB queries

```sql
-- Index JSONB key
CREATE INDEX idx_users_metadata_role ON users ((metadata->>'role'));

-- Query JSONB
SELECT * FROM users
WHERE metadata->>'role' = 'admin'
AND metadata @> '{"active": true}';

-- Update nested key
UPDATE users
SET metadata = jsonb_set(metadata, '{preferences,theme}', '"dark"')
WHERE id = $1;
```

## Full-text search

```sql
-- Index
CREATE INDEX idx_articles_search ON articles
USING GIN(to_tsvector('english', title || ' ' || body));

-- Query
SELECT *, ts_rank(to_tsvector('english', title || ' ' || body), query) AS rank
FROM articles, to_tsquery('english', $1) query
WHERE to_tsvector('english', title || ' ' || body) @@ query
ORDER BY rank DESC;
```

## Pagination

```sql
-- Offset (simple, degrades on large tables)
SELECT * FROM orders ORDER BY created_at DESC LIMIT $1 OFFSET $2;

-- Keyset / cursor (preferred for large tables)
SELECT * FROM orders
WHERE created_at < $1  -- cursor value from previous page
ORDER BY created_at DESC
LIMIT $2;
```

## EXPLAIN ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE user_id = $1;
```

## Window functions

```sql
SELECT
    user_id,
    order_id,
    amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at) AS running_total,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
FROM orders;
```

## Array operations

```sql
-- Array column
CREATE TABLE tags (id UUID PRIMARY KEY, post_id UUID, names TEXT[]);

SELECT * FROM tags WHERE 'postgresql' = ANY(names);
SELECT * FROM tags WHERE names @> ARRAY['postgresql', 'sql'];
```

## Constraint naming convention

```sql
CONSTRAINT [table]_[col]_[type]
-- Examples:
CONSTRAINT orders_status_chk CHECK (status IN ('pending','completed','cancelled'))
CONSTRAINT users_email_uq UNIQUE (email)
```
