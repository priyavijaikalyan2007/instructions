<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 82caf28f-8ab6-4b29-b187-cf536fdb6c3f
Created: 2026
-->

<!-- AGENT: Coding style conventions and formatting rules for the codebase. -->

# Coding Style Guide

A guide for maintainable code in C#, Swift, Go, Rust, Java, TypeScript, JavaScript, Python, HTML, CSS, and SCSS.

## Core Philosophy

**The Student Principle**: Assume that the code you write will be read, maintained, deployed, and operated 
by a less than gifted high school student. Write code with that in mind.

- **Explicit**: Write explicit code that reveals intent
- **Simple**: Write concise code that gets the job done without cleverness
- **Readable**: Assume you will read this code months from now and won't remember what you did
- **Language**: Adhere to the business communication standards in [LANGUAGE.md](LANGUAGE.md)

---

## General Standards

### Foundational References

Use the references in the selected language guide. The shared formatting and construction rules in this file remain authoritative.

## Formatting Rules

### Indentation and Line Length

Use the same house style across languages. Language conventions govern names and semantics, not a different preferred visual style.

- Use four spaces for indentation. Do not use tabs.
- Keep source lines at or below 120 characters.
- Use Allman braces, with each opening brace on its own line wherever the grammar permits it.
- Keep one type per file, including a five-line struct.
- Keep one statement and one expression per line.
- Configure formatters to preserve this policy. Do not accept unrelated formatter changes during a behavior change.

Apply syntax-required exceptions from the selected language guide. Keep the remaining house rules unchanged.

See [C#](csharp/CSHARP.md#indentation-and-line-length).

### Brace Style

Prefer **Allman style** braces in every brace-based language. Put the opening brace on its own line.
Apply only the syntax exceptions documented in the selected language guide.

See [C#](csharp/CSHARP.md#brace-style).

See [TypeScript](typescript/TYPESCRIPT.md#brace-style).

### Always Use Braces

Always use braces around control-flow bodies where the language uses braces, even for a single statement.
Do not replace a multi-step block with a terse conditional expression.

See [C#](csharp/CSHARP.md#always-use-braces).

See [TypeScript](typescript/TYPESCRIPT.md#always-use-braces).

### Parentheses for Clarity

Use parentheses around expressions even when operator precedence is obvious.

See [C#](csharp/CSHARP.md#parentheses-for-clarity).

See [TypeScript](typescript/TYPESCRIPT.md#parentheses-for-clarity).

### Whitespace for Readability

Use blank lines to separate logical groups of code.

See [C#](csharp/CSHARP.md#whitespace-for-readability).

See [TypeScript](typescript/TYPESCRIPT.md#whitespace-for-readability).

### Parameter Alignment

Align parameters using newlines and consistent indentation.

See [C#](csharp/CSHARP.md#parameter-alignment).

See [TypeScript](typescript/TYPESCRIPT.md#parameter-alignment).

---

## Naming Conventions

Use the same naming decisions for each concept, then apply the spelling and visibility rules in the selected language guide.
Do not rename a wire field, database column, or public API merely to match an internal variable convention.

| Element | Shared rule |
| --- | --- |
| Types | Name the domain concept or responsibility. Avoid redundant words such as `DataObject`. |
| Interfaces, protocols, traits | Name the contract. Use the language's prefix and suffix conventions. |
| Functions and methods | Name the action or returned value. Make side effects clear. |
| Fields and properties | Name the stored meaning. Include units when a number could be ambiguous. |
| Booleans | State the condition, such as `isEnabled`, `is_enabled`, or `IsEnabled`. |
| Constants | Name the fixed meaning rather than its current literal value. |
| Parameters and locals | Use domain names. Reserve short counters for short, obvious loops. |
| Type parameters | Describe the role when a generic letter would hide the contract. |
| Files | Match the type or responsibility, using the language's filename convention. |

Detailed naming tables and examples are in the selected language guide.

### C# Naming

See [C#](csharp/CSHARP.md#naming).

### TypeScript / JavaScript

See [JavaScript](javascript/JAVASCRIPT.md#naming), [TypeScript](typescript/TYPESCRIPT.md#naming).

### SCSS / CSS

See [CSS](css/CSS.md#naming), [SCSS](scss/SCSS.md#naming).

### HTML Naming

See [HTML](html/HTML.md#naming).

### Python Naming

See [Python](python/PYTHON.md#naming).

### Swift Naming

See [Swift](swift/SWIFT.md#naming).

### Go Naming

See [Go](go/GO.md#naming).

### Rust Naming

See [Rust](rust/RUST.md#naming).

### Java Naming

See [Java](java/JAVA.md#naming).

### Variable Naming Guidelines

- Use short names for counters and indexes: `i`, `j`, `k`, `n`
- Use descriptive names for everything else
- Name variables in the domain of the application

See [C#](csharp/CSHARP.md#variable-naming-guidelines).

## SCSS-Specific Rules

See [SCSS](scss/SCSS.md#scss-construction).

### Variable Overrides

See [SCSS](scss/SCSS.md#scss-construction).

### Nesting Depth

See [SCSS](scss/SCSS.md#scss-construction).

### Avoid `!important`

See [SCSS](scss/SCSS.md#scss-construction).

## File Organization

### One Type Per File

Keep one type per file in every language, even when the type is a five-line struct or a small interface.
Prefer separate files because filesystem searches should locate a type without searching file contents.
Nested types and extensions may remain beside their owning type when that arrangement explains a cohesive relationship.
Prefer a separate file when the relationship is clear without nesting. Do not group unrelated types to save files.

Use the filename and module rules in the selected language guide.

Examples may show several labeled files together to explain a relationship. Split them at the file labels in actual code.

See [C#](csharp/CSHARP.md#one-type-per-file).

Rationale: Searching for files is faster than searching in files.

---

## Method and Function Design

### Size Limits

Keep functions and methods at or below 30 lines of code. Do not pad a shorter function.
If a function exceeds this limit, extract smaller functions with clear responsibilities.

### Nesting Limits

Limit nesting to 3-4 levels. The first statement in a method is level 1. Use early returns to flatten logic.

See [C#](csharp/CSHARP.md#nesting-limits).

See [TypeScript](typescript/TYPESCRIPT.md#nesting-limits).

---

## Error Handling

### Early Returns (Guard Clauses)

Use early returns to handle edge cases and invalid states at the beginning of functions or methods.

See [C#](csharp/CSHARP.md#early-returns-guard-clauses).

See [TypeScript](typescript/TYPESCRIPT.md#early-returns-guard-clauses).

### Assertions and Preconditions

Use assertions to validate assumptions and catch programming errors early in development.

See [C#](csharp/CSHARP.md#assertions-and-preconditions).

See [TypeScript](typescript/TYPESCRIPT.md#assertions-and-preconditions).

See [Python](python/PYTHON.md#assertions-and-preconditions).

### Constraints and Invariants

Use type constraints and validation to enforce business rules.

See [C#](csharp/CSHARP.md#constraints-and-invariants).

See [TypeScript](typescript/TYPESCRIPT.md#constraints-and-invariants).

### Exception Handling Patterns

See [C#](csharp/CSHARP.md#exception-handling-patterns).

See [Python](python/PYTHON.md#exception-handling-patterns).

---

## Explicit Code Style

Avoid clever tricks. Write code that clearly expresses intent.

See [C#](csharp/CSHARP.md#explicit-code-style).

When using advanced techniques (SIMD, specific algorithms), explain them in comments with references.

See [C#](csharp/CSHARP.md#explicit-code-style).

See [TypeScript](typescript/TYPESCRIPT.md#explicit-code-style).

---

## Language-Specific Patterns

### Python-Specific

See [Python](python/PYTHON.md#language-constructs).

### TypeScript-Specific

See [TypeScript](typescript/TYPESCRIPT.md#language-constructs).

### Swift-Specific

See [Swift](swift/SWIFT.md#language-constructs).

### Go-Specific

See [Go](go/GO.md#language-constructs).

### Rust-Specific

See [Rust](rust/RUST.md#language-constructs).

### Java-Specific

See [Java](java/JAVA.md#language-constructs).

### C#-Specific

See [C#](csharp/CSHARP.md#language-constructs).

## Summary Checklist

- [ ] One type per file, with only justified nested-type or extension exceptions
- [ ] Maximum 120 characters per source line
- [ ] Four spaces for indentation, with no tabs
- [ ] Allman braces wherever the language grammar permits them
- [ ] Only the syntax exceptions in the selected language guide are applied
- [ ] Always use braces for control flow in languages that have braces
- [ ] Parentheses around expressions for clarity
- [ ] Maximum 30 lines per function or method
- [ ] Maximum three levels of nesting
- [ ] Early returns for guard clauses
- [ ] Assertions for invariants
- [ ] Domain-appropriate naming
- [ ] Explicit code over clever tricks

## Named constants

- **"No Magic Numbers."**
- **Extraction:** Any number (e.g., `3000` ms timeout) or string (e.g., "Admin" role) that appears more than once—or has semantic meaning—must be a named constant.

## Code hygiene

- **"Delete, don't disable."**
- **No Commented-Out Code:** Do not leave blocks of commented-out code (C#, SCSS, TypeScript, Javascript or HTML) "just in case". Rely on Git history.
- **Import Cleanup:** Unused imports and variables are (C# usings, SCSS imports, TypeScript imports, and variables are technical debt. Remove them immediately before considering a task complete. Remove them before considering a task complete.
