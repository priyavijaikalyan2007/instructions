<!-- AGENT: Criteria and guidelines for selecting third-party backend libraries. -->

# Backend Library Selection Guidelines

This document outlines the mandatory criteria and preferred categories for selecting third-party libraries for the backend services. All engineering agents and team members must adhere to these guidelines when introducing new dependencies to the project.

## 1. Selection Guidelines

When evaluating a library for inclusion in the codebase, assess it against the following prioritized criteria:

### 1.1 Observability (Critical)
*   **Requirement:** The library must emit internal logs and metrics.
*   **Standard:** It should support or integrate easily with well-known logging abstractions (e.g., Serilog, Log4net, Microsoft.Extensions.Logging) to ensure its inner functioning is exposable.
*   **Goal:** We must be able to debug issues within the library in production without needing to attach a debugger or fork the source.

### 1.2 Performance
*   **Requirement:** The library must be highly performant and memory-efficient.
*   **Evaluation:** Look for benchmarks, low allocation patterns (e.g., `Span<T>` usage in .NET), and suitability for high-throughput scenarios.

### 1.3 Usage & Community
*   **Requirement:** The library must have wide industry usage and an active community.
*   **Signs of Health:** Frequent commits, recent releases, responsive issue trackers, and a large number of stars/forks on repositories like GitHub.

### 1.4 Licensing
*   **Requirement:** Open source with a permissive license.
*   **Allowed Licenses:** MIT, Apache 2.0, BSD, etc.
*   **Prohibited:** GPL or any viral license that requires open-sourcing our proprietary code.
*   **Exception:** Closed source libraries are acceptable *only* if they have an extensive, permanently free option and are industry standards, but open source is strictly preferred.

### 1.5 Cloud-Native Suitability
*   **Requirement:** Suitable for use in high-performance, stateless backend cloud services.
*   **Patterns:** Must support dependency injection, asynchronous programming (async/await), and be thread-safe.

### 1.6 Documentation
*   **Requirement:** Extensive, clear, and up-to-date documentation.
*   **Details:** Should include API references, getting started guides, and common usage examples.

### 1.7 Longevity
*   **Requirement:** Proven track record of stability.
*   **Metric:** Should be in wide use for at least 2-3 years. Avoid "flavor of the month" libraries that may be abandoned quickly.

### 1.8 Corporate/Foundation Backing (Preferred)
*   **Preference:** Libraries maintained or contributed to by major, well-known technology companies (e.g., Microsoft, Google, Amazon, Netflix, Uber, Lyft, Airbnb, Facebook) or established foundations (e.g., Apache, CNCF, .NET Foundation).
*   **Avoid:** Critical infrastructure dependencies maintained by a single, unaffiliated developer without a succession plan, unless no other viable option exists.

### 1.9 Ranked Options
*   **Strategy:** If multiple viable candidates exist, rank them (Top 1, 2, 3) based on adherence to the above guidelines. Do not list more than 3 options.

---

## 2. Library Categories

Agents and engineers should select libraries for the following capabilities using the guidelines above:

### Core Infrastructure
*   **Inversion of Control (IoC) / Dependency Injection:** Containers for managing dependencies and lifecycles.
*   **Logging & Observability:** Structured logging, metrics collection, and distributed tracing.
*   **Configuration:** Providers for reading settings from env vars, files, or secrets managers.

### Data & Storage
*   **Database Drivers / ORMs:** High-performance clients for SQL (PostgreSQL, SQL Server) and NoSQL databases.
*   **Object-Object Mapping:** Efficient mapping between domain entities and DTOs/Data Models.
*   **Distributed Caching:** Clients for Redis, Memcached, etc.

### Utilities & Helpers
*   **Time & Duration:** Handling dates, times, timezones, and durations (e.g., NodaTime).
*   **Human Readable Entities / IDs:** Generating slug-friendly or user-friendly IDs (e.g., NanoID, Sqids).
*   **Literate Errors:** Libraries for structured, readable, and machine-parsable error handling (e.g., Result pattern, Problem Details).
*   **Serialization:** High-performance JSON, Protobuf, or MessagePack serializers.
*   **Resiliency:** Retry policies, circuit breakers, and rate limiting (e.g., Polly).

### Content & Presentation
*   **Templating Engines:** Rendering text-based content for emails, reports, or server-side views (e.g., Handlebars, Liquid, Razor).
*   **UI Components:** (If applicable to backend-served frontends) Component libraries for administrative dashboards or internal tools.

### Web & API
*   **HTTP Clients:** Resilient and performant clients for calling external APIs.
*   **Validation:** Fluent validation for request models and domain objects.
*   **API Documentation:** OpenAPI/Swagger generation.
