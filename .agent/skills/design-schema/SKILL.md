---
name: design-schema
description: >
  Produces a normalized relational database schema with tables, columns, types, primary keys, foreign keys,
  and indexes. Use this skill whenever the user wants to design a database schema, define tables and relationships,
  model a data structure in SQL, create an entity-relationship model, design a database for a feature or system,
  or asks "how should I structure the database?" Also trigger for "what tables do I need?", "design the data model",
  or "normalize this into a schema". Distinct from writer-sql (which writes queries against an existing schema)
  and writer-migration (which writes migration scripts for an existing schema).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# design-schema

Produce a **normalized relational database schema** with DDL, relationship documentation, and design rationale.

## What makes a great schema

A good schema encodes business rules structurally so they can't be violated at the application layer. It anticipates common query patterns and pre-optimizes with the right indexes. It's normalized enough to avoid update anomalies, but not over-normalized to the point of making every query a 6-way join.

## Detect the SQL dialect

Identify the target database from context:

| Signal                                                       | Dialect                                    |
| ------------------------------------------------------------ | ------------------------------------------ |
| "postgres", `.sql` with Postgres types, `JSONB`, `uuid-ossp` | PostgreSQL                                 |
| "mysql", "mariadb", `AUTO_INCREMENT`                         | MySQL / MariaDB                            |
| "sqlite", mobile app, embedded                               | SQLite                                     |
| "mssql", "sql server", T-SQL                                 | MSSQL                                      |
| "oracle"                                                     | Oracle                                     |
| Ambiguous / not mentioned                                    | Default to PostgreSQL; note the assumption |

## Information gathering

Extract:

- **Domain** and core entities (e.g., e-commerce: products, orders, customers)
- **Key relationships** (one-to-many, many-to-many, hierarchical)
- **Cardinality constraints** (nullable FKs, required fields)
- **Query patterns** (what queries will be most frequent — guides index design)
- **Scale hints** (millions of rows? partitioning needed?)
- **Special requirements**: soft deletes, multi-tenancy, audit log, temporal data

## Output format

### Part 1: Entity-Relationship Summary

```
## Entity-Relationship Overview

### Entities
- **[Entity]** — [1-line description]

### Relationships
- [Entity A] has many [Entity B] (via `[table].fk_[entity_a]_id`)
- [Entity A] and [Entity B] are many-to-many (via `[junction_table]`)
```

### Part 2: DDL

Produce `CREATE TABLE` statements in dependency order (referenced tables first).

**PostgreSQL template:**

```sql
-- ============================================================
-- [Schema Name]: [Domain Description]
-- Generated: [YYYY-MM-DD]
-- Dialect: PostgreSQL 15+
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ------------------------------------------------------------
-- [table_name]
-- [1-line description of what this table stores]
-- ------------------------------------------------------------
CREATE TABLE [table_name] (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- [Domain-specific columns]
    [column_name] [TYPE] NOT NULL,           -- [inline comment explaining business rule]
    [column_name] [TYPE],                    -- nullable: [reason]

    -- Soft delete support
    deleted_at    TIMESTAMPTZ,               -- NULL = active

    -- Audit
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Constraints
    CONSTRAINT [table_name]_[rule]_chk CHECK ([condition]),
    CONSTRAINT [table_name]_[unique_field]_uq UNIQUE ([field])
);

-- Indexes
CREATE INDEX [table_name]_[col]_idx ON [table_name] ([col]);
-- For soft deletes: only index active rows
CREATE INDEX [table_name]_[col]_active_idx ON [table_name] ([col]) WHERE deleted_at IS NULL;

-- ------------------------------------------------------------
-- [junction_table] — many-to-many between [A] and [B]
-- ------------------------------------------------------------
CREATE TABLE [junction_table] (
    [entity_a]_id  UUID NOT NULL REFERENCES [table_a](id) ON DELETE CASCADE,
    [entity_b]_id  UUID NOT NULL REFERENCES [table_b](id) ON DELETE CASCADE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY ([entity_a]_id, [entity_b]_id)
);
```

### Part 3: Relationship Matrix

| Table   | Column           | References     | On Delete                     | Notes              |
| ------- | ---------------- | -------------- | ----------------------------- | ------------------ |
| [child] | `fk_[parent]_id` | `[parent](id)` | CASCADE / SET NULL / RESTRICT | [when to use each] |

### Part 4: Index Rationale

| Index               | Columns   | Purpose                     |
| ------------------- | --------- | --------------------------- |
| `[table]_[col]_idx` | `([col])` | [Which query this supports] |

### Part 5: Design Decisions

Document key choices:

- **Why UUID vs serial?** UUIDs enable distributed ID generation and prevent ID enumeration. Use BIGSERIAL if insert volume is extreme and you don't need distribution.
- **Why soft delete?** If the entity has audit / compliance needs or is referenced by other records that should remain consistent.
- **Normalization level:** Note if you've intentionally denormalized something and why.

## Design guidelines

**Naming:**

- Table names: `snake_case`, plural (`orders`, `order_items`)
- Column names: `snake_case`, singular
- FK columns: `[referenced_table_singular]_id` (e.g., `user_id`, `order_id`)
- Constraint names: `[table]_[description]_[type]` (e.g., `orders_status_chk`, `users_email_uq`)
- Index names: `[table]_[col(s)]_idx`

**Type selection:**

- IDs: `UUID` (with `uuid_generate_v4()` default) unless high-volume serial is needed
- Text: `TEXT` for variable length (no magic VARCHAR lengths unless there's a business rule)
- Money: `NUMERIC(15,4)` — never `FLOAT`
- Status/enum: `TEXT` with a CHECK constraint or a proper `ENUM` type, noted
- Timestamps: `TIMESTAMPTZ` (always timezone-aware)

**Standard columns on every table:**

- `id UUID PRIMARY KEY`
- `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`
- `deleted_at TIMESTAMPTZ` — only if soft delete is appropriate

**Referential integrity:**

- All FKs should be explicit with ON DELETE behavior stated
- CASCADE: child rows are meaningless without the parent
- SET NULL: child rows can exist without the parent (nullable FK)
- RESTRICT: prevent deletion if children exist (default safe choice)

**Indexing strategy:**

- Index every FK column (Postgres doesn't do this automatically)
- Index columns that appear frequently in WHERE clauses on large tables
- Partial indexes for soft-delete patterns: `WHERE deleted_at IS NULL`
- Avoid over-indexing write-heavy tables

## Scale / special patterns

Add these sections only if relevant:

**Multi-tenancy:**
Add `tenant_id UUID NOT NULL REFERENCES tenants(id)` to every tenant-scoped table. Add `tenant_id` as the first column of composite indexes.

**Audit log:**

```sql
CREATE TABLE audit_log (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name    TEXT NOT NULL,
    record_id     UUID NOT NULL,
    action        TEXT NOT NULL CHECK (action IN ('INSERT','UPDATE','DELETE')),
    old_values    JSONB,
    new_values    JSONB,
    changed_by    UUID REFERENCES users(id),
    changed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Temporal / history tables:**
If the user needs full history of changes, note this is a separate pattern (temporal tables or CDC) and offer to design it.
