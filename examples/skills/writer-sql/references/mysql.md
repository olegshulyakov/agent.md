# MySQL / MariaDB Reference

## Key types

- `BIGINT UNSIGNED AUTO_INCREMENT` — primary keys (or `CHAR(36)` for UUID)
- `VARCHAR(n)` — always specify length (required by MySQL)
- `DECIMAL(p,s)` — exact decimals (not FLOAT for money)
- `DATETIME` / `TIMESTAMP` — TIMESTAMP auto-converts to UTC; DATETIME stores as-is
- `JSON` — native JSON type (MySQL 5.7.8+, MariaDB 10.2+)
- `TEXT` / `MEDIUMTEXT` / `LONGTEXT` — for large text (no indexes without prefix)
- `TINYINT(1)` — booleans (MySQL has no native BOOLEAN, maps to TINYINT)

## Upsert

```sql
INSERT INTO users (email, name, updated_at)
VALUES (?, ?, NOW())
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    updated_at = NOW();
```

## Auto-increment and UUIDs

```sql
-- Integer PK (simpler, better performance)
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ...
);

-- UUID PK (distributed-safe)
CREATE TABLE users (
    id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,
    ...
) ENGINE=InnoDB;
```

## Storage engines

- Always use `ENGINE=InnoDB` (transactions, foreign keys, row-level locking)
- `ENGINE=MyISAM` is legacy — never use for new tables

## Character set

```sql
-- Database level
CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Table level (always explicit)
CREATE TABLE articles (
    ...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

`utf8mb4` is required for emoji and full Unicode support. `utf8` in MySQL is 3-byte only.

## JSON columns

```sql
CREATE TABLE events (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payload JSON NOT NULL,
    -- Virtual columns for JSON key indexing:
    event_type VARCHAR(50) AS (JSON_UNQUOTE(payload->>'$.type')) STORED,
    INDEX idx_events_type (event_type)
);

-- Query
SELECT * FROM events WHERE JSON_UNQUOTE(payload->>'$.userId') = ?;
```

## Full-text search

```sql
-- Index (MyISAM supports this; InnoDB from 5.6+)
ALTER TABLE articles ADD FULLTEXT(title, body);

-- Query
SELECT *, MATCH(title, body) AGAINST (? IN BOOLEAN MODE) AS score
FROM articles
WHERE MATCH(title, body) AGAINST (? IN BOOLEAN MODE)
ORDER BY score DESC;
```

## EXPLAIN

```sql
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE user_id = ?;
```

## Pagination — keyset preferred

```sql
-- Offset (avoid on large tables)
SELECT * FROM orders ORDER BY created_at DESC LIMIT ? OFFSET ?;

-- Keyset
SELECT * FROM orders
WHERE created_at < ?  -- cursor
ORDER BY created_at DESC
LIMIT ?;
```

## Common gotchas

- `GROUP BY` in MySQL 5.7+ with `ONLY_FULL_GROUP_BY` mode: all non-aggregate SELECT columns must be in GROUP BY
- `ENUM` type: changes to ENUM values require ALTER TABLE (expensive on large tables); prefer VARCHAR + CHECK constraint or a lookup table
- String comparison is case-insensitive by default (depends on collation)
- No `RETURNING` clause — use `LAST_INSERT_ID()` after INSERT
