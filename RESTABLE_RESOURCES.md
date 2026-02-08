<!-- AGENT: Standards for implementing human-friendly, shareable URLs for all resources. -->

# Restable Resources: Human-Friendly URLs for the Super-App

This document outlines the standard for implementing "Restable URLs" in our platform. A "Restable URL" ensures that every distinct resource (a diagram, a checklist, a thought stream) has a unique, permanent, and sharable web address.

**Goal:** Users must be able to bookmark, email, or Slack a link to a specific resource, and clicking that link must open the correct application and load that exact resource in the correct state.

## 1. The URL Philosophy

URLs are the UI for locating data. They should be:
1.  **Readable:** `knobby.io/diagrams/org-chart-2024`
2.  **Predictable:** `/{app-name}/{resource-type}/{id}`
3.  **Hackable:** Users should guess that deleting `/{id}` takes them to the resource list.

### 1.1 The Standard URL Structure

All applications in the super-app shell must adhere to this hierarchy:

```
https://{domain}/{app}/{view}/{id-slug}?{query-params}
```

*   **{app}:** The application namespace (e.g., `thinker`, `diagrams`, `strukture`).
*   **{view}:** The type of view or resource (e.g., `canvas`, `list`, `settings`). Default to `canvas` or `list` if omitted.
*   **{id-slug}:** The unique identifier, optionally paired with a human-readable slug.
*   **{query-params}:** Transient state (e.g., `?zoom=1.5`, `?mode=edit`, `?search=term`).

### Examples:
*   **Home:** `knobby.io/`
*   **App Home:** `knobby.io/diagrams` (Shows list of diagrams)
*   **Specific Resource:** `knobby.io/diagrams/canvas/xK9j2P-q3-marketing-flow`
*   **Specific Resource (Clean):** `knobby.io/checklists/run/daily-standup-checklist`

---

## 2. Technical Implementation (Super-App + Iframes)

Since our architecture uses a parent Shell loading sub-apps in `<iframe>`s, we cannot rely on standard browser navigation (which would reload the shell). We must use the **History API** and **PostMessage** communication.

### 2.1 The Two-Way Synchronization Protocol

The Browser URL is the "Source of Truth". The Shell and Iframe must stay in sync.

#### A. Shell-to-Iframe (Inbound Link)
When a user opens `knobby.io/diagrams/edit/123`:
1.  **Shell** parses the URL.
2.  **Shell** loads the `diagrams` iframe (if not loaded).
3.  **Shell** sends a `NAVIGATE_TO` message to the iframe.
4.  **Iframe** receives message and renders Diagram 123.

#### B. Iframe-to-Shell (User Navigation)
When a user clicks "New Diagram" inside the `diagrams` iframe:
1.  **Iframe** creates the diagram (ID: 456).
2.  **Iframe** sends a `URL_CHANGED` message to the Shell.
3.  **Shell** updates the browser URL to `knobby.io/diagrams/edit/456` using `history.pushState`.
4.  **Important:** The Shell does *not* reload the page.

### 2.2 The Message Contract

**1. Shell -> Iframe (`NAVIGATE_TO`)**
Sent when the browser URL changes (popstate) or initial load.
```typescript
{
  type: "NAVIGATE_TO",
  path: "/edit/123",    // The path *relative* to the app
  queryParams: { mode: "view" }
}
```

**2. Iframe -> Shell (`URL_CHANGED`)**
Sent when the user navigates inside the app.
```typescript
{
  type: "URL_CHANGED",
  path: "/edit/456",
  title: "New Marketing Flow" // Optional: Updates browser tab title
}
```

---

## 3. Human-Readable IDs (Slugs)

Do not expose raw database UUIDs or auto-increment integers if possible. They are ugly and error-prone to transcribe.

### 3.1 Guideline
Use a combination of a **short, collision-resistant ID** and a **user-controlled slug**.

*   **Format:** `{short-id}-{slug}`
*   **Library:** Use **Sqids** (recommended in `DOTNETFX_SELECTION.md`) to encode IDs, or **NanoID** for random strings.

**Example:**
*   Database ID: `550e8400-e29b...`
*   Short ID: `xK9j2P`
*   User Title: "Marketing Q1 Plan"
*   **Resulting Slug:** `xK9j2P-marketing-q1-plan`

### 3.2 Resolution Logic
When the backend/frontend receives `xK9j2P-marketing-q1-plan`:
1.  Extract the ID part (`xK9j2P`).
2.  Lookup resource by ID.
3.  (Optional) If the slug part (`marketing-q1-plan`) doesn't match the current title, 301 Redirect (or `replaceState`) to the canonical URL. This prevents "link rot" if the title changes.

---

## 4. Coding Agent Instructions

When implementing new features or apps:
1.  **Never** use `window.location.href = ...` inside an iframe. It breaks the shell.
2.  **Always** emit `URL_CHANGED` messages when the primary view changes.
3.  **Always** listen for `NAVIGATE_TO` messages and handle them idempotently.
4.  **Deep Linking:** Ensure every "page" or "modal" of consequence has a URL representation. If it's not in the URL, it doesn't exist to the outside world.
