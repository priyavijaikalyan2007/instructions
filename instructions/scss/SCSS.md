<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: fb8a4298-2c88-4f8f-9aa4-185e54783fb8
Created: 2026
-->

<!-- AGENT: SCSS conventions and task examples; load only when this language is in scope. -->

# SCSS instructions

Read this guide when the task changes SCSS source or its language-specific build and test configuration.
Examples in instruction documents do not make a language part of the consuming project.
Start with references, formatting, naming, and file organization when those sections exist.
Read task sections as needed. Read pattern examples only for patterns selected during planning.
Shared policies remain in the topic guides. Read only the topics that apply to the task.
Do not weaken a shared requirement because this guide omits it.

Also read [CSS.md](../css/CSS.md) for shared selector naming and CSS rules.

Shared rules: [Style](../CODING_STYLE.md), [Comments](../COMMENTING.md), [Markers](../MARKERS.md), [Testing](../TESTING.md), [Logging](../LOGGING.md), [Performance](../PERFORMANCE.md), [Patterns](../GOF_PATTERNS.md).

Apply [shared style](../CODING_STYLE.md), including Allman braces, four-space indentation, and one type per file.
Use only the grammar exceptions stated in this guide.
If an example shows several top-level types, put each type in its own file in production.
Examples may omit surrounding project types or test fixtures. Use the repository's configured dependencies and contracts.

Read by task: [Naming](#naming), [SCSS construction](#scss-construction), [Comments](#comments), [Navigation markers](#navigation-markers), [Marker examples](#marker-examples), [Review checklist](#review-checklist).

## Naming

Use [CSS naming](../css/CSS.md#naming) for selectors and component prefixes.

| Element | Convention | Example |
|---------|------------|---------|
| SCSS variables | $lowercase-hyphenated | `$primary`, `$font-size-sm` |
| SCSS mixins | lowercase-hyphenated | `@mixin responsive-grid` |
| SCSS placeholders | %lowercase-hyphenated | `%visually-hidden` |

```scss
// Component-scoped class names
.errordialog-header
{
    background-color: $gray-900;
    color: white;
    padding: $spacer;
}

.errordialog-body
{
    padding: $spacer;
    font-size: $font-size-base;
}

.errordialog-suggestion
{
    color: $gray-600;
    font-style: italic;
}
```

## SCSS construction

### Variable Overrides

Always override Bootstrap variables in `_variables.scss`, not in component files.

```scss
// Good — in _variables.scss
$border-radius: 0 !default;

// Bad — in a component file
.my-component
{
    border-radius: 0; // Fights Bootstrap's default
}
```

### Nesting Depth

Limit SCSS nesting to 3 levels. Deep nesting produces overly specific selectors.

```scss
// Bad — too deep
.sidebar
{
    .nav
    {
        .nav-item
        {
            .nav-link
            {
                &:hover
                {
                    // 5 levels deep
                }
            }
        }
    }
}

// Good — flattened
.sidebar .nav-link
{
    // styles

    &:hover
    {
        // styles
    }
}
```

### Avoid `!important`

Never use `!important` in component SCSS. If a style is not applying, the selector specificity is wrong —
fix the selector, not the declaration.

The only exception is utility classes in the theme itself (e.g., `.p-compact`), where `!important` follows
Bootstrap's utility convention.

---

## Comments

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

## Navigation markers

Use `/* */` block comments so the header is preserved in unminified CSS output.

```scss
/*
 * ⚓ COMPONENT: MetricCard
 * 📜 PURPOSE: Styles for the metric card dashboard component.
 * 🔗 RELATES: [[EnterpriseTheme]], [[DashboardLayout]]
 */
```

## Marker examples

### 3. Global Concept Registry

```scss
// Metric label — uses the [[EnterpriseTheme]] small font size and muted colour
.metric-label {
    font-size: $font-size-sm;
    color: $gray-600;
}
```

### 4. Section Markers (Long Files)

```scss
// ============================================================================
// CUSTOM COMPONENT STYLES
// ============================================================================

// ============================================================================
// UTILITY CLASSES
// ============================================================================
```

## Review checklist

- [ ] SCSS nesting max 3 levels

- [ ] No `!important` in component SCSS


## Security

Apply [CSS security](../css/CSS.md#security) to the generated styles.
Compile trusted project source. Do not expose an unrestricted Sass compiler as a user-input transformation service.
Constrain import paths and custom build functions. Review build plugins and dependencies as executable code.
Keep credentials out of variables, generated CSS, and source maps.
