<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 65f0c083-038c-4fb4-8271-644cacaee806
Created: 2026
-->

<!-- AGENT: Marker guidance for fast navigation and shared conventions. -->
# Agent Navigation Markers & Annotations

To accelerate agent comprehension and navigation, we use a standard system of **Semantic Markers**. These markers act as high-speed indexing tags, allowing agents to understand a file's purpose, dependencies, and flow without analysing the entire content.

## 0. Principles

- **Be consistent:** Use the same marker names everywhere.
- **Be minimal:** Add only markers that materially improve navigation.
- **Keep them current:** If you change responsibility or flow, update markers in the same edit.
- **Do not change logic:** Markers are comments or directives only.

## 1. The "Fast-Read" File Header

Every significant source file (Classes, Services, Controllers, Complex Components) must start with a **Structured Header Block**. This allows agents to read the first 20 lines of a file and immediately understand its context.

**Format:**
```csharp
/* 
 * ----------------------------------------------------------------------------
 * ⚓ COMPONENT: [ComponentName]
 * 📜 PURPOSE: [Concise description of what this file does]
 * 🔗 RELATES: [Reference to related files or specs, e.g., [[AuthSpec]]]
 * ⚡ FLOW: [Inbound Caller] -> [This Component] -> [Outbound Dependency]
 * 🛡️ SECURITY: [Security Role/Constraint, e.g., Requires 'Admin']
 * ----------------------------------------------------------------------------
 */
```

**Example:**
```typescript
/*
 * ----------------------------------------------------------------------------
 * ⚓ COMPONENT: UserProfileController
 * 📜 PURPOSE: Handles fetching and updating user profile settings and avatars.
 * 🔗 RELATES: [[UserProfileService]], [[AvatarUpload]]
 * ⚡ FLOW: [Router] -> [This] -> [Database]
 * 🛡️ SECURITY: Requires 'AuthenticatedUser' policy.
 * ----------------------------------------------------------------------------
 */
export class UserProfileController { ... }
```

## 2. In-Code Semantic Tags

Use these tags within comments to map logic flow and decision history.

### 2.1 Navigation Tags
*   `// @entrypoint`: Marks the start of a public API or execution flow.
*   `// @dependency: [File/Service]`: Explicitly marks a hidden or key dependency.
*   `// @maps_to: [DB_Table/Column]`: Links code entities to database schema.
*   `// @config: [SettingName]`: Marks a dependency on a configuration value (env var, appsettings key).
*   `// @middleware`: Marks a middleware or pipeline component that intercepts requests.
*   `// @background`: Marks a background job, hosted service, or scheduled task.

### 2.2 Logic Flow Indicators
*   `// -> Dispatches: [EventName]`: Indicates an event emission.
*   `// <- Handles: [EventName]`: Indicates an event handler.
*   `// >> Delegates to: [Component]`: Indicates a hand-off of responsibility.

### 2.3 Context Anchors
*   `// ⚓ [ConceptName]`: Defines the canonical location for a business concept.
    *   *Usage:* "If you are looking for how 'Tax' is calculated, look for `⚓ TaxCalculation`."

### 2.4 Agent Work Tags

Use these tags for targeted follow-up by other agents. Align with `COMMENTING.md`.

*   `// @agent:test` — Requires tests or test coverage.
*   `// @agent:security` — Requires security review.
*   `// @agent:review` — Requires human verification.
*   `// @agent:refactor` — Candidate for future refactor.

### 2.5 Annotation Alignment

The semantic markers above complement the standard annotations defined in `COMMENTING.md` (`TODO`, `FIXME`, `SECURITY`, `PERF`, etc.). Use annotations for *status* (what state is this code in?) and semantic markers for *navigation* (where does this code fit in the system?). Both are captured by the repository index (see `REPO_INDEX.md`).

## 3. Global Concept Registry

We use **Wiki-Style Links** `[[ConceptName]]` in comments to reference shared business logic across the stack.

*   **Syntax:** `[[Concept]]`
*   **Behavior:** Agents should search for `⚓ Concept` to find the definition.

**Example:**
```csharp
// Validates the cart items against the [[InventoryRules]].
public void ValidateCart() { ... }
```

## 4. Section Markers (Long Files)

Use clear section headers so agents can scan large files quickly.

```csharp
// ============================================================================
// PUBLIC API
// ============================================================================
```

## 5. Language-Specific Collapsible Regions

When supported by the language and tooling, use region directives to collapse large sections. In C#, use `#region` and `#endregion` for blocks that are meaningful as a unit (for example, "Public API", "Private Helpers"). Keep regions shallow; do not nest more than one level.

```csharp
#region Public API
public Task<User> GetUserAsync(...) { ... }
#endregion
```

## 6. HTML and CSS Files

Apply markers using HTML comments. This is relevant for the vanilla HTML frontend files in `frontend/`.

**HTML:**
```html
<!--
  ⚓ COMPONENT: SessionCanvas
  📜 PURPOSE: Main canvas for Thinker brainstorm sessions.
  🔗 RELATES: [[ThinkerSession]], [[IdeaBubble]]
  ⚡ FLOW: [AppShell] -> [This] -> [SessionAPI]
-->
```

**CSS:**
```css
/*
 * ⚓ COMPONENT: ThinkerStyles
 * 📜 PURPOSE: Styles for the Thinker brainstorm canvas and idea bubbles.
 * 🔗 RELATES: [[SessionCanvas]]
 */
```

## 7. Documentation and Playbooks

Apply markers in Markdown and other documentation so agents can find intent quickly.

**Required (top of file):**

```markdown
<!-- AGENT: Short purpose and scope for this document. -->
```

**Optional inline anchors:**

```markdown
<!-- @entrypoint: Primary workflow start for this doc -->
<!-- ⚓ ConceptName: Canonical explanation lives here -->
```

## 8. Relationship to the Knowledge Base

Markers and the knowledge base (`KNOWLEDGE_ARCHITECTURE.md`) serve different purposes but reinforce each other:

| Artifact | Purpose | Lives In |
|----------|---------|----------|
| Semantic Markers | Fast in-file navigation and context | Source files (comments) |
| `concepts.yaml` | Cross-file concept registry | `./agentknowledge/` |
| `decisions.yaml` | Architectural decision log | `./agentknowledge/` |
| Repository Index | Full-text + marker search | `./local/repo-index.sqlite` |

When you add an `⚓ ConceptName` anchor to a source file, also ensure the concept is registered in `concepts.yaml` so agents can look it up without scanning every file.

## 9. Do and Do Not

**Do**
- Add headers to all non-trivial files you touch.
- Use `// @entrypoint` on public API surfaces.
- Keep markers in sync with code changes.
- Update `concepts.yaml` when adding a new `⚓ ConceptName` anchor.
- Rebuild the repository index after a marker migration pass (`python3 scripts/repo-index.py rebuild`).

**Do Not**
- Add markers to tiny utility files unless they are core to a workflow.
- Duplicate headers; update the existing block instead.
- Use markers to hide TODO work; use `TODO` or `@agent:*` tags.
- Invent new marker tags outside this document; extend this list first so all agents share the same vocabulary.