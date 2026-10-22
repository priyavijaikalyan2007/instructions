<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 73503b77-47df-428c-a0bd-94cb17d79350
Created: 2026
-->

<!-- AGENT: Frontend development guidelines and architecture for the TypeScript/HTMX stack. -->

# Frontend and browser UI

## Target scope

Browser pages, dynamic UI, login flows, and reusable browser components.
API, authentication, synchronization, and permission sections apply to browser work that uses those features.
SaaS composition and asset compilation/delivery examples are linked separately.
Use the frontend framework and design system recorded in PROJECT.md.
Bootstrap, HTMX, the enterprise shell, and the supplied theme catalog are scoped implementation profiles, not consequences of having a browser frontend.
Read their sections only when that component uses the named stack or the corresponding project choice is checked.

## Topic references

| Work in scope | Existing guidance |
| --- | --- |
| Shared repository commands | [REPO.md](../REPO.md) |
| Common interaction and save safety | [UI_UX.md](../UI_UX.md) |
| Selected component behavior profiles | [UI_UX_COMPONENTS.md](../UI_UX_COMPONENTS.md) |
| Browser keyboard registry | [KEYBOARD.md](KEYBOARD.md) |
| Persistence integrity across adapters | [PERSISTENCE.md](../PERSISTENCE.md) |
| Browser TypeScript source | [TYPESCRIPT.md](../typescript/TYPESCRIPT.md) |
| Shared JavaScript source rules | [JAVASCRIPT.md](../javascript/JAVASCRIPT.md) |
| Page and template markup | [HTML.md](../html/HTML.md) |
| Browser stylesheets | [CSS.md](../css/CSS.md) |
| SCSS and Sass source | [SCSS.md](../scss/SCSS.md) |
| Shared browser logging | [FRONTEND_LOGGING.md](FRONTEND_LOGGING.md) |
| Reusable browser components | [COMPONENTS.md](COMPONENTS.md) |
| Component discovery | [MASTER_COMPONENT_LIST.md](MASTER_COMPONENT_LIST.md) |
| Static assets, bundling, and published output | [STATIC_ASSETS.md](../static-assets/STATIC_ASSETS.md) |
| Web application composition | [SAAS.md](../saas/SAAS.md) |

## Recommended source layout

For a new service UI, use `src/service/<service-name>/frontend/.`
For a reusable component library, use `src/library/<library-name>/` and its declared package layout.
Apply the [shared folder convention](../REPO.md#folder-and-file-structure). Preserve existing configured source paths.

Keep the frontend manifest, editable TypeScript, templates, styles, imported assets, and component tests in that frontend project.
Use the service's sibling static/ only for authored files copied directly without compilation.
Keep compiled bundles and assembled public files in ignored build output.
A framework-required public/ or wwwroot/ directory must have a documented source/output mapping.
Keep one editable source for each asset. Do not edit a copied or compiled version instead.
Use root `test/<service-name>/` for workflows spanning browser, backend, or native clients.
Separate deployment later through build and deployment configuration, without moving frontend source.

# 1. General Principles

## 1.1. Standards Compliance

- Use HTML5 and modern ECMAScript standards.
- Prioritize native HTML capabilities over complex JavaScript solutions.
- Ensure cross-browser compatibility (latest Chrome, Firefox, Safari, Edge).
- Maintain semantic HTML structure in all component templates and demo pages.
See [SAAS.md](../saas/SAAS.md#frontend-source-layout).

## 1.2. Performance Considerations

- Minimise DOM manipulations in component JavaScript.
- Use efficient selector methods (`getElementById`, `querySelector`).
- Leverage CSS for animations and transitions — avoid JavaScript animation where CSS suffices.
- Keep the compiled CSS output small; avoid generating redundant selectors.
- Do not import the entirety of a library when only a small part is needed.
- Implement lazy loading where appropriate
- Use event delegation for dynamic elements

## 1.3. Accessibility and Usability

- Implement WCAG 2.1 AA guidelines.
- Provide clear focus states on all interactive elements.
- Use semantic HTML elements (`<button>`, `<nav>`, `<table>`, not styled `<div>`s).
- Include appropriate ARIA attributes in component templates.
- Ensure keyboard navigability for all interactive components.
- Ensure responsive design for multiple device types.
- Maintain sufficient color contrast.
- Use legible font sizes.
- Support screen reader compatibility.

## 1.4. Error Handling

- Implement graceful error management, specifically literate errors as outlined in instructions/LITERATE_ERRORS.md.
- Provide user-friendly error messages
- Log errors for debugging
- Use try-catch blocks strategically

## 1.5. Recommended Technologies

This is the vanilla TypeScript/Bootstrap implementation profile. Apply it only when that frontend stack is configured.

- Use Bootstrap 5 as the primary UI and component framework.
- Use TypeScript with a simple compile step to convert into Javascript. Fallback to vanilla Javascript.
  Do not use overcomplicated technologies like React. For smaller, simpler, projects you can consider using
  vanilla Javascript.
- Use CSS Grid / Flexbox for layouts.
- Target modern, standards compliant web browsers ignoring older web browsers like Internet Explorer.
- Use the Fetch API for AJAX API calls.
- Use Service Workers for long running sync-style operations.
- Use web components for reusable elements.

## 1.6. Code Generation Best Practices

- Prefer composition over inheritance.
- Use immutable data structures where possible.
- Minimize global variables.
- Implement defensive programming techniques.
See [SAAS.md](../saas/SAAS.md#cross-layer-data-mapping).

## 1.7. Error Handling

- Use try-catch blocks in component TypeScript where DOM operations could fail.
- Log errors using `console.error` with the `[ComponentName]` prefix (see `instructions/LOGGING.md`).
- Never use `window.alert()` or `window.confirm()` in component code.
- Fail gracefully: if a component cannot initialise, log the error and leave the DOM unchanged.

## 1.8. Browser Compatibility

- Support latest versions of:
  - Chrome
  - Firefox
  - Safari
  - Edge
- Provide graceful degradation for older browsers

## 1.9. Security Considerations

Whether we are building an application or a component library or a theme library, security matters.

See [FRONTEND.md](#web-application-authentication).
- Use HTTPS for all communications.
- Sanitise any user-provided content before injecting it into the DOM in component TypeScript.
  Use `textContent` instead of `innerHTML` where possible. Sanitize user input in all components.
- Prevent XSS and CSRF vulnerabilities in all components.
- Do not include inline event handlers (`onclick="..."`) in component HTML templates.
- Do not embed external scripts.

## 1.10. Browser Compatibility

Support the latest versions of:

- Chrome
- Firefox
- Safari
- Edge

Do not support Internet Explorer. Use modern CSS features (Grid, Flexbox, custom properties) freely.
The PostCSS autoprefixer handles vendor prefixes for supported browsers.

## 1.11. Commenting & Logging

You must follow the same logging and commenting model as the backend for the frontend.
See instructions/COMMENTING.md and instructions/LOGGING.md. Again, in the frontend, make sure to log:

1. Method/Function Entry/Exit

   - Log function name
   - Log input parameters (scrubbed of sensitive data)
   - Log return values or error conditions
   - Include timing information when relevant

2. External Service Interactions

   - Log remote request details
   - Log response status
   - Log request/response sizes
   - Capture request/response timestamps
   - Omit sensitive payload details

3. Error and Exception Handling

   - Log full error stack traces
   - Capture error context and triggering conditions
   - Include relevant application state information

4. State Changes

   - Log significant state transitions
   - Record user actions leading to state changes
   - Capture system events and configuration modifications

### 1.11.1. Logging Best Practices

- Use structured logging.
- Include correlation IDs to track request flows.
- Implement log levels (DEBUG, INFO, WARN, ERROR).
- Ensure logs are easily parseable by log management tools.

### 1.11.2. Example Logging Structure

```javascript
function processUserOrder(userId, orderDetails) {
  logger.info('Processing user order', {
    userId: userId,
    orderSize: orderDetails.items.length,
    timestamp: new Date().toISOString()
  });

  try {
    // Order processing logic
    logger.debug('Order processing steps', {
      stage: 'validation',
      isValid: true
    });
  } catch (error) {
    logger.error('Order processing failed', {
      userId: userId,
      errorMessage: error.message,
      errorCode: error.code
    });
    throw error;
  }
}
```

### 1.11.3. Performance Considerations

- Implement efficient logging mechanisms
- Use asynchronous logging to minimize performance impact

### 1.11.4. Security Reminders

- Never log:
  - Authentication credentials
  - Session tokens
  - Personal identification information
  - Encryption keys
- Sanitize and mask sensitive data before logging

## 1.12. Application Structure

See [SAAS.md](../saas/SAAS.md#super-app-shell).

## 2. Technology Stack

See [STATIC_ASSETS.md](../static-assets/STATIC_ASSETS.md#static-build-and-hosting-example).

# 3. UI Framework and Styling

## 2.1. Core Resources

See [STATIC_ASSETS.md](../static-assets/STATIC_ASSETS.md#theme-resources).

## 2.2. Styling Principles

Bootstrap and the theme catalog below apply only to that configured design system. Other frontends use their declared tokens and catalog.

1. Prefer vanilla Bootstrap styles.
2. Write custom CSS/JS/Typescript only when absolutely necessary.
3. Prioritize functional design with accessibility considerations over fancy animations etc.
4. Maintain consistent color schemes, typography, and layout across applications.
5. Ensure responsive design for multiple device types.
6. Start at `https://theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_REFERENCE.md` to determine availabe
   or to be built components. Do not invent new components yourself.

# 3. User Experience Standards

## 3.1. Keyboard Navigation

- Implement standard keyboard shortcuts. See instructions/frontend/KEYBOARD.md for guidance.
- Ensure logical tab order for form and interactive elements

## 3.2. UI Interaction Patterns

- Implement context-appropriate:
  - Panning
  - Zooming
  - Fit to window
  - Grid snapping
  - Auto layout features

## 3.3. Help and Onboarding

- Include help buttons for complex input elements
- Develop walkthrough guides for each application
- Provide contextual tooltips and explanations

## 3.4. Accessibility Guidelines

### 3.4.1. Accessibility Hierarchy

- Prioritize application functionality
- Implement accessibility features without compromising core functionality
- Recognize that some complex interactions may limit full accessibility

## 3.5. Performance Optimization

- Minimize external library dependencies
- Use lazy loading for components
- Optimize asset delivery
- Implement efficient state management

# 4. Framework & Library Selection Principles

## 4.1. General Approach

- Prioritize existing, well-maintained libraries and frameworks
- Prefer open-source solutions
- Select libraries with:
  - Active maintenance
  - Good documentation
  - Strong community support
  - Performance optimization
  - Regular security updates

## 4.2. Recommended Libraries by Function

### 4.2.1. Mapping

- Leaflet.js: Primary choice for map-based applications
- OpenLayers: Alternative for complex geospatial projects

### 4.2.2. Data Visualization

- D3.js: Highly customizable, complex visualizations
- Google Charts: Simple, quick charting
- Apache ECharts: Comprehensive charting
- Charts.js: Lightweight, responsive charts
- Highcharts: Enterprise-grade visualization
- Grid.JS: Enterprise grade tabular data visualization with sorting, searching, pagination, coloring etc.

### 4.2.3. User Experience

- IntroJS: Application walkthroughs
- Popper.js: Tooltips and popovers
- AnimeJS: Advanced animations
- jQuery: DOM manipulation (if necessary)

### 4.2.4. Form Handling

- SurveyJS: Dynamic form building
- Alpaca: Complex form generation
- Cleave.js: Input formatting

### 4.2.5. Datetime & Localization

- MomentJS: Datetime manipulation
- date-fns: Modern datetime library

### 4.2.6. Diagramming & Graph Visualization

**Simple Graph/Network Visualization:**
- Cytoscape.js: Network graphs, node-link diagrams, simple flowcharts
  - Best for: relationship visualization, network topology, simple graphs
  - Limitations: Single label per node, limited shape complexity

**Complex Vector Diagramming (Recommended):**
- maxGraph (Apache 2.0): Full-featured diagramming library
  - Fork of mxGraph (powers draw.io/diagrams.net)
  - True vector shapes (SVG-based, resizable without loss)
  - Multi-compartment shapes (UML classes with properties/methods)
  - Built-in support for: UML, BPMN, flowcharts, ER diagrams
  - Multiple editable text areas per shape
  - Professional stencil/shape library support
  - Works with vanilla JS/TypeScript (no React/Vue required)
  - Best for: enterprise diagramming, UML, architecture diagrams, complex flowcharts

**When to Use Which:**
| Use Case | Recommended Library |
|----------|---------------------|
| Network/graph visualization | Cytoscape.js |
| Simple flowcharts (basic shapes) | Cytoscape.js |
| UML diagrams | maxGraph |
| BPMN/process diagrams | maxGraph |
| Architecture diagrams (C4, cloud) | maxGraph |
| Complex shapes with compartments | maxGraph |
| Resizable vector shapes | maxGraph |

**Note:** GoJS is powerful but requires a commercial license for production use.

## 4.3. Best Practices

- Modular code design
- Responsive layouts
- Performance optimization
- Accessibility compliance
- Cross-browser compatibility
- Consistent coding standards

## 4.4. Performance Considerations

See [STATIC_ASSETS.md](../static-assets/STATIC_ASSETS.md#browser-bundling-guidance).

## 4.5. Security Guidelines

- Sanitize user inputs
- Implement proper authentication flows
- Use HTTPS
- Protect against XSS and CSRF
- Keep dependencies updated
- Follow OWASP guidelines for web applications.

## 4.6. Recommended Toolchain

- Framework: Bootstrap 5.0
- Code: TypeScript
- Styling: Bootstrap, or CSS Modules
- Testing: Jest

# 5. API Centric Thinking

## 5.1. General Principles

### 5.1.1. API and Data Management

1. Backend API Integration

   - Create individual JavaScript functions for each significant backend API
   - APIs should cover core actions:
     * Data loading
     * Data saving
     * Authentication
     * Session management
     * Settings modifications
     * Import/Export functions
     * AI/ML provider interactions

2. Local Storage and Synchronization

   - Use browser's localStorage as primary local cache
   - Implement background synchronization mechanisms using ServiceWorkers.
   - Sync edits to server:
     * Immediate background sync for critical updates
     * Periodic sync for non-critical changes
   - Provide placeholder functions for future API implementations

## 5.2. Initial Development Setup

### 5.2.1. Backend API Hosting

See [BACKEND.md](../backend/BACKEND.md#api-organization).

## 5.3. Frontend Function Pattern

```javascript
async function apiFunction(parameters) {
  try {
    // Placeholder for API call
    const response = await fetch('/api/endpoint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(parameters)
    });

    if (!response.ok) {
      throw new Error('API request failed');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    // Implement appropriate error handling
  }
}
```

## 5.4. Key Considerations

- Always handle potential API failures
- Implement proper logging (see instructions/LOGGING.md)
- Provide user-friendly error messages
- Ensure responsive design
- Optimize performance
- Maintain clean, readable code

# 7. Data Centric Thinking

## 7.1. Core Principles

### 7.1.1. Data-Centric Design Philosophy

- Prioritize data structure and flow over visual presentation
- Represent all data as JSON objects
- Implement data management as primary concern before UI design

## 7.2. Data Management Strategies

### 7.2.1. JSON-First Approach

- All data must be structured as JSON
- Use consistent JSON schemas across frontend and backend
- Implement universal data transformation functions
- Support both local storage and API-based data retrieval

### 7.2.2. Data Synchronization Considerations

- Implement eTags for version tracking
- Create delta detection mechanisms
- Support optimistic and pessimistic update models
- Handle concurrent editing scenarios

## 7.3. Technical Implementation Guidelines

### 7.3.1. Storage Mechanisms

- Prefer JSON-based storage solutions
- Use browser localStorage/sessionStorage
- Implement IndexedDB for complex data structures
- Design fallback mechanisms for storage failures

### 7.3.2. API Interaction Patterns

- Use consistent data transfer protocols
- Implement robust error handling
- Support partial data updates
- Design for graceful network interruptions

### 7.3.3. State Management

- Use immutable data structures
- Implement unidirectional data flow
- Minimize complex state mutations
- Prefer reactive programming paradigms

## 7.4. Recommended Technologies

- React with TypeScript
- Redux or MobX for state management
- Axios for API interactions
- JSON Schema for data validation

### 7.4.1. Performance Considerations

- Minimize unnecessary re-renders
- Implement efficient data serialization
- Use memoization techniques
- Optimize JSON parsing and transformation

### 7.4.2. Security Principles

- Sanitize all incoming JSON data
- Implement strict type checking
- Use JSON.parse() with reviver functions
- Validate data schemas before processing

# 8. Sub-Application Structure

See [SAAS.md](../saas/SAAS.md#sub-application-structure).

## 8.1. Super-App Model

See [SAAS.md](../saas/SAAS.md#sub-application-structure).

## 8.2. UI Layout

See [SAAS.md](../saas/SAAS.md#sub-application-structure).

## 8.3. UI Behaviors

See [SAAS.md](../saas/SAAS.md#sub-application-structure).

# 9. Access Control UI Patterns

The permission services, field names, and sharing APIs below implement the selected Knobby authorization example.
Other clients reflect their own server contract. Native platform permissions and share sheets use instructions/apps/APPS.md.

## 9.1. Access Level Indicator

All applications with sharing functionality should display the user's access level prominently.

### 9.1.1. Access Level Badge

Display a badge in the toolbar showing the user's access level:

```html
<span id="access-level-indicator" class="access-level-badge" style="display: none;"></span>
```

### 9.1.2. Badge Styling

```css
.access-level-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.5rem;
    font-size: 0.625rem;
    font-weight: 500;
    border-radius: 0.25rem;
    white-space: nowrap;
}

.access-level-badge.owner {
    background: #dcfce7;
    color: #166534;
}

.access-level-badge.editor {
    background: #dbeafe;
    color: #1e40af;
}

.access-level-badge.viewer {
    background: #fef3c7;
    color: #92400e;
}

.access-level-badge.commenter {
    background: #f3e8ff;
    color: #6b21a8;
}
```

## 9.2. Disabling Edit Controls for Viewers

When a user has view-only access, disable all editing functionality.

### 9.2.1. UI Elements to Disable

- Mode buttons (Edit, Link modes)
- Save/Undo/Redo buttons
- Delete buttons
- Paste/Layout buttons
- Make text inputs readonly
- Disable canvas editing (node creation, linking)

### 9.2.2. Implementation Pattern

```javascript
let currentAccessLevel = null;
let canEditSession = true;

function updateAccessLevelUI() {
    const indicator = document.getElementById('access-level-indicator');

    if (!currentAccessLevel || !currentResource) {
        indicator.style.display = 'none';
        canEditSession = true;
        return;
    }

    // Show badge
    indicator.style.display = 'inline-flex';
    indicator.className = 'access-level-badge ' + currentAccessLevel;

    const labelMap = {
        'owner': 'Owner',
        'editor': 'Can Edit',
        'viewer': 'View Only',
        'commenter': 'Can Comment'
    };
    indicator.textContent = labelMap[currentAccessLevel] || currentAccessLevel;

    // Determine capabilities
    canEditSession = currentAccessLevel === 'owner' || currentAccessLevel === 'editor';
    const canDelete = currentAccessLevel === 'owner';

    // Disable buttons
    document.getElementById('btn-delete').disabled = !canDelete;
    document.getElementById('btn-save').disabled = !canEditSession;
    document.getElementById('btn-undo').disabled = !canEditSession;
    document.getElementById('btn-redo').disabled = !canEditSession;

    // Make inputs readonly
    document.querySelectorAll('.editable-input').forEach(input => {
        input.readOnly = !canEditSession;
    });

    // Log view-only mode
    if (!canEditSession) {
        logInfo('View-only mode - editing disabled');
    }
}
```

### 9.2.3. Protecting Edit Functions

Guard all editing functions to prevent viewers from making changes:

```javascript
function createNode(x, y, label) {
    if (!canEditSession) {
        logInfo('View-only mode - cannot create nodes');
        return;
    }
    // ... node creation logic
}

function saveEdit() {
    if (!canEditSession) {
        logInfo('View-only mode - cannot save edits');
        return;
    }
    // ... save logic
}

function setMode(mode) {
    // Prevent viewers from entering edit modes
    if (!canEditSession && (mode === 'edit' || mode === 'link')) {
        logInfo('View-only mode - cannot switch to ' + mode + ' mode');
        return;
    }
    // ... mode switching logic
}
```

## 9.3. Loading Access Level from API

When loading a resource, extract and apply the access level from the API response:

```javascript
async function loadResource(id) {
    const response = await api.getResource(id);

    currentResource = response;
    currentAccessLevel = response.access_level || 'owner';

    logInfo('Resource access level: ' + currentAccessLevel);

    // Render resource
    renderResource();

    // Update UI based on access level
    updateAccessLevelUI();
}
```

## 9.4. Share Button Behavior

The Share button should always be visible but behave differently based on access:

- **Owners**: Can view and modify sharing settings
- **Editors/Viewers**: Can view sharing settings (read-only)

```javascript
function shareResource() {
    if (!currentResource) {
        alert('Please select a resource first.');
        return;
    }

    // Share modal handles read-only display for non-owners
    ShareModal.open({
        resourceNamespace: 'myapp',
        resourceType: 'resource',
        resourceId: currentResource.id,
        resourceName: currentResource.name || 'Untitled',
    });
}
```

## 9.5. Disabling Canvas Interactions for Viewers

For canvas-based diagramming applications, viewers must not be able to drag or edit elements.

### Cytoscape.js Settings

```javascript
// In updateAccessLevelUI()
if (!canEditSession) {
    // Disable node dragging
    cy.autoungrabify(true);
    cy.boxSelectionEnabled(false);
} else {
    cy.autoungrabify(false);
    cy.boxSelectionEnabled(true);
}
```

### Cytoscape.js Key Methods

| Method | Effect |
|--------|--------|
| `cy.autoungrabify(true)` | Prevents all nodes from being grabbed/dragged |
| `cy.boxSelectionEnabled(false)` | Disables rectangular selection |
| `setMode('pan')` | Force pan mode for navigation only |

### maxGraph Settings

```javascript
// In updateAccessLevelUI()
if (!canEditSession) {
    // Disable all editing
    graph.setEnabled(false);
    graph.setCellsMovable(false);
    graph.setCellsResizable(false);
    graph.setCellsEditable(false);
    graph.setConnectable(false);
} else {
    graph.setEnabled(true);
    graph.setCellsMovable(true);
    graph.setCellsResizable(true);
    graph.setCellsEditable(true);
    graph.setConnectable(true);
}
```

### maxGraph Key Methods

| Method | Effect |
|--------|--------|
| `graph.setEnabled(false)` | Disables all graph interactions |
| `graph.setCellsMovable(false)` | Prevents cells from being dragged |
| `graph.setCellsResizable(false)` | Prevents cells from being resized |
| `graph.setCellsEditable(false)` | Prevents in-place text editing |
| `graph.setConnectable(false)` | Prevents creating new connections |

## 9.6. Authentication Check Patterns

Each app uses a different API wrapper. Always use the correct one.

```javascript
// CORRECT - use app-specific API
if (!app || !app.useBackend) {
    alert('Please log in.');
    return;
}

// INCORRECT - window.api may not exist in all apps
if (!window.api || !window.api.isAuthenticated()) { ... }
```

## Browser scripting

- Use TypeScript for non-trivial browser scripting, with HTML, CSS/SCSS, and the declared component library.

## Component-library contracts

- Document each component's factory, options, events, public types, state capture/restore, dependencies, and cleanup contract.

- Use unit, browser, accessibility, visual, and consumer-artifact checks as appropriate.

- The consuming application owns authentication, persistence, and the host logging pipeline.

## component-reuse workflow

Use the component catalog recorded in PROJECT.md before implementing a replacement.
The URL workflow below applies only when the supplied theme catalog is selected for the component.

- Before building new browser UI components, always consult the file
  `https://theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_INDEX.md` to see
  if a reusable component exists. If a resuable component exists, then consult
  `https://theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_REFERENCE.md`
  to look up the component and related documentation.
  If no resuable component exists, then check
  `https://theme.priyavijai-kalyan2007.workers.dev/docs/MASTER_COMPONENT_INDEX.md` to see if a
  component yet to be built will fit your needs. If so, then request that the component be built instead.
  If you have the permissions to do so, you may file a GitHub issue to the repository
  `https://github.com/priyavijaikalyan2007/b2btheme`
  Finally, if no existing component fits the need and none of the components in the master list suffice,
  produce a specification for the resuable UI components and then wait for the user to confirm that the
  components are available for use before proceeding. This ensures that UI code uses cleanly built resuable
  components with standardized repeatable patterns and not AI slop.
  You may also file an issue to the repository `https://github.com/priyavijaikalyan2007/b2btheme` asking for
  the new component. Include the specification in the issue.

## Frontend library selection

- When selecting libraries for frontend functionality, always consult instructions/frontend/FRONTEND_LIBRARY_SELECTION.md for guidelines
  and instructions/frontend/FRONTEND_SELECTION.md for pre-canned recommendations.

## web application authentication

- Implement secure authentication mechanisms.

## component state

Every component should provide a mechanism to export and import its current UI state.
That is, what node is selected, whether nodes are expanded or collapsed, whether a sidebar is
expanded or collapsed, which ribbon tools are selected and more. This enables consuming applications to
integrate UI state preservation and reload into their user experience.

## browser testing

The following framework examples apply to browser frontend tests. Retain the project's configured runner for server-side JavaScript.

**Unit Tests:**
- Use Jest or Vitest as the test runner
- Test React components with React Testing Library
- Test hooks with @testing-library/react-hooks
- Mock API calls with MSW (Mock Service Worker)

**Integration Tests:**
- Test component interactions
- Test API client functions against mock servers

**E2E Tests:**
- Use Playwright for browser automation
- Test critical user flows end-to-end

## browser performance guidance

### 2.1 Loading & Bundle Size

See [STATIC_ASSETS.md](../static-assets/STATIC_ASSETS.md#asset-loading-and-production-output).

### 2.2 Rendering & DOM
*   **Minimize Reflows**: Avoid "layout thrashing." Read layout properties (e.g., `offsetHeight`) first, then write style changes. Do not interleave them.
*   **Batch DOM Updates**: Use `DocumentFragment` to append multiple elements at once.
*   **Virtualization**: For lists with > 100 items, use "virtual scrolling" (rendering only visible items).
*   **CSS Selectors**: Avoid complex, deep selectors. Use simple class selectors (BEM-style preferred).
*   **Animations**: Use CSS `transform` and `opacity` for animations. These run on the compositor thread. Avoid animating `top`, `left`, `width`, or `height`.

### 2.3 Local Storage & Caching strategy
*   **Aggressive Caching**: Use `localStorage` or `IndexedDB` to cache user data (e.g., session lists, diagrams).
    *   *Pattern*: "Stale-While-Revalidate". Show cached data immediately, then fetch updates in the background.
See [STATIC_ASSETS.md](../static-assets/STATIC_ASSETS.md#asset-caching).

### 2.4 Memory Management
*   **Event Listeners**: Always remove event listeners when components/elements are destroyed to prevent memory leaks.
*   **Large Objects**: Avoid keeping large datasets in global scope.
*   **WeakMap/WeakSet**: Use `WeakMap` for associating data with DOM elements to ensure garbage collection works.

### 2.5 Service Workers & Background Tasks
*   **Local-First Architecture**: For data-heavy apps (like "Thinker"), writes should go to `localStorage` or `IndexedDB` immediately.
    *   **Background Sync**: Use a Service Worker to sync local changes to the server in the background. This keeps the UI responsive even during network latency or outages.
*   **Offloading Work**: Move heavy computations (e.g., parsing large datasets, complex geometry calculations, loading heavy tool palettes) to a **Web Worker** or **Service Worker**.
    *   *Rule*: If a task takes > 50ms, it should not be on the main thread.

---

## browser performance budgets

*   **Budget**:
    *   **First Contentful Paint (FCP)**: < 1.0s
    *   **Time to Interactive (TTI)**: < 1.5s
    *   **Interaction to Next Paint (INP)**: < 200ms

## browser UI thread guidance

*   The UI thread must never be blocked.
*   Offload heavy computation to Web Workers or the backend.
*   Yield to the main thread frequently during long tasks.

---

## browser performance checks

*   **Lighthouse**: Run Chrome Lighthouse audits on frontend pages regularly.

## Bootstrap discipline

Apply these rules only to components built with the configured Bootstrap theme.

- **"Override, don't overwrite."**
- **Variables First:** When changing the appearance of any Bootstrap element, modify `_variables.scss` before writing custom CSS. If Bootstrap provides a variable for the property, use it.
- **No Hardcoded Values:** Never hardcode hex colours (e.g., `#FF0000`), pixel sizes, or font stacks in component SCSS or HTML. Use the semantic names defined in `_variables.scss` (e.g., `$danger`, `$font-size-sm`, `$spacer`).
- **Unit Consistency:** Do not mix `px`, `rem`, `em`, and `%` arbitrarily. Follow the spacing scale in `_variables.scss`. Use `rem` for sizing, `px` only for borders and fine details (1px borders, box shadows).
- **Explicit Dependencies:** If a component requires Bootstrap JavaScript (e.g., `bootstrap.Modal`), document this in the component's README and in `instructions/frontend/COMPONENTS.md`.

## component boundaries

- **"Components are guests, not owners."**
- **No Global Side Effects:** A component's SCSS must not modify global Bootstrap styles, override utility classes, or change the behaviour of elements outside its own scope.
- **Namespace Classes:** Prefix all custom classes with the component name (e.g., `.errordialog-header`, `.combobox-dropdown`). Do not use generic class names like `.header` or `.dropdown-list` that could collide with Bootstrap or the host application.

## styling consistency

- **"Single Source of Truth."**
- **Framework Purity:** If the project uses Tailwind CSS, **do not** write inline `style={{ ... }}` or create separate `.css` files.
- **Unit Consistency:** Do not mix `px`, `rem`, `em`, and `%` arbitrarily. Inspect `tailwind.config.js` or `variables.css` and use the defined spacing/color scales.
- **Color Variables:** Never hardcode hex codes (e.g., `#FF0000`). Use the semantic names defined in the theme (e.g., `text-error`, `bg-primary`).

## component tests

When building TypeScript components, add unit tests using Jest or Vitest that verify:
- The component initialises correctly with valid inputs.
- The component handles missing or invalid inputs gracefully (logs a warning/error, does not throw).
- The component produces the expected DOM structure.

## component visual checks

Use the configured demo or integration surface for the affected component.
The demo/index.html path below belongs to the selected theme component-library example.

After any theme or component change, open `demo/index.html` in a browser and visually verify that:
- No existing components are broken.
- New components render as specified.
- Colours, spacing, and typography are consistent with the theme.

## browser workflow tests

You must add Playwright end-to-end tests for all user-facing changes.

## canvas sizing

- **Explicit Dimensions:** For canvas/visualization libraries (Cytoscape, maxGraph), **never** rely on CSS flexbox/grid alone. Always enforce or check for explicit pixel dimensions (`getBoundingClientRect()`) before initialization.

## browser dependency restriction

This restriction applies to the configured vanilla component-library profile. Other components retain their declared framework.

- **No UI Frameworks:** Do not install React, Vue, Angular, jQuery, or any UI framework. This is explicitly prohibited by the project's architecture.

## UI error propagation

- **UI Propagation:** Follow [error placement](../UI_UX.md#error-placement). Visible forms show inline errors or a persistent summary.
- Use the configured literate error dialog for failed commands without a suitable visible error surface, such as Save on a canvas.
- Keep transient notifications consistent with the host. Do not replace an actionable failure with a console-only log or native browser alert.

## stylesheet cleanup

- **No Dead CSS:** If a refactor removes a component or class, delete the corresponding styles. Do not leave orphaned selectors.

## progressive data rendering

*   **Purpose:** Split a large object's retrieval into "Shallow" (immediate UI rendering) and "Deep" (lazy-loading expensive details like history or attachments).
*   **Implementation:** Render metadata first; lazy-load details via HTMX or `IntersectionObserver`.

## Visible data first

4.  **Default to Partial Hydration**: Only load what is immediately visible. Use "View More" or tabs for deep data.

## Browser familiarity and placement examples

Users shouldn't have to relearn how to use a computer when they use our software.
*   **Standard Shortcuts:** `Ctrl+C` must copy. `Ctrl+Z` must undo. `Esc` must close modals or cancel actions.
*   **Standard Locations:** The "Close" button goes in the top-right. The "Save" button goes at the bottom-right of a form (or top-right of a sticky header).
*   **Fitts's Law:** Make important targets (like "Save" or "Delete") large and easy to click. Place related controls close to each other.

## Browser visual examples

The Bootstrap grid, font sizes, and color palette below are examples for that configured design system.

### 3.1. Color & Contrast
*   **Semantic Colors:**
    *   <span style="color:blue">**Primary (Blue/Brand)**</span>: Main actions (Save, Submit, Create).
    *   <span style="color:green">**Success (Green)**</span>: Confirmation messages, successful states.
    *   <span style="color:red">**Danger (Red)**</span>: Destructive actions (Delete, Remove).
    *   <span style="color:orange">**Warning (Yellow/Orange)**</span>: Non-blocking issues, alerts.
    *   <span style="color:gray">**Neutral (Gray)**</span>: Secondary actions (Cancel), borders, dividers.
*   **Accessibility:** Ensure a contrast ratio of at least 4.5:1 for text against its background.

### 3.2. Typography
*   **Hierarchy:** Use font size and weight to establish order.
    *   `h1`: Page titles.
    *   `h2`: Section headers.
    *   `h3`: Card/Panel headers.
    *   `body`: Standard readable text (14px-16px).
    *   `small`: Metadata, help text.
*   **Readability:** Keep line lengths between 45-75 characters for comfortable reading.

### 3.3. Spacing & Layout
*   **White Space:** Use white space to group related elements. Elements close together are perceived as related (Law of Proximity).
*   **Grid System:** Use the Bootstrap grid (Rows/Cols) to ensure alignment. Everything should align to a conceptual grid.
*   **Consistency:** Use consistent margins and padding (e.g., always `1rem` or `16px` between cards).

## Browser feedback surfaces

*   **Hover:** Interactive elements must have a hover state to indicate clickability.
*   **Focus:** Focus rings are mandatory for accessibility. Never remove `outline: none` without replacing it.
*   **Loading & Progress (Crucial):**
    *   **Never leave the user guessing.** If an operation takes > 200ms, show an indicator.
    *   **Initial Load:** Use **Skeleton Screens** (gray placeholders) or a global loading spinner to indicate the app is initializing. Do not show a blank white screen.
    *   **Background Actions (Auto-save):** Show a non-intrusive status indicator (e.g., "Saving..." -> "All changes saved") in the toolbar or footer.
    *   **Blocking Operations:** If the user *cannot* interact with the app while processing (e.g., "Importing large file"), use a **Progress Modal** with a visible progress bar or spinner and a descriptive text ("Importing... 45%").
    *   **Lazy Loading:** When loading parts of the UI (like a heavy tool palette), show a local spinner placeholder where the content will appear.
*   **Transient feedback:** Use the configured toast surface for transient messages. Use [error placement](../UI_UX.md#error-placement) for failures. Do not show success modals.

## Browser markup accessibility

Accessibility is not just for disabled users; it improves the experience for everyone.
*   **Alt Text:** All meaningful images must have `alt` text. Decorative images should have `alt=""`.
*   **Semantic HTML:** Use `<button>` for buttons, `<a>` for links. Don't use `<div>` with an `onclick` handler unless you reimplement all button behaviors (focus, enter key, space key).
*   **Screen Readers:** Ensure logical tab order.

## Browser theme and component reuse

The named catalog and theme resource below apply when PROJECT.md selects that catalog.
Other frontends reuse their own declared components and appearance tokens.

### 1.1. Standardized Component Library
*   **Mandate:** Agents MUST NOT create new UI components if a suitable component exists in `instructions/frontend/MASTER_COMPONENT_LIST.md`.
*   **Execution:** Before implementing a feature (e.g., a date picker, a progress modal, or a tree view), search the `instructions/frontend/MASTER_COMPONENT_LIST.md` and use the approved implementation pattern.
*   **Reasoning:** Prevents "component bloat" and ensures that accessibility, keyboard shortcuts, and core behaviors are uniform across the entire platform.

### 1.2. Global Styling Application
*   **Mandate:** All components, including modal dialogs and dynamically generated elements, MUST inherit the main application's theme and font settings.
*   **Execution:** Use the global CSS theme defined in [STATIC_ASSETS.md](../static-assets/STATIC_ASSETS.md#theme-resources). Do not use hardcoded colors or font-family declarations in component-specific styles.
*   **Modals:** Ensure Bootstrap modals use the standard theme classes. Buttons in modals must match the sizing and styling of buttons in the main application toolbar.

## Browser layout state

The localStorage adapter below belongs to the selected enterprise browser-shell example.
Other browser components preserve required state through their configured persistence mechanism.

### 3.1. Persistence Mandate
*   **Mandate:** UI configuration state MUST be preserved across sessions and sub-app switches using `localStorage`.
*   **Execution:** Automatically save and restore the following states:
    *   Sidebar collapse/expand state and width.
    *   Log Console height and collapse state.
    *   Grid settings (size, snap-to-grid toggle).
    *   Last active tab in multi-tabbed panels.
    *   Selected view mode (e.g., List vs. Grid).

### 3.2. Implementation Pattern
```typescript
// Example state preservation pattern
const APP_STATE_KEY = 'subapp_name_ui_state';

function saveUIState(state: Record<string, any>) {
    const currentState = JSON.parse(localStorage.getItem(APP_STATE_KEY) || '{}');
    localStorage.setItem(APP_STATE_KEY, JSON.stringify({ ...currentState, ...state }));
}

function restoreUIState() {
    const state = JSON.parse(localStorage.getItem(APP_STATE_KEY) || '{}');
    // Apply state to components
    if (state.gridSize) setGridSize(state.gridSize);
    if (state.sidebarCollapsed) toggleSidebar(true);
}
```


## Security boundaries

Read [general security](../SECURITY_GUIDELINES.md) and the selected HTML, JavaScript, and TypeScript security sections.
Keep frontend permission checks for usability. The backend must authorize every protected operation independently.
Protect cookie-authenticated mutations against cross-site request forgery. Configure credentialed CORS for explicit permitted origins.

Prefer a Content Security Policy response header. Restrict scripts and other resources to the required sources.
Use nonces or hashes where the configured delivery model needs inline code. Avoid unsafe-inline and unsafe-eval.
Set framing policy through frame-ancestors, with compatible X-Frame-Options where needed.
A CSP meta element cannot express every header control, including frame-ancestors.
Set X-Content-Type-Options: nosniff and appropriate cache controls for sensitive responses.
Use CDN delivery only for assets that do not expose private user or tenant content.
Review third-party scripts, dependency provenance, and subresource integrity where appropriate.
See [OWASP CSP guidance](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html).

Test rich content, embedded views, exports, clipboard actions, and session expiry.
Apply [clipboard and storage controls](../SECURITY_GUIDELINES.md#sensitive-data-lifecycle) to browser features.
