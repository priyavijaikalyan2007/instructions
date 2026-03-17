<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 21f7e69d-baa7-42e1-bb60-60a8d618d7dc
Created: 2026
-->

<!-- AGENT: Approved and recommended libraries for the TypeScript/Bootstrap 5 frontend stack. -->

# Frontend Library Selection (Enterprise SaaS)

This document lists the approved and recommended libraries for the frontend of our Enterprise SaaS applications, adhering to the "Pure TypeScript + Bootstrap 5" stack guidelines.

**Core Stack:** Pure TypeScript, HTMX, HTML5, CSS3, Bootstrap 5+.

---

## 1. Core Architecture & Styling

### CSS Framework
1.  **Bootstrap 5+**
    *   **Usage:** Primary UI framework. Use the compiled CSS/JS bundles.
    *   **Customization:** Customize via SCSS variables (colors, fonts, spacing) rather than overriding CSS classes.
    *   **Icons:** **Bootstrap Icons** (preferred) or **FontAwesome 6 Free**.

### Interactivity & State
1.  **HTMX**
    *   **Why:** Enables server-driven interactions (swapping HTML partials) without complex client-side state management.
    *   **Usage:** Use for form submissions, infinite scrolling, tab switching, and updating content areas.
2.  **Alpine.js** (Use sparingly)
    *   **Why:** For small "islands of interactivity" (toggles, simple local state) where writing a full TypeScript class is overkill.
    *   **Constraint:** Do not build the entire app in Alpine.

### Build Tooling
1.  **Vite**
    *   **Why:** Fast, modern build tool for TypeScript. Handles bundling, minification, and HMR (Hot Module Replacement).
2.  **TypeScript**
    *   **Why:** Strict type safety is mandatory. No `.js` files allowed for new code.

---

## 2. Complex UI Components

### Data Grids / Tables
1.  **Grid.js**
    *   **Why:** Lightweight, dependency-free table plugin. Supports sorting, searching, pagination, and server-side data loading.
    *   **Integration:** Easy to style with Bootstrap themes.
2.  **Tabulator**
    *   **Why:** Enterprise-grade tables. Supports complex grouping, trees, freezing columns, and editing.
    *   **Integration:** Has a native Bootstrap 5 theme.

### Maps & Geospatial
1.  **Leaflet.js**
    *   **Why:** Primary choice for map-based applications. Lightweight and widely supported.
2.  **OpenLayers**
    *   **Why:** Alternative for complex geospatial projects requiring advanced features.

### Diagramming & Graphs
1.  **maxGraph**
    *   **Why:** **Recommended** for complex vector diagramming (UML, BPMN, Architecture).
    *   **Details:** Fork of `mxGraph` (powers draw.io). True vector shapes, multi-compartment support, TypeScript native.
2.  **Cytoscape.js**
    *   **Why:** **Recommended** for network graphs and simple relationship visualization.
    *   **Constraint:** Better for viewing networks than creating complex editable diagrams.

### Data Visualization (Charts)
1.  **Apache ECharts**
    *   **Why:** Comprehensive, enterprise-grade charting. Handles large datasets well.
2.  **Chart.js**
    *   **Why:** Lightweight, simple, and responsive. Good for basic dashboards.
3.  **D3.js**
    *   **Why:** For highly custom, low-level visualizations where standard charts aren't enough.

### Form Handling & Rich Text
1.  **Quill**
    *   **Why:** Modern, WYSIWYG rich text editor. Clean JSON output, easy to extend.
    *   **Bootstrap:** Styles easily to match inputs.
2.  **Choices.js**
    *   **Why:** Lightweight alternative to Select2. No jQuery dependency. Great for "multi-select" or searchable dropdowns.
3.  **Flatpickr**
    *   **Why:** Lightweight, powerful date/time picker. Zero dependencies.

### User Onboarding & Tours
1.  **Intro.js**
    *   **Why:** For step-by-step application walkthroughs and onboarding tours.
2.  **Driver.js**
    *   **Why:** Lightweight, vanilla JS alternative for highlighting elements.

---

## 3. Utilities & Helpers

### Date & Time
1.  **date-fns**
    *   **Why:** Modern, modular, and functional date library. Tree-shakeable (unlike Moment.js).
2.  **Day.js**
    *   **Why:** Tiny (2KB) alternative to Moment.js with a compatible API.

### Formatting & Input
1.  **Cleave.js**
    *   **Why:** For formatting input fields while typing (credit cards, phone numbers, dates).

### Notifications & Tooltips
1.  **Toastify-js**
    *   **Why:** Lightweight, dependency-free toast notifications.
2.  **Popper.js** (Included in Bootstrap)
    *   **Why:** Powering Bootstrap's tooltips and popovers. Use the Bootstrap API directly.

### Animations
1.  **Anime.js**
    *   **Why:** Powerful, lightweight animation engine for complex sequences.
2.  **Animate.css**
    *   **Why:** CSS-only classes for simple entrance/exit animations.

---

## 4. Testing & Quality

### Testing Frameworks
1.  **Playwright**
    *   **Why:** Preferred End-to-End (E2E) testing framework. Fast, reliable, and supports all modern browsers.
2.  **Vitest**
    *   **Why:** Unit testing framework. Native Vite integration, fast execution.

### Linting
1.  **ESLint**
    *   **Config:** Use `typescript-eslint` with strict rules.
2.  **Prettier**
    *   **Why:** Automatic code formatting to ensure consistency.