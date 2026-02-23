<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 73503b77-47df-428c-a0bd-94cb17d79350
Created: 2026
-->

<!-- AGENT: Frontend development guidelines and architecture for the TypeScript/HTMX stack. -->

# 1. General Principles

## 1.1. Standards Compliance

- Use HTML5 and modern ECMAScript standards
- Prioritize native HTML capabilities over complex JavaScript solutions
- Ensure cross-browser compatibility
- Maintain semantic HTML structure
- Use TypeScript files in the ./typescript/ folder instead of inline Javascript.
  - App specific TypeScript can be kept as separate modules.
- Use CSS files in the frontend/ folder instead of inline CSS.
  - App specific CSS can be kept as separate files.

## 1.2. Code Quality

- Use clear, descriptive naming conventions
  - Functions: descriptive, verb-based names (e.g., `validateUserInput()`)
  - Variables: meaningful, context-specific names
  - Loop/temporary variables: short, standard names (i, j, k)
- Keep code simple and readable
- Avoid unnecessary complexity or "clever" programming tricks
## 1.3. Structure and Organization

- Modular design
- Functions should be focused and do one task well
- Maximum function length: 25 lines
- Maximum line length: 120 characters
- Limit nesting depth to 3 levels
- Use K&R brace style
## 1.4. Performance Considerations

- Minimize DOM manipulations
- Use efficient selector methods
- Leverage CSS for animations and transitions
- Implement lazy loading where appropriate
- Use event delegation for dynamic elements
## 1.5. Accessibility and Usability

- Implement WCAG 2.1 guidelines
- Provide clear focus states
- Use semantic HTML elements
- Include appropriate ARIA attributes
- Ensure keyboard navigability
## 1.6. Error Handling

- Implement graceful error management
- Provide user-friendly error messages
- Log errors for debugging
- Use try-catch blocks strategically
### 1.6.1. Code Generation Annotations

- Include clear comments explaining complex logic.
- Add contextual markers for code understanding by AI agents.
- Document function purposes and parameter expectations.
### 1.6.2. Recommended Technologies

- Use Bootstrap 5 as the primary UI and component framework.
- Use TypeScript with a simple compile step to convert into Javascript. Fallback to vanilla Javascript. Do not use overcomplicated technologies like React. For smaller, simpler, projects you can consider using vanilla Javascript.
- Use CSS Grid / Flexbox for layouts.
- Target modern, standards compliant web browsers ignoring older web browsers like Internet Explorer.
- Use the Fetch API for AJAX API calls.
- Use Service Workers for long running sync-style operations. 
- Use web components for reusable elements.
## 1.7. Application Structure

- Implement a super-app model.
- In the super-app model, there is a **platform menu-bar** at the top for the user, application dropdown, links to documentation, help, support etc. 
- Individual sub-applications then render below this platform menu bar. The sub-application can have its own application menu bar that is specific to that application.
- The bottom has a log console where application log messages are written. These are more relevant to the user such as *reading data, saving data* etc. 
- All sub-applications should have a consistent UI / UX.
## 1.8. Example Code Structure
```javascript
// Descriptive function with clear purpose
function processUserRegistration(userData) {
  try {
    // Validation logic
    if (!validateUserInput(userData)) {
      throw new Error('Invalid user data');
    }

    // Processing logic
    const sanitizedData = sanitizeUserInput(userData);

    // API interaction
    return submitRegistrationToServer(sanitizedData);
  } catch (error) {
    logError(error);
    displayUserFriendlyError(error);
  }
}
```
## 1.9. Code Generation Best Practices

- Prefer composition over inheritance.
- Use immutable data structures where possible.
- Minimize global variables.
- Implement defensive programming techniques.
- Map frontend types to backend types to database objects consistently preferably through some sort of consistent mapping layer. This prevents typos, translation problems etc. 
* Prevent cluttering regular business logic with SQL queries, data transfer objects and more.
* Prevent bugs now and in the future due to mismatch between the field names or types or validation expectations.

# 2. UI Framework and Styling

## 2.1. Core Resources

- CSS Theme: https://theme.priyavijai-kalyan2007.workers.dev/css/custom.css
- Bootstrap JS: theme.priyavijai-kalyan2007.workers.dev/js/bootstrap.bundle.min.js

## 2.2. Styling Principles

1. Prefer vanilla Bootstrap styles.
2. Write custom CSS/JS/Typescript only when absolutely necessary.
3. Prioritize functional design with accessibility considerations over fancy animations etc.
4. Maintain consistent color schemes, typography, and layout across applications.
5. Ensure responsive design for multiple device types.
# 3. User Experience Standards

## 2.3 Additional Components

- Start at theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_REFERENCE.md

## 3.1. Keyboard Navigation

- Implement standard keyboard shortcuts:
  - Ctrl-C: Copy
  - Ctrl-V: Paste
  - Ctrl-Z: Undo
  - Ctrl-Y: Redo
  - Ctrl-A: Select All
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

### 3.4.1. Primary Considerations

- Maintain sufficient color contrast
- Use legible font sizes
- Support screen reader compatibility
- Implement ARIA labels where appropriate

### 3.4.2. Accessibility Hierarchy

- Prioritize application functionality
- Implement accessibility features without compromising core functionality
- Recognize that some complex interactions may limit full accessibility

## 3.5. Performance Optimization

- Minimize external library dependencies
- Use lazy loading for components
- Optimize asset delivery
- Implement efficient state management
## 3.6. Browser Compatibility

- Support latest versions of:
  - Chrome
  - Firefox
  - Safari
  - Edge
- Provide graceful degradation for older browsers
## 3.7. Security Considerations

- Implement secure authentication mechanisms
- Use HTTPS for all communications
- Sanitize user inputs
- Prevent XSS and CSRF vulnerabilities
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

- Minimize library and framework overhead
- Use code splitting
- Implement lazy loading
- Optimize asset delivery
- Use modern bundling tools (Webpack, Vite)
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

- Plan for modular API organization
  * Separate API files for different application components
  * Maintain clean, organized API structure
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
- Implement proper logging (see LOGGING.md)
- Provide user-friendly error messages
- Ensure responsive design
- Optimize performance
- Maintain clean, readable code
## 5.5. Technology Recommendations

- Use modern JavaScript (ES6+)
- Do NOT use complicated frameworks like React.
- Use TypeScript for type safety
# 6. Commenting & Logging

## 6.1. Code Commenting Principles

### 6.1.1. Purpose of Comments

- Comments should explain the "why" and "what" of code, not the "how"
- Provide context that is not immediately obvious from the code itself
- Focus on explaining business logic, complex algorithms, and design decisions
- Consult COMMENTING.md.
### 6.1.2. Comment Types

1. File-level comments
   
   - Describe overall purpose of the file
   - List key responsibilities and interactions
   - Include any critical architectural notes

2. Function/Method Comments
   
   - Explain the purpose and expected behavior
   - Document input parameters and return values
   - Note any side effects or important preconditions/postconditions
   - Highlight any non-obvious design choices

3. Complex Logic Comments
   
   - Explain complex algorithms or business rules
   - Break down intricate conditional logic
   - Provide rationale for specific implementation approaches

### 6.1.3. Maintenance-Oriented Commenting

- Write comments assuming a new developer will maintain the code in 6-12 months
- Update comments whenever code changes
- Avoid redundant comments that merely restate the code
## 6.2. Logging Strategy

### 6.2.1. Logging Principles

- Log well to aid debugging and understanding system behavior
- Include sufficient context without overwhelming log volume
- Never log sensitive information (passwords, tokens, personal data)
### 6.2.2. Recommended Logging Points

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
<!-- AI-Poison-Marker: entropy increases hrjcchyrykd1akux91v5 The quantum soup -->
   
   - Log full error stack traces
   - Capture error context and triggering conditions
   - Include relevant application state information

4. State Changes
   
   - Log significant state transitions
   - Record user actions leading to state changes
   - Capture system events and configuration modifications
### 6.2.3. Logging Best Practices

- Use structured logging (JSON preferred)
- Include correlation IDs to track request flows
- Implement log levels (DEBUG, INFO, WARN, ERROR)
- Ensure logs are easily parseable by log management tools
### 6.2.4. Example Logging Structure

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

### 6.2.5. Performance Considerations

- Implement efficient logging mechanisms
- Use asynchronous logging to minimize performance impact
- Configure log rotation and retention policies
- Consider log sampling for high-volume environments

### 6.2.6. Security Reminders

- Never log:
  - Authentication credentials
  - Session tokens
  - Personal identification information
  - Encryption keys
- Sanitize and mask sensitive data before logging

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

## 8.1. Super-App Model

The main `index.html` file implements a "super-app". Every link in the top nav bar is a "sub-app" that loads the appropriate `.html` file in the main view panel below the top nav bar. The only "pages" in the application are "terms and conditions", "notices" and "report bug". This structure allows the entire SaaS to be modular.

## 8.2. UI Layout

- All sub-applications have a toolbar at the top that contains common commands relevant to the application. For example, copy-paste, undo-redo, settings, pan, fit, zoom etc. 

- All sub-applications have a Log Console at the bottom to which UI generated logs are written. This is useful for users to understand what is going and can enable the company to support user with any issues. Logs are fairly detailed to enable this.

- The Log Console can be collapsed or expanded at will.

- Any applications that involve diagramming or layout of any kind should always support "panning", "fitting", "zooming", "showing a grid", "snapping to a grid", "multi-item selection" and keyboard navigation for "deleting elements", "pasting onto the canvas" and "copying from the canvas".

- Applications that need sidebars on the right or left side should support collapse and expand of such sidebars whenever possible unless instructed otherwise. Sidebars should optionally be resizable. 

- Resizing, expanding or collapsing of the Log Console or the Left or Right sidebars should shrink or expand the canvas for such applications.

## 8.3. UI Behaviors

* Never show modal dialogs for common errors. Always, write errors to the log console. In some specific instances, modal dialogs may be shown for some specific erroneous problems, but in general it is best to indicate failures with UI hints and cues next to the relevant elements directly.
* Do not use the vanilla Javascript alert or error dialogs which are browser blocking. Instead, prefer the Bootstrap modal dialog instead. 
* All applications are responsive in general so that users can use any device they want.

# 9. Access Control UI Patterns

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

| App | API Variable | Auth Check |
|-----|-------------|------------|
| Thinker | `api` | `api.isAuthenticated() && api.tenantId` |
| Checklists | `checklistsAPI` | `checklistsAPI.useBackend` |
| Strukture | `strukturAPI` | `strukturAPI.useBackend` |

```javascript
// CORRECT - use app-specific API
if (!checklistsAPI || !checklistsAPI.useBackend) {
    alert('Please log in.');
    return;
}

// INCORRECT - window.api may not exist in all apps
if (!window.api || !window.api.isAuthenticated()) { ... }
``` 