<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 1cc640db-86ee-4f65-844d-bb1b0f1d97eb
Created: 2026
-->

<!-- AGENT: Go conventions and task examples; load only when this language is in scope. -->

# Go instructions

Read this guide when the task changes Go source or its language-specific build and test configuration.
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

Read by task: [References](#references), [Formatting](#formatting), [Naming](#naming), [File organization](#file-organization), [Language constructs](#language-constructs), [Comments](#comments), [Navigation markers](#navigation-markers), [Folding](#folding), [Testing](#testing), [Test examples](#test-examples), [Coverage](#coverage), [Logging](#logging), [Log identity helper](#log-identity-helper), [Logging examples](#logging-examples), [Performance](#performance), [Design patterns](#design-patterns).

## References

1. Follow [Effective Go](https://go.dev/doc/effective_go) for API names, errors, and language semantics.
2. Apply the formatting and file rules in this document, including the required Go brace exceptions.

## Formatting

Go's semicolon insertion requires same-line braces for function bodies, control flow, and composite literals.
This is a syntax limit, not a preference for another style. Keep four-space indentation and the other house rules in Go.
Do not run default `gofmt` as an automatic rewrite when its output would violate the house style.
Use syntax, compile, and lint checks separately when the configured formatter cannot express this style.
See the [Go semicolon rules](https://go.dev/ref/spec#Semicolons).

## Naming

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

## File organization

`order.go`, `order_store.go`, and `order_status.go` in the same package.

## Language constructs

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

## Comments

Follow [Go doc comments](https://go.dev/doc/comment). Start exported declaration comments with the declared name.
Place a documentation comment directly before the declaration it describes.
Document error behavior, context cancellation, ownership, and concurrent-use guarantees when relevant.
Keep navigation headers separate so they do not become an unrelated declaration's documentation.

```go
package quantities

import (
    "fmt"
    "strconv"
)

// ParseQuantity parses a positive decimal quantity.
// It returns an error for invalid text, overflow, or a nonpositive value.
// It does not retain the input and is safe for concurrent calls.
func ParseQuantity(text string) (int, error) {
    quantity, err := strconv.Atoi(text)
    if err != nil {
        return 0, fmt.Errorf("parse quantity: %w", err)
    }
    if quantity <= 0 {
        return 0, fmt.Errorf("quantity must be positive")
    }
    return quantity, nil
}
```

## Navigation markers

```go
// File: quantity_policy.go
// COMPONENT: QuantityPolicy
// PURPOSE: Validates a quantity before constructing an order.
// RELATES: [[OrderValidation]]
// FLOW: Command -> quantity policy -> order constructor
// SECURITY: Validate external values before storing them.

package quantities

// @entrypoint
// IsValidQuantity reports whether the quantity is positive.
func IsValidQuantity(quantity int) bool {
    return quantity > 0
}
```

The blank line before `package` separates navigation metadata from package documentation.
Preserve Go build constraints and the cgo preamble when adding a header.

## Folding

Use ordinary section comments unless the project declares supported IDE folding markers.
Do not copy C# `#region` directives into this language.

## Testing

Use the standard `testing` package, table-driven tests where useful, and `go test ./...`.
Run `go test -race ./...` for concurrency changes on a supported target.
Use fuzz tests for parsers and other input boundaries when appropriate.

```go
// File: order_summary_test.go
package orders

import "testing"

func TestDisplayLabelWithPositiveQuantityIncludesQuantity(t *testing.T) {
    order, err := NewOrderSummary("order-1", "Sample Customer", 2)
    if err != nil {
        t.Fatalf("create test order: %v", err)
    }
    if actual := order.DisplayLabel(); actual != "Sample Customer: 2" {
        t.Errorf("label = %q, want %q", actual, "Sample Customer: 2")
    }
}

func TestConstructorWithZeroQuantityReturnsError(t *testing.T) {
    _, err := NewOrderSummary("order-1", "Sample Customer", 0)
    if err == nil {
        t.Fatal("expected a quantity validation error")
    }
}
```

Use `t.TempDir()` and `t.Cleanup` for owned resources. Mark tests parallel only when their state and external resources are independent.
Race checks supplement behavior tests. They do not prove that cancellation, timeouts, or goroutine shutdown follow the contract.

## Test examples

### Infrastructure as Code (Terraform)

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

## Coverage

Use `go test ./... -coverprofile=coverage.out` and `go tool cover -func=coverage.out`.

## Logging

Use the established logger, such as standard-library `log/slog`, and propagate request context.

## Log identity helper

Go uses the standard library and four-space indentation:

```go
// File: log_identity.go
package logidentity

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/binary"
    "encoding/hex"
    "errors"
)

// UserLogKey returns a stable tenant-scoped pseudonym for approved log correlation.
func UserLogKey(key []byte, tenantID string, canonicalUsername string) (string, error) {
    if len(key) < 32 {
        return "", errors.New("a logging key needs at least 32 bytes")
    }
    payload := []byte("log-user-v1\x00")
    for _, field := range []string{tenantID, canonicalUsername} {
        encoded := []byte(field)
        if len(encoded) > 1024 {
            return "", errors.New("a log identity field exceeds its limit")
        }
        payload = binary.BigEndian.AppendUint32(payload, uint32(len(encoded)))
        payload = append(payload, encoded...)
    }
    mac := hmac.New(sha256.New, key)
    _, _ = mac.Write(payload) // Standard hash writers do not return write errors.
    return "user-hmac-v1:" + hex.EncodeToString(mac.Sum(nil)), nil
}
```

## Logging examples

```go
package main

import (
    "context"
    "log/slog"
)

// Key for Context
type key int
const (
    correlationIDKey key = iota
    tenantIDKey
)

// Middleware to inject context
func withContext(ctx context.Context, correlationID, tenantID string) context.Context {
    ctx = context.WithValue(ctx, correlationIDKey, correlationID)
    ctx = context.WithValue(ctx, tenantIDKey, tenantID)
    return ctx
}

// Logger helper to extract context
func logAt(ctx context.Context, level slog.Level, msg string, args ...any) {
    // Extract context
    cID, _ := ctx.Value(correlationIDKey).(string)
    tID, _ := ctx.Value(tenantIDKey).(string)

    // Add standard context attributes
    baseArgs := []any{
        slog.String("correlation_id", cID),
        slog.String("tenant_id", tID),
    }
    finalArgs := append(baseArgs, args...)

    slog.Log(ctx, level, msg, finalArgs...)
}

func processOrder(ctx context.Context, orderID string, amount float64) {
    // TRACE: Entry. Configure level -8 in the application's slog handler.
    logAt(ctx, slog.Level(-8), "Entering processOrder", slog.String("order_id", orderID))

    // BRANCHING: Log condition data before "if"
    isHighValue := amount > 1000.0
    logAt(ctx, slog.LevelDebug, "Evaluating high value check", slog.Bool("is_high_value", isHighValue))

    if isHighValue {
        logAt(ctx, slog.LevelDebug, "Branch taken: High Value Protocol")
        // ... logic
    } else {
        logAt(ctx, slog.LevelDebug, "Branch taken: Standard Protocol")
    }

    // EXIT
    logAt(ctx, slog.Level(-8), "Exiting processOrder")
}
```

---

## Performance

Measure latency, throughput, allocations, and bounded concurrency before optimizing.

- Use representative benchmarks and allocation measurements, such as `go test -bench . -benchmem`.
- Use the project's CPU, heap, goroutine, and blocking profiles when a measurement indicates a regression.
- Bound goroutine fan-out, queue depth, buffer sizes, and external calls.
- Propagate context deadlines and cancellation. Ensure abandoned work does not keep consuming resources.
- Measure serialization and I/O before adding caches, pools, or custom memory reuse.
- Benchmark release-like builds on the target architecture and retain the baseline and workload.

## Design patterns

### 1) Abstract Factory

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#1-abstract-factory).

```go
package examples

type ThemeFactory interface
{
    MakeButton() string
    MakeInput() string
}

type DarkTheme struct
{
}

func (theme DarkTheme) MakeButton() string {
    return "dark-button"
}

func (theme DarkTheme) MakeInput() string {
    return "dark-input"
}
```

### 2) Builder

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#2-builder).

```go
package examples

import "strings"

type ReportBuilder struct
{
    title string
    sections []string
}

func (builder *ReportBuilder) WithTitle(value string) *ReportBuilder {
    builder.title = value
    return builder
}

func (builder *ReportBuilder) AddSection(value string) *ReportBuilder {
    builder.sections = append(builder.sections, value)
    return builder
}

func (builder *ReportBuilder) Build() string {
    parts := append([]string{builder.title}, builder.sections...)
    return strings.Join(parts, "\n")
}
```

### 3) Factory Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#3-factory-method).

```go
package examples

import "strings"

type Exporter struct
{
    CreateWriter func() func(string) string
}

func (exporter Exporter) Export(text string) string {
    return exporter.CreateWriter()(text)
}

func NewUppercaseExporter() Exporter {
    return Exporter{
        CreateWriter: func() func(string) string {
            return strings.ToUpper
        },
    }
}
```

### 4) Prototype

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#4-prototype).

```go
package examples

type Layout struct
{
    Title string
    Columns []string
}

func (layout Layout) Clone() Layout {
    clone := layout
    clone.Columns = append([]string(nil), layout.Columns...)
    return clone
}
```

### 5) Singleton

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#5-singleton).

```go
package examples

import "sync"

type appSettings struct
{
    timeZone string
}

var settingsOnce sync.Once
var settingsValue *appSettings

func AppSettings() *appSettings {
    settingsOnce.Do(func() {
        settingsValue = &appSettings{timeZone: "UTC"}
    })
    return settingsValue
}
```

### 6) Adapter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#6-adapter).

```go
package examples

type PrinterAdapter struct
{
    SendBytes func([]byte) int
}

func (adapter PrinterAdapter) PrintText(text string) int {
    return adapter.SendBytes([]byte(text))
}
```

### 7) Bridge

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#7-bridge).

```go
package examples

type Circle struct
{
    Radius float64
    RenderCircle func(float64) string
}

func (circle Circle) Draw() string {
    return circle.RenderCircle(circle.Radius)
}
```

### 8) Composite

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#8-composite).

```go
package examples

type Node struct
{
    Value int
    Children []*Node
}

func (node Node) Total() int {
    total := node.Value
    for _, child := range node.Children {
        total += child.Total()
    }
    return total
}
```

### 9) Decorator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#9-decorator).

```go
package examples

type Render func() string

func WithBrackets(render Render) Render {
    return func() string {
        return "[" + render() + "]"
    }
}
```

### 10) Facade

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#10-facade).

```go
package examples

type ExportFacade struct
{
    Read func() (string, error)
    FormatText func(string) (string, error)
    Write func(string) error
}

func (facade ExportFacade) Run() error {
    text, err := facade.Read()
    if err != nil {
        return err
    }
    formatted, err := facade.FormatText(text)
    if err != nil {
        return err
    }
    return facade.Write(formatted)
}
```

### 11) Flyweight

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#11-flyweight).

```go
package examples

type Icon struct
{
    Path string
}

type IconFactory struct
{
    cache map[string]*Icon
}

func NewIconFactory() *IconFactory {
    return &IconFactory{cache: make(map[string]*Icon)}
}

func (factory *IconFactory) Get(path string) *Icon {
    if existing, found := factory.cache[path]; found {
        return existing
    }
    created := &Icon{Path: path}
    factory.cache[path] = created
    return created
}
```

### 12) Proxy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#12-proxy).

```go
package examples

import "errors"

type DocumentProxy struct
{
    CanRead func() bool
    Read func() (string, error)
}

func (proxy DocumentProxy) Load() (string, error) {
    if !proxy.CanRead() {
        return "", errors.New("document access denied")
    }
    return proxy.Read()
}
```

### 13) Chain of Responsibility

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#13-chain-of-responsibility).

```go
package examples

type ValidationChain []func(int) error

func (chain ValidationChain) Validate(value int) error {
    for _, handler := range chain {
        if err := handler(value); err != nil {
            return err
        }
    }
    return nil
}
```

### 14) Command

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#14-command).

```go
package examples

type Counter struct
{
    Value int
}

type IncrementCommand struct
{
    Counter *Counter
}

func (command IncrementCommand) Execute() {
    command.Counter.Value += 1
}

func (command IncrementCommand) Undo() {
    command.Counter.Value -= 1
}
```

### 15) Interpreter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#15-interpreter).

```go
package examples

type Expression interface
{
    Evaluate() int
}

type Number int

func (number Number) Evaluate() int {
    return int(number)
}

type Add struct
{
    Left Expression
    Right Expression
}

func (expression Add) Evaluate() int {
    return expression.Left.Evaluate() + expression.Right.Evaluate()
}
```

### 16) Iterator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#16-iterator).

```go
package examples

type EvenIterator struct
{
    Values []int
    index int
}

func (iterator *EvenIterator) Next() (int, bool) {
    for iterator.index < len(iterator.Values) {
        value := iterator.Values[iterator.index]
        iterator.index += 1
        if value % 2 == 0 {
            return value, true
        }
    }
    return 0, false
}
```

### 17) Mediator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#17-mediator).

```go
package examples

type FormMediator struct
{
    ShowTitle func(string)
    MarkDirty func()
}

func (mediator FormMediator) TitleChanged(title string) {
    mediator.ShowTitle(title)
    mediator.MarkDirty()
}
```

### 18) Memento

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#18-memento).

```go
package examples

type EditorSnapshot struct
{
    text string
}

type TextEditor struct
{
    Text string
}

func (editor TextEditor) Snapshot() EditorSnapshot {
    return EditorSnapshot{text: editor.Text}
}

func (editor *TextEditor) Restore(snapshot EditorSnapshot) {
    editor.Text = snapshot.text
}
```

### 19) Observer

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#19-observer).

```go
package examples

type Publisher struct
{
    listeners map[int]func(string)
    nextToken int
}

func (publisher *Publisher) Subscribe(listener func(string)) int {
    if publisher.listeners == nil {
        publisher.listeners = make(map[int]func(string))
    }
    publisher.nextToken += 1
    publisher.listeners[publisher.nextToken] = listener
    return publisher.nextToken
}

func (publisher *Publisher) Unsubscribe(token int) {
    delete(publisher.listeners, token)
}

func (publisher *Publisher) Publish(message string) {
    listeners := make([]func(string), 0, len(publisher.listeners))
    for _, listener := range publisher.listeners {
        listeners = append(listeners, listener)
    }
    for _, listener := range listeners {
        listener(message)
    }
}
```

### 20) State

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#20-state).

```go
package examples

import "errors"

type JobState int

const (
    JobIdle JobState = iota
    JobRunning
    JobComplete
)

type Job struct
{
    State JobState
}

func (job *Job) Start() error {
    if job.State != JobIdle {
        return errors.New("only an idle job can start")
    }
    job.State = JobRunning
    return nil
}

func (job *Job) Complete() error {
    if job.State != JobRunning {
        return errors.New("only a running job can complete")
    }
    job.State = JobComplete
    return nil
}
```

### 21) Strategy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#21-strategy).

```go
package examples

type Formatter func(string) string

func FormatText(text string, strategy Formatter) string {
    return strategy(text)
}
```

### 22) Template Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#22-template-method).

```go
package examples

type Importer interface
{
    Read() (string, error)
    Validate(string) error
    Save(string) error
}

func RunImport(importer Importer) error {
    text, err := importer.Read()
    if err != nil {
        return err
    }
    if err := importer.Validate(text); err != nil {
        return err
    }
    return importer.Save(text)
}
```

### 23) Visitor

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#23-visitor).

```go
package examples

import "strconv"

type ValueVisitor interface
{
    VisitText(string) string
    VisitNumber(int) string
}

type TextValue string

func (value TextValue) Accept(visitor ValueVisitor) string {
    return visitor.VisitText(string(value))
}

type NumberValue int

func (value NumberValue) Accept(visitor ValueVisitor) string {
    return visitor.VisitNumber(int(value))
}

type RenderVisitor struct
{
}

func (visitor RenderVisitor) VisitText(value string) string {
    return "text:" + value
}

func (visitor RenderVisitor) VisitNumber(value int) string {
    return "number:" + strconv.Itoa(value)
}
```


## Security

Apply [general security](../SECURITY_GUIDELINES.md), including tenant isolation and memory limitations.
Pass query values separately to `database/sql`. Placeholder syntax depends on the configured driver.
Do not build SQL with `fmt.Sprintf`. Use bounded request contexts and check errors, including row iteration errors.
See [Go SQL injection prevention](https://go.dev/doc/database/sql-injection).

```go
// SECURITY: PostgreSQL driver example. Tenant identity comes from verified application context.
rows, err := db.QueryContext(ctx,
    "SELECT display_name FROM customer WHERE tenant_id = $1 AND id = $2",
    authorizedTenantID, customerID)
if err != nil {
    return err
}
defer rows.Close()
```

Go requires the opening brace on the same line. Continue by reading rows and checking `rows.Err()`.
Use `html/template` for HTML output. Do not convert untrusted content to trusted template types.
Use argument arrays through `os/exec`. Do not pass untrusted command text through a shell.
Create temporary files through `os.CreateTemp` inside a private directory. Close and remove them on every exit path.
Avoid converting secret byte slices into strings. Clear owned slices before reuse, while documenting retained-copy limits.
The garbage collector and compiler do not provide a general secret-erasure or non-swapping guarantee.
Synchronize shared mutable state and run the race detector for affected concurrency paths.
A race-free implementation still needs authorization and resource limits.

See [Go temporary-file creation](https://pkg.go.dev/os#CreateTemp) for creation permissions and cleanup responsibilities.
