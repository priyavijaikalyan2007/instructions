<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 08bc6ee5-e2cc-4de2-ab23-0802f26881d3
Created: 2026
-->

<!-- AGENT: Code commenting standards and best practices for maintainable code. -->

# Code Commenting Guide for AI Coding Agents

A comprehensive reference for generating well-commented, maintainable code.

---

## 1. Core Philosophy

### 1.1 The Audience

Write comments for:

- **Future You** — You won't remember your reasoning in six months. Comments are documentation for your past 
  self's thinking.
- **The Less Experienced** — Assume the reader is a capable but inexperienced developer who needs context, 
  not hand-holding.
- **Posterity** — Someone will maintain this code long after you're gone. Days, weeks, years - they deserve context.
- **Agents** — Other AI agents (review, security, testing, refactoring) will parse this code. Guide them.

### 1.2 The Tone

Comments must adhere to the style and tone guidelines defined in [LANGUAGE.md](./LANGUAGE.md). In summary:

- Simple, concise, and precise
- Neutral, unemotional, and objective
- Neutral international English with American spelling, as specified in `LANGUAGE.md`
- Free of technical jargon, profanity, or overly complex words
- Upleveled but accessible to non-native speakers

---

## 2. What to Comment

### 2.1 General Guidance

1. File-level comments

   - Describe overall purpose of the file
   - List key responsibilities and interactions
   - Include any critical architectural notes

2. Function/Method Comments

   - Explain the purpose and expected behavior
   - Document input parameters and return values
   - Note any side effects or important preconditions/postconditions
   - Highlight any non-obvious design choices

3. Complex Logic Comments

   - Explain complex algorithms or business rules
   - Break down intricate conditional logic
   - Provide rationale for specific implementation approaches

### 2.2 All Entities

Every named construct deserves a comment explaining its purpose and intended usage:

| Entity Type | Comment Should Include |
|-------------|------------------------|
| Classes / Structs | Purpose, responsibilities, key collaborators |
| Interfaces | Contract description, expected implementations |
| Functions / Methods | What it does, parameters, return value, side effects |
| Fields / Properties | What it represents, valid values, units if applicable |
| Enums | What the enumeration represents, each member's meaning |
| SCSS Mixins | What it generates, parameters, where it is used |
| SCSS Variables (custom) | What it controls, valid values, units |
| Constants | Why this value, where it came from |

### 2.3 Significant Logic Blocks

Comment any non-trivial block of logic:

- SQL transactions and queries
- Object mappings and transformations
- API calls (especially external services)
- DOM manipulation sequences
- Event handler registration and delegation
- Bootstrap JavaScript API interactions
- Complex SCSS calculations or selector chains
- Build pipeline steps
- Computation logic and algorithms
- Configuration loading and validation
- Authentication/authorization flows
- Error handling strategies
- Caching logic
- Concurrency and synchronization
- File I/O operations

### 2.4 Non-Obvious Decisions

Comment when:

- The obvious approach wasn't taken (and why)
- A workaround exists for a bug or limitation
- A workaround exists for a browser bug or Bootstrap limitation
- Performance considerations drove the design
- Security or privacy concerns influenced the code
- Regulatory or compliance requirements apply
- Accessibility requirements influenced the code

---

## 3. How to Comment

### 3.1 What, Why — Not How

```csharp
// BAD: How (redundant with code)
// Loop through users and check if email contains @
foreach (var user in users)
{
    if (user.Email.Contains("@")) { ... }
}

// GOOD: What and Why
// Filter to valid users only—external imports may lack email validation
foreach (var user in users)
{
    if (user.Email.Contains("@")) { ... }
}
```

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

Use consistent annotations to mark code states and intentions:

| Annotation | Purpose |
|------------|---------|
| `TODO` | Work to be completed |
| `FIXME` | Known broken code needing repair |
| `BUG` | Documents a known bug |
| `BUGFIX` | Explains why code exists to fix a bug |
| `HACK` | Temporary workaround, not ideal |
| `PERF` | Performance-related note or optimisation |
| `SECURITY` | Security-sensitive code |
| `PRIVACY` | Privacy-sensitive data handling |
| `LOCALIZE` | Needs localization/i18n work |
| `DEPRECATED` | Scheduled for removal |
| `REVIEW` | Needs human review |

Format: `// ANNOTATION: Description with context`

```csharp
// TODO: Replace with batch API call once available (Q3 2025)
// BUGFIX: Null check added—legacy records may have missing tenant IDs (see issue #1234)
// PERF: Cached here to avoid N+1 query in the parent loop
// SECURITY: Input sanitized to prevent SQL injection
```

```typescript
// TODO: Add keyboard navigation for arrow keys (spec section 3.2)
// BUGFIX: Chrome 120 requires explicit tabindex for focus — see issue #42
// HACK: Bootstrap 5.3 modal backdrop z-index conflict — revisit after upgrade
```

### 3.3 Agent Markers

Guide automated tools with explicit markers:

```csharp
// @agent:test — Cover edge case where input is empty collection
// @agent:security — Validate this doesn't expose PII in logs
// @agent:review — Complex logic, needs human verification
// @agent:refactor — Candidate for extraction once patterns stabilize
```

```typescript
// @agent:test — Cover edge case where container ID is null
// @agent:security — Verify this does not inject unsanitised HTML
// @agent:review — Complex selector logic, needs human verification
// @agent:refactor — Candidate for extraction once more components exist
```

### 3.4 Section Headers

For longer files, use section comments to create navigable structure:

```csharp
// ============================================================================
// CONFIGURATION
// ============================================================================

// ============================================================================
// PUBLIC API
// ============================================================================

// ============================================================================
// PRIVATE HELPERS
// ============================================================================
```

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

---

## 4. Language-Specific Conventions

### 4.1 C# / .NET

Use XML documentation for public APIs:

```csharp
/// <summary>
/// Calculates the pro-rated subscription cost for a partial billing period.
/// </summary>
/// <param name="plan">The subscription plan to calculate for.</param>
/// <param name="startDate">The start of the partial period.</param>
/// <param name="endDate">The end of the partial period.</param>
/// <returns>The pro-rated cost in the plan's currency.</returns>
/// <exception cref="ArgumentException">Thrown when endDate precedes startDate.</exception>
public decimal CalculateProratedCost(Plan plan, DateTime startDate, DateTime endDate)
```

### 4.2 TypeScript / JavaScript

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

### 4.3 Python

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

### 4.4 SQL

Comment tables, columns, and complex queries:

```sql
-- Tenant table: Root entity for multi-tenancy isolation
-- All user data is partitioned by tenant_id for security and performance
CREATE TABLE tenants (
    id UUID PRIMARY KEY,           -- Immutable identifier
    name VARCHAR(255) NOT NULL,    -- Display name, user-editable
    slug VARCHAR(100) UNIQUE,      -- URL-safe identifier for routing
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Fetch active subscriptions with plan details
-- PERF: Uses covering index on (tenant_id, status) for the WHERE clause
SELECT s.*, p.name as plan_name, p.price
FROM subscriptions s
JOIN plans p ON s.plan_id = p.id
WHERE s.tenant_id = @tenantId
  AND s.status = 'active';
```

### 4.5 SCSS

Use `/* */` block comments for file headers and section markers (preserved in compiled CSS when not minified). Use `//` line comments for inline explanations (stripped during compilation).

```scss
/*
 * ⚓ COMPONENT: MetricCard
 * 📜 PURPOSE: Styles for the metric card dashboard component.
 * 🔗 RELATES: [[DashboardLayout]]
 */

// Card container — uses theme border and spacing variables
.metric-card {
    padding: $spacer;
    border: 1px solid $gray-300;
    // PERF: Using a simple border instead of box-shadow for rendering performance
    background: white;
}

// Value display — large, bold, high contrast for readability
.metric-value {
    font-size: 1.5rem;
    font-weight: $font-weight-bold;
    color: $gray-900;
}
```

### 4.6 HTML

Use HTML comments for component markers and agent navigation:

```html
<!--
  ⚓ COMPONENT: ErrorDialog
  📜 PURPOSE: Demo markup for the error dialog component.
  🔗 RELATES: [[LiterateErrors]]
-->
<div id="error-dialog-demo">
    <!-- Action buttons — see spec section 4.1 for required actions -->
    <div class="errordialog-actions">
        ...
    </div>
</div>
```

---

### 4.7 Swift

Use `///` documentation comments for public APIs, following [Swift API conventions](https://www.swift.org/documentation/api-design-guidelines/).
Describe parameters, return values, thrown errors, actor isolation, and cancellation when relevant.
Use `// MARK: - Section name` for sections that benefit Xcode navigation.

### 4.8 Go

Follow [Go doc comments](https://go.dev/doc/comment). Start exported declaration comments with the declared name.
Place a documentation comment directly before the declaration it describes.
Document error behavior, context cancellation, ownership, and concurrent-use guarantees when relevant.
Keep navigation headers separate so they do not become an unrelated declaration's documentation.

### 4.9 Rust

Use `///` for item documentation and `//!` for module or crate documentation, following [rustdoc conventions](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html).
Document errors, panics, ownership, and examples where relevant.
Document caller obligations under `# Safety` for unsafe APIs and explain each unsafe block's safety invariant.
Use ordinary comments for navigation markers rather than exposing internal markers as public API documentation.

### 4.10 Java

Use `/** ... */` Javadoc comments directly before documented declarations, following the [Javadoc specification](https://docs.oracle.com/en/java/javase/21/docs/specs/javadoc/doc-comment-spec.html).
Document parameters, results, exceptions, resource ownership, and thread-safety guarantees when relevant.
Keep ordinary navigation comments separate from Javadoc.

---

## 5. Maintaining Comments

### 5.1 Living Documentation

Comments must evolve with the code:

- Update comments when logic changes.
- Remove comments for deleted code.
- Mark outdated comments for review if uncertain.
- Treat comment rot as a code smell.

### 5.2 Review Checklist

When modifying code, verify:

- [ ] Entity comments still accurate
- [ ] Logic block comments reflect current behavior
- [ ] Annotations are still relevant (TODOs completed? BUGFIXes still needed?)
- [ ] Agent markers still appropriate

---

## 6. What Not to Comment in Code

### 6.1 Tutorials and Guides

Code comments are not the place for:

- Framework tutorials
- Technology introductions
- Architecture overviews
- Setup instructions
- Onboarding material

**Instead:** Create documents in `/guides/` with:

- Markdown format
- Links to official documentation
- Team-specific conventions and decisions
- Examples and diagrams as needed

Example structure:

```
/guides/
  authentication.md      # How our auth system works
  database-patterns.md   # Our ORM conventions and query patterns
  api-design.md          # REST conventions and versioning
  deployment.md          # CI/CD and release process
```

### 6.2 Obvious Code

Don't comment self-evident operations:

```csharp
// BAD: States the obvious
// Increment the counter
counter++;

// Set the user's name
user.Name = name;

// Return the result
return result;
```

```typescript
// BAD: States the obvious
// Increment the counter
counter++;

// Set the title text
titleElement.textContent = title;

// Return the result
return result;
```

---

## 7. Quick Reference

### Comment Decision Tree

```
Is this an entity (class, function, field, mixin, variable, etc.)?
  → YES: Add purpose and usage comment

Is this a significant logic block?
  → YES: Add what/why comment

Is this a non-obvious decision?
  → YES: Explain the reasoning

Is there work to be done or a known issue?
  → YES: Add appropriate annotation

Should an agent pay special attention here?
  → YES: Add agent marker

Would this need a tutorial to understand?
  → YES: Write a guide in /guides/, not a comment
```

### Annotation Quick Reference

```
TODO:       Future work
FIXME:      Broken, needs repair
BUG:        Known defect
BUGFIX:     Explains bug fix rationale
HACK:       Temporary workaround
PERF:       Performance note
SECURITY:   Security-sensitive
PRIVACY:    Privacy-sensitive
LOCALIZE:   Needs i18n
DEPRECATED: Removal planned
REVIEW:     Needs human eyes
```

---

*Remember: A well-commented codebase is a gift to everyone who touches it—including future you.*
