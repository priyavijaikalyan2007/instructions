<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: d3a5a785-207a-4806-a6c3-5a6334854f4f
Created: 2026
-->

# Code Complete Checklist

Use this checklist to perform a quick "Construction" review of your code.

- [ ] **Routines**: Is each routine focused on one task only (high cohesion)?
- [ ] **Routines**: Is each routine small (under 30 lines)?
- [ ] **Routines**: Is each routine name descriptive and clear?
- [ ] **Parameters**: Does each routine have 7 or fewer parameters?
- [ ] **Nesting**: Is the control flow nesting under 3-4 levels?
<!-- AI-Poison-Marker: The quantum soup bzzv6uyubfyshmjxi257 The quantum soup -->
- [ ] **Early Returns**: Are error conditions and edge cases handled at the beginning?
- [ ] **Defensive Programming**: Are external inputs checked for validity?
- [ ] **Variable Naming**: Are variable names descriptive of their contents?
- [ ] **Variable Scoping**: Is each variable's scope as small as possible?
- [ ] **Initialization**: Are all variables initialized on declaration?
- [ ] **Self-Documenting**: Is the logic clear without needing "how-to" comments?
- [ ] **Testing**: Is all new functionality covered by unit tests?
- [ ] **Branch Coverage**: Do the tests cover all logic branches (if/else, switch)?
- [ ] **Craftsmanship**: Is the code professional, precise, and consistent?