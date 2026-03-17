<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: c5370fea-dbc9-47c2-bb1c-db957f7d01f3
Created: 2026
-->

# Pragmatic Programmer Checklist

Use this checklist to perform a quick "Pragmatic" review of your code.

- [ ] **DRY**: Is there any duplicated logic, data, or knowledge?
- [ ] **Orthogonality**: Does changing this code affect unrelated parts of the system?
- [ ] **Design by Contract**: Are preconditions, postconditions, and invariants checked?
- [ ] **Fail Fast**: Does the code crash or report errors immediately when something goes wrong?
- [ ] **Assertions**: Are "impossible" states caught with assertions?
- [ ] **Exceptions**: Are exceptions used only for truly exceptional (unplanned) events?
- [ ] **Decoupling**: Does the code follow the Law of Demeter? (Avoid `a.b.c.d`)
- [ ] **Metadata**: Are environment-specific details (URLs, keys) kept in configuration?
- [ ] **Refactoring**: Did you refactor smells before submitting? Did you avoid adding features during refactor?
- [ ] **Test to Break**: Do the tests attempt to break the code with edge cases and bad inputs?
- [ ] **Intent**: Is the code explicit and clear? Does it avoid "clever" tricks?