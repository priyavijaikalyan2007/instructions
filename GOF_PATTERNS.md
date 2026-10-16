<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 96556d56-4611-4e45-9c41-22ba6722244c
Created: 2026
-->

<!-- AGENT: Practical guidance on applying Gang of Four design patterns in the codebase. -->

# Gang of Four (GoF) Design Patterns - Coding Agent Guide

Purpose: Provide balanced, practical guidance on when and how to apply GoF patterns in this codebase.

Principles
- Use patterns when they solve a real problem: variability, testability, separation of concerns, or extensibility.
- Do not force a pattern if a simple function, small class, or library feature suffices.
- Prefer clarity over cleverness. A pattern is a shared vocabulary, not a requirement.

Format per pattern
- Intent: What it is for.
- When to use: Signals that pattern helps.
- Avoid when: Common overuse cases.
- C# / TypeScript / JavaScript / Python / Swift / Go / Java / Rust: minimal examples.

The examples isolate each pattern. They do not prescribe a new framework or replace the project's existing APIs.
When a block contains multiple top-level types, put each type in its own file in production.
Keep a type's extensions or nested implementation types together only when that placement has a clear purpose.
Use four spaces, no tabs, a 120-character line limit, and Allman braces wherever the grammar permits them.
Go requires same-line braces for functions and control flow. Python uses indentation instead of braces.
Preserve those syntax requirements rather than copying invalid code or allowing a formatter to change the shared style.
The added examples use standard-library features. Wire real UI controls, persistence, and logging at the application boundary.

---

## Creational Patterns

### 1) Abstract Factory
Intent: Create families of related objects without specifying concrete classes.
When to use: Interchangeable product families with compatibility constraints.
Avoid when: Only one product family or no compatibility constraints.

C#
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

TypeScript
```ts
interface WidgetFactory
{
    createButton(): Button;
    createInput(): Input;
}

class DarkFactory implements WidgetFactory
{
    public createButton(): Button
    {
        return new DarkButton();
    }

    public createInput(): Input
    {
        return new DarkInput();
    }
}
```

JavaScript
```js
class DarkFactory
{
    createButton()
    {
        return new DarkButton();
    }

    createInput()
    {
        return new DarkInput();
    }
}
```

The added examples use product labels to show compatible families without UI dependencies. Real factories return the project's control interfaces.

Python
```python
from typing import Protocol

class ThemeFactory(Protocol):
    def make_button(self) -> str: ...
    def make_input(self) -> str: ...

class DarkTheme:
    def make_button(self) -> str:
        return "dark-button"

    def make_input(self) -> str:
        return "dark-input"
```

Swift
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

Go
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

Java
```java
interface ThemeFactory
{
    String makeButton();
    String makeInput();
}

final class DarkTheme implements ThemeFactory
{
    public String makeButton()
    {
        return "dark-button";
    }

    public String makeInput()
    {
        return "dark-input";
    }
}
```

Rust
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
Intent: Construct complex objects step-by-step with a fluent API.
When to use: Many optional fields or required ordering.
Avoid when: A simple constructor or object literal is enough.

C#
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

TypeScript
```ts
class ReportBuilder
{
    private report: Report = { title: "", sections: [] };

    public title(value: string): ReportBuilder
    {
        this.report.title = value;
        return this;
    }

    public addSection(section: string): ReportBuilder
    {
        this.report.sections.push(section);
        return this;
    }

    public build(): Report
    {
        return this.report;
    }
}
```

JavaScript
```js
class ReportBuilder
{
    constructor()
    {
        this.report = { title: "", sections: [] };
    }

    title(value)
    {
        this.report.title = value;
        return this;
    }

    addSection(section)
    {
        this.report.sections.push(section);
        return this;
    }

    build()
    {
        return this.report;
    }
}
```

The added builders return an independent string value. For mutable report objects, copy state or consume the builder to prevent later mutation.

Python
```python
class ReportBuilder:
    def __init__(self) -> None:
        self._title = ""
        self._sections: list[str] = []

    def with_title(self, title: str) -> "ReportBuilder":
        self._title = title
        return self

    def add_section(self, section: str) -> "ReportBuilder":
        self._sections.append(section)
        return self

    def build(self) -> str:
        return "\n".join([self._title, *self._sections])
```

Swift
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

Go
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

Java
```java
import java.util.ArrayList;
import java.util.List;

final class ReportBuilder
{
    private String title = "";
    private final List<String> sections = new ArrayList<>();

    ReportBuilder withTitle(String value)
    {
        this.title = value;
        return this;
    }

    ReportBuilder addSection(String value)
    {
        this.sections.add(value);
        return this;
    }

    String build()
    {
        return this.title + "\n" + String.join("\n", this.sections);
    }
}
```

Rust
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
Intent: Let subclasses decide which class to instantiate.
When to use: Creation varies by subclass or runtime type selection.
Avoid when: Only one concrete type exists.

C#
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

TypeScript
```ts
abstract class Exporter
{
    public abstract createWriter(): Writer;
}

class CsvExporter extends Exporter
{
    public createWriter(): Writer
    {
        return new CsvWriter();
    }
}
```

JavaScript
```js
class Exporter
{
    createWriter()
    {
        throw new Error("Override required");
    }
}

class CsvExporter extends Exporter
{
    createWriter()
    {
        return new CsvWriter();
    }
}
```

Python and Java use class-based creation hooks. Swift and Rust use protocol or trait defaults. Go injects a factory function.

Python
```python
from abc import ABC, abstractmethod
from typing import Callable

class Exporter(ABC):
    @abstractmethod
    def create_writer(self) -> Callable[[str], str]: ...

    def export(self, text: str) -> str:
        return self.create_writer()(text)

class UppercaseExporter(Exporter):
    def create_writer(self) -> Callable[[str], str]:
        return str.upper
```

Swift
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

Go
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

Java
```java
import java.util.Locale;
import java.util.function.UnaryOperator;

abstract class Exporter
{
    abstract UnaryOperator<String> createWriter();

    final String export(String text)
    {
        return createWriter().apply(text);
    }
}

final class UppercaseExporter extends Exporter
{
    UnaryOperator<String> createWriter()
    {
        return text ->
        {
            return text.toUpperCase(Locale.ROOT);
        };
    }
}
```

Rust
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
Intent: Create new objects by cloning existing ones.
When to use: Expensive creation; need variations of a configured object.
Avoid when: Cloning is complex or error-prone.

C#
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

TypeScript
```ts
class Template
{
    public constructor(public name: string)
    {
    }

    public clone(): Template
    {
        return new Template(this.name);
    }
}
```

JavaScript
```js
class Template
{
    constructor(name)
    {
        this.name = name;
    }

    clone()
    {
        return new Template(this.name);
    }
}
```

Copy mutable owned state when independent edits are required. Swift and Rust value copies, Go slice copies, and Java defensive copies express that contract.

Python
```python
from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class Layout:
    title: str
    columns: list[str] = field(default_factory=list)

    def clone(self) -> "Layout":
        return deepcopy(self)
```

Swift
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

Go
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

Java
```java
import java.util.ArrayList;
import java.util.List;

final class Layout
{
    String title;
    final List<String> columns;

    Layout(String title, List<String> columns)
    {
        this.title = title;
        this.columns = new ArrayList<>(columns);
    }

    Layout copy()
    {
        return new Layout(this.title, this.columns);
    }
}
```

Rust
```rust
#[derive(Clone)]
struct Layout
{
    title: String,
    columns: Vec<String>,
}
```

### 5) Singleton
Intent: Ensure a class has one instance and a global access point.
When to use: A shared, stateless service or cache with strict single-instance semantics.
Avoid when: You need multiple configurations or test isolation; prefer DI.

C#
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

TypeScript
```ts
class AppClock
{
    private static readonly instance: AppClock = new AppClock();

    private constructor()
    {
    }

    public static getInstance(): AppClock
    {
        return AppClock.instance;
    }
}
```

JavaScript
```js
class AppClock
{
    constructor()
    {
        this.now = () => new Date();
    }
}

const AppClockSingleton = (() =>
{
    const instance = new AppClock();
    return {
        getInstance()
        {
            return instance;
        }
    };
})();
```

These instances are process-local. Prefer injected settings when tests need isolation. Protect mutable shared state rather than assuming singleton construction makes it safe.

Python
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class _AppSettings:
    time_zone: str = "UTC"

_settings = _AppSettings()

def app_settings() -> _AppSettings:
    return _settings
```

Swift
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

Go
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

Java
```java
enum AppSettings
{
    INSTANCE;

    String timeZone()
    {
        return "UTC";
    }
}
```

Rust
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

---

## Structural Patterns

### 6) Adapter
Intent: Convert one interface to another clients expect.
When to use: Integrating legacy or third-party APIs.
Avoid when: You can change the client or use native interface directly.

C#
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

TypeScript
```ts
class AuthAdapter implements AuthClient
{
    public constructor(private readonly legacy: LegacyAuth)
    {
    }

    public login(creds: Creds): Promise<Token>
    {
        return this.legacy.signIn(creds.user, creds.pass);
    }
}
```

JavaScript
```js
class AuthAdapter
{
    constructor(legacy)
    {
        this.legacy = legacy;
    }

    login(creds)
    {
        return this.legacy.signIn(creds.user, creds.pass);
    }
}
```

The adapter translates the boundary contract and delegates once. Preserve real encoding and failure rules instead of concealing them.

Python
```python
from typing import Callable

class PrinterAdapter:
    def __init__(self, send_bytes: Callable[[bytes], int]) -> None:
        self._send_bytes = send_bytes

    def print_text(self, text: str) -> int:
        return self._send_bytes(text.encode("utf-8"))
```

Swift
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

Go
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

Java
```java
import java.nio.charset.StandardCharsets;
import java.util.function.ToIntFunction;

final class PrinterAdapter
{
    private final ToIntFunction<byte[]> sendBytes;

    PrinterAdapter(ToIntFunction<byte[]> sendBytes)
    {
        this.sendBytes = sendBytes;
    }

    int printText(String text)
    {
        return this.sendBytes.applyAsInt(text.getBytes(StandardCharsets.UTF_8));
    }
}
```

Rust
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
Intent: Separate abstraction from implementation so both can vary.
When to use: Multiple orthogonal dimensions (e.g., UI type and theme).
Avoid when: Only one dimension exists.

C#
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

TypeScript
```ts
interface Renderer
{
    drawCircle(radius: number): void;
}

abstract class Shape
{
    protected constructor(protected renderer: Renderer)
    {
    }
}

class Circle extends Shape
{
    public draw(): void
    {
        this.renderer.drawCircle(10);
    }
}
```

JavaScript
```js
class Shape
{
    constructor(renderer)
    {
        this.renderer = renderer;
    }
}

class Circle extends Shape
{
    draw()
    {
        this.renderer.drawCircle(10);
    }
}
```

The shape owns geometry and receives a renderer. More shapes and rendering backends can vary independently without a subclass for each combination.

Python
```python
from typing import Callable

class Circle:
    def __init__(self, radius: float, render_circle: Callable[[float], str]) -> None:
        self._radius = radius
        self._render_circle = render_circle

    def draw(self) -> str:
        return self._render_circle(self._radius)
```

Swift
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

Go
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

Java
```java
import java.util.function.DoubleFunction;

final class Circle
{
    private final double radius;
    private final DoubleFunction<String> renderCircle;

    Circle(double radius, DoubleFunction<String> renderCircle)
    {
        this.radius = radius;
        this.renderCircle = renderCircle;
    }

    String draw()
    {
        return this.renderCircle.apply(this.radius);
    }
}
```

Rust
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
Intent: Treat individual objects and compositions uniformly.
When to use: Tree structures with leaf and container nodes.
Avoid when: Simple flat lists.

C#
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

TypeScript
```ts
interface Node
{
    render(): void;
}

class Leaf implements Node
{
    public render(): void
    {
    }
}

class Group implements Node
{
    private readonly children: Node[] = [];

    public add(child: Node): void
    {
        this.children.push(child);
    }

    public render(): void
    {
        for (const child of this.children)
        {
            child.render();
        }
    }
}
```

JavaScript
```js
class Group
{
    constructor()
    {
        this.children = [];
    }

    add(child)
    {
        this.children.push(child);
    }

    render()
    {
        for (const child of this.children)
        {
            child.render();
        }
    }
}
```

The uniform node or enum gives leaves and branches the same traversal contract. Bound recursion and reject cycles when loading external trees.

Python
```python
from dataclasses import dataclass, field

@dataclass
class Node:
    value: int
    children: list["Node"] = field(default_factory=list)

    def total(self) -> int:
        return self.value + sum(child.total() for child in self.children)
```

Swift
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

Go
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

Java
```java
import java.util.List;

final class Node
{
    private final int value;
    private final List<Node> children;

    Node(int value, List<Node> children)
    {
        this.value = value;
        this.children = List.copyOf(children);
    }

    int total()
    {
        int total = this.value;
        for (Node child : this.children)
        {
            total += child.total();
        }
        return total;
    }
}
```

Rust
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
Intent: Add responsibilities dynamically without subclassing.
When to use: Optional behaviors layered at runtime (logging, caching).
Avoid when: Behavior is fixed or class hierarchy is simpler.

C#
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

TypeScript
```ts
interface Writer
{
    write(value: string): string;
}

class UpperWriter implements Writer
{
    public write(value: string): string
    {
        return value.toUpperCase();
    }
}

class TrimWriter implements Writer
{
    public constructor(private readonly inner: Writer)
    {
    }

    public write(value: string): string
    {
        return this.inner.write(value.trim());
    }
}
```

JavaScript
```js
class TrimWriter
{
    constructor(inner)
    {
        this.inner = inner;
    }

    write(value)
    {
        return this.inner.write(value.trim());
    }
}
```

A function wrapper is sufficient when only behavior changes. Use a richer interface when resource ownership or several operations require it.

Python
```python
from typing import Callable

def with_brackets(render: Callable[[], str]) -> Callable[[], str]:
    def decorated() -> str:
        return "[" + render() + "]"
    return decorated
```

Swift
```swift
func withBrackets(_ render: @escaping () -> String) -> () -> String
{
    return
    {
        return "[" + render() + "]"
    }
}
```

Go
```go
package examples

type Render func() string

func WithBrackets(render Render) Render {
    return func() string {
        return "[" + render() + "]"
    }
}
```

Java
```java
import java.util.function.Supplier;

final class RenderDecorators
{
    static Supplier<String> withBrackets(Supplier<String> render)
    {
        return () ->
        {
            return "[" + render.get() + "]";
        };
    }
}
```

Rust
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
Intent: Provide a simplified API over a complex subsystem.
When to use: Complex modules with many steps; reduce coupling.
Avoid when: Subsystem is already small.

C#
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

TypeScript
```ts
class ExportFacade
{
    public constructor(private readonly renderer: Renderer, private readonly storage: Storage)
    {
    }

    public export(document: Document): Promise<string>
    {
        const file = this.renderer.render(document);
        return this.storage.save(file);
    }
}
```

JavaScript
```js
class ExportFacade
{
    constructor(renderer, storage)
    {
        this.renderer = renderer;
        this.storage = storage;
    }

    export(document)
    {
        const file = this.renderer.render(document);
        return this.storage.save(file);
    }
}
```

The facade orders read, format, and write operations. Failures propagate to the caller, and a failed read or format must prevent the write.

Python
```python
from typing import Callable

class ExportFacade:
    def __init__(self, read: Callable[[], str], format_text: Callable[[str], str],
                 write: Callable[[str], None]) -> None:
        self._read = read
        self._format_text = format_text
        self._write = write

    def run(self) -> None:
        text = self._read()
        formatted = self._format_text(text)
        self._write(formatted)
```

Swift
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

Go
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

Java
```java
import java.util.function.Consumer;
import java.util.function.Supplier;
import java.util.function.UnaryOperator;

final class ExportFacade
{
    private final Supplier<String> read;
    private final UnaryOperator<String> formatText;
    private final Consumer<String> write;

    ExportFacade(Supplier<String> read, UnaryOperator<String> formatText, Consumer<String> write)
    {
        this.read = read;
        this.formatText = formatText;
        this.write = write;
    }

    void run()
    {
        String text = this.read.get();
        String formatted = this.formatText.apply(text);
        this.write.accept(formatted);
    }
}
```

Rust
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
Intent: Share common state to reduce memory usage.
When to use: Huge numbers of similar objects.
Avoid when: State is mostly unique or mutation makes sharing risky.

C#
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

TypeScript
```ts
class IconFactory
{
    private readonly cache: Map<string, Icon> = new Map();

    public get(path: string): Icon
    {
        const cached = this.cache.get(path);
        if (cached)
        {
            return cached;
        }

        const created = new Icon(path);
        this.cache.set(path, created);
        return created;
    }
}
```

JavaScript
```js
class IconFactory
{
    constructor()
    {
        this.cache = new Map();
    }

    get(path)
    {
        const cached = this.cache.get(path);
        if (cached)
        {
            return cached;
        }

        const created = new Icon(path);
        this.cache.set(path, created);
        return created;
    }
}
```

The factory shares immutable icons. These caches are confined to one execution context. Define synchronization, cache bounds, and eviction for production.

Python
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Icon:
    path: str

class IconFactory:
    def __init__(self) -> None:
        self._cache: dict[str, Icon] = {}

    def get(self, path: str) -> Icon:
        if path not in self._cache:
            self._cache[path] = Icon(path)
        return self._cache[path]
```

Swift
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

Go
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

Java
```java
import java.util.HashMap;
import java.util.Map;

record Icon(String path)
{
}

final class IconFactory
{
    private final Map<String, Icon> cache = new HashMap<>();

    Icon get(String path)
    {
        return this.cache.computeIfAbsent(path, Icon::new);
    }
}
```

Rust
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
Intent: Control access to an object (lazy load, security, caching).
When to use: Expensive objects or access control.
Avoid when: Direct access is safe and simple.

C#
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

TypeScript
```ts
class SecuredRepo implements Repo
{
    public constructor(private readonly inner: Repo, private readonly auth: Auth)
    {
    }

    public get(id: string): Promise<Item>
    {
        this.auth.ensure("read");
        return this.inner.get(id);
    }
}
```

JavaScript
```js
class SecuredRepo
{
    constructor(inner, auth)
    {
        this.inner = inner;
        this.auth = auth;
    }

    get(id)
    {
        this.auth.ensure("read");
        return this.inner.get(id);
    }
}
```

Authorize every protected read before delegation. Supply trusted resource-scoped authorization from the server or local security boundary, not a UI visibility flag.

Python
```python
from typing import Callable

class DocumentProxy:
    def __init__(self, can_read: Callable[[], bool], read: Callable[[], str]) -> None:
        self._can_read = can_read
        self._read = read

    def read(self) -> str:
        if not self._can_read():
            raise PermissionError("Document access denied.")
        return self._read()
```

Swift
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

Go
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

Java
```java
import java.util.function.BooleanSupplier;
import java.util.function.Supplier;

final class DocumentProxy
{
    private final BooleanSupplier canRead;
    private final Supplier<String> read;

    DocumentProxy(BooleanSupplier canRead, Supplier<String> read)
    {
        this.canRead = canRead;
        this.read = read;
    }

    String load()
    {
        if (!this.canRead.getAsBoolean())
        {
            throw new SecurityException("Document access denied.");
        }
        return this.read.get();
    }
}
```

Rust
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

---

## Behavioral Patterns

### 13) Chain of Responsibility
Intent: Pass a request through a chain until handled.
When to use: Pipeline of handlers (validation, policy checks).
Avoid when: A single, fixed handler suffices.

C#
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

TypeScript
```ts
abstract class Handler
{
    protected next?: Handler;

    public setNext(next: Handler): Handler
    {
        this.next = next;
        return next;
    }

    public abstract handle(request: Request): boolean;
}

class AuthHandler extends Handler
{
    public handle(request: Request): boolean
    {
        if (!request.user)
        {
            return false;
        }

        return this.next?.handle(request) ?? true;
    }
}
```

JavaScript
```js
class Handler
{
    setNext(next)
    {
        this.next = next;
        return next;
    }

    handle(request)
    {
        throw new Error("Override required");
    }
}

class AuthHandler extends Handler
{
    handle(request)
    {
        if (!request.user)
        {
            return false;
        }

        return this.next ? this.next.handle(request) : true;
    }
}
```

Stop at the first validation failure. Define whether later checks depend on earlier checks before changing their order.

Python
```python
from collections.abc import Callable, Iterable

def validate_chain(value: int, handlers: Iterable[Callable[[int], str | None]]) -> str | None:
    for handler in handlers:
        error = handler(value)
        if error is not None:
            return error
    return None
```

Swift
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

Go
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

Java
```java
import java.util.List;
import java.util.Optional;
import java.util.function.IntFunction;

final class ValidationChain
{
    private final List<IntFunction<Optional<String>>> handlers;

    ValidationChain(List<IntFunction<Optional<String>>> handlers)
    {
        this.handlers = List.copyOf(handlers);
    }

    Optional<String> validate(int value)
    {
        for (IntFunction<Optional<String>> handler : this.handlers)
        {
            Optional<String> error = handler.apply(value);
            if (error.isPresent())
            {
                return error;
            }
        }
        return Optional.empty();
    }
}
```

Rust
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
Intent: Encapsulate a request as an object (undo/redo, queues).
When to use: Undo, retries, queues, or logs.
Avoid when: Simple direct method call.

C#
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

TypeScript
```ts
interface Command
{
    execute(): void;
    undo(): void;
}

class RenameCommand implements Command
{
    private prev = "";

    public constructor(private readonly item: Item, private readonly next: string)
    {
    }

    public execute(): void
    {
        this.prev = this.item.name;
        this.item.name = this.next;
    }

    public undo(): void
    {
        this.item.name = this.prev;
    }
}
```

JavaScript
```js
class RenameCommand
{
    constructor(item, next)
    {
        this.item = item;
        this.next = next;
        this.prev = "";
    }

    execute()
    {
        this.prev = this.item.name;
        this.item.name = this.next;
    }

    undo()
    {
        this.item.name = this.prev;
    }
}
```

The invoker pairs execution and undo and serializes changes to the target. These examples do not provide an undo history or concurrent editing protocol.

Python
```python
from dataclasses import dataclass

@dataclass
class Counter:
    value: int = 0

class IncrementCommand:
    def __init__(self, counter: Counter) -> None:
        self._counter = counter

    def execute(self) -> None:
        self._counter.value += 1

    def undo(self) -> None:
        self._counter.value -= 1
```

Swift
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

Go
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

Java
```java
final class Counter
{
    int value;
}

final class IncrementCommand
{
    private final Counter counter;

    IncrementCommand(Counter counter)
    {
        this.counter = counter;
    }

    void execute()
    {
        this.counter.value += 1;
    }

    void undo()
    {
        this.counter.value -= 1;
    }
}
```

Rust
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
Intent: Define a grammar and interpret sentences in that language.
When to use: Simple DSLs (filters, rules).
Avoid when: Use a real parser or library instead.

C#
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

TypeScript
```ts
interface Expression
{
    evaluate(context: Context): boolean;
}

class AndExpression implements Expression
{
    public constructor(private readonly left: Expression, private readonly right: Expression)
    {
    }

    public evaluate(context: Context): boolean
    {
        return this.left.evaluate(context) && this.right.evaluate(context);
    }
}
```

JavaScript
```js
class AndExpression
{
    constructor(left, right)
    {
        this.left = left;
        this.right = right;
    }

    evaluate(context)
    {
        return this.left.evaluate(context) && this.right.evaluate(context);
    }
}
```

Interpret a typed expression tree rather than executing source text. Bound depth and validate numeric overflow when accepting external expressions.

Python
```python
from dataclasses import dataclass
from typing import Protocol

class Expression(Protocol):
    def evaluate(self) -> int: ...

@dataclass(frozen=True)
class Number:
    value: int

    def evaluate(self) -> int:
        return self.value

@dataclass(frozen=True)
class Add:
    left: Expression
    right: Expression

    def evaluate(self) -> int:
        return self.left.evaluate() + self.right.evaluate()
```

Swift
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

Go
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

Java
```java
interface Expression
{
    int evaluate();
}

record NumberExpression(int value) implements Expression
{
    public int evaluate()
    {
        return this.value;
    }
}

record AddExpression(Expression left, Expression right) implements Expression
{
    public int evaluate()
    {
        return this.left.evaluate() + this.right.evaluate();
    }
}
```

Rust
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
Intent: Traverse a collection without exposing its representation.
When to use: Custom collections; controlled traversal.
Avoid when: Native iterators already exist and suffice.

C#
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

TypeScript
```ts
class ListIterator<T> implements Iterator<T>
{
    private index = 0;

    public constructor(private readonly items: T[])
    {
    }

    public next(): IteratorResult<T>
    {
        if (this.index >= this.items.length)
        {
            return { done: true, value: undefined as unknown as T };
        }

        const value = this.items[this.index];
        this.index += 1;
        return { done: false, value };
    }
}
```

JavaScript
```js
const collection = {
    items: [1, 2],
    [Symbol.iterator]()
    {
        let index = 0;
        return {
            next: () =>
            {
                const done = index >= this.items.length;
                const value = done ? undefined : this.items[index];
                index += 1;
                return { done, value };
            }
        };
    }
};
```

The iterator exposes exhaustion explicitly. Keep traversal state private, and define mutation behavior if the underlying collection can change.

Python
```python
from collections.abc import Iterator, Sequence

def even_values(values: Sequence[int]) -> Iterator[int]:
    for value in values:
        if value % 2 == 0:
            yield value
```

Swift
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

Go
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

Java
```java
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

final class EvenIterator implements Iterator<Integer>
{
    private final List<Integer> values;
    private int index;

    EvenIterator(List<Integer> values)
    {
        this.values = List.copyOf(values);
    }

    public boolean hasNext()
    {
        while (this.index < this.values.size() && this.values.get(this.index) % 2 != 0)
        {
            this.index += 1;
        }
        return this.index < this.values.size();
    }

    public Integer next()
    {
        if (!hasNext())
        {
            throw new NoSuchElementException();
        }
        int value = this.values.get(this.index);
        this.index += 1;
        return value;
    }
}
```

Rust
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
Intent: Centralize complex communications between objects.
When to use: Many-to-many object interactions.
Avoid when: Only a few direct relationships.

C#
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

TypeScript
```ts
interface Mediator
{
    notify(sender: object, evt: string): void;
}

class DialogMediator implements Mediator
{
    public notify(sender: object, evt: string): void
    {
    }
}
```

JavaScript
```js
class DialogMediator
{
    notify(sender, evt)
    {
    }
}
```

The mediator coordinates related actions through injected callbacks. Keep business rules in services when coordination grows beyond this UI interaction.

Python
```python
from typing import Callable

class FormMediator:
    def __init__(self, show_title: Callable[[str], None], mark_dirty: Callable[[], None]) -> None:
        self._show_title = show_title
        self._mark_dirty = mark_dirty

    def title_changed(self, title: str) -> None:
        self._show_title(title)
        self._mark_dirty()
```

Swift
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

Go
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

Java
```java
import java.util.function.Consumer;

final class FormMediator
{
    private final Consumer<String> showTitle;
    private final Runnable markDirty;

    FormMediator(Consumer<String> showTitle, Runnable markDirty)
    {
        this.showTitle = showTitle;
        this.markDirty = markDirty;
    }

    void titleChanged(String title)
    {
        this.showTitle.accept(title);
        this.markDirty.run();
    }
}
```

Rust
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
Intent: Capture and restore object state without exposing internals.
When to use: Undo/redo, snapshots.
Avoid when: State is huge or storing is expensive.

C#
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

TypeScript
```ts
type Snapshot = {
    name: string;
    count: number;
};

class Editor
{
    public constructor(public name: string, public count: number)
    {
    }

    public save(): Snapshot
    {
        return { name: this.name, count: this.count };
    }

    public restore(snapshot: Snapshot): void
    {
        this.name = snapshot.name;
        this.count = snapshot.count;
    }
}
```

JavaScript
```js
class Editor
{
    constructor(name, count)
    {
        this.name = name;
        this.count = count;
    }

    save()
    {
        return { name: this.name, count: this.count };
    }

    restore(snapshot)
    {
        this.name = snapshot.name;
        this.count = snapshot.count;
    }
}
```

The snapshot stores an independent value. For complex documents, define deep-copy boundaries, versioning, and memory limits for retained snapshots.

Python
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EditorSnapshot:
    text: str

class TextEditor:
    def __init__(self, text: str) -> None:
        self.text = text

    def snapshot(self) -> EditorSnapshot:
        return EditorSnapshot(self.text)

    def restore(self, snapshot: EditorSnapshot) -> None:
        self.text = snapshot.text
```

Swift
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

Go
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

Java
```java
record EditorSnapshot(String text)
{
}

final class TextEditor
{
    String text;

    TextEditor(String text)
    {
        this.text = text;
    }

    EditorSnapshot snapshot()
    {
        return new EditorSnapshot(this.text);
    }

    void restore(EditorSnapshot snapshot)
    {
        this.text = snapshot.text();
    }
}
```

Rust
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
Intent: One-to-many dependency; publish/subscribe updates.
When to use: UI state updates, event systems.
Avoid when: Tight synchronous control needed.

C#
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

TypeScript
```ts
class Subject
{
    private readonly subscribers: Array<() => void> = [];

    public subscribe(action: () => void): void
    {
        this.subscribers.push(action);
    }

    public notify(): void
    {
        for (const subscriber of this.subscribers)
        {
            subscriber();
        }
    }
}
```

JavaScript
```js
class Subject
{
    constructor()
    {
        this.subscribers = [];
    }

    subscribe(action)
    {
        this.subscribers.push(action);
    }

    notify()
    {
        for (const subscriber of this.subscribers)
        {
            subscriber();
        }
    }
}
```

Retain the subscription token and unsubscribe at the owner's lifecycle boundary. The examples are confined to one execution context. Callback snapshots permit stable delivery during dispatch. Rust borrowing prevents subscription changes during its synchronous publish call.

Python
```python
from typing import Callable

class Publisher:
    def __init__(self) -> None:
        self._listeners: dict[int, Callable[[str], None]] = {}
        self._next_token = 0

    def subscribe(self, listener: Callable[[str], None]) -> int:
        self._next_token += 1
        self._listeners[self._next_token] = listener
        return self._next_token

    def unsubscribe(self, token: int) -> None:
        self._listeners.pop(token, None)

    def publish(self, message: str) -> None:
        for listener in tuple(self._listeners.values()):
            listener(message)
```

Swift
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

Go
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

Java
```java
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;

final class Publisher
{
    private final Map<Long, Consumer<String>> listeners = new LinkedHashMap<>();
    private long nextToken;

    long subscribe(Consumer<String> listener)
    {
        this.nextToken += 1;
        this.listeners.put(this.nextToken, listener);
        return this.nextToken;
    }

    void unsubscribe(long token)
    {
        this.listeners.remove(token);
    }

    void publish(String message)
    {
        for (Consumer<String> listener : List.copyOf(this.listeners.values()))
        {
            listener.accept(message);
        }
    }
}
```

Rust
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
Intent: Allow an object to alter behavior when its internal state changes.
When to use: Explicit state transitions (editor modes, workflows).
Avoid when: Simple if/else is enough.

C#
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

TypeScript
```ts
interface State
{
    handle(context: Context): void;
}

class ReadyState implements State
{
    public handle(context: Context): void
    {
        context.state = new BusyState();
    }
}

class BusyState implements State
{
    public handle(context: Context): void
    {
    }
}

class Context
{
    public state: State = new ReadyState();

    public request(): void
    {
        this.state.handle(this);
    }
}
```

JavaScript
```js
class ReadyState
{
    handle(context)
    {
        context.state = new BusyState();
    }
}

class BusyState
{
    handle(context)
    {
    }
}

class Context
{
    constructor()
    {
        this.state = new ReadyState();
    }

    request()
    {
        this.state.handle(this);
    }
}
```

Only valid transitions change state. Define retry, cancellation, and recovery states when the real workflow requires them.

Python
```python
from enum import Enum, auto

class JobState(Enum):
    IDLE = auto()
    RUNNING = auto()
    COMPLETE = auto()

class Job:
    def __init__(self) -> None:
        self.state = JobState.IDLE

    def start(self) -> None:
        if self.state is not JobState.IDLE:
            raise RuntimeError("Only an idle job can start.")
        self.state = JobState.RUNNING

    def complete(self) -> None:
        if self.state is not JobState.RUNNING:
            raise RuntimeError("Only a running job can complete.")
        self.state = JobState.COMPLETE
```

Swift
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

Go
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

Java
```java
enum JobState
{
    IDLE, RUNNING, COMPLETE
}

final class Job
{
    private JobState state = JobState.IDLE;

    JobState state()
    {
        return this.state;
    }

    void start()
    {
        if (this.state != JobState.IDLE)
        {
            throw new IllegalStateException("Only an idle job can start.");
        }
        this.state = JobState.RUNNING;
    }

    void complete()
    {
        if (this.state != JobState.RUNNING)
        {
            throw new IllegalStateException("Only a running job can complete.");
        }
        this.state = JobState.COMPLETE;
    }
}
```

Rust
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
Intent: Define a family of algorithms and make them interchangeable.
When to use: Multiple algorithms for same task (pricing, scoring).
Avoid when: Only one algorithm needed.

C#
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

TypeScript
```ts
interface PriceStrategy
{
    calc(basePrice: number): number;
}

class VipPrice implements PriceStrategy
{
    public calc(basePrice: number): number
    {
        return basePrice * 0.9;
    }
}
```

JavaScript
```js
class VipPrice
{
    calc(basePrice)
    {
        return basePrice * 0.9;
    }
}
```

Inject a function when one operation varies. Use a protocol, trait, or interface only when a wider contract earns the extra abstraction.

Python
```python
from typing import Callable

def format_text(text: str, strategy: Callable[[str], str]) -> str:
    return strategy(text)
```

Swift
```swift
func formatText(_ text: String, using strategy: (String) -> String) -> String
{
    return strategy(text)
}
```

Go
```go
package examples

type Formatter func(string) string

func FormatText(text string, strategy Formatter) string {
    return strategy(text)
}
```

Java
```java
import java.util.function.UnaryOperator;

final class TextFormatter
{
    static String format(String text, UnaryOperator<String> strategy)
    {
        return strategy.apply(text);
    }
}
```

Rust
```rust
fn format_text(text: &str, strategy: impl Fn(&str) -> String) -> String
{
    strategy(text)
}
```

### 22) Template Method
Intent: Define skeleton of an algorithm with steps overridden by subclasses.
When to use: Shared steps with variation.
Avoid when: Composition or Strategy is clearer.

C#
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

TypeScript
```ts
abstract class Importer
{
    public run(): void
    {
        this.read();
        this.validate();
        this.save();
    }

    protected abstract read(): void;

    protected validate(): void
    {
    }

    protected abstract save(): void;
}
```

JavaScript
```js
class Importer
{
    run()
    {
        this.read();
        this.validate();
        this.save();
    }

    read()
    {
        throw new Error("Override required");
    }

    validate()
    {
    }

    save()
    {
        throw new Error("Override required");
    }
}
```

A failed read or validation prevents saving. Java uses a final template method. Protocol and trait defaults do not enforce that same override restriction.

Python
```python
from abc import ABC, abstractmethod
from typing import final

class Importer(ABC):
    @abstractmethod
    def read(self) -> str: ...

    def validate(self, text: str) -> None:
        if not text:
            raise ValueError("Import content must not be empty.")

    @abstractmethod
    def save(self, text: str) -> None: ...

    @final
    def run(self) -> None:
        text = self.read()
        self.validate(text)
        self.save(text)
```

Swift
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

Go
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

Java
```java
abstract class Importer
{
    abstract String read();
    abstract void save(String text);

    void validate(String text)
    {
        if (text.isEmpty())
        {
            throw new IllegalArgumentException("Import content must not be empty.");
        }
    }

    final void run()
    {
        String text = read();
        validate(text);
        save(text);
    }
}
```

Rust
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
Intent: Add new operations to object structures without modifying them.
When to use: Stable object structure with many operations.
Avoid when: Structure changes frequently or overhead is high.

C#
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

TypeScript
```ts
interface Visitor
{
    visitA(node: NodeA): void;
    visitB(node: NodeB): void;
}

interface Node
{
    accept(visitor: Visitor): void;
}

class NodeA implements Node
{
    public accept(visitor: Visitor): void
    {
        visitor.visitA(this);
    }
}
```

JavaScript
```js
class NodeA
{
    accept(visitor)
    {
        visitor.visitA(this);
    }
}
```

Swift and Rust use exhaustive enum dispatch for a closed set of values. Class-based visitors suit a stable type hierarchy that gains new operations.

Python
```python
from dataclasses import dataclass
from typing import Protocol

class ValueVisitor(Protocol):
    def visit_text(self, value: str) -> str: ...
    def visit_number(self, value: int) -> str: ...

@dataclass(frozen=True)
class TextValue:
    value: str

    def accept(self, visitor: ValueVisitor) -> str:
        return visitor.visit_text(self.value)

@dataclass(frozen=True)
class NumberValue:
    value: int

    def accept(self, visitor: ValueVisitor) -> str:
        return visitor.visit_number(self.value)

class RenderVisitor:
    def visit_text(self, value: str) -> str:
        return "text:" + value

    def visit_number(self, value: int) -> str:
        return "number:" + str(value)
```

Swift
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

Go
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

Java
```java
interface ValueVisitor
{
    String visitText(String value);
    String visitNumber(int value);
}

record TextValue(String value)
{
    String accept(ValueVisitor visitor)
    {
        return visitor.visitText(this.value);
    }
}

record NumberValue(int value)
{
    String accept(ValueVisitor visitor)
    {
        return visitor.visitNumber(this.value);
    }
}

final class RenderVisitor implements ValueVisitor
{
    public String visitText(String value)
    {
        return "text:" + value;
    }

    public String visitNumber(int value)
    {
        return "number:" + value;
    }
}
```

Rust
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

---

## Usage Guidance in This Codebase

Choose a pattern for the problem, then express it through the language's normal constructs.
Swift protocols, Go interfaces and functions, Rust traits and enums, and Java interfaces need not reproduce a C# class hierarchy.
Prefer a direct function or type when a pattern adds no useful separation.
- Prefer Strategy for pluggable AI providers, pricing, validation, or formatting.
- Use Factory/Abstract Factory when supporting multiple backend providers with consistent interfaces.
- Use Command and Memento for undo/redo and user actions that require audit trails.
- Use Observer for UI updates and real-time collaboration events.
- Use Adapter/Facade for third-party or legacy API integration.
- Use Decorator for optional behaviors like logging, caching, instrumentation.
### Relationship to Martin Fowler Refactoring Techniques

When applying a GoF pattern in this codebase, use the corresponding Fowler refactoring technique to get there safely:

| GoF Pattern | Primary Fowler Technique | When to Apply |
|-------------|-------------------------|---------------|
| Strategy | Replace Conditional with Polymorphism | A switch/if-else dispatches to type-specific logic (providers, settings, permissions). |
| Facade | Extract Class | A service exceeds 500 lines or mixes HTTP/DB/business concerns. |
| Adapter | Extract Interface + Extract Class | Code is tightly coupled to a third-party API (Auth0, AI providers). |
| Decorator | Extract Method + Pull Up Method | Cross-cutting logic (logging, audit, caching) is duplicated in multiple locations. |
| State | Replace Type Code with Class | String constants represent lifecycle states with transition rules. |
| Composite | Encapsulate Collection + Replace Type Code with Class | `Dictionary<string, object>` or `List<object>` models structured, typed data. |
| Command | Extract Class | A method both parses input and executes side effects (violation of SRP). |

### Migration Approach

Per `MIGRATIONS.md`, every pattern application follows the Golden Loop:

1. **Baseline:** Ensure passing tests cover the code being refactored. Fill gaps to =90%.
2. **Refactor:** Apply the pattern using the Fowler technique. Keep logic 1:1 initially.
3. **Verify:** Run all tests. Fix the refactored code (not the tests) until they pass.
4. **Polish:** Make idiomatic improvements. Run tests after each change.
5. **Commit:** One refactoring per commit with a conventional message.

## Balance Checklist

Before applying a pattern, ask:
- Does this reduce complexity or just add ceremony?
- Will another developer recognise this pattern quickly?
- Is there a smaller, clearer alternative (Extract Method before Extract Class)?
- Does the product roadmap justify the extensibility this pattern provides?
- Are we complying with `CODING_STYLE.md` (max 30-line methods, Allman braces where valid, 4-space indentation, one type per file)?
- Have we established a test baseline per `MIGRATIONS.md` Phase 1?
