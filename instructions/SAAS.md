<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 3a6918c6-c9e5-46af-b979-c46f11981da8
Created: 2026
-->

<!-- AGENT: Target routing and extracted existing guidance for saas and web applications. -->

# SaaS and web applications

## Target scope

A SaaS is a product composed of the enabled services and user interfaces in one monolithic repository.
It may include a backend, browser frontend, database, static assets, docs, website, generated SDKs, and native clients.
Native clients are optional. Their platforms and SaaS-client relationship come from instructions/project/PROJECT_PROFILE.md.
Read only the components changed by the task. Presence in the repository does not require reading every component's implementation.

## Surface selection

| Changed surface | Read |
| --- | --- |
| Java or C# service implementation | [BACKEND.md](BACKEND.md) and the configured service language |
| Browser interface | [FRONTEND.md](FRONTEND.md), affected browser languages, and static asset guidance |
| Native client integration | [APPS.md](APPS.md), [SDKs.md](SDKs.md), and the native source language |
| API contract shared by clients | [API_GUIDELINES.md](API_GUIDELINES.md), [SDKs.md](SDKs.md), and affected consumer guides |
| Stored data | [PERSISTENCE.md](PERSISTENCE.md), with SQL guidance only for SQL changes |
| Separate static website | [WEBSITES.md](WEBSITES.md) and affected asset/language guidance |

Use generated SDKs from the API specification as the normal native service boundary.
Keep generator configuration, output paths, server framework, and packaging facts in instructions/project/PROJECT.md.
Native application behavior still includes appropriate session handling, secure credential storage, and usable failure feedback.
Offline editing, background synchronization, tenants, and workspaces apply only when configured product capabilities need them.
A container can package the server and browser frontend. Native clients have separate application build and release artifacts.

The enterprise browser-shell sections below are a selectable example, not the definition of SaaS.
Apply that shell, its layout, settings, and test identities only when the corresponding project choice is checked.
The .NET layout and packaging examples apply only to that declared backend model.

## Topic references

| Work in scope | Existing guidance |
| --- | --- |
| Shared repository work | [REPO.md](REPO.md) |
| Stored data across application layers | [PERSISTENCE.md](PERSISTENCE.md) |
| Shared UI/UX behavior | [UI_UX.md](UI_UX.md) |
| Backend target | [BACKEND.md](BACKEND.md) |
| Frontend target | [FRONTEND.md](FRONTEND.md) |
| Optional native SaaS client | [APPS.md](APPS.md#native-saas-clients) |
| Generated SDKs and client contracts | [SDKs.md](SDKs.md) |
| Static assets and delivery | [STATIC_ASSETS.md](STATIC_ASSETS.md) |
| Access control and sharing across the application | [ACCESS_CONTROL.md](ACCESS_CONTROL.md) |
| Resource deletion across backend and UI | [DELETION.md](DELETION.md) |

## Application routes and pages

- Serve frontend routes and APIs through the application, including pages when needed.

## combined layout

This is a .NET/browser layout example. Use the configured component paths from instructions/project/PROJECT.md.

```text
api/                   .NET backend, domain services, HTTP boundaries, and persistence
frontend/              Browser HTML, CSS, and source assets
typescript/            TypeScript source compiled into the browser output
unittests/             Backend unit tests
integrationtests/      Real service and database integration tests
playwrighttests/       Browser workflows and accessibility checks
sql/migrations/        Ordered, executable database migrations
specs/                 Product requirements, designs, and progress
playbooks/             Operator and development procedures
docs/                  User and integrator documentation
```

## frontend source layout

These paths belong to the enterprise browser example. Use the configured source/output mapping in other projects.

- Use TypeScript files in the ./typescript/ folder instead of inline Javascript.
  - App specific TypeScript can be kept as separate modules.
- Use CSS files in the frontend/ folder instead of inline CSS.
  - App specific CSS can be kept as separate files.

## cross-layer data mapping

- Map frontend types to backend types to database objects consistently preferably through
  some sort of consistent mapping layer. This prevents typos, translation problems etc.
- Prevent cluttering regular business logic with data transfer objects and more.
- Prevent bugs now and in the future due to mismatch between the field names or types or validation expectations.

## super-app shell

Apply this section only when the Enterprise browser shell example is selected in instructions/project/PROJECT_PROFILE.md.

- Implement a super-app model.
- In the super-app model, there is a **platform menu-bar** at the top for the user, application dropdown,
  links to documentation, help, support etc.
- Individual sub-applications then render below this platform menu bar. The sub-application can have its
  own application menu bar that is specific to that application.
- The bottom has a log console where application log messages are written. These are more relevant to the user
  such as *reading data, saving data* etc.
- All sub-applications should have a consistent UI / UX.

---

## sub-application structure

Apply this section only to the selected enterprise browser shell. Native clients use native navigation.

### 8.1. Super-App Model

The main `index.html` file implements a "super-app". Every link in the top nav bar is a "sub-app" that loads the appropriate `.html` file in the main view panel below the top nav bar. The only "pages" in the application are "terms and conditions", "notices" and "report bug". This structure allows the entire SaaS to be modular.

### 8.2. UI Layout

- All sub-applications have a toolbar at the top that contains common commands relevant to the application. For example, copy-paste, undo-redo, settings, pan, fit, zoom etc.

- All sub-applications have a Log Console at the bottom to which UI generated logs are written. This is useful for users to understand what is going and can enable the company to support user with any issues. Logs are fairly detailed to enable this.

- The Log Console can be collapsed or expanded at will.

- Any applications that involve diagramming or layout of any kind should always support "panning", "fitting", "zooming", "showing a grid", "snapping to a grid", "multi-item selection" and keyboard navigation for "deleting elements", "pasting onto the canvas" and "copying from the canvas".

- Applications that need sidebars on the right or left side should support collapse and expand of such sidebars whenever possible unless instructed otherwise. Sidebars should optionally be resizable.

- Resizing, expanding or collapsing of the Log Console or the Left or Right sidebars should shrink or expand the canvas for such applications.

### 8.3. UI Behaviors

* Show validation and form errors inline in the visible editing surface.
* For a failed command such as Save without a suitable visible error surface, show the literate error dialog.
* Keep technical diagnostics in the log console. Follow [error placement](UI_UX.md#error-placement) for the presentation choice.
* Do not use the vanilla Javascript alert or error dialogs which are browser blocking. Instead, prefer the Bootstrap modal dialog instead.
* All applications are responsive in general so that users can use any device they want.

## monolith documentation packaging

For the .NET monolith example, documentation is hosted with the application and follows the packaging rules below.
Native apps, tools, static websites, and other services use their repository's documented delivery pipeline.

1.  **Repository Structure:**
    *   All external-facing documentation source files must reside in `/docs/external/`.

2.  **URL Structure:**
    *   **Production:** `prod.<appdomain>.io/docs/` (Application: `prod.<appdomain>.io`)
    *   **Staging (Development):** `dev.<appdomain>.io/docs/` (Application: `dev.<appdomain>.io`)

3.  **Build & Packaging:**
    *   The documentation is part of the single monolith Docker container.
    *   Build scripts must copy/process contents from `/docs/external/` to the `wwwroot/docs/` directory within the final build image.
    *   The web server must be configured to serve static content from `wwwroot/docs/` when the `/docs/` path is requested.

---

## data-contract verification

- **"Explicitly define the data contract between layers."**
-  **Casing Check:** When writing API endpoints or Client wrappers, you **must** explicitly verify JSON property names.
  - *C# Backend:* Use `[JsonPropertyName("camelCaseName")]` on DTOs to ensure frontend compatibility.
  - *JS Client:* If the backend expects `snake_case`, use a `toBackendFormat()` mapper. **Never assume automapping works.**
- **Payload Verification:** Before marking a task done, verify: "Does the frontend payload structure (nested objects, field names) match the backend DTO *exactly*?"

## persistence and UI integration

Follow the save through the generated SDK or configured client to the backend and persistence boundary.
The fetch-based checklist below describes the browser implementation of that flow.

- **"UI updates are secondary to Persistence."**
- **Persistence First:** When implementing a CRUD action (Delete, Save, Update), write the API call **first**. Do not write the optimistic UI update until the API call is scaffolded.
- **Verify the Loop:** For every `delete()` or `save()` function:
  - Does it call `api.doAction()`?
  - Does `api.doAction()` make a `fetch()`?
  - Does the backend endpoint actually *use* the received data? (Check for "ignored parameters").

## cross-layer naming

Keep the configured serialization contract consistent. The Program.cs example applies only to a .NET backend.

- **"Uniformity is a feature."**
- **Global Standards:** If you encounter a camelCase vs. snake_case mismatch between backend/frontend or components:
  - **Do NOT** apply local patches or field renaming in a single component.
  - **Action:** Enforce a system-wide serialization standard (e.g., Global JSON settings in Program.cs). Ensure all APIs conform to this standard.
- **Rule:** A codebase should look like it was written by one person. Mismatched casing styles across files are unacceptable.

## local test identities

This test-identity convention belongs to the selected enterprise browser-shell example.

- Use test users in the format `userNNN@test.<appdomain>.io` (e.g., `user001@test.domain.io`, `user042@test.domain.io`).
- `test.<appdomain>.io` is a non-existent domain reserved exclusively for testing.
- The test login endpoint must only be enabled in the local **testing** environment.
- Logins from `@test.<appdomain>.io` must only be accepted in the local **testing** environment.
- Logins from `@test.<appdomain>.io` must be **rejected** in development and production environments.
- Test login endpoints must be **disabled and non-functional** in development and production environments.

---

## application URL configuration

- Keep application URLs in the configured environment settings rather than hardcoding them in source.
- Use the Java framework's configured properties for Java services and the project's configuration mechanism for native clients.
- For .NET use `appsettings.json`. For the configured Vite frontend use `import.meta.env`.

## web performance context

This document outlines the performance standards and best practices for our high-performance web application.

**Target**: Low latency (< 100ms interactions), minimal CPU/Memory footprint, supporting devices ranging from low-power corporate laptops to high-end workstations.

**Example web stack**:
*   **Frontend**: Vanilla JS / TypeScript (ES6), HTML5, Bootstrap 5.
*   **Backend**: ASP.NET Core 10.0 (API + Static Serving).
*   **Database**: PostgreSQL 17.6 (Supabase).

## cross-layer autocomplete optimization

*   **Purpose:** Provide sub-100ms search results across millions of records.
*   **Implementation:**
    *   **Frontend**: Debouncing (300ms) and mandatory result capping (e.g., `limit=10`).
    *   **Backend**: Use `text_pattern_ops` in Postgres for efficient prefix indexing.

## access-control integration

This section describes the selected Knobby authorization example. Other projects use their configured authorization model.

### RBAC & FGAC Compliance
A full Role-Based Access Control (RBAC) and Fine-Grained Access Control (FGAC) system has been implemented. Refer to:
- `specs/access_control.raw.md`
- `specs/access_control.prd.md`
- `instructions/ACCESS_CONTROL.md`

For every new application, resource type, or feature, you must:
- Identify what access control changes are needed
- Implement proper permission checks
- Update access control specifications if new resource types or permissions are introduced

## workspace settings integration

This section applies to the selected enterprise browser shell with workspace/global settings.

### Feature Settings Management
Every new feature, capability, application, or change may introduce settings that control behavior. You must:
- Identify any new settings required by the change
- Update workspace and global settings dialogs to include new settings
- Choose sensible defaults for all new settings
- Ensure global-to-workspace settings inheritance remains intact

## Enterprise shell consistency

Apply this section only to the selected enterprise browser shell.

### 2.1. Standardized Panel Placement
To optimize for muscle memory, key functional areas must always appear in the same relative positions across all sub-apps:
*   **Resource Explorer / Navigation:** Always on the **LEFT** side.
*   **Details / Property Inspector / Settings:** Always on the **RIGHT** side.
*   **Log Console / Output:** Always at the **BOTTOM**.
*   **Main Workspace / Canvas:** Always in the **CENTER**.

### 2.2. Toolbar & Menu Consistency
Toolbars and Menu Bars MUST follow a predictable order for core operations.

#### 2.2.1. "File" Operations (Management)
Common management actions should be grouped at the **START** (left) of the toolbar or under a "File" menu item:
1.  **New** (Ctrl+N)
2.  **Save** (Ctrl+S)
3.  **Delete** (Delete)
4.  **Import**
5.  **Export**

#### 2.2.2. "Edit" Operations (Manipulation)
Common editing actions should be grouped together, typically after File operations or under an "Edit" menu item:
1.  **Undo** (Ctrl+Z)
2.  **Redo** (Ctrl+Y)
3.  **Cut** (Ctrl+X)
4.  **Copy** (Ctrl+C)
5.  **Paste** (Ctrl+V)

#### 2.2.3. View/Context Operations
Application-specific view controls (Zoom, Pan, Fit, Grid Snapping) should follow Edit operations.

### 2.3. Keyboard Shortcut Visibility
*   **Mandate:** Every menu item or toolbar button that supports a keyboard shortcut MUST display that shortcut next to the label or in its tooltip.
*   **Execution:** For menu items, use a right-aligned span for the shortcut (e.g., `Save <span class="shortcut">Ctrl+S</span>`). For toolbar buttons, include it in the `title` attribute or tooltip (e.g., `Save (Ctrl+S)`).

## Enterprise shell feedback

Apply this section only to the selected enterprise browser shell.

### 4.1. Action Feedback
*   Every button click must result in an immediate visual state change (active/pressed state).
*   For blocking operations in this browser shell, use the standardized `Progress Modal` from `instructions/MASTER_COMPONENT_LIST.md`.
*   For work that can continue in the background, use the non-blocking progress behavior in [UI_UX.md](UI_UX.md#progress-and-long-running-operations).

### 4.2. Error Handling
*   Write technical diagnostics to the shell **Log Console**. Show actionable failure guidance at the affected field or operation, as specified in [UI_UX.md](UI_UX.md#validation-and-error-behavior).
*   Failed commands without a suitable visible error surface use the literate error dialog. Form errors remain inline or in a persistent summary. Never use browser `alert()` or `confirm()`.
