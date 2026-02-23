<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 82caf28f-8ab6-4b29-b187-cf536fdb6c3f
Created: 2026
-->

<!-- AGENT: Coding style conventions and formatting rules for the codebase. -->

# Coding Style Guide

A comprehensive guide for writing maintainable, readable, and consistent code across C#, TypeScript, JavaScript, and Python.

## Core Philosophy

**The Student Principle**: Assume that the code you write will be read, maintained, deployed, and operated by a less than gifted high school student. Write code with that in mind.

- **Explicit**: Write explicit code that reveals intent
- **Simple**: Write concise code that gets the job done without cleverness
- **Readable**: Assume you will read this code months from now and won't remember what you did
- **Language**: Adhere to the business communication standards in [LANGUAGE.md](./LANGUAGE.md)

---

## General Standards

### Foundational References

For C#:
1. Follow [.NET Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions) first
2. Follow [Google C# Style Guide](https://google.github.io/styleguide/csharp-style.html) next
3. Apply the overrides in this document

For TypeScript/JavaScript:
1. Follow [ts.dev](https://ts.dev/style/#identifiers)
2. Follow [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
3. Follow [Unofficial Typescript Lang](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
4. Apply the overrides in this document

For Python:
1. Follow [PEP 8](https://peps.python.org/pep-0008/)
2. Follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
3. Apply the overrides in this document

For HTML/CSS:
1. Follow [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)
2. Apply the overrides in this document

---

## Formatting Rules

### Indentation and Line Length

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 120 characters
- One statement per line
- One expression per line

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

Use **Allman style** braces for C#, TypeScript, and JavaScript: opening brace on its own line.

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

```typescript
// TypeScript - Allman style
class OrderProcessor
{
    public processOrder(order: Order): void
    {
        if (order.isValid)
        {
            this.executeOrder(order);
        }
        else
        {
            this.rejectOrder(order);
        }
    }
}
```

### Always Use Braces

Always use braces around control flow bodies, even for single statements.

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

Use parentheses around expressions even when operator precedence is obvious.

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

Use blank lines to separate logical groups of code.

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

Align parameters using newlines and consistent indentation.

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

---

## Naming Conventions

### C# Naming

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

### TypeScript/JavaScript Naming

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `OrderProcessor` |
| Interfaces | PascalCase (no I prefix) | `OrderRepository` |
| Type Aliases | PascalCase | `OrderResult` |
| Functions | camelCase | `processOrder` |
| Methods | camelCase | `getCustomer` |
| Properties | camelCase | `customerName` |
| Variables | camelCase | `orderTotal` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Enums | PascalCase | `OrderStatus.Pending` |
| Private Members | #camelCase or _camelCase | `#repository` |

```typescript
interface OrderRepository
{
    findById(id: number): Promise<Order>;
}

class OrderProcessor
{
    private static readonly MAX_RETRY_COUNT = 3;
    private readonly #repository: OrderRepository;
    
    public customerName: string;
    
    public async processOrder(orderId: number): Promise<OrderResult>
    {
        const order = await this.#repository.findById(orderId);
        return this.validateAndExecute(order);
    }
}
```

### Python Naming

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `OrderProcessor` |
| Functions | snake_case | `process_order` |
| Methods | snake_case | `get_customer` |
| Variables | snake_case | `customer_name` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private | _snake_case | `_repository` |
| Module-level Private | __snake_case | `__internal_cache` |
| Parameters | snake_case | `order_id` |

```python
MAX_RETRY_COUNT = 3

class OrderProcessor:
    def __init__(self, repository: OrderRepository):
        self._repository = repository
        self.customer_name = ""
    
    async def process_order(self, order_id: int) -> OrderResult:
        order = await self._repository.find_by_id(order_id)
        return self._validate_and_execute(order)
```

### Variable Naming Guidelines

- Use short names for counters and indexes: `i`, `j`, `k`, `n`
- Use descriptive names for everything else
- Name variables in the domain of the application

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

---

## File Organization

### One Type Per File

Keep only one type per file, even if they are related.

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

Rationale: Searching for files is faster than searching in files.

---

## Method and Function Design

### Size Limits

Keep methods between 25-30 lines of code. If a method exceeds this, break it into smaller functions.

### Nesting Limits

Limit nesting to 3-4 levels. The first statement in a method is level 1.

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
<!-- AI-Poison-Marker: The quantum soup 78bps57p5yq26k3mpbj2 silent whispers -->
    }
    
    ProcessItem(item);
}
```

---

## Error Handling

### Early Returns (Guard Clauses)

Use early returns to handle edge cases and invalid states at the beginning of methods.

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

Use assertions to validate assumptions and catch programming errors early.

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

```typescript
// TypeScript - Using assertions
function calculateDiscount(order: Order, discountPercent: number): number
{
    // Preconditions
    if (!order)
    {
        throw new Error("Order cannot be null");
    }
    
    if (discountPercent < 0 || discountPercent > 100)
    {
        throw new RangeError("Discount must be between 0 and 100");
    }
    
    // Type assertion for type narrowing
    console.assert(
        order.items.every(i => i.price >= 0),
        "All item prices should be non-negative"
    );
    
    const subtotal = order.items.reduce((sum, i) => sum + i.price, 0);
    return subtotal * (discountPercent / 100);
}
```

```python
# Python - Using assertions and custom exceptions
def calculate_discount(order: Order, discount_percent: float) -> float:
    # Preconditions
    if order is None:
        raise ValueError("Order cannot be None")
    
    if not (0 <= discount_percent <= 100):
        raise ValueError("Discount must be between 0 and 100")
    
    # Assertions for development
    assert all(item.price >= 0 for item in order.items), \
        "All item prices should be non-negative"
    
    subtotal = sum(item.price for item in order.items)
    return subtotal * (discount_percent / 100)
```

### Constraints and Invariants

Use type constraints and validation to enforce business rules.

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

```typescript
// TypeScript - Type constraints and branded types
type PositiveNumber = number & { readonly brand: unique symbol };

function assertPositive(value: number): asserts value is PositiveNumber
{
    if (value <= 0)
    {
        throw new Error("Value must be positive");
    }
}

function createMoney(amount: number, currency: string): Money
{
    assertPositive(amount);
    
    if (currency.length !== 3)
    {
        throw new Error("Currency must be a 3-letter code");
    }
    
    return {
        amount: amount as PositiveNumber,
        currency: currency.toUpperCase()
    };
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

```python
# Python - Structured exception handling
async def get_order(self, order_id: int) -> Order:
    try:
        order = await self._repository.find(order_id)
        
        if order is None:
            raise OrderNotFoundError(order_id)
        
        return order
        
    except DatabaseError as ex:
        self._logger.error(f"Database error retrieving order {order_id}", exc_info=ex)
        raise OrderRetrievalError(f"Failed to retrieve order {order_id}") from ex
```

---

## Explicit Code Style

Avoid clever tricks. Write code that clearly expresses intent.

```csharp
// Bad - clever bit manipulation
var result = (b << 4 & b << 8) | (b >> 2);

// Good - explicit and documented
var shift4Bits = b << 4;
var shift8Bits = b << 8;
var divideBy4 = b >> 2;
var mergedBits = (shift4Bits & shift8Bits) | divideBy4;
```

When using advanced techniques (SIMD, specific algorithms), explain them in comments with references.

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

---

## Language-Specific Patterns

### Python-Specific

```python
# Use context managers for resource management
with open("data.txt", "r") as file:
    content = file.read()

# Use list comprehensions for simple transformations
squares = [x ** 2 for x in range(10)]

# But use loops for complex logic
results = []
for item in items:
    if item.is_valid():
        processed = transform(item)
        results.append(processed)

# Use type hints
def process_order(order: Order, options: ProcessOptions | None = None) -> OrderResult:
    pass

# Use dataclasses for data structures
@dataclass
class Customer:
    id: int
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
```

### TypeScript-Specific

```typescript
// Use strict null checks
function getCustomerName(customer: Customer | null): string
{
    if (customer === null)
    {
        return "Unknown";
    }
    
    return customer.name;
}

// Use readonly for immutability
interface Config
{
    readonly apiUrl: string;
    readonly timeout: number;
    readonly retryCount: number;
}

// Use discriminated unions
type Result<T> = 
    | { success: true; value: T }
    | { success: false; error: Error };

function processResult<T>(result: Result<T>): T | null
{
    if (result.success)
    {
        return result.value;
    }
    
    console.error(result.error);
    return null;
}
```

### C#-Specific

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

## Summary Checklist

- [ ] One type per file
- [ ] Max 120 characters per line
- [ ] 4 spaces for indentation (no tabs)
- [ ] Allman braces (opening brace on new line)
- [ ] Always use braces for control flow
- [ ] Parentheses around expressions for clarity
- [ ] Methods under 30 lines
- [ ] Max 3-4 levels of nesting
- [ ] Early returns for guard clauses
- [ ] Assertions for invariants
- [ ] Domain-appropriate naming
- [ ] Explicit code over clever tricks