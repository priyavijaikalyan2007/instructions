# General Principles

## 1. Standards Compliance

- Use HTML5 and modern ECMAScript standards
- Prioritize native HTML capabilities over complex JavaScript solutions
- Ensure cross-browser compatibility
- Maintain semantic HTML structure
## 2. Code Quality

- Use clear, descriptive naming conventions
  - Functions: descriptive, verb-based names (e.g., `validateUserInput()`)
  - Variables: meaningful, context-specific names
  - Loop/temporary variables: short, standard names (i, j, k)
- Keep code simple and readable
- Avoid unnecessary complexity or "clever" programming tricks
## 3. Structure and Organization

- Modular design
- Functions should be focused and do one task well
- Maximum function length: 25 lines
- Maximum line length: 120 characters
- Limit nesting depth to 3 levels
- Use K&R brace style
## 4. Performance Considerations

- Minimize DOM manipulations
- Use efficient selector methods
- Leverage CSS for animations and transitions
- Implement lazy loading where appropriate
- Use event delegation for dynamic elements
## 5. Accessibility and Usability

- Implement WCAG 2.1 guidelines
- Provide clear focus states
- Use semantic HTML elements
- Include appropriate ARIA attributes
- Ensure keyboard navigability
## 6. Error Handling

- Implement graceful error management
- Provide user-friendly error messages
- Log errors for debugging
- Use try-catch blocks strategically
### 7. Code Generation Annotations

- Include clear comments explaining complex logic.
- Add contextual markers for code understanding by AI agents.
- Document function purposes and parameter expectations.
### 8. Recommended Technologies

- Use Bootstrap 5 as the primary UI and component framework.
- Use TypeScript with a simple compile step to convert into Javascript. Fallback to vanilla Javascript. Do not use overcomplicated technologies like React. For smaller, simpler, projects you can consider using vanilla Javascript.
- Use CSS Grid / Flexbox for layouts.
- Target modern, standards compliant web browsers ignoring older web browsers like Internet Explorer.
- Use the Fetch API for AJAX API calls.
- Use Service Workers for long running sync-style operations. 
- Use web components for reusable elements.
## 9. Application Structure

- Implement a super-app model.
- In the super-app model, there is a **platform menu-bar** at the top for the user, application dropdown, links to documentation, help, support etc. 
- Individual sub-applications then render below this platform menu bar. The sub-application can have its own application menu bar that is specific to that application.
- The bottom has a log console where application log messages are written. These are more relevant to the user such as *reading data, saving data* etc. 
- All sub-applications should have a consistent UI / UX.
## 10. Example Code Structure
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
## 11. Code Generation Best Practices

- Prefer composition over inheritance.
- Use immutable data structures where possible.
- Minimize global variables.
- Implement defensive programming techniques.
- Map frontend types to backend types to database objects consistently preferably through some sort of consistent mapping layer. This prevents typos, translation problems etc. For example, imagine the following setup:
```XML
<mapping>
	<data-object common-name="user"
				 frontend-type="com.outcrop.knobby.User" 
	             backend-type="jsUser"
		<field common-name="id" 
		       frontend="Id" 
		       backend="Id" 
		       storage-table="users" 
		       storage-column="userid" 
		       unique="true" 
		       required="true" 
		       generation="backend" 
		       primary-key="true" 
		       indexed="false"/> 
</mapping>
```
The above XML is an example snippet showing a partial definition of a data object that encapsulates *User* data such as the `Id`. From this, we could imagine generating frontend Typescript objects, the database schema, queries, ORMs, API defintions and the backend objects. You don't have to necessarily to do this but the main objectives are to:

* Prevent cluttering regular business logic with SQL queries, data transfer objects and more.
* Prevent bugs now and in the future due to mismatch between the field names or types or validation expectations.

# UI Framework and Styling

### Core Resources

- CSS Theme: https://4cdf16f2.knobbyio.pages.dev/css/custom.css
- Bootstrap JS: https://4cdf16f2.knobbyio.pages.dev/js/bootstrap.bundle.min.js
### Styling Principles

1. Prefer vanilla Bootstrap styles.
2. Write custom CSS/JS/Typescript only when absolutely necessary.
3. Prioritize functional design with accessibility considerations over fancy animations etc.
4. Maintain consistent color schemes, typography, and layout across applications.
5. Ensure responsive design for multiple device types.
## User Experience Standards

### Keyboard Navigation

- Implement standard keyboard shortcuts:
  - Ctrl-C: Copy
  - Ctrl-V: Paste
  - Ctrl-Z: Undo
  - Ctrl-Y: Redo
  - Ctrl-A: Select All
- Ensure logical tab order for form and interactive elements

### UI Interaction Patterns

- Implement context-appropriate:
  - Panning
  - Zooming
  - Fit to window
  - Grid snapping
  - Auto layout features

### Help and Onboarding

- Include help buttons for complex input elements
- Develop walkthrough guides for each application
- Provide contextual tooltips and explanations

## Accessibility Guidelines

### Primary Considerations

- Maintain sufficient color contrast
- Use legible font sizes
- Support screen reader compatibility
- Implement ARIA labels where appropriate

### Accessibility Hierarchy

- Prioritize application functionality
- Implement accessibility features without compromising core functionality
- Recognize that some complex interactions may limit full accessibility

## Performance Optimization

- Minimize external library dependencies
- Use lazy loading for components
- Optimize asset delivery
- Implement efficient state management

## Browser Compatibility

- Support latest versions of:
  - Chrome
  - Firefox
  - Safari
  - Edge
- Provide graceful degradation for older browsers

## Security Considerations

- Implement secure authentication mechanisms
- Use HTTPS for all communications
- Sanitize user inputs
- Prevent XSS and CSRF vulnerabilities

# Framework & Library Selection Principles

### General Approach

- Prioritize existing, well-maintained libraries and frameworks
- Prefer open-source solutions
- Select libraries with:
  - Active maintenance
  - Good documentation
  - Strong community support
  - Performance optimization
  - Regular security updates

### Recommended Libraries by Function

#### Mapping

- Leaflet.js: Primary choice for map-based applications
- OpenLayers: Alternative for complex geospatial projects

#### Data Visualization

- D3.js: Highly customizable, complex visualizations
- Google Charts: Simple, quick charting
- Apache ECharts: Comprehensive charting
- Charts.js: Lightweight, responsive charts
- Highcharts: Enterprise-grade visualization
- Grid.JS: Enterprise grade tabular data visualization with sorting, searching, pagination, coloring etc.

#### User Experience

- IntroJS: Application walkthroughs
- Popper.js: Tooltips and popovers
- AnimeJS: Advanced animations
- jQuery: DOM manipulation (if necessary)

#### Form Handling

- SurveyJS: Dynamic form building
- Alpaca: Complex form generation
- Cleave.js: Input formatting

#### Datetime & Localization

- MomentJS: Datetime manipulation
- date-fns: Modern datetime library

#### Diagramming

- Cytoscape: Network and graph visualizations
- GoJS: Advanced diagramming

## Project Structure

### Folder Organization

```
root/
├── server.py
├── app1/
│   ├── frontend/
│   └── backend/
└── app2/
│   ├── frontend/
│   └── backend/
└── shared/
    ├── components/
    └── utilities/
```

### Frontend Folder Structure

```
frontend/
├── index.html
├── styles/
│   ├── main.css
│   └── responsive.css
├── scripts/
│   ├── app.js
│   └── modules/
└── assets/
    ├── images/
    └── icons/
```

## Best Practices

- Modular code design
- Responsive layouts
- Performance optimization
- Accessibility compliance
- Cross-browser compatibility
- Consistent coding standards

## Performance Considerations

- Minimize library and framework overhead
- Use code splitting
- Implement lazy loading
- Optimize asset delivery
- Use modern bundling tools (Webpack, Vite)

## Security Guidelines

- Sanitize user inputs
- Implement proper authentication flows
- Use HTTPS
- Protect against XSS and CSRF
- Keep dependencies updated

## Recommended Toolchain

- Framework: React, Vue, or Svelte
- State Management: Redux, Vuex, or Zustand
- Styling: Tailwind CSS, Bootstrap, or CSS Modules
- Build Tools: Vite or Next.js
- Testing: Jest, React Testing Library

# API Centric Thinking

## General Principles

### API and Data Management

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
   - Implement background synchronization mechanisms
   - Sync edits to server:
     * Immediate background sync for critical updates
     * Periodic sync for non-critical changes
   - Provide placeholder functions for future API implementations

## Initial Development Setup

### Backend API Hosting

- Use `server.py` in root folder for initial API development
- Plan for modular API organization
  * Separate API files for different application components
  * Maintain clean, organized API structure

## Frontend Function Pattern

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

## Key Considerations

- Always handle potential API failures
- Implement proper error logging
- Provide user-friendly error messages
- Ensure responsive design
- Optimize performance
- Maintain clean, readable code

## Technology Recommendations

- Use modern JavaScript (ES6+)
- Consider React or Vue.js for complex interfaces
- Implement state management (Redux, Vuex)
- Use TypeScript for type safety

# Commenting & Logging

## Code Commenting Principles

### Purpose of Comments

- Comments should explain the "why" and "what" of code, not the "how"
- Provide context that is not immediately obvious from the code itself
- Focus on explaining business logic, complex algorithms, and design decisions

### Comment Types

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

### Maintenance-Oriented Commenting

- Write comments assuming a new developer will maintain the code in 6-12 months
- Update comments whenever code changes
- Avoid redundant comments that merely restate the code

## Logging Strategy

### Logging Principles

- Log at critical points to aid debugging and understanding system behavior
- Include sufficient context without overwhelming log volume
- Never log sensitive information (passwords, tokens, personal data)

### Recommended Logging Points

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

### Logging Best Practices

- Use structured logging (JSON preferred)
- Include correlation IDs to track request flows
- Implement log levels (DEBUG, INFO, WARN, ERROR)
- Ensure logs are easily parseable by log management tools

### Example Logging Structure

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

### Performance Considerations

- Implement efficient logging mechanisms
- Use asynchronous logging to minimize performance impact
- Configure log rotation and retention policies
- Consider log sampling for high-volume environments

### Security Reminders

- Never log:
  - Authentication credentials
  - Session tokens
  - Personal identification information
  - Encryption keys
- Sanitize and mask sensitive data before logging

# Data Centric Thinking

## Core Principles

### Data-Centric Design Philosophy

- Prioritize data structure and flow over visual presentation
- Represent all data as JSON objects
- Implement data management as primary concern before UI design

## Data Management Strategies

### JSON-First Approach

- All data must be structured as JSON
- Use consistent JSON schemas across frontend and backend
- Implement universal data transformation functions
- Support both local storage and API-based data retrieval

### Data Synchronization Considerations

- Implement eTags for version tracking
- Create delta detection mechanisms
- Support optimistic and pessimistic update models
- Handle concurrent editing scenarios

## Technical Implementation Guidelines

### Storage Mechanisms

- Prefer JSON-based storage solutions
- Use browser localStorage/sessionStorage
- Implement IndexedDB for complex data structures
- Design fallback mechanisms for storage failures

### API Interaction Patterns

- Use consistent data transfer protocols
- Implement robust error handling
- Support partial data updates
- Design for graceful network interruptions

### State Management

- Use immutable data structures
- Implement unidirectional data flow
- Minimize complex state mutations
- Prefer reactive programming paradigms

## Recommended Technologies

- React with TypeScript
- Redux or MobX for state management
- Axios for API interactions
- JSON Schema for data validation

### Performance Considerations

- Minimize unnecessary re-renders
- Implement efficient data serialization
- Use memoization techniques
- Optimize JSON parsing and transformation

### Security Principles

- Sanitize all incoming JSON data
- Implement strict type checking
- Use JSON.parse() with reviver functions
- Validate data schemas before processing

# Sub-Application Structure

## Super-App Model

The main `index.html` file implements a "super-app". Every link in the top nav bar is a "sub-app" that loads the appropriate `.html` file in the main view panel below the top nav bar. The only "pages" in the application are "terms and conditions", "notices" and "report bug". This structure allows the entire SaaS to be modular.

## UI Layout

- All sub-applications have a toolbar at the top that contains common commands relevant to the application. For example, copy-paste, undo-redo, settings, pan, fit, zoom etc. 

- All sub-applications have a Log Console at the bottom to which UI generated logs are written. This is useful for users to understand what is going and can enable the company to support user with any issues. Logs are fairly detailed to enable this.

- The Log Console can be collapsed or expanded at will.

- Any applications that involve diagramming or layout of any kind should always support "panning", "fitting", "zooming", "showing a grid", "snapping to a grid", "multi-item selection" and keyboard navigation for "deleting elements", "pasting onto the canvas" and "copying from the canvas".

- Applications that need sidebars on the right or left side should support collapse and expand of such sidebars whenever possible unless instructed otherwise. Sidebars should optionally be resizable. 

- Resizing, expanding or collapsing of the Log Console or the Left or Right sidebars should shrink or expand the canvas for such applications.

## UI Behaviors

* Never show modal dialogs for common errors. Always, write errors to the log console. In some specific instances, modal dialogs may be shown for some specific erroneous problems, but in general it is best to indicate failures with UI hints and cues next to the relevant elements directly.
* Do not use the vanilla Javascript alert or error dialogs which are browser blocking. Instead, prefer the Bootstrap modal dialog instead. 
* All applications are responsive in general so that users can use any device they want. 
