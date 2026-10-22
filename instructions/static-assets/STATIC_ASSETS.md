<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: d8953930-d828-44c8-ae2f-a8d9c2884e92
Created: 2026
-->

<!-- AGENT: Target routing and extracted existing guidance for static assets and distribution. -->

# Static assets and distribution

## Target scope

Source assets, compiled browser bundles, component-library output, static hosting, and CDN delivery.

## Topic references

| Work in scope | Existing guidance |
| --- | --- |
| Shared repository commands | [REPO.md](../REPO.md) |
| HTML markup | [HTML.md](../html/HTML.md) |
| CSS rules | [CSS.md](../css/CSS.md) |
| SCSS compilation and stylesheet rules | [SCSS.md](../scss/SCSS.md) |
| Browser scripting languages | [WORKFLOW.md](../WORKFLOW.md#select-language-guides) |
| Existing published artifact tests | [TEST_PLAN.md](../TEST_PLAN.md) |
| Publication and consumer contracts | [DOCUMENTATION.md](../DOCUMENTATION.md#verified-facts-and-published-contracts) |

## CDN and air-gap delivery

- Truly static browser assets may come from a content delivery network (CDN).

- For air-gapped environments, package required assets locally and serve them without external network dependencies.

## Source and compiled output

- When Vite is configured, keep its source/output mapping. Do not edit compiled JavaScript as a substitute for TypeScript source.

## Component-library build

- Use the library's declared stack, such as vanilla TypeScript, HTML, CSS/SCSS, Bootstrap, and Node.js build tools.

- Keep source components separate from generated bundles, generated documentation, and distribution output.

For component libraries, use the declared package scripts.

## Static source ownership

Apply the [shared folder convention](../REPO.md#source-assets-and-generated-output).
Use `src/service/<service-name>/static/` or `src/website/<website-name>/static/` for source copied without compilation.
Keep assets imported by a frontend build with that frontend's source.
Do not put generated JavaScript or CSS in editable static/ directories.
A runtime's wwwroot/, public/, or equivalent directory can receive assembled output from the build.
Record its input mapping and whether the directory contains authored source, generated output, or clearly separated portions.
Preserve established mappings in existing projects.
Source ownership does not select CDN delivery, container packaging, or an independent website.

## component-library layout

For a new reusable library, use `src/library/<library-name>/.`
The following paths are relative to that library's project root.

```text
components/<name>/     Component source, styles, and component-specific fixtures
scss/                  Shared variables and stylesheet source
assets/                Source icons, fonts, and other licensed assets
demo/                  Editable examples and integration scenarios
test/                  Library component and distribution tests, subject to toolchain conventions
scripts/               Library-specific build, bundle, and validation automation
```

Keep package manifests and lockfiles with the library.
Keep consumer documentation under root `docs/<library-name>/` and include required package documentation during the build.
Use root test/ for workflows that span the library and consuming applications.
Keep generated bundles, published demos, and generated API documentation in ignored output locations.
Preserve tool-required source and tests/ directories. Do not rename them merely to match the repository-wide test/ spelling.
Register new demos and guides in the library's discovery and publication pipeline.
Create a reusable library only when its public contract and ownership justify one. Avoid a general miscellaneous shared/ directory.

## static build and hosting example

This example applies only when the Theme component-library example is checked in PROJECT_PROFILE.md.
It does not select Cloudflare hosting or a library build for a Java SaaS container.
The selected library example uses this stack:

| Layer | Technology | Notes |
|-------|-----------|-------|
| Styling | SCSS (Sass) compiled to CSS | Bootstrap 5 variable overrides + custom component styles |
| Logic | TypeScript compiled to JavaScript | For interactive components only |
| Structure | HTML5 | Component templates and demo pages |
| Build | npm scripts, Sass CLI, PostCSS | No bundler (Webpack/Vite) unless components require it |
| Deployment | Cloudflare Pages via Wrangler | Static asset hosting |

**Do not introduce:**
- Use modern JavaScript (ES6+)
- JavaScript frameworks (React, Vue, Angular, Svelte)
- CSS-in-JS solutions (styled-components, Emotion)
- Complex bundlers unless a component genuinely requires module resolution

---

## theme resources

These URLs belong to the selected theme-library example. Other components use the catalog recorded in PROJECT.md.

- CSS Theme: https://theme.priyavijai-kalyan2007.workers.dev/css/custom.css
- Bootstrap JS: theme.priyavijai-kalyan2007.workers.dev/js/bootstrap.bundle.min.js

## browser bundling guidance

- Minimize library and framework overhead
- Use code splitting
- Implement lazy loading
- Optimize asset delivery
- Use modern bundling tools (Webpack, Vite)

## CDN component integration

**Fallback Code Prohibition:**
Do not substitute a component that reports fabricated data or success when initialization fails.
Follow the degraded-behavior rules in `instructions/PRAGMATIC_PROGRAMMER.md`. Report the failure and preserve the user's state.
When a shared component is defective, fix its source or report the defect through the project's workflow.

**Peer Dependency Loading:**
CDN components may wrap third-party libraries (e.g., MarkdownEditor wraps Vditor, Diagrams wraps
maxGraph). When adding a CDN component to an HTML page:
1. Check what peer dependencies the component requires (look for `window.X` checks or "library not
   found" error messages in the component source).
2. Load the peer dependency's CSS in `<head>` **before** the component's CSS.
3. Load the peer dependency's JS via `<script>` **before** the component's JS.
4. If you are unsure whether a peer dependency is needed, fetch the component JS and search for
   `window.` global checks or console error messages about missing libraries.

**API Signature Verification:**
Before calling a CDN component factory function, verify the actual function signature by reading the
component source. Do NOT guess parameter order or option names from memory. Common mistakes:
- Passing a single options object when the factory takes `(id: string, options)`.
- Using option names that don't exist (e.g., `theme`, `showToolbar` instead of `contained`,
  `showInlineToolbar`).
- Using invalid enum values (e.g., `mode: 'split'` instead of `mode: 'sidebyside'`).

**Toolbar State Management:**
When using the CDN Toolbar component, ALL button state changes must go through `toolbar.setToolState()`.
Never use direct DOM manipulation (`classList.toggle('active', ...)`) on toolbar buttons — this causes
the component's internal state to diverge from the visual state.

## asset caching

*   **Asset Caching**: Static assets (images, fonts, JS, CSS) must be served with long-term `Cache-Control` headers (e.g., `public, max-age=31536000, immutable`).

## stylesheet build checks

You must verify that `npm run build` completes without errors after every change to SCSS files. A broken build is never acceptable.

## asset loading and production output

*   **ES6 Modules**: Use native ES6 modules. Avoid heavy bundlers where vanilla modules suffice.
*   **Code Splitting**: Lazy load non-critical modules using dynamic imports (`import()`).
    See [JavaScript](../javascript/JAVASCRIPT.md#21-loading--bundle-size).
*   **Minification**: Ensure all production assets (JS/CSS) are minified (part of the build pipeline).
*   **Preloading**: Use `<link rel="preload">` for critical resources (fonts, main CSS, main JS).


## Security scope

Apply [general security](../SECURITY_GUIDELINES.md) and the selected language security sections.
Select clipboard, temporary storage, sensitive memory, and tenant-isolation controls when the changed behavior uses them.
For any AI or ML feature, also apply [AIML_SECURITY.md](../AIML_SECURITY.md).
