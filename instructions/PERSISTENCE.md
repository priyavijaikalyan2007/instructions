<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: a300e0c9-c0e4-436c-a338-9d58103f24de
Created: 2026
-->

<!-- AGENT: Storage, transactions, migrations, data integrity, and persistence checks across targets. -->

# Persistence and data integrity

Read this guide when work changes stored data, transactions, schema evolution, or persistence behavior.
Backend services, native applications, and local tools can all persist data.
SQL source conventions remain in [SQL.md](sql/SQL.md). Browser storage adapters remain in [FRONTEND.md](frontend/FRONTEND.md).
User-visible save and recovery behavior belongs to [UI_UX.md](UI_UX.md#save-and-navigation-safety).

| Storage work | Related guidance |
| --- | --- |
| SQL syntax, naming, queries, indexes, and engine-specific tuning | [SQL.md](sql/SQL.md) |
| Native storage and document lifecycle | [APPS.md](apps/APPS.md) |
| Local files and CLI processing | [TOOLS.md](tools/TOOLS.md) |
| Ownership and authorization | [ACCESS_CONTROL.md](ACCESS_CONTROL.md) |
| Deletion and retention behavior | [DELETION.md](DELETION.md) |
| Failure signals and protection against destructive writes | [PRAGMATIC_PROGRAMMER.md](PRAGMATIC_PROGRAMMER.md#degraded-behavior-and-data-integrity) |

## Read by storage work

| Changed behavior | Sections |
| --- | --- |
| Database source, migration ownership, and service boundaries | [Database source ownership](#database-source-ownership) |
| Related writes, integrity, and persistence checks | [Related writes and transactions](#related-writes-and-transactions) |
| PostgreSQL/EF Core manual SQL workflow | [Configured example](#postgresql-and-ef-core-manual-sql-example) |
| Async side effects or precomputed data | [Transactional outbox](#transactional-outbox), [materialized projections](#materialized-projections) |
| EF Core query translation or computed properties | [Query convention](#entity-framework-query-convention), [computed properties](#entity-framework-computed-properties) |
| Context and connection ownership | [Operation lifetimes](#operation-and-connection-lifetimes) |

## Database source ownership

Apply the [shared database ownership convention](REPO.md#service-database-ownership) when a new service owns database scripts.
Use `src/service/<service-name>/database/` rather than a repository-wide directory shared implicitly by unrelated services.
Keep only the migration, schema, and seed inputs required by the configured workflow.
Do not maintain an editable schema dump alongside migrations unless the build verifies their relationship.
Keep backend entities, ORM mappings, and repositories under backend/.
Tool-required migration classes and snapshots can remain in their backend project.
Choose one authoritative migration sequence per schema and record its owner and execution command in project facts.

Use `src/database/<database-name>/` only for a deliberately independent database component with an explicit migration owner.
A shared database server does not require shared schema ownership or a shared source directory.
Keep infrastructure definitions in deploy/ and operating procedures in playbooks/.
Keep database files, credentials, backups, and production dumps outside tracked source.
Native and tool storage remains with its app or tool. Do not introduce a service database layout for local persistence.

When new database scripts enter scope, add their source path to the owning backend component's profile.
If SQL files change, select SQL guidance alongside persistence guidance.
Preserve an existing migration path until a separately approved migration updates scripts, deployment inputs, and tests.

## Related writes and transactions

Commit related writes in one database transaction when they must succeed or fail together.
Do not swallow a secondary write failure and report success while leaving required records inconsistent.
For writes across databases or external services, define delivery, retry, idempotency, and reconciliation requirements before choosing a mechanism.
Use the project's migration convention and verify that a new environment receives its required schema baseline before incremental migrations.
Test database-specific constraints and transactions against the actual database engine rather than an in-memory substitute.

## PostgreSQL and EF Core manual-SQL example

This example applies only when the consuming repository declares a PostgreSQL/EF Core workflow based on manual SQL migrations.
Its paths, names, history-table insert, and version are examples of that workflow, not universal persistence requirements.
Use the consuming repository's configured migration convention and versions.

- Use the configured PostgreSQL and data-access versions. Keep executable SQL migration scripts in the project's migration directory.

### Plain SQL Over ORM Migration Tools
Always prefer writing plain SQL scripts for database migrations instead of using ORM migration tools like `dotnet ef migrations`. This approach:
- Provides better control and visibility over what changes are being made
- Avoids version mismatches and tooling issues
- Is more portable and easier to review
- Works reliably regardless of ORM tool versions

### Migration Guidelines
- For a new service, place SQL scripts in `src/service/<service-name>/database/migrations/`.
- Preserve an existing configured migration path. Use naming format: `YYYYMMDD_description.sql`.
- Use `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS` for idempotency
- Include proper foreign key constraints with `ON DELETE CASCADE` or `ON DELETE SET NULL` as appropriate
- Add timestamps (`created_at`, `updated_at`) to all tables
- After running the SQL, record the migration in EF Core's history table:
  ```sql
  INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
  VALUES ('YYYYMMDD_MigrationName', '10.0.2')
  ON CONFLICT ("MigrationId") DO NOTHING;
  ```

### Running Migrations
Use `psql` directly to run migrations:
```bash
PGPASSWORD=<password> psql -h <host> -p <port> -U <user> -d <database> -f <migration_file.sql>
```

## Transactional outbox

*   **Purpose:** Prevent blocking user requests during external side-effects (emails, search index updates).
*   **Implementation:** Save the event to an `outbox` table in the same DB transaction; process via background worker.

## Materialized projections

The PostgreSQL implementation below applies only when that database is configured.
Other engines use the project's declared projection mechanism.

*   **Purpose:** Pre-calculate complex joins into a flat, read-optimized table.
*   **Implementation:** Use Postgres `MATERIALIZED VIEW` with unique indexes and concurrent refreshes.

---

## Entity Framework query convention

* StyleCop and compiler warnings are constantly emitted that says do not use String.Equals instead suggesting StringComparison. However, this is NOT correct advice for Dotnet Entity Framework (EF) and LINQ queries. When you need to make case insensitive comparisons, you will have to use String.Equals with appropriate case conversion first done on arguments.

## Entity Framework computed properties

- **Explicit Ignores:** In EF Core, use Fluent API `modelBuilder.Entity<T>().Ignore(x => x.Prop)` for all computed properties. Do not rely on `[NotMapped]`.

## Operation and connection lifetimes

Match service and connection lifetimes to the request or operation. Do not share a non-thread-safe context between concurrent operations.
