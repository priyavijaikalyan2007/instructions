<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 2e4289bf-4901-4547-a219-a724e2d81b9b
Created: 2026
-->

<!-- AGENT: Python conventions and task examples; load only when this language is in scope. -->

# Python instructions

Read this guide when the task changes Python source or its language-specific build and test configuration.
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

Read by task: [References](#references), [Formatting](#formatting), [Style examples](#style-examples), [Naming](#naming), [File organization](#file-organization), [Language constructs](#language-constructs), [Comments](#comments), [Navigation markers](#navigation-markers), [Testing](#testing), [Coverage](#coverage), [Logging](#logging), [Log identity helper](#log-identity-helper), [Logging examples](#logging-examples), [Performance](#performance), [Design patterns](#design-patterns).

## References

1. Follow [PEP 8](https://peps.python.org/pep-0008/)
2. Follow [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
3. Apply the overrides in this document

## Formatting

Python uses indentation instead of braces. Do not add braces to Python control-flow blocks.

## Style examples

### Assertions and Preconditions

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

### Exception Handling Patterns

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

## Naming

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

## File organization

`order.py`, `order_store.py`, and `order_status.py` in the same package.

## Language constructs

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

## Comments

Use docstrings following Google or NumPy style:

```python
def calculate_prorated_cost(plan: Plan, start_date: date, end_date: date) -> Decimal:
    """
    Calculates the pro-rated subscription cost for a partial billing period.

    Args:
        plan: The subscription plan to calculate for.
        start_date: The start of the partial period.
        end_date: The end of the partial period.

    Returns:
        The pro-rated cost in the plan's currency.

    Raises:
        ValueError: When end_date precedes start_date.
    """
```

A Python docstring also states ownership and concurrency guarantees when callers need them.
Use `Raises` for expected runtime failures rather than presenting them as assertions.

```python
def parse_quantity(text: str) -> int:
    """Parses a positive decimal quantity without retaining the input.

    Args:
        text: The complete decimal quantity.

    Returns:
        The positive quantity.

    Raises:
        ValueError: If the text is invalid or the quantity is nonpositive.
    """
    quantity = int(text)
    if quantity <= 0:
        raise ValueError("Quantity must be positive.")
    return quantity
```

## Navigation markers

```python
# File: quantity_policy.py
# COMPONENT: QuantityPolicy
# PURPOSE: Validates quantities before an order is created.
# RELATES: [[OrderValidation]]
# FLOW: CLI or UI -> quantity policy -> order constructor
# SECURITY: Does not accept a quantity without validation.

# @entrypoint
# @config: maximum_quantity
# OrderValidation: Canonical quantity boundary.
def is_valid_quantity(quantity: int, maximum_quantity: int) -> bool:
    """Returns whether the quantity is within the permitted range."""
    return 0 < quantity <= maximum_quantity
```

Use `#` rather than `//`. Keep shebangs, encoding declarations, and module docstrings in their required positions.

## Testing

**Unit Tests:**
- Use pytest as the test framework
- Use pytest-mock for mocking
- Use hypothesis for property-based testing

**Integration Tests:**
- Test against real infrastructure in test environments
- Use pytest fixtures for resource management

```python
# File: tests/test_order_summary.py
import unittest
from order_summary import OrderSummary

class OrderSummaryTests(unittest.TestCase):
    def test_display_label_with_positive_quantity_includes_quantity(self) -> None:
        order = OrderSummary("order-1", "Sample Customer", 2)
        self.assertEqual(order.display_label(), "Sample Customer: 2")

    def test_constructor_with_zero_quantity_raises(self) -> None:
        with self.assertRaises(ValueError):
            OrderSummary("order-1", "Sample Customer", 0)
```

Use temporary directories for file-processing tests. Inject clocks, HTTP clients, and subprocess runners at real external boundaries.
Test cancellation and resource cleanup separately from successful output. Do not mock the function whose behavior the test should verify.

## Coverage

- Use pytest-cov
- Run with `pytest --cov=src --cov-report=html`

```bash
# Python
pytest --cov=src --cov-report=html --cov-report=term-missing
```

## Logging

Use configured `logging` handlers and `contextvars` for operation context across async tasks.

## Log identity helper

Python uses the standard library:

```python
# File: log_identity.py
import hashlib
import hmac

def user_log_key(key: bytes, tenant_id: str, canonical_username: str) -> str:
    """Returns a stable tenant-scoped pseudonym for approved log correlation."""
    if len(key) < 32:
        raise ValueError("A logging key needs at least 32 bytes.")
    payload = bytearray(b"log-user-v1\x00")
    for field in (tenant_id, canonical_username):
        encoded = field.encode("utf-8")
        if len(encoded) > 1024:
            raise ValueError("A log identity field exceeds its limit.")
        payload.extend(len(encoded).to_bytes(4, "big"))
        payload.extend(encoded)
    digest = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return "user-hmac-v1:" + digest
```

## Logging examples

```python
import logging
import contextvars

# Context variables for async safety
correlation_id_ctx = contextvars.ContextVar("correlation_id", default="N/A")

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_ctx.get()
        return True

logging.basicConfig(format='%(asctime)s [%(correlation_id)s] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addFilter(ContextFilter())

def process_user_data(user_data):
    # SECURITY: Exclude credentials and tokens from logs.
    logger.debug("Entering process_user_data")

    try:
        # QUERY LOGGING
        query = "SELECT * FROM users WHERE id = ?"
        logger.debug(f"Executing Query: {query}")

        result = None # Simulate DB call

        if result is None:
            # NULL RETURN LOGGING
            logger.warning("Query returned NULL/Empty result")

    except Exception as e:
        logger.exception("Error processing user data")

# Simulating entry
correlation_id_ctx.set("abc-123-xyz")
process_user_data({"secret": "my_password"})
```

---

## Performance

- Use `cProfile`, `timeit`, or the project's profiler with representative data and the configured interpreter.
- Measure peak memory as well as duration for large files and collections.
- Prefer streaming or bounded batches when the complete input need not remain in memory.
- Use async I/O for suitable I/O-bound work. Do not assume that async makes CPU-bound Python work parallel.
- Keep blocking work off an event loop and account for process startup and serialization when choosing worker processes.
- Optimize a measured hot path. Do not replace readable Python with a native extension without a demonstrated need.

## Design patterns

### 1) Abstract Factory

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#1-abstract-factory).

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

### 2) Builder

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#2-builder).

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

### 3) Factory Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#3-factory-method).

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

### 4) Prototype

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#4-prototype).

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

### 5) Singleton

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#5-singleton).

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class _AppSettings:
    time_zone: str = "UTC"

_settings = _AppSettings()

def app_settings() -> _AppSettings:
    return _settings
```

### 6) Adapter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#6-adapter).

```python
from typing import Callable

class PrinterAdapter:
    def __init__(self, send_bytes: Callable[[bytes], int]) -> None:
        self._send_bytes = send_bytes

    def print_text(self, text: str) -> int:
        return self._send_bytes(text.encode("utf-8"))
```

### 7) Bridge

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#7-bridge).

```python
from typing import Callable

class Circle:
    def __init__(self, radius: float, render_circle: Callable[[float], str]) -> None:
        self._radius = radius
        self._render_circle = render_circle

    def draw(self) -> str:
        return self._render_circle(self._radius)
```

### 8) Composite

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#8-composite).

```python
from dataclasses import dataclass, field

@dataclass
class Node:
    value: int
    children: list["Node"] = field(default_factory=list)

    def total(self) -> int:
        return self.value + sum(child.total() for child in self.children)
```

### 9) Decorator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#9-decorator).

```python
from typing import Callable

def with_brackets(render: Callable[[], str]) -> Callable[[], str]:
    def decorated() -> str:
        return "[" + render() + "]"
    return decorated
```

### 10) Facade

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#10-facade).

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

### 11) Flyweight

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#11-flyweight).

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

### 12) Proxy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#12-proxy).

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

### 13) Chain of Responsibility

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#13-chain-of-responsibility).

```python
from collections.abc import Callable, Iterable

def validate_chain(value: int, handlers: Iterable[Callable[[int], str | None]]) -> str | None:
    for handler in handlers:
        error = handler(value)
        if error is not None:
            return error
    return None
```

### 14) Command

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#14-command).

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

### 15) Interpreter

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#15-interpreter).

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

### 16) Iterator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#16-iterator).

```python
from collections.abc import Iterator, Sequence

def even_values(values: Sequence[int]) -> Iterator[int]:
    for value in values:
        if value % 2 == 0:
            yield value
```

### 17) Mediator

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#17-mediator).

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

### 18) Memento

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#18-memento).

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

### 19) Observer

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#19-observer).

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

### 20) State

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#20-state).

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

### 21) Strategy

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#21-strategy).

```python
from typing import Callable

def format_text(text: str, strategy: Callable[[str], str]) -> str:
    return strategy(text)
```

### 22) Template Method

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#22-template-method).

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

### 23) Visitor

Shared intent and selection criteria: [GOF_PATTERNS.md](../GOF_PATTERNS.md#23-visitor).

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


## Security

Apply [general security](../SECURITY_GUIDELINES.md). Do not use `eval` or `exec` on untrusted text.
Do not deserialize untrusted `pickle` content, including model artifacts. Use bounded parsers and explicit data contracts.
If YAML is required, use a safe loader and bound its resource use.
See [Python pickle security](https://docs.python.org/3/library/pickle.html).

Pass SQL values through the driver's parameter API. Pass subprocess arguments as a sequence without `shell=True`.
Validate executable paths and option-like arguments. Keep credentials out of process arguments and inherited environments when possible.
Pin dependencies and verify hashes under the project's dependency policy.

```python
# SECURITY: SQLite example. Keep user content separate from the query.
rows = connection.execute(
    "SELECT display_name FROM customer WHERE tenant_id = ? AND id = ?",
    (authorized_tenant_id, customer_id),
)
```

Use `TemporaryFile` or `TemporaryDirectory` for temporary work, preferably inside an application-controlled private directory.
Do not use `mktemp` followed by a separate open. Cleanup does not guarantee secure erasure from storage.
See [Python tempfile](https://docs.python.org/3/library/tempfile.html).
Keep secrets short-lived and avoid formatting them into strings or tracebacks.
`del` removes a reference. It does not erase bytes, other references, interpreter copies, or swap.
A mutable `bytearray` can reduce avoidable copies, but it is not a portable secure-memory container.
