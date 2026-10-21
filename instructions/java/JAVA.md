<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 65977edc-82bf-4427-9663-6dc1884786b6
Created: 2026
-->

<!-- AGENT: Java conventions and task examples; load only when this language is in scope. -->

# Java instructions

Read this guide when the task changes Java source or its language-specific build and test configuration.
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

Read by task: [References](#references), [Naming](#naming), [File organization](#file-organization), [Language constructs](#language-constructs), [Comments](#comments), [Navigation markers](#navigation-markers), [Folding](#folding), [Testing](#testing), [Coverage](#coverage), [Logging](#logging), [Log identity helper](#log-identity-helper), [Logging examples](#logging-examples), [Performance](#performance), [Design patterns](#design-patterns).

## References

1. Follow the project's JDK, framework, and public API contracts.
2. Apply the naming, formatting, and file rules in this document.

## Naming

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

## File organization

`Order.java`, `OrderStore.java`, and `OrderStatus.java`. Match a public type to its filename.

## Language constructs

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

## Comments

Use `/** ... */` Javadoc comments directly before documented declarations, following the [Javadoc specification](https://docs.oracle.com/en/java/javase/21/docs/specs/javadoc/doc-comment-spec.html).
Document parameters, results, exceptions, resource ownership, and thread-safety guarantees when relevant.
Keep ordinary navigation comments separate from Javadoc.

```java
// File: QuantityParser.java
public final class QuantityParser
{
    /**
     * Parses a positive decimal quantity without retaining the input.
     * @param text the complete decimal quantity
     * @return the positive quantity
     * @throws NumberFormatException if the text is invalid or exceeds the integer range
     * @throws IllegalArgumentException if the parsed value is nonpositive
     */
    public static int parseQuantity(String text)
    {
        int quantity = Integer.parseInt(text);
        if (quantity <= 0)
        {
            throw new IllegalArgumentException("Quantity must be positive.");
        }
        return quantity;
    }
}
```

---

## Navigation markers

```java
// File: QuantityPolicy.java
/*
 * COMPONENT: QuantityPolicy
 * PURPOSE: Validates a quantity before constructing an order.
 * RELATES: [[OrderValidation]]
 * FLOW: HTTP or CLI boundary -> quantity policy -> order constructor
 * SECURITY: Validate external values before storing them.
 */
public final class QuantityPolicy
{
    // @entrypoint
    /** Returns whether the quantity is positive. */
    public static boolean isValidQuantity(int quantity)
    {
        return quantity > 0;
    }
}
```

These examples spell out the standard fields in ASCII. The corresponding symbols used elsewhere in this guide carry the same meanings.
Preserve annotation and documentation attachment. Never insert a marker between an annotation and the declaration it controls.

## Folding

Use ordinary section comments unless the project declares supported IDE folding markers.
Do not copy C# `#region` directives into this language.

## Testing

Use the project's existing test framework and Maven or Gradle wrapper.
Run the documented unit and integration tasks rather than assuming that `test` includes every integration suite.
For host extensions, test against the host runtime and dependency versions actually shipped.

```java
// File: OrderSummaryTests.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

final class OrderSummaryTests
{
    @Test
    void displayLabelWithPositiveQuantityIncludesQuantity()
    {
        OrderSummary order = new OrderSummary("order-1", "Sample Customer", 2);
        assertEquals("Sample Customer: 2", order.displayLabel());
    }

    @Test
    void constructorWithZeroQuantityThrows()
    {
        assertThrows(IllegalArgumentException.class, () ->
        {
            new OrderSummary("order-1", "Sample Customer", 0);
        });
    }
}
```

This example uses JUnit Jupiter. Retain the configured framework rather than introducing a second framework for a single test.
Use the project's container or host-runtime harness for database and extension behavior. Preserve interrupt status and close test-owned resources.

## Coverage

Use the project's configured JaCoCo or equivalent Maven/Gradle integration and retain its reports.

## Logging

Use the project's logging facade or the host platform's logger. Avoid competing runtime logging backends in plugins.

## Log identity helper

Java uses JDK cryptography and hexadecimal utilities:

```java
// File: LogIdentity.java
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.util.HexFormat;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public final class LogIdentity
{
    public static String userLogKey(byte[] key, String tenantId, String canonicalUsername)
        throws GeneralSecurityException
    {
        if (key.length < 32)
        {
            throw new IllegalArgumentException("A logging key needs at least 32 bytes.");
        }
        byte[] payload = payload(tenantId, canonicalUsername);
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(key, "HmacSHA256"));
        return "user-hmac-v1:" + HexFormat.of().formatHex(mac.doFinal(payload));
    }

    private static byte[] payload(String tenantId, String canonicalUsername)
    {
        byte[] domain = "log-user-v1\0".getBytes(StandardCharsets.UTF_8);
        byte[] tenant = tenantId.getBytes(StandardCharsets.UTF_8);
        byte[] user = canonicalUsername.getBytes(StandardCharsets.UTF_8);
        if (tenant.length > 1024 || user.length > 1024)
        {
            throw new IllegalArgumentException("A log identity field exceeds its limit.");
        }
        return ByteBuffer.allocate(domain.length + 8 + tenant.length + user.length)
            .put(domain).putInt(tenant.length).put(tenant).putInt(user.length).put(user).array();
    }
}
```

## Logging examples

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

public class OrderService
{
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    public void handleRequest(String userRequestID, String tenantID)
    {
        // CONTEXT: Setup MDC at entry point
        String correlationID = java.util.UUID.randomUUID().toString();
        MDC.put("correlation_id", correlationID);
        MDC.put("request_id", userRequestID != null ? userRequestID : generateMangledID());
        MDC.put("tenant_id", tenantID);

        try
        {
            logger.info("Request processing started");
            processData("sensitive_value");
        }
        catch (Exception e)
        {
            logger.error("Exception encountered", e);
        }
        finally
        {
            logger.info("Request processing finished");
            MDC.clear(); // Cleanup thread local
        }
    }

    private void processData(String input)
    {
        // SECURITY: Exclude the sensitive input from logs.
        logger.debug("Entering processData");

        // ... logic
    }

    private String generateMangledID()
    {
        return java.util.UUID.randomUUID().toString();
    }

}
```

---

## Performance

Measure latency, throughput, allocations, and bounded concurrency before optimizing.

- Separate JVM warmup from steady-state measurements. Use the project's benchmark harness when optimizing hot methods.
- Use Java Flight Recorder and allocation/GC evidence to investigate latency or memory changes.
- Bound executor queues and connection pools. Do not assume that a different thread model removes resource limits.
- Close owned resources and preserve interruption so canceled work can stop.
- Test with the actual host runtime and classpath for extensions rather than a convenient standalone JVM configuration.
- Compare packaged startup and runtime behavior with the deployed launch mode.

## Design patterns

### 1) Abstract Factory

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#1-abstract-factory).

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

### 2) Builder

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#2-builder).

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

### 3) Factory Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#3-factory-method).

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

### 4) Prototype

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#4-prototype).

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

### 5) Singleton

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#5-singleton).

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

### 6) Adapter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#6-adapter).

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

### 7) Bridge

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#7-bridge).

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

### 8) Composite

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#8-composite).

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

### 9) Decorator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#9-decorator).

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

### 10) Facade

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#10-facade).

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

### 11) Flyweight

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#11-flyweight).

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

### 12) Proxy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#12-proxy).

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

### 13) Chain of Responsibility

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#13-chain-of-responsibility).

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

### 14) Command

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#14-command).

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

### 15) Interpreter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#15-interpreter).

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

### 16) Iterator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#16-iterator).

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

### 17) Mediator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#17-mediator).

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

### 18) Memento

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#18-memento).

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

### 19) Observer

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#19-observer).

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

### 20) State

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#20-state).

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

### 21) Strategy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#21-strategy).

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

### 22) Template Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#22-template-method).

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

### 23) Visitor

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#23-visitor).

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


## Security

Apply [general security](../SECURITY_GUIDELINES.md), including tenant context and sensitive-memory limits.
Bind SQL values through `PreparedStatement` or the ORM's parameter API.
Do not concatenate values into SQL, JPQL, shell commands, or expression-language inputs.
Disable external entities and DTD processing when parsing untrusted XML through the configured parser.
Avoid native Java deserialization for untrusted data. Use an explicit data contract and a bounded parser.
Do not enable arbitrary polymorphic type loading from incoming JSON.
See [OWASP Java security](https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html).

```java
// SECURITY: Values remain data. authorizedTenantId comes from verified application context.
try (PreparedStatement statement = connection.prepareStatement(
    "SELECT display_name FROM customer WHERE tenant_id = ? AND id = ?"))
{
    statement.setString(1, authorizedTenantId);
    statement.setString(2, customerId);
    try (ResultSet rows = statement.executeQuery())
    {
        readAuthorizedResult(rows);
    }
}
```

Use short-lived `char[]` or `byte[]` for secrets when the receiving API supports them.
Clear owned arrays in a `finally` block. Avoid conversion to immutable strings and unnecessary copies.
`Arrays.fill` reduces retention in that array. It does not prove that JVM copies, dumps, or swapped pages are erased.
Use platform credential services for persistence. Do not invent a Java secure-string class with unsupported guarantees.
Use `Files.createTempFile` in a private directory and set restrictive creation attributes where supported.
Test permissions on every supported operating system.

For password callbacks, clear both the callback state and any returned copy when finished.
See [PasswordCallback](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/javax/security/auth/callback/PasswordCallback.html).
For temporary creation attributes, see [Files.createTempFile](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/nio/file/Files.html).
