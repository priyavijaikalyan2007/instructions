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
    - *Note: Adhere to the routine size and parameter rules in [CODING_STYLE.md](./CODING_STYLE.md).*

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
    - *Note: Adhere to the naming conventions in [CODING_STYLE.md](./CODING_STYLE.md).*

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
    - Use standard coding styles and patterns (as defined in [CODING_STYLE.md](./CODING_STYLE.md)).
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
