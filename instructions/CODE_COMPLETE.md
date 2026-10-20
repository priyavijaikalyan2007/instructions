<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 56e48bb8-298b-4f63-9543-dba7be79c7a4
Created: 2026
-->

<!-- AGENT: Shared construction guidance and integrated implementation lessons. -->

# Code Complete Instructions for Agents

This document outlines the core software construction principles and practices from *Code Complete* by Steve McConnell. All coding agents MUST adhere to these guidelines to ensure the production of high-quality, professional-grade software.

## 1. Quality Foundations

### Design as an Iterative Process
- **Mandate**: Software design is a process of discovery. Be prepared to revisit and refine design.
- **Application**: 
    - Don't settle for the first design that works.
    - If construction reveals a better design, refactor to it.

### Abstract Data Types (ADTs)
- **Mandate**: Group data and operations into cohesive ADTs.
- **Application**:
    - Avoid exposing raw data structures. Wrap them in a class or interface that defines its behavior.
    - Use interfaces or type aliases to represent domain-specific concepts (e.g., `CustomerId`, `OrderAmount`).

### Software Craftsmanship
- **Mandate**: Quality construction is about professionalism and precision.
- **Application**:
    - Always aim for "self-documenting" code. If you need a comment to explain "what" a line does, the code is likely unclear.
    - Use comments to explain "why" a design choice was made, not "how" the code works.

---

## 2. Construction Guidelines

### Routines (Methods and Functions)
- **Mandate**: Routines should be small, focused, and have high cohesion.
- **Application**:
    - **Cohesion**: A routine should do one thing and one thing only.
    - **Coupling**: Minimize dependencies between routines.
    - **Naming**: Use verbs and objects for routine names (e.g., `GetCustomerById`, `CalculateOrderTotal`).
    - **Size**: Routines should be no longer than 25-30 lines of code. If longer, refactor.
    - **Parameters**: Limit the number of parameters to 7 or fewer. If more are needed, pass a "parameter object."
    - *Note: Adhere to the routine size and parameter rules in [CODING_STYLE.md](CODING_STYLE.md).*

### Control Structures
- **Mandate**: Keep control flow simple and linear.
- **Application**:
    - Minimize nesting (stay under 3-4 levels).
    - Use "early returns" (guard clauses) to handle error conditions first.
    - Prefer `if-else` or `switch` over complex, multi-branch `if` statements.
    - Ensure loop conditions are clear and loops are small.

### Defensive Programming
- **Mandate**: Protect your code from invalid inputs and unexpected states.
- **Application**:
    - Check all external inputs for validity.
    - Use assertions to catch bugs in your own code during development.
    - Use exceptions to handle runtime errors that are "outside" your program's control.

---

## 3. Data and Variables

### Variable Naming
- **Mandate**: Choose variable names that accurately describe the data they hold.
- **Application**:
    - **Descriptive**: Names like `customerName` or `totalPrice` are better than `name` or `total`.
    - **Length**: Use names that are long enough to be clear, but not so long they become cumbersome.
    - **Avoid**: `tmp`, `data`, `obj`, `item` (unless in a very short loop).
    - *Note: Adhere to the naming conventions in [CODING_STYLE.md](CODING_STYLE.md).*

### Variable Scope and Lifetime
- **Mandate**: Keep the scope of a variable as small as possible.
- **Application**:
    - Declare variables close to where they are first used.
    - Do not use global variables. Use classes or state containers.
    - **Live Time**: Minimize the number of lines between the first and last use of a variable.

### Variable Initialization
- **Mandate**: Initialize variables as they are declared.
- **Application**:
    - Do not leave variables in an uninitialized or "junk" state.
    - If a language supports `const` or `readonly`, use it by default.

---

## 4. Construction Practices

### Pseudocode Programming Process (PPP)
- **Mandate**: Think before you code. Use pseudocode to design routines.
- **Application**:
    - Before implementing a complex routine, write out the logic in comments as a "blueprint."
    - Once the logic is sound, implement the code around the comments.

### Self-Documenting Code
- **Mandate**: Code should explain itself.
- **Application**:
    - Use descriptive names for variables, routines, and classes.
    - Use well-defined abstractions.
    - Use standard coding styles and patterns (as defined in [CODING_STYLE.md](CODING_STYLE.md)).
    - Only use comments for "non-obvious" logic, design decisions, or complex algorithms.

### Developer Testing
- **Mandate**: Developers are responsible for the quality of their code.
- **Application**:
    - Write unit tests for all public routines.
    - Test edge cases, boundary values, and error conditions.
    - Run the full test suite before submitting changes.

---

## 5. Checklist for Code Complete Agents

- [ ] Is the design iterative and refined?
- [ ] Are routines small, cohesive, and lightly coupled?
- [ ] Is the control flow simple and linear?
- [ ] Are variables initialized and scoped correctly?
- [ ] Is the code "defensively" written?
- [ ] Is the code self-documenting?
- [ ] Are all new routines covered by unit tests?
- [ ] Did I follow the "one thing per routine" principle?

## Direct type compatibility

This lesson concerns internal modules that share the same domain types.
API serialization boundaries retain their explicit contracts and mappings from [API_GUIDELINES.md](backend/API_GUIDELINES.md).

- **"Align the source, don't bridge the gap."**
- **Eliminate Converters:** If Module A produces data that Module B cannot consume directly:
  - **Do NOT** write a converter/mapper function between them if you own both modules.
  - **Action:** Refactor Module A or Module B so that their data types are identical.
- **Performance:** Unnecessary conversion layers waste CPU cycles and introduce points of failure.

## Architectural consistency

- **"Do not invent new patterns."**
- **Pattern Mimicry:** Before writing a new Controller, Service, or Component, examine three existing ones.
  - If existing Controllers use a Service layer, **do not** write a Controller that queries EF Core directly.
  - If existing Frontend components use `React Query`, **do not** write a component that uses `fetch` in `useEffect`.
  - If the backend uses the Repository pattern, **do not** introduce the Unit of Work pattern or direct `DbContext` usage in a single isolated area.

## Dependency discipline

- **"Use what is already there."**
- **Duplicate Check:** Before adding a package, check the project manifests and lockfiles for an existing dependency that meets the need.
  Include `Package.swift`, `go.mod`, `Cargo.toml`, Maven/Gradle files, `package.json`, and `.csproj` files where applicable. Adding a dependency requires justification.
  - If `Day.js` is installed, **do not** install `Moment.js`.
  - If `Newtonsoft.Json` is used, **do not** introduce `System.Text.Json` unless part of a documented migration.
- **Triviality Check:** Do not add libraries for trivial one-line functions (e.g., `is-odd`, `left-pad`). Write the helper function yourself.

## Hierarchical data

- **Recursive awareness:** If a data model is hierarchical (trees, checklists, folders), update logic **must** be recursive or use flattened ID lookups. Simple index-based access (`list[i]`) is forbidden for nested data.
