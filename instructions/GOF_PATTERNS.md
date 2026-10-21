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
- Language links: examples in the selected programming-language guide.

The examples isolate each pattern. They do not prescribe a new framework or replace the project's existing APIs.
When a language example contains multiple top-level types, put each type in its own file in production.
Keep a type's extensions or nested implementation types together only when that placement has a clear purpose.
Use four spaces, no tabs, a 120-character line limit, and Allman braces wherever the grammar permits them.
Apply the syntax exceptions in the selected language guide.
Connect real UI controls, persistence, and logging at the application boundary.

---

## Creational Patterns

### 1) Abstract Factory

Intent: Create families of related objects without specifying concrete classes.
When to use: Interchangeable product families with compatibility constraints.
Avoid when: Only one product family or no compatibility constraints.

The language examples use product labels to show compatible families without UI dependencies. Real factories return the project's control interfaces.

Language examples: [C#](csharp/CSHARP.md#1-abstract-factory), [TypeScript](typescript/TYPESCRIPT.md#1-abstract-factory), [JavaScript](javascript/JAVASCRIPT.md#1-abstract-factory), [Python](python/PYTHON.md#1-abstract-factory), [Swift](swift/SWIFT.md#1-abstract-factory), [Go](go/GO.md#1-abstract-factory), [Java](java/JAVA.md#1-abstract-factory), [Rust](rust/RUST.md#1-abstract-factory).

### 2) Builder

Intent: Construct complex objects step-by-step with a fluent API.
When to use: Many optional fields or required ordering.
Avoid when: A simple constructor or object literal is enough.

The example builders return an independent string value. For mutable report objects, copy state or consume the builder to prevent later mutation.

Language examples: [C#](csharp/CSHARP.md#2-builder), [TypeScript](typescript/TYPESCRIPT.md#2-builder), [JavaScript](javascript/JAVASCRIPT.md#2-builder), [Python](python/PYTHON.md#2-builder), [Swift](swift/SWIFT.md#2-builder), [Go](go/GO.md#2-builder), [Java](java/JAVA.md#2-builder), [Rust](rust/RUST.md#2-builder).

### 3) Factory Method

Intent: Let subclasses decide which class to instantiate.
When to use: Creation varies by subclass or runtime type selection.
Avoid when: Only one concrete type exists.

Python and Java use class-based creation hooks. Swift and Rust use protocol or trait defaults. Go injects a factory function.

Language examples: [C#](csharp/CSHARP.md#3-factory-method), [TypeScript](typescript/TYPESCRIPT.md#3-factory-method), [JavaScript](javascript/JAVASCRIPT.md#3-factory-method), [Python](python/PYTHON.md#3-factory-method), [Swift](swift/SWIFT.md#3-factory-method), [Go](go/GO.md#3-factory-method), [Java](java/JAVA.md#3-factory-method), [Rust](rust/RUST.md#3-factory-method).

### 4) Prototype

Intent: Create new objects by cloning existing ones.
When to use: Expensive creation; need variations of a configured object.
Avoid when: Cloning is complex or error-prone.

Copy mutable owned state when independent edits are required. Swift and Rust value copies, Go slice copies, and Java defensive copies express that contract.

Language examples: [C#](csharp/CSHARP.md#4-prototype), [TypeScript](typescript/TYPESCRIPT.md#4-prototype), [JavaScript](javascript/JAVASCRIPT.md#4-prototype), [Python](python/PYTHON.md#4-prototype), [Swift](swift/SWIFT.md#4-prototype), [Go](go/GO.md#4-prototype), [Java](java/JAVA.md#4-prototype), [Rust](rust/RUST.md#4-prototype).

### 5) Singleton

Intent: Ensure a class has one instance and a global access point.
When to use: A shared, stateless service or cache with strict single-instance semantics.
Avoid when: You need multiple configurations or test isolation; prefer DI.

These instances are process-local. Prefer injected settings when tests need isolation. Protect mutable shared state rather than assuming singleton construction makes it safe.

Language examples: [C#](csharp/CSHARP.md#5-singleton), [TypeScript](typescript/TYPESCRIPT.md#5-singleton), [JavaScript](javascript/JAVASCRIPT.md#5-singleton), [Python](python/PYTHON.md#5-singleton), [Swift](swift/SWIFT.md#5-singleton), [Go](go/GO.md#5-singleton), [Java](java/JAVA.md#5-singleton), [Rust](rust/RUST.md#5-singleton).

## Structural Patterns

### 6) Adapter

Intent: Convert one interface to another clients expect.
When to use: Integrating legacy or third-party APIs.
Avoid when: You can change the client or use native interface directly.

The adapter translates the boundary contract and delegates once. Preserve real encoding and failure rules instead of concealing them.

Language examples: [C#](csharp/CSHARP.md#6-adapter), [TypeScript](typescript/TYPESCRIPT.md#6-adapter), [JavaScript](javascript/JAVASCRIPT.md#6-adapter), [Python](python/PYTHON.md#6-adapter), [Swift](swift/SWIFT.md#6-adapter), [Go](go/GO.md#6-adapter), [Java](java/JAVA.md#6-adapter), [Rust](rust/RUST.md#6-adapter).

### 7) Bridge

Intent: Separate abstraction from implementation so both can vary.
When to use: Multiple orthogonal dimensions (e.g., UI type and theme).
Avoid when: Only one dimension exists.

The shape owns geometry and receives a renderer. More shapes and rendering backends can vary independently without a subclass for each combination.

Language examples: [C#](csharp/CSHARP.md#7-bridge), [TypeScript](typescript/TYPESCRIPT.md#7-bridge), [JavaScript](javascript/JAVASCRIPT.md#7-bridge), [Python](python/PYTHON.md#7-bridge), [Swift](swift/SWIFT.md#7-bridge), [Go](go/GO.md#7-bridge), [Java](java/JAVA.md#7-bridge), [Rust](rust/RUST.md#7-bridge).

### 8) Composite

Intent: Treat individual objects and compositions uniformly.
When to use: Tree structures with leaf and container nodes.
Avoid when: Simple flat lists.

The uniform node or enum gives leaves and branches the same traversal contract. Bound recursion and reject cycles when loading external trees.

Language examples: [C#](csharp/CSHARP.md#8-composite), [TypeScript](typescript/TYPESCRIPT.md#8-composite), [JavaScript](javascript/JAVASCRIPT.md#8-composite), [Python](python/PYTHON.md#8-composite), [Swift](swift/SWIFT.md#8-composite), [Go](go/GO.md#8-composite), [Java](java/JAVA.md#8-composite), [Rust](rust/RUST.md#8-composite).

### 9) Decorator

Intent: Add responsibilities dynamically without subclassing.
When to use: Optional behaviors layered at runtime (logging, caching).
Avoid when: Behavior is fixed or class hierarchy is simpler.

A function wrapper is sufficient when only behavior changes. Use a richer interface when resource ownership or several operations require it.

Language examples: [C#](csharp/CSHARP.md#9-decorator), [TypeScript](typescript/TYPESCRIPT.md#9-decorator), [JavaScript](javascript/JAVASCRIPT.md#9-decorator), [Python](python/PYTHON.md#9-decorator), [Swift](swift/SWIFT.md#9-decorator), [Go](go/GO.md#9-decorator), [Java](java/JAVA.md#9-decorator), [Rust](rust/RUST.md#9-decorator).

### 10) Facade

Intent: Provide a simplified API over a complex subsystem.
When to use: Complex modules with many steps; reduce coupling.
Avoid when: Subsystem is already small.

The facade orders read, format, and write operations. Failures propagate to the caller, and a failed read or format must prevent the write.

Language examples: [C#](csharp/CSHARP.md#10-facade), [TypeScript](typescript/TYPESCRIPT.md#10-facade), [JavaScript](javascript/JAVASCRIPT.md#10-facade), [Python](python/PYTHON.md#10-facade), [Swift](swift/SWIFT.md#10-facade), [Go](go/GO.md#10-facade), [Java](java/JAVA.md#10-facade), [Rust](rust/RUST.md#10-facade).

### 11) Flyweight

Intent: Share common state to reduce memory usage.
When to use: Huge numbers of similar objects.
Avoid when: State is mostly unique or mutation makes sharing risky.

The factory shares immutable icons. These caches are confined to one execution context. Define synchronization, cache bounds, and eviction for production.

Language examples: [C#](csharp/CSHARP.md#11-flyweight), [TypeScript](typescript/TYPESCRIPT.md#11-flyweight), [JavaScript](javascript/JAVASCRIPT.md#11-flyweight), [Python](python/PYTHON.md#11-flyweight), [Swift](swift/SWIFT.md#11-flyweight), [Go](go/GO.md#11-flyweight), [Java](java/JAVA.md#11-flyweight), [Rust](rust/RUST.md#11-flyweight).

### 12) Proxy

Intent: Control access to an object (lazy load, security, caching).
When to use: Expensive objects or access control.
Avoid when: Direct access is safe and simple.

Authorize every protected read before delegation. Supply trusted resource-scoped authorization from the server or local security boundary, not a UI visibility flag.

Language examples: [C#](csharp/CSHARP.md#12-proxy), [TypeScript](typescript/TYPESCRIPT.md#12-proxy), [JavaScript](javascript/JAVASCRIPT.md#12-proxy), [Python](python/PYTHON.md#12-proxy), [Swift](swift/SWIFT.md#12-proxy), [Go](go/GO.md#12-proxy), [Java](java/JAVA.md#12-proxy), [Rust](rust/RUST.md#12-proxy).

## Behavioral Patterns

### 13) Chain of Responsibility

Intent: Pass a request through a chain until handled.
When to use: Pipeline of handlers (validation, policy checks).
Avoid when: A single, fixed handler suffices.

Stop at the first validation failure. Define whether later checks depend on earlier checks before changing their order.

Language examples: [C#](csharp/CSHARP.md#13-chain-of-responsibility), [TypeScript](typescript/TYPESCRIPT.md#13-chain-of-responsibility), [JavaScript](javascript/JAVASCRIPT.md#13-chain-of-responsibility), [Python](python/PYTHON.md#13-chain-of-responsibility), [Swift](swift/SWIFT.md#13-chain-of-responsibility), [Go](go/GO.md#13-chain-of-responsibility), [Java](java/JAVA.md#13-chain-of-responsibility), [Rust](rust/RUST.md#13-chain-of-responsibility).

### 14) Command

Intent: Encapsulate a request as an object (undo/redo, queues).
When to use: Undo, retries, queues, or logs.
Avoid when: Simple direct method call.

The invoker pairs execution and undo and serializes changes to the target. These examples do not provide an undo history or concurrent editing protocol.

Language examples: [C#](csharp/CSHARP.md#14-command), [TypeScript](typescript/TYPESCRIPT.md#14-command), [JavaScript](javascript/JAVASCRIPT.md#14-command), [Python](python/PYTHON.md#14-command), [Swift](swift/SWIFT.md#14-command), [Go](go/GO.md#14-command), [Java](java/JAVA.md#14-command), [Rust](rust/RUST.md#14-command).

### 15) Interpreter

Intent: Define a grammar and interpret sentences in that language.
When to use: Simple DSLs (filters, rules).
Avoid when: Use a real parser or library instead.

Interpret a typed expression tree rather than executing source text. Bound depth and validate numeric overflow when accepting external expressions.

Language examples: [C#](csharp/CSHARP.md#15-interpreter), [TypeScript](typescript/TYPESCRIPT.md#15-interpreter), [JavaScript](javascript/JAVASCRIPT.md#15-interpreter), [Python](python/PYTHON.md#15-interpreter), [Swift](swift/SWIFT.md#15-interpreter), [Go](go/GO.md#15-interpreter), [Java](java/JAVA.md#15-interpreter), [Rust](rust/RUST.md#15-interpreter).

### 16) Iterator

Intent: Traverse a collection without exposing its representation.
When to use: Custom collections; controlled traversal.
Avoid when: Native iterators already exist and suffice.

The iterator exposes exhaustion explicitly. Keep traversal state private, and define mutation behavior if the underlying collection can change.

Language examples: [C#](csharp/CSHARP.md#16-iterator), [TypeScript](typescript/TYPESCRIPT.md#16-iterator), [JavaScript](javascript/JAVASCRIPT.md#16-iterator), [Python](python/PYTHON.md#16-iterator), [Swift](swift/SWIFT.md#16-iterator), [Go](go/GO.md#16-iterator), [Java](java/JAVA.md#16-iterator), [Rust](rust/RUST.md#16-iterator).

### 17) Mediator

Intent: Centralize complex communications between objects.
When to use: Many-to-many object interactions.
Avoid when: Only a few direct relationships.

The mediator coordinates related actions through injected callbacks. Keep business rules in services when coordination grows beyond this UI interaction.

Language examples: [C#](csharp/CSHARP.md#17-mediator), [TypeScript](typescript/TYPESCRIPT.md#17-mediator), [JavaScript](javascript/JAVASCRIPT.md#17-mediator), [Python](python/PYTHON.md#17-mediator), [Swift](swift/SWIFT.md#17-mediator), [Go](go/GO.md#17-mediator), [Java](java/JAVA.md#17-mediator), [Rust](rust/RUST.md#17-mediator).

### 18) Memento

Intent: Capture and restore object state without exposing internals.
When to use: Undo/redo, snapshots.
Avoid when: State is huge or storing is expensive.

The snapshot stores an independent value. For complex documents, define deep-copy boundaries, versioning, and memory limits for retained snapshots.

Language examples: [C#](csharp/CSHARP.md#18-memento), [TypeScript](typescript/TYPESCRIPT.md#18-memento), [JavaScript](javascript/JAVASCRIPT.md#18-memento), [Python](python/PYTHON.md#18-memento), [Swift](swift/SWIFT.md#18-memento), [Go](go/GO.md#18-memento), [Java](java/JAVA.md#18-memento), [Rust](rust/RUST.md#18-memento).

### 19) Observer

Intent: One-to-many dependency; publish/subscribe updates.
When to use: UI state updates, event systems.
Avoid when: Tight synchronous control needed.

Retain the subscription token and unsubscribe at the owner's lifecycle boundary. The examples are confined to one execution context. Callback snapshots permit stable delivery during dispatch. Rust borrowing prevents subscription changes during its synchronous publish call.

Language examples: [C#](csharp/CSHARP.md#19-observer), [TypeScript](typescript/TYPESCRIPT.md#19-observer), [JavaScript](javascript/JAVASCRIPT.md#19-observer), [Python](python/PYTHON.md#19-observer), [Swift](swift/SWIFT.md#19-observer), [Go](go/GO.md#19-observer), [Java](java/JAVA.md#19-observer), [Rust](rust/RUST.md#19-observer).

### 20) State

Intent: Allow an object to alter behavior when its internal state changes.
When to use: Explicit state transitions (editor modes, workflows).
Avoid when: Simple if/else is enough.

Only valid transitions change state. Define retry, cancellation, and recovery states when the real workflow requires them.

Language examples: [C#](csharp/CSHARP.md#20-state), [TypeScript](typescript/TYPESCRIPT.md#20-state), [JavaScript](javascript/JAVASCRIPT.md#20-state), [Python](python/PYTHON.md#20-state), [Swift](swift/SWIFT.md#20-state), [Go](go/GO.md#20-state), [Java](java/JAVA.md#20-state), [Rust](rust/RUST.md#20-state).

### 21) Strategy

Intent: Define a family of algorithms and make them interchangeable.
When to use: Multiple algorithms for same task (pricing, scoring).
Avoid when: Only one algorithm needed.

Inject a function when one operation varies. Use a protocol, trait, or interface only when a wider contract earns the extra abstraction.

Language examples: [C#](csharp/CSHARP.md#21-strategy), [TypeScript](typescript/TYPESCRIPT.md#21-strategy), [JavaScript](javascript/JAVASCRIPT.md#21-strategy), [Python](python/PYTHON.md#21-strategy), [Swift](swift/SWIFT.md#21-strategy), [Go](go/GO.md#21-strategy), [Java](java/JAVA.md#21-strategy), [Rust](rust/RUST.md#21-strategy).

### 22) Template Method

Intent: Define skeleton of an algorithm with steps overridden by subclasses.
When to use: Shared steps with variation.
Avoid when: Composition or Strategy is clearer.

A failed read or validation prevents saving. Java uses a final template method. Protocol and trait defaults do not enforce that same override restriction.

Language examples: [C#](csharp/CSHARP.md#22-template-method), [TypeScript](typescript/TYPESCRIPT.md#22-template-method), [JavaScript](javascript/JAVASCRIPT.md#22-template-method), [Python](python/PYTHON.md#22-template-method), [Swift](swift/SWIFT.md#22-template-method), [Go](go/GO.md#22-template-method), [Java](java/JAVA.md#22-template-method), [Rust](rust/RUST.md#22-template-method).

### 23) Visitor

Intent: Add new operations to object structures without modifying them.
When to use: Stable object structure with many operations.
Avoid when: Structure changes frequently or overhead is high.

Swift and Rust use exhaustive enum dispatch for a closed set of values. Class-based visitors suit a stable type hierarchy that gains new operations.

Language examples: [C#](csharp/CSHARP.md#23-visitor), [TypeScript](typescript/TYPESCRIPT.md#23-visitor), [JavaScript](javascript/JAVASCRIPT.md#23-visitor), [Python](python/PYTHON.md#23-visitor), [Swift](swift/SWIFT.md#23-visitor), [Go](go/GO.md#23-visitor), [Java](java/JAVA.md#23-visitor), [Rust](rust/RUST.md#23-visitor).

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

Per `instructions/MIGRATIONS.md`, every pattern application follows the Golden Loop:

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
- Are we complying with `instructions/CODING_STYLE.md` (max 30-line methods, Allman braces where valid, 4-space indentation, one type per file)?
- Have we established a test baseline per `instructions/MIGRATIONS.md` Phase 1?
