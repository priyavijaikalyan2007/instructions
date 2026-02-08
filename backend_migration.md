# Backend Migration Specification: Python to ASP.NET Core 10.0

## Executive Summary

This specification guides the migration of an existing Python backend (built with Claude Code) to ASP.NET Core 10.0. The goal is to create a production-grade, enterprise-quality B2B SaaS backend with superior code structure, readability, maintainability, and scalability.

---

## Table of Contents

1. [Migration Objectives](#1-migration-objectives)
2. [Architecture Principles](#2-architecture-principles)
3. [C# Language Guidelines](#3-c-language-guidelines)
4. [Project Structure](#4-project-structure)
5. [Framework Selection Matrix](#5-framework-selection-matrix)
6. [Implementation Patterns](#6-implementation-patterns)
7. [Data Access Layer](#7-data-access-layer)
8. [Logging Strategy](#8-logging-strategy)
9. [Documentation Standards](#9-documentation-standards)
10. [Build and Performance](#10-build-and-performance)
11. [Testing Strategy](#11-testing-strategy)
12. [Cloud Deployment (GCP Cloud Run / AWS EKS)](#12-cloud-deployment-gcp-cloud-run--aws-eks)

---

## 1. Migration Objectives

### Primary Goals

- **Code Quality**: Produce clean, readable, maintainable code that reads like a well-written book
- **Performance**: Minimize resource consumption (compute, memory, network) to reduce operational costs
- **Scalability**: Build for enterprise-grade multi-tenant B2B SaaS requirements
- **Debuggability**: All code paths must be understandable using a simple debugger

### Non-Goals

- Over-engineering with excessive abstractions
- Magic/reflection-heavy patterns that obscure control flow
- Framework-generated boilerplate that adds complexity without value

---

## 2. Architecture Principles

### 2.1 Composition Over Inheritance

**DO**: Assemble complex types from smaller, focused components.

```csharp
// CORRECT: Composition
public class Car
{
    public Engine Engine { get; }
    public Chassis Chassis { get; }
    public SteeringSystem Steering { get; }
    public WheelSet Wheels { get; }
    
    public Car(Engine engine, Chassis chassis, SteeringSystem steering, WheelSet wheels)
    {
        Engine = engine;
        Chassis = chassis;
        Steering = steering;
        Wheels = wheels;
    }
}
```

**DON'T**: Create deep inheritance hierarchies with abstract base classes.

```csharp
// AVOID: Unnecessary inheritance
public abstract class Vehicle { }
public abstract class MotorVehicle : Vehicle { }
public abstract class FourWheeledMotorVehicle : MotorVehicle { }
public class Car : FourWheeledMotorVehicle { }
```

### 2.2 Domain-Oriented Object Design

Model types that represent domain concepts with behavior, not just data transfer objects.

```csharp
/// <summary>
/// Represents a user's checklist with full lifecycle management.
/// Encapsulates business logic for loading, modifying, and persisting checklist state.
/// </summary>
public class Checklist
{
    public Guid Id { get; private set; }
    public Guid OwnerId { get; private set; }
    public string Title { get; private set; }
    public IReadOnlyList<ChecklistItem> Items => _items.AsReadOnly();
    
    private readonly List<ChecklistItem> _items;
    
    /// <summary>
    /// Marks the checklist as complete and raises a completion event.
    /// </summary>
    /// <returns>ChecklistCompletedEvent for downstream processing (e.g., email notifications)</returns>
    public ChecklistCompletedEvent Complete()
    {
        // Business logic here
        return new ChecklistCompletedEvent(this);
    }
    
    /// <summary>
    /// Persists the current state to the database.
    /// </summary>
    public async Task SaveAsync(IChecklistRepository repository, CancellationToken ct)
    {
        await repository.UpdateAsync(this, ct);
    }
}
```

### 2.3 Context Pattern for Cross-Cutting Concerns

Use a strongly-typed context object to pass cross-cutting data through the call stack without polluting method signatures.

```csharp
/// <summary>
/// Strongly-typed property bag for request-scoped cross-cutting concerns.
/// Designed for extensibility as new contextual requirements emerge.
/// </summary>
public class OperationContext
{
    public Guid CorrelationId { get; init; }
    public Guid TenantId { get; init; }
    public Guid UserId { get; init; }
    public MetricsCollector Metrics { get; init; }
    public CancellationToken CancellationToken { get; init; }
    
    /// <summary>
    /// Extensible property bag for future cross-cutting concerns.
    /// Use sparingly; prefer strongly-typed properties for common data.
    /// </summary>
    public IDictionary<string, object> Extensions { get; } = new Dictionary<string, object>();
}
```

### 2.4 Standard Design Patterns

Apply these patterns judiciously where they provide clear value:

| Pattern | Use When |
|---------|----------|
| **Decorator** | Adding behavior to existing types without modification |
| **Singleton** | Stateless services, configuration, caches |
| **Factory** | Complex object construction with validation |
| **Strategy** | Interchangeable algorithms (e.g., pricing tiers) |
| **Observer/Event** | Decoupled reactions to state changes |
| **Mediator** | Decoupling request handlers from controllers (via MediatR) |

### 2.5 Minimal Abstractions

**Rule**: If a Service Locator suffices, don't implement full IoC. If a simple class suffices, don't create interfaces and abstract classes.

```csharp
// AVOID: Unnecessary abstraction layers
public interface IEmailService { }
public abstract class BaseEmailService : IEmailService { }
public class SmtpEmailService : BaseEmailService { }
public class EmailServiceFactory : IEmailServiceFactory { }

// PREFER: Simple, direct implementation
public class EmailService
{
    public async Task SendAsync(Email email, CancellationToken ct) { }
}
```

---

## 3. C# Language Guidelines

### 3.1 Prefer Native .NET Solutions

The .NET standard library is extensive and optimized. Use external frameworks only when native solutions are insufficient.

```csharp
// PREFER: Built-in System.Text.Json
var json = JsonSerializer.Serialize(data, JsonSerializerOptions.Default);

// PREFER: Built-in HttpClientFactory
services.AddHttpClient<IExternalApiClient, ExternalApiClient>();

// PREFER: Built-in IDistributedCache
services.AddStackExchangeRedisCache(options => { });
```

### 3.2 Async/Await for All I/O

Use asynchronous I/O throughout to maximize throughput with minimal resource consumption.

```csharp
/// <summary>
/// Retrieves a checklist by ID with full item details.
/// </summary>
/// <param name="id">The unique checklist identifier</param>
/// <param name="ct">Cancellation token for request cancellation</param>
/// <returns>The checklist if found; null otherwise</returns>
public async Task<Checklist?> GetByIdAsync(Guid id, CancellationToken ct)
{
    return await _dbContext.Checklists
        .Include(c => c.Items)
        .FirstOrDefaultAsync(c => c.Id == id, ct);
}
```

### 3.3 Cancellation Token Support

All long-running and I/O operations must accept and respect `CancellationToken`.

```csharp
/// <summary>
/// Processes a batch of items with progress reporting and cancellation support.
/// </summary>
/// <param name="items">Items to process</param>
/// <param name="progress">Optional progress reporter</param>
/// <param name="ct">Cancellation token - checked between each item</param>
public async Task ProcessBatchAsync(
    IEnumerable<Item> items, 
    IProgress<int>? progress, 
    CancellationToken ct)
{
    var processed = 0;
    foreach (var item in items)
    {
        ct.ThrowIfCancellationRequested();
        await ProcessItemAsync(item, ct);
        progress?.Report(++processed);
    }
}
```

### 3.4 Modern C# Features (Use Judiciously)

Balance brevity with readability and maintainability.

```csharp
// GOOD: Primary constructors for simple DTOs
public record ChecklistDto(Guid Id, string Title, IReadOnlyList<ChecklistItemDto> Items);

// GOOD: Pattern matching for clear conditionals
var result = status switch
{
    ChecklistStatus.Draft => HandleDraft(),
    ChecklistStatus.Active => HandleActive(),
    ChecklistStatus.Completed => HandleCompleted(),
    _ => throw new InvalidOperationException($"Unknown status: {status}")
};

// GOOD: Span<T> for performance-critical memory operations
public static ReadOnlySpan<byte> ParseHeader(ReadOnlySpan<byte> data)
{
    return data[..HeaderLength];
}

// AVOID: Excessive brevity that sacrifices clarity
// Bad: var x = items?.FirstOrDefault(i => i?.Value?.Length > 0)?.Value ?? "";
// Good: Extract to well-named method with clear null handling
```

---

## 4. Project Structure

### 4.1 Directory Layout

```
src/
├── MyApp.Api/                    # ASP.NET Core Web API entry point
│   ├── Program.cs                # Minimal hosting setup
│   ├── appsettings.json          # Configuration
│   ├── Controllers/              # API controllers (thin, delegate to services)
│   │   └── ChecklistsController.cs
│   ├── Middleware/               # Custom middleware
│   │   ├── CorrelationIdMiddleware.cs
│   │   └── ExceptionHandlingMiddleware.cs
│   └── Filters/                  # Action filters
│       └── ValidationFilter.cs
│
├── MyApp.Domain/                 # Domain models and business logic
│   ├── Entities/                 # Domain entities with behavior
│   │   ├── Checklist.cs
│   │   └── ChecklistItem.cs
│   ├── Events/                   # Domain events
│   │   └── ChecklistCompletedEvent.cs
│   ├── Services/                 # Domain services
│   │   └── ChecklistService.cs
│   └── Specifications/           # Query specifications (if using Ardalis.Specification)
│       └── ActiveChecklistsSpec.cs
│
├── MyApp.Application/            # Application layer (use cases, orchestration)
│   ├── Commands/                 # CQRS commands (if using MediatR)
│   │   └── CompleteChecklistCommand.cs
│   ├── Queries/                  # CQRS queries
│   │   └── GetChecklistQuery.cs
│   ├── Handlers/                 # Command/Query handlers
│   │   ├── CompleteChecklistHandler.cs
│   │   └── GetChecklistHandler.cs
│   ├── Validators/               # FluentValidation validators
│   │   └── CompleteChecklistValidator.cs
│   └── Mappings/                 # Object mapping profiles
│       └── ChecklistMappings.cs
│
├── MyApp.Infrastructure/         # External concerns implementation
│   ├── Data/                     # Database access
│   │   ├── AppDbContext.cs
│   │   ├── Configurations/       # EF Core entity configurations
│   │   │   └── ChecklistConfiguration.cs
│   │   ├── Repositories/         # Repository implementations
│   │   │   └── ChecklistRepository.cs
│   │   ├── Queries/              # Raw SQL queries (loaded from files)
│   │   │   ├── QueryLoader.cs
│   │   │   └── sql/
│   │   │       ├── GetChecklistSummary.sql
│   │   │       └── GetOverdueItems.sql
│   │   └── Migrations/           # EF Core migrations
│   │
│   ├── Caching/                  # Cache implementations
│   │   └── RedisCacheService.cs
│   ├── Messaging/                # Message bus implementations
│   │   └── MassTransitConfiguration.cs
│   ├── Email/                    # Email service implementations
│   │   ├── EmailService.cs
│   │   └── Templates/            # Email templates
│   │       └── checklist-completed.html
│   └── External/                 # External API clients
│       └── PaymentGatewayClient.cs
│
├── MyApp.Shared/                 # Shared utilities and DTOs
│   ├── DTOs/                     # Data transfer objects
│   │   └── ChecklistDto.cs
│   ├── Extensions/               # Extension methods
│   │   └── StringExtensions.cs
│   └── Constants/                # Application constants
│       └── ErrorCodes.cs
│
└── tests/
    ├── MyApp.UnitTests/
    ├── MyApp.IntegrationTests/
    └── MyApp.ArchitectureTests/
```

### 4.2 Separation Principles

| Layer | Contains | Depends On |
|-------|----------|------------|
| **Api** | Controllers, Middleware, Filters | Application, Shared |
| **Domain** | Entities, Domain Events, Domain Services | None (core) |
| **Application** | Commands, Queries, Handlers, Validators | Domain, Shared |
| **Infrastructure** | DbContext, Repositories, External Clients | Application, Domain, Shared |
| **Shared** | DTOs, Extensions, Constants | None |

---

## 5. Framework Selection Matrix

### 5.1 Core Framework Selections

Use these frameworks consistently. **Do not mix competing frameworks for the same functionality.**

| Category | Selected Framework | Rationale |
|----------|-------------------|-----------|
| **Web Framework** | ASP.NET Core 10.0 | Foundation, Microsoft-supported |
| **ORM** | Entity Framework Core + Npgsql | PostgreSQL support, migrations, LINQ |
| **Micro-ORM** | Dapper | Performance-critical raw SQL queries |
| **JSON** | System.Text.Json | Native, fastest, AOT-compatible |
| **Logging** | Serilog | Structured logging, Elasticsearch sink |
| **Validation** | FluentValidation | Fluent API, separation of concerns |
| **Mapping** | Mapster | Faster than AutoMapper, simpler API |
| **Caching** | FusionCache + StackExchange.Redis | Hybrid cache with stampede protection |
| **Messaging** | MassTransit | RabbitMQ/Amazon SQS abstraction, sagas |
| **Background Jobs** | Hangfire | Persistence, dashboard, recurring jobs |
| **Workflows** | Elsa Workflows | Visual designer, embeddable |
| **Resilience** | Polly | Retry, circuit breaker, timeout |
| **HTTP Clients** | Refit | Type-safe REST clients |
| **API Documentation** | NSwag | OpenAPI + TypeScript client generation |
| **Testing** | xUnit + FluentAssertions | Modern, parallel execution |
| **Mocking** | NSubstitute | Cleaner syntax than Moq |
| **Multi-Tenancy** | Finbuckle.MultiTenant | Comprehensive B2B SaaS support |
| **Feature Flags** | Flagsmith | Self-hosted or cloud, no vendor lock-in |

### 5.2 Framework Decision Rules

1. **Default to .NET native solutions** before considering external frameworks
2. **One framework per concern** — never mix FluentValidation with DataAnnotations for the same validation
3. **Evaluate licensing** — EPPlus, iText, Duende IdentityServer require commercial licenses for revenue >$1M
4. **Prefer source-generator libraries** — Mapperly, System.Text.Json source generators for AOT/performance

---

## 6. Implementation Patterns

### 6.1 Controller Design (Thin Controllers)

Controllers should only route requests and delegate to application services.

```csharp
/// <summary>
/// API endpoints for checklist management.
/// </summary>
[ApiController]
[Route("api/v1/checklists")]
public class ChecklistsController : ControllerBase
{
    private readonly IMediator _mediator;
    
    public ChecklistsController(IMediator mediator)
    {
        _mediator = mediator;
    }
    
    /// <summary>
    /// Retrieves a checklist by its unique identifier.
    /// </summary>
    /// <param name="id">The checklist ID</param>
    /// <param name="ct">Cancellation token</param>
    /// <returns>The checklist details</returns>
    /// <response code="200">Returns the checklist</response>
    /// <response code="404">Checklist not found</response>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(ChecklistDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ChecklistDto>> GetById(Guid id, CancellationToken ct)
    {
        var result = await _mediator.Send(new GetChecklistQuery(id), ct);
        return result is null ? NotFound() : Ok(result);
    }
    
    /// <summary>
    /// Marks a checklist as complete.
    /// </summary>
    /// <param name="id">The checklist ID to complete</param>
    /// <param name="ct">Cancellation token</param>
    /// <returns>No content on success</returns>
    /// <response code="204">Checklist completed successfully</response>
    /// <response code="404">Checklist not found</response>
    /// <response code="400">Checklist already completed or invalid state</response>
    [HttpPost("{id:guid}/complete")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Complete(Guid id, CancellationToken ct)
    {
        await _mediator.Send(new CompleteChecklistCommand(id), ct);
        return NoContent();
    }
}
```

### 6.2 Event-Driven Architecture

Decouple business logic reactions using domain events.

```csharp
/// <summary>
/// Domain event raised when a checklist is marked as complete.
/// Consumers may react by sending notifications, updating analytics, etc.
/// </summary>
public record ChecklistCompletedEvent(
    Guid ChecklistId,
    Guid OwnerId,
    DateTime CompletedAt
) : INotification;

/// <summary>
/// Handles checklist completion by sending email notifications.
/// Configured in DI to subscribe to ChecklistCompletedEvent.
/// </summary>
public class SendCompletionEmailHandler : INotificationHandler<ChecklistCompletedEvent>
{
    private readonly IEmailService _emailService;
    private readonly IUserRepository _userRepository;
    private readonly ITemplateEngine _templates;
    private readonly ILogger<SendCompletionEmailHandler> _logger;
    
    public SendCompletionEmailHandler(
        IEmailService emailService,
        IUserRepository userRepository,
        ITemplateEngine templates,
        ILogger<SendCompletionEmailHandler> logger)
    {
        _emailService = emailService;
        _userRepository = userRepository;
        _templates = templates;
        _logger = logger;
    }
    
    /// <summary>
    /// Sends a completion notification email to the checklist owner.
    /// Failures are logged but do not fail the overall operation.
    /// </summary>
    public async Task Handle(ChecklistCompletedEvent notification, CancellationToken ct)
    {
        _logger.LogInformation(
            "Sending completion email for checklist {ChecklistId} to user {UserId}",
            notification.ChecklistId,
            notification.OwnerId);
        
        var user = await _userRepository.GetByIdAsync(notification.OwnerId, ct);
        if (user?.Email is null)
        {
            _logger.LogWarning("User {UserId} has no email address", notification.OwnerId);
            return;
        }
        
        var body = await _templates.RenderAsync("checklist-completed", new
        {
            UserName = user.DisplayName,
            ChecklistId = notification.ChecklistId,
            CompletedAt = notification.CompletedAt
        }, ct);
        
        await _emailService.SendAsync(new Email
        {
            To = user.Email,
            Subject = "Your checklist is complete!",
            Body = body,
            IsHtml = true
        }, ct);
    }
}
```

### 6.3 Avoid Magic — Explicit Over Implicit

Minimize reflection, attributes, and convention-based behavior that obscures control flow.

```csharp
// AVOID: Magic attribute-based behavior that requires framework knowledge
[AutoValidate]
[AutoLog]
[AutoCache(Duration = 300)]
[AutoRetry(MaxAttempts = 3)]
public class MyHandler { }

// PREFER: Explicit pipeline behavior registration
services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly);
    cfg.AddBehavior<LoggingBehavior>();           // Explicit logging
    cfg.AddBehavior<ValidationBehavior>();        // Explicit validation
});

// Caching is explicit in the handler
public async Task<ChecklistDto?> Handle(GetChecklistQuery query, CancellationToken ct)
{
    var cacheKey = $"checklist:{query.Id}";
    
    return await _cache.GetOrSetAsync(cacheKey, async _ =>
    {
        return await _repository.GetByIdAsync(query.Id, ct);
    }, options => options.SetDuration(TimeSpan.FromMinutes(5)), ct);
}
```

---

## 7. Data Access Layer

### 7.1 Query Separation

Keep SQL queries in separate files, loaded at runtime.

**File: `Infrastructure/Data/Queries/sql/GetChecklistSummary.sql`**
```sql
-- GetChecklistSummary.sql
-- Retrieves a summary of checklist completion status for a tenant.
-- Parameters:
--   @TenantId: The tenant identifier (GUID)
--   @Since: Only include checklists modified after this date
-- Returns: ChecklistId, Title, TotalItems, CompletedItems, CompletionPercentage

SELECT 
    c.id AS "ChecklistId",
    c.title AS "Title",
    COUNT(i.id) AS "TotalItems",
    COUNT(i.id) FILTER (WHERE i.is_completed) AS "CompletedItems",
    CASE 
        WHEN COUNT(i.id) = 0 THEN 0
        ELSE ROUND(100.0 * COUNT(i.id) FILTER (WHERE i.is_completed) / COUNT(i.id), 2)
    END AS "CompletionPercentage"
FROM checklists c
LEFT JOIN checklist_items i ON i.checklist_id = c.id
WHERE c.tenant_id = @TenantId
  AND c.updated_at >= @Since
GROUP BY c.id, c.title
ORDER BY c.updated_at DESC;
```

**File: `Infrastructure/Data/Queries/QueryLoader.cs`**
```csharp
/// <summary>
/// Loads SQL queries from embedded resources or files.
/// Queries are cached after first load for performance.
/// </summary>
public class QueryLoader
{
    private readonly ConcurrentDictionary<string, string> _cache = new();
    private readonly string _basePath;
    
    public QueryLoader(IHostEnvironment env)
    {
        _basePath = Path.Combine(env.ContentRootPath, "Data", "Queries", "sql");
    }
    
    /// <summary>
    /// Loads a SQL query by name (without .sql extension).
    /// </summary>
    /// <param name="queryName">The query file name without extension</param>
    /// <returns>The SQL query text</returns>
    /// <exception cref="FileNotFoundException">Query file does not exist</exception>
    public string Load(string queryName)
    {
        return _cache.GetOrAdd(queryName, name =>
        {
            var path = Path.Combine(_basePath, $"{name}.sql");
            if (!File.Exists(path))
                throw new FileNotFoundException($"Query file not found: {path}");
            return File.ReadAllText(path);
        });
    }
}
```

### 7.2 Repository Pattern with Dapper for Complex Queries

```csharp
/// <summary>
/// Repository for checklist data access.
/// Uses EF Core for standard CRUD, Dapper for complex queries.
/// </summary>
public class ChecklistRepository : IChecklistRepository
{
    private readonly AppDbContext _dbContext;
    private readonly QueryLoader _queries;
    private readonly ILogger<ChecklistRepository> _logger;
    
    public ChecklistRepository(
        AppDbContext dbContext, 
        QueryLoader queries,
        ILogger<ChecklistRepository> logger)
    {
        _dbContext = dbContext;
        _queries = queries;
        _logger = logger;
    }
    
    /// <summary>
    /// Retrieves a checklist by ID using EF Core with eager loading.
    /// </summary>
    public async Task<Checklist?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        return await _dbContext.Checklists
            .Include(c => c.Items)
            .FirstOrDefaultAsync(c => c.Id == id, ct);
    }
    
    /// <summary>
    /// Retrieves checklist summaries using raw SQL for optimal performance.
    /// Uses Dapper for direct query execution against the connection.
    /// </summary>
    /// <param name="tenantId">Tenant filter</param>
    /// <param name="since">Only include checklists modified after this date</param>
    /// <param name="ct">Cancellation token</param>
    /// <returns>Summary DTOs for matching checklists</returns>
    public async Task<IReadOnlyList<ChecklistSummaryDto>> GetSummariesAsync(
        Guid tenantId, 
        DateTime since, 
        CancellationToken ct)
    {
        var sql = _queries.Load("GetChecklistSummary");
        var connection = _dbContext.Database.GetDbConnection();
        
        var command = new CommandDefinition(
            sql, 
            new { TenantId = tenantId, Since = since },
            cancellationToken: ct);
        
        var results = await connection.QueryAsync<ChecklistSummaryDto>(command);
        return results.ToList();
    }
}
```

### 7.3 Security — Parameterized Queries Only

**NEVER** use string interpolation or concatenation for SQL queries.

```csharp
// DANGEROUS: SQL injection vulnerability
var sql = $"SELECT * FROM users WHERE email = '{email}'";  // NEVER DO THIS

// SAFE: Parameterized query
var sql = "SELECT * FROM users WHERE email = @Email";
await connection.QueryAsync<User>(sql, new { Email = email });
```

---

## 8. Logging Strategy

### 8.1 Serilog Configuration

```csharp
// Program.cs
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)
    .MinimumLevel.Override("Microsoft.EntityFrameworkCore", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithProperty("Application", "MyApp")
    .Enrich.WithProperty("Environment", builder.Environment.EnvironmentName)
    .WriteTo.Console(outputTemplate: 
        "[{Timestamp:HH:mm:ss} {Level:u3}] {SourceContext}: {Message:lj}{NewLine}{Exception}")
    .WriteTo.Elasticsearch(new ElasticsearchSinkOptions(new Uri(elasticUrl))
    {
        AutoRegisterTemplate = true,
        IndexFormat = "myapp-logs-{0:yyyy.MM.dd}",
        ModifyConnectionSettings = conn => conn.BasicAuthentication(user, pass)
    })
    .CreateLogger();

builder.Host.UseSerilog();
```

### 8.2 Structured Logging Practices

```csharp
/// <summary>
/// Service for checklist business operations.
/// </summary>
public class ChecklistService
{
    private readonly ILogger<ChecklistService> _logger;
    
    /// <summary>
    /// Completes a checklist and publishes the completion event.
    /// </summary>
    /// <param name="checklistId">The checklist to complete</param>
    /// <param name="userId">The user performing the action</param>
    /// <param name="ct">Cancellation token</param>
    /// <exception cref="NotFoundException">Checklist does not exist</exception>
    /// <exception cref="InvalidOperationException">Checklist already completed</exception>
    public async Task CompleteAsync(Guid checklistId, Guid userId, CancellationToken ct)
    {
        // CORRECT: Structured logging with named properties
        _logger.LogInformation(
            "Completing checklist {ChecklistId} for user {UserId}",
            checklistId,
            userId);
        
        try
        {
            // ... business logic
            
            _logger.LogInformation(
                "Checklist {ChecklistId} completed successfully in {ElapsedMs}ms",
                checklistId,
                stopwatch.ElapsedMilliseconds);
        }
        catch (Exception ex)
        {
            // CORRECT: Exception as first parameter, then message template
            _logger.LogError(ex,
                "Failed to complete checklist {ChecklistId} for user {UserId}",
                checklistId,
                userId);
            throw;
        }
    }
}
```

### 8.3 Dynamic Log Level Configuration

Support runtime log level changes via configuration.

```csharp
// appsettings.json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning",
        "MyApp.Infrastructure.Data": "Debug"  // Enable debug for data layer
      }
    },
    "DynamicLevels": {
      "PerUser": {
        "user-123": "Debug"  // Debug logging for specific user
      },
      "PerTenant": {
        "tenant-456": "Verbose"  // Verbose logging for specific tenant
      }
    }
  }
}
```

---

## 9. Documentation Standards

### 9.1 XML Documentation Requirements

Every public type and method must have XML documentation.

```csharp
/// <summary>
/// Represents a user's checklist for task management.
/// </summary>
/// <remarks>
/// Checklists support hierarchical items, completion tracking, and event notifications.
/// A checklist belongs to exactly one tenant and one owner.
/// 
/// Lifecycle states:
/// - Draft: Initial state, items can be added/removed
/// - Active: Published for use, items can be completed
/// - Completed: All items done or manually marked complete
/// - Archived: Soft-deleted, retained for audit purposes
/// </remarks>
public class Checklist
{
    /// <summary>
    /// Marks a checklist item as completed.
    /// </summary>
    /// <param name="itemId">The item identifier within this checklist</param>
    /// <param name="completedBy">The user marking the item complete</param>
    /// <param name="notes">Optional completion notes</param>
    /// <returns>True if the item was marked complete; false if already complete</returns>
    /// <exception cref="ArgumentException">
    /// Thrown when <paramref name="itemId"/> does not exist in this checklist.
    /// </exception>
    /// <exception cref="InvalidOperationException">
    /// Thrown when the checklist is not in Active state.
    /// </exception>
    /// <example>
    /// <code>
    /// var checklist = await repository.GetByIdAsync(id, ct);
    /// if (checklist.MarkItemComplete(itemId, userId, "Verified by QA"))
    /// {
    ///     await repository.UpdateAsync(checklist, ct);
    /// }
    /// </code>
    /// </example>
    public bool MarkItemComplete(Guid itemId, Guid completedBy, string? notes = null)
    {
        // Implementation
    }
}
```

### 9.2 Documentation Focus

| Document | Don't Document |
|----------|----------------|
| **Why** this approach was chosen | **How** the algorithm works (code is self-explanatory) |
| **What** the method does (behavior) | Implementation details obvious from code |
| **Inputs** with validation constraints | Every line of code |
| **Outputs** with possible values | Temporary variables |
| **Failure modes** with error codes | Private helper methods (unless complex) |

---

## 10. Build and Performance

### 10.1 Project Configuration

```xml
<!-- Directory.Build.props (solution root) -->
<Project>
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <OutputPath>$(SolutionDir)artifacts\$(Configuration)\$(MSBuildProjectName)</OutputPath>
  </PropertyGroup>
</Project>
```

### 10.2 Performance Requirements

| Optimization | Implementation |
|--------------|----------------|
| **Response Compression** | Enable Brotli/Gzip via `ResponseCompression` middleware |
| **JSON Source Generators** | Use `[JsonSerializable]` for AOT-compatible serialization |
| **Connection Pooling** | Configure Npgsql connection pool (min 10, max 100) |
| **Caching** | FusionCache with Redis backplane for distributed scenarios |
| **Async Streaming** | Use `IAsyncEnumerable` for large result sets |
| **Memory** | Use `Span<T>`, `Memory<T>` for buffer operations |

### 10.3 Build Output Structure

```
artifacts/
├── Debug/
│   ├── MyApp.Api/
│   ├── MyApp.Domain/
│   └── ...
├── Release/
│   ├── MyApp.Api/
│   ├── MyApp.Domain/
│   └── ...
└── publish/
    └── MyApp.Api/          # Self-contained deployment package
```

---

## 11. Testing Strategy

### 11.1 Test Organization

```csharp
// Unit test example
public class ChecklistServiceTests
{
    private readonly IChecklistRepository _repository;
    private readonly IMediator _mediator;
    private readonly ChecklistService _sut;
    
    public ChecklistServiceTests()
    {
        _repository = Substitute.For<IChecklistRepository>();
        _mediator = Substitute.For<IMediator>();
        _sut = new ChecklistService(_repository, _mediator);
    }
    
    [Fact]
    public async Task CompleteAsync_WhenChecklistExists_PublishesCompletionEvent()
    {
        // Arrange
        var checklistId = Guid.NewGuid();
        var userId = Guid.NewGuid();
        var checklist = new ChecklistBuilder().WithId(checklistId).Build();
        
        _repository.GetByIdAsync(checklistId, Arg.Any<CancellationToken>())
            .Returns(checklist);
        
        // Act
        await _sut.CompleteAsync(checklistId, userId, CancellationToken.None);
        
        // Assert
        await _mediator.Received(1).Publish(
            Arg.Is<ChecklistCompletedEvent>(e => e.ChecklistId == checklistId),
            Arg.Any<CancellationToken>());
    }
}
```

### 11.2 Integration Tests with TestContainers

```csharp
public class ChecklistRepositoryIntegrationTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres;
    private AppDbContext _dbContext = null!;
    
    public ChecklistRepositoryIntegrationTests()
    {
        _postgres = new PostgreSqlBuilder()
            .WithImage("postgres:16-alpine")
            .Build();
    }
    
    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();
        
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseNpgsql(_postgres.GetConnectionString())
            .Options;
        
        _dbContext = new AppDbContext(options);
        await _dbContext.Database.MigrateAsync();
    }
    
    public async Task DisposeAsync()
    {
        await _dbContext.DisposeAsync();
        await _postgres.DisposeAsync();
    }
    
    [Fact]
    public async Task GetByIdAsync_WhenExists_ReturnsChecklistWithItems()
    {
        // Arrange
        var checklist = new ChecklistBuilder()
            .WithItems(3)
            .Build();
        
        _dbContext.Checklists.Add(checklist);
        await _dbContext.SaveChangesAsync();
        
        var repository = new ChecklistRepository(_dbContext, new QueryLoader(/* ... */));
        
        // Act
        var result = await repository.GetByIdAsync(checklist.Id, CancellationToken.None);
        
        // Assert
        result.Should().NotBeNull();
        result!.Items.Should().HaveCount(3);
    }
}
```

---

## 12. Cloud Deployment (GCP Cloud Run / AWS EKS)

### 12.1 Container Configuration

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine AS base
WORKDIR /app
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENV DOTNET_RUNNING_IN_CONTAINER=true

FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build
WORKDIR /src
COPY ["src/MyApp.Api/MyApp.Api.csproj", "MyApp.Api/"]
COPY ["src/MyApp.Domain/MyApp.Domain.csproj", "MyApp.Domain/"]
COPY ["src/MyApp.Application/MyApp.Application.csproj", "MyApp.Application/"]
COPY ["src/MyApp.Infrastructure/MyApp.Infrastructure.csproj", "MyApp.Infrastructure/"]
COPY ["src/MyApp.Shared/MyApp.Shared.csproj", "MyApp.Shared/"]
RUN dotnet restore "MyApp.Api/MyApp.Api.csproj"
COPY src/ .
RUN dotnet publish "MyApp.Api/MyApp.Api.csproj" -c Release -o /app/publish --no-restore

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
# Run as non-root user for security
USER app
ENTRYPOINT ["dotnet", "MyApp.Api.dll"]
```

### 12.2 Cloud-Native Configuration

```csharp
// Program.cs - Cloud-agnostic configuration
var builder = WebApplication.CreateBuilder(args);

// Configuration sources (environment variables take precedence)
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true)
    .AddEnvironmentVariables("MYAPP_");  // Prefix for app-specific env vars

// Health checks for container orchestration
builder.Services.AddHealthChecks()
    .AddNpgSql(builder.Configuration.GetConnectionString("PostgreSQL")!)
    .AddRedis(builder.Configuration.GetConnectionString("Redis")!)
    .AddRabbitMQ(rabbitConnectionString: builder.Configuration.GetConnectionString("RabbitMQ")!);

// Graceful shutdown support (critical for Cloud Run / EKS)
builder.Services.Configure<HostOptions>(options =>
{
    options.ShutdownTimeout = TimeSpan.FromSeconds(30);
});
```

### 12.3 Secrets Management

Use cloud-native secrets management instead of hardcoded configuration.

**GCP Cloud Run:**
```csharp
// Install: Google.Cloud.SecretManager.V1
builder.Configuration.AddGoogleCloudSecretManager(
    projectId: builder.Configuration["GCP_PROJECT_ID"]);
```

**AWS EKS:**
```csharp
// Install: AWSSDK.SecretsManager, Amazon.Extensions.Configuration.SystemsManager
builder.Configuration
    .AddSecretsManager(configurator: options =>
    {
        options.SecretFilter = entry => entry.Name.StartsWith("myapp/");
        options.KeyGenerator = (_, key) => key.Replace("myapp/", "").Replace("/", ":");
    })
    .AddSystemsManager("/myapp/config");  // AWS Parameter Store
```

**Cloud-Agnostic (HashiCorp Vault):**
```csharp
// Install: VaultSharp.Extensions.Configuration
builder.Configuration.AddVaultConfiguration(
    () => new VaultOptions(
        vaultAddress: builder.Configuration["VAULT_ADDR"],
        vaultToken: builder.Configuration["VAULT_TOKEN"]),
    basePath: "secret/myapp",
    mountPoint: "secret");
```

### 12.4 Platform-Specific Considerations

| Aspect | GCP Cloud Run | AWS EKS |
|--------|---------------|---------|
| **Scaling** | Automatic (0 to N) | HPA + Cluster Autoscaler |
| **Secrets** | Secret Manager | Secrets Manager / Parameter Store |
| **Database** | Cloud SQL (PostgreSQL) | RDS PostgreSQL / Aurora |
| **Redis** | Memorystore | ElastiCache |
| **Message Queue** | Pub/Sub or self-managed RabbitMQ | Amazon SQS / Amazon MQ (RabbitMQ) |
| **Logging** | Cloud Logging (stdout captured) | CloudWatch (Fluent Bit sidecar) |
| **Load Balancing** | Built-in | ALB Ingress Controller |
| **Service Mesh** | Cloud Run handles internally | AWS App Mesh / Istio (optional) |

### 12.5 Environment Variables Pattern

```yaml
# Example: Cloud Run service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: myapp-api
spec:
  template:
    spec:
      containers:
        - image: gcr.io/PROJECT_ID/myapp-api:latest
          env:
            - name: MYAPP_ConnectionStrings__PostgreSQL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: connection-string
            - name: MYAPP_ConnectionStrings__Redis
              value: "redis-host:6379"
            - name: ASPNETCORE_ENVIRONMENT
              value: "Production"
          resources:
            limits:
              cpu: "2"
              memory: "1Gi"
```

```yaml
# Example: EKS deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-api
spec:
  template:
    spec:
      serviceAccountName: myapp-service-account  # For IRSA (IAM Roles for Service Accounts)
      containers:
        - name: myapp-api
          image: 123456789.dkr.ecr.region.amazonaws.com/myapp-api:latest
          env:
            - name: MYAPP_ConnectionStrings__PostgreSQL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: connection-string
          envFrom:
            - configMapRef:
                name: myapp-config
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
```

### 12.6 Health Check Endpoints

```csharp
// Program.cs
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false  // Liveness: just checks if app responds
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")  // Readiness: checks dependencies
});

app.MapHealthChecks("/health/startup", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("startup")  // Startup: one-time init checks
});
```

---

## Appendix A: Migration Checklist

Use this checklist to track migration progress:

- [ ] **Phase 1: Project Setup**
  - [ ] Create solution structure with all projects
  - [ ] Configure Directory.Build.props
  - [ ] Set up Serilog with Elasticsearch sink
  - [ ] Configure EF Core with Npgsql

- [ ] **Phase 2: Domain Layer**
  - [ ] Migrate domain entities with behavior
  - [ ] Define domain events
  - [ ] Implement domain services

- [ ] **Phase 3: Infrastructure**
  - [ ] Configure DbContext with entity configurations
  - [ ] Implement repositories (EF Core + Dapper)
  - [ ] Set up MassTransit for messaging
  - [ ] Configure Redis caching with FusionCache

- [ ] **Phase 4: Application Layer**
  - [ ] Implement MediatR commands/queries
  - [ ] Create FluentValidation validators
  - [ ] Configure Mapster mappings

- [ ] **Phase 5: API Layer**
  - [ ] Create controllers (thin, delegate to MediatR)
  - [ ] Configure middleware pipeline
  - [ ] Set up NSwag for OpenAPI
  - [ ] Implement health checks (liveness, readiness, startup)

- [ ] **Phase 6: Testing**
  - [ ] Unit tests with xUnit + NSubstitute
  - [ ] Integration tests with TestContainers
  - [ ] Architecture tests with NetArchTest

- [ ] **Phase 7: Performance**
  - [ ] Enable response compression
  - [ ] Configure JSON source generators
  - [ ] Optimize connection pools
  - [ ] Benchmark critical paths

- [ ] **Phase 8: Cloud Deployment**
  - [ ] Create optimized multi-stage Dockerfile
  - [ ] Configure secrets management (GCP Secret Manager / AWS Secrets Manager / Vault)
  - [ ] Set up environment-specific configuration
  - [ ] Configure container resource limits
  - [ ] Implement graceful shutdown handling
  - [ ] Set up CI/CD pipeline for container builds
  - [ ] Configure logging for cloud platform (stdout for Cloud Run, Fluent Bit for EKS)

---

## Appendix B: Quick Reference — When to Use What

| Scenario | Framework | Notes |
|----------|-----------|-------|
| Standard CRUD | EF Core | Include eager loading |
| Complex reports | Dapper + SQL files | Raw SQL for performance |
| API validation | FluentValidation | Separate validator classes |
| Object mapping | Mapster | Configure in Application layer |
| Background jobs | Hangfire | With PostgreSQL storage |
| Async messaging | MassTransit | RabbitMQ (self-managed) or Amazon SQS |
| User workflows | Elsa Workflows | Embeddable visual designer |
| HTTP clients | Refit | Define interface, Refit implements |
| Resilience | Polly | Wrap all external calls |
| Caching | FusionCache | Hybrid with Redis backplane |
| Feature flags | Flagsmith | Self-hosted or cloud, vendor-neutral |
| Multi-tenancy | Finbuckle.MultiTenant | Required for B2B SaaS |
| Secrets (GCP) | Google.Cloud.SecretManager | GCP Secret Manager integration |
| Secrets (AWS) | AWSSDK.SecretsManager | AWS Secrets Manager integration |
| Secrets (portable) | VaultSharp | HashiCorp Vault, cloud-agnostic |
| Container health | AspNetCore.Diagnostics.HealthChecks | Liveness/readiness probes |

---

*Document Version: 1.0*  
*Last Updated: January 2026*  
*For use with: Claude Code + ASP.NET Core 10.0*
