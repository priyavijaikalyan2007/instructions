<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: b2d8f4e1-6a39-4c02-af7b-3e5a9d1c8b26
Created: 2026
-->

<!-- AGENT: Backend service boundaries, atomic writes, runtime compatibility, and persistence checks. -->

# Backend Development Guidelines

Keep business logic in services or domain functions, separate from HTTP handlers and framework extension entry points.
Apply the same separation in .NET, Java, Go, and Rust using their normal language constructs.

## Related writes and persistence

Commit related writes in one database transaction when they must succeed or fail together.
Do not swallow a secondary write failure and report success while leaving required records inconsistent.
For writes across databases or external services, define delivery, retry, idempotency, and reconciliation requirements before choosing a mechanism.
Use the project's migration convention and verify that a new environment receives its required schema baseline before incremental migrations.
Test database-specific constraints and transactions against the actual database engine rather than an in-memory substitute.

## Runtime and resource boundaries

Match service and connection lifetimes to the request or operation. Do not share a non-thread-safe context between concurrent operations.
Propagate cancellation and release owned resources on success and failure.
For host extensions, verify APIs and dependency ownership against the runtime version actually shipped.
Reproduce deployment failures using the exact artifact and production launch path when available.
Do not assume that a development entry point exercises the packaged production artifact.
