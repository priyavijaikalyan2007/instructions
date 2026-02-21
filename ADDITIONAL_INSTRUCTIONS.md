<!-- AGENT: Additional context-specific instructions and exceptions for coding agents. -->

# Additional Instructions for Coding Agents

These instructions supplement the primary guidelines in `AGENTS.md`, `CODING_STYLE.md`, and `FRONTEND.md`. They capture lessons learned and non-obvious rules specific to this Bootstrap 5 theme and component library.

---

## Coding

### Bootstrap Discipline

- **"Override, don't overwrite."**
- **Variables First:** When changing the appearance of any Bootstrap element, modify `_variables.scss` before writing custom CSS. If Bootstrap provides a variable for the property, use it.
- **No Hardcoded Values:** Never hardcode hex colours (e.g., `#FF0000`), pixel sizes, or font stacks in component SCSS or HTML. Use the semantic names defined in `_variables.scss` (e.g., `$danger`, `$font-size-sm`, `$spacer`).
- **Unit Consistency:** Do not mix `px`, `rem`, `em`, and `%` arbitrarily. Follow the spacing scale in `_variables.scss`. Use `rem` for sizing, `px` only for borders and fine details (1px borders, box shadows).
- **Explicit Dependencies:** If a component requires Bootstrap JavaScript (e.g., `bootstrap.Modal`), document this in the component's README and in `COMPONENTS.md`.

### Component Self-Containment

- **"Components are guests, not owners."**
- **No Global Side Effects:** A component's SCSS must not modify global Bootstrap styles, override utility classes, or change the behaviour of elements outside its own scope.
- **Namespace Classes:** Prefix all custom classes with the component name (e.g., `.errordialog-header`, `.combobox-dropdown`). Do not use generic class names like `.header` or `.dropdown-list` that could collide with Bootstrap or the host application.

### C# Linting

* StyleCop and compiler warnings are constantly emitted that says do not use String.Equals instead suggesting StringComparison. However, this is NOT correct advice for Dotnet Entity Framework (EF) and LINQ queries. When you need to make case insensitive comparisons, you will have to use String.Equals with appropriate case conversion first done on arguments. 
* Please place `using` statements inside the namespace.

### Data Contract Mandate (The "Rosetta Stone" Rule)

- **"Explicitly define the data contract between layers."**
-  **Casing Check:** When writing API endpoints or Client wrappers, you **must** explicitly verify JSON property names.
  - *C# Backend:* Use `[JsonPropertyName("camelCaseName")]` on DTOs to ensure frontend compatibility.
  - *JS Client:* If the backend expects `snake_case`, use a `toBackendFormat()` mapper. **Never assume automapping works.**
- **Payload Verification:** Before marking a task done, verify: "Does the frontend payload structure (nested objects, field names) match the backend DTO *exactly*?"

### The "Hollow Function" Prohibition

- **"UI updates are secondary to Persistence."**
- **Persistence First:** When implementing a CRUD action (Delete, Save, Update), write the API call **first**. Do not write the optimistic UI update until the API call is scaffolded.
- **Verify the Loop:** For every `delete()` or `save()` function:
  - Does it call `api.doAction()`?
  - Does `api.doAction()` make a `fetch()`?
  - Does the backend endpoint actually *use* the received data? (Check for "ignored parameters").

### Complexity & State Management

- **"Assume nesting, assume async, assume latency."**
- **Await Everything:** All data modification functions must be `async` and properly `await`ed before rendering.
- **Recursive awareness:** If a data model is hierarchical (trees, checklists, folders), update logic **must** be recursive or use flattened ID lookups. Simple index-based access (`list[i]`) is forbidden for nested data.
- **Explicit Dimensions:** For canvas/visualization libraries (Cytoscape, maxGraph), **never** rely on CSS flexbox/grid alone. Always enforce or check for explicit pixel dimensions (`getBoundingClientRect()`) before initialization.

### Security Defaults

- **"Secure by Design, not by Patch."**
- **No PII in URLs:** Never pass email, names, or IDs in Query Parameters. Use Session/Claims or POST bodies.
- **Auth Decorators:** No API endpoint is created without an `[Authorize]` or `[RequirePermission]` attribute unless explicitly public (like login).
- **Explicit Ignores:** In EF Core, use Fluent API `modelBuilder.Entity<T>().Ignore(x => x.Prop)` for all computed properties. Do not rely on `[NotMapped]`.

### Root Cause Refactoring (No Ad-Hoc Patches)

- **"Fix it right, don't just make it work."**
- **Consolidate, Don't Duplicate:** If you find duplicate or parallel implementations (e.g., a JS registry and a TS registry), do not patch the one that "works" and force the system to use both.
  - **Action:** Merge the logic into the strictly better implementation (e.g., TypeScript) and delete the legacy/duplicate file.
- **Deep Fixes:** Do not write "glue code" to handle bugs in upstream logic. Fix the upstream logic.

### Data & Naming Consistency

- **"Uniformity is a feature."**
- **Global Standards:** If you encounter a camelCase vs. snake_case mismatch between backend/frontend or components:
  - **Do NOT** apply local patches or field renaming in a single component.
  - **Action:** Enforce a system-wide serialization standard (e.g., Global JSON settings in Program.cs). Ensure all APIs conform to this standard.
- **Rule:** A codebase should look like it was written by one person. Mismatched casing styles across files are unacceptable.

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
- **Duplicate Check:** Before adding a new package (npm or NuGet), check `package.json` or check `.csproj` files. This library has minimal dependencies by design (Bootstrap, Sass, PostCSS, Wrangler). Adding a dependency requires justification.
  - If `Day.js` is installed, **do not** install `Moment.js`.
  - If `Newtonsoft.Json` is used, **do not** introduce `System.Text.Json` unless part of a documented migration.
- **Triviality Check:** Do not add libraries for trivial one-line functions (e.g., `is-odd`, `left-pad`). Write the helper function yourself.
- **No UI Frameworks:** Do not install React, Vue, Angular, jQuery, or any UI framework. This is explicitly prohibited by the project's architecture.

### Async Consistency

- **"One style, everywhere."**
- If the codebase uses `async/await`, use it exclusively. Do not mix `Promise.then()` chains with `async/await` in the same component.

### Visual & Styling Rigor

- **"Single Source of Truth."**
- **Framework Purity:** If the project uses Tailwind CSS, **do not** write inline `style={{ ... }}` or create separate `.css` files.
- **Unit Consistency:** Do not mix `px`, `rem`, `em`, and `%` arbitrarily. Inspect `tailwind.config.js` or `variables.css` and use the defined spacing/color scales.
- **Color Variables:** Never hardcode hex codes (e.g., `#FF0000`). Use the semantic names defined in the theme (e.g., `text-error`, `bg-primary`).

### Error Handling Standardization

- **"Fail consistently."**
- **Unified Strategy:** Do not mix "Return Null on Failure" with "Throw Exception on Failure". Inspect the `Services` folder to determine the project's standard contract.
- **UI Propagation:** Ensure errors propagate to the UI consistently. If the app uses a global Toast notification system for API errors, do not implement a local `alert()` or console-only error log.

### Configuration & Magic Constants

- **"No Magic Numbers."**
- **Extraction:** Any number (e.g., `3000` ms timeout) or string (e.g., "Admin" role) that appears more than once—or has semantic meaning—must be a named constant.
- **Environment Isolation:** **Never** hardcode URLs (e.g., `http://localhost:5000`) inside code. Use `appsettings.json` (backend) or `import.meta.env` (frontend).

### Code Hygiene & "Zombie" Code

- **"Delete, don't disable."**
- **No Commented-Out Code:** Do not leave blocks of commented-out code (C#, SCSS, TypeScript, Javascript or HTML) "just in case". Rely on Git history.
- **Import Cleanup:** Unused imports and variables are (C# usings, SCSS imports, TypeScript imports, and variables are technical debt. Remove them immediately before considering a task complete. Remove them before considering a task complete.
- **No Dead CSS:** If a refactor removes a component or class, delete the corresponding styles. Do not leave orphaned selectors.


## Testing

### SCSS Build Verification

You must verify that `npm run build` completes without errors after every change to SCSS files. A broken build is never acceptable.

### Component Testing

When building TypeScript components, add unit tests using Jest or Vitest that verify:
- The component initialises correctly with valid inputs.
- The component handles missing or invalid inputs gracefully (logs a warning/error, does not throw).
- The component produces the expected DOM structure.

### Visual Verification

After any theme or component change, open `demo/index.html` in a browser and visually verify that:
- No existing components are broken.
- New components render as specified.
- Colours, spacing, and typography are consistent with the theme.

### Unit Tests
You must always add unit tests for all code changes. This is non-negotiable.

### Testing Strategy
- **Bug Fixes**: When fixing bugs, add regression tests to prevent the bug from recurring.
- **New Features**: When adding features, functionality, or capabilities, add unit tests that verify:
  - All expected functionality works correctly (happy paths)
  - Invalid inputs, edge cases, and failure conditions are handled properly (unhappy paths)
  - In other words, test both what *should* work and what *should not* be possible or work.

### Playwright Tests
You must add Playwright end-to-end tests for all user-facing changes.

### Test Users
- Use test users in the format `userNNN@test.<appdomain>.io` (e.g., `user001@test.domain.io`, `user042@test.domain.io`).
- `test.<appdomain>.io` is a non-existent domain reserved exclusively for testing.
- The test login endpoint must only be enabled in the local **testing** environment.
- Logins from `@test.<appdomain>.io` must only be accepted in the local **testing** environment.
- Logins from `@test.<appdomain>.io` must be **rejected** in development and production environments.
- Test login endpoints must be **disabled and non-functional** in development and production environments.

---

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

### RBAC & FGAC Compliance
A full Role-Based Access Control (RBAC) and Fine-Grained Access Control (FGAC) system has been implemented. Refer to:
- `specs/access_control.raw.md`
- `specs/access_control.prd.md`
- `ACCESS_CONTROL.md`

For every new application, resource type, or feature, you must:
- Identify what access control changes are needed
- Implement proper permission checks
- Update access control specifications if new resource types or permissions are introduced

## Database Migrations

### Plain SQL Over ORM Migration Tools
Always prefer writing plain SQL scripts for database migrations instead of using ORM migration tools like `dotnet ef migrations`. This approach:
- Provides better control and visibility over what changes are being made
- Avoids version mismatches and tooling issues
- Is more portable and easier to review
- Works reliably regardless of ORM tool versions

### Migration Guidelines
- Place SQL migration scripts in `/sql/migrations/` with naming format: `YYYYMMDD_description.sql`
- Use `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS` for idempotency
- Include proper foreign key constraints with `ON DELETE CASCADE` or `ON DELETE SET NULL` as appropriate
- Add timestamps (`created_at`, `updated_at`) to all tables
- After running the SQL, record the migration in EF Core's history table:
  ```sql
  INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
  VALUES ('YYYYMMDD_MigrationName', '10.0.2')
  ON CONFLICT ("MigrationId") DO NOTHING;
  ```
- Update the model snapshot (`KnobbyDbContextModelSnapshot.cs`) manually to keep EF Core in sync

### Running Migrations
Use `psql` directly to run migrations:
```bash
PGPASSWORD=<password> psql -h <host> -p <port> -U <user> -d <database> -f <migration_file.sql>
```

### CDN Component Integration

**Fallback Code Prohibition:**
Do NOT write fallback code assuming shared UI components break. Assume that they should work and the UI
team is committed to fixing them. This additional complexity is unnecessary. If there is an issue with
a component, produce a bug report instead.

**Peer Dependency Loading:**
CDN components may wrap third-party libraries (e.g., MarkdownEditor wraps Vditor, Diagrams wraps
maxGraph). When adding a CDN component to an HTML page:
1. Check what peer dependencies the component requires (look for `window.X` checks or "library not
   found" error messages in the component source).
2. Load the peer dependency's CSS in `<head>` **before** the component's CSS.
3. Load the peer dependency's JS via `<script>` **before** the component's JS.
4. If you are unsure whether a peer dependency is needed, fetch the component JS and search for
   `window.` global checks or console error messages about missing libraries.

**API Signature Verification:**
Before calling a CDN component factory function, verify the actual function signature by reading the
component source. Do NOT guess parameter order or option names from memory. Common mistakes:
- Passing a single options object when the factory takes `(id: string, options)`.
- Using option names that don't exist (e.g., `theme`, `showToolbar` instead of `contained`,
  `showInlineToolbar`).
- Using invalid enum values (e.g., `mode: 'split'` instead of `mode: 'sidebyside'`).

**Toolbar State Management:**
When using the CDN Toolbar component, ALL button state changes must go through `toolbar.setToolState()`.
Never use direct DOM manipulation (`classList.toggle('active', ...)`) on toolbar buttons — this causes
the component's internal state to diverge from the visual state.

## Settings

### Feature Settings Management
Every new feature, capability, application, or change may introduce settings that control behavior. You must:
- Identify any new settings required by the change
- Update workspace and global settings dialogs to include new settings
- Choose sensible defaults for all new settings
- Ensure global-to-workspace settings inheritance remains intact
