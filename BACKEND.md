<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: b2d8f4e1-6a39-4c02-af7b-3e5a9d1c8b26
Created: 2026
-->

<!-- AGENT: Backend service boundaries, atomic writes, runtime compatibility, and persistence checks. -->

# Backend services

## Target scope

Server, container, and Kubernetes-hosted service work: APIs, databases, entities, data models, and service operations.

## Existing topic references

| Work in scope | Existing guidance |
| --- | --- |
| C# service source | [CSHARP.md](./CSHARP.md) |
| Java service or extension source | [JAVA.md](./JAVA.md) |
| API resources, relationships, naming, HTTP methods, and serialization | [API_GUIDELINES.md](./API_GUIDELINES.md) |
| Human-usable resource URLs | [RESTABLE_RESOURCES.md](./RESTABLE_RESOURCES.md) |
| Data entities and relationships in the knowledge base | [KNOWLEDGE_ARCHITECTURE.md](./KNOWLEDGE_ARCHITECTURE.md#22-file-formats) |
| Database language and engine-specific rules | [SQL.md](./SQL.md) |
| Resource ownership and authorization | [ACCESS_CONTROL.md](./ACCESS_CONTROL.md) |
| Resource deletion across persistence and APIs | [DELETION.md](./DELETION.md) |
| Server-owned secrets and encryption | [SECRET_HANDLING.md](./SECRET_HANDLING.md) |
| Local development for the combined application example | [SAAS.md](./SAAS.md#existing-combined-layout) |

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

## Extracted instruction sections

- [Configured backend](#configured-backend)
- [Database configuration](#database-configuration)
- [Runtime and deployment](#runtime-and-deployment)
- [Identity-service example](#identity-service-example)
- [Existing Java and identity layout](#existing-java-and-identity-layout)
- [Existing local script example](#existing-local-script-example)
- [Local endpoints and dependencies](#local-endpoints-and-dependencies)
- [Backend library selection](#backend-library-selection)
- [Existing API organization](#existing-api-organization)
- [Existing database migrations](#existing-database-migrations)
- [Existing ASP.NET Core performance guidance](#existing-aspnet-core-performance-guidance)
- [Existing API performance guidance](#existing-api-performance-guidance)
- [Existing data-fetching optimization patterns](#existing-data-fetching-optimization-patterns)
- [Existing API latency budget](#existing-api-latency-budget)
- [Existing endpoint performance checks](#existing-endpoint-performance-checks)
- [Existing API security defaults](#existing-api-security-defaults)
- [Existing host dependency verification](#existing-host-dependency-verification)
- [Existing Entity Framework query convention](#existing-entity-framework-query-convention)

## Configured backend

- Use the project's configured backend, such as ASP.NET Core 10.0+ or Java. Match its runtime and deployment mode.

## Database configuration

- Use the configured PostgreSQL and data-access versions. Keep executable SQL migration scripts in the project's migration directory.

## Runtime and deployment

- Read deployment configuration for containers, Cloud Run, background roles, and resource limits. Do not assume a fixed image size.

## Identity-service example

- Use Java and the configured JDK for identity-server extensions. Keycloak projects may include providers, browser themes, and a container deployment.
- Match extension APIs to the host runtime and distinguish host-provided dependencies from bundled dependencies.
- Use the Maven or Gradle wrapper and the repository's configured toolchain.
- A general Java web application uses its declared web framework. Keycloak is an identity-service choice, not a universal Java backend.
- Use TypeScript for non-trivial browser logic. Preserve the host's template, security-header, and asset-delivery contracts.

## Existing Java and identity layout

```text
src/providers/         Java host extensions, with their own Maven/Gradle source and test roots
src/themes/            Host-rendered templates, styles, and browser assets
src/main/java/         Application Java code when this is a standard Java backend
src/main/resources/    Application configuration and packaged resources
src/test/java/         Unit and integration tests under the configured runner
sql/                   Application-owned database scripts, when applicable
Dockerfile             Container build, when the deployment uses containers
target/ or build/      Generated output, never the source to edit
```

The identity extension roots and standard Java roots are alternatives, not duplicate homes for the same code.

## Existing local script example

Use the following commands when the consuming repository provides these scripts.
Otherwise, use its documented build and test commands for the configured toolchain.

### Clean
```bash
./clean.sh
```

### Build
```bash
./build.sh
```

### Test
```bash
./test.sh
```

### Run
```bash
./run.sh
```

### Deploy
```bash
./redeploy.sh
```

## Local endpoints and dependencies

Read the consuming repository's README, launch configuration, and scripts for ports, health checks, and local dependencies.
The SaaS, identity service, component demo, and website may each use different endpoints.
Native apps and local tools need no listening port unless their design explicitly includes a service.
Use configured local credentials. Never copy example credentials into a deployed environment.

## Backend library selection

- When selecting libaries for backend functionality, always consult BACKEND_LIBRARY_SELECTION.md for guidelines
  and, for .NET projects, DOTNETFX_SELECTION.md for pre-canned recommendations.

## Existing API organization

- Plan for modular API organization
  * Separate API files for different application components
  * Maintain clean, organized API structure

## Existing database migrations

### Plain SQL Over ORM Migration Tools
Always prefer writing plain SQL scripts for database migrations instead of using ORM migration tools like `dotnet ef migrations`. This approach:
- Provides better control and visibility over what changes are being made
- Avoids version mismatches and tooling issues
- Is more portable and easier to review
- Works reliably regardless of ORM tool versions

### Migration Guidelines
- Place SQL migration scripts in `/sql/migrations/` with naming format: `YYYYMMDD_description.sql`
- Use `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS` for idempotency
- Include proper foreign key constraints with `ON DELETE CASCADE` or `ON DELETE SET NULL` as appropriate
- Add timestamps (`created_at`, `updated_at`) to all tables
- After running the SQL, record the migration in EF Core's history table:
  ```sql
  INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
  VALUES ('YYYYMMDD_MigrationName', '10.0.2')
  ON CONFLICT ("MigrationId") DO NOTHING;
  ```
- Update the model snapshot (`KnobbyDbContextModelSnapshot.cs`) manually to keep EF Core in sync

### Running Migrations
Use `psql` directly to run migrations:
```bash
PGPASSWORD=<password> psql -h <host> -p <port> -U <user> -d <database> -f <migration_file.sql>
```

## Existing ASP.NET Core performance guidance

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

## Existing API performance guidance

### 5.1 Payloads
*   **Null Suppression**: Configure the JSON serializer to ignore null values.
    See [C#](./CSHARP.md#51-payloads).
*   **Compression**: Enable Response Compression (Brotli/Gzip) in ASP.NET Core middleware.
    See [C#](./CSHARP.md#51-payloads).

### 5.2 Latency Reduction
*   **Parallelism**: If an API needs data from three independent services/tables, fetch them in parallel using `Task.WhenAll`, not sequentially.
    See [C#](./CSHARP.md#52-latency-reduction).

## Existing data-fetching optimization patterns

The following patterns **must** be prioritized by coding agents over naive "fetch all" or "sequential" implementations.

### 7.1 Pattern: Selective Fetching (Partial Objects)
*   **Purpose:** Eliminate over-fetching by only retrieving the specific fields required for the current UI component.
*   **Implementation (C# / EF Core):**
    See [C#](./CSHARP.md#71-pattern-selective-fetching-partial-objects).

### 7.2 Pattern: The DataLoader (Batching & Deduplication)
*   **Purpose:** Solve the "N+1 Problem" by batching multiple independent requests into a single call.
*   **Implementation:** Use **GreenDonut** or similar for .NET batching logic.

### 7.5 Pattern: Transactional Outbox (Async Side-Effects)
*   **Purpose:** Prevent blocking user requests during external side-effects (emails, search index updates).
*   **Implementation:** Save the event to an `outbox` table in the same DB transaction; process via background worker.

### 7.6 Pattern: Materialized Projections
*   **Purpose:** Pre-calculate complex joins into a flat, read-optimized table.
*   **Implementation:** Use Postgres `MATERIALIZED VIEW` with unique indexes and concurrent refreshes.

---

## Existing API latency budget

*   **API Response Time**: < 100ms (p95)

## Existing endpoint performance checks

*   **Load Testing**: Use k6 or JMeter to stress test endpoints.

*   **Profiling**: Use `dotnet-counters` and `dotnet-trace` to identify bottlenecks in the backend.

## Existing API security defaults

- **"Secure by Design, not by Patch."**
- **No PII in URLs:** Never pass email, names, or IDs in Query Parameters. Use Session/Claims or POST bodies.
- **Auth Decorators:** No API endpoint is created without an `[Authorize]` or `[RequirePermission]` attribute unless explicitly public (like login).
- **Explicit Ignores:** In EF Core, use Fluent API `modelBuilder.Entity<T>().Ignore(x => x.Prop)` for all computed properties. Do not rely on `[NotMapped]`.

## Existing host dependency verification

- For Java extensions, match host APIs and avoid bundling host-provided classes. Use the build's declared dependency scope.

## Existing Entity Framework query convention

* StyleCop and compiler warnings are constantly emitted that says do not use String.Equals instead suggesting StringComparison. However, this is NOT correct advice for Dotnet Entity Framework (EF) and LINQ queries. When you need to make case insensitive comparisons, you will have to use String.Equals with appropriate case conversion first done on arguments.
