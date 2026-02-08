# Database Debugging Playbook

This document is a "First Responder" guide for diagnosing and resolving database performance issues, errors, and bottlenecks in our PostgreSQL (Supabase) environment.

---

## 1. The "Vital Signs" Check
Before diving into code, check the database pulse.

### 1.1 Cache Hit Ratio
If this is below **99%**, your RAM is too low or your working set is too large. You are hitting the disk (slow).

```sql
SELECT 
  sum(heap_blks_read) as disk_reads,
  sum(heap_blks_hit)  as cache_hits,
  round(sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read) + 1)::numeric, 4) as hit_ratio
FROM pg_statio_user_tables;
```

### 1.2 Active Connections
Are we hitting connection limits?

```sql
SELECT state, count(*) 
FROM pg_stat_activity 
GROUP BY state;
```
*   `active`: Currently running a query. High numbers here indicate a bottleneck.
*   `idle in transaction`: **DANGER**. The application opened a transaction but isn't doing anything. This holds locks and prevents vacuuming.

### 1.3 Blocked Queries
Find who is blocking whom.

```sql
SELECT
    activity.pid,
    activity.usename,
    activity.query,
    blocking.pid AS blocking_id,
    blocking.query AS blocking_query
FROM pg_stat_activity AS activity
JOIN pg_blocking_pids(activity.pid) AS blockers ON blocking.pid = blockers.blocking_pids[1]
JOIN pg_stat_activity AS blocking ON blocking.pid = blockers.blocking_pids[1];
```

---

## 2. Slow Query Investigation

The `pg_stat_statements` extension is your best friend. It records the performance of all queries executed.

### 2.1 Top 5 Most Expensive Queries (Total Time)
Optimizing these gives the best ROI for system-wide load.

```sql
SELECT 
    round(total_exec_time::numeric, 2) as total_time_ms,
    calls,
    round(mean_exec_time::numeric, 2) as avg_time_ms,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 5;
```

### 2.2 Top 5 Slowest Queries (Per Call)
These affect individual user latency (the "spinning wheel" effect).

```sql
SELECT 
    round(mean_exec_time::numeric, 2) as avg_time_ms,
    calls,
    query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 5;
```

---

## 3. Explaining the Plan

When you identify a slow query, prefix it with `EXPLAIN (ANALYZE, BUFFERS)` to see exactly what Postgres did.

### 3.1 Key Terms in EXPLAIN
*   **`Seq Scan`**: **Bad** (usually). It read the whole table. Missing index?
*   **`Index Scan`**: **Good**. It used the index to find the row.
*   **`Index Only Scan`**: **Excellent**. It got the data straight from the index without touching the heap (table).
*   **`Bitmap Heap Scan`**: **Okay**. Used an index to find locations, then grabbed them in batches.
*   **`Buffers: shared hit=N`**: How many 8kb pages came from RAM.
*   **`Buffers: shared read=N`**: How many 8kb pages came from DISK (Slow!).

### 3.2 Common Antipatterns

#### The "Missing Index"
```
Seq Scan on large_table (cost=0.00..99999.00 rows=500 width=100)
Filter: (tenant_id = '...')
```
**Fix**: Add an index on `tenant_id`.

#### The "Function Wrapper" (Non-SARGable)
```sql
-- BAD: Postgres cannot use index on created_at
SELECT * FROM orders WHERE DATE(created_at) = '2024-01-01';

-- GOOD: Index can be used
SELECT * FROM orders WHERE created_at >= '2024-01-01 00:00:00' 
                       AND created_at <  '2024-01-02 00:00:00';
```

#### The "Distinct Bomb"
```sql
-- SLOW: Sorts millions of rows to find unique values
SELECT DISTINCT status FROM orders;

-- FAST: Use a recursive CTE or separate lookup table if cardinality is low
```

---

## 4. Emergency Actions

### 4.1 Killing a Runaway Query
If a query is consuming 100% CPU and bringing the site down:

1.  Find the `pid` from `pg_stat_activity`.
2.  Kill it.

```sql
-- Polite kill (SIGINT)
SELECT pg_cancel_backend(pid);

-- Force kill (SIGTERM) - Use if polite kill fails
SELECT pg_terminate_backend(pid);
```

### 4.2 Maintenance
If performance degrades over time, the table stats might be stale, causing the planner to make bad choices.

```sql
-- Update statistics for a specific table
ANALYZE VERBOSE table_name;

-- Reclaim space and update stats (heavier)
VACUUM (VERBOSE, ANALYZE) table_name;
```

---

## 5. Index Maintenance

### 5.1 Finding Unused Indexes
Indexes slow down writes. If you don't read from them, delete them.

```sql
SELECT
    schemaname || '.' || relname AS table,
    indexrelname AS index,
    pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
    idx_scan as index_scans
FROM pg_stat_user_indexes i
JOIN pg_index using (indexrelid)
WHERE idx_scan = 0
AND indisunique IS FALSE;
```

### 5.2 Finding Bloated Tables
Tables with high dead tuple counts need vacuuming.

```sql
SELECT 
    relname AS TableName, 
    n_live_tup AS LiveTuples, 
    n_dead_tup AS DeadTuples,
    round(n_dead_tup::numeric / (n_live_tup+n_dead_tup+1)::numeric, 2) as dead_ratio
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
```
