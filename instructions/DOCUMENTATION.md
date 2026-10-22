<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: f5bb83d2-d8a9-4f52-8dff-4ebd2f93456e
Created: 2026
-->

<!-- AGENT: Technical documentation standards and workflows for product documentation. -->

# Technical Documentation Guidelines

This document outlines the standards and workflows for generating and maintaining product documentation. 
As the **Principal Technical Writer**, it is your responsibility to ensure all documentation is comprehensive, 
accurate, and accessible.
---

## Core Principles

1.  **Audience-Centric:** Tailor content to the specific user persona (End User, Developer, Admin) — 
   whether they are an agent extending the library, a developer integrating it, or a beginner learning web development.
2.  **Living Documentation:** Documentation must evolve synchronously with the codebase.
3.  **Visual Consistency:** The documentation must mirror the application's styling, branding, and user interface
    patterns to ensure a seamless user experience.
4.  **Language:** Strictly adhere to the guidelines in [LANGUAGE.md](LANGUAGE.md).
5.  **Visuals:** Use actual screenshots, diagrams, or recordings when the available tools support them.
    Use a clearly labeled placeholder when required media cannot be produced.

---

## Verified facts and published contracts

Keep each changing fact in one authoritative location and link to it from other documents.
Separate implemented behavior, planned work, estimates, and verified results.
For public API, component, or artifact changes, update the consumer contract in the same change.
Register new guides and demos in the project's navigation and publication pipeline.
Verify the published output and its links, not only the source file's existence.

## Documentation Categories

### 1. Product Documentation (End User)
**Audience:** Daily users of the application.
**Focus:** Task completion, feature usage, and workflow optimisation.
**Location:** `/docs/external/user/`

*   **Structure:**
    *   **Getting Started:** First steps and account setup.
    *   **Feature Guides:** Step-by-step instructions for core features.
    *   **FAQs:** Common questions and troubleshooting.
    *   **Best Practices:** How to get the most value from the product.

### 2. Integrator Documentation (API)
**Audience:** Developers and system integrators.
**Focus:** API surface, authentication, and data integration.
**Location:** `/docs/external/api/`

*   **Structure:**
    *   **Authentication:** Methods (OAuth, API Keys) and security standards.
    *   **Endpoints:** Detailed reference with methods, paths, and parameters.
    *   **Models:** Data schemas and field definitions.
    *   **Examples:** Clear request and response snippets (JSON/XML).
    *   **Errors:** Standard error codes and troubleshooting.

### 3. Enterprise Admin Documentation
**Audience:** System administrators, security officers, and IT managers.
**Focus:** Configuration, security, compliance, and user management.
**Location:** `/docs/external/admin/`

*   **Structure:**
    *   **Deployment:** Installation and environment setup.
    *   **Configuration:** Environment variables, settings files, and system options.
    *   **Security:** Access control, audit logs, and compliance standards (e.g., GDPR, SOC2).
    *   **User Management:** Provisioning (SSO/SAML), roles, and permissions.

### 4. Release Notes & Updates
**Audience:** All users and stakeholders.
**Focus:** What changed, why it matters, and how to upgrade.
**Location:** `/docs/external/updates/` (derived from `CHANGELOG.md`)

*   **Structure:**
    *   **New Features:** Description of new capabilities.
    *   **Improvements:** Enhancements to existing features.
    *   **Bug Fixes:** Resolved issues.
    *   **Breaking Changes:** Critical information for upgrades/migrations.

---

## Hosting and Deployment Architecture

Use the project's declared documentation delivery. The linked .NET monolith packaging is a configured example, not a Java or native requirement.

See [SAAS.md](saas/SAAS.md#monolith-documentation-packaging).

## Visual Identity and Styling

To maintain a cohesive user experience, the documentation website must be indistinguishable from the main application in terms of visual design.

1.  **Unified Styling:** Use the same CSS frameworks, design tokens, colour palettes, and typography as the main application.
2.  **Shared Components:** Where possible, reuse UI components (e.g., headers, footers, navigation bars) from the application to ensure consistency.
3.  **No Stylistic Divergence:** Avoid using default documentation templates (e.g., standard Swagger UI or Docusaurus themes) if they do not match the application's unique aesthetic. Customize documentation interfaces to the consuming project's declared design system.

---

## Workflow Integration

Documentation is part of the "Definition of Done". No feature or fix is complete until its documentation is updated.

1.  **Analyze Impact:** When making code changes, identify which documentation categories are affected.
2.  **Update Synchronously:** Modify the relevant documentation files in the same pull request or commit as the code change.
3.  **Verify:** Ensure that code examples in documentation match the new implementation.

---

## Media and Placeholders

Capture actual application output when the available tools support it.
If required media cannot be captured, use the following labeled placeholder and state what remains to be verified.

**Requirement:** All placeholders must have a mild drop shadow and clear label.

### Placeholder Snippet
```html
<div style="
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 24px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    background-color: #f9fafb;
    text-align: center;
    margin: 20px 0;
    font-family: sans-serif;
    color: #6b7280;">
    <strong>[MEDIA TYPE: Description of content]</strong><br>
    <em>(e.g., Screenshot of the User Settings dashboard)</em>
</div>
```

**Usage Examples:**
-   `[VIDEO: Tutorial on creating a new project]`
-   `[SCREENSHOT: The 'Advanced Configuration' panel]`
-   `[DIAGRAM: Authentication flow sequence]`

---

## Style and Organization

- **Hierarchy:** Use clear headings (`#`, `##`, `###`) to structure content logically.
- **Code blocks:** Use fenced code blocks with language hints (` ```html `, ` ```scss `, ` ```typescript `).
- **Navigation:** Ensure file names are descriptive and folder structures are intuitive.
-   **Formatting:**
    *   Use **bold** for UI elements (buttons, labels) and key terms.
    *   Use `code blocks` for file paths, commands, and snippets.
    *   Use lists for steps and item enumeration.
    *   Use numbered lists for sequential steps, bullet lists for unordered items.
    *   Use relative links to other files in the repository (e.g., `[CODING_STYLE.md](CODING_STYLE.md)`).

---

## Workflow Integration

Documentation is part of the "Definition of Done". A change is not complete until:

1. The relevant documentation files are updated.
2. `instructions/frontend/COMPONENTS.md` is updated if a component was added or changed.
3. `demo/index.html` includes the new or changed component.
4. `CONVERSATION.md` records the change.
