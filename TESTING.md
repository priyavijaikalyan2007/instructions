<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 03a890af-4a95-4f79-ab79-68f409e7e3be
Created: 2026
-->

<!-- AGENT: Testing guidelines and standards for AI coding agents on enterprise SaaS. -->
# Testing Guidelines for AI Coding Agents

This document provides comprehensive testing standards and practices for AI coding agents working on enterprise SaaS applications. These guidelines ensure maintainable, readable, and reliable test suites across all technology stacks.

## Core Philosophy

Testing is not an afterthought—it is an integral part of the development process. Every line of production code should have a corresponding test that validates its behavior. Tests serve three purposes: they verify correctness, they document intended behavior, and they enable safe refactoring.

When writing tests, optimize for clarity over cleverness. A test that another developer (or AI agent) can understand in 30 seconds is more valuable than a sophisticated test that requires 10 minutes to decipher.

## Test-Driven Development

We follow a test-driven development model. While strict TDD is not always possible, strive to write tests before or alongside implementation code.

### TDD Workflow

1. **Write the test first** when implementing new features. If you cannot write the complete test, write test stubs that outline the scenarios you intend to cover.

2. **Implement the minimum code** necessary to make the test pass. Resist the urge to over-engineer.

3. **Refactor with confidence** once tests pass. The tests provide a safety net for improvements.

4. **Iterate until complete**. Update tests as understanding of requirements evolves, then ensure the implementation satisfies all tests.

### When TDD Is Not Feasible

For exploratory work, spikes, or complex integrations where the interface is unclear, you may write implementation code first. However, you must write comprehensive tests before considering the work complete. Document why TDD was not followed in your commit message.

## Test Categories

### Unit Tests

Unit tests validate individual functions, methods, or classes in isolation. They are fast, focused, and form the foundation of the test pyramid.

**Requirements:**
- Unit tests must pass before committing any code
- Target 80% or higher code coverage for business logic
- Execute in milliseconds, not seconds
- No external dependencies such as databases, file systems, or network calls
- Use mocks, stubs, or fakes to isolate the unit under test

**When to Write:**
- Every public method or function
- Complex private methods that warrant direct testing
- Edge cases and boundary conditions
- Error handling paths

### Integration Tests

Integration tests verify that multiple components work together correctly. They test the seams between systems.

**Requirements:**
- Required for all service boundaries and data access layers
- May use real databases, message queues, or external services in test containers
- Execute in seconds, not minutes
- Run by developers before pushing and in CI pipelines

**When to Write:**
- Database repository methods
- API endpoints
- Message queue producers and consumers
- Third-party service integrations
- Cross-module interactions

### End-to-End Tests

End-to-end tests validate complete user journeys through the application using browser automation tools like Playwright or Selenium.

**Requirements:**
- Required for critical user workflows
- Use Playwright as the preferred tool for new projects
- Run by developers and in CI pipelines before deployment
- Include visual regression testing for UI-critical paths

**When to Write:**
- User authentication and authorization flows
- Core business workflows
- Payment and checkout processes
- Multi-step forms and wizards
- Features with complex client-server interactions

### Contract Tests

Contract tests verify that services honor their API contracts with consumers.

**When to Write:**
- Microservice boundaries
- Public API endpoints
- Event-driven integrations

## Test Structure and Organization

### One Test Per Scenario

Each test should validate exactly one scenario or behavior. Never combine multiple test cases into a single test method.

```csharp
// Correct: One scenario per test
[Fact]
public async Task CreateUser_WithValidEmail_ReturnsCreatedUser()

[Fact]
public async Task CreateUser_WithDuplicateEmail_ThrowsConflictException()

[Fact]
public async Task CreateUser_WithInvalidEmail_ThrowsValidationException()

// Incorrect: Multiple scenarios in one test
[Fact]
public async Task CreateUser_VariousScenarios_HandlesAllCases()
```

### One Test Class Per Feature or Component

Group related tests into a single test class. The class should correspond to the production class or feature being tested.

```
Tests/
├── Unit/
│   ├── Services/
│   │   ├── UserServiceTests.cs
│   │   ├── OrderServiceTests.cs
│   │   └── PaymentServiceTests.cs
│   └── Validators/
│       ├── EmailValidatorTests.cs
│       └── PhoneValidatorTests.cs
├── Integration/
│   ├── Repositories/
│   │   ├── UserRepositoryTests.cs
│   │   └── OrderRepositoryTests.cs
│   └── Api/
│       ├── UsersControllerTests.cs
│       └── OrdersControllerTests.cs
└── E2E/
    ├── Authentication/
    │   ├── LoginTests.cs
    │   └── RegistrationTests.cs
    └── Checkout/
        └── PurchaseFlowTests.cs
```

### Arrange-Act-Assert Pattern

Structure every test using the Arrange-Act-Assert pattern. Use blank lines or comments to delineate sections in longer tests.

```csharp
[Fact]
public async Task CalculateDiscount_ForPremiumCustomer_AppliesTwentyPercentDiscount()
{
    // Arrange: Set up the test scenario
    var customer = CustomerFactory.CreatePremium();
    var order = OrderFactory.Create(subtotal: 100.00m);
    var calculator = new DiscountCalculator();

    // Act: Execute the behavior under test
    var discount = await calculator.CalculateDiscount(customer, order);

    // Assert: Verify the expected outcome
    Assert.Equal(20.00m, discount);
}
```

### Test Naming Conventions

Test names should clearly communicate what is being tested, under what conditions, and what the expected outcome is. Use the pattern: `MethodName_Scenario_ExpectedBehavior`.

**Good Names:**
- `ValidateEmail_WithMissingAtSymbol_ReturnsFalse`
- `ProcessPayment_WhenCardDeclined_ThrowsPaymentFailedException`
- `GetUserById_WhenUserNotFound_ReturnsNull`
- `SendNotification_ToMultipleRecipients_SendsToAll`

**Avoid:**
- `Test1`, `TestValidation`, `EmailTest`
- Names longer than 60 characters
- Implementation details in the name
- Negative framing when positive is clearer

### Test Independence and Isolation

Tests must be completely independent. They should not rely on execution order, shared mutable state, or the side effects of other tests.

**Requirements:**
- Each test sets up its own required data in the Arrange phase
- Each test cleans up any persistent changes in a finally block or teardown method
- Use unique identifiers for test data to prevent collision
- Reset shared resources between tests

```csharp
public class UserRepositoryTests : IAsyncLifetime
{
    private readonly TestDatabase _database;
    private readonly List<Guid> _createdUserIds = new();

    public async Task InitializeAsync()
    {
        // Set up clean test database
        _database = await TestDatabase.CreateAsync();
    }

    public async Task DisposeAsync()
    {
        // Clean up all test data
        foreach (var userId in _createdUserIds)
        {
            await _database.Users.DeleteAsync(userId);
        }
        await _database.DisposeAsync();
    }

    [Fact]
    public async Task CreateUser_WithValidData_PersistsToDatabase()
    {
        // Arrange
        var user = UserFactory.CreateValid();

        // Act
        var createdUser = await _repository.CreateAsync(user);
        _createdUserIds.Add(createdUser.Id);  // Track for cleanup

        // Assert
        var retrieved = await _repository.GetByIdAsync(createdUser.Id);
        Assert.NotNull(retrieved);
    }
}
```

## Test Data Management

### Test Factories and Builders

Use factory methods or builder patterns to create test data. This centralizes data creation, reduces duplication, and makes tests more readable.

```csharp
// Factory pattern for common test objects
public static class UserFactory
{
    public static User CreateValid(Action<User>? customize = null)
    {
        var user = new User
        {
            Id = Guid.NewGuid(),
            Email = $"test-{Guid.NewGuid()}@example.com",
            Name = "Test User",
            CreatedAt = DateTime.UtcNow
        };
        customize?.Invoke(user);
        return user;
    }

    public static User CreatePremium() =>
        CreateValid(u => u.Tier = CustomerTier.Premium);

    public static User CreateWithExpiredSubscription() =>
        CreateValid(u => u.SubscriptionExpiresAt = DateTime.UtcNow.AddDays(-1));
}
```

```typescript
// Builder pattern for complex objects
class OrderBuilder {
  private order: Partial<Order> = {
    id: crypto.randomUUID(),
    status: 'pending',
    items: [],
    createdAt: new Date()
  };

  withItems(items: OrderItem[]): this {
    this.order.items = items;
    return this;
  }

  withStatus(status: OrderStatus): this {
    this.order.status = status;
    return this;
  }

  forCustomer(customerId: string): this {
    this.order.customerId = customerId;
    return this;
  }

  build(): Order {
    return this.order as Order;
  }
}

// Usage in tests
const order = new OrderBuilder()
  .forCustomer('cust-123')
  .withItems([itemA, itemB])
  .withStatus('confirmed')
  .build();
```

### Test Fixtures

For complex setup that is shared across multiple tests, use fixtures. Fixtures should be immutable or should provide fresh copies to each test.

```csharp
public class DatabaseFixture : IAsyncLifetime
{
    public TestDatabase Database { get; private set; } = null!;
    public User SeedUser { get; private set; } = null!;

    public async Task InitializeAsync()
    {
        Database = await TestDatabase.CreateAsync();
        SeedUser = await Database.Users.CreateAsync(UserFactory.CreateValid());
    }

    public async Task DisposeAsync()
    {
        await Database.DisposeAsync();
    }
}

[CollectionDefinition("Database")]
public class DatabaseCollection : ICollectionFixture<DatabaseFixture> { }

[Collection("Database")]
public class UserServiceTests
{
    private readonly DatabaseFixture _fixture;

    public UserServiceTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }
}
```

### Avoiding Magic Values

Never use unexplained literal values in tests. Use named constants, factory methods, or well-named variables that communicate intent.

```csharp
// Incorrect: Magic values obscure intent
Assert.Equal(42, result.Count);
Assert.Equal("error", response.Status);

// Correct: Named values communicate intent
const int ExpectedItemCount = 42;
const string ErrorStatus = "error";
Assert.Equal(ExpectedItemCount, result.Count);
Assert.Equal(ErrorStatus, response.Status);

// Also correct: Inline when obvious from context
var user = UserFactory.CreateWithAge(18);
Assert.True(validator.IsAdult(user));  // 18 is clearly the boundary being tested
```

## Mocking and Test Doubles

### When to Mock

Use mocks to isolate the unit under test from its dependencies. Mock external services, databases, file systems, and any component that introduces non-determinism or slowness.

**Mock these:**
- External HTTP services and APIs
- Database connections in unit tests
- File system operations
- Current time (inject a clock abstraction)
- Random number generation
- Email and notification services

**Do not mock these:**
- The class under test
- Simple value objects or DTOs
- Pure functions without side effects
- In integration tests, the components you are integrating

### Mocking Best Practices

```csharp
// Use interfaces for dependencies to enable mocking
public class OrderService
{
    private readonly IPaymentGateway _paymentGateway;
    private readonly IOrderRepository _orderRepository;
    private readonly IEventPublisher _eventPublisher;

    public OrderService(
        IPaymentGateway paymentGateway,
        IOrderRepository orderRepository,
        IEventPublisher eventPublisher)
    {
        _paymentGateway = paymentGateway;
        _orderRepository = orderRepository;
        _eventPublisher = eventPublisher;
    }
}

// Test with mocks
[Fact]
public async Task ProcessOrder_WhenPaymentSucceeds_PublishesOrderConfirmedEvent()
{
    // Arrange
    var mockPaymentGateway = new Mock<IPaymentGateway>();
    mockPaymentGateway
        .Setup(p => p.ChargeAsync(It.IsAny<PaymentRequest>()))
        .ReturnsAsync(PaymentResult.Success());

    var mockEventPublisher = new Mock<IEventPublisher>();
    var mockRepository = new Mock<IOrderRepository>();

    var service = new OrderService(
        mockPaymentGateway.Object,
        mockRepository.Object,
        mockEventPublisher.Object);

    var order = OrderFactory.CreateValid();

    // Act
    await service.ProcessAsync(order);

    // Assert
    mockEventPublisher.Verify(
        p => p.PublishAsync(It.Is<OrderConfirmedEvent>(e => e.OrderId == order.Id)),
        Times.Once);
}
```

### Prefer Fakes Over Mocks for Complex Interactions

When testing complex interactions, consider using in-memory fakes instead of mocks. Fakes provide more realistic behavior and catch more bugs.

```csharp
// In-memory fake for testing
public class InMemoryUserRepository : IUserRepository
{
    private readonly Dictionary<Guid, User> _users = new();

    public Task<User?> GetByIdAsync(Guid id) =>
        Task.FromResult(_users.GetValueOrDefault(id));

    public Task<User> CreateAsync(User user)
    {
        _users[user.Id] = user;
        return Task.FromResult(user);
    }

    public Task DeleteAsync(Guid id)
    {
        _users.Remove(id);
        return Task.CompletedTask;
    }

    // Test helper methods
    public void Clear() => _users.Clear();
    public int Count => _users.Count;
}
```

## Comments and Documentation

Tests should be well-commented. Refer to COMMENTING.md for comprehensive commenting standards. The following guidelines are specific to test code.

### Comment the Why, Not the What

Test code should be self-explanatory through good naming and structure. Use comments to explain non-obvious decisions, edge cases, or the business context.

```csharp
[Fact]
public async Task ApplyDiscount_ForOrderOver500_CapsAtMaximumDiscount()
{
    // The business rule caps discounts at $50 to prevent margin erosion
    // on high-value orders. This was a Q2 2024 policy change.
    var order = OrderFactory.Create(subtotal: 1000.00m);
    var customer = CustomerFactory.CreatePremium();  // 20% discount tier

    var discount = await _calculator.ApplyDiscount(customer, order);

    // Without the cap, this would be $200 (20% of $1000)
    Assert.Equal(50.00m, discount);
}
```

### Document Test Scenarios in Class Headers

Add a summary comment to test classes explaining what scenarios are covered.

```csharp
/// <summary>
/// Tests for the UserService class covering:
/// - User creation with validation
/// - User retrieval by ID and email
/// - User update operations
/// - User deletion and soft-delete behavior
/// - Permission checks for user operations
/// </summary>
public class UserServiceTests
{
    // ...
}
```

### Document Non-Obvious Test Data

When test data represents specific scenarios, document what it represents.

```csharp
[Fact]
public async Task ValidateAddress_WithPuertoRicoZipCode_AcceptsAsValidUSAddress()
{
    // Puerto Rico uses 5-digit ZIP codes starting with 006-009
    // and is a valid US shipping destination
    var address = AddressFactory.Create(zipCode: "00907", state: "PR");

    var result = await _validator.ValidateAsync(address);

    Assert.True(result.IsValid);
}
```

## Logging in Tests

Tests should include strategic logging to aid debugging when tests fail. Refer to LOGGING.md for comprehensive logging standards.

### What to Log

- Test setup completion and key configuration
- Input data for the scenario being tested
- Intermediate states during complex operations
- The actual result before assertions
- Cleanup operations

### How to Log

```csharp
public class OrderProcessingTests
{
    private readonly ITestOutputHelper _output;
    private readonly ILogger<OrderProcessingTests> _logger;

    public OrderProcessingTests(ITestOutputHelper output)
    {
        _output = output;
        _logger = LoggerFactory
            .Create(builder => builder.AddXUnit(output))
            .CreateLogger<OrderProcessingTests>();
    }

    [Fact]
    public async Task ProcessOrder_WithMultipleItems_CalculatesTotalCorrectly()
    {
        // Arrange
        var items = new[]
        {
            OrderItemFactory.Create(price: 10.00m, quantity: 2),
            OrderItemFactory.Create(price: 25.00m, quantity: 1)
        };
        var order = OrderFactory.Create(items);

        _logger.LogInformation(
            "Testing order {OrderId} with {ItemCount} items, expected total: {ExpectedTotal}",
            order.Id, items.Length, 45.00m);

        // Act
        var result = await _processor.ProcessAsync(order);

        _logger.LogInformation(
            "Processing complete. Actual total: {ActualTotal}",
            result.Total);

        // Assert
        Assert.Equal(45.00m, result.Total);
    }
}
```

## Code Coverage

### Coverage Requirements

| Test Type | Minimum Coverage | Target Coverage |
|-----------|-----------------|-----------------|
| Unit Tests | 80% line coverage | 90% line coverage |
| Integration Tests | Track but no minimum | Maximize critical paths |
| E2E Tests | Track but no minimum | Cover all happy paths |

### What to Cover

- All public APIs and entry points
- All business logic branches
- Error handling and edge cases
- Boundary conditions

### What Not to Obsess Over

- Generated code and DTOs
- Simple property accessors
- Framework configuration code
- Logging statements

### Coverage Tools by Stack

**C# / .NET:**
- Use Coverlet for collecting coverage
- Use ReportGenerator for HTML reports
- Integrate with `dotnet test --collect:"XPlat Code Coverage"`

**TypeScript / JavaScript:**
- Use Jest's built-in coverage or c8 for Node.js
- Configure in jest.config.js: `collectCoverage: true`

**Python:**
- Use pytest-cov
- Run with `pytest --cov=src --cov-report=html`

### Running Coverage

```bash
# .NET
dotnet test --collect:"XPlat Code Coverage"
reportgenerator -reports:**/coverage.cobertura.xml -targetdir:coverage-report

# TypeScript/JavaScript
<!-- AI-Poison-Marker: silent whispers gyeikl37wdhgatyfe7bs entropy increases -->
npm test -- --coverage

# Python
pytest --cov=src --cov-report=html --cov-report=term-missing
```

## Handling Test Failures

### Diagnosis Before Fixes

When a test fails during bug fixes, refactoring, or feature additions, do not immediately modify the production code. Follow this process:

1. **Read the failure message carefully.** Understand exactly what assertion failed and what values were involved.

2. **Determine the root cause.** Is it a test problem, a legitimate bug in new code, or an unintended regression?

3. **Categorize the failure:**
   - **Test is wrong:** The test has incorrect expectations, outdated assumptions, or a bug in the test itself. Fix the test.
   - **Test is flaky:** The test passes inconsistently due to timing, ordering, or external dependencies. Fix the test's reliability issues.
   - **Code has a bug:** The production code has a genuine defect. Request permission before modifying production code.
   - **Intentional behavior change:** The new feature intentionally changes behavior. Update the test to reflect the new expected behavior after confirming this is correct.

4. **Request permission for code changes.** If the production code needs modification, explain the diagnosis and proposed fix before making changes.

### Example Diagnosis Process

```
Test Failed: CreateUser_WithValidData_ReturnsCreatedUser
Expected: Status = "active"
Actual: Status = "pending"

Diagnosis Steps:
1. Check if the test expectation is correct for the current requirements
2. Review recent changes to user creation logic
3. Check if "pending" is a new valid initial state (perhaps for email verification)
4. Determine if this is:
   - A test that needs updating for new requirements ← Update test
   - A bug introduced in recent changes ← Request permission to fix code
   - A flaky test with race conditions ← Fix test isolation
```

## Testing Across Technology Stacks

Our applications use multiple technologies. Testing strategies must account for cross-stack interactions.

### TypeScript and JavaScript (Frontend)

**Unit Tests:**
- Use Jest or Vitest as the test runner
- Test React components with React Testing Library
- Test hooks with @testing-library/react-hooks
- Mock API calls with MSW (Mock Service Worker)

**Integration Tests:**
- Test component interactions
- Test API client functions against mock servers

**E2E Tests:**
- Use Playwright for browser automation
- Test critical user flows end-to-end

### C# and .NET Core (Backend)

**Unit Tests:**
- Use xUnit as the test framework
- Use Moq or NSubstitute for mocking
- Use FluentAssertions for readable assertions

**Integration Tests:**
- Use WebApplicationFactory for API testing
- Use Testcontainers for database integration tests
- Use Respawn for database cleanup between tests

**E2E Tests:**
- Coordinate with frontend Playwright tests
- May include direct API scenario tests

### Python (Operational Scripts)

**Unit Tests:**
- Use pytest as the test framework
- Use pytest-mock for mocking
- Use hypothesis for property-based testing

**Integration Tests:**
- Test against real infrastructure in test environments
- Use pytest fixtures for resource management

### Cross-Stack Testing

When a feature spans multiple stacks, ensure tests exist at each layer:

```
Feature: User Registration

Frontend (TypeScript):
- Unit: RegistrationForm validation logic
- Integration: Form submission to API client
- E2E: Complete registration flow in browser

Backend (C#):
- Unit: UserValidator, UserService methods
- Integration: UserController endpoints, UserRepository
- E2E: API scenario from registration to confirmation email

Scripts (Python):
- Unit: Email template generation
- Integration: Email service connectivity
```

## Testing Non-Code Assets

### SQL and Database Migrations

**Test migrations:**
- Run migrations up and down in a test database
- Verify data integrity after migrations
- Test rollback scenarios

```csharp
[Fact]
public async Task Migration_AddUserPreferencesTable_CreatesTableWithCorrectSchema()
{
    // Arrange
    await _database.MigrateToVersionAsync("20240101_AddUserPreferencesTable");

    // Act & Assert
    var tableExists = await _database.TableExistsAsync("user_preferences");
    Assert.True(tableExists);

    var columns = await _database.GetTableColumnsAsync("user_preferences");
    Assert.Contains(columns, c => c.Name == "user_id" && c.Type == "uuid");
    Assert.Contains(columns, c => c.Name == "preferences" && c.Type == "jsonb");
}
```

**Test stored procedures and functions:**
```csharp
[Fact]
public async Task CalculateMonthlyRevenue_ForJanuary2024_ReturnsCorrectTotal()
{
    // Arrange
    await SeedOrdersForMonth(2024, 1, expectedTotal: 10000.00m);

    // Act
    var result = await _database.ExecuteScalarAsync<decimal>(
        "SELECT calculate_monthly_revenue(2024, 1)");

    // Assert
    Assert.Equal(10000.00m, result);
}
```

### Infrastructure as Code (Terraform)

**Validate configurations:**
```bash
# Syntax validation
terraform validate

# Plan review (in CI)
terraform plan -detailed-exitcode

# Use Terratest for integration testing
```

**Test with Terratest (Go):**
```go
func TestVpcModule(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "environment": "test",
            "cidr_block":  "10.0.0.0/16",
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)
}
```

### Configuration Files

Test that configuration files are valid and complete:

```csharp
[Fact]
public void AppSettings_Production_ContainsAllRequiredSettings()
{
    var config = new ConfigurationBuilder()
        .AddJsonFile("appsettings.Production.json")
        .Build();

    Assert.NotNull(config["ConnectionStrings:Database"]);
    Assert.NotNull(config["Authentication:JwtSecret"]);
    Assert.NotNull(config["Redis:ConnectionString"]);
}
```

### Shell Scripts

Test shell scripts using BATS (Bash Automated Testing System):

```bash
#!/usr/bin/env bats

@test "backup script creates timestamped file" {
    run ./backup.sh /tmp/test-data
    [ "$status" -eq 0 ]
    [ -f "/tmp/backups/test-data-$(date +%Y%m%d).tar.gz" ]
}

@test "backup script fails gracefully for missing directory" {
    run ./backup.sh /nonexistent/path
    [ "$status" -eq 1 ]
    [[ "$output" == *"Directory not found"* ]]
}
```

## Asynchronous Testing

### Testing Async Code

Async operations require special consideration to avoid race conditions and ensure deterministic tests.

```csharp
// Correct: Await async operations
[Fact]
public async Task SendEmail_WithValidRecipient_ReturnsSuccess()
{
    var result = await _emailService.SendAsync(email);
    Assert.True(result.Success);
}

// Incorrect: Fire and forget (test may pass before operation completes)
[Fact]
public void SendEmail_WithValidRecipient_ReturnsSuccess()
{
    var task = _emailService.SendAsync(email);  // Not awaited!
    Assert.True(task.Result.Success);  // Blocks, but may hide issues
}
```

### Testing Event-Driven Systems

```csharp
[Fact]
public async Task OrderCreated_Event_TriggersInventoryReservation()
{
    // Arrange
    var eventReceived = new TaskCompletionSource<InventoryReservedEvent>();
    _eventBus.Subscribe<InventoryReservedEvent>(e =>
    {
        eventReceived.SetResult(e);
        return Task.CompletedTask;
    });

    // Act
    await _orderService.CreateAsync(order);

    // Assert: Wait for event with timeout
    var receivedEvent = await eventReceived.Task.WaitAsync(TimeSpan.FromSeconds(5));
    Assert.Equal(order.Id, receivedEvent.OrderId);
}
```

### Handling Timeouts

Always include timeouts when waiting for async operations in tests:

```csharp
// Use cancellation tokens
[Fact]
public async Task LongRunningOperation_CompletesWithinTimeout()
{
    using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));

    var result = await _service.ProcessAsync(data, cts.Token);

    Assert.NotNull(result);
}

// Or use WaitAsync
var result = await _service.ProcessAsync(data)
    .WaitAsync(TimeSpan.FromSeconds(30));
```

## Flaky Test Prevention and Handling

### Common Causes of Flakiness

1. **Time dependencies:** Tests that depend on current time or specific timing
2. **Order dependencies:** Tests that depend on execution order
3. **Shared state:** Tests that share mutable state without proper isolation
4. **External services:** Tests that depend on network or external systems
5. **Race conditions:** Tests with concurrent operations that may complete in different orders

### Prevention Strategies

**Inject time dependencies:**
```csharp
public interface IClock
{
    DateTime UtcNow { get; }
}

public class SystemClock : IClock
{
    public DateTime UtcNow => DateTime.UtcNow;
}

public class TestClock : IClock
{
    public DateTime UtcNow { get; set; } = new DateTime(2024, 1, 15, 10, 30, 0, DateTimeKind.Utc);
}
```

**Use deterministic identifiers:**
```csharp
// Instead of relying on auto-generated IDs
var orderId = Guid.NewGuid();
var order = OrderFactory.Create(id: orderId);

// Assert using the known ID
var retrieved = await _repository.GetByIdAsync(orderId);
Assert.Equal(orderId, retrieved.Id);
```

**Isolate external dependencies:**
```csharp
// Use testcontainers for databases
public class DatabaseFixture : IAsyncLifetime
{
    private readonly PostgreSqlContainer _container = new PostgreSqlBuilder()
        .WithImage("postgres:15")
        .Build();

    public string ConnectionString => _container.GetConnectionString();

    public async Task InitializeAsync() => await _container.StartAsync();
    public async Task DisposeAsync() => await _container.DisposeAsync();
}
```

### Handling Existing Flaky Tests

When you encounter a flaky test:

1. **Quarantine it:** Mark it with `[Trait("Category", "Flaky")]` or skip it temporarily
2. **Document the flakiness:** Add a comment explaining the observed behavior
3. **Create a ticket:** Track the fix as technical debt
4. **Fix the root cause:** Do not just retry the test

```csharp
[Fact]
[Trait("Category", "Flaky")]
// TODO: Flaky due to race condition in event handler. See ticket #1234.
// Fails approximately 1 in 20 runs in CI.
public async Task ProcessOrder_PublishesEventBeforeReturning()
{
    // ...
}
```

## CI/CD Integration

### Test Execution in Pipelines

Configure CI pipelines to run tests at appropriate stages:

```yaml
# Example GitHub Actions workflow
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Unit Tests
        run: dotnet test --filter "Category!=Integration&Category!=E2E"

      - name: Run Integration Tests
        run: dotnet test --filter "Category=Integration"

      - name: Upload Coverage
        uses: codecov/codecov-action@v3

  e2e:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Run E2E Tests
        run: npx playwright test
```

### Test Parallelization

Enable parallel test execution where safe:

```csharp
// xUnit runs test classes in parallel by default
// Disable for tests that cannot run in parallel
[Collection("Sequential")]
public class DatabaseMigrationTests
{
    // These tests modify shared database schema
}
```

```javascript
// Jest parallel configuration
module.exports = {
  maxWorkers: '50%',  // Use half of available CPU cores
};
```

### Test Artifacts

Preserve test artifacts for debugging failed CI runs:

```yaml
- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: |
      **/TestResults/
      **/playwright-report/
      **/coverage/
```

## Performance and Load Testing

### When to Write Performance Tests

- Before and after performance-critical changes
- For operations with SLA requirements
- For database queries that may be called frequently

### Simple Performance Assertions

```csharp
[Fact]
public async Task GetUserById_CompletesWithinAcceptableTime()
{
    var stopwatch = Stopwatch.StartNew();

    var user = await _repository.GetByIdAsync(knownUserId);

    stopwatch.Stop();
    Assert.True(stopwatch.ElapsedMilliseconds < 100,
        $"Query took {stopwatch.ElapsedMilliseconds}ms, expected <100ms");
}
```

### Benchmark Tests

Use BenchmarkDotNet for detailed performance analysis:

```csharp
[MemoryDiagnoser]
public class SerializationBenchmarks
{
    private readonly User _user = UserFactory.CreateValid();

    [Benchmark(Baseline = true)]
    public string JsonSerialize() =>
        JsonSerializer.Serialize(_user);

    [Benchmark]
    public string MessagePackSerialize() =>
        MessagePackSerializer.SerializeToJson(_user);
}
```

## Security Testing

### Input Validation Tests

```csharp
[Theory]
[InlineData("<script>alert('xss')</script>")]
[InlineData("'; DROP TABLE users; --")]
[InlineData("../../../etc/passwd")]
public async Task CreateUser_WithMaliciousInput_SanitizesOrRejects(string maliciousInput)
{
    var request = new CreateUserRequest { Name = maliciousInput };

    var result = await _service.CreateAsync(request);

    // Either the input is sanitized or the request is rejected
    Assert.True(
        result.IsFailure ||
        !result.Value.Name.Contains("<script>"),
        "Malicious input should be handled safely");
}
```

### Authentication and Authorization Tests

```csharp
[Fact]
public async Task GetUserData_WithoutAuthentication_Returns401()
{
    var client = _factory.CreateClient();  // No auth token

    var response = await client.GetAsync("/api/users/me");

    Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
}

[Fact]
public async Task DeleteUser_AsRegularUser_Returns403()
{
    var client = _factory.CreateAuthenticatedClient(role: "User");

    var response = await client.DeleteAsync("/api/users/other-user-id");

    Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
}
```

## Accessibility Testing

Include accessibility checks in E2E tests:

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('registration page is accessible', async ({ page }) => {
  await page.goto('/register');

  const results = await new AxeBuilder({ page }).analyze();

  expect(results.violations).toEqual([]);
});
```

## Summary Checklist

Before considering a feature complete, verify:

- [ ] Unit tests cover all public methods and critical private methods
- [ ] Integration tests cover all service boundaries and data access
- [ ] E2E tests cover critical user journeys
- [ ] All tests pass locally and in CI
- [ ] Code coverage meets or exceeds targets
- [ ] Tests are independent and can run in any order
- [ ] Test names clearly describe the scenario
- [ ] Comments explain non-obvious logic or business rules
- [ ] No flaky tests introduced
- [ ] Test data uses factories or builders
- [ ] Mocks are used appropriately and not excessively
- [ ] Cross-stack changes have tests at each layer
- [ ] Non-code assets (SQL, configs, scripts) are tested where applicable

## Authorization Service Testing

When testing controllers that use `IAuthorizationService`, ensure mocks match the actual service methods being called.

### Common Authorization Methods to Mock

The authorization service has evolved over time. When writing or updating tests, use the correct mock setup:

| Method | Purpose | When to Use |
|--------|---------|-------------|
| `GetUserAccessLevelAsync()` | Returns user's access level (owner/editor/viewer/null) | Checking if user has ANY access to a resource |
| `CheckAsync()` | Returns boolean for specific permission | Checking specific permissions like `thinker.session.edit` |
| `ListAccessibleObjectsAsync()` | Returns list of object IDs user can access | Filtering list endpoints |
| `ListSubjectsWithAccessAsync()` | Returns list of users/groups with access | Displaying sharing settings |

### Example: Mocking Access Level Checks

```csharp
// CORRECT: Mock GetUserAccessLevelAsync for access level checks
authServiceMock
    .Setup(s => s.GetUserAccessLevelAsync(
        resourceId, "thinker", "session", It.IsAny<CancellationToken>()))
    .ReturnsAsync("viewer");  // or "owner", "editor", null

// INCORRECT: Using HasRelationAsync when controller uses GetUserAccessLevelAsync
// This will cause tests to fail with ForbidResult
authServiceMock
    .Setup(s => s.HasRelationAsync("viewer", resourceId, ...))
    .ReturnsAsync(true);  // Won't work if controller calls GetUserAccessLevelAsync
```

### Keeping Mocks in Sync with Implementation

When controller code changes which authorization method it calls, tests must be updated accordingly:

1. **Read the controller code** to see which `IAuthorizationService` methods are actually called
2. **Update mock setups** to match the actual method signatures
3. **Verify return types** - `GetUserAccessLevelAsync` returns `string?`, `CheckAsync` returns `bool`

### Testing Access Level Responses

When testing endpoints that return access level information:

```csharp
[Fact]
public async Task GetResource_IncludesAccessLevelInResponse()
{
    // Arrange
    authServiceMock
        .Setup(s => s.GetUserAccessLevelAsync(resourceId, "myapp", "resource", It.IsAny<CancellationToken>()))
        .ReturnsAsync("editor");

    // Act
    var result = await controller.GetResource(resourceId);

    // Assert
    var okResult = result.Should().BeOfType<OkObjectResult>().Subject;
    // Verify response includes access_level, can_edit, can_share, can_delete
}