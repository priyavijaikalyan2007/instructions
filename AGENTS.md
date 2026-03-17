<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: db94a357-73e9-4c29-8a8a-83d8b85f3eb6
Created: 2026
-->

<!-- AGENT: Master instructions file for coding agents; start here for all tasks. -->

# Introduction

First, read `README.md` to understand the situation, background and problem statement we are addressing and the solution we are building. Then continue from here.

# Structure

This folder contains the root of an enterprise SaaS. This SaaS follows a super-app model where the index.html in the `frontend/` folder contains the main frontend shell of the application. Each individual application's frontend code is contained in a separate sub-folder within `frontend/` such as `tenant/`. The backend is Asp.Net Core 10.0 application whose code is in the `api/` folder. All APIs are served by this backend; all frontend routes are served as static files middleware in this application as well. Thus, `api/` and `frontend/` are combined together as a single standalone Asp.NET Core 10.0 application and deployed together in a single Docker container deployed on GCP Cloud Run.

# Instructions

## Stack

**Hybrid Model**: Single server serves both APIs and web pages
- Backend: ASP.NET Core 10.0 (Self-contained deployment)
- Frontend: Vanilla HTML + Javascript (small) + TypeScript (large) + Bootstrap 5 in the folder `./frontend/`
- Frontend Scripts: TypeScript (in the folder `./typescript/` which when compiled with Vite copies compiled files to `./frontend/`)
  - **NOTE**: For all non-trivial frontend scripting, you MUST use TypeScript. The moment any inline Javascript becomes more than 10 lines of code, you should migrate to TypeScript. It is best to write TypeScript from the beginning.
- Database: PostgreSQL 17.6 with Dotnet EF Core. Mirgation and other SQL scripts are placed in `./sql/`. Always write SQL scripts for migration that can be run by the user against the appropriate environment.
- Image Size: ~280-300MB (runtime-deps base + runtime + frontend)
- Deployment: Self-contained (includes .NET runtime) to Cloud Run on Google Cloud Platform.
- **Swagger UI** - http://localhost:8080/swagger. 

## Folder & File Structure

+ typescript/        - All Typesript that will be compiled into Javascript goes here. All compiled output should be placed in frontend/
+ frontend/          - All frontend code (HTML, Javasript, CSS) goes here.
+ api/               - Asp.net Core 10.0 project and code for the monolith backend server. This monolith serves both static routes & APIs.
+ playwrighttests/   - .Net Core 10.0 based Playwright UI tests. 
+ integrationtests/  - .Net Core 10.0 based system integration tests.
+ unittests/         - .Net Core 10.0 based unit tests.
+ sql/               - All SQL code for database creation, modification, updates, migration should be placed here.
+ specs/             - All product specifications (both raw, product requirements etc.) will be found here.
+ playbooks/         - All generated documentation, guides, tutorials etc. relevant to product development and testing should be placed here.
+ docs/              - All product documentation relevant to customers or users or integrators should be placed here.

## Operating Style

Use the **V-V-P-T-I-R-V-C** loop (Plan → Test → Implement → Refactor → Verify) for your core workflow. This is a strict **Test-Driven Development** workflow. For all software engineering tasks, you MUST follow this sequence. **Never write implementation code before writing a failing test.**

+ **Validate (Request):** Analyse the prompt for ambiguity. Restate the core requirement and constraints to ensure alignment before acting.

+ **Verify (State):** Inspect the current codebase context. Read relevant files to confirm the environment is clean and assumptions about the existing code are correct. Consult `agentknowledge/concepts.yaml` to locate related code.

+ **Plan (Design):** Draft a concrete, step-by-step technical plan. This step is where architecture happens — not during implementation. The plan MUST include:
  1. **Files to modify or create** — list every file.
  2. **Pattern selection** — consult `GOF_PATTERNS.md` and select any GoF patterns that apply. Justify each choice against the Balance Checklist. If no pattern is needed, state "No pattern required — simple function/class suffices."
  3. **Interface design** — define the public interfaces (method signatures, DTOs) BEFORE thinking about implementation.
  4. **Layering check** — confirm that business logic is in services (not controllers), HTTP concerns are in controllers, cross-cutting concerns use middleware or filters.
  5. **Review the plan** against project conventions (`CODING_STYLE.md`, `SECURITY_GUIDELINES.md`, `API_GUIDELINES.md`, `PERFORMANCE.md`). Ensure the approach is idiomatic and low-risk.

+ **Test First (Red):** Write the tests BEFORE writing any implementation code. This is the "Red" phase of TDD.
  1. Write unit tests that describe the expected behaviour of the new code. Follow `TESTING.md` conventions (Arrange-Act-Assert, one assertion per test, descriptive names).
  2. For new interfaces or services, write tests against the interface contract.
  3. For bug fixes, write a test that reproduces the bug and currently fails.
  4. For refactorings, verify that existing tests pass as a baseline (per `MIGRATIONS.md` Phase 1). Fill coverage gaps to ≥90% BEFORE refactoring.
  5. Run the tests — they MUST fail (Red). If they pass, the tests are not testing the new behaviour.

+ **Implement (Green):** Write the minimum code needed to make the failing tests pass. This is the "Green" phase of TDD.
  1. Focus on correctness, not elegance. Get the tests to pass with the simplest implementation.
  2. Apply the GoF patterns identified in the Plan step.
  3. Follow `CODING_STYLE.md` (Allman braces, max 30-line methods, max 3 nesting levels, guard clauses).
  4. Add logging per `LOGGING.md`, comments per `COMMENTING.md`, and markers per `MARKERS.md`.
  5. Run the tests — they MUST pass (Green). If they fail, fix the implementation, NOT the tests.

+ **Refactor (Clean):** Now that tests pass, improve the code structure without changing behaviour. This is the "Refactor" phase of TDD. Apply Martin Fowler refactoring techniques:
  1. **Extract Method** — break methods exceeding 30 lines into smaller, named methods.
  2. **Extract Class** — split classes exceeding 500 lines or having multiple responsibilities.
  3. **Replace Conditional with Polymorphism** — replace switch/if-else chains dispatching to type-specific code with Strategy or polymorphic calls.
  4. **Replace Magic String with Symbolic Constant** — replace hardcoded strings in conditionals with enums or constants.
  5. **Move Method** — move logic to the class where it belongs (e.g., business logic out of controllers).
  6. **Encapsulate Collection** — replace `Dictionary<string, object>` with strongly-typed classes.
  7. Run the tests after EACH refactoring step. If tests fail, revert the last refactoring.

+ **Verify (Full):** Execute the new tests AND all relevant regression tests. Ensure everything passes locally. Run `dotnet build` with zero warnings. Run `./test.sh` for full suite validation.

+ **Commit:** Stage the verified changes and create a commit with a concise, conventional message (e.g., `fix: ...`, `feat: ...`, `refactor: ...`). One logical change per commit.

## (CRITICAL) Thinking
I urge you to think along the lines of Steve Jobs, Douglas Normal, Jonathan Ivy and others. The details are important in making sure the software and documentation we provide our users offer an amazing, consistent, thoughtful and complete end to end experience.

## Development (CRITICAL)
- You must adhere to the language conventions provided in LANGUAGE.md.
- You must utilize the navigation markers defined in [MARKERS.md](./MARKERS.md) in all generated code. See the Agent Knowledge Base section below for how to read and update `./agentknowledge/` every session. In additon, use the Git Log, CONVERSATION.md files, specifications in ./specs/ and language server plugins to locate code, decisions and more. Rely on grep and globbing only at the end.
- When dealing with secrets of any kind, especially user provided secrets, always consult SECRET_HANDLING.md to understand how to architect that properly.
- Always consult CODING_STYLE.md when writing code. This is important for maintainability.
- **(CRITICAL)** Always consult GOF_PATTERNS.md when designing new services, controllers, or significant features. Select patterns during the **Plan** step, not during implementation. Consult the "Usage Guidance in This Codebase" section for patterns already in use and anti-patterns to avoid.
- Always consult DOCUMENTATION.md when generating internal operator or external user facing documentation.
- Always consult MIGRATIONS.md when migrating from one stack to another such as Javascript to TypeScript, Python to .NET Core etc.
- Always consult LOGGING.md so that you add appropriate logging configuration and log statements to all generated code.
- Always consult COMMENTING.md so that you add appropriate comments to all generated code.
- Always consult PRAGMATIC_PROGRAMMER.md for pragmatic engineering principles and PRAGMATIC_PROGRAMMER.checklist.md for a quick review.
- Always consult CODE_COMPLETE.md for software construction best practices and CODE_COMPLETE.checklist.md for a quick review.
- Always consult SECURITY_GUIDELINES.md so that you are aware of how to mitigate security concerns and do not introduce inadvertent security issues.
- Always consult FRONTEND.md when frontend code changes are involved.
- Always consult DELETION.md when adding new types of resources that users will use.
- Always consult UX_UI_GUIDELINES.md when thinking about any new capability or feature.
- Always consult UI_UX_CONSISTENCY.md when thinking about and implementing UIs. 
- Always consult API_GUIDELINES.md when implementing new APIs.
- Always consult PERFORMANCE.md when implementing backends, frontends or APIs. It is important to keep performance in mind upfront.
- **(CRITICAL)** Always consult TESTING.md when writing tests. Tests are written BEFORE implementation code (TDD "Red" phase). Having maintainable and comprehensive tests is the foundation of code quality. Without tests, refactoring is unsafe.
- Always consult MIGRATIONS.md when refactoring or restructuring existing code, not just when migrating between stacks. The Golden Loop (baseline → refactor → verify) applies to all refactorings. Establish a test baseline before changing any code.
- When creating backend code, consult BACKEND.md.
- When selecting libaries for backend functionality, always consult BACKEND_LIBRARY_SELECTION.md for guidelines and DOTNETFX_SELECTION.md for pre-canned recommendations. 
- When selecting libraries for frontend functionality, always consult FRONTEND_LIBRARY_SELECTION.md for guidelines and FRONTEND_SELECTION.md for pre-canned recommendations.
- Before building new UI components, always consult the file `https://theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_INDEX.md` to see 
  if a reusable component exists. If a resuable component exists, then consult 
  `https://theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_REFERENCE.md` to look up the component and related documentation. 
  If no resuable component exists, then check `https://theme.priyavijai-kalyan2007.workers.dev/docs/MASTER_COMPONENT_INDEX.md` to see if a 
  component yet to be built will fit your needs. If so, then request that the component be built instead. 
  If you have the permissions to do so, you may file a GitHub issue to the repository `https://github.com/priyavijaikalyan2007/instructions`
  Finally, if no existing component fits the need and none of the components in the master list suffice, 
  produce a specification for the resuable UI components and then wait for the user to confirm that the 
  components are available for use before proceeding. This ensures that UI code uses cleanly built resuable 
  components with standardized repeatable patterns and not AI slop. You may also file an issue to the repository `https://github.com/priyavijaikalyan2007/instructions` asking for the new component. Include the specification in the issue.
- Always consult RESTABLE_RESOURCES.md for how to setup resource URLs to be restable and usable by humans.
- Always consult LITERATE_ERRORS.md for how to construct error messages to be usable and meaningful to users and operators.
- Always consult LLM_TECHNIQUES.md and NON_LLM_AIML_TECHNIQUES.md to determine the best approach for infusing any AI or ML feature. It's important to choose the right AI or ML technique instead of one-shotting everything with LLMs. Make sure to consult AIML_SECURITY.md *every time* to make sure AI or ML features especially those involving LLMs do not lead to system compromise or data exfiltration.
- When creating SDKs, consult SDKs.md.
- **When implementing access control, sharing, or permissions, always consult ACCESS_CONTROL.md.** This includes:
  - Defining new permissions and roles
  - Setting resource ownership
  - Adding permission checks to controllers
  - Integrating Share buttons in frontend
  - Writing authorization tests
- Always consult ADDITIONAL_INSTRUCTIONS.md which contain some refinements. 
- Always make sure that all generated code includes copyright information following the instructions in ./COPYRIGHT_HEADER.md
- Generate a concise summary of changes for each set of changes and commit the Git code. Don't push yet.

## Local Development

### Clean
```bash
./clean.sh
```

### Build
```bash
./build.sh
```

### Test
```bash
./test.sh
```

### Run
```bash
./run.sh
```

### Deploy
```bash
./redeploy.sh
```

## Local Endpoints

After `run.sh` starts, about 1 minute later, the app should be available at `http://localhost:8080`. 
The local database is PostgreSQL. User name is `postgres` and password is `postgres`. Database is `postgres`.

# Agent Knowledge Base (CRITICAL)

The directory `./agentknowledge/` contains a machine-readable knowledge graph of the codebase. See [KNOWLEDGE_ARCHITECTURE.md](./KNOWLEDGE_ARCHITECTURE.md) for the full specification.

## Session Start — Read
At the beginning of every session, read these files to orient yourself:
1. `agentknowledge/concepts.yaml` — Business concepts mapped to anchor files. Use this to locate code instead of blind searching.
2. `agentknowledge/entities.yaml` — Data models mapped to code files, database tables, and relationships.
3. `agentknowledge/decisions.yaml` — Architectural Decision Records (ADRs). Consult before proposing alternative approaches; the decision may already be recorded and reasoned.

## Session End — Update
Before your final commit in a session, update these files if your work changed the codebase meaningfully:

| Trigger | Action |
|---------|--------|
| Created a new service, controller, or shared module | Add a concept entry to `concepts.yaml` with `name`, `definition`, `anchor_file`, `related`. |
| Created or modified a data model / entity | Add or update an entry in `entities.yaml` with `name`, `table`, `file`, `description`, `related`. |
| Made an architectural decision (new library, new pattern, new infrastructure choice) | Add an ADR entry to `decisions.yaml` with `id` (next `ADR-NNN`), `title`, `date`, `status`, `context`, `files`. |
| Completed any significant task | Append a single JSON line to `history.jsonl` with `date`, `task`, `files`, `summary`. |

## Rules
- **Never delete** existing entries — only add or update.
- **Never rewrite** `history.jsonl` — it is append-only.
- Keep concept names in PascalCase and stable; other files may reference them.
- If a decision is superseded, set its `status` to `Superseded` and add the replacement ADR id.

# History and Status

Always keep all provided input from me to you, the agent, in the file CONVERSATION.md. Write the request + your output summary into the CONVERSATION.md file as well. This helps keep track of all refinements and changes over time. If this file already exists, also attempt to read it to understand everything that has been done so far. Leverage the `git log` to understand past changes and refinements. Use agentic markers in all generated files to guide yourself. This combination should give you almost all context about what was achieved.

Always keep the per-application progress and plans in an application specific file inside the `./specs/` directory. For example, as we are working on the *Diagrams* app, keep progress from CONVERSATION.md, your context, your history, the `git log`, bug fixes, refinements in the file `./specs/diagrams.status.md`. This makes it easier to resume sessions working on the app over time or for bug fixes etc. This is going to be shorter context than CONVERSATION.md which is quite large.
