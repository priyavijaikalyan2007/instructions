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

**Remember**: Fast software feels professional. Slow software feels broken.
