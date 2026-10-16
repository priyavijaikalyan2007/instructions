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

For Swift:
1. Follow [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/) for names and contracts.
2. Apply the formatting and file rules in this document.

For Go:
1. Follow [Effective Go](https://go.dev/doc/effective_go) for API names, errors, and language semantics.
2. Apply the formatting and file rules in this document, including the required Go brace exceptions.

For Rust:
1. Follow [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) for public contracts and names.
2. Apply the formatting and file rules in this document instead of the default formatter style.

For Java:
1. Follow the project's JDK, framework, and public API contracts.
2. Apply the naming, formatting, and file rules in this document.

For HTML/CSS/SCSS:
1. Follow [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)
2. Apply the overrides in this document

---

## Formatting Rules

### Indentation and Line Length

Use the same house style across languages. Language conventions govern names and semantics, not a different preferred visual style.

- Use four spaces for indentation. Do not use tabs.
- Keep source lines at or below 120 characters.
- Use Allman braces, with each opening brace on its own line wherever the grammar permits it.
- Keep one type per file, including a five-line struct.
- Keep one statement and one expression per line.
- Configure formatters to preserve this policy. Do not accept unrelated formatter changes during a behavior change.

Python uses indentation instead of braces. Do not add braces to Python control-flow blocks.
Go's semicolon insertion requires same-line braces for function bodies, control flow, and composite literals.
This is a syntax limit, not a preference for another style. Keep four-space indentation and the other house rules in Go.
Do not run default `gofmt` or `rustfmt` as an automatic rewrite when their output would violate the house style.
Use syntax, compile, and lint checks separately from formatting checks when the configured formatter cannot express this style.
See the [Go semicolon rules](https://go.dev/ref/spec#Semicolons) for the required Go exception.

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

Prefer **Allman style** braces in every brace-based language. Put the opening brace on its own line.
The Go syntax limit above is the only Go brace exception. Python block syntax remains indentation-based.

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

Always use braces around control-flow bodies where the language uses braces, even for a single statement.
Python uses an indented block. Do not replace a multi-step block with a terse conditional expression.

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

Use the same naming decisions for each concept, then apply the language's spelling and visibility rules below.
Do not rename a wire field, database column, or public API merely to match an internal variable convention.

| Element | Shared rule |
| --- | --- |
| Types | Name the domain concept or responsibility. Avoid redundant words such as `DataObject`. |
| Interfaces, protocols, traits | Name the contract. Use the language's prefix and suffix conventions. |
| Functions and methods | Name the action or returned value. Make side effects clear. |
| Fields and properties | Name the stored meaning. Include units when a number could be ambiguous. |
| Booleans | State the condition, such as `isEnabled`, `is_enabled`, or `IsEnabled`. |
| Constants | Name the fixed meaning rather than its current literal value. |
| Parameters and locals | Use domain names. Reserve short counters for short, obvious loops. |
| Type parameters | Describe the role when a generic letter would hide the contract. |
| Files | Match the type or responsibility, using the language's filename convention. |

C# and TypeScript retain their detailed tables below. The other tables use the same categories and state their differences explicitly.

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
    readonly #container: HTMLElement;

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
.errordialog-header
{
    background-color: $gray-900;
    color: white;
    padding: $spacer;
}

.errordialog-body
{
    padding: $spacer;
    font-size: $font-size-base;
}

.errordialog-suggestion
{
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
| --- | --- | --- |
| Classes and dataclasses | PascalCase | `OrderSummary` |
| Protocols and abstract classes | PascalCase, no `I` prefix | `OrderStore` |
| Functions and methods | snake_case | `load_order` |
| Public instance attributes | snake_case | `order_id` |
| Nonpublic attributes | Leading underscore | `_customer_name` |
| Name-mangled class attributes | Double underscore only when subclass collision requires it | `__cache` |
| Properties | snake_case | `display_name` |
| Module and class constants | SCREAMING_SNAKE_CASE | `DEFAULT_QUANTITY` |
| Parameters and local variables | snake_case | `order_id`, `item_count` |
| Booleans | snake_case condition | `is_enabled` |
| Enums and members | PascalCase type, uppercase members | `OrderStatus.PENDING` |
| Generic type parameters | Descriptive PascalCase | `TOrder` |
| Async functions | snake_case, with the same naming rule as synchronous functions | `load_order` |
| Modules and files | snake_case | `order_summary.py` |

An underscore communicates nonpublic intent. It does not enforce access control.
Reserve double-leading-and-trailing names for Python's defined special methods, such as `__init__`.
Use type annotations for public contracts and retain the project's supported Python version.

```python
# File: order_summary.py
DEFAULT_QUANTITY = 1

class OrderSummary:
    """Describes an order with nonpublic fields and read-only public properties."""

    def __init__(self, order_id: str, customer_name: str, quantity: int = DEFAULT_QUANTITY) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        self._order_id = order_id
        self._customer_name = customer_name
        self._quantity = quantity

    @property
    def order_id(self) -> str:
        """Returns the stable order identifier."""
        return self._order_id

    @property
    def quantity(self) -> int:
        """Returns the number of ordered items."""
        return self._quantity

    def display_label(self) -> str:
        """Returns the label shown to the user."""
        return f"{self._customer_name}: {self._quantity}"
```

### Swift Naming

| Element | Convention | Example |
| --- | --- | --- |
| Classes, structs, actors | PascalCase | `OrderSummary`, `OrderStore` |
| Protocols | PascalCase, no `I` prefix | `OrderRepository` |
| Functions and methods | camelCase, meaningful argument labels | `loadOrder(id:)` |
| Stored and computed properties | camelCase | `orderID`, `displayLabel` |
| Private fields | camelCase with an access modifier, no required underscore | `private let customerName` |
| Public members | camelCase with explicit public access when exported | `public var isEnabled` |
| Static and instance constants | camelCase with `let` | `defaultQuantity` |
| Parameters and local variables | camelCase | `orderID`, `itemCount` |
| Booleans | camelCase condition | `isEnabled`, `hasChanges` |
| Enum types and cases | PascalCase type, camelCase cases | `OrderStatus.pending` |
| Generic type parameters | Descriptive PascalCase | `Element`, `OrderType` |
| Async methods | camelCase with `async` in the signature | `loadOrder(id:) async throws` |
| Extensions | Use the extended type's name | `extension OrderSummary` |
| Source files | PascalCase matching the type | `OrderSummary.swift` |

Prefer `let` when a value does not change. Use access modifiers to express visibility rather than encoding visibility in the name.
Use [Swift API conventions](https://www.swift.org/documentation/api-design-guidelines/) for argument labels and API meanings.

```swift
// File: OrderSummary.swift
struct OrderSummary
{
    /// Validation errors owned by this value type.
    enum ValidationError: Error
    {
        case invalidQuantity
    }

    static let defaultQuantity = 1
    let orderID: String
    let quantity: Int
    private let customerName: String

    init(orderID: String, customerName: String, quantity: Int = defaultQuantity) throws
    {
        guard quantity > 0 else
        {
            throw ValidationError.invalidQuantity
        }
        self.orderID = orderID
        self.customerName = customerName
        self.quantity = quantity
    }

    func displayLabel() -> String
    {
        return "\(customerName): \(quantity)"
    }
}
```

The nested validation error describes this type's own constructor contract. Move it to a separate file if other types need it independently.

### Go Naming

| Element | Convention | Example |
| --- | --- | --- |
| Exported structs and named types | PascalCase | `OrderSummary` |
| Unexported structs and named types | camelCase | `orderCache` |
| Interfaces | PascalCase when exported, narrow contract name | `OrderStore`, `Reader` |
| Exported functions and methods | PascalCase | `NewOrderSummary`, `DisplayLabel` |
| Unexported functions and methods | camelCase | `validateQuantity` |
| Exported fields | PascalCase | `OrderID` |
| Unexported fields | camelCase | `customerName` |
| Constants | Visibility follows capitalization, no required uppercase underscore style | `DefaultQuantity` |
| Parameters and locals | camelCase | `orderID`, `itemCount` |
| Booleans | Condition name with appropriate visibility | `isEnabled`, `IsEnabled` |
| Enum-like values | Named type and descriptive constants | `OrderStatus`, `OrderPending` |
| Generic type parameters | Short or descriptive exported-style names | `T`, `Element` |
| Packages | Short lowercase name | `orders` |
| Source files | snake_case matching the type | `order_summary.go` |

Capitalization controls export. Go has no `private`, `readonly`, or class inheritance modifier.
Keep invariant-bearing fields unexported and expose methods when callers must not mutate them directly.
The example uses four spaces and only the same-line braces required by Go syntax.

```go
// File: order_summary.go
package orders

import (
    "errors"
    "fmt"
)

const DefaultQuantity = 1

// OrderSummary describes an order and keeps quantity changes internal.
type OrderSummary struct
{
    OrderID string
    customerName string
    quantity int
}

// NewOrderSummary rejects nonpositive quantities.
func NewOrderSummary(orderID string, customerName string, quantity int) (*OrderSummary, error) {
    if quantity <= 0 {
        return nil, errors.New("quantity must be positive")
    }
    return &OrderSummary{
        OrderID: orderID,
        customerName: customerName,
        quantity: quantity,
    }, nil
}

// DisplayLabel returns the label shown to the user.
func (order *OrderSummary) DisplayLabel() string {
    return fmt.Sprintf("%s: %d", order.customerName, order.quantity)
}
```

### Rust Naming

| Element | Convention | Example |
| --- | --- | --- |
| Structs and enums | PascalCase | `OrderSummary`, `OrderStatus` |
| Traits | PascalCase, no `I` prefix | `OrderStore` |
| Functions and methods | snake_case | `new`, `display_label` |
| Public fields | snake_case with `pub` when deliberately exported | `pub order_id` |
| Private fields | snake_case, private by default | `customer_name` |
| Associated and module constants | SCREAMING_SNAKE_CASE | `DEFAULT_QUANTITY` |
| Static values | SCREAMING_SNAKE_CASE | `ORDER_COUNTER` |
| Parameters and locals | snake_case | `order_id`, `item_count` |
| Booleans | snake_case condition | `is_enabled` |
| Enum variants | PascalCase | `OrderStatus::Pending` |
| Generic type parameters | Descriptive PascalCase or established short name | `Element`, `T` |
| Lifetimes | Short lowercase semantic name | `'input`, `'a` |
| Async methods | snake_case with `async` in the signature | `async fn load_order` |
| Modules and files | snake_case | `order_summary.rs` |

Use `pub`, `pub(crate)`, and module privacy deliberately. A field name does not grant access.
Use ownership and `Result` to express contracts. Allman braces remain the house style rather than the default formatter output.

```rust
// File: order_summary.rs
/// Describes an order with a validated positive quantity.
pub struct OrderSummary
{
    pub order_id: String,
    customer_name: String,
    quantity: u32,
}

impl OrderSummary
{
    pub const DEFAULT_QUANTITY: u32 = 1;

    /// Returns an error when quantity is zero.
    pub fn new(order_id: String, customer_name: String, quantity: u32) -> Result<Self, &'static str>
    {
        if quantity == 0
        {
            return Err("quantity must be positive");
        }
        Ok(Self
        {
            order_id,
            customer_name,
            quantity,
        })
    }

    pub fn display_label(&self) -> String
    {
        format!("{}: {}", self.customer_name, self.quantity)
    }
}
```

### Java Naming

| Element | Convention | Example |
| --- | --- | --- |
| Classes and records | PascalCase | `OrderSummary` |
| Interfaces | PascalCase, no `I` prefix | `OrderStore` |
| Methods | camelCase | `displayLabel`, `getOrderId` |
| Public fields | camelCase, expose only when the API requires direct fields | `orderId` |
| Private fields | camelCase with `private`, no required underscore | `customerName` |
| Properties | camelCase accessors where the framework uses bean conventions | `getQuantity`, `setQuantity` |
| Constants | SCREAMING_SNAKE_CASE with `static final` | `DEFAULT_QUANTITY` |
| Parameters and locals | camelCase | `orderId`, `itemCount` |
| Booleans | camelCase condition | `isEnabled`, `hasChanges` |
| Enum types and members | PascalCase type, uppercase members | `OrderStatus.PENDING` |
| Generic type parameters | Established short name or descriptive role | `T`, `TOrder` |
| Async methods | camelCase, return the declared future/completion contract | `loadOrder` |
| Packages | Lowercase qualified name | `com.example.orders` |
| Source files | Public top-level type name | `OrderSummary.java` |

Use access modifiers for visibility and `final` for references or values that must not be reassigned.
Do not add C# interface prefixes or async suffixes merely to make languages look identical.

```java
// File: OrderSummary.java
public final class OrderSummary
{
    public static final int DEFAULT_QUANTITY = 1;
    private final String orderId;
    private final String customerName;
    private final int quantity;

    public OrderSummary(String orderId, String customerName, int quantity)
    {
        if (quantity <= 0)
        {
            throw new IllegalArgumentException("Quantity must be positive.");
        }
        this.orderId = orderId;
        this.customerName = customerName;
        this.quantity = quantity;
    }

    public String getOrderId()
    {
        return this.orderId;
    }

    public String displayLabel()
    {
        return this.customerName + ": " + this.quantity;
    }
}
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

## SCSS-Specific Rules

### Variable Overrides

Always override Bootstrap variables in `_variables.scss`, not in component files.

```scss
// Good — in _variables.scss
$border-radius: 0 !default;

// Bad — in a component file
.my-component
{
    border-radius: 0; // Fights Bootstrap's default
}
```

### Nesting Depth

Limit SCSS nesting to 3 levels. Deep nesting produces overly specific selectors.

```scss
// Bad — too deep
.sidebar
{
    .nav
    {
        .nav-item
        {
            .nav-link
            {
                &:hover
                {
                    // 5 levels deep
                }
            }
        }
    }
}

// Good — flattened
.sidebar .nav-link
{
    // styles

    &:hover
    {
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

Keep one type per file in every language, even when the type is a five-line struct or a small interface.
Prefer separate files because filesystem searches should locate a type without searching file contents.
Nested types and extensions may remain beside their owning type when that arrangement explains a cohesive relationship.
Prefer a separate file when the relationship is clear without nesting. Do not group unrelated types to save files.

| Language | File organization |
| --- | --- |
| C# | `Order.cs`, `IOrderStore.cs`, and `OrderStatus.cs`. |
| Swift | `Order.swift`, `OrderStore.swift`, and, where useful, `Order+Validation.swift`. |
| Go | `order.go`, `order_store.go`, and `order_status.go` in the same package. |
| Rust | `order.rs`, `order_store.rs`, and `order_status.rs`, registered by their parent module. |
| Java | `Order.java`, `OrderStore.java`, and `OrderStatus.java`. Match a public type to its filename. |
| Python | `order.py`, `order_store.py`, and `order_status.py` in the same package. |
| TypeScript | `order.ts`, `order-store.ts`, and `order-status.ts`. |

Examples may show several labeled files together to explain a relationship. Split them at the file labels in actual code.
A Rust `impl` belongs with its type or a deliberate extension module. It is not a second type.

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

Keep functions and methods at or below 30 lines of code. Do not pad a shorter function.
If a function exceeds this limit, extract smaller functions with clear responsibilities.

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

Use typed errors for expected failures. Check cancellation during long-running work and let the caller choose the recovery behavior.

```swift
// File: QuantityCounter.swift
struct QuantityCounter
{
    func countPositive(_ quantities: [Int]) throws -> Int
    {
        try Task.checkCancellation()
        var count = 0
        for quantity in quantities
        {
            try Task.checkCancellation()
            if quantity > 0
            {
                count += 1
            }
        }
        return count
    }
}
```

### Go-Specific

- Return and check `error` values. Add useful context without losing the wrapped error.
- Pass `context.Context` to operations that support cancellation or deadlines. Do not use panic for expected failures.
- Give each goroutine a defined lifetime and shutdown path. Synchronize shared mutable state.
- Define small interfaces where consumers need them. Avoid copying inheritance-based designs into Go.
- Close owned resources and preserve meaningful errors from final writes, flushes, and closes.

Keep cancellation checks in long-running work. Return an error without presenting partial output as a complete result.

```go
package quantities

import (
    "context"
    "errors"
)

// CountPositive returns the number of positive quantities, or a cancellation error.
func CountPositive(ctx context.Context, quantities []int) (int, error) {
    if ctx == nil {
        return 0, errors.New("context is required")
    }
    count := 0
    for _, quantity := range quantities {
        if err := ctx.Err(); err != nil {
            return 0, err
        }
        if quantity > 0 {
            count += 1
        }
    }
    return count, nil
}
```

### Rust-Specific

- Use ownership and borrowing to express resource lifetimes. Do not clone values solely to avoid understanding a borrow error.
- Use `Result` for recoverable failures and `Option` for an expected absence. Avoid `unwrap` and `expect` on fallible external input.
- Keep `unsafe` blocks narrow and document their safety invariants.
- Choose shared ownership and an async runtime only when the requirements justify them.
- Propagate cancellation and release resources when tasks finish or stop.

Borrow input when ownership does not need to move. Use checked arithmetic when external values can overflow the result.

```rust
// File: quantity_total.rs
/// Adds quantities without copying or taking ownership of the input.
///
/// # Errors
/// Returns an error if the sum exceeds the supported range.
pub fn total_quantity(quantities: &[u32]) -> Result<u32, &'static str>
{
    let mut total: u32 = 0;
    for quantity in quantities
    {
        total = total.checked_add(*quantity).ok_or("quantity total exceeds its limit")?;
    }
    Ok(total)
}
```

### Java-Specific

- Use the JDK and Maven or Gradle toolchain configured by the repository.
- Use try-with-resources for owned `AutoCloseable` resources. Preserve interruption when handling `InterruptedException`.
- State nullability and mutability expectations in API contracts. Use the project's established error model.
- Keep business logic separate from HTTP handlers and framework extension entry points.
- Match host-provided APIs and dependency versions when building plugins or providers.

Close owned file resources through try-with-resources. Distinguish an empty file from a failed read instead of returning fabricated content.

```java
// File: FirstLineReader.java
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Optional;

public final class FirstLineReader
{
    public Optional<String> read(Path path) throws IOException
    {
        try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8))
        {
            return Optional.ofNullable(reader.readLine());
        }
    }
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

- [ ] One type per file, with only justified nested-type or extension exceptions
- [ ] Maximum 120 characters per source line
- [ ] Four spaces for indentation, with no tabs
- [ ] Allman braces wherever the language grammar permits them
- [ ] Go uses only its required syntax exceptions, and Python uses indentation-based blocks
- [ ] Always use braces for control flow in languages that have braces
- [ ] Parentheses around expressions for clarity
- [ ] Maximum 30 lines per function or method
- [ ] Maximum three levels of nesting
- [ ] Early returns for guard clauses
- [ ] Assertions for invariants
- [ ] SCSS nesting max 3 levels
- [ ] No `!important` in component SCSS
- [ ] Component CSS classes prefixed with component name
- [ ] Domain-appropriate naming
- [ ] Explicit code over clever tricks
