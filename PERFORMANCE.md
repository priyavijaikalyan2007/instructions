<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 04125933-4c89-4e50-8e5f-69d99bf68e40
Created: 2026
-->

<!-- AGENT: Performance budgets and measurement guidance for web, native, and tool workloads. -->

# Performance Guidelines

This document outlines the performance standards and best practices for our high-performance web application.

**Target**: Low latency (< 100ms interactions), minimal CPU/Memory footprint, supporting devices ranging from low-power corporate laptops to high-end workstations.

**Example web stack**:
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

### 1.4 Native Apps and Tools

Web paint metrics apply to browser surfaces. Define native app and tool budgets for their actual workloads and target devices.
Use representative workloads and the project's profiler or benchmark tools. Record the baseline and test environment.

### 1.5 Swift and Apple Platforms

See [Swift](./SWIFT.md#performance).

### 1.6 Go Tools and Services

See [Go](./GO.md#performance).

### 1.7 Rust Tools and Services

See [Rust](./RUST.md#performance).

### 1.8 Java Applications and Extensions

See [Java](./JAVA.md#performance).

### 1.9 Python Tools and Services

See [Python](./PYTHON.md#performance).

## 2. Frontend Performance (TS/JS & HTML/CSS)

### 2.1 Loading & Bundle Size
*   **ES6 Modules**: Use native ES6 modules. Avoid heavy bundlers where vanilla modules suffice.
*   **Code Splitting**: Lazy load non-critical modules using dynamic imports (`import()`).
    See [JavaScript](./JAVASCRIPT.md#21-loading--bundle-size).
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

See [C#](./CSHARP.md#performance).

### 3.1 Async/Await

See [C#](./CSHARP.md#performance).

### 3.2 JSON Serialization

See [C#](./CSHARP.md#performance).

### 3.3 Memory & Garbage Collection (GC)

See [C#](./CSHARP.md#performance).

### 3.4 Caching (Server-Side)

See [C#](./CSHARP.md#performance).

## 4. Database Performance (PostgreSQL 17)

See [SQL](./SQL.md#performance).

### 4.1 Architecture: Multi-Tenancy & Scaling

See [SQL](./SQL.md#performance).

### 4.2 Schema Design & Data Types

See [SQL](./SQL.md#performance).

### 4.3 Indexing Strategy

See [SQL](./SQL.md#performance).

### 4.4 Query Optimization Patterns

See [SQL](./SQL.md#performance).

### 4.5 Server Configuration (Supabase/Postgres Tunables)

See [SQL](./SQL.md#performance).

### 4.6 Advanced & Unconventional Optimizations

See [SQL](./SQL.md#performance).

### 4.7 Specialized Patterns & Supabase Features

See [SQL](./SQL.md#performance).

### 4.8 Expert Optimizations & Hidden Gems

See [SQL](./SQL.md#performance).

### 4.9 Operational Excellence & Schema Evolution

See [SQL](./SQL.md#performance).

## 5. API Design for Performance

### 5.1 Payloads
*   **Null Suppression**: Configure the JSON serializer to ignore null values.
    See [C#](./CSHARP.md#51-payloads).
*   **Compression**: Enable Response Compression (Brotli/Gzip) in ASP.NET Core middleware.
    See [C#](./CSHARP.md#51-payloads).

### 5.2 Latency Reduction
*   **Parallelism**: If an API needs data from three independent services/tables, fetch them in parallel using `Task.WhenAll`, not sequentially.
    See [C#](./CSHARP.md#52-latency-reduction).

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
    See [C#](./CSHARP.md#71-pattern-selective-fetching-partial-objects).

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
