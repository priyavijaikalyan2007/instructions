# .NET Backend Library Selection (ASP.NET Core 10.0+)

This document lists the approved and recommended libraries for the backend monolithic service, selected based on the criteria in `BACKEND_LIBRARY_SELECTION.md` (Observability, Performance, Usage, Licensing, and Longevity).

## 1. Core Infrastructure

### Inversion of Control (IoC)
1.  **Microsoft.Extensions.DependencyInjection** (with **Scrutor**)
    *   **Why:** Built-in, high performance, and standard. `Scrutor` adds essential assembly scanning and decorator support without the overhead of a full 3rd party container.
    *   **Backing:** Microsoft / Open Source.

### Logging
1.  **Serilog**
    *   **Why:** The industry standard for structured logging in .NET. Unmatched sink ecosystem (Elasticsearch, Console, File, Seq).
    *   **Backing:** .NET Foundation / Broad Community.

### Observability (Metrics & Tracing)
1.  **OpenTelemetry .NET**
    *   **Why:** Vendor-neutral standard for distributed tracing and metrics. Replaces proprietary agents and legacy libraries like App.Metrics.
    *   **Backing:** CNCF (Cloud Native Computing Foundation).

### Configuration
1.  **Microsoft.Extensions.Configuration**
    *   **Why:** Built-in, robust support for Environment Variables, JSON, User Secrets, and Azure Key Vault.
    *   **Backing:** Microsoft.

---

## 2. Data & Storage

### Database (ORM & Drivers)
1.  **Entity Framework Core** (with **Npgsql**)
    *   **Why:** Primary ORM. Excellent LINQ translation, migrations, and performance in recent versions. `Npgsql` is the best-in-class PostgreSQL driver.
    *   **Backing:** Microsoft / Npgsql Team.
2.  **Dapper**
    *   **Why:** Use *only* for raw SQL performance-critical queries where EF Core overhead is unacceptable.
    *   **Backing:** Stack Overflow.
3.  **AWS SDK for DynamoDB** / **Google.Cloud.Spanner.Data**
    *   **Why:** Official, high-performance clients for specialized cloud databases.
    *   **Backing:** Amazon / Google.

### Caching & State
1.  **FusionCache**
    *   **Why:** Superior to raw `StackExchange.Redis`. Handles "cache stampede" protection, fail-safe (stale data serving), and soft/hard timeouts automatically.
    *   **Backing:** Open Source (ZiggyCreatures) - Widely adopted.
2.  **Microsoft.Orleans**
    *   **Why:** Best-in-class framework for distributed state management (Virtual Actors). Handles high-concurrency state persistence elegantly.
    *   **Backing:** Microsoft Research.

### Object-Object Mapping
1.  **Mapster**
    *   **Why:** Extremely high performance (often beats manual code), easy scanning, and no-allocation options. Preferred over AutoMapper for raw speed.
    *   **Backing:** Open Source.
2.  **Mapperly**
    *   **Why:** Source-generator based (compile-time). Zero runtime overhead.
    *   **Backing:** Open Source.

---

## 3. Communication & Protocols

### Real-Time & RPC
1.  **SignalR**
    *   **Why:** The standard for two-way real-time communication (WebSockets with fallback). Highly scalable with Redis backplane.
    *   **Backing:** Microsoft.
2.  **Grpc.AspNetCore**
    *   **Why:** High-performance, contract-first RPC framework. Essential for inter-service communication.
    *   **Backing:** Microsoft / CNCF.

### File Transfer
1.  **TusDotNet**
    *   **Why:** Implements the open "tus" protocol for resumable file uploads. Essential for handling large file uploads reliably over poor networks.
    *   **Backing:** Open Source (Tus Project).

---

## 4. Utilities & Helpers

### Time & Duration
1.  **NodaTime**
    *   **Why:** Prevents common DateTime bugs. Forces handling of TimeZones and Durations correctly.
    *   **Backing:** Jon Skeet (Google).

### Human Readable IDs
1.  **Sqids** (formerly Hashids)
    *   **Why:** Generates short, unique, YouTube-like IDs from numbers. Collision-free and URL-safe.
    *   **Backing:** Open Source Community standard.
2.  **NanoID**
    *   **Why:** If random non-sequential IDs are required. Faster and safer than GUIDs for URLs.
    *   **Backing:** Open Source.

### Resiliency
1.  **Polly**
    *   **Why:** Mandatory for all external HTTP/Database calls. Handles Retries, Circuit Breakers, and Timeouts.
    *   **Backing:** .NET Foundation.

### Validation
1.  **FluentValidation**
    *   **Why:** Separates validation logic from DTOs. Highly readable, testable, and integrates seamlessly with ASP.NET Core.
    *   **Backing:** .NET Foundation.

### Serialization & Compression
1.  **System.Text.Json**
    *   **Why:** Built-in, zero-allocation, high performance JSON serializer.
    *   **Backing:** Microsoft.
2.  **MessagePack-CSharp**
    *   **Why:** Ultra-fast binary serialization. Use for internal caching/state where JSON size is a bottleneck.
    *   **Backing:** MessagePack Community.
3.  **System.IO.Compression**
    *   **Why:** Built-in high-performance Brotli and Gzip streams.
    *   **Backing:** Microsoft.

---

## 5. Security & Identity

### Authentication & Authorization
1.  **OpenIddict**
    *   **Why:** Flexible, open-source OpenID Connect server. excellent alternative to commercial IdentityServer for custom auth providers.
    *   **Backing:** Open Source (Kevin Chalet).
2.  **Microsoft.Identity.Web**
    *   **Why:** Streamlined auth for Azure AD / Microsoft Entra ID integration.
    *   **Backing:** Microsoft.
3.  **Audit.NET**
    *   **Why:** Extensive framework for auditing operations. Outputs to files, DBs, or Event Log. Essential for compliance.
    *   **Backing:** Open Source (ThePirat).

### Cryptography & Headers
1.  **NWebsec** (or Built-in Middleware)
    *   **Why:** Easy configuration of security headers (CSP, HSTS).
    *   **Backing:** Open Source.
2.  **Sodium.Core** (libsodium-net)
    *   **Why:** Safe, modern cryptography (Ed25519, Argon2) if `System.Security.Cryptography` is insufficient.
    *   **Backing:** Open Source.

---

## 6. AI & Machine Learning

### Frameworks & Agents
1.  **Microsoft.SemanticKernel**
    *   **Why:** The "OS" for AI apps. Orchestrates LLMs (OpenAI, Azure), memory, and plugins. Best-in-class for building agentic workflows in .NET.
    *   **Backing:** Microsoft.
2.  **ML.NET**
    *   **Why:** Train and consume custom machine learning models (Regression, Classification) entirely within .NET.
    *   **Backing:** Microsoft / .NET Foundation.

---

## 7. Cloud & Enterprise Integrations

### Cloud SDKs
1.  **AWS SDK for .NET** / **Azure SDK for .NET** / **Google.Cloud.* Libraries**
    *   **Why:** Always use the official, vendor-supported SDKs for cloud resources.
    *   **Backing:** Amazon / Microsoft / Google.

### Communication & Telephony
1.  **Twilio**
    *   **Why:** Industry standard for SMS, Voice, and WhatsApp. Robust C# SDK.
    *   **Backing:** Twilio.
2.  **Slack.Webhooks** / **Telegram.Bot**
    *   **Why:** Simple, strongly-typed wrappers for chatops and notifications.
    *   **Backing:** Open Source.

---

## 8. System & Low-Level Operations

### Operations & Profiling
1.  **MiniProfiler**
    *   **Why:** Lightweight, production-safe profiler to debug performance issues (SQL, HTTP) in real-time.
    *   **Backing:** Stack Overflow.
2.  **CliWrap**
    *   **Why:** Fluent, async wrapper for running external shell commands/processes. Much safer than `System.Diagnostics.Process`.
    *   **Backing:** Open Source (Tyrrrz).
3.  **DotNext**
    *   **Why:** Advanced low-level primitives, including a RAFT consensus implementation for building distributed clusters.
    *   **Backing:** Open Source (Sakuno).

---

## 9. Content & Presentation

### Templating (Email/Reports)
1.  **Fluid**
    *   **Why:** Safe, fast Liquid template engine. Prevents code injection (unlike Razor) and is user-editable.
    *   **Backing:** Open Source.
2.  **RazorLight**
    *   **Why:** If strict compile-time checking of views is needed and templates are trusted (developer-written).
    *   **Backing:** Open Source.

### Server-Side UI Components
*Note: While client-side JavaScript (React/Angular) is primary, these are excellent for internal tools, admin dashboards, or complex interactive "islands" within server-rendered pages.*

1.  **MudBlazor**
    *   **Type:** Blazor Component Library (Material Design).
    *   **Why:** Extensive collection of attractive, free, and open-source components. Pure C# (no JS dependencies). Perfect for quickly building functional admin panels.
    *   **Backing:** Open Source (MIT).
2.  **Radzen.Blazor**
    *   **Type:** Blazor Component Library.
    *   **Why:** Robust DataGrid, Scheduler, and Charts. Even the free version is extremely feature-rich.
    *   **Backing:** Radzen (Paid support available, library is free).
3.  **Microsoft Fluent UI Blazor**
    *   **Type:** Blazor Component Library (Fluent Design).
    *   **Why:** Implements Microsoft's official design system (looks like Windows 11 / Microsoft 365). Great for corporate internal tools that need to feel "native" to the Microsoft ecosystem.
    *   **Backing:** Microsoft.
4.  **Htmx.Net**
    *   **Type:** ASP.NET Core Helpers for HTMX.
    *   **Why:** Allows for "HTML-over-the-wire" interactivity in standard Razor Pages/MVC without writing complex JavaScript or adopting a full SPA framework. Good for progressive enhancement.
    *   **Backing:** Open Source.
5.  **AntDesign.Blazor**
    *   **Type:** Blazor Component Library.
    *   **Why:** Faithful implementation of the popular Ant Design system (Alibaba). Excellent for enterprise-grade UI complexity.
    *   **Backing:** Open Source (Boyan Zhunet).
6.  **SmartComponents** (Experimental)
    *   **Type:** AI-enhanced Blazor Components.
    *   **Why:** Drop-in components for "Smart Paste", "Smart TextArea" (auto-complete), providing AI features with minimal code.
    *   **Backing:** Microsoft (Steven Sanderson).

### PDF / Excel
1.  **QuestPDF**
    *   **Why:** Modern, fluent API for PDF generation. Much better DX than iText or PDFSharp. (Check license for enterprise).
    *   **Backing:** Open Source.
2.  **ClosedXML**
    *   **Why:** Great for generating Excel files (.xlsx) without installing Office.
    *   **Backing:** Open Source.

---

## 10. Web & API

### API Documentation
1.  **Scalar.AspNetCore**
    *   **Why:** Modern, beautiful replacement for Swagger UI. Better UX.
    *   **Backing:** Scalar.
2.  **Swashbuckle.AspNetCore**
    *   **Why:** The classic reliable fallback if Scalar has compatibility issues.
    *   **Backing:** Community.

### HTTP Clients
1.  **Refit**
    *   **Why:** Type-safe, interface-based HTTP client. Reduces boilerplate significantly compared to `HttpClient`.
    *   **Backing:** .NET Foundation.

### API Versioning
1.  **Asp.Versioning.Http**
    *   **Why:** The official Microsoft approach for REST API versioning.
    *   **Backing:** Microsoft.

---

## 11. Error Handling & Functional Patterns

### Literate Errors
1.  **FluentResults**
    *   **Why:** "Railway Oriented Programming" pattern. Returns Success/Fail objects instead of throwing exceptions for control flow.
    *   **Backing:** Open Source.
2.  **OneOf**
    *   **Why:** Discriminated unions for C#. Great for returning explicit types like `OneOf<User, NotFound, ValidationError>`.
    *   **Backing:** Open Source.

### Standardized Problems
1.  **Hellang.Middleware.ProblemDetails** (or Built-in)
    *   **Why:** Implements RFC 7807 (Problem Details for HTTP APIs) automatically. Maps exceptions to standardized JSON error responses.
    *   **Backing:** Open Source / Microsoft.

---

## 12. Background Jobs & Orchestration

### Background Jobs
1.  **Hangfire**
    *   **Why:** Best-in-class dashboard, persistence, and reliability for fire-and-forget or cron jobs.
    *   **Backing:** HangfireIO.

### Messaging (Pub/Sub)
1.  **MassTransit**
    *   **Why:** The standard for messaging in .NET. Abstracts RabbitMQ/SQS/AzureSB. Includes Sagas and Outbox pattern support.
    *   **Backing:** MassTransit Project.

### Workflow Orchestration
1.  **Elsa Workflows**
    *   **Why:** Code-first or visual workflow engine. Good for complex business logic flows.
    *   **Backing:** Elsa Project.

---

## 13. Testing

### Unit & Integration
1.  **xUnit**
    *   **Why:** Modern, extensible, parallel execution.
    *   **Backing:** .NET Foundation.
2.  **FluentAssertions**
    *   **Why:** Human-readable assertions.
    *   **Backing:** Open Source.
3.  **TestContainers**
    *   **Why:** Spins up real Docker containers (Postgres, Redis) for integration tests. Eliminates "works on my machine" issues.
    *   **Backing:** AtomicJar / Docker.