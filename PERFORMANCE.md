<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 04125933-4c89-4e50-8e5f-69d99bf68e40
Created: 2026
-->

# Performance Guidelines

This document outlines the performance standards and best practices for our high-performance web application.

**Target**: Low latency (< 100ms interactions), minimal CPU/Memory footprint, supporting devices ranging from low-power corporate laptops to high-end workstations.

**Stack**:
*   **Frontend**: Vanilla JS / TypeScript (ES6), HTML5, Bootstrap 5.
*   **Backend**: ASP.NET Core 10.0 (API + Static Serving).
*   **Database**: PostgreSQL 17.6 (Supabase).

---

## 1. General Principles

### 1.1 "Performance is a Feature"
*   Performance is not an afterthought; it is a core requirement.
*   **Budget**:
    *   **First Contentful Paint (FCP)**: < 1.0s
    *   **Time to Interactive (TTI)**: < 1.5s
    *   **API Response Time**: < 100ms (p95)
    *   **Interaction to Next Paint (INP)**: < 200ms

### 1.2 "Network is the Bottleneck"
*   Assume the user is on a flaky 4G connection.
*   Minimize the number of round trips.
*   Minimize payload sizes.

### 1.3 "The Main Thread is Sacred"
*   The UI thread must never be blocked.
*   Offload heavy computation to Web Workers or the backend.
*   Yield to the main thread frequently during long tasks.

---

## 2. Frontend Performance (TS/JS & HTML/CSS)

### 2.1 Loading & Bundle Size
*   **ES6 Modules**: Use native ES6 modules. Avoid heavy bundlers where vanilla modules suffice.
*   **Code Splitting**: Lazy load non-critical modules using dynamic imports (`import()`).
    ```javascript
    // Load heavy charting library only when needed
    if (showChart) {
        const { renderChart } = await import('./modules/charting.js');
        renderChart();
    }
    ```
*   **Minification**: Ensure all production assets (JS/CSS) are minified (part of the build pipeline).
*   **Preloading**: Use `<link rel="preload">` for critical resources (fonts, main CSS, main JS).

### 2.2 Rendering & DOM
*   **Minimize Reflows**: Avoid "layout thrashing." Read layout properties (e.g., `offsetHeight`) first, then write style changes. Do not interleave them.
*   **Batch DOM Updates**: Use `DocumentFragment` to append multiple elements at once.
*   **Virtualization**: For lists with > 100 items, use "virtual scrolling" (rendering only visible items).
*   **CSS Selectors**: Avoid complex, deep selectors. Use simple class selectors (BEM-style preferred).
*   **Animations**: Use CSS `transform` and `opacity` for animations. These run on the compositor thread. Avoid animating `top`, `left`, `width`, or `height`.

### 2.3 Local Storage & Caching strategy
*   **Aggressive Caching**: Use `localStorage` or `IndexedDB` to cache user data (e.g., session lists, diagrams).
    *   *Pattern*: "Stale-While-Revalidate". Show cached data immediately, then fetch updates in the background.
*   **Asset Caching**: Static assets (images, fonts, JS, CSS) must be served with long-term `Cache-Control` headers (e.g., `public, max-age=31536000, immutable`).

### 2.4 Memory Management
*   **Event Listeners**: Always remove event listeners when components/elements are destroyed to prevent memory leaks.
*   **Large Objects**: Avoid keeping large datasets in global scope.
*   **WeakMap/WeakSet**: Use `WeakMap` for associating data with DOM elements to ensure garbage collection works.

### 2.5 Service Workers & Background Tasks
*   **Local-First Architecture**: For data-heavy apps (like "Thinker"), writes should go to `localStorage` or `IndexedDB` immediately.
    *   **Background Sync**: Use a Service Worker to sync local changes to the server in the background. This keeps the UI responsive even during network latency or outages.
*   **Offloading Work**: Move heavy computations (e.g., parsing large datasets, complex geometry calculations, loading heavy tool palettes) to a **Web Worker** or **Service Worker**.
    *   *Rule*: If a task takes > 50ms, it should not be on the main thread.

---

## 3. Backend Performance (ASP.NET Core 10.0)

### 3.1 Async/Await
*   **Async All the Way**: Every I/O operation (Database, File, Network) **must** be `async`.
*   **Avoid `.Result` / `.Wait()`**: These cause thread pool starvation. Always use `await`.
*   **`ConfigureAwait(false)`**: Not strictly necessary in ASP.NET Core (no SynchronizationContext), but good practice in library code.

### 3.2 JSON Serialization
*   **System.Text.Json**: Use the built-in `System.Text.Json`. It is significantly faster and allocates less memory than `Newtonsoft.Json`.
*   **Source Generators**: Use JSON source generators for AOT compatibility and maximum serialization performance.
    ```csharp
    [JsonSerializable(typeof(MyDto))]
    internal partial class MyJsonContext : JsonSerializerContext { }
    ```

### 3.3 Memory & Garbage Collection (GC)
*   **Structs vs Classes**: Use `readonly struct` for small, immutable data carriers to reduce heap allocations.
*   **Span<T> / Memory<T>**: Use `Span<T>` for string/array slicing to avoid creating new substrings/arrays.
*   **StringBuilder**: Use `StringBuilder` (or `ZString`) for complex string concatenation.
*   **Pooling**: Use `ArrayPool<T>` for large temporary buffers.

### 3.4 Caching (Server-Side)
*   **IMemoryCache**: Use in-process memory cache for small, high-read reference data (e.g., configuration, tenant settings).
    *   *Expiration*: Always set absolute or sliding expiration.
*   **Output Caching**: Use `[OutputCache]` for public, static-like API endpoints.

---

## 4. Database Performance (PostgreSQL 17)

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

## 5. API Design for Performance

### 5.1 Payloads
*   **Null Suppression**: Configure the JSON serializer to ignore null values.
    ```csharp
    options.JsonSerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull;
    ```
*   **Compression**: Enable Response Compression (Brotli/Gzip) in ASP.NET Core middleware.
    ```csharp
    builder.Services.AddResponseCompression(options => {
        options.EnableForHttps = true;
    });
    ```

### 5.2 Latency Reduction
*   **Parallelism**: If an API needs data from three independent services/tables, fetch them in parallel using `Task.WhenAll`, not sequentially.
    ```csharp
    var task1 = GetUserAsync(id);
    var task2 = GetOrdersAsync(id);
    await Task.WhenAll(task1, task2); // Runs concurrently
    ```

## 6. Performance Testing

*   **Load Testing**: Use k6 or JMeter to stress test endpoints.
*   **Profiling**: Use `dotnet-counters` and `dotnet-trace` to identify bottlenecks in the backend.
*   **Lighthouse**: Run Chrome Lighthouse audits on frontend pages regularly.

---

## 7. High-Scale Optimization Patterns

The following patterns **must** be prioritized by coding agents over naive "fetch all" or "sequential" implementations.

### 7.1 Pattern: Selective Fetching (Partial Objects)
*   **Purpose:** Eliminate over-fetching by only retrieving the specific fields required for the current UI component.
*   **Implementation (C# / EF Core):**
    ```csharp
    // ✅ OPTIMIZED: Fetches only required columns
    var userCard = await db.Users
        .Where(u => u.Id == id)
        .Select(u => new UserCardDto {
            FullName = u.FullName,
            AvatarUrl = u.AvatarUrl
        })
        .FirstOrDefaultAsync();
    ```

### 7.2 Pattern: The DataLoader (Batching & Deduplication)
*   **Purpose:** Solve the "N+1 Problem" by batching multiple independent requests into a single call.
*   **Implementation:** Use **GreenDonut** or similar for .NET batching logic.

### 7.3 Pattern: Autocomplete / PeoplePicker Optimization
*   **Purpose:** Provide sub-100ms search results across millions of records.
*   **Implementation:**
    *   **Frontend**: Debouncing (300ms) and mandatory result capping (e.g., `limit=10`).
    *   **Backend**: Use `text_pattern_ops` in Postgres for efficient prefix indexing.

### 7.4 Pattern: Shallow-Deep Hydration
*   **Purpose:** Split a large object's retrieval into "Shallow" (immediate UI rendering) and "Deep" (lazy-loading expensive details like history or attachments).
*   **Implementation:** Render metadata first; lazy-load details via HTMX or `IntersectionObserver`.

### 7.5 Pattern: Transactional Outbox (Async Side-Effects)
*   **Purpose:** Prevent blocking user requests during external side-effects (emails, search index updates).
*   **Implementation:** Save the event to an `outbox` table in the same DB transaction; process via background worker.

### 7.6 Pattern: Materialized Projections
*   **Purpose:** Pre-calculate complex joins into a flat, read-optimized table.
*   **Implementation:** Use Postgres `MATERIALIZED VIEW` with unique indexes and concurrent refreshes.

---

## 8. Final Directive for Coding Agents

1.  **Stop the "Fetch All" Habit**: Never use `SELECT *` or `FindAsync(id)` if the UI only needs a subset of columns.
2.  **Cap Everything**: Every list or search API **must** have a hard `LIMIT` or `Take()`.
3.  **Parallelize I/O**: Use `Task.WhenAll` for independent fetches from different sources.
4.  **Default to Partial Hydration**: Only load what is immediately visible. Use "View More" or tabs for deep data.

---

**Remember**: Fast software feels professional. Slow software feels broken.