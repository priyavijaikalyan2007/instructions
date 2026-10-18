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

Common performance rules and links to target-specific guidance follow.

---

## 1. General Principles

### 1.1 "Performance is a Feature"
*   Performance is not an afterthought; it is a core requirement.
See [FRONTEND.md](./FRONTEND.md#existing-browser-performance-budgets) for browser budgets and [BACKEND.md](./BACKEND.md#existing-api-latency-budget) for the existing API budget.

### 1.2 "Network is the Bottleneck"
*   Assume the user is on a flaky 4G connection.
*   Minimize the number of round trips.
*   Minimize payload sizes.

### 1.3 "The Main Thread is Sacred"

See [FRONTEND.md](./FRONTEND.md#existing-browser-ui-thread-guidance).

### 1.4 Native Apps and Tools

Web paint metrics apply to browser surfaces. Define native app and tool budgets for their actual workloads and target devices.
Use representative workloads and the project's profiler or benchmark tools. Record the baseline and test environment.

### 1.5 Swift and Apple Platforms

See [Native apps](./APPS.md#existing-apple-performance-guidance).

### 1.6 Go Tools and Services

See [Go](./GO.md#performance).

### 1.7 Rust Tools and Services

See [Rust](./RUST.md#performance).

### 1.8 Java Applications and Extensions

See [Java](./JAVA.md#performance).

### 1.9 Python Tools and Services

See [Python](./PYTHON.md#performance).

## 2. Frontend Performance (TS/JS & HTML/CSS)

See [FRONTEND.md](./FRONTEND.md#existing-browser-performance-guidance).

### 2.1 Loading & Bundle Size

See [STATIC_ASSETS.md](./STATIC_ASSETS.md#existing-asset-loading-and-production-output).

### 2.2 Rendering & DOM

See [FRONTEND.md](./FRONTEND.md#existing-browser-performance-guidance).

### 2.3 Local Storage & Caching strategy

See [FRONTEND.md](./FRONTEND.md#existing-browser-performance-guidance).

### 2.4 Memory Management

See [FRONTEND.md](./FRONTEND.md#existing-browser-performance-guidance).

### 2.5 Service Workers & Background Tasks

See [FRONTEND.md](./FRONTEND.md#existing-browser-performance-guidance).

## 3. Backend Performance (ASP.NET Core 10.0)

See [Backend](./BACKEND.md#existing-aspnet-core-performance-guidance).

### 3.1 Async/Await

See [Backend](./BACKEND.md#existing-aspnet-core-performance-guidance).

### 3.2 JSON Serialization

See [Backend](./BACKEND.md#existing-aspnet-core-performance-guidance).

### 3.3 Memory & Garbage Collection (GC)

See [Backend](./BACKEND.md#existing-aspnet-core-performance-guidance).

### 3.4 Caching (Server-Side)

See [Backend](./BACKEND.md#existing-aspnet-core-performance-guidance).

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

See [BACKEND.md](./BACKEND.md#existing-api-performance-guidance).

### 5.1 Payloads

See [BACKEND.md](./BACKEND.md#existing-api-performance-guidance).

### 5.2 Latency Reduction

See [BACKEND.md](./BACKEND.md#existing-api-performance-guidance).

## 6. Performance Testing

See [BACKEND.md](./BACKEND.md#existing-endpoint-performance-checks).
See [FRONTEND.md](./FRONTEND.md#existing-browser-performance-checks).

---

## 7. High-Scale Optimization Patterns

See [BACKEND.md](./BACKEND.md#existing-data-fetching-optimization-patterns).

### 7.1 Pattern: Selective Fetching (Partial Objects)

See [BACKEND.md](./BACKEND.md#existing-data-fetching-optimization-patterns).

### 7.2 Pattern: The DataLoader (Batching & Deduplication)

See [BACKEND.md](./BACKEND.md#existing-data-fetching-optimization-patterns).

### 7.3 Pattern: Autocomplete / PeoplePicker Optimization

See [SAAS.md](./SAAS.md#existing-cross-layer-autocomplete-optimization).

### 7.4 Pattern: Shallow-Deep Hydration

See [FRONTEND.md](./FRONTEND.md#existing-progressive-data-rendering).

### 7.5 Pattern: Transactional Outbox (Async Side-Effects)

See [BACKEND.md](./BACKEND.md#existing-data-fetching-optimization-patterns).

### 7.6 Pattern: Materialized Projections

See [BACKEND.md](./BACKEND.md#existing-data-fetching-optimization-patterns).

## 8. Final Directive for Coding Agents

1.  **Stop the "Fetch All" Habit**: Never use `SELECT *` or `FindAsync(id)` if the UI only needs a subset of columns.
2.  **Cap Everything**: Every list or search API **must** have a hard `LIMIT` or `Take()`.
3.  **Parallelize I/O**: Use `Task.WhenAll` for independent fetches from different sources.
4.  **Default to Partial Hydration**: Only load what is immediately visible. Use "View More" or tabs for deep data.

---

**Remember**: Fast software feels professional. Slow software feels broken.
