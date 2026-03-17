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

- **Future You** — You won't remember your reasoning in six months. Comments are documentation for your past self's thinking.
- **The Less Experienced** — Assume the reader is a capable but inexperienced developer who needs context, not hand-holding.
- **Posterity** — Someone will maintain this code long after you're gone. Days, weeks, years—they deserve context.
- **Agents** — Other AI agents (review, security, testing, refactoring) will parse this code. Guide them.

### 1.2 The Tone

Comments must adhere to the style and tone guidelines defined in [LANGUAGE.md](./LANGUAGE.md). In summary:

- Simple, concise, and precise
- Neutral, unemotional, and objective
- Standard British English for business communication
- Free of technical jargon, profanity, or overly complex words
- Upleveled but accessible to non-native speakers

---

## 2. What to Comment

### 2.1 All Entities

Every named construct deserves a comment explaining its purpose and intended usage:

| Entity Type | Comment Should Include |
|-------------|------------------------|
| Classes / Structs | Purpose, responsibilities, key collaborators |
| Interfaces | Contract description, expected implementations |
| Functions / Methods | What it does, parameters, return value, side effects |
| Fields / Properties | What it represents, valid values, units if applicable |
| Enums | What the enumeration represents, each member's meaning |
| Constants | Why this value, where it came from |

### 2.2 Significant Logic Blocks

Comment any non-trivial block of logic:

- SQL transactions and queries
- Object mappings and transformations
- API calls (especially external services)
- Computation logic and algorithms
- Configuration loading and validation
- Authentication/authorization flows
- Error handling strategies
- Caching logic
- Concurrency and synchronization
- File I/O operations

### 2.3 Non-Obvious Decisions

Comment when:

- The obvious approach wasn't taken (and why)
- A workaround exists for a bug or limitation
- Performance considerations drove the design
- Security or privacy concerns influenced the code
- Regulatory or compliance requirements apply

---

## 3. How to Comment

### 3.1 What, Why—Not How

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

### 3.2 Standard Annotations

Use consistent annotations to mark code states and intentions:

| Annotation | Purpose |
|------------|---------|
| `TODO` | Work to be completed |
| `FIXME` | Known broken code needing repair |
| `BUG` | Documents a known bug |
| `BUGFIX` | Explains why code exists to fix a bug |
| `HACK` | Temporary workaround, not ideal |
| `PERF` | Performance-related note or optimization |
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

### 3.3 Agent Markers

Guide automated tools with explicit markers:

```csharp
// @agent:test — Cover edge case where input is empty collection
// @agent:security — Validate this doesn't expose PII in logs
// @agent:review — Complex logic, needs human verification
// @agent:refactor — Candidate for extraction once patterns stabilize
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

---

## 5. Maintaining Comments

### 5.1 Living Documentation

Comments must evolve with the code:

- Update comments when logic changes
- Remove comments for deleted code
- Mark outdated comments for review if uncertain
- Treat comment rot as a code smell

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

---

## 7. Quick Reference

### Comment Decision Tree

```
Is this an entity (class, function, field, etc.)?
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