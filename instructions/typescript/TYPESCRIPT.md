<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 0283ca94-4c88-4806-9b1c-d22876bffd64
Created: 2026
-->

<!-- AGENT: TypeScript conventions and task examples; load only when this language is in scope. -->

# TypeScript instructions

Read this guide when the task changes TypeScript source or its language-specific build and test configuration.
Examples in instruction documents do not make a language part of the consuming project.
Start with references, formatting, naming, and file organization when those sections exist.
Read task sections as needed. Read pattern examples only for patterns selected during planning.
Shared policies remain in the topic guides. Read only the topics that apply to the task.
Do not weaken a shared requirement because this guide omits it.

Also read [JAVASCRIPT.md](../javascript/JAVASCRIPT.md) for shared naming, runtime, testing, and coverage rules.

Shared rules: [Style](../CODING_STYLE.md), [Comments](../COMMENTING.md), [Markers](../MARKERS.md), [Testing](../TESTING.md), [Logging](../LOGGING.md), [Performance](../PERFORMANCE.md), [Patterns](../GOF_PATTERNS.md).

Apply [shared style](../CODING_STYLE.md), including Allman braces, four-space indentation, and one type per file.
Use only the grammar exceptions stated in this guide.
If an example shows several top-level types, put each type in its own file in production.
Examples may omit surrounding project types or test fixtures. Use the repository's configured dependencies and contracts.

Read by task: [References](#references), [Style examples](#style-examples), [Naming](#naming), [File organization](#file-organization), [Language constructs](#language-constructs), [Comments](#comments), [Comment examples](#comment-examples), [Navigation markers](#navigation-markers), [Marker examples](#marker-examples), [Test examples](#test-examples), [Logging examples](#logging-examples), [Migration from JavaScript](#migration-from-javascript), [Design patterns](#design-patterns).

## References

1. Follow [ts.dev](https://ts.dev/style/#identifiers)
2. Follow [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
3. Follow [Unofficial Typescript Lang](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
4. Apply the overrides in this document

## Style examples

### Brace Style

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

```typescript
// Bad
if (a && b || c)

// Good
if ((a && b) || c)
```

### Whitespace for Readability

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

### Nesting Limits

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

### Early Returns (Guard Clauses)

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

### Constraints and Invariants

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

### Explicit Code Style

```typescript
// Bad — clever but obscure
const result = (b << 4 & b << 8) | (b >> 2);

// Good — explicit and clear
const shift4Bits = b << 4;
const shift8Bits = b << 8;
const divideBy4 = b >> 2;
const mergedBits = (shift4Bits & shift8Bits) | divideBy4;
```

## Naming

Use [JavaScript naming](../javascript/JAVASCRIPT.md#naming) for classes, functions, properties, constants, and private members.

| Element | Convention | Example |
|---------|------------|---------|
| Interfaces | PascalCase (no I prefix) | `ErrorDialogOptions` |
| Type Aliases | PascalCase | `DialogAction` |
| Enums | PascalCase | `DialogType.Error` |

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

## File organization

`order.ts`, `order-store.ts`, and `order-status.ts`.

## Language constructs

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

## Comments

Use JSDoc for functions and complex types:

```typescript
/**
 * Displays a structured error dialog using Bootstrap's modal.
 *
 * @param containerId - The DOM element ID where the modal will be injected
 * @param options - The error information to display
 * @returns void
 */
function showErrorDialog(containerId: string, options: ErrorDialogOptions): void {
}

/**
 * Debounces a function call to prevent rapid repeated execution.
 *
 * @param fn - The function to debounce
 * @param delayMs - Milliseconds to wait before executing
 * @returns A debounced version of the input function
 */
function debounce<T extends (...args: unknown[]) => void>(
  fn: T,
  delayMs: number
): (...args: Parameters<T>) => void
```

## Comment examples

### 3.1 What, Why — Not How

```typescript
// BAD: How (redundant with code)
// Loop through items and check if element exists
for (const item of items)
{
    if (document.getElementById(item.id)) { ... }
}

// GOOD: What and Why
// Remove stale dialog elements — components may leave orphaned modals after errors
for (const item of items)
{
    if (document.getElementById(item.id)) { ... }
}
```

### 3.2 Standard Annotations

```typescript
// TODO: Add keyboard navigation for arrow keys (spec section 3.2)
// BUGFIX: Chrome 120 requires explicit tabindex for focus — see issue #42
// HACK: Bootstrap 5.3 modal backdrop z-index conflict — revisit after upgrade
```

### 3.3 Agent Markers

```typescript
// @agent:test — Cover edge case where container ID is null
// @agent:security — Verify this does not inject unsanitised HTML
// @agent:review — Complex selector logic, needs human verification
// @agent:refactor — Candidate for extraction once more components exist
```

### 3.4 Section Headers

```typescript
// ============================================================================
// PUBLIC API
// ============================================================================

// ============================================================================
// PRIVATE HELPERS
// ============================================================================

// ============================================================================
// EVENT HANDLERS
// ============================================================================
```

### 6.2 Obvious Code

```typescript
// BAD: States the obvious
// Increment the counter
counter++;

// Set the title text
titleElement.textContent = title;

// Return the result
return result;
```

## Navigation markers

```typescript
/*
 * ----------------------------------------------------------------------------
 * ⚓ COMPONENT: [ComponentName]
 * 📜 PURPOSE: [Concise description of what this file does]
 * 🔗 RELATES: [Reference to related files or specs, e.g., [[LiterateErrors]]]
 * ⚡ FLOW: [Inbound Caller] -> [This Component] -> [Outbound Dependency]
 * ----------------------------------------------------------------------------
 */
```

```typescript
/*
 * ----------------------------------------------------------------------------
 * ⚓ COMPONENT: ErrorDialog
 * 📜 PURPOSE: Renders literate error messages in a Bootstrap 5 modal dialog.
 * 🔗 RELATES: [[LiterateErrors]], [[ErrorDialogSpec]]
 * ⚡ FLOW: [Consumer App] -> [showErrorDialog()] -> [Bootstrap Modal API]
 * ----------------------------------------------------------------------------
 */
export function showErrorDialog(containerId: string, options: LiterateError): void
{
    // ...
}
/*
 * ----------------------------------------------------------------------------
 * ⚓ COMPONENT: UserProfileController
 * 📜 PURPOSE: Handles fetching and updating user profile settings and avatars.
 * 🔗 RELATES: [[UserProfileService]], [[AvatarUpload]]
 * ⚡ FLOW: [Router] -> [This] -> [Database]
 * 🛡️ SECURITY: Requires 'AuthenticatedUser' policy.
 * ----------------------------------------------------------------------------
 */
export class UserProfileController { ... }
```

## Marker examples

### 3. Global Concept Registry

```typescript
// Renders the error message following the [[LiterateErrors]] guidelines.
function renderErrorMessage(container: HTMLElement, error: LiterateError): void
{
    // ...
}
```

### 4. Section Markers (Long Files)

```typescript
// ============================================================================
// PUBLIC API
// ============================================================================

// ============================================================================
// PRIVATE HELPERS
// ============================================================================

// ============================================================================
// EVENT HANDLERS
// ============================================================================
```

## Test examples

### Test Factories and Builders

```typescript
// Builder pattern for complex objects
class OrderBuilder {
  private order: Partial<Order> = {
    id: crypto.randomUUID(),
    status: 'pending',
    items: [],
    createdAt: new Date()
  };

  withItems(items: OrderItem[]): this {
    this.order.items = items;
    return this;
  }

  withStatus(status: OrderStatus): this {
    this.order.status = status;
    return this;
  }

  forCustomer(customerId: string): this {
    this.order.customerId = customerId;
    return this;
  }

  build(): Order {
    return this.order as Order;
  }
}

// Usage in tests
const order = new OrderBuilder()
  .forCustomer('cust-123')
  .withItems([itemA, itemB])
  .withStatus('confirmed')
  .build();
```

### Accessibility Testing

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('registration page is accessible', async ({ page }) => {
  await page.goto('/register');

  const results = await new AxeBuilder({ page }).analyze();

  expect(results.violations).toEqual([]);
});
```

## Logging examples

```ts
import { AsyncLocalStorage } from 'node:async_hooks';
import * as winston from 'winston';

const asyncLocalStorage = new AsyncLocalStorage<Map<string, string>>();
const logger = winston.createLogger(
{
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.printf(({ timestamp, level, message }) =>
        {
            const store = asyncLocalStorage.getStore();
            const correlationID = store?.get('correlationId') ?? 'no-context';
            const tenantID = store?.get('tenantId') ?? 'unknown';
            return `${timestamp} [${correlationID}] [${tenantID}] ${level}: ${message}`;
        })
    ),
    transports: [new winston.transports.Console()]
});

function sensitiveOperation(input: string): void
{
    // SECURITY: Log approved branch metadata rather than the sensitive input.
    logger.debug("Entering sensitiveOperation");
    const condition = input.length > 5;
    logger.debug(`Evaluating condition: input.length > 5 is ${condition}`);
    if (condition)
    {
        logger.debug("Branch: Long input path");
    }
    else
    {
        logger.debug("Branch: Short input path");
    }
    logger.debug("Exiting sensitiveOperation");
}

function requestHandler(): void
{
    const store = new Map<string, string>();
    store.set('correlationId', 'uuid-1234-5678');
    store.set('tenantId', 'tenant-A');
    asyncLocalStorage.run(store, () =>
    {
        sensitiveOperation("secretData");
    });
}

requestHandler();
```

---

## Migration from JavaScript

1.  **Phase 1**:
    *   User asks to migrate `utils.js`.
    *   *Agent Action*: Check for `utils.test.js`. If missing, create it. Run `jest utils.test.js` to confirm it passes.

2.  **Phase 2**:
    *   *Agent Action*: Rename `utils.js` to `utils.ts`. Add type annotations (`any` is acceptable temporarily if strictness causes blocks, but aim for specific types).
    *   Run `tsc`. Fix "Implicit any" or "Property does not exist" errors.

3.  **Phase 3**:
    *   *Agent Action*: Rename `utils.test.js` to `utils.test.ts`.
    *   Run `jest`.
    *   *Error*: "Expected 5, got '5'".
    *   *Fix*: Update `utils.ts` to ensure return type is `number`, not string.

4.  **Phase 4**:
    *   *Agent Action*: Change `interface` definitions to be more specific. Run tests. Pass.

---

## Design patterns

### 1) Abstract Factory

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#1-abstract-factory).

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

### 2) Builder

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#2-builder).

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

### 3) Factory Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#3-factory-method).

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

### 4) Prototype

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#4-prototype).

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

### 5) Singleton

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#5-singleton).

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

### 6) Adapter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#6-adapter).

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

### 7) Bridge

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#7-bridge).

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

### 8) Composite

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#8-composite).

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

### 9) Decorator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#9-decorator).

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

### 10) Facade

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#10-facade).

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

### 11) Flyweight

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#11-flyweight).

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

### 12) Proxy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#12-proxy).

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

### 13) Chain of Responsibility

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#13-chain-of-responsibility).

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

### 14) Command

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#14-command).

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

### 15) Interpreter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#15-interpreter).

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

### 16) Iterator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#16-iterator).

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

### 17) Mediator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#17-mediator).

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

### 18) Memento

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#18-memento).

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

### 19) Observer

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#19-observer).

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

### 20) State

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#20-state).

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

### 21) Strategy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#21-strategy).

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

### 22) Template Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#22-template-method).

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

### 23) Visitor

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#23-visitor).

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


## Security

Apply [JavaScript security](../javascript/JAVASCRIPT.md#security) and [general security](../SECURITY_GUIDELINES.md).
TypeScript types do not validate runtime input. Treat JSON, messages, storage values, and model output as `unknown` until checked.
Avoid `as`, non-null assertions, or `any` as substitutes for validation at a trust boundary.
Use the configured schema validator for complex objects and reject unsupported fields where the contract requires strictness.

```typescript
// SECURITY: Validate runtime shape before the UI consumes the value.
function readLabel(value: unknown): string
{
    if (typeof value !== "string" || value.length > 200)
    {
        throw new Error("The label must be text within the allowed length.");
    }

    return value;
}
```

The example limit is illustrative. Use the project's named limit in production.
Validation does not make the returned string safe HTML. Use `textContent` for plain text.
Keep credentials out of source maps, generated declarations, bundles, and logged error contexts.

See [TypeScript type assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions) for the absence of runtime validation.
