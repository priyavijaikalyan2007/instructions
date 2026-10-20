<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 65f0c083-038c-4fb4-8271-644cacaee806
Created: 2026
-->

<!-- AGENT: Marker guidance for fast navigation and shared conventions. -->
# Agent Navigation Markers and Annotations

To accelerate agent comprehension and navigation, we use a standard system of **Semantic Markers**. 
These markers act as high-speed indexing tags, allowing agents to understand a file's purpose, dependencies,
and flow without analysing the entire content.

---

## 0. Principles

- **Be consistent:** Use the same marker names everywhere.
- **Be minimal:** Add only markers that materially improve navigation.
- **Keep them current:** If you change responsibility or flow, update markers in the same edit.
- **Do not change logic:** Markers are comments or directives only.

---

## 1. The "Fast-Read" File Header

Every significant source file (C#, Swift, Go, Rust, Java, TypeScript, SCSS, HTML, and Markdown)
containing classes, services, controllers, components, utilities and more must start with a **Structured Header Block**. 
This allows agents to read the first 20 lines of a file and immediately understand its context.

### TypeScript Format

See [TypeScript](typescript/TYPESCRIPT.md#navigation-markers).

### C# Format

See [C#](csharp/CSHARP.md#navigation-markers).

### Swift, Go, Rust, and Java Format

Use the header syntax and directive-placement rules in the selected language guide.
Keep public documentation comments separate from navigation metadata.
Use the standard COMPONENT, PURPOSE, RELATES, FLOW, and optional SECURITY fields.
Do not add comments to formats that prohibit them, such as JSON.
Keep public documentation comments separate as described in [COMMENTING.md](COMMENTING.md).
Do not insert markers between a documentation comment or annotation and its declaration.
Use ASCII field names when a parser or file format does not support the marker symbols.
Preserve the directive positions and blank lines required by the selected language.
Keep required copyright information in the existing file header.

### Python Format

See [Python](python/PYTHON.md#navigation-markers).

### Swift Format

See [Swift](swift/SWIFT.md#navigation-markers).

### Go Format

See [Go](go/GO.md#navigation-markers).

### Rust Format

See [Rust](rust/RUST.md#navigation-markers).

### Java Format

See [Java](java/JAVA.md#navigation-markers).

### SCSS Format

See [SCSS](scss/SCSS.md#navigation-markers).

### HTML Format

See [HTML](html/HTML.md#navigation-markers).

### CSS Format

See [CSS](css/CSS.md#navigation-markers).

## 2. In-Code Semantic Tags

Use these tags within comments to map logic flow and decision history.

### 2.1 Navigation Tags

- `// @entrypoint`: Marks the start of a public API or execution flow.
- `// @dependency: [File/Service/Component]`: Explicitly marks a hidden or key dependency.
- `// @maps_to: [DB_Table/Column]`: Links code entities to database schema.
- `// @config: [SettingName]`: Marks a dependency on a configuration value (SCSS variable, build option, env var, appsettings key).
- `// @middleware`: Marks a middleware or pipeline component that intercepts requests.
- `// @background`: Marks a background job, hosted service, or scheduled task.

### 2.2 Logic Flow Indicators

- `// -> Dispatches: [EventName]`: Indicates an event emission (e.g., custom DOM events).
- `// <- Handles: [EventName]`: Indicates an event handler.
- `// >> Delegates to: [Component]`: Indicates a hand-off of responsibility (e.g., calling Bootstrap's Modal API).

### 2.3 Context Anchors

- `// ⚓ [ConceptName]`: Defines the canonical location for a design or business concept.
    - *Usage:* "If you are looking for how 'Tax' is calculated, look for `⚓ TaxCalculation`."
    - *Usage:* "If you are looking for how the enterprise colour palette is defined, look for `⚓ EnterpriseTheme`."

### 2.4 Agent Work Tags

Use these tags for targeted follow-up by other agents. Align with `instructions/COMMENTING.md`.

- `// @agent:test` — Requires tests or test coverage.
- `// @agent:security` — Requires security review (e.g., DOM injection risks).
- `// @agent:review` — Requires human verification.
- `// @agent:refactor` — Candidate for future refactor.

### 2.5 Annotation Alignment

The semantic markers above complement the standard annotations defined in `instructions/COMMENTING.md`
(`TODO`, `FIXME`, `SECURITY`, `PERF`, etc.). Use annotations for *status* (what state is this code in?) 
and semantic markers for *navigation* (where does this code fit in the system?). 
Both are captured by the repository index (see `instructions/REPO_INDEX.md`).

---

## 3. Global Concept Registry

We use **Wiki-Style Links** `[[ConceptName]]` in comments to reference shared concepts or business logic across the stack.

- **Syntax:** `[[Concept]]`
- **Behavior:** Agents should search for `⚓ Concept` to find the definition.

**Example:**

See [TypeScript](typescript/TYPESCRIPT.md#3-global-concept-registry).

See [SCSS](scss/SCSS.md#3-global-concept-registry).

See [C#](csharp/CSHARP.md#3-global-concept-registry).

---

## 4. Section Markers (Long Files)

Use clear section headers so agents can scan large files quickly.

**TypeScript:**

See [TypeScript](typescript/TYPESCRIPT.md#4-section-markers-long-files).

**SCSS:**

See [SCSS](scss/SCSS.md#4-section-markers-long-files).

**C#:**

See [C#](csharp/CSHARP.md#4-section-markers-long-files).

---

## 5. Language-Specific Collapsible Regions

Use folding syntax from the selected language guide when the project supports it. Keep regions shallow.

## 6. Documentation and Playbooks

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

---

## 8. Relationship to the Knowledge Base

Markers and the knowledge base (`instructions/KNOWLEDGE_ARCHITECTURE.md`) serve different purposes but reinforce each other:

| Artifact | Purpose | Lives In |
|----------|---------|----------|
| Semantic Markers | Fast in-file navigation and context | Source files (comments) |
| `concepts.yaml` | Cross-file concept registry | `./agentknowledge/` |
| `decisions.yaml` | Architectural decision log | `./agentknowledge/` |
| Repository Index | Full-text + marker search | `./local/repo-index.sqlite` |

When you add an `⚓ ConceptName` anchor to a source file, also ensure the concept is registered in `concepts.yaml` 
so agents can look it up without scanning every file.

---

## 9. Do and Do Not

**Do**
- Add headers to all non-trivial files you create or modify.
- Use `// @entrypoint` on public API surfaces (such as public API functions in component TypeScript, C# Controller Classes etc.)
- Keep markers in sync with code changes.
- Update `concepts.yaml` when adding a new `⚓ ConceptName` anchor.
- Rebuild the repository index after a marker migration pass (`python3 scripts/repo-index.py rebuild`).

**Do Not**
- Add markers to tiny utility files unless they are core to a workflow.
- Duplicate headers; update the existing block instead.
- Use markers to hide TODO work; use `TODO` or `@agent:*` tags.
- Invent new marker tags outside this document; extend this list first so all agents share the same vocabulary.
