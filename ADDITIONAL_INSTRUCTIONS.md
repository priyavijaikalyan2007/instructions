<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: afef1ced-80d9-421b-9bbc-06e17b7b7fce
Created: 2026
-->

<!-- AGENT: Additional context-specific instructions and exceptions for coding agents. -->

# Additional Instructions for Coding Agents

These instructions supplement `AGENTS.md`, `CODING_STYLE.md`, and the selected target guides. They capture reusable lessons for apps, tools, websites, and web applications. Bootstrap-specific rules apply to projects that use that library.

---

## Coding

### Context Efficiency (Token Discipline)

- **"Read once, cite forever; research before you edit."**
- **Cite, don't re-read.** If you have already read a file in the current session, refer to it by `path:line` (e.g., `frontend/component-studio.html:142`) instead of re-reading it. Only re-`Read` when:
  1. The file has been edited since you last read it (by you or a hook), OR
  2. You need lines outside the range you previously read, OR
  3. Enough turns have passed that the content was likely compressed out of context.
  When you do re-read a partial range, use `offset` and `limit` — never re-read a whole file to grab one function.
- **Read tightly.** Prefer `Grep` with `-n` and small `-C` context (2–5 lines) over `Read` of an entire file. Reserve full `Read` for files under ~300 lines, or when you genuinely need the whole picture (e.g., understanding a class structure end-to-end).
- **Read before edit; research before modify.** Before `Edit`/`Write` on a file, you must have read it in this session. Before modifying a function's signature or behaviour, `Grep` for all callers (by symbol name) so you know the blast radius. Editing blind causes failed edits, rollbacks, and rework — all of which cost more tokens than the upfront read.
- **Target prompts to exact locations.** When delegating to subagents or describing work, name the file and line range (`In api/Services/AuthService.cs lines 80–140, the ValidateToken method...`). This prevents the subagent from re-discovering what you already know.
- **Trust prior context within a session.** Do not re-verify file contents you just edited — `Edit`/`Write` would have errored if it failed. The harness tracks file state for you.

### Source and Contract Verification

- Edit source files rather than generated or copied build output. Confirm the source/output mapping before changing an unfamiliar file.
- Verify dependency APIs against the version actually shipped. Check the host runtime before adding a replacement for an existing service.
- See [BACKEND.md](./BACKEND.md#existing-host-dependency-verification).
- Stage only files that belong to the task. Preserve unrelated working-tree changes and useful failure evidence.
- Record accepted quality deviations with a reason, owner, resolution plan, and review trigger in the project's existing tracking record.
- Treat measured counts as dated evidence. Record the file set, counting rule, command, and known exclusions.

### Bootstrap Discipline

See [FRONTEND.md](./FRONTEND.md#existing-bootstrap-discipline).

### Component Self-Containment

See [FRONTEND.md](./FRONTEND.md#existing-component-boundaries).

### C# Linting

- See [BACKEND.md](./BACKEND.md#existing-entity-framework-query-convention).
* Please place `using` statements inside the namespace.

### Data Contract Mandate (The "Rosetta Stone" Rule)

See [SAAS.md](./SAAS.md#existing-data-contract-verification).

### The "Hollow Function" Prohibition

See [SAAS.md](./SAAS.md#existing-persistence-and-ui-integration).

### Complexity & State Management

- **"Assume nesting, assume async, assume latency."**
- **Await Everything:** All data modification functions must be `async` and properly `await`ed before rendering.
- **Recursive awareness:** If a data model is hierarchical (trees, checklists, folders), update logic **must** be recursive or use flattened ID lookups. Simple index-based access (`list[i]`) is forbidden for nested data.
- See [FRONTEND.md](./FRONTEND.md#existing-canvas-sizing).

### Security Defaults

See [BACKEND.md](./BACKEND.md#existing-api-security-defaults).

### Root Cause Refactoring (No Ad-Hoc Patches)

- **"Fix it right, don't just make it work."**
- **Consolidate, Don't Duplicate:** If you find duplicate or parallel implementations (e.g., a JS registry and a TS registry), do not patch the one that "works" and force the system to use both.
  - **Action:** Merge the logic into the strictly better implementation (e.g., TypeScript) and delete the legacy/duplicate file.
- **Deep Fixes:** Do not write "glue code" to handle bugs in upstream logic. Fix the upstream logic.

### Data & Naming Consistency

See [SAAS.md](./SAAS.md#existing-cross-layer-naming).

### Direct Type Compatibility (No Unnecessary Adapters)

- **"Align the source, don't bridge the gap."**
- **Eliminate Converters:** If Module A produces data that Module B cannot consume directly:
  - **Do NOT** write a converter/mapper function between them if you own both modules.
  - **Action:** Refactor Module A or Module B so that their data types are identical.
- **Performance:** Unnecessary conversion layers waste CPU cycles and introduce points of failure.

### Architectural Homogeneity (The "Look Left, Look Right" Rule)

- **"Do not invent new patterns."**
- **Pattern Mimicry:** Before writing a new Controller, Service, or Component, examine three existing ones.
  - If existing Controllers use a Service layer, **do not** write a Controller that queries EF Core directly.
  - If existing Frontend components use `React Query`, **do not** write a component that uses `fetch` in `useEffect`.
  - If the backend uses the Repository pattern, **do not** introduce the Unit of Work pattern or direct `DbContext` usage in a single isolated area.
- **Async Consistency:** Do not mix `Promise.then()` chains with `async/await`. If the codebase uses `async/await`, use it exclusively.

### Dependency Discipline (The "No New Toys" Rule)

- **"Use what is already there."**
- **Duplicate Check:** Before adding a package, check the project manifests and lockfiles for an existing dependency that meets the need.
  Include `Package.swift`, `go.mod`, `Cargo.toml`, Maven/Gradle files, `package.json`, and `.csproj` files where applicable. Adding a dependency requires justification.
  - If `Day.js` is installed, **do not** install `Moment.js`.
  - If `Newtonsoft.Json` is used, **do not** introduce `System.Text.Json` unless part of a documented migration.
- **Triviality Check:** Do not add libraries for trivial one-line functions (e.g., `is-odd`, `left-pad`). Write the helper function yourself.
- See [FRONTEND.md](./FRONTEND.md#existing-browser-dependency-restriction).

### Async Consistency

- **"One style, everywhere."**
- If the codebase uses `async/await`, use it exclusively. Do not mix `Promise.then()` chains with `async/await` in the same component.

### Visual & Styling Rigor

See [FRONTEND.md](./FRONTEND.md#existing-styling-consistency).

### Error Handling Standardization

- **"Fail consistently."**
- **Unified Strategy:** Do not mix "Return Null on Failure" with "Throw Exception on Failure". Inspect the `Services` folder to determine the project's standard contract.
- See [FRONTEND.md](./FRONTEND.md#existing-ui-error-propagation).

### Configuration & Magic Constants

- **"No Magic Numbers."**
- **Extraction:** Any number (e.g., `3000` ms timeout) or string (e.g., "Admin" role) that appears more than once—or has semantic meaning—must be a named constant.
- See [SAAS.md](./SAAS.md#existing-application-url-configuration).

### Code Hygiene & "Zombie" Code

- **"Delete, don't disable."**
- **No Commented-Out Code:** Do not leave blocks of commented-out code (C#, SCSS, TypeScript, Javascript or HTML) "just in case". Rely on Git history.
- **Import Cleanup:** Unused imports and variables are (C# usings, SCSS imports, TypeScript imports, and variables are technical debt. Remove them immediately before considering a task complete. Remove them before considering a task complete.
- See [FRONTEND.md](./FRONTEND.md#existing-stylesheet-cleanup).


## Testing

### SCSS Build Verification

See [STATIC_ASSETS.md](./STATIC_ASSETS.md#existing-stylesheet-build-checks).

### Component Testing

See [FRONTEND.md](./FRONTEND.md#existing-component-tests).

### Visual Verification

See [FRONTEND.md](./FRONTEND.md#existing-component-visual-checks).

### Unit Tests
You must always add unit tests for all code changes. This is non-negotiable.

### Testing Strategy
- **Bug Fixes**: When fixing bugs, add regression tests to prevent the bug from recurring.
- **New Features**: When adding features, functionality, or capabilities, add unit tests that verify:
  - All expected functionality works correctly (happy paths)
  - Invalid inputs, edge cases, and failure conditions are handled properly (unhappy paths)
  - In other words, test both what *should* work and what *should not* be possible or work.

### Playwright Tests

See [FRONTEND.md](./FRONTEND.md#existing-browser-workflow-tests).

### Test Users

See [SAAS.md](./SAAS.md#existing-local-test-identities).

## Clarification

### Clarifying Questions
When any aspect of a task is unclear or ambiguous, ask clarifying questions before proceeding. Present the various choices or interpretations you see. It is better to ask questions than to make potentially incorrect assumptions.

### Avoid Assumptions (User Configuration First)
When the product already provides user-configurable settings (e.g., AI provider/model, API keys, tenant/workspace settings), **do not hardcode or assume defaults**. Always:
- Use the existing configuration surfaces and stored settings.
- If a required configuration is missing or ambiguous, **ask the user** rather than choosing a model/provider or behavior unilaterally.
- Document any fallback behavior explicitly and only after confirmation.

### UX First
Always consider the user experience before finalizing UI or workflow changes.
- Consult `UX_UI_GUIDELINES.md` for any UI/UX work.
- If a `UI_UX_EXPERIENCES.md` file exists, consult it as well and follow its guidance.
- If the intended user flow is unclear, **pause and ask for clarification**.

## Memory

### CONVERSATION.md Updates
You must always update `CONVERSATION.md` with a brief description of changes made after each set of changes. This file serves as organizational and agentic memory tracking the evolution of the product. Do not skip this step.

## Changes
### `git commit`
You must always commit all changes to `git` with a concise description of changes made after each set of changes. This ensures that work is not lost.

## Access Control

See [SAAS.md](./SAAS.md#existing-access-control-integration).

### RBAC & FGAC Compliance

See [SAAS.md](./SAAS.md#existing-access-control-integration).

## Database Migrations

See [BACKEND.md](./BACKEND.md#existing-database-migrations).

### Plain SQL Over ORM Migration Tools

See [BACKEND.md](./BACKEND.md#existing-database-migrations).

### Migration Guidelines

See [BACKEND.md](./BACKEND.md#existing-database-migrations).

### Running Migrations

See [BACKEND.md](./BACKEND.md#existing-database-migrations).

### CDN Component Integration

See [STATIC_ASSETS.md](./STATIC_ASSETS.md#existing-cdn-component-integration).

### UI State Management

See [FRONTEND.md](./FRONTEND.md#existing-component-state).

## Settings

See [SAAS.md](./SAAS.md#existing-workspace-settings-integration).

### Feature Settings Management

See [SAAS.md](./SAAS.md#existing-workspace-settings-integration).
