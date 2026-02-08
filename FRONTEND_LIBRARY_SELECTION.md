# Frontend Library Selection Guidelines (Enterprise SaaS)

This document outlines the mandatory criteria and preferred categories for selecting third-party libraries for the frontend of our Enterprise SaaS applications.

**Core Stack:** Pure TypeScript, HTMX, HTML5, CSS3, and Bootstrap 5+.
**Anti-Pattern:** Avoid heavy Single Page Application (SPA) frameworks like React, Angular, or Vue unless strictly necessary for a specific, isolated "island" of high complexity.

## 1. Selection Guidelines

When evaluating a frontend library, assess it against the following prioritized criteria:

### 1.1 Technology Alignment (Critical)
*   **Requirement:** Libraries must be compatible with **Vanilla TypeScript** and **standard DOM APIs**.
*   **Constraint:** Do *not* select libraries that require a specific framework runtime (e.g., "React Components", "Vue Plugins") unless they provide a standalone vanilla JS/TS adapter.
*   **Interactivity:** Preference for libraries that play well with **HTMX** (server-driven state) rather than managing complex client-side state.

### 1.2 Bootstrap Compatibility (Critical)
*   **Requirement:** Visual components must integrate seamlessly with **Bootstrap 5+**.
*   **Styling:** Libraries should either:
    *   Use standard Bootstrap classes natively.
    *   Allow extensive customization via SASS/CSS variables to match the Bootstrap theme.
    *   Not impose "Shadow DOM" styles that are impossible to override without hacks.
*   **JavaScript:** Prefer "Bootstrap Native" compatible libraries that do not depend on jQuery (Bootstrap 5 dropped jQuery).

### 1.3 TypeScript Support
*   **Requirement:** First-class TypeScript support is mandatory.
*   **Details:** The library must ship with high-quality `.d.ts` type definitions or be written in TypeScript. We want type safety across the entire codebase.

### 1.4 Performance & Bundle Size
*   **Requirement:** Libraries should be lightweight and modular (tree-shakeable).
*   **Goal:** Minimize initial page load time. Avoid importing huge monolithic libraries when a small utility function will do.

### 1.5 Observability & Debugging
*   **Requirement:** The library should emit meaningful errors and warnings to the browser console.
*   **Standard:** Errors should be readable and point to the root cause (e.g., "Invalid date format" vs "undefined is not a function").

### 1.6 Licensing & Longevity
*   **Requirement:** Open Source (MIT, Apache 2.0).
*   **Backing:** Maintained by established communities or companies. Avoid abandoned projects (no commits in >1 year).

---

## 2. Library Categories

Agents and engineers should select libraries for the following capabilities:

### Core Architecture
*   **Server-Driven UI:** Libraries for swapping HTML via AJAX (HTMX).
*   **Micro-Interactions:** Lightweight logic for toggles, dropdowns, etc., if Bootstrap JS is insufficient (Alpine.js is acceptable for small bits, but Vanilla TS is preferred).

### Styling & Design System
*   **CSS Framework:** Bootstrap 5+ (Customized via SCSS).
*   **Icons:** SVG-based icon sets that scale well and are standard (Bootstrap Icons, FontAwesome).
*   **Animations:** Lightweight CSS or JS animation libraries (e.g., Animate.css).

### Complex UI Components
*   **Data Grids/Tables:** High-performance tables with sorting, filtering, and pagination (Must support Bootstrap styling).
*   **Rich Text Editors:** WYSIWYG editors that output clean HTML.
*   **Form Controls:** Date pickers, select inputs (Select2 alternatives), and file uploaders that look native to Bootstrap.
*   **Modals & Toasts:** Extensions to standard Bootstrap implementations if more features are needed.

### Data Visualization
*   **Charting:** Charts and graphs for analytics dashboards. Must be responsive and themable.

### Utilities
*   **Date & Time:** Manipulation and formatting (e.g., date-fns, Day.js). *Avoid Moment.js due to size.*
*   **Formatting:** Numbers, currencies, and strings.
*   **Validation:** Client-side validation libraries that can integrate with server-side validation responses.

### Build & Quality
*   **Build Tooling:** Vite (preferred for speed) or Webpack.
*   **Linting & Formatting:** ESLint (TypeScript), Prettier.
*   **Testing:**
    *   **E2E:** Playwright (preferred) or Cypress.
    *   **Unit:** Vitest or Jest.
