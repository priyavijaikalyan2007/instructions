<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 19139cb0-1a0e-475a-96ee-e6658d75aa16
Created: 2026
-->

<!-- AGENT: JavaScript conventions and task examples; load only when this language is in scope. -->

# JavaScript instructions

Read this guide when the task changes JavaScript source or its language-specific build and test configuration.
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

Read by task: [Naming](#naming), [File organization](#file-organization), [Async style](#consistent-async-style), [Comments](#comments), [Navigation markers](#navigation-markers), [Testing](../frontend/FRONTEND.md#browser-testing), [Test examples](#test-examples), [Coverage](#coverage), [Logging](#logging), [Performance examples](#performance-examples), [Design patterns](#design-patterns).

For server-side Google Apps Script, also read [APPS_SCRIPT.md](../apps-script/APPS_SCRIPT.md).
Its runtime restrictions apply to syntax, dependencies, host callbacks, and service calls.
Browser-side HTML-service code follows browser JavaScript rules rather than server runtime restrictions.

## Naming

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `ErrorDialog` |
| Functions | camelCase | `showErrorDialog` |
| Methods | camelCase | `renderContent` |
| Properties | camelCase | `errorCode` |
| Variables | camelCase | `containerElement` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private Members | #camelCase or _camelCase, subject to runtime support | `#container` or `_container` |

## File organization

Use one top-level type per file, such as `order.js`, `order-store.js`, and `order-status.js`.

## Consistent async style

- **"One style, everywhere."**
- If the codebase uses `async/await`, use it exclusively. Do not mix `Promise.then()` chains with `async/await` in the same component.

## Comments

Use JSDoc for public functions and complex contracts. Explain parameters, return values, side effects, and expected failures.
Use ordinary comments for navigation markers rather than publishing them as API documentation.

## Navigation markers

Use `//` or `/* ... */` comments with the standard fields in [MARKERS.md](../MARKERS.md).
Place file headers before implementation code. Preserve directives and documentation attachment.

## Testing

See [FRONTEND.md](../frontend/FRONTEND.md#browser-testing).

## Test examples

### Test Parallelization

```javascript
// Jest parallel configuration
module.exports = {
  maxWorkers: '50%',  // Use half of available CPU cores
};
```

## Coverage

- Use Jest's built-in coverage or c8 for Node.js
- Configure in jest.config.js: `collectCoverage: true`

```bash
# TypeScript/JavaScript
npm test -- --coverage
```

## Logging

Use the declared browser or server logger and preserve useful error context.

## Performance examples

### 2.1 Loading & Bundle Size

```javascript
// Load heavy charting library only when needed
if (showChart) {
    const { renderChart } = await import('./modules/charting.js');
    renderChart();
}
```

## Design patterns

### 1) Abstract Factory

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#1-abstract-factory).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#2-builder).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#3-factory-method).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#4-prototype).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#5-singleton).

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

### 6) Adapter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#6-adapter).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#7-bridge).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#8-composite).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#9-decorator).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#10-facade).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#11-flyweight).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#12-proxy).

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

### 13) Chain of Responsibility

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#13-chain-of-responsibility).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#14-command).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#15-interpreter).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#16-iterator).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#17-mediator).

```js
class DialogMediator
{
    notify(sender, evt)
    {
    }
}
```

### 18) Memento

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#18-memento).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#19-observer).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#20-state).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#21-strategy).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#22-template-method).

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

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#23-visitor).

```js
class NodeA
{
    accept(visitor)
    {
        visitor.visitA(this);
    }
}
```


## Security

Apply [general security](../SECURITY_GUIDELINES.md) in browser and server JavaScript.
Do not execute external, user-provided, or model-generated strings through `eval`, `Function`, or string-valued timers.
Do not treat imported JSON as executable JavaScript. Validate parsed objects against an explicit contract.
Reject dangerous merge keys such as `__proto__`, `constructor`, and `prototype` when accepting arbitrary object keys.
Prefer `Map` or `Object.create(null)` for dictionaries that do not need prototype inheritance.

For plain text, use DOM text APIs:

```javascript
// SECURITY: Content remains text even when it includes markup.
const label = document.createElement("span");
label.textContent = externalLabel;
container.appendChild(label);
```

Do not pass external content to `innerHTML`, `outerHTML`, `insertAdjacentHTML`, or `document.write` without the required safe transformation.
Use a maintained sanitizer for intentional rich HTML. Never build an HTML sanitizer from regular expressions.
See [OWASP DOM XSS prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html).

Keep renderer output encoding enabled. Framework escape hatches such as React's `dangerouslySetInnerHTML` require reviewed rich-content handling.
Sanitize after Markdown conversion and before the HTML sink. Do not mutate sanitized markup through unsafe concatenation.
Validate URL schemes and intended destinations separately. Escaping HTML does not make a `javascript:` URL safe.
Use Trusted Types where supported as additional sink enforcement, not as a substitute for a safe policy.
See [OWASP XSS prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html).

Do not store service secrets in browser bundles or assume local storage protects tokens from injected scripts.
Use the project's session design, including protected cookies where appropriate.
Do not log clipboard data, tokens, or sensitive object graphs.
JavaScript provides no general reliable zeroing or page-locking guarantee for strings and managed objects.
