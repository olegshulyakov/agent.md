# SQLite Reference

## Key concepts

SQLite has **type affinity** — not strict types. Declared types are suggestions, not enforcements (unless STRICT mode is used).

### Type affinity rules

| Declared type contains | Affinity |
|----------------------|---------|
| INT | INTEGER |
| CHAR, CLOB, TEXT | TEXT |
| BLOB or nothing | BLOB |
| REAL, FLOA, DOUB | REAL |
| Everything else | NUMERIC |

### Strict mode (SQLite 3.37+)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    score REAL
) STRICT;
```

Use STRICT for new tables to get actual type enforcement.

## Primary keys and ROWID

```sql
-- INTEGER PRIMARY KEY is an alias for ROWID (fast)
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- WITHOUT ROWID: good for small, frequently-read tables without rowid access
CREATE TABLE kv_store (
    key TEXT NOT NULL,
    value BLOB,
    PRIMARY KEY (key)
) WITHOUT ROWID;
```

## UUID simulation

SQLite has no native UUID type. Use TEXT:

```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(4))) || '-' ||
        lower(hex(randomblob(2))) || '-4' ||
        substr(lower(hex(randomblob(2))),2) || '-' ||
        substr('89ab',abs(random()) % 4 + 1, 1) ||
        substr(lower(hex(randomblob(2))),2) || '-' ||
        lower(hex(randomblob(6)))),
    ...
);
```

Or generate UUIDs in application code and insert as TEXT.

## JSON (SQLite 3.38+)

```sql
-- JSON functions
SELECT json_extract(payload, '$.userId') AS user_id FROM events;
SELECT json_object('id', id, 'name', name) AS json FROM users;

-- JSON in WHERE
SELECT * FROM events WHERE json_extract(payload, '$.type') = 'login';
```

## Full-text search (FTS5)

```sql
-- Create virtual FTS table
CREATE VIRTUAL TABLE articles_fts USING fts5(title, body, content=articles, content_rowid=id);

-- Trigger to keep in sync
CREATE TRIGGER articles_ai AFTER INSERT ON articles BEGIN
    INSERT INTO articles_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;

-- Query
SELECT a.* FROM articles a
JOIN articles_fts f ON f.rowid = a.id
WHERE articles_fts MATCH 'sqlite full-text'
ORDER BY rank;
```

## Limitations to be aware of

- **No ALTER TABLE ADD COLUMN with constraints**: only bare ADD COLUMN is supported (no NOT NULL with no default, no UNIQUE)
- **No DROP COLUMN** (before 3.35): must recreate the table
- **No RIGHT JOIN or FULL OUTER JOIN** (before 3.39)
- **Single writer**: SQLite uses file-level locking. WAL mode helps for concurrent readers

## WAL mode (recommended for most apps)

```sql
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;  -- good tradeoff for WAL
PRAGMA foreign_keys=ON;     -- MUST enable explicitly — off by default!
PRAGMA cache_size=-64000;   -- 64MB page cache
```

Always enable `foreign_keys=ON` at connection open — SQLite ignores FK constraints by default.

## Upsert

```sql
INSERT INTO users (email, name, updated_at)
VALUES (?, ?, datetime('now'))
ON CONFLICT(email)
DO UPDATE SET
    name = excluded.name,
    updated_at = excluded.updated_at;
```

## Date/time

SQLite stores dates as TEXT (ISO 8601), REAL (Julian day), or INTEGER (Unix timestamp).

```sql
-- Insert current time
INSERT INTO events (occurred_at) VALUES (datetime('now'));

-- Query by date range
SELECT * FROM events
WHERE occurred_at BETWEEN datetime('now', '-7 days') AND datetime('now');
```
