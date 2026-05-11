---
name: report-db-health
description: >
  Produces a database health report covering slow queries, index usage, table bloat, connection pool
  status, and replication lag. Use this skill whenever the user wants to assess database performance,
  investigate slow queries, check index effectiveness, analyze table bloat, review database health,
  identify performance bottlenecks in their database, or asks to "generate a DB health report",
  "investigate slow queries", "check index usage", "analyze table bloat", "review database performance",
  "what's wrong with my database", "check replication lag", or "find missing indexes". Also trigger
  for "DB performance audit", "PostgreSQL health check", "MySQL slow query analysis", and
  "database optimization report". Distinct from writer-sql (writes queries) and design-schema
  (designs schema structure).
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# report-db-health

Produce a **database health report** with query diagnostics, index analysis, bloat assessment, and actionable recommendations.

## Supported databases

Detect from context: **PostgreSQL** (default), **MySQL/MariaDB**, **MSSQL**, **SQLite**.

Generate the appropriate diagnostic queries for the detected dialect.

## Information gathering

From context, identify:
- **Database engine and version**: PostgreSQL 15? MySQL 8?
- **Evidence provided**: Slow query logs, `pg_stat_*` data, EXPLAIN output, monitoring screenshots?
- **Concern**: Slow queries, high CPU, high connections, storage, replication?
- **Scale**: Approximate table sizes, row counts, QPS?

If no evidence is provided, generate the diagnostic queries the user should run, then explain how to interpret results.

## Output format

```markdown
# Database Health Report

**Database:** [PostgreSQL/MySQL/MSSQL] [version]
**Database name:** [db_name]
**Report date:** [date]
**Assessed by:** [name]
**Overall health:** 🔴 Critical / 🟠 Degraded / 🟡 Fair / 🟢 Healthy

---

## Executive Summary

[3–5 sentences: Overall health, top 2–3 findings, most urgent action items.]

---

## 1. Slow Query Analysis

### Top Slow Queries

Run this to identify the worst offenders (PostgreSQL):

```sql
-- Requires pg_stat_statements extension
SELECT
    round(total_exec_time::numeric, 2)     AS total_ms,
    round(mean_exec_time::numeric, 2)      AS avg_ms,
    round(stddev_exec_time::numeric, 2)    AS stddev_ms,
    calls,
    round((100.0 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS pct_total,
    left(query, 120)                       AS query_preview
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

### Findings

| Rank | Query | Avg (ms) | Calls/day | Total Time | Issue |
|------|-------|----------|-----------|------------|-------|
| 1 | `SELECT * FROM orders WHERE customer_id = ...` | [X] | [N] | [X%] | Missing index on customer_id |
| 2 | `UPDATE inventory SET ...` | [X] | [N] | [X%] | Lock contention |

### EXPLAIN Analysis

For problematic query [paste query here]:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
[your query here];
```

**Reading the plan:**
- `Seq Scan` on large table → likely missing index
- `Rows Removed by Filter: N` much larger than rows returned → poor selectivity
- `Buffers: shared hit=X read=Y` — high `read` value → data not in cache
- Nested loop with many iterations on outer side → N+1 query pattern

---

## 2. Index Analysis

### Unused Indexes (candidates for removal)

```sql
-- PostgreSQL: indexes never or rarely scanned
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan < 50
ORDER BY pg_relation_size(indexrelid) DESC;
```

| Index | Table | Scans | Size | Recommendation |
|-------|-------|-------|------|----------------|
| `idx_orders_legacy_status` | orders | 3 | 450 MB | 🔴 DROP — unused, large |
| `idx_users_temp` | users | 12 | 50 MB | 🟡 Monitor — rarely used |

### Missing Indexes

```sql
-- PostgreSQL: tables with high sequential scans suggesting missing indexes
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    round(seq_scan::numeric / nullif(idx_scan + seq_scan, 0) * 100, 1) AS seq_scan_pct
FROM pg_stat_user_tables
WHERE seq_scan > 100
ORDER BY seq_tup_read DESC
LIMIT 20;
```

| Table | Seq Scans | Seq Rows Read | Recommended Index |
|-------|-----------|---------------|-------------------|
| `orders` | 5,203 | 48M | `CREATE INDEX idx_orders_customer ON orders(customer_id);` |
| `events` | 1,102 | 15M | `CREATE INDEX idx_events_created ON events(created_at DESC);` |

### Duplicate / Redundant Indexes

```sql
-- Identify redundant indexes (subset indexes)
SELECT
    a.indexname AS idx_a, b.indexname AS idx_b,
    a.tablename
FROM pg_indexes a
JOIN pg_indexes b ON a.tablename = b.tablename AND a.indexname <> b.indexname
WHERE position(a.indexdef IN b.indexdef) > 0;
```

---

## 3. Table Bloat

Table bloat occurs when dead rows from UPDATEs/DELETEs are not reclaimed (PostgreSQL MVCC).

```sql
-- Approximate table bloat (PostgreSQL)
SELECT
    schemaname, tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    n_dead_tup,
    round(n_dead_tup::numeric / nullif(n_live_tup + n_dead_tup, 0) * 100, 1) AS dead_pct,
    last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;
```

| Table | Live Rows | Dead Rows | Dead % | Last Autovacuum | Action |
|-------|-----------|-----------|--------|----------------|--------|
| `events` | 2M | 800K | 40% | 3 days ago | `VACUUM ANALYZE events;` |
| `sessions` | 50K | 200K | 80% | Never | 🔴 `VACUUM FULL sessions;` |

**Autovacuum tuning** (if bloat is chronic):
```sql
-- Per-table autovacuum tuning
ALTER TABLE events SET (
    autovacuum_vacuum_scale_factor = 0.01,  -- Vacuum at 1% dead rows
    autovacuum_analyze_scale_factor = 0.005
);
```

---

## 4. Connection Pool Status

```sql
-- PostgreSQL connection state
SELECT state, count(*), max(now() - state_change) AS max_duration
FROM pg_stat_activity
WHERE datname = current_database()
GROUP BY state
ORDER BY count DESC;

-- Long-running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity
WHERE state <> 'idle' AND now() - pg_stat_activity.query_start > interval '30 seconds'
ORDER BY duration DESC;
```

| State | Count | Concern |
|-------|-------|---------|
| active | [N] | Normal |
| idle in transaction | [N] | 🟠 Investigate if > 10 — possible connection leak |
| waiting | [N] | 🔴 Lock contention |

**Recommendations:**
- [ ] Set `statement_timeout = '30s'` to kill runaway queries
- [ ] Set `idle_in_transaction_session_timeout = '60s'` to reclaim leaked connections
- [ ] Connection pool (PgBouncer) recommended if `max_connections` is routinely > 80% utilized

---

## 5. Replication Lag (if applicable)

```sql
-- PostgreSQL replication status
SELECT
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication;
```

| Replica | Write Lag | Flush Lag | Replay Lag | Status |
|---------|-----------|-----------|------------|--------|
| [IP] | [X ms] | [X ms] | [X ms] | 🟢 Healthy / 🔴 Critical |

---

## 6. Storage Analysis

```sql
-- Top tables by size
SELECT
    schemaname, tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table,
    pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename)) AS indexes
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 15;
```

---

## Recommendations Summary

### 🔴 Immediate (this sprint)

- [ ] **Create index on `orders.customer_id`** — eliminates full seq scan on [N]M row table
- [ ] **VACUUM FULL `sessions` table** — 80% bloat; schedule during low traffic window
- [ ] **Investigate idle-in-transaction connections** — potential connection leak in [service]

### 🟠 Short-term (this quarter)

- [ ] **Drop [N] unused indexes** ([list]) — free up [X GB] of storage
- [ ] **Tune autovacuum on `events` table** — chronic bloat suggests vacuum not keeping up
- [ ] **Add PgBouncer** — connection pooling to reduce overhead at high concurrency

### 🟡 Monitor

- [ ] **Replication lag on replica [IP]** — within SLA but trending up; investigate write volume
- [ ] **Cache hit rate** — currently [X%]; target > 99% for OLTP workloads

---

## Diagnostic Query Pack

If you want to run all diagnostics at once, run each query in `psql` or your preferred DB client and paste results back for interpretation.
```

## Calibration

- **No data provided**: Generate the diagnostic queries + explanation of what each reveals
- **Query log provided**: Analyze and rank; identify most impactful queries to optimize
- **EXPLAIN output provided**: Read the plan and provide specific optimization recommendations
- **General health check**: Run all five sections (queries, indexes, bloat, connections, storage)
