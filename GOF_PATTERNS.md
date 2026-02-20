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
- C# / TypeScript / JavaScript: minimal examples.

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

---

## Usage Guidance in This Codebase
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
- Are we complying with `CODING_STYLE.md` (max 30-line methods, Allman braces, one type per file)?
- Have we established a test baseline per `MIGRATIONS.md` Phase 1?
