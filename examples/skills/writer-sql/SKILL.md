---
name: writer-sql
description: >
  Design database schemas and write or optimize SQL queries. Routes schema work, query writing,
  dialect guidance, normalization, indexing, and troubleshooting to the right reference.
author: Oleg Shulyakov
license: MIT
version: 1.1.0
---

# writer-sql (router)

A **router** skill to write **production-quality SQL** for OLTP databases. Route to the appropriate SQL sub-skill based on the user's request.

## Task detection

### Top-level routing

| If the user asks...                                 | Route to...            |
| --------------------------------------------------- | ---------------------- |
| Design a database schema for an e-commerce platform | `references/design.md` |
| What tables do I need for a blog?                   | `references/design.md` |
| Normalize this into a schema                        | `references/design.md` |
| Write a query to find top 10 customers by revenue   | `references/common.md` |
| Optimize this slow join                             | `references/common.md` |
| How do I use CTEs?                                  | `references/common.md` |

After routing to `references/common.md`, detect the dialect and load the corresponding dialect reference (see below).

### Dialect-specific routing

When the question targets a specific database — load its reference directly:

| "How do I..." example                      | Read this first          |
| ------------------------------------------ | ------------------------ |
| Do full-text search in Postgres?           | `references/postgres.md` |
| Write a JSONB query                        | `references/postgres.md` |
| Postgres upsert with ON CONFLICT           | `references/postgres.md` |
| Write a MySQL upsert with ON DUPLICATE KEY | `references/mysql.md`    |
| MySQL JSON columns and virtual indexes     | `references/mysql.md`    |
| utf8mb4 charset setup                      | `references/mysql.md`    |
| Write a T-SQL stored procedure             | `references/mssql.md`    |
| MSSQL pagination with OFFSET-FETCH         | `references/mssql.md`    |
| SQL Server MERGE upsert                    | `references/mssql.md`    |
| Enable WAL mode in SQLite                  | `references/sqlite.md`   |
| SQLite FTS5 full-text search               | `references/sqlite.md`   |
| SQLite type affinity                       | `references/sqlite.md`   |
| Write a PL/SQL procedure                   | `references/oracle.md`   |
| Oracle MERGE upsert                        | `references/oracle.md`   |
| Oracle row limiting clause                 | `references/oracle.md`   |

## Output format

Always produce:

1. **The SQL** — formatted, readable, with comments
2. **Explanation** — what it does and why the approach was chosen (1–3 sentences per non-trivial decision)
3. **Performance notes** — indexes this query benefits from, or will create
4. **Edge cases** — NULLs, empty sets, concurrent modification
