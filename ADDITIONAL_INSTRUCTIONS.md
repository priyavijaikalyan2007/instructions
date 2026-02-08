# Additional Instructions for Coding Agents

## Coding

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


## Testing

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
- Use test users in the format `userNNN@test.knobby.io` (e.g., `user001@test.knobby.io`, `user042@test.knobby.io`).
- `test.knobby.io` is a non-existent domain reserved exclusively for testing.
- The test login endpoint must only be enabled in the local **testing** environment.
- Logins from `@test.knobby.io` must only be accepted in the local **testing** environment.
- Logins from `@test.knobby.io` must be **rejected** in development and production environments.
- Test login endpoints must be **disabled and non-functional** in development and production environments.

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

## Settings

### Feature Settings Management
Every new feature, capability, application, or change may introduce settings that control behavior. You must:
- Identify any new settings required by the change
- Update workspace and global settings dialogs to include new settings
- Choose sensible defaults for all new settings
- Ensure global-to-workspace settings inheritance remains intact
