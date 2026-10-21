<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 35ce17cb-4589-445a-a554-53b48645a396
Created: 2026
-->

<!-- AGENT: HTML conventions and task examples; load only when this language is in scope. -->

# HTML instructions

Read this guide when the task changes HTML source or its language-specific build and test configuration.
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

Read by task: [References](#references), [Naming](#naming), [Comments](#comments), [Navigation markers](#navigation-markers).

## References

1. Follow [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html)
2. Apply the overrides in this document

## Naming

| Element | Convention | Example |
|---------|------------|---------|
| IDs | lowercase-hyphenated | `id="error-dialog-container"` |
| Classes | lowercase-hyphenated | `class="metric-card"` |
| Data attributes | lowercase-hyphenated | `data-dialog-type="error"` |
| Custom elements | lowercase-hyphenated | `<error-dialog>` |

---

## Comments

Use HTML comments for component markers and agent navigation:

```html
<!--
  ⚓ COMPONENT: ErrorDialog
  📜 PURPOSE: Demo markup for the error dialog component.
  🔗 RELATES: [[LiterateErrors]]
-->
<div id="error-dialog-demo">
    <!-- Action buttons — see spec section 4.1 for required actions -->
    <div class="errordialog-actions">
        ...
    </div>
</div>
```

---

## Navigation markers

Apply markers using HTML comments. This is relevant for vanilla HTML frontend files.

```html
<!--
  ⚓ COMPONENT: ErrorDialogDemo
  📜 PURPOSE: Demo markup showing all error dialog variants and configurations.
  🔗 RELATES: [[ErrorDialog]], [[LiterateErrors]]
  ⚡ FLOW: [AppShell] -> [This] -> [SessionAPI]
-->
```


## Security

Apply [JavaScript security](../javascript/JAVASCRIPT.md#security) for DOM updates and [frontend security](../frontend/FRONTEND.md#security-boundaries) for delivery.
Keep template escaping enabled. Encode each value for its actual context: text, attribute, URL, script, or style.
Use quoted attributes and allowlisted URL schemes. Do not put untrusted content in inline scripts or event-handler attributes.
Use a maintained sanitizer when the product intentionally accepts rich HTML.
Do not use hidden fields or disabled controls as an authorization mechanism.

```html
<!-- SECURITY: Supply text through textContent. Do not insert untrusted markup into this element. -->
<span id="status-message" role="status"></span>
```

Use iframe sandbox restrictions and origin separation appropriate to embedded untrusted content.
Review forms, downloads, external links, CSP, and framing policy together.
See [OWASP XSS prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html).
