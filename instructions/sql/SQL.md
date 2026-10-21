<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 4af1189d-7fa1-4561-9bd3-5524c709265e
Created: 2026
-->

<!-- AGENT: SQL conventions and task examples; load only when this language is in scope. -->

# SQL instructions

Read this guide when the task changes SQL source or its language-specific build and test configuration.
Examples in instruction documents do not make a language part of the consuming project.
Start with references, formatting, naming, and file organization when those sections exist.
Read task sections as needed. Read pattern examples only for patterns selected during planning.
Shared policies remain in the topic guides. Read only the topics that apply to the task.
Do not weaken a shared requirement because this guide omits it.

Shared rules: [Style](../CODING_STYLE.md), [Comments](../COMMENTING.md), [Markers](../MARKERS.md), [Testing](../TESTING.md), [Logging](../LOGGING.md), [Performance](../PERFORMANCE.md), [Patterns](../GOF_PATTERNS.md).

Apply [shared style](../CODING_STYLE.md), including Allman braces, four-space indentation, and one type per file.
Use only the grammar exceptions stated in this guide.
If an example shows several top-level types, put each type in its own file in production.
Examples may omit surrounding project types or test fixtures. Use the repository's configured dependencies and contracts.

Read by task: [Construction](#construction), [Comments](#comments), [Testing](#testing), [Performance](#performance).

Use [PERSISTENCE.md](../PERSISTENCE.md) for shared transaction, migration, and stored-data integrity rules.

## Construction

Use the configured database engine and migration convention. Do not apply PostgreSQL-specific advice to another database engine.

## Comments

Comment tables, columns, and complex queries:

```sql
-- Tenant table: Root entity for multi-tenancy isolation
-- All user data is partitioned by tenant_id for security and performance
CREATE TABLE tenants (
    id UUID PRIMARY KEY,           -- Immutable identifier
    name VARCHAR(255) NOT NULL,    -- Display name, user-editable
    slug VARCHAR(100) UNIQUE,      -- URL-safe identifier for routing
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Fetch active subscriptions with plan details
-- PERF: Uses covering index on (tenant_id, status) for the WHERE clause
SELECT s.*, p.name as plan_name, p.price
FROM subscriptions s
JOIN plans p ON s.plan_id = p.id
WHERE s.tenant_id = @tenantId
  AND s.status = 'active';
```

## Testing

Use [SQL and database migration checks](../TESTING.md#sql-and-database-migrations).
Verify schema changes, data integrity, stored routines, and rollback behavior against the actual database engine.

## Performance

### 4.1 Architecture: Multi-Tenancy & Scaling
*   **Hybrid Tenant Model**:
    *   **Standard Tenants (The 99%)**: Use **Row-Level Security (RLS)** in shared tables. This maximizes resource utilization and cache hits.
        *   *Requirement*: Every table must have a `tenant_id` column.
        *   *Requirement*: RLS policies must be enabled on all tables.
    *   **VIP Tenants (Noisy Neighbors)**: For tenants exceeding threshold (e.g., >100GB data or >1000 TPS), use **Table Partitioning** or move to a dedicated database instance. Do not penalize small tenants for the load of large ones.
*   **Connection Pooling (Critical)**:
    *   **PgBouncer is Mandatory**: Direct connections to Postgres are expensive (~10MB RAM per connection).
    *   **Transaction Mode**: Configure Supabase/PgBouncer in "Transaction Mode".
    *   **Client Limits**: Set strict pool limits in the API to prevent starving the DB CPU.

### 4.2 Schema Design & Data Types
*   **Primary Keys**: Use **UUIDv7** (Time-Ordered UUIDs).
    *   *Why*: Standard UUIDv4 causes B-Tree index fragmentation and random I/O. UUIDv7 provides locality (inserts happen at the "end" of the index) while maintaining global uniqueness.
*   **JSONB Usage**:
    *   Use `JSONB` for flexible schemas (e.g., "Settings", "CustomFields").
    *   **Do Not** use `JSONB` for high-cardinality foreign keys or fields used in frequent `JOIN` conditions. Extract these to proper columns.
*   **Timestamps**: All tables must have `created_at` (immutable) and `updated_at`.
*   **Soft Deletes**: If using `is_deleted` or `deleted_at`, you **must** use Partial Indexes (see below).

### 4.3 Indexing Strategy
*   **The "Tenant First" Rule**: Almost every index in a shared-table model should start with `tenant_id`.
    *   *Example*: `CREATE INDEX idx_users_email ON users (tenant_id, email);`
*   **Partial Indexes**: Dramatically reduce index size by excluding "deleted" or "processed" rows.
    *   *Example*: `CREATE INDEX idx_active_orders ON orders (tenant_id, status) WHERE deleted_at IS NULL;`
*   **Covering Indexes (`INCLUDE`)**: Use `INCLUDE` to store extra payload data in the index leaf nodes, allowing "Index Only Scans" (no heap lookup required).
    *   *Example*: `CREATE INDEX idx_users_lookup ON users (tenant_id, id) INCLUDE (email, full_name);`
*   **GIN Indexes**: For `JSONB`, use GIN indexes.
    *   *Tip*: Use `jsonb_path_ops` GIN indexes if you only need `@>` (contains) operator support. It is smaller and faster than default `jsonb_ops`.

### 4.4 Query Optimization Patterns
*   **Avoid `COUNT(*)`**: Exact counts on large PostgreSQL tables are slow (MVCC requires visiting every row).
    *   *Solution*: Use "Estimated Counts" (from system stats) for totals > 10,000, or maintain a dedicated "counter table" incremented via triggers.
*   **Common Table Expressions (CTEs)**:
    *   Postgres 12+ optimizes CTEs well, but be careful.
    *   If a CTE is referenced only once, it's usually inlined.
    *   Use `MATERIALIZED` keyword only if you strictly need to prevent the optimizer from restructuring the query (e.g., acting as a fence).
*   **LATERAL Joins**: Use `LATERAL` joins for "Top-N-per-group" queries.
    *   *Scenario*: "Get the latest 3 comments for each of these 10 posts."
*   **Batch Writes**:
    *   Use `COPY` (via `Npgsql.BinaryImporter`) for bulk inserts (> 1,000 rows). It is 10x faster than `INSERT`.
    *   For updates, use `UPDATE ... FROM (VALUES ...)` syntax to update thousands of rows in a single round-trip.

### 4.5 Server Configuration (Supabase/Postgres Tunables)
*   **`shared_buffers`**: Typically 25% of RAM.
*   **`work_mem`**: Be conservative. This is *per operation*. High `work_mem` + high connections = OOM Crash.
*   **`effective_cache_size`**: Set to ~75% of RAM to help the planner estimate OS file cache usage.
*   **`wal_level`**: Minimal unless using logical replication (Realtime). If Realtime is unused for a table, disable the replication slot to save I/O.

---

### 4.6 Advanced & Unconventional Optimizations
*   **Kill `OR` with `UNION ALL`**:
    *   *Problem*: `WHERE status = 'active' OR priority = 'high'` often results in a full table scan because Postgres struggles to combine indexes for `OR`.
    *   *Fix*: Rewrite as two queries joined by `UNION ALL`. This allows Postgres to use the best index for *each* part independently.
*   **Bulk Updates via `VALUES`**:
    *   Instead of N separate `UPDATE` statements, use a single query with a joined `VALUES` list.
    *   *SQL*: `UPDATE users AS u SET status = v.status FROM (VALUES (1, 'active'), (2, 'banned')) AS v(id, status) WHERE u.id = v.id;`
*   **Composite Keyset Pagination**:
    *   For pagination on multiple columns (e.g., "Sort by Date, then ID"), use row-value comparison syntax.
    *   *Bad*: `WHERE created_at >= ? AND (created_at > ? OR id > ?)`
    *   *Good*: `WHERE (created_at, id) > (?, ?)` (Requires a composite index on `(created_at, id)`).
*   **The "Slow Index Scan" Trap**:
    *   Sometimes `ORDER BY created_at LIMIT 10` tricks Postgres into scanning the `created_at` index backwards, checking millions of rows against a filter that matches nothing.
    *   *Fix*: Use a "Materialized CTE" fence to force the filter first, *then* sort (if the result set is small).

### 4.7 Specialized Patterns & Supabase Features
*   **Pagination Keys (Cursors)**:
    *   **Generation**: Never expose raw DB values in cursors. Create an opaque cursor by encoding the keyset values (e.g., `Base64(created_at|id)`).
    *   **Usage**: The API decodes the cursor and applies the row-value filter: `WHERE (created_at, id) < (cursor_date, cursor_id)`.
*   **Supported Extensions**:
    *   **`pgvector`**: Mandatory for AI/Embeddings. Use **HNSW** indexes (`vector_cosine_ops`) for performance over IVFFlat.
    *   **`pg_cron`**: Use for simple scheduled maintenance (e.g., "Delete soft-deleted rows older than 30 days"). Keep logic simple; don't build a complex job queue here.
    *   **`postgis`**: Use for any geo-spatial queries. Standard distance calcs are slow without it.
    *   **`pg_net`**: Use for invoking webhooks from triggers. **Warning**: Ensure it is configured async to avoid blocking the transaction commit.
*   **Optimistic Concurrency Control (OCC)**:
    *   **Use `xmin`**: Postgres has a built-in system column `xmin` that changes on every update. Use it for version checking without adding a custom column.
    *   *SQL*: `UPDATE table SET ... WHERE id = @id AND xmin = @version;` (Throw concurrency exception if 0 rows updated).
*   **Atomic Counters**:
    *   Avoid Read-Modify-Write loops. Use atomic updates with `RETURNING`.
    *   *SQL*: `UPDATE stats SET views = views + 1 WHERE id = @id RETURNING views;`
*   **Blob & Metadata Separation**:
    *   **Pattern**: Store metadata (filename, size, type, owner) in the PostgreSQL table. Store the actual bytes in **Supabase Storage** (S3-compatible).
    *   **Linkage**: Use a Transactional Outbox or simple "Upload then DB Insert" flow.
    *   **Security**: Apply RLS policies to the Storage Bucket that mirror the DB Row RLS.
*   **Database Events & Queues**:
    *   **Supabase Realtime**: Use for UI updates (CDC).
    *   **Transactional Outbox**: For critical side effects (e.g., "Send Email on Signup"), insert a row into an `events` table within the main transaction. Have a separate worker process pick these up. This guarantees the event exists if and only if the transaction committed.

### 4.8 Expert Optimizations & Hidden Gems
*   **Hash Indexes (Postgres 10+)**:
    *   **Use Case**: Equality-only lookups on high-cardinality data (e.g., Session IDs, API Keys, URL slugs).
    *   **Benefit**: Smaller and faster than B-Tree for pure lookups.
    *   **Critical Warning**: **Cannot enforce UNIQUE constraints**. If you need a Primary Key or Unique constraint, you **must** use B-Tree. Use Hash only for non-unique lookups or as a secondary index.
    *   **Limitation**: No range queries (`>`, `<`) or sorting. Safe to use in Postgres 10+.
    *   *SQL*: `CREATE INDEX idx_sessions_token ON sessions USING HASH (token);`
*   **Large Text & TOAST**:
    *   **Select Discipline**: **Never** `SELECT *` if the table has large text/JSON columns. It forces Postgres to de-TOAST (fetch/decompress) data you might not need.
    *   **Storage Strategy**: For archival text (logs, blobs) rarely queried but often inserted, consider `ALTER COLUMN ... SET STORAGE EXTERNAL`. This prevents compression (saving CPU) but keeps data out of the main heap (keeping the hot table small).
    *   **Indexing Text**: Do not B-Tree index a whole URL or Log body.
        *   Exact match? Use **Hash Index**.
        *   Prefix search? Use **B-Tree** with `text_pattern_ops` or a partial expression index `(substring(col, 1, 50))`.
*   **`DISTINCT ON`**:
    *   The "Postgres Special" for getting the *first* row per group. often cleaner/faster than Window Functions.
    *   *SQL*: `SELECT DISTINCT ON (tenant_id) * FROM events ORDER BY tenant_id, created_at DESC;` (Gets the latest event for every tenant).
*   **Advisory Locks**:
    *   Use `pg_try_advisory_xact_lock(key)` for application-level distributed locks (e.g., ensuring only one worker processes a specific tenant's background job).
    *   **Benefit**: Extremely lightweight, memory-only, no table bloat (VACUUM not needed), auto-releases on transaction end.
*   **Correctness & Safety Patterns**:
    *   **Avoid `MERGE`**: In highly concurrent OLTP, `MERGE` can suffer from race conditions. Always prefer `INSERT ... ON CONFLICT` (Upsert) which is atomic and robust in Postgres.
    *   **`NOT IN` Trap**: **Never** use `NOT IN (subquery)`. If the subquery returns a single `NULL`, the result is empty. Always use `NOT EXISTS` or `LEFT JOIN ... WHERE IS NULL`.
    *   **Date Ranges**: Avoid `BETWEEN` for timestamps (it includes both ends). Use Half-Open Intervals (`>= start AND < end`) to correctly handle midnight boundaries.
    *   **No Overlaps**: Use `tstzrange` types with `EXCLUDE USING GIST` constraints to strictly prevent overlapping schedules/bookings at the DB level. "Application-level checks" for overlaps always fail under concurrency.

### 4.9 Operational Excellence & Schema Evolution
*   **Composite Index Ordering**:
    *   **The Golden Rule**: **Equality First, Range Last**.
    *   *Why*: B-Tree indexes traverse left-to-right. Once a Range condition (`>`, `<`) is applied, the index cannot efficiently jump to specific values for subsequent columns.
    *   *Bad*: `(created_at, tenant_id)` -> Querying `tenant_id=5 AND created_at > '2024-01-01'` has to scan all `2024` entries.
    *   *Good*: `(tenant_id, created_at)` -> Jumps straight to `tenant_id=5`, then scans the date range.
*   **BRIN Indexes (Block Range INdexes)**:
    *   **Use Case**: Massive "Append-Only" tables (Logs, Audit Trails, IoT Events) where data is naturally correlated with physical location (e.g., time-ordered).
    *   **Perfect Pair**: Works excellently with **UUIDv7** (time-ordered) or `created_at`.
    *   **Benefit**: Indexes are tiny (kilobytes vs gigabytes).
    *   *SQL*: `CREATE INDEX idx_logs_date ON logs USING BRIN (created_at);`
*   **Safe Migrations (Zero Downtime)**:
    *   **Concurrency**: **Always** use `CREATE INDEX CONCURRENTLY` in production. Standard creation locks the table against writes, causing outages.
    *   **Lock Protection**: Set `SET lock_timeout = '2s'` at the start of migration scripts.
        *   *Why*: If a long-running query holds a lock, your migration waits. While waiting, it queues up *all* subsequent app queries, causing a "pile-up" outage. Failing fast is safer.
    *   **Adding Columns**: In Postgres 11+, adding columns with constant defaults (e.g., `DEFAULT 0`) is instant (metadata change).
*   **Massive Bulk Loading**:
    *   **Strategy**: If inserting millions of rows at once (e.g., initial migration):
        1. Drop non-unique indexes and Foreign Keys.
        2. Load data (using `COPY`).
        3. Recreate indexes/FKs (increase `maintenance_work_mem` for this session).
    *   *Why*: Updating the B-Tree for every single row is significantly slower than building the tree from scratch.
*   **Constraints are Cheaper than Code**:
    *   Use `CHECK` constraints (e.g., `price > 0`, `status IN ('new', 'done')`).
    *   **Benefit**: Stops bad data at the gate with zero network round-trips. "Data Integrity is the ultimate performance optimization" because you don't have to write cleanup scripts later.


## Security

Apply [general security](../SECURITY_GUIDELINES.md) and [PERSISTENCE.md](../PERSISTENCE.md).
Bind data values through parameters in every client language and database access layer.
Do not rely on quote replacement or string escaping as the primary injection defense.
Parameters normally represent values, not table names, column names, or sort keywords.
For dynamic identifiers, select from a fixed application-owned mapping and use the database's identifier-quoting API where needed.
Stored procedures also require safe parameter handling if they construct dynamic SQL.
Separate runtime access from schema migration and administration privileges.
See [OWASP SQL injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).

```sql
-- SECURITY: PostgreSQL statement executed through a driver with separately bound values.
SELECT display_name
FROM customer
WHERE tenant_id = $1
    AND id = $2;
```

The application supplies an authorized tenant identity. Parameterization alone does not establish tenant ownership.
Scope updates, deletes, joins, bulk imports, and exports as well as reads.
Limit returned columns and row counts. Avoid disclosing internal metadata through errors or query diagnostics.
Test policies through the actual application role. Review privileged functions, search paths, and connection-pool context reset.
Use the shared [tenant-isolation checks](../SECURITY_GUIDELINES.md#tenant-isolation).
