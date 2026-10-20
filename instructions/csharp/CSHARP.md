<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: d33479b4-7501-42e5-8f62-0dd924d6e250
Created: 2026
-->

<!-- AGENT: C# conventions and task examples; load only when this language is in scope. -->

# C# instructions

Read this guide when the task changes C# source or its language-specific build and test configuration.
Examples in instruction documents do not make a language part of the consuming project.
Start with references, formatting, naming, and file organization when those sections exist.
Read task sections as needed. Read pattern examples only for patterns selected during planning.
Shared policies remain in the topic guides. Read only the topics that apply to the task.
Do not weaken a shared requirement because this guide omits it.

Shared rules: [Style](../CODING_STYLE.md), [Comments](../COMMENTING.md), [Markers](../MARKERS.md), [Testing](../TESTING.md), [Logging](../LOGGING.md), [Performance](../PERFORMANCE.md), [Patterns](../GOF_PATTERNS.md).

Apply [shared style](../CODING_STYLE.md), including Allman braces, four-space indentation, and one type per file.
Use only the grammar exceptions stated in this guide.
If an example shows several top-level types, put each type in its own file in production.
Examples may omit surrounding project types or test fixtures. Use the repository's configured dependencies and contracts.

Read by task: [References](#references), [Style examples](#style-examples), [Naming](#naming), [File organization](#file-organization), [Language constructs](#language-constructs), [Comments](#comments), [Comment examples](#comment-examples), [Navigation markers](#navigation-markers), [Folding](#folding), [Marker examples](#marker-examples), [Testing](#testing), [Test naming](#test-naming), [Test examples](#test-examples), [Authorization service testing](#authorization-service-testing), [Coverage](#coverage), [Logging](#logging), [Logging examples](#logging-examples), [Performance](../backend/BACKEND.md#aspnet-core-performance-guidance), [Performance examples](#performance-examples), [Secret handling](#secret-handling), [Design patterns](#design-patterns).

## References

1. Follow [.NET Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions) first
2. Follow [Google C# Style Guide](https://google.github.io/styleguide/csharp-style.html) next
3. Apply the overrides in this document

## Style examples

### Indentation and Line Length

```csharp
// Bad
a(); b();
int x = 1, y = 2, z = 3;

// Good
a();
b();

int x = 1;
int y = 2;
int z = 3;
```

### Brace Style

```csharp
// C# - Allman style
public class OrderProcessor
{
    public void ProcessOrder(Order order)
    {
        if (order.IsValid)
        {
            ExecuteOrder(order);
        }
        else
        {
            RejectOrder(order);
        }
    }
}
```

### Always Use Braces

```csharp
// Bad
if (isValid)
    Process();

// Good
if (isValid)
{
    Process();
}

// Bad (lambda)
items.Select(x => x * 2);

// Good (lambda with body)
items.Select(x =>
{
    return x * 2;
});
```

### Parentheses for Clarity

```csharp
// Bad
int result = a + b * c >> 2;

// Good
int result = (a + (b * c)) >> 2;

// Bad
if (a && b || c)

// Good
if ((a && b) || c)
```

### Whitespace for Readability

```csharp
// Bad
var transaction = CreateTransaction();
transactionCount += 1;
ProcessNextItem();
ValidateState();

// Good
var transaction = CreateTransaction();

transactionCount += 1;

ProcessNextItem();
ValidateState();
```

### Parameter Alignment

```csharp
// Short parameter list - single line is fine
public void Save(string name, int id)

// Long parameter list - align on new lines
public async Task<OrderResult> ProcessOrderAsync(
    Order order,
    Customer customer,
    PaymentMethod paymentMethod,
    ShippingAddress shippingAddress,
    CancellationToken cancellationToken)
{
    // ...
}
```

```csharp
// Variable alignment
var customerName    = "Acme Corp";
var orderId         = 12345;
var totalAmount     = 999.99m;
var isHighPriority  = true;
```

### Variable Naming Guidelines

```csharp
// Domain-specific naming for a chemistry application
public class ReactionSimulator
{
    public Reaction SimulateReaction(
        Catalyst catalyst,
        List<Reagent> reagents,
        EquilibriumConditions conditions)
    {
        for (int i = 0; i < reagents.Count; i++)
        {
            var reagent = reagents[i];
            // Process reagent...
        }
    }
}
```

### One Type Per File

```
// Bad - all in Person.cs
Person.cs contains:
  - Person
  - IPerson
  - PersonFactory
  - PersonBuilder

// Good - separate files
Person.cs
IPerson.cs
PersonFactory.cs
PersonBuilder.cs
```

### Nesting Limits

```csharp
// Bad - too deeply nested
public void ProcessOrders(List<Order> orders)
{
    foreach (var order in orders)                           // Level 1
    {
        if (order.IsValid)                                  // Level 2
        {
            foreach (var item in order.Items)               // Level 3
            {
                if (item.RequiresProcessing)                // Level 4
                {
                    if (item.HasInventory)                  // Level 5 - TOO DEEP!
                    {
                        ProcessItem(item);
                    }
                }
            }
        }
    }
}

// Good - refactored with early returns and extracted methods
public void ProcessOrders(List<Order> orders)
{
    foreach (var order in orders)
    {
        ProcessOrder(order);
    }
}

private void ProcessOrder(Order order)
{
    if (!order.IsValid)
    {
        return;
    }

    foreach (var item in order.Items)
    {
        ProcessItemIfEligible(item);
    }
}

private void ProcessItemIfEligible(OrderItem item)
{
    if (!item.RequiresProcessing || !item.HasInventory)
    {
        return;
    }

    ProcessItem(item);
}
```

### Early Returns (Guard Clauses)

```csharp
// Bad - deeply nested validation
public OrderResult ProcessOrder(Order order)
{
    if (order != null)
    {
        if (order.Items.Count > 0)
        {
            if (order.Customer != null)
            {
                // Actual logic buried deep
                return ExecuteOrder(order);
            }
            else
            {
                return OrderResult.InvalidCustomer;
            }
        }
        else
        {
            return OrderResult.NoItems;
        }
    }
    else
    {
        return OrderResult.NullOrder;
    }
}

// Good - guard clauses with early returns
public OrderResult ProcessOrder(Order order)
{
    if (order == null)
    {
        return OrderResult.NullOrder;
    }

    if (order.Items.Count == 0)
    {
        return OrderResult.NoItems;
    }

    if (order.Customer == null)
    {
        return OrderResult.InvalidCustomer;
    }

    // Happy path is clear and unindented
    return ExecuteOrder(order);
}
```

### Assertions and Preconditions

```csharp
// C# - Using Debug.Assert and ArgumentException
public decimal CalculateDiscount(Order order, decimal discountPercent)
{
    // Preconditions - validate arguments
    ArgumentNullException.ThrowIfNull(order);

    if (discountPercent < 0 || discountPercent > 100)
    {
        throw new ArgumentOutOfRangeException(
            nameof(discountPercent),
            "Discount must be between 0 and 100");
    }

    // Assertions - validate assumptions (development only)
    Debug.Assert(order.Items.All(i => i.Price >= 0), "All item prices should be non-negative");

    var subtotal = order.Items.Sum(i => i.Price);
    return subtotal * (discountPercent / 100m);
}
```

### Constraints and Invariants

```csharp
// C# - Record with validation
public record Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        if (amount < 0)
        {
            throw new ArgumentException("Amount cannot be negative", nameof(amount));
        }

        if (string.IsNullOrWhiteSpace(currency) || currency.Length != 3)
        {
            throw new ArgumentException("Currency must be a 3-letter code", nameof(currency));
        }

        Amount = amount;
        Currency = currency.ToUpperInvariant();
    }
}

// C# - Generic constraints
public class Repository<TEntity> where TEntity : class, IEntity, new()
{
    public TEntity Create()
    {
        var entity = new TEntity();
        entity.Id = GenerateId();
        return entity;
    }
}
```

### Exception Handling Patterns

```csharp
// C# - Structured exception handling
public async Task<Order> GetOrderAsync(int orderId)
{
    try
    {
        var order = await _repository.FindAsync(orderId);

        if (order == null)
        {
            throw new OrderNotFoundException(orderId);
        }

        return order;
    }
    catch (DbException ex)
    {
        _logger.LogError(ex, "Database error retrieving order {OrderId}", orderId);
        throw new OrderRetrievalException($"Failed to retrieve order {orderId}", ex);
    }
}
```

### Explicit Code Style

```csharp
// Bad - clever bit manipulation
var result = (b << 4 & b << 8) | (b >> 2);

// Good - explicit and documented
var shift4Bits = b << 4;
var shift8Bits = b << 8;
var divideBy4 = b >> 2;
var mergedBits = (shift4Bits & shift8Bits) | divideBy4;
```

```csharp
// Using SIMD for vectorized addition
// See: https://docs.microsoft.com/en-us/dotnet/standard/simd
public static void AddVectors(float[] a, float[] b, float[] result)
{
    int simdLength = Vector<float>.Count;
    int i = 0;

    // Process vectors in SIMD-width chunks
    for (; i <= a.Length - simdLength; i += simdLength)
    {
        var va = new Vector<float>(a, i);
        var vb = new Vector<float>(b, i);
        (va + vb).CopyTo(result, i);
    }

    // Handle remaining elements
    for (; i < a.Length; i++)
    {
        result[i] = a[i] + b[i];
    }
}
```

## Naming

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `OrderProcessor` |
| Interfaces | IPascalCase | `IOrderRepository` |
| Methods | PascalCase | `ProcessOrder` |
| Properties | PascalCase | `CustomerName` |
| Public Fields | PascalCase | `MaxRetryCount` |
| Private Fields | _camelCase | `_orderRepository` |
| Parameters | camelCase | `orderId` |
| Local Variables | camelCase | `customerName` |
| Constants | PascalCase | `DefaultTimeout` |
| Enums | PascalCase | `OrderStatus.Pending` |
| Type Parameters | TPascalCase | `TEntity`, `TResult` |
| Async Methods | PascalCase + Async | `GetOrderAsync` |

```csharp
public class OrderProcessor : IOrderProcessor
{
    private const int DefaultTimeout = 30;
    private readonly IOrderRepository _orderRepository;

    public string CustomerName { get; set; }

    public async Task<Order> GetOrderAsync(int orderId)
    {
        var order = await _orderRepository.FindAsync(orderId);
        return order;
    }
}
```

## File organization

`Order.cs`, `IOrderStore.cs`, and `OrderStatus.cs`.

### Namespace imports

* Please place `using` statements inside the namespace.

## Language constructs

```csharp
// Use records for immutable data
public record OrderSummary(
    int OrderId,
    string CustomerName,
    decimal Total,
    DateTime CreatedAt);

// Use pattern matching
public string GetOrderStatus(Order order) => order switch
{
    { IsCancelled: true } => "Cancelled",
    { IsShipped: true } => "Shipped",
    { IsPaid: true } => "Processing",
    _ => "Pending"
};

// Use nullable reference types
public Customer? FindCustomer(int id)
{
    return _customers.FirstOrDefault(c => c.Id == id);
}

// Use collection expressions (C# 12+)
List<int> numbers = [1, 2, 3, 4, 5];
```

---

## Comments

Use XML documentation for public APIs:

```csharp
/// <summary>
/// Calculates the pro-rated subscription cost for a partial billing period.
/// </summary>
/// <param name="plan">The subscription plan to calculate for.</param>
/// <param name="startDate">The start of the partial period.</param>
/// <param name="endDate">The end of the partial period.</param>
/// <returns>The pro-rated cost in the plan's currency.</returns>
/// <exception cref="ArgumentException">Thrown when endDate precedes startDate.</exception>
public decimal CalculateProratedCost(Plan plan, DateTime startDate, DateTime endDate)
```

## Comment examples

### 3.1 What, Why — Not How

```csharp
// BAD: How (redundant with code)
// Loop through users and check if email contains @
foreach (var user in users)
{
    if (user.Email.Contains("@")) { ... }
}

// GOOD: What and Why
// Filter to valid users only—external imports may lack email validation
foreach (var user in users)
{
    if (user.Email.Contains("@")) { ... }
}
```

### 3.2 Standard Annotations

```csharp
// TODO: Replace with batch API call once available (Q3 2025)
// BUGFIX: Null check added—legacy records may have missing tenant IDs (see issue #1234)
// PERF: Cached here to avoid N+1 query in the parent loop
// SECURITY: Input sanitized to prevent SQL injection
```

### 3.3 Agent Markers

```csharp
// @agent:test — Cover edge case where input is empty collection
// @agent:security — Validate this doesn't expose PII in logs
// @agent:review — Complex logic, needs human verification
// @agent:refactor — Candidate for extraction once patterns stabilize
```

### 3.4 Section Headers

```csharp
// ============================================================================
// CONFIGURATION
// ============================================================================

// ============================================================================
// PUBLIC API
// ============================================================================

// ============================================================================
// PRIVATE HELPERS
// ============================================================================
```

### 6.2 Obvious Code

```csharp
// BAD: States the obvious
// Increment the counter
counter++;

// Set the user's name
user.Name = name;

// Return the result
return result;
```

## Navigation markers

```csharp
/*
 * ----------------------------------------------------------------------------
 * ⚓ COMPONENT: [ComponentName]
 * 📜 PURPOSE: [Concise description of what this file does]
 * 🔗 RELATES: [Reference to related files or specs, e.g., [[AuthSpec]]]
 * ⚡ FLOW: [Inbound Caller] -> [This Component] -> [Outbound Dependency]
 * 🛡️ SECURITY: [Security Role/Constraint, e.g., Requires 'Admin']
 * ----------------------------------------------------------------------------
 */
```

## Folding

When supported by the language and tooling, use region directives to collapse large sections.
In C#, use `#region` and `#endregion` for blocks that are meaningful as a unit
(for example, "Public API", "Private Helpers"). Keep regions shallow; do not nest more than one level.

```csharp
#region Public API
public Task<User> GetUserAsync(...) { ... }
#endregion
```

## Marker examples

### 3. Global Concept Registry

```csharp
// Validates the cart items against the [[InventoryRules]].
public void ValidateCart() { ... }
```

### 4. Section Markers (Long Files)

```csharp
// ============================================================================
// PUBLIC API
// ============================================================================
```

## Testing

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

## Test naming

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

## Test examples

### Test file organization

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

### One Test Per Scenario

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

### Arrange-Act-Assert Pattern

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

### Test Independence and Isolation

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

### Test Factories and Builders

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

### Test Fixtures

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

### Comment the Why, Not the What

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

### SQL and Database Migrations

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

### Configuration Files

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

### Testing Async Code

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

### Prevention Strategies

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

```csharp
// Instead of relying on auto-generated IDs
var orderId = Guid.NewGuid();
var order = OrderFactory.Create(id: orderId);

// Assert using the known ID
var retrieved = await _repository.GetByIdAsync(orderId);
Assert.Equal(orderId, retrieved.Id);
```

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

### Test Execution in Pipelines

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

```csharp
// xUnit runs test classes in parallel by default
// Disable for tests that cannot run in parallel
[Collection("Sequential")]
public class DatabaseMigrationTests
{
    // These tests modify shared database schema
}
```

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

## Authorization service testing

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
```

## Coverage

- Use Coverlet for collecting coverage
- Use ReportGenerator for HTML reports
- Integrate with `dotnet test --collect:"XPlat Code Coverage"`

```bash
# .NET
dotnet test --collect:"XPlat Code Coverage"
reportgenerator -reports:**/coverage.cobertura.xml -targetdir:coverage-report
```

## Logging

Use the configured `ILogger` pipeline and scopes.

## Logging examples

```csharp
using Serilog;
using Serilog.Context;

public class PaymentService
{
    public void ProcessPayment(string tenantId, decimal amount)
    {
        // CONTEXT: Push properties to context
        using (LogContext.PushProperty("CorrelationId", Guid.NewGuid()))
        using (LogContext.PushProperty("TenantId", tenantId))
        {
            Log.Information("Entering ProcessPayment");

            // BRANCHING: Pre-calculation logging
            bool requiresAudit = amount >= 10000;
            Log.Debug("Audit Condition Evaluation: Amount={Amount}, RequiresAudit={RequiresAudit}", amount, requiresAudit);

            try
            {
                if (requiresAudit)
                {
                    Log.Information("Branch: Audit path taken");
                    // ...
                }
            }
            catch (Exception ex)
            {
                Log.Error(ex, "Failed to process payment");
                throw; // Rethrow implies we log and bubble up
            }
            finally
            {
                // FINALLY LOGGING
                Log.Debug("Exiting ProcessPayment (In Finally Block)");
            }
        }
    }
}
```

---

## Performance

See [BACKEND.md](../backend/BACKEND.md#aspnet-core-performance-guidance).

### 3.1 Async/Await

See [BACKEND.md](../backend/BACKEND.md#aspnet-core-performance-guidance).

### 3.2 JSON Serialization

See [BACKEND.md](../backend/BACKEND.md#aspnet-core-performance-guidance).

### 3.3 Memory & Garbage Collection (GC)

See [BACKEND.md](../backend/BACKEND.md#aspnet-core-performance-guidance).

### 3.4 Caching (Server-Side)

See [BACKEND.md](../backend/BACKEND.md#aspnet-core-performance-guidance).

## Performance examples

### 5.1 Payloads

```csharp
options.JsonSerializerOptions.DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull;
```

```csharp
builder.Services.AddResponseCompression(options => {
    options.EnableForHttps = true;
});
```

### 5.2 Latency Reduction

```csharp
var task1 = GetUserAsync(id);
var task2 = GetOrdersAsync(id);
await Task.WhenAll(task1, task2); // Runs concurrently
```

### 7.1 Pattern: Selective Fetching (Partial Objects)

```csharp
// ✅ OPTIMIZED: Fetches only required columns
var userCard = await db.Users
    .Where(u => u.Id == id)
    .Select(u => new UserCardDto {
        FullName = u.FullName,
        AvatarUrl = u.AvatarUrl
    })
    .FirstOrDefaultAsync();
```

## Secret handling

### 3.1 The `ISecretProtectionService`

```csharp
public interface ISecretProtectionService
{
    /// <summary>
    /// Encrypts a plaintext secret using the current active key version.
    /// </summary>
    /// <param name="plaintext">The raw secret.</param>
    /// <returns>The serialized JSON envelope string.</returns>
    Task<string> ProtectAsync(string plaintext);

    /// <summary>
    /// Decrypts a protected secret. Automatically resolves the correct key
    /// based on the version metadata in the envelope.
    /// </summary>
    /// <param name="envelopeJson">The serialized JSON envelope.</param>
    /// <returns>The plaintext secret.</returns>
    Task<string> UnprotectAsync(string envelopeJson);
}
```

## Design patterns

### 1) Abstract Factory

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#1-abstract-factory).

```csharp
public interface IWidgetFactory
{
    IButton CreateButton();
    IInput CreateInput();
}

public sealed class DarkFactory : IWidgetFactory
{
    public IButton CreateButton()
    {
        return new DarkButton();
    }

    public IInput CreateInput()
    {
        return new DarkInput();
    }
}
```

### 2) Builder

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#2-builder).

```csharp
public sealed class ReportBuilder
{
    private readonly Report _report = new();

    public ReportBuilder Title(string value)
    {
        _report.Title = value;
        return this;
    }

    public ReportBuilder AddSection(string section)
    {
        _report.Sections.Add(section);
        return this;
    }

    public Report Build()
    {
        return _report;
    }
}
```

### 3) Factory Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#3-factory-method).

```csharp
public abstract class Exporter
{
    public abstract IWriter CreateWriter();
}

public sealed class CsvExporter : Exporter
{
    public override IWriter CreateWriter()
    {
        return new CsvWriter();
    }
}
```

### 4) Prototype

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#4-prototype).

```csharp
public sealed class Template : ICloneable
{
    public string Name { get; set; } = string.Empty;

    public object Clone()
    {
        return MemberwiseClone();
    }
}
```

### 5) Singleton

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#5-singleton).

```csharp
public sealed class AppClock
{
    private static readonly AppClock InstanceValue = new();

    private AppClock()
    {
    }

    public static AppClock Instance
    {
        get
        {
            return InstanceValue;
        }
    }
}
```

### 6) Adapter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#6-adapter).

```csharp
public sealed class AuthAdapter : IAuthClient
{
    private readonly LegacyAuth _legacy;

    public AuthAdapter(LegacyAuth legacy)
    {
        _legacy = legacy;
    }

    public Task<Token> LoginAsync(Creds creds)
    {
        return _legacy.SignInAsync(creds.User, creds.Pass);
    }
}
```

### 7) Bridge

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#7-bridge).

```csharp
public interface IRenderer
{
    void DrawCircle(int radius);
}

public abstract class Shape
{
    protected Shape(IRenderer renderer)
    {
        Renderer = renderer;
    }

    protected IRenderer Renderer { get; }
}

public sealed class Circle : Shape
{
    public Circle(IRenderer renderer)
        : base(renderer)
    {
    }

    public void Draw()
    {
        Renderer.DrawCircle(10);
    }
}
```

### 8) Composite

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#8-composite).

```csharp
public interface INode
{
    void Render();
}

public sealed class Leaf : INode
{
    public void Render()
    {
    }
}

public sealed class Group : INode
{
    private readonly List<INode> _children = new();

    public void Add(INode child)
    {
        _children.Add(child);
    }

    public void Render()
    {
        foreach (var child in _children)
        {
            child.Render();
        }
    }
}
```

### 9) Decorator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#9-decorator).

```csharp
public interface IWriter
{
    string Write(string value);
}

public sealed class UpperWriter : IWriter
{
    public string Write(string value)
    {
        return value.ToUpperInvariant();
    }
}

public sealed class TrimWriter : IWriter
{
    private readonly IWriter _inner;

    public TrimWriter(IWriter inner)
    {
        _inner = inner;
    }

    public string Write(string value)
    {
        return _inner.Write(value.Trim());
    }
}
```

### 10) Facade

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#10-facade).

```csharp
public sealed class ExportFacade
{
    private readonly Renderer _renderer;
    private readonly Storage _storage;

    public ExportFacade(Renderer renderer, Storage storage)
    {
        _renderer = renderer;
        _storage = storage;
    }

    public Task<string> ExportAsync(Document document)
    {
        var file = _renderer.Render(document);
        return _storage.SaveAsync(file);
    }
}
```

### 11) Flyweight

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#11-flyweight).

```csharp
public sealed class Icon
{
    public Icon(string path)
    {
        Path = path;
    }

    public string Path { get; }
}

public sealed class IconFactory
{
    private readonly Dictionary<string, Icon> _cache = new();

    public Icon Get(string path)
    {
        if (_cache.TryGetValue(path, out var icon))
        {
            return icon;
        }

        var created = new Icon(path);
        _cache[path] = created;
        return created;
    }
}
```

### 12) Proxy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#12-proxy).

```csharp
public sealed class SecuredRepo : IRepo
{
    private readonly IRepo _inner;
    private readonly IAuth _auth;

    public SecuredRepo(IRepo inner, IAuth auth)
    {
        _inner = inner;
        _auth = auth;
    }

    public Task<Item> GetAsync(string id)
    {
        _auth.Ensure("read");
        return _inner.GetAsync(id);
    }
}
```

### 13) Chain of Responsibility

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#13-chain-of-responsibility).

```csharp
public abstract class Handler
{
    protected Handler? Next;

    public Handler SetNext(Handler next)
    {
        Next = next;
        return next;
    }

    public abstract bool Handle(Request request);
}

public sealed class AuthHandler : Handler
{
    public override bool Handle(Request request)
    {
        if (request.User is null)
        {
            return false;
        }

        return Next?.Handle(request) ?? true;
    }
}
```

### 14) Command

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#14-command).

```csharp
public interface ICommand
{
    void Execute();
    void Undo();
}

public sealed class RenameCommand : ICommand
{
    private readonly Item _item;
    private readonly string _next;
    private string _prev = string.Empty;

    public RenameCommand(Item item, string next)
    {
        _item = item;
        _next = next;
    }

    public void Execute()
    {
        _prev = _item.Name;
        _item.Name = _next;
    }

    public void Undo()
    {
        _item.Name = _prev;
    }
}
```

### 15) Interpreter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#15-interpreter).

```csharp
public interface IExpression
{
    bool Evaluate(Context context);
}

public sealed class AndExpression : IExpression
{
    private readonly IExpression _left;
    private readonly IExpression _right;

    public AndExpression(IExpression left, IExpression right)
    {
        _left = left;
        _right = right;
    }

    public bool Evaluate(Context context)
    {
        return _left.Evaluate(context) && _right.Evaluate(context);
    }
}
```

### 16) Iterator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#16-iterator).

```csharp
public sealed class ListIterator<T> : IEnumerator<T>
{
    private readonly List<T> _items;
    private int _index = -1;

    public ListIterator(List<T> items)
    {
        _items = items;
    }

    public T Current => _items[_index];

    object IEnumerator.Current => Current;

    public bool MoveNext()
    {
        _index += 1;
        return (_index < _items.Count);
    }

    public void Reset()
    {
        _index = -1;
    }

    public void Dispose()
    {
    }
}
```

### 17) Mediator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#17-mediator).

```csharp
public interface IMediator
{
    void Notify(object sender, string evt);
}

public sealed class DialogMediator : IMediator
{
    public void Notify(object sender, string evt)
    {
    }
}
```

### 18) Memento

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#18-memento).

```csharp
public sealed record Snapshot(string Name, int Count);

public sealed class Editor
{
    public string Name { get; set; } = string.Empty;
    public int Count { get; set; }

    public Snapshot Save()
    {
        return new Snapshot(Name, Count);
    }

    public void Restore(Snapshot snapshot)
    {
        Name = snapshot.Name;
        Count = snapshot.Count;
    }
}
```

### 19) Observer

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#19-observer).

```csharp
public sealed class Subject
{
    private readonly List<Action> _subscribers = new();

    public void Subscribe(Action action)
    {
        _subscribers.Add(action);
    }

    public void Notify()
    {
        foreach (var subscriber in _subscribers)
        {
            subscriber();
        }
    }
}
```

### 20) State

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#20-state).

```csharp
public interface IState
{
    void Handle(Context context);
}

public sealed class ReadyState : IState
{
    public void Handle(Context context)
    {
        context.State = new BusyState();
    }
}

public sealed class BusyState : IState
{
    public void Handle(Context context)
    {
    }
}

public sealed class Context
{
    public IState State { get; set; } = new ReadyState();

    public void Request()
    {
        State.Handle(this);
    }
}
```

### 21) Strategy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#21-strategy).

```csharp
public interface IPriceStrategy
{
    decimal Calc(decimal basePrice);
}

public sealed class VipPrice : IPriceStrategy
{
    public decimal Calc(decimal basePrice)
    {
        return basePrice * 0.9m;
    }
}
```

### 22) Template Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#22-template-method).

```csharp
public abstract class Importer
{
    public void Run()
    {
        Read();
        Validate();
        Save();
    }

    protected abstract void Read();

    protected virtual void Validate()
    {
    }

    protected abstract void Save();
}
```

### 23) Visitor

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#23-visitor).

```csharp
public interface IVisitor
{
    void Visit(NodeA node);
    void Visit(NodeB node);
}

public interface INode
{
    void Accept(IVisitor visitor);
}

public sealed class NodeA : INode
{
    public void Accept(IVisitor visitor)
    {
        visitor.Visit(this);
    }
}
```


## Security

Apply [general security](../SECURITY_GUIDELINES.md) and [secret handling](../SECRET_HANDLING.md).
Use the configured authentication framework. Require authorization by default and explicit review for anonymous endpoints.
Enforce HTTPS and production HSTS through the configured application or trusted proxy boundary.
Use dedicated request models to prevent mass assignment. Validate ownership separately from role checks.
Do not deserialize untrusted data with `BinaryFormatter` or enable arbitrary polymorphic types.
For Newtonsoft.Json, retain `TypeNameHandling.None` unless a reviewed trusted contract requires otherwise.
See [OWASP .NET security](https://cheatsheetseries.owasp.org/cheatsheets/DotNet_Security_Cheat_Sheet.html).

### SQL and EF Core

Use parameter binding through LINQ, typed database parameters, or the configured safe SQL API.
For `FromSqlRaw`, pass values separately. Do not interpolate input into the SQL string.
Project only authorized response fields. Returning a full entity can reveal internal or sensitive fields.

```csharp
// SECURITY: Parameter binding protects the value. Tenant authorization is a separate prerequisite.
var orders = context.Orders.FromSqlRaw(
    "SELECT * FROM orders WHERE tenant_id = {0} AND id = {1}",
    authorizedTenantId,
    orderId);
```

This fragment returns entities for internal processing. Map them to an authorized response model before returning data.
See [EF Core SQL queries](https://learn.microsoft.com/en-us/ef/core/querying/sql-queries).

### Sensitive memory

Do not introduce `SecureString` as the default for new .NET development. Microsoft recommends against that use.
If a legacy API requires it, document platform behavior, dispose it promptly, and clear any unmanaged plaintext conversion.
Wrapping an existing immutable string does not erase the original string.
Protection differs by operating system. Do not assume encryption on non-Windows platforms.
See [Microsoft SecureString guidance](https://learn.microsoft.com/en-us/dotnet/fundamentals/runtime-libraries/system-security-securestring).

For owned byte buffers, use `CryptographicOperations.ZeroMemory` in cleanup paths.
Avoid extra string conversions and clear pooled buffers before returning them.

```csharp
// SECURITY: Clear this owned buffer even when the operation fails.
try
{
    UseSecret(secretBytes);
}
finally
{
    CryptographicOperations.ZeroMemory(secretBytes);
}
```

`UseSecret` represents application code that must not retain a copy.
Clearing this buffer does not clear prior copies or lock pages against swapping.
See [ZeroMemory](https://learn.microsoft.com/dotnet/api/system.security.cryptography.cryptographicoperations.zeromemory).
