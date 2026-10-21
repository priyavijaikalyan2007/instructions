<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 502a2a91-9515-458a-b070-89713ce2976f
Created: 2026
-->

<!-- AGENT: Swift conventions and task examples; load only when this language is in scope. -->

# Swift instructions

Read this guide when the task changes Swift source or its language-specific build and test configuration.
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

Read by task: [References](#references), [Naming](#naming), [File organization](#file-organization), [Language constructs](#language-constructs), [Comments](#comments), [Navigation markers](#navigation-markers), [Folding](#folding), [Testing](#testing), [Coverage](#coverage), [Logging](#logging), [Log identity helper](#log-identity-helper), [Logging examples](#logging-examples), [Performance](../apps/APPS.md#apple-performance-guidance), [Secret handling](../apps/APPS.md#apple-credential-storage), [Design patterns](#design-patterns).

## References

1. Follow [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/) for names and contracts.
2. Apply the formatting and file rules in this document.

## Naming

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

## File organization

`Order.swift`, `OrderStore.swift`, and, where useful, `Order+Validation.swift`.

## Language constructs

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

## Comments

Use `///` documentation comments for public APIs, following [Swift API conventions](https://www.swift.org/documentation/api-design-guidelines/).
Describe parameters, return values, thrown errors, actor isolation, and cancellation when relevant.
Use `// MARK: - Section name` for sections that benefit Xcode navigation.

```swift
/// Parses a positive quantity from user-entered text.
/// - Parameter text: The complete decimal quantity, without surrounding spaces.
/// - Returns: The quantity, or nil when the text is invalid or nonpositive.
/// - Important: This function does not log or retain the input.
func parseQuantity(_ text: String) -> Int?
{
    guard let quantity = Int(text), quantity > 0 else
    {
        return nil
    }
    return quantity
}
```

## Navigation markers

```swift
// File: QuantityPolicy.swift
/*
 * COMPONENT: QuantityPolicy
 * PURPOSE: Validates a quantity before constructing an order.
 * RELATES: [[OrderValidation]]
 * FLOW: Native view -> quantity policy -> order constructor
 * SECURITY: Validate imported values before storing them.
 */

// MARK: - Public API
// @entrypoint
func isValidQuantity(_ quantity: Int) -> Bool
{
    return quantity > 0
}
```

## Folding

Swift uses `// MARK: - Section name` for Xcode navigation.

## Testing

Use the project's Swift Testing or XCTest setup for unit and integration tests.
See [APPS.md](../apps/APPS.md#apple-application-testing).
Run `swift test` for Swift packages and the documented Xcode scheme and destination for application tests.

```swift
// File: OrderSummaryTests.swift
import XCTest

final class OrderSummaryTests: XCTestCase
{
    func testDisplayLabelWithPositiveQuantityIncludesQuantity() throws
    {
        let order = try OrderSummary(orderID: "order-1", customerName: "Sample Customer", quantity: 2)
        XCTAssertEqual(order.displayLabel(), "Sample Customer: 2")
    }

    func testConstructorWithZeroQuantityThrows()
    {
        XCTAssertThrowsError(try OrderSummary(orderID: "order-1", customerName: "Sample Customer", quantity: 0))
    }
}
```

Add the test file to the correct test target and import the application module with `@testable` where needed.

## Coverage

Collect coverage through the configured Xcode test plan or `swift test --enable-code-coverage` for packages.

## Logging

Use the project's logging API, such as `Logger` from `OSLog`, with appropriate privacy annotations.

## Log identity helper

Swift uses CryptoKit. A distributed app must not contain a shared backend logging key.
Use a protected local key for local correlation or a server-issued opaque identifier for cross-device server correlation.

```swift
// File: LogIdentity.swift
import CryptoKit
import Foundation

struct LogIdentity
{
    enum ValidationError: Error
    {
        case invalidKey
        case oversizedField
    }

    static func userLogKey(key: Data, tenantID: String, canonicalUsername: String) throws -> String
    {
        guard key.count >= 32 else
        {
            throw ValidationError.invalidKey
        }
        let payload = try identityPayload(tenantID: tenantID, canonicalUsername: canonicalUsername)
        let digest = HMAC<SHA256>.authenticationCode(for: payload, using: SymmetricKey(data: key))
        return "user-hmac-v1:" + digest.map
        {
            String(format: "%02x", $0)
        }.joined()
    }

    private static func identityPayload(tenantID: String, canonicalUsername: String) throws -> Data
    {
        var payload = Data("log-user-v1\0".utf8)
        for field in [tenantID, canonicalUsername]
        {
            let bytes = Array(field.utf8)
            guard bytes.count <= 1024 else
            {
                throw ValidationError.oversizedField
            }
            let length = UInt32(bytes.count)
            payload.append(contentsOf: [24, 16, 8, 0].map
            {
                UInt8((length >> $0) & 0xff)
            })
            payload.append(contentsOf: bytes)
        }
        return payload
    }
}
```

## Logging examples

Pass approved context into the operation. Use a protected local pseudonym or a server-issued identifier, not a raw username.
Mark only approved fields public. Native unified logging controls storage and collection, so do not create a duplicate plaintext sink by default.

```swift
// File: OrderDiagnostics.swift
import OSLog

struct OrderDiagnostics
{
    let logger: Logger

    func recordValidation(correlationID: String, userKey: String, quantity: Int) -> Bool
    {
        logger.debug("validation.start correlation_id=\(correlationID, privacy: .public)")
        defer
        {
            logger.debug("validation.end correlation_id=\(correlationID, privacy: .public)")
        }
        guard quantity > 0 else
        {
            logger.error("validation.failed user_key=\(userKey, privacy: .public) reason=nonpositive_quantity")
            return false
        }
        logger.info("validation.ok user_key=\(userKey, privacy: .public) quantity=\(quantity)")
        return true
    }
}
```

The application creates the logger with its configured subsystem and category.
Attach task, scene, or document identifiers when they help diagnose concurrency and lifecycle behavior.
Do not assume that a thread identifier identifies an async operation.

## Performance

See [APPS.md](../apps/APPS.md#apple-performance-guidance).

## Secret handling

See [APPS.md](../apps/APPS.md#apple-credential-storage).

## Design patterns

### 1) Abstract Factory

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#1-abstract-factory).

```swift
protocol ThemeFactory
{
    func makeButton() -> String
    func makeInput() -> String
}

struct DarkTheme: ThemeFactory
{
    func makeButton() -> String
    {
        return "dark-button"
    }

    func makeInput() -> String
    {
        return "dark-input"
    }
}
```

### 2) Builder

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#2-builder).

```swift
struct ReportBuilder
{
    private var title = ""
    private var sections: [String] = []

    mutating func setTitle(_ value: String)
    {
        title = value
    }

    mutating func addSection(_ value: String)
    {
        sections.append(value)
    }

    func build() -> String
    {
        return ([title] + sections).joined(separator: "\n")
    }
}
```

### 3) Factory Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#3-factory-method).

```swift
protocol Exporter
{
    func createWriter() -> (String) -> String
}

extension Exporter
{
    func export(_ text: String) -> String
    {
        return createWriter()(text)
    }
}

struct UppercaseExporter: Exporter
{
    func createWriter() -> (String) -> String
    {
        return
        {
            $0.uppercased()
        }
    }
}
```

### 4) Prototype

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#4-prototype).

```swift
struct Layout
{
    var title: String
    var columns: [String]

    func clone() -> Layout
    {
        return self
    }
}
```

### 5) Singleton

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#5-singleton).

```swift
final class AppSettings: Sendable
{
    static let shared = AppSettings()
    let timeZone = "UTC"

    private init()
    {
    }
}
```

### 6) Adapter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#6-adapter).

```swift
struct PrinterAdapter
{
    let sendBytes: ([UInt8]) -> Int

    func printText(_ text: String) -> Int
    {
        return sendBytes(Array(text.utf8))
    }
}
```

### 7) Bridge

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#7-bridge).

```swift
struct Circle
{
    let radius: Double
    let renderCircle: (Double) -> String

    func draw() -> String
    {
        return renderCircle(radius)
    }
}
```

### 8) Composite

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#8-composite).

```swift
indirect enum Node
{
    case leaf(Int)
    case branch([Node])

    func total() -> Int
    {
        switch self
        {
            case .leaf(let value):
                return value
            case .branch(let children):
                return children.reduce(0)
                {
                    $0 + $1.total()
                }
        }
    }
}
```

### 9) Decorator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#9-decorator).

```swift
func withBrackets(_ render: @escaping () -> String) -> () -> String
{
    return
    {
        return "[" + render() + "]"
    }
}
```

### 10) Facade

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#10-facade).

```swift
struct ExportFacade
{
    let read: () throws -> String
    let formatText: (String) throws -> String
    let write: (String) throws -> Void

    func run() throws
    {
        let text = try read()
        let formatted = try formatText(text)
        try write(formatted)
    }
}
```

### 11) Flyweight

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#11-flyweight).

```swift
final class Icon
{
    let path: String

    init(path: String)
    {
        self.path = path
    }
}

final class IconFactory
{
    private var cache: [String: Icon] = [:]

    func get(_ path: String) -> Icon
    {
        if let existing = cache[path]
        {
            return existing
        }
        let created = Icon(path: path)
        cache[path] = created
        return created
    }
}
```

### 12) Proxy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#12-proxy).

```swift
struct DocumentProxy
{
    enum AccessError: Error
    {
        case denied
    }

    let canRead: () -> Bool
    let read: () throws -> String

    func load() throws -> String
    {
        guard canRead() else
        {
            throw AccessError.denied
        }
        return try read()
    }
}
```

### 13) Chain of Responsibility

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#13-chain-of-responsibility).

```swift
func validateChain(_ value: Int, handlers: [(Int) -> String?]) -> String?
{
    for handler in handlers
    {
        if let error = handler(value)
        {
            return error
        }
    }
    return nil
}
```

### 14) Command

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#14-command).

```swift
final class Counter
{
    var value = 0
}

struct IncrementCommand
{
    let counter: Counter

    func execute()
    {
        counter.value += 1
    }

    func undo()
    {
        counter.value -= 1
    }
}
```

### 15) Interpreter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#15-interpreter).

```swift
indirect enum Expression
{
    case number(Int)
    case add(Expression, Expression)

    func evaluate() -> Int
    {
        switch self
        {
            case .number(let value):
                return value
            case .add(let left, let right):
                return left.evaluate() + right.evaluate()
        }
    }
}
```

### 16) Iterator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#16-iterator).

```swift
struct EvenIterator: IteratorProtocol
{
    let values: [Int]
    private var index = 0

    init(values: [Int])
    {
        self.values = values
    }

    mutating func next() -> Int?
    {
        while index < values.count
        {
            let value = values[index]
            index += 1
            if value.isMultiple(of: 2)
            {
                return value
            }
        }
        return nil
    }
}
```

### 17) Mediator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#17-mediator).

```swift
struct FormMediator
{
    let showTitle: (String) -> Void
    let markDirty: () -> Void

    func titleChanged(_ title: String)
    {
        showTitle(title)
        markDirty()
    }
}
```

### 18) Memento

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#18-memento).

```swift
struct EditorSnapshot
{
    let text: String
}

struct TextEditor
{
    var text: String

    func snapshot() -> EditorSnapshot
    {
        return EditorSnapshot(text: text)
    }

    mutating func restore(_ snapshot: EditorSnapshot)
    {
        text = snapshot.text
    }
}
```

### 19) Observer

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#19-observer).

```swift
final class Publisher
{
    private var listeners: [Int: (String) -> Void] = [:]
    private var nextToken = 0

    func subscribe(_ listener: @escaping (String) -> Void) -> Int
    {
        nextToken += 1
        listeners[nextToken] = listener
        return nextToken
    }

    func unsubscribe(_ token: Int)
    {
        listeners[token] = nil
    }

    func publish(_ message: String)
    {
        for listener in Array(listeners.values)
        {
            listener(message)
        }
    }
}
```

### 20) State

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#20-state).

```swift
enum JobState
{
    case idle
    case running
    case complete
}

struct Job
{
    private(set) var state = JobState.idle

    mutating func start() -> Bool
    {
        guard state == .idle else
        {
            return false
        }
        state = .running
        return true
    }

    mutating func complete() -> Bool
    {
        guard state == .running else
        {
            return false
        }
        state = .complete
        return true
    }
}
```

### 21) Strategy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#21-strategy).

```swift
func formatText(_ text: String, using strategy: (String) -> String) -> String
{
    return strategy(text)
}
```

### 22) Template Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#22-template-method).

```swift
enum ImportError: Error
{
    case emptyContent
}

protocol Importer
{
    func read() throws -> String
    func validate(_ text: String) throws
    func save(_ text: String) throws
}

extension Importer
{
    func validate(_ text: String) throws
    {
        guard !text.isEmpty else
        {
            throw ImportError.emptyContent
        }
    }

    func run() throws
    {
        let text = try read()
        try validate(text)
        try save(text)
    }
}
```

### 23) Visitor

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#23-visitor).

```swift
protocol ValueVisitor
{
    func visit(text: String) -> String
    func visit(number: Int) -> String
}

enum Value
{
    case text(String)
    case number(Int)

    func accept(_ visitor: any ValueVisitor) -> String
    {
        switch self
        {
            case .text(let text):
                return visitor.visit(text: text)
            case .number(let number):
                return visitor.visit(number: number)
        }
    }
}

struct RenderVisitor: ValueVisitor
{
    func visit(text: String) -> String
    {
        return "text:" + text
    }

    func visit(number: Int) -> String
    {
        return "number:" + String(number)
    }
}
```


## Security

Apply [general security](../SECURITY_GUIDELINES.md) and [secret handling](../SECRET_HANDLING.md).
Store persistent credentials through Keychain Services. Choose accessibility, device migration, and synchronization settings deliberately.
Use Secure Enclave-backed keys only for supported key operations. It is not general-purpose storage for arbitrary secrets.
Do not put tokens in UserDefaults, app resources, diagnostic output, or ordinary exported documents.
Respect transport security and platform trust evaluation. Do not bypass certificate validation to make a request succeed.
See [Apple Keychain Services](https://developer.apple.com/documentation/security/keychain-services).

For a UIKit target, configure intentional sensitive copying through supported pasteboard options:

```swift
// SECURITY: Limit device propagation and clipboard lifetime after an explicit Copy action.
UIPasteboard.general.setItems(
    [["public.utf8-plain-text": valueToCopy]],
    options: [
        .localOnly: true,
        .expirationDate: Date().addingTimeInterval(clipboardLifetime)
    ]
)
```

The project defines `clipboardLifetime`. Other applications can still read the local clipboard under platform rules.
See [Apple pasteboard configuration](https://developer.apple.com/documentation/uikit/uipasteboard/setitems(_:options:)).
Do not assume these UIKit options exist on `NSPasteboard`. Check supported AppKit controls separately.

Swift strings and `Data` can create copies through value semantics and bridging.
Clearing one buffer does not prove all plaintext copies disappeared. Use a vetted native buffer abstraction when stronger control is required.
Keep unsafe buffer scopes short and document ownership. Check the actual memory-locking and dump-exclusion support.
For stored sensitive files, use supported data-protection attributes and intentional backup policies.
Apply shared temporary-file controls to imports, previews, autosave, and exports.
