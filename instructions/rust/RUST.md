<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 588d6a37-db12-42a0-a2ef-a3e794110c13
Created: 2026
-->

<!-- AGENT: Rust conventions and task examples; load only when this language is in scope. -->

# Rust instructions

Read this guide when the task changes Rust source or its language-specific build and test configuration.
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

Read by task: [References](#references), [Formatting](#formatting), [Naming](#naming), [File organization](#file-organization), [Language constructs](#language-constructs), [Comments](#comments), [Navigation markers](#navigation-markers), [Folding](#folding), [Testing](#testing), [Coverage](#coverage), [Logging](#logging), [Log identity helper](#log-identity-helper), [Logging examples](#logging-examples), [Performance](#performance), [Design patterns](#design-patterns).

## References

1. Follow [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) for public contracts and names.
2. Apply the formatting and file rules in this document instead of the default formatter style.

## Formatting

Do not run default `rustfmt` as an automatic rewrite when its output would violate the house style.
Use syntax, compile, and lint checks separately when the configured formatter cannot express this style.

## Naming

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

## File organization

`order.rs`, `order_store.rs`, and `order_status.rs`, registered by their parent module.

A Rust `impl` belongs with its type or a deliberate extension module. It is not a second type.

## Language constructs

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

## Comments

Use `///` for item documentation and `//!` for module or crate documentation, following [rustdoc conventions](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html).
Document errors, panics, ownership, and examples where relevant.
Document caller obligations under `# Safety` for unsafe APIs and explain each unsafe block's safety invariant.
Use ordinary comments for navigation markers rather than exposing internal markers as public API documentation.

```rust
/// Parses a positive quantity without retaining the input.
///
/// # Errors
/// Returns an error for invalid decimal text, overflow, or zero.
///
/// # Examples
/// The caller handles the error instead of treating a failed parse as zero.
pub fn parse_quantity(text: &str) -> Result<u32, String>
{
    let quantity = text.parse::<u32>().map_err(|_|
    {
        "invalid quantity".to_owned()
    })?;
    if quantity == 0
    {
        return Err("quantity must be positive".to_owned());
    }
    Ok(quantity)
}
```

## Navigation markers

```rust
// File: quantity_policy.rs
/*
 * COMPONENT: QuantityPolicy
 * PURPOSE: Validates a quantity before constructing an order.
 * RELATES: [[OrderValidation]]
 * FLOW: Command -> quantity policy -> order constructor
 * SECURITY: Validate external values before storing them.
 */

// @entrypoint
/// Returns whether a signed external quantity is positive.
pub fn is_valid_quantity(quantity: i64) -> bool
{
    quantity > 0
}
```

Keep `//!` module documentation and crate attributes valid. Use ordinary comments for navigation tags rather than publishing them as rustdoc.

## Folding

Use ordinary section comments unless the project declares supported IDE folding markers.
Do not copy C# `#region` directives into this language.

## Testing

Use unit tests, integration tests, and documentation tests through `cargo test`.
Check relevant feature combinations and targets declared by the project.
Run the configured style and Clippy checks alongside behavior tests.
Do not use default `cargo fmt` output to override the Allman and indentation rules in `instructions/CODING_STYLE.md`.

```rust
// File: order_summary.rs, nested test module beside the owning type.
#[cfg(test)]
mod tests
{
    use super::OrderSummary;

    #[test]
    fn display_label_with_positive_quantity_includes_quantity()
    {
        let order = OrderSummary::new("order-1".into(), "Sample Customer".into(), 2)
            .expect("the fixture quantity is valid");
        assert_eq!(order.display_label(), "Sample Customer: 2");
    }

    #[test]
    fn constructor_with_zero_quantity_returns_error()
    {
        assert!(OrderSummary::new("order-1".into(), "Sample Customer".into(), 0).is_err());
    }
}
```

`expect` is appropriate for a known-valid test fixture. It is not permission to panic on fallible production input.
Use `tests/` for public-boundary integration tests. Test declared features, foreign-function boundaries, and drop/cancellation behavior where affected.

## Coverage

Use the project's configured coverage tool, such as `cargo llvm-cov`, with its declared targets and features.

## Logging

Use the configured `tracing` or `log` facade. Let the application configure subscribers or backends.

## Log identity helper

Rust uses the established RustCrypto implementations. These versions illustrate compatible APIs, not a universal dependency upgrade requirement:

```toml
[dependencies]
hmac = "0.13"
sha2 = "0.11"
```

```rust
// File: log_identity.rs
use hmac::{Hmac, KeyInit, Mac};
use sha2::Sha256;

/// Returns a stable tenant-scoped pseudonym for approved log correlation.
pub fn user_log_key(key: &[u8], tenant_id: &str, canonical_username: &str) -> Result<String, &'static str>
{
    if key.len() < 32
    {
        return Err("a logging key needs at least 32 bytes");
    }
    let mut mac = Hmac::<Sha256>::new_from_slice(key).map_err(|_|
    {
        "invalid logging key"
    })?;
    mac.update(b"log-user-v1\0");
    for field in [tenant_id, canonical_username]
    {
        let bytes = field.as_bytes();
        if bytes.len() > 1024
        {
            return Err("a log identity field exceeds its limit");
        }
        mac.update(&(bytes.len() as u32).to_be_bytes());
        mac.update(bytes);
    }
    let hex = mac.finalize().into_bytes().iter().map(|byte|
    {
        format!("{byte:02x}")
    }).collect::<String>();
    Ok(format!("user-hmac-v1:{hex}"))
}
```

## Logging examples

Use the project's configured subscriber and sinks. This synchronous example enters a span and receives an already-approved user key.
For async work, instrument the future instead of holding a synchronous entered-span guard across `await`.

```rust
// File: order_diagnostics.rs
pub fn validate_quantity(correlation_id: &str, user_key: &str, quantity: i64) -> Result<i64, &'static str>
{
    let span = tracing::info_span!("validate_quantity", correlation_id, user_key);
    let _entered = span.enter();
    tracing::trace!("operation started");
    let result = if quantity > 0
    {
        tracing::debug!(quantity, "positive quantity branch");
        Ok(quantity)
    }
    else
    {
        tracing::warn!(reason = "nonpositive_quantity", "validation failed");
        Err("quantity must be positive")
    };
    tracing::trace!(success = result.is_ok(), "operation finished");
    result
}
```

The example assumes the existing `tracing` dependency. It does not install a subscriber from library code.
Keep structured fields stable so tools can filter by correlation ID, user key, operation, and failure reason.

## Performance

Measure latency, throughput, allocations, and bounded concurrency before optimizing.

- Measure the release profile and actual target. Debug-build performance is not a release baseline.
- Use the project's benchmark harness and record relevant feature flags, allocator, and async runtime configuration.
- Avoid unnecessary clones and allocations, but do not trade ownership clarity or memory safety for an unmeasured saving.
- Bound task spawning and buffering. Keep blocking I/O off an async executor's worker threads when the runtime requires it.
- Inspect resource lifetimes and dropped tasks when memory or file handles grow over time.
- Treat unsafe optimizations as a separate, justified change with safety tests and measured benefit.

## Design patterns

### 1) Abstract Factory

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#1-abstract-factory).

```rust
trait ThemeFactory
{
    fn make_button(&self) -> &'static str;
    fn make_input(&self) -> &'static str;
}

struct DarkTheme;

impl ThemeFactory for DarkTheme
{
    fn make_button(&self) -> &'static str
    {
        "dark-button"
    }

    fn make_input(&self) -> &'static str
    {
        "dark-input"
    }
}
```

### 2) Builder

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#2-builder).

```rust
#[derive(Default)]
struct ReportBuilder
{
    title: String,
    sections: Vec<String>,
}

impl ReportBuilder
{
    fn with_title(mut self, value: String) -> Self
    {
        self.title = value;
        self
    }

    fn add_section(mut self, value: String) -> Self
    {
        self.sections.push(value);
        self
    }

    fn build(self) -> String
    {
        let mut parts = vec![self.title];
        parts.extend(self.sections);
        parts.join("\n")
    }
}
```

### 3) Factory Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#3-factory-method).

```rust
trait Exporter
{
    fn create_writer(&self) -> Box<dyn Fn(&str) -> String>;

    fn export(&self, text: &str) -> String
    {
        self.create_writer()(text)
    }
}

struct UppercaseExporter;

impl Exporter for UppercaseExporter
{
    fn create_writer(&self) -> Box<dyn Fn(&str) -> String>
    {
        Box::new(|text|
        {
            text.to_uppercase()
        })
    }
}
```

### 4) Prototype

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#4-prototype).

```rust
#[derive(Clone)]
struct Layout
{
    title: String,
    columns: Vec<String>,
}
```

### 5) Singleton

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#5-singleton).

```rust
use std::sync::OnceLock;

struct AppSettings
{
    time_zone: &'static str,
}

static SETTINGS: OnceLock<AppSettings> = OnceLock::new();

fn app_settings() -> &'static AppSettings
{
    SETTINGS.get_or_init(||
    {
        AppSettings
        {
            time_zone: "UTC",
        }
    })
}
```

### 6) Adapter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#6-adapter).

```rust
struct PrinterAdapter<F: Fn(&[u8]) -> usize>
{
    send_bytes: F,
}

impl<F: Fn(&[u8]) -> usize> PrinterAdapter<F>
{
    fn print_text(&self, text: &str) -> usize
    {
        (self.send_bytes)(text.as_bytes())
    }
}
```

### 7) Bridge

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#7-bridge).

```rust
struct Circle<F: Fn(f64) -> String>
{
    radius: f64,
    render_circle: F,
}

impl<F: Fn(f64) -> String> Circle<F>
{
    fn draw(&self) -> String
    {
        (self.render_circle)(self.radius)
    }
}
```

### 8) Composite

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#8-composite).

```rust
enum Node
{
    Leaf(i32),
    Branch(Vec<Node>),
}

impl Node
{
    fn total(&self) -> i32
    {
        match self
        {
            Self::Leaf(value) => *value,
            Self::Branch(children) => children.iter().map(Node::total).sum(),
        }
    }
}
```

### 9) Decorator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#9-decorator).

```rust
fn with_brackets(render: impl Fn() -> String) -> impl Fn() -> String
{
    move ||
    {
        format!("[{}]", render())
    }
}
```

### 10) Facade

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#10-facade).

```rust
struct ExportFacade
{
    read: Box<dyn Fn() -> Result<String, &'static str>>,
    format_text: Box<dyn Fn(&str) -> Result<String, &'static str>>,
    write: Box<dyn Fn(&str) -> Result<(), &'static str>>,
}

impl ExportFacade
{
    fn run(&self) -> Result<(), &'static str>
    {
        let text = (self.read)()?;
        let formatted = (self.format_text)(&text)?;
        (self.write)(&formatted)
    }
}
```

### 11) Flyweight

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#11-flyweight).

```rust
use std::collections::HashMap;
use std::sync::Arc;

struct Icon
{
    path: String,
}

#[derive(Default)]
struct IconFactory
{
    cache: HashMap<String, Arc<Icon>>,
}

impl IconFactory
{
    fn get(&mut self, path: &str) -> Arc<Icon>
    {
        Arc::clone(self.cache.entry(path.to_owned()).or_insert_with(||
        {
            Arc::new(Icon
            {
                path: path.to_owned(),
            })
        }))
    }
}
```

### 12) Proxy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#12-proxy).

```rust
struct DocumentProxy
{
    can_read: Box<dyn Fn() -> bool>,
    read: Box<dyn Fn() -> Result<String, &'static str>>,
}

impl DocumentProxy
{
    fn load(&self) -> Result<String, &'static str>
    {
        if !(self.can_read)()
        {
            return Err("document access denied");
        }
        (self.read)()
    }
}
```

### 13) Chain of Responsibility

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#13-chain-of-responsibility).

```rust
fn validate_chain(value: i32, handlers: &[fn(i32) -> Result<(), &'static str>]) -> Result<(), &'static str>
{
    for handler in handlers
    {
        handler(value)?;
    }
    Ok(())
}
```

### 14) Command

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#14-command).

```rust
struct IncrementCommand
{
    delta: i32,
}

impl IncrementCommand
{
    fn execute(&self, counter: &mut i32)
    {
        *counter += self.delta;
    }

    fn undo(&self, counter: &mut i32)
    {
        *counter -= self.delta;
    }
}
```

### 15) Interpreter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#15-interpreter).

```rust
enum Expression
{
    Number(i32),
    Add(Box<Expression>, Box<Expression>),
}

impl Expression
{
    fn evaluate(&self) -> i32
    {
        match self
        {
            Self::Number(value) => *value,
            Self::Add(left, right) => left.evaluate() + right.evaluate(),
        }
    }
}
```

### 16) Iterator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#16-iterator).

```rust
struct EvenIterator
{
    values: Vec<i32>,
    index: usize,
}

impl Iterator for EvenIterator
{
    type Item = i32;

    fn next(&mut self) -> Option<Self::Item>
    {
        while self.index < self.values.len()
        {
            let value = self.values[self.index];
            self.index += 1;
            if value % 2 == 0
            {
                return Some(value);
            }
        }
        None
    }
}
```

### 17) Mediator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#17-mediator).

```rust
struct FormMediator
{
    show_title: Box<dyn Fn(&str)>,
    mark_dirty: Box<dyn Fn()>,
}

impl FormMediator
{
    fn title_changed(&self, title: &str)
    {
        (self.show_title)(title);
        (self.mark_dirty)();
    }
}
```

### 18) Memento

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#18-memento).

```rust
struct EditorSnapshot
{
    text: String,
}

struct TextEditor
{
    text: String,
}

impl TextEditor
{
    fn snapshot(&self) -> EditorSnapshot
    {
        EditorSnapshot
        {
            text: self.text.clone(),
        }
    }

    fn restore(&mut self, snapshot: &EditorSnapshot)
    {
        self.text = snapshot.text.clone();
    }
}
```

### 19) Observer

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#19-observer).

```rust
use std::collections::HashMap;

#[derive(Default)]
struct Publisher
{
    listeners: HashMap<usize, Box<dyn Fn(&str)>>,
    next_token: usize,
}

impl Publisher
{
    fn subscribe(&mut self, listener: Box<dyn Fn(&str)>) -> usize
    {
        self.next_token += 1;
        self.listeners.insert(self.next_token, listener);
        self.next_token
    }

    fn unsubscribe(&mut self, token: usize)
    {
        self.listeners.remove(&token);
    }

    fn publish(&self, message: &str)
    {
        for listener in self.listeners.values()
        {
            listener(message);
        }
    }
}
```

### 20) State

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#20-state).

```rust
#[derive(Debug, PartialEq)]
enum JobState
{
    Idle,
    Running,
    Complete,
}

impl JobState
{
    fn start(&mut self) -> Result<(), &'static str>
    {
        if *self != Self::Idle
        {
            return Err("only an idle job can start");
        }
        *self = Self::Running;
        Ok(())
    }

    fn complete(&mut self) -> Result<(), &'static str>
    {
        if *self != Self::Running
        {
            return Err("only a running job can complete");
        }
        *self = Self::Complete;
        Ok(())
    }
}
```

### 21) Strategy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#21-strategy).

```rust
fn format_text(text: &str, strategy: impl Fn(&str) -> String) -> String
{
    strategy(text)
}
```

### 22) Template Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#22-template-method).

```rust
trait Importer
{
    fn read(&self) -> Result<String, &'static str>;
    fn save(&self, text: &str) -> Result<(), &'static str>;

    fn validate(&self, text: &str) -> Result<(), &'static str>
    {
        if text.is_empty()
        {
            return Err("import content must not be empty");
        }
        Ok(())
    }

    fn run(&self) -> Result<(), &'static str>
    {
        let text = self.read()?;
        self.validate(&text)?;
        self.save(&text)
    }
}
```

### 23) Visitor

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#23-visitor).

```rust
trait ValueVisitor
{
    fn visit_text(&self, value: &str) -> String;
    fn visit_number(&self, value: i32) -> String;
}

enum Value
{
    Text(String),
    Number(i32),
}

impl Value
{
    fn accept(&self, visitor: &dyn ValueVisitor) -> String
    {
        match self
        {
            Self::Text(text) => visitor.visit_text(text),
            Self::Number(number) => visitor.visit_number(*number),
        }
    }
}

struct RenderVisitor;

impl ValueVisitor for RenderVisitor
{
    fn visit_text(&self, value: &str) -> String
    {
        format!("text:{value}")
    }

    fn visit_number(&self, value: i32) -> String
    {
        format!("number:{value}")
    }
}
```


## Security

Apply [general security](../SECURITY_GUIDELINES.md). Memory safety does not replace validation or authorization.
Use parameterized database APIs and explicit serialization contracts.
Use `Command` arguments without a shell. Validate option-like user arguments and executable paths.
Validate lengths, ownership, lifetimes, and pointer assumptions at every `unsafe` or foreign-function boundary.
Document the safety invariant and test it. Avoid panics on malformed external input.

For sensitive owned values, consider an approved zeroing abstraction such as `zeroize::Zeroizing`:

```rust
// SECURITY: Zero this owned buffer on normal scope exit and unwinding.
use zeroize::Zeroizing;

let secret = Zeroizing::new(load_secret_bytes()?);
use_secret(secret.as_slice())?;
```

The application supplies both functions. They must not retain plaintext copies.
`Zeroizing` does not lock pages or erase copies created by moves, reallocations, or called libraries.
Destructors do not run on every termination path, including process abort.
Check the crate's actual guarantees and runtime compatibility before adoption.
See [zeroize documentation](https://docs.rs/zeroize/latest/zeroize/).
Use secure exclusive temporary-file creation with restrictive permissions through the approved platform API or crate.
Validate path containment and symlink behavior separately from file creation.
