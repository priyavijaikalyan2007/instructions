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

Comments must adhere to the style and tone guidelines defined in [LANGUAGE.md](LANGUAGE.md). In summary:

- Simple, concise, and precise
- Neutral, unemotional, and objective
- Neutral international English with American spelling, as specified in `instructions/LANGUAGE.md`
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

See [C#](csharp/CSHARP.md#31-what-why--not-how).

See [TypeScript](typescript/TYPESCRIPT.md#31-what-why--not-how).

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

Format each annotation using the comment syntax in the selected language guide: `ANNOTATION: Description with context`.

See [C#](csharp/CSHARP.md#32-standard-annotations).

See [TypeScript](typescript/TYPESCRIPT.md#32-standard-annotations).

### 3.3 Agent Markers

Guide automated tools with explicit markers:

See [C#](csharp/CSHARP.md#33-agent-markers).

See [TypeScript](typescript/TYPESCRIPT.md#33-agent-markers).

### 3.4 Section Headers

For longer files, use section comments to create navigable structure:

See [C#](csharp/CSHARP.md#34-section-headers).

See [TypeScript](typescript/TYPESCRIPT.md#34-section-headers).

---

## 4. Language-Specific Conventions

### 4.1 C# / .NET

See [C#](csharp/CSHARP.md#comments).

### 4.2 TypeScript / JavaScript

See [TypeScript](typescript/TYPESCRIPT.md#comments).

### 4.3 Python

See [Python](python/PYTHON.md#comments).

### 4.4 SQL

See [SQL](sql/SQL.md#comments).

### 4.5 SCSS

See [SCSS](scss/SCSS.md#comments).

### 4.6 HTML

See [HTML](html/HTML.md#comments).

### 4.7 Swift

See [Swift](swift/SWIFT.md#comments).

### 4.8 Go

See [Go](go/GO.md#comments).

### 4.9 Rust

See [Rust](rust/RUST.md#comments).

### 4.10 Java

See [Java](java/JAVA.md#comments).

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

See [C#](csharp/CSHARP.md#62-obvious-code).

See [TypeScript](typescript/TYPESCRIPT.md#62-obvious-code).

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
