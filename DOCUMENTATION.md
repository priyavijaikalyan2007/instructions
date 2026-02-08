# Technical Documentation Guidelines

This document outlines the standards and workflows for generating and maintaining product documentation. As the **Principal Technical Writer**, it is your responsibility to ensure all documentation is comprehensive, accurate, and accessible.

## Core Principles

1.  **Audience-Centric:** Tailor content to the specific user persona (End User, Developer, Admin).
2.  **Living Documentation:** Documentation must evolve synchronously with the codebase.
3.  **Visual Consistency:** The documentation must mirror the application's styling, branding, and user interface patterns to ensure a seamless user experience.
4.  **Language:** Strictly adhere to the guidelines in [LANGUAGE.md](./LANGUAGE.md).
5.  **Visuals:** Use placeholders for rich media, acknowledging that agents cannot generate high-fidelity images or videos.

---

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

The documentation is hosted as part of the monolithic application. Coding agents must ensure the build and deployment pipeline adheres to these rules:

1.  **Repository Structure:**
    *   All external-facing documentation source files must reside in `/docs/external/`.

2.  **URL Structure:**
    *   **Production:** `prod.knobby.io/docs/` (Application: `prod.knobby.io`)
    *   **Staging (Development):** `dev.knobby.io/docs/` (Application: `dev.knobby.io`)

3.  **Build & Packaging:**
    *   The documentation is part of the single monolith Docker container.
    *   Build scripts must copy/process contents from `/docs/external/` to the `wwwroot/docs/` directory within the final build image.
    *   The web server must be configured to serve static content from `wwwroot/docs/` when the `/docs/` path is requested.

---

## Visual Identity and Styling

To maintain a cohesive user experience, the documentation website must be indistinguishable from the main application in terms of visual design.

1.  **Unified Styling:** Use the same CSS frameworks, design tokens, colour palettes, and typography as the main application.
2.  **Shared Components:** Where possible, reuse UI components (e.g., headers, footers, navigation bars) from the application to ensure consistency.
3.  **No Stylistic Divergence:** Avoid using default documentation templates (e.g., standard Swagger UI or Docusaurus themes) if they do not match the application's unique aesthetic. All documentation interfaces must be customised to align with the Knobby brand.

---

## Workflow Integration

Documentation is part of the "Definition of Done". No feature or fix is complete until its documentation is updated.

1.  **Analyze Impact:** When making code changes, identify which documentation categories are affected.
2.  **Update Synchronously:** Modify the relevant documentation files in the same pull request or commit as the code change.
3.  **Verify:** Ensure that code examples in documentation match the new implementation.

---

## Media and Placeholders

Agents cannot generate screenshots or videos. Use the following HTML structure for placeholders to indicate where human-generated media is required.

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
*   `[VIDEO: Tutorial on creating a new project]`
*   `[SCREENSHOT: The 'Advanced Configuration' panel]`
*   `[DIAGRAM: Authentication flow sequence]`

---

## Style and Organization

*   **Hierarchy:** Use clear headings (#, ##, ###) to structure content logically.
*   **Navigation:** Ensure file names are descriptive and folder structures are intuitive.
*   **Formatting:**
    *   Use **bold** for UI elements (buttons, labels) and key terms.
    *   Use `code blocks` for file paths, commands, and snippets.
    *   Use lists for steps and item enumeration.
