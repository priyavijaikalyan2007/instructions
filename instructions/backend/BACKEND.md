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

## Environment convention

For new backend components, use test for the local machine, dev for staging, and prod for production.
Keep actual destinations, database ownership, and configuration paths in project facts.
Setup defines names and script placeholders. It does not provision those environments.
Preserve established environment mappings unless the task explicitly migrates them.
Read [project scaffolding](../PROJECT_SCAFFOLDING.md) before implementing generated operation scripts.

## Target scope

Server, container, and Kubernetes-hosted service work: APIs, databases, entities, data models, and service operations.

## Topic references

| Work in scope | Existing guidance |
| --- | --- |
| Shared setup, build/test/run commands, and endpoints | [REPO.md](../REPO.md) |
| Transactions, migrations, and stored-data integrity | [PERSISTENCE.md](../PERSISTENCE.md) |
| C# service source | [CSHARP.md](../csharp/CSHARP.md) |
| Java service or extension source | [JAVA.md](../java/JAVA.md) |
| API resources, relationships, naming, HTTP methods, and serialization | [API_GUIDELINES.md](API_GUIDELINES.md) |
| Human-usable resource URLs | [RESTABLE_RESOURCES.md](../RESTABLE_RESOURCES.md) |
| Data entities and relationships in the knowledge base | [KNOWLEDGE_ARCHITECTURE.md](../KNOWLEDGE_ARCHITECTURE.md#22-file-formats) |
| Database language and engine-specific rules | [SQL.md](../sql/SQL.md) |
| Resource ownership and authorization | [ACCESS_CONTROL.md](../ACCESS_CONTROL.md) |
| Resource deletion across persistence and APIs | [DELETION.md](../DELETION.md) |
| Server-owned secrets and encryption | [SECRET_HANDLING.md](../SECRET_HANDLING.md) |
| Local development for the combined application example | [SAAS.md](../saas/SAAS.md#combined-layout) |

# Backend Development Guidelines

Keep business logic in services or domain functions, separate from HTTP handlers and framework extension entry points.
Apply the same separation in .NET, Java, Go, and Rust using their normal language constructs.

## Read by backend language

Read shared service boundaries, resource limits, and API behavior for every backend.
Use [Java](../java/JAVA.md#performance) for Java runtime, testing, logging, profiling, and packaged execution.
The ASP.NET Core section and .NET implementation notes apply only to a configured .NET component.
A container does not select .NET, Keycloak, Cloud Run, or Kubernetes by itself.
Use the component's actual framework, toolchain, and launch configuration from PROJECT.md and its manifests.

## Runtime and resource boundaries

Propagate cancellation and release owned resources on success and failure.
For host extensions, verify APIs and dependency ownership against the runtime version actually shipped.
Reproduce deployment failures using the exact artifact and production launch path when available.
Do not assume that a development entry point exercises the packaged production artifact.

## Configured backend

- Use the project's configured backend, such as ASP.NET Core 10.0+ or Java. Match its runtime and deployment mode.

## Runtime and deployment

- Read deployment configuration for containers, Cloud Run, background roles, and resource limits. Do not assume a fixed image size.

## Identity-service example

- Use Java and the configured JDK for identity-server extensions. Keycloak projects may include providers, browser themes, and a container deployment.
- Match extension APIs to the host runtime and distinguish host-provided dependencies from bundled dependencies.
- Use the Maven or Gradle wrapper and the repository's configured toolchain.
- A general Java web application uses its declared web framework. Keycloak is an identity-service choice, not a universal Java backend.
- Use TypeScript for non-trivial browser logic. Preserve the host's template, security-header, and asset-delivery contracts.

## Service source layout

Use `src/service/<service-name>/backend/` for a new backend, including an API-only microservice.
Apply the [shared folder convention](../REPO.md#folder-and-file-structure) and preserve existing configured layouts.
Keep backend project manifests, dependencies, component tests, and framework resources with the backend.
Use sibling database/ for service-owned database scripts, not for entities or ORM mappings.
Add that database path to the backend component's profile scope when those scripts enter the project.
Do not create browser or database components merely because the source type is service.

```text
src/service/<service-name>/
    backend/               One or more configured backend projects or packages
    database/              Owned schema scripts and migrations, when applicable
    frontend/              Browser source, only when selected
    static/                Direct-copy static source, only when needed
deploy/<service-name>/     Runtime, container, and infrastructure definitions
test/<service-name>/       Tests spanning this backend and other components
```

Keep domain models and processing code in their backend projects.
Tool-required migrations and snapshots stay in that backend project. Keep one migration authority for each schema.
Store operator procedures in playbooks/ and public API documentation in docs/.

## Java and identity layout

The following paths are relative to `src/service/<service-name>/backend/` for a new Java backend.

```text
pom.xml or build.gradle    Project manifest, with its configured wrapper and dependency policy
src/main/java/            Application source
src/main/resources/       Configuration and packaged resources
src/test/java/            Component unit and integration tests
target/ or build/          Ignored generated output
```

A host-extension project can instead use `providers/<provider-name>/` with its own standard Java project roots.
Place source for host-packaged themes in a named location such as `backend/themes/<theme-name>/.`
Keep identity-host themes distinct from an independently served browser frontend.
The provider and application layouts are alternatives, not duplicate homes for the same implementation.
Repository-wide deployment definitions belong in `deploy/<service-name>/.`
Keep build inputs such as a backend-specific Dockerfile with the component when its build context requires that location.

## Backend library selection

- When selecting libaries for backend functionality, always consult instructions/backend/BACKEND_LIBRARY_SELECTION.md for guidelines
  and, for .NET projects, instructions/csharp/DOTNETFX_SELECTION.md for pre-canned recommendations.

## API organization

- Plan for modular API organization
  * Separate API files for different application components
  * Maintain clean, organized API structure

## ASP.NET Core performance guidance

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

## API performance guidance

Minimize response payloads, avoid unnecessary serialization, and run independent I/O concurrently within configured resource limits.
Use the selected backend framework's serializer and response-compression facilities.

### .NET implementation notes

The implementation requirements in this subsection apply only to .NET backends.

### 5.1 Payloads

The following implementation notes apply to .NET backends.
*   **Null Suppression**: Configure the JSON serializer to ignore null values.
    See [C#](../csharp/CSHARP.md#51-payloads).
*   **Compression**: Enable Response Compression (Brotli/Gzip) in ASP.NET Core middleware.
    See [C#](../csharp/CSHARP.md#51-payloads).

### 5.2 Latency Reduction

The following implementation note applies to .NET backends. Java uses its configured concurrency model.
*   **Parallelism**: If an API needs data from three independent services/tables, fetch them in parallel using `Task.WhenAll`, not sequentially.
    See [C#](../csharp/CSHARP.md#52-latency-reduction).

## data-fetching optimization patterns

Apply bounded fetching and batching principles across backends. C#/EF Core and GreenDonut are .NET implementation examples.
Java services use their configured data-access and batching facilities.

The following patterns **must** be prioritized by coding agents over naive "fetch all" or "sequential" implementations.

### 7.1 Pattern: Selective Fetching (Partial Objects)
*   **Purpose:** Eliminate over-fetching by only retrieving the specific fields required for the current UI component.
*   **Implementation (C# / EF Core):**
    See [C#](../csharp/CSHARP.md#71-pattern-selective-fetching-partial-objects).

### 7.2 Pattern: The DataLoader (Batching & Deduplication)
*   **Purpose:** Solve the "N+1 Problem" by batching multiple independent requests into a single call.
*   **.NET implementation:** Use **GreenDonut** or similar for .NET batching logic.

## API latency budget

*   **API Response Time**: < 100ms (p95)

## endpoint performance checks

*   **Load Testing**: Use k6 or JMeter to stress test endpoints.

*   **Java profiling:** Use the Java Flight Recorder and allocation/GC guidance in [JAVA.md](../java/JAVA.md#performance).
*   **.NET profiling:** Use `dotnet-counters` and `dotnet-trace` for configured .NET backends.

## API security defaults

- **"Secure by Design, not by Patch."**
- **No PII in URLs:** Never pass email, names, or IDs in Query Parameters. Use Session/Claims or POST bodies.
- Protect nonpublic endpoints using the configured framework's authentication and authorization mechanism.
- **.NET implementation:** Use `[Authorize]` or `[RequirePermission]` unless the endpoint is explicitly public, such as login.

## host dependency verification

- For Java extensions, match host APIs and avoid bundling host-provided classes. Use the build's declared dependency scope.

## Bounded API data access

1. Retrieve only the fields required by the requested view.
2. Apply a hard result limit to every list or search API.
3. Run independent I/O concurrently using the configured language and runtime.

For SQL, use an explicit projection and LIMIT. For C#/EF Core, use the matching projection and Take().
Task.WhenAll is the .NET example. Java code follows its configured concurrency and cancellation model.

---

**Remember**: Fast software feels professional. Slow software feels broken.


## Security scope

Apply [general security](../SECURITY_GUIDELINES.md) and the selected language security sections.
Select clipboard, temporary storage, sensitive memory, and tenant-isolation controls when the changed behavior uses them.
For any AI or ML feature, also apply [AIML_SECURITY.md](../AIML_SECURITY.md).
