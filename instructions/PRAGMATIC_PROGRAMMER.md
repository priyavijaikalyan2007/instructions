<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 73b56f31-ea7f-4e62-a9b7-e0da9e52d562
Created: 2026
-->

<!-- AGENT: Shared construction principles, including safe failure and degraded behavior. -->

# Pragmatic Programmer Instructions for Agents

This document outlines the core principles and practices from *The Pragmatic Programmer* by Andrew Hunt and David Thomas. All coding agents MUST adhere to these guidelines to ensure the production of robust, maintainable, and flexible software.

## 1. Core Philosophy

### DRY - Don't Repeat Yourself
- **Mandate**: Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.
- **Application**: 
    - Do not duplicate logic in multiple functions.
    - Do not duplicate knowledge between code and documentation (prefer self-documenting code).
    - Do not duplicate data structures (derive data when possible).
    - If you find yourself copy-pasting code, stop and refactor into a shared abstraction.

### Orthogonality
- **Mandate**: Design components that are independent and have a single, well-defined purpose.
- **Application**:
    - Changing one component should not require changes in unrelated components.
    - Keep UI logic separate from business logic, and business logic separate from data persistence.
    - Use Dependency Injection to decouple components.

### Good Enough Software
- **Mandate**: Quality is a systems issue. Know when to stop.
- **Application**: 
    - Implement the requested feature completely and robustly, but avoid "gold-plating" (adding unrequested features).
    - Ensure code is "Pragmatically" tested and documented.

---

## 2. Pragmatic Design

### Design by Contract (DbC)
- **Mandate**: Use clearly defined contracts to ensure software correctness.
- **Application**:
    - **Preconditions**: Validate inputs at the entry of every routine.
    - **Postconditions**: Ensure the state is valid before returning.
    - **Class Invariants**: Ensure the object remains in a valid state throughout its lifecycle.
    - *Note: Adhere to the guard clause patterns in [CODING_STYLE.md](CODING_STYLE.md).*

### Dead Programs Tell No Tales
- **Mandate**: When code fails, fail fast and loudly.
- **Application**:
    - Do not "catch and swallow" exceptions.
    - If a state is impossible, use an assertion to crash the program during development.
    - Do not return "magic values" (like -1 or null) to indicate errors if the language supports exceptions or Result types.

#### Degraded behavior and data integrity

A failed read must remain distinguishable from a successful read of empty data.
Do not return plausible defaults, empty documents, or null-object implementations that callers can mistake for authoritative state.
A degraded component must report its failure and must not supply fabricated state to a write or autosave.
Preserve the last known state when a load or save fails.
Read-only views and explicitly stale cached values are valid degraded modes when callers can identify their limits.
Apply this rule to dependency failures, native document loads, browser storage, and service responses.
Test both the failure signal and the prevention of destructive writes.

### Assertive Programming
- **Mandate**: If it can't happen, use assertions to ensure it doesn't.
- **Application**:
    - Use assertions to validate internal state and logic that "should never be false."
    - Do not use assertions for runtime error handling (use exceptions or error returns for those).

---

## 3. Implementation Tools and Techniques

### The Power of Plain Text
- **Mandate**: Keep knowledge in human-readable formats.
- **Application**:
    - Prefer JSON, YAML, or Markdown for configuration and documentation.
    - Ensure your generated code is readable without specialized IDE tools.

### Decoupling and the Law of Demeter
- **Mandate**: Minimize coupling between modules.
- **Application**:
    - A method should only call methods of:
        1. Its own class.
        2. Objects passed as parameters.
        3. Objects it creates.
        4. Global constants.
    - **Avoid**: `order.Customer.Address.ZipCode`. Instead, use `order.GetCustomerZipCode()`.

### Metaprogramming
- **Mandate**: Put abstractions in code, details in metadata.
- **Application**:
    - Use configuration files or environment variables for values that change across environments (URLs, ports, API keys).
    - Avoid hardcoding business rules that are likely to change.

---

## 4. Pragmatic Projects

### Refactoring
- **Mandate**: Refactor early and often.
- **Application**:
    - Refactor when you see a "violation" of DRY, or when code becomes "smelly" (too large, complex, or coupled).
    - **The Golden Rule**: Do not try to refactor and add new functionality at the same time. These are two separate tasks.
    - Always run tests after refactoring.

### Test to Break
- **Mandate**: Software that isn't tested doesn't work.
- **Application**:
    - Write unit tests for all new logic.
    - Design tests to find bugs, not just to prove the code works. Use edge cases, boundary values, and "impossible" inputs.
    - Aim for high branch coverage, not just line coverage.

### Tracing vs. Logging
- **Mandate**: Use tracing for flow control and logging for audit/errors.
- **Application**:
    - Use structured logging (e.g., Serilog, Winston, Python Logging).
    - Ensure log messages are meaningful and contain sufficient context for debugging.

---

## 5. Checklist for Pragmatic Agents

- [ ] Is this code DRY?
- [ ] Are components orthogonal and decoupled?
- [ ] Are preconditions and postconditions handled?
- [ ] Does the code fail fast on errors?
- [ ] Have I used assertions for "impossible" states?
- [ ] Is the logic clear and un-clever?
- [ ] Are there tests that attempt to break the new functionality?
- [ ] Did I refactor smells before submitting?

## Correct causes at their source

- **"Fix it right, don't just make it work."**
- **Consolidate, Don't Duplicate:** If you find duplicate or parallel implementations (e.g., a JS registry and a TS registry), do not patch the one that "works" and force the system to use both.
  - **Action:** Merge the logic into the strictly better implementation (e.g., TypeScript) and delete the legacy/duplicate file.
- **Deep Fixes:** Do not write "glue code" to handle bugs in upstream logic. Fix the upstream logic.
