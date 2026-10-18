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

Common performance rules apply across targets. Read the matching target or language sections for workload-specific guidance.

## Performance is a feature

*   Performance is not an afterthought; it is a core requirement.

## Network cost

*   Assume the user is on a flaky 4G connection.
*   Minimize the number of round trips.
*   Minimize payload sizes.

## Workload budgets and measurement

Web paint metrics apply to browser surfaces. Define native app and tool budgets for their actual workloads and target devices.
Use representative workloads and the project's profiler or benchmark tools. Record the baseline and test environment.

## Select performance guidance

| Workload | Read |
| --- | --- |
| Browser budgets, rendering, UI thread, and Lighthouse | [FRONTEND.md](./FRONTEND.md#browser-performance-guidance) |
| Asset loading, bundling, caching, and delivery | [STATIC_ASSETS.md](./STATIC_ASSETS.md) |
| API budgets, ASP.NET Core runtime, bounded fetches, and endpoint checks | [BACKEND.md](./BACKEND.md) |
| Transactions, outbox, projections, and stored data | [PERSISTENCE.md](./PERSISTENCE.md) |
| PostgreSQL query and engine tuning | [SQL.md](./SQL.md#performance) |
| Native Apple performance | [APPS.md](./APPS.md#apple-performance-guidance) |
| Go profiling and benchmarks | [GO.md](./GO.md#performance) |
| Rust profiling and benchmarks | [RUST.md](./RUST.md#performance) |
| Java runtime and extension performance | [JAVA.md](./JAVA.md#performance) |
| Python workloads | [PYTHON.md](./PYTHON.md#performance) |
