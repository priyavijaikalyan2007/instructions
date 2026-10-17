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

## Select language guides

Select guides from the source files and boundaries that the task changes.
Use manifests and build scripts to confirm the language and runtime.
Code examples in this instruction repository do not select a language for the consuming project.

| Changed source or configuration | Read |
| --- | --- |
| C#, .NET, or C# in Razor views | [CSHARP.md](./CSHARP.md) |
| Swift and native Apple target configuration | [SWIFT.md](./SWIFT.md) |
| Go source and module configuration | [GO.md](./GO.md) |
| Rust source and Cargo configuration | [RUST.md](./RUST.md) |
| Java source and JVM build configuration | [JAVA.md](./JAVA.md) |
| Python source and package configuration | [PYTHON.md](./PYTHON.md) |
| JavaScript source and runtime configuration | [JAVASCRIPT.md](./JAVASCRIPT.md) |
| TypeScript source, declarations, and compiler configuration | [TYPESCRIPT.md](./TYPESCRIPT.md) and its shared [JavaScript rules](./JAVASCRIPT.md) |
| HTML markup and markup in templates or views | [HTML.md](./HTML.md) |
| CSS stylesheets | [CSS.md](./CSS.md) |
| SCSS source and Sass build configuration | [SCSS.md](./SCSS.md) and its shared [CSS rules](./CSS.md) |
| SQL queries, schema changes, and migrations | [SQL.md](./SQL.md) |
| Shell scripts, Bash, and BATS tests | [SHELL.md](./SHELL.md) |

Read every language involved in the changed behavior, including embedded SQL, markup, or styles.
For example, a C# API change may need only CSHARP.md. A Swift model change may need only SWIFT.md.
A TypeScript component with HTML and SCSS changes needs the JavaScript, TypeScript, HTML, CSS, and SCSS guides.
Follow language links only when they match the selected languages. Read each selected section once per task.

Start with the selected guide's references, formatting, naming, and file organization sections.
Read its task sections as needed. Read design-pattern examples only for patterns selected during planning.
The shared topic guides remain authoritative for common rules. Their language indexes are references for the selected languages.
LANGUAGE.md governs natural-language writing and is separate from the programming-language guides.

For documentation-only changes, read LANGUAGE.md and DOCUMENTATION.md.
Read a programming-language guide when the task changes or verifies examples in that language.
Product, framework, and component reference files remain selected by the task under Development below.

# Structure

Choose the project model from the consuming repository's README, source, manifests, and build scripts.
A repository may contain several models, such as native apps plus their public website.
The choices below guide work within existing projects. They do not authorize moving files or changing architecture.

| Project model | Typical architecture | Main responsibilities |
| --- | --- | --- |
| Enterprise SaaS application | .NET or Java backend, browser frontend, persistent storage, and background workers. | Tenant-aware APIs, frontend routes and pages, authorization, data ownership, and operations. |
| Enterprise identity service | Java extensions hosted by an identity server, browser themes, and a configured runtime or container. | Sign-in flows, identity federation, tokens, extension compatibility, and identity-service operations. |
| Native Apple applications | Swift targets for macOS, iOS, and iPadOS, with shared logic and platform-specific views and adapters. | Native lifecycle, local persistence, permissions, accessibility, platform layouts, signing, and releases. |
| Reusable component library | TypeScript components, CSS/SCSS, licensed assets, build tools, and generated distribution bundles. | Public contracts, reusable controls, state capture and restoration, cleanup, demos, documentation, and consumer compatibility. |
| Local tools | Go, Rust, or Python executables or packages, with thin command entry points and testable processing code. | Arguments, local files, cancellation, diagnostics, exit status, and release binaries or packages. |
| Website | Static or server-rendered HTML and CSS, with optional TypeScript modules and backend services. | Content, navigation, assets, forms, accessibility, and static or server delivery. |

These models are starting points. Select versions, commands, APIs, and paths from the consuming repository's configuration.
Use the stack and layout guidance below without depending on another repository's files.
Prefer Allman braces throughout. Keep four-space indentation, no tabs, one type per file, and lines at most 120 characters.
Follow the syntax limits documented in `CODING_STYLE.md` rather than emitting invalid code.
Before writing code, read `CODING_STYLE.md`, `COMMENTING.md`, and `MARKERS.md` for shared construction rules.
For testing and logging work, read the shared topic guide and the matching sections in the selected language guides.

# Instructions

## Stack

### Enterprise SaaS application

- Use the project's configured backend, such as ASP.NET Core 10.0+ or Java. Match its runtime and deployment mode.
- Serve frontend routes and APIs through the application, including pages when needed.
- Truly static browser assets may come from a content delivery network (CDN).
- For air-gapped environments, package required assets locally and serve them without external network dependencies.
- Use TypeScript for non-trivial browser scripting, with HTML, CSS/SCSS, and the declared component library.
- Keep the configured Vite source/output mapping. Do not edit compiled JavaScript as a substitute for its TypeScript source.
- Use the configured PostgreSQL and data-access versions. Keep executable SQL migration scripts in the project's migration directory.
- Read deployment configuration for containers, Cloud Run, background roles, and resource limits. Do not assume a fixed image size.

### Enterprise identity service or Java web application

- Use Java and the configured JDK for identity-server extensions. Keycloak projects may include providers, browser themes, and a container deployment.
- Match extension APIs to the host runtime and distinguish host-provided dependencies from bundled dependencies.
- Use the Maven or Gradle wrapper and the repository's configured toolchain.
- A general Java web application uses its declared web framework. Keycloak is an identity-service choice, not a universal Java backend.
- Use TypeScript for non-trivial browser logic. Preserve the host's template, security-header, and asset-delivery contracts.

### Native macOS, iOS, and iPadOS applications

- Use Swift and the project's SwiftUI, AppKit, or UIKit targets. Share platform-independent logic without duplicating it across targets.
- Read the Xcode project and build scripts for deployment targets, SDKs, architectures, schemes, signing, and capabilities.
- Use native persistence and state restoration. A local app does not require a server, database, login, or analytics by default.
- Test platform permissions, document access, app lifecycle, accessibility, and platform-specific layouts where affected.
- Treat building, signing, archiving, uploading, submitting for review, and releasing as separate operations.
- Follow the repository's release scripts. Keep private signing material and service credentials out of source and app bundles.

### Reusable component library

- Use the library's declared stack, such as vanilla TypeScript, HTML, CSS/SCSS, Bootstrap, and Node.js build tools.
- Keep source components separate from generated bundles, generated documentation, and distribution output.
- Document each component's factory, options, events, public types, state capture/restore, dependencies, and cleanup contract.
- Use unit, browser, accessibility, visual, and consumer-artifact checks as appropriate.
- The consuming application owns authentication, persistence, and the host logging pipeline.

### Local Go, Rust, and Python tools

- Go uses its configured `go.mod` toolchain and standard module layout. Rust uses Cargo and the declared Rust edition/toolchain.
- Python uses the project's interpreter, `pyproject.toml`, environment, and dependency lock policy.
- Keep argument parsing and process setup separate from testable processing logic.
- Keep machine-readable output on stdout and diagnostics on stderr. Document exit status, cancellation, and partial-output behavior.
- Bound memory, concurrency, and file operations. Preserve user data when processing fails.
- Add network services, databases, or native UI dependencies only when the tool's requirements need them.

### Websites and browser scripting

- A static website may use HTML and CSS with no backend or JavaScript.
- Use the project's asset and delivery pipeline. Apply API guidance only when the website actually calls or serves APIs.
- Use TypeScript for non-trivial browser scripting. Move inline JavaScript beyond ten lines into a TypeScript module.
- Apply browser component rules to browser UIs. Native apps use platform controls and their declared design conventions.

## Folder & File Structure

Preserve the consuming repository's established layout. Use the following examples when a new project needs a layout.
Keep specifications in `specs/`, operator guides in `playbooks/`, and user/integrator documentation in `docs/` where those conventions apply.
Keep one type per source file, including short structs. See `CODING_STYLE.md` for nested-type and extension exceptions.

### Enterprise SaaS application

```text
api/                   .NET backend, domain services, HTTP boundaries, and persistence
frontend/              Browser HTML, CSS, and source assets
typescript/            TypeScript source compiled into the browser output
unittests/             Backend unit tests
integrationtests/      Real service and database integration tests
playwrighttests/       Browser workflows and accessibility checks
sql/migrations/        Ordered, executable database migrations
specs/                 Product requirements, designs, and progress
playbooks/             Operator and development procedures
docs/                  User and integrator documentation
```

### Enterprise identity service or Java backend

```text
src/providers/         Java host extensions, with their own Maven/Gradle source and test roots
src/themes/            Host-rendered templates, styles, and browser assets
src/main/java/         Application Java code when this is a standard Java backend
src/main/resources/    Application configuration and packaged resources
src/test/java/         Unit and integration tests under the configured runner
sql/                   Application-owned database scripts, when applicable
Dockerfile             Container build, when the deployment uses containers
target/ or build/      Generated output, never the source to edit
```

The identity extension roots and standard Java roots are alternatives, not duplicate homes for the same code.

### Native Apple applications

For a repository with several native applications, use `src/<app-name>/` when a new layout is needed.
Give each application its own build, tests, and documentation.

```text
src/<app-name>/
    Shared/            Swift logic and resources shared between platform targets
    <AppName>/         macOS application entry point, views, and platform adapters
    <AppName>Mobile/   iOS/iPadOS entry point, views, and platform adapters
    <AppName>Tests/    Unit and integration tests
    <AppName>.xcodeproj/  Targets, schemes, build settings, and project membership
    Testing/           Manual regression plans and nonprivate sample data
    AppStore/          Product metadata, review notes, and media plans
    scripts/           App-specific build, archive, signing, and upload procedures
    build/             Generated artifacts, excluded from source control
src/web/               Public website, when this repository also owns one
```

For a Swift package, use `Sources/<Target>/` and `Tests/<Target>Tests/` with `Package.swift` instead of inventing an Xcode layout.
Adding a source file also requires checking target membership and resource packaging.

### Reusable component library

```text
components/<name>/     Component TypeScript, styles, tests, and usage documentation
scss/                  Theme variables, shared styles, and component imports
assets/                Source icons, fonts, and other licensed assets
demo/                  Discoverable component examples and integration scenarios
docs/                  Consumer contracts, API references, and integration guides
scripts/               Build, bundle, validation, and publication tools
tests/                 Browser, distribution, and cross-component tests
dist/                  Generated bundles, assets, demos, and documentation
```

Keep source and generated documents distinguishable. Register new demos and guides in the library's discovery and publication pipeline.

### Local tools

| Purpose | Go | Rust | Python |
| --- | --- | --- | --- |
| Manifest | `go.mod`, `go.sum` | `Cargo.toml`, configured `Cargo.lock` policy | `pyproject.toml`, project lockfile |
| Entry point | `cmd/<tool>/main.go` | `src/main.rs` | `src/<package>/__main__.py` |
| Processing code | `internal/<package>/` | `src/<module>/`, exposed through `src/lib.rs` | `src/<package>/` |
| Public reusable API | Dedicated package only when needed | Deliberate library exports in `src/lib.rs` | Deliberate package exports |
| Tests | Beside code as `*_test.go` | Module tests and `tests/` integration tests | `tests/` or the established colocated convention |
| Build output | Ignored `bin/` or `build/` | Ignored `target/` | Ignored `build/`, `dist/`, and environment directories |

Keep Go type files in the appropriate existing package. Register Rust type files in their parent module and set visibility deliberately.
Do not create a package or crate for every type merely to satisfy the file rule.

## Operating Style

Use the **V-V-P-T-I-R-V-C** loop (Plan → Test → Implement → Refactor → Verify) for your core workflow. 
This is a strict **Test-Driven Development** workflow. For all software engineering tasks, you MUST follow 
this sequence. **Never write implementation code before writing a failing test.**

+ **Validate (Request):** Analyse the prompt for ambiguity. Restate the core requirement and constraints 
  to ensure alignment before acting.
  
+ **Verify (State):** Inspect the current codebase context. Read relevant files to confirm the environment 
  is clean and assumptions about the existing code are correct. Consult `agentknowledge/concepts.yaml` 
  to locate related code.
  
+ **Plan (Design):** Draft a concrete, step-by-step technical plan. This step is where architecture happens - not 
  during implementation. The plan MUST include:
  1. **Files to modify or create** - list every file.
  2. **Pattern selection** - consult `GOF_PATTERNS.md` and select any GoF patterns that apply. Justify 
     each choice against the Balance Checklist. If no pattern is needed, state 
     "No pattern required - simple function/class suffices."
  3. **Interface design** - define the public interfaces (method signatures, DTOs) BEFORE thinking about implementation.
  4. **Layering check** - confirm that business logic is in services (not controllers), 
     HTTP concerns are in controllers, cross-cutting concerns use middleware or filters.
     For native apps and tools, keep UI or CLI entry points thin and put processing logic in testable services or functions.
  5. **Review the plan** against applicable project conventions and the selected language guides.
     Use `CODING_STYLE.md` and `SECURITY_GUIDELINES.md`. Read `API_GUIDELINES.md` for API work and relevant `PERFORMANCE.md` sections.
     Ensure the approach is idiomatic and low-risk.
     
+ **Test First (Red):** Write the tests BEFORE writing any implementation code. This is the "Red" phase of TDD.
  1. Write unit tests that describe the expected behaviour of the new code. Follow `TESTING.md` conventions 
     (Arrange-Act-Assert, one assertion per test, descriptive names).
  2. For new interfaces or services, write tests against the interface contract.
  3. For bug fixes, write a test that reproduces the bug and currently fails.
  4. For refactorings, verify that existing tests pass as a baseline (per `MIGRATIONS.md` Phase 1). 
     Fill coverage gaps to >=90% BEFORE refactoring.
  5. Run the tests - they MUST fail (Red). If they pass, the tests are not testing the new behaviour.

+ **Implement (Green):** Write the minimum code needed to make the failing tests pass. This is the "Green" phase of TDD.
  1. Focus on correctness, not elegance. Get the tests to pass with the simplest implementation.
  2. Apply the GoF patterns identified in the Plan step.
  3. Follow `CODING_STYLE.md` (Allman braces, 4-space indentation, one type per file, max 30-line methods, max 3 nesting levels, guard clauses).
  4. Add logging per `LOGGING.md`, comments per `COMMENTING.md`, and markers per `MARKERS.md`.
     Use the corresponding language-guide sections for syntax, APIs, and examples.
  5. Run the tests - they MUST pass (Green). If they fail, fix the implementation, NOT the tests.

+ **Refactor (Clean):** Now that tests pass, improve the code structure without changing behaviour. 
  This is the "Refactor" phase of TDD. Apply Martin Fowler refactoring techniques:
  1. **Extract Method** - break methods exceeding 30 lines into smaller, named methods.
  2. **Extract Class** - split classes exceeding 500 lines or having multiple responsibilities.
  3. **Replace Conditional with Polymorphism** - replace switch/if-else chains dispatching to type-specific 
     code with Strategy or polymorphic calls.
  4. **Replace Magic String with Symbolic Constant** - replace hardcoded strings in conditionals with enums or 
     constants.
  5. **Move Method** - move logic to the class where it belongs (e.g., business logic out of controllers).
  6. **Encapsulate Collection** - replace `Dictionary<string, object>` with strongly-typed classes.
  7. Run the tests after EACH refactoring step. If tests fail, revert the last refactoring.

+ **Verify (Full):** Execute the new tests AND all relevant regression tests. Ensure everything passes locally. 
  Run the project's full validation command. Use `./test.sh` when that script exists.

+ **Commit:** Stage the verified changes and create a commit with a concise, conventional message 
  (e.g., `fix: ...`, `feat: ...`, `refactor: ...`). One logical change per commit.

## (CRITICAL) Thinking
I urge you to think along the lines of Steve Jobs, Douglas Normal, Jonathan Ivy and others. The details 
are important in making sure the software and documentation we provide our users offer an amazing, 
consistent, thoughtful and complete end to end experience.

## Development (CRITICAL)
- Use LANGUAGE.md for writing style. Use only the programming-language guides selected above for code conventions.
- You must utilize the navigation markers defined in [MARKERS.md](./MARKERS.md) in all generated code. 
  See the Agent Knowledge Base section below for how to read and update `./agentknowledge/` every session. 
  In additon, use the Git Log, CONVERSATION.md files, specifications in ./specs/ and language server plugins 
  to locate code, decisions and more. Rely on grep and globbing only at the end.
- When dealing with secrets of any kind, especially user provided secrets, always consult SECRET_HANDLING.md 
  to understand how to architect that properly.
- Always consult CODING_STYLE.md when writing code. This is important for maintainability.
- **(CRITICAL)** Always consult GOF_PATTERNS.md when designing new services, controllers, or significant features. 
  Select patterns during the **Plan** step, not during implementation. Consult the "Usage Guidance in This Codebase" 
  section for patterns already in use and anti-patterns to avoid. Consult GOF_REFACTOR.md for the active 
  refactoring backlog and to understand the target architecture.
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
- Always consult MIGRATIONS.md when refactoring or restructuring existing code, not just when migrating between stacks. 
  The Golden Loop (baseline -> refactor -> verify) applies to all refactorings. Establish a test baseline 
  before changing any code.
- When creating backend code, consult BACKEND.md.
- When selecting libaries for backend functionality, always consult BACKEND_LIBRARY_SELECTION.md for guidelines 
  and, for .NET projects, DOTNETFX_SELECTION.md for pre-canned recommendations.
- When selecting libraries for frontend functionality, always consult FRONTEND_LIBRARY_SELECTION.md for guidelines 
  and FRONTEND_SELECTION.md for pre-canned recommendations.
- Before building new browser UI components, always consult the file
  `https://theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_INDEX.md` to see 
  if a reusable component exists. If a resuable component exists, then consult 
  `https://theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_REFERENCE.md` 
  to look up the component and related documentation. 
  If no resuable component exists, then check 
  `https://theme.priyavijai-kalyan2007.workers.dev/docs/MASTER_COMPONENT_INDEX.md` to see if a 
  component yet to be built will fit your needs. If so, then request that the component be built instead. 
  If you have the permissions to do so, you may file a GitHub issue to the repository 
  `https://github.com/priyavijaikalyan2007/b2btheme`
  Finally, if no existing component fits the need and none of the components in the master list suffice, 
  produce a specification for the resuable UI components and then wait for the user to confirm that the 
  components are available for use before proceeding. This ensures that UI code uses cleanly built resuable 
  components with standardized repeatable patterns and not AI slop. 
  You may also file an issue to the repository `https://github.com/priyavijaikalyan2007/b2btheme` asking for 
  the new component. Include the specification in the issue.
- Always consult RESTABLE_RESOURCES.md for how to setup resource URLs to be restable and usable by humans.
- Always consult LITERATE_ERRORS.md for how to construct error messages to be usable and meaningful to users
  and operators.
- Always consult LLM_TECHNIQUES.md and NON_LLM_AIML_TECHNIQUES.md to determine the best approach for infusing 
  any AI or ML feature. It's important to choose the right AI or ML technique instead of one-shotting everything 
  with LLMs. Make sure to consult AIML_SECURITY.md *every time* to make sure AI or ML features, especially 
  those involving LLMs do not lead to system compromise or data exfiltration.
- When creating SDKs, consult SDKs.md.
- **When implementing access control, sharing, or permissions, always consult ACCESS_CONTROL.md.** This includes:
  - Defining new permissions and roles
  - Setting resource ownership
  - Adding permission checks to controllers
  - Integrating Share buttons in frontend
  - Writing authorization tests
- Always consult ADDITIONAL_INSTRUCTIONS.md which contain some refinements. 
- Always make sure that all generated code includes copyright information following the instructions in 
  COPYRIGHT_HEADER.md
- Generate a concise summary of changes for each set of changes and commit the Git code. Don't push yet.

## Local Development

For native apps, use the app-specific build modes and Xcode schemes documented by the repository.
For component libraries, use the declared package scripts. Go, Rust, and Python tools use their documented module/package commands.
A build or test command does not authorize deployment, signing-key export, app-store submission, or release.

Use the following commands when the consuming repository provides these scripts.
Otherwise, use its documented build and test commands for the configured toolchain.

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

Read the consuming repository's README, launch configuration, and scripts for ports, health checks, and local dependencies.
The SaaS, identity service, component demo, and website may each use different endpoints.
Native apps and local tools need no listening port unless their design explicitly includes a service.
Use configured local credentials. Never copy example credentials into a deployed environment.

# Agent Knowledge Base (CRITICAL)

The directory `./agentknowledge/` contains a machine-readable knowledge graph of the codebase. 
See [KNOWLEDGE_ARCHITECTURE.md](./KNOWLEDGE_ARCHITECTURE.md) for the full specification.

## Session Start - Read
At the beginning of every session, read these files to orient yourself:
1. `agentknowledge/concepts.yaml` - Business concepts mapped to anchor files. 
   Use this to locate code instead of blind searching.
2. `agentknowledge/entities.yaml` - Data models mapped to code files, database tables, and relationships.
3. `agentknowledge/decisions.yaml` - Architectural Decision Records (ADRs). 
   Consult before proposing alternative approaches; the decision may already be recorded and reasoned.

## Session End - Update
Before your final commit in a session, update these files if your work changed the codebase meaningfully:

| Trigger | Action |
|---------|--------|
| Created a new service, controller, or shared module | Add a concept entry to `concepts.yaml` with `name`, `definition`, `anchor_file`, `related`. |
| Created or modified a data model / entity | Add or update an entry in `entities.yaml` with `name`, `table`, `file`, `description`, `related`. |
| Made an architectural decision (new library, new pattern, new infrastructure choice) | Add an ADR entry to `decisions.yaml` with `id` (next `ADR-NNN`), `title`, `date`, `status`, `context`, `files`. |
| Completed any significant task | Append a single JSON line to `history.jsonl` with `date`, `task`, `files`, `summary`. |
| Made any user-visible change (feature, fix, refactor) | Add an entry to `CHANGELOG.md` under the current date with the appropriate category (Added/Changed/Fixed/Removed). Keep entries concise — one line per change. |

## Rules
- **Never delete** existing entries — only add or update.
- **Never rewrite** `history.jsonl` — it is append-only.
- Keep concept names in PascalCase and stable; other files may reference them.
- If a decision is superseded, set its `status` to `Superseded` and add the replacement ADR id.

# History and Status

Always keep all provided input from me to you, the agent, in the file CONVERSATION.md. 
Write the request + your output summary into the CONVERSATION.md file as well. 
This helps keep track of all refinements and changes over time. If this file already exists, 
also attempt to read it to understand everything that has been done so far. 
Leverage the `git log` to understand past changes and refinements. 
Use agentic markers in all generated files to guide yourself. 
This combination should give you almost all context about what was achieved.

Always keep the per-application progress and plans in an application specific file inside the `./specs/` directory.
For example, as we are working on the *Diagrams* app, keep progress from CONVERSATION.md, 
your context, your history, the `git log`, bug fixes, refinements in the file `./specs/diagrams.status.md`.
This makes it easier to resume sessions working on the app over time or for bug fixes etc. 
This is going to be shorter context than CONVERSATION.md which is quite large.
