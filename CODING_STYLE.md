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

A guide for maintainable code in C#, Swift, Go, Rust, Java, TypeScript, JavaScript, Python, HTML, CSS, and SCSS.

## Core Philosophy

**The Student Principle**: Assume that the code you write will be read, maintained, deployed, and operated 
by a less than gifted high school student. Write code with that in mind.

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

For HTML/CSS/SCSS:
1. Follow [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)
2. Apply the overrides in this document

---

## Formatting Rules

### Indentation and Line Length

Language-specific rules below take precedence over the general formatting defaults.
Use the repository's configured formatter and supported toolchain version.
Do not reformat unrelated code as part of a behavior change.

| Language | Formatting and braces |
| --- | --- |
| C#, TypeScript, JavaScript | Keep the Allman style below unless the project declares a different style. |
| Swift | Use the project's Swift formatter configuration. Keep opening braces on the declaration or control-flow line. |
| Go | Use `gofmt`, including its tabs and same-line opening braces. Do not impose the general space or line-length rules. |
| Rust | Use `cargo fmt` and the project's `rustfmt` configuration, including same-line opening braces. |
| Java | Use the project's formatter and existing brace style. For new projects, use same-line opening braces. |

The following indentation and line-length defaults apply where the table does not specify otherwise:

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

```typescript
// Bad
if (isValid)
    process();

// Good
if (isValid)
{
    process();
}
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

```typescript
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

```typescript
// Bad
const container = getContainer();
containerCount += 1;
processNext();
validateState();

// Good
const container = getContainer();

containerCount += 1;

processNext();
validateState();
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

```typescript
// Short parameter list — single line
function save(name: string, id: number): void

// Long parameter list — align on new lines
function showErrorDialog(
    containerId: string,
    title: string,
    message: string,
    suggestion: string | undefined,
    technicalDetail: string | undefined): void
{
    // ...
}
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

### TypeScript / JavaScript

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `ErrorDialog` |
| Interfaces | PascalCase (no I prefix) | `ErrorDialogOptions` |
| Type Aliases | PascalCase | `DialogAction` |
| Functions | camelCase | `showErrorDialog` |
| Methods | camelCase | `renderContent` |
| Properties | camelCase | `errorCode` |
| Variables | camelCase | `containerElement` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Enums | PascalCase | `DialogType.Error` |
| Private Members | #camelCase or _camelCase | `#container` |

```typescript
interface ErrorDialogOptions
{
    readonly title: string;
    readonly message: string;
    readonly suggestion?: string;
}

class ErrorDialog
{
    private static readonly MAX_VISIBLE_ACTIONS = 3;
    private readonly #container: HTMLElement;

    public errorCode: string;

    public async showDialog(options: ErrorDialogOptions): Promise<void>
    {
        const dialog = this.#container.querySelector(".errordialog");
        // ...
    }
}
```

### SCSS / CSS

| Element | Convention | Example |
|---------|------------|---------|
| Class names | lowercase-hyphenated | `.metric-card`, `.toolbar-actions` |
| Component prefix | component name | `.errordialog-header`, `.combobox-item` |
| SCSS variables | $lowercase-hyphenated | `$primary`, `$font-size-sm` |
| SCSS mixins | lowercase-hyphenated | `@mixin responsive-grid` |
| SCSS placeholders | %lowercase-hyphenated | `%visually-hidden` |
| BEM (if used) | block__element--modifier | `.card__header--compact` |

```scss
// Component-scoped class names
.errordialog-header {
    background-color: $gray-900;
    color: white;
    padding: $spacer;
}

.errordialog-body {
    padding: $spacer;
    font-size: $font-size-base;
}

.errordialog-suggestion {
    color: $gray-600;
    font-style: italic;
}
```

### HTML Naming

| Element | Convention | Example |
|---------|------------|---------|
| IDs | lowercase-hyphenated | `id="error-dialog-container"` |
| Classes | lowercase-hyphenated | `class="metric-card"` |
| Data attributes | lowercase-hyphenated | `data-dialog-type="error"` |
| Custom elements | lowercase-hyphenated | `<error-dialog>` |

---

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

### Swift, Go, Rust, and Java Naming

| Language | Types | Functions, methods, and values | Packages or modules |
| --- | --- | --- | --- |
| Swift | `Order`, `OrderStore` for types and protocols | `loadOrder`, `orderID` | Follow the package and target names. |
| Go | `Order` when exported, `order` when unexported | `LoadOrder` when exported, `loadOrder` when unexported | Short lowercase package names, such as `orders`. |
| Rust | `Order`, `OrderStore` for types and traits | `load_order`, `order_id`. Constants use `MAX_RETRIES`. | `snake_case`, such as `order_store`. |
| Java | `Order`, `OrderStore` for classes and interfaces | `loadOrder`, `orderId`. Constants use `MAX_RETRIES`. | Lowercase package names. |

Use meaningful argument labels in Swift. Do not copy C# interface prefixes or async naming into other languages.
Use [Swift API conventions](https://www.swift.org/documentation/api-design-guidelines/), [Go conventions](https://go.dev/doc/effective_go), and the [Rust style guide](https://doc.rust-lang.org/style-guide/).

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

## SCSS-Specific Rules

### Variable Overrides

Always override Bootstrap variables in `_variables.scss`, not in component files.

```scss
// Good — in _variables.scss
$border-radius: 0 !default;

// Bad — in a component file
.my-component {
    border-radius: 0; // Fights Bootstrap's default
}
```

### Nesting Depth

Limit SCSS nesting to 3 levels. Deep nesting produces overly specific selectors.

```scss
// Bad — too deep
.sidebar {
    .nav {
        .nav-item {
            .nav-link {
                &:hover {
                    // 5 levels deep
                }
            }
        }
    }
}

// Good — flattened
.sidebar .nav-link {
    // styles

    &:hover {
        // styles
    }
}
```

### Avoid `!important`

Never use `!important` in component SCSS. If a style is not applying, the selector specificity is wrong — 
fix the selector, not the declaration.

The only exception is utility classes in the theme itself (e.g., `.p-compact`), where `!important` follows 
Bootstrap's utility convention.

---

## File Organization

### One Type Per File

Keep one type per file in C# and TypeScript/JavaScript.
Keep one primary type per file in Swift and Java.
Keep Swift extensions and nested helper types together when they form one cohesive unit.
For Java, match the source filename to its public top-level type.
For Go and Rust, group related declarations by package or module responsibility rather than creating a file for every type.
The C# example below illustrates the one-type rule.

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

Keep functions or methods between 25-30 lines of code. If a function or method exceeds this, break it 
into smaller functions or methods.

### Nesting Limits

Limit nesting to 3-4 levels. The first statement in a method is level 1. Use early returns to flatten logic.

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

```typescript
// Bad — too deeply nested
function processItems(items: Item[]): void
{
    for (const item of items)
    {
        if (item.isValid)
        {
            if (item.hasContent)
            {
                if (item.isVisible)
                {
                    renderItem(item);
                }
            }
        }
    }
}

// Good — early returns
function processItems(items: Item[]): void
{
    for (const item of items)
    {
        processItem(item);
    }
}

function processItem(item: Item): void
{
    if (!item.isValid || !item.hasContent || !item.isVisible)
    {
        return;
    }

    renderItem(item);
}
```

---

## Error Handling

### Early Returns (Guard Clauses)

Use early returns to handle edge cases and invalid states at the beginning of functions or methods.

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

```typescript
function showDialog(containerId: string, options: ErrorDialogOptions): void
{
    if (!containerId)
    {
        console.error("[ErrorDialog] No container ID provided");
        return;
    }

    const container = document.getElementById(containerId);
    if (!container)
    {
        console.error("[ErrorDialog] Container not found:", containerId);
        return;
    }

    if (!options.title && !options.message)
    {
        console.warn("[ErrorDialog] No title or message provided");
        return;
    }

    // Happy path — render the dialog
    renderDialog(container, options);
}
```

### Assertions and Preconditions

Use assertions to validate assumptions and catch programming errors early in development.

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

function calculateDiscount(price: number, percent: number): number
{
    if (percent < 0 || percent > 100)
    {
        throw new RangeError("Discount percent must be between 0 and 100");
    }

    console.assert(
        price >= 0,
        "Price should be non-negative"
    );

    return price * (percent / 100);
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

```typescript
// Bad — clever but obscure
const result = (b << 4 & b << 8) | (b >> 2);

// Good — explicit and clear
const shift4Bits = b << 4;
const shift8Bits = b << 8;
const divideBy4 = b >> 2;
const mergedBits = (shift4Bits & shift8Bits) | divideBy4;
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

Use the project's strict type checks and validate external data at runtime boundaries.
Declare public browser globals in the project's type declarations rather than using `window as any` or chained assertions.
For a closed set of property names, use a union or `keyof` instead of broadening the whole object to an untyped record.
Preserve the published global API when changing declarations, aliases, or bundle structure.

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

### Swift-Specific

- Prefer `let` when a value does not change. Use value types when they match the model's semantics.
- Handle optionals explicitly. Avoid force unwraps and `try!` in paths that can fail at runtime.
- Use structured concurrency, propagate cancellation, and respect actor isolation when sharing mutable state.
- Keep UI updates on the main actor. Release observers, timers, and other owned resources at the correct lifecycle boundary.
- Use protocols or injected functions where they provide a useful contract. Do not add protocols solely to mirror classes.

### Go-Specific

- Return and check `error` values. Add useful context without losing the wrapped error.
- Pass `context.Context` to operations that support cancellation or deadlines. Do not use panic for expected failures.
- Give each goroutine a defined lifetime and shutdown path. Synchronize shared mutable state.
- Define small interfaces where consumers need them. Avoid copying inheritance-based designs into Go.
- Close owned resources and preserve meaningful errors from final writes, flushes, and closes.

### Rust-Specific

- Use ownership and borrowing to express resource lifetimes. Do not clone values solely to avoid understanding a borrow error.
- Use `Result` for recoverable failures and `Option` for an expected absence. Avoid `unwrap` and `expect` on fallible external input.
- Keep `unsafe` blocks narrow and document their safety invariants.
- Choose shared ownership and an async runtime only when the requirements justify them.
- Propagate cancellation and release resources when tasks finish or stop.

### Java-Specific

- Use the JDK and Maven or Gradle toolchain configured by the repository.
- Use try-with-resources for owned `AutoCloseable` resources. Preserve interruption when handling `InterruptedException`.
- State nullability and mutability expectations in API contracts. Use the project's established error model.
- Keep business logic separate from HTTP handlers and framework extension entry points.
- Match host-provided APIs and dependency versions when building plugins or providers.

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

- [ ] File organization follows the language-specific rules
- [ ] Line length and indentation follow the language-specific formatter or defaults
- [ ] Brace style follows the language-specific rules
- [ ] Always use braces for control flow
- [ ] Parentheses around expressions for clarity
- [ ] Functions and methods under 30 lines
- [ ] Max 3-4 levels of nesting
- [ ] Early returns for guard clauses
- [ ] Assertions for invariants
- [ ] SCSS nesting max 3 levels
- [ ] No `!important` in component SCSS
- [ ] Component CSS classes prefixed with component name
- [ ] Domain-appropriate naming
- [ ] Explicit code over clever tricks
