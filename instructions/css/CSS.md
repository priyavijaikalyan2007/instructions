<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: b01da639-9dc7-4698-a8ee-8e70e15f32d4
Created: 2026
-->

<!-- AGENT: CSS conventions and task examples; load only when this language is in scope. -->

# CSS instructions

Read this guide when the task changes CSS source or its language-specific build and test configuration.
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

Read by task: [References](#references), [Naming](#naming), [Construction](#construction), [Comments](#comments), [Navigation markers](#navigation-markers), [Review checklist](#review-checklist).

## References

1. Follow [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)
2. Apply the overrides in this document

## Naming

| Element | Convention | Example |
|---------|------------|---------|
| Class names | lowercase-hyphenated | `.metric-card`, `.toolbar-actions` |
| Component prefix | component name | `.errordialog-header`, `.combobox-item` |
| BEM (if used) | block__element--modifier | `.card__header--compact` |

## Construction

Keep component selectors prefixed with the component name. Use the project's declared CSS framework and token conventions.

## Comments

Use `/* ... */` comments for CSS. Describe the component, state, accessibility reason, or non-obvious override.

## Navigation markers

```css
/*
 * ⚓ COMPONENT: ThinkerStyles
 * 📜 PURPOSE: Styles for the Thinker brainstorm canvas and idea bubbles.
 * 🔗 RELATES: [[SessionCanvas]]
 */
```

---

## Review checklist

- [ ] Component CSS classes prefixed with component name


## Security

Treat external styles and CSS values as untrusted content.
Do not insert arbitrary user text into stylesheets, selectors, `url()`, or inline styles.
Map user choices to predefined classes or validated values with explicit units and bounds.
Styles can trigger external requests or obscure trusted controls. Restrict remote fonts, imports, and images through delivery policy.
CSS hiding does not remove sensitive data from the DOM or enforce authorization.
Apply [HTML security](../html/HTML.md#security) and [frontend security](../frontend/FRONTEND.md#security-boundaries).
