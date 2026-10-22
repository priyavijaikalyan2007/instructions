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

Start with the project configuration below for business context and the work in scope.
Read [instructions/README.md](README.md) for the shared instruction library overview.
Read the consuming repository's product README when one is provided.

## Load project configuration

Read PROJECT_PROFILE.md when it exists.
Read its configured project-facts and additional-instructions files before planning or editing.
Read [AGENT_ROLES.md](AGENT_ROLES.md) and use the profile assignments for your host tool.
Use the explicit user task when no role is assigned. Roles do not grant permissions or authorize delegation.
PROJECT.md contains facts, not behavioral instructions.
Use only enabled components that the task changes. Select their targets, actual languages, platforms, and applicable shared concerns.
For a SaaS client integration, also read the SaaS composition and the configured SDK component's contract guidance.
A shared API-contract change selects affected consumers. A local UI change does not select unrelated backend implementation.
Unchecked components and examples do not enter scope merely because their files are present.
Treat missing configured files, unresolved values, or source/profile disagreements as configuration gaps.
Explicit Source state: planned permits absent literal source paths while defining instructions for new work.
Optional Source folders metadata selects directory creation after preview and apply approval.
An empty bootstrapped folder still represents planned work, not implemented source.
It does not mean that source exists or that a build passed. Resolve other gaps before dependent work.
For an older repository without a profile, infer existing scope from its README, source, manifests, and scripts.
Do not invent project facts or enable components from this instruction repository's examples.

Read [REPO.md](REPO.md#project-configuration) for profile setup and selection rules.
Read [REPO.md](REPO.md) for shared repository setup, commands, source verification, and session records.

## Select target guides

Select targets for the work that the task changes, then select the languages used in that work.
A repository can combine several targets. Its primary language or hosting platform does not select every target.
The target guides group existing instructions and link to existing topic guides.
Read the sections that apply to the changed behavior and the configured project model.

| Work in the task | Target guides | Language examples |
| --- | --- | --- |
| Backend services, APIs, backend-owned data models and persistence, containers, and service development | [BACKEND.md](backend/BACKEND.md) | C#, Java, SQL, or the service's actual language |
| Browser pages, dynamic pages, login, and web application UI | [FRONTEND.md](frontend/FRONTEND.md) | TypeScript, JavaScript, HTML, CSS, SCSS |
| SaaS flows across browser, backend, SDKs, or optional native clients | [SAAS.md](saas/SAAS.md), plus only affected target guides | The languages of the affected components |
| CLI tools, CLI plugins, and plugins for CLI tools | [TOOLS.md](tools/TOOLS.md) | Python, Go, Rust, or the tool's actual language |
| Native iOS, Android, iPadOS, ChromeOS, or macOS applications | [APPS.md](apps/APPS.md) | Swift for the existing Apple examples, or the target's actual language |
| Static websites without an application backend | [WEBSITES.md](website/WEBSITES.md) and [STATIC_ASSETS.md](static-assets/STATIC_ASSETS.md) | HTML, CSS, SCSS, JavaScript, TypeScript |
| Static assets, bundles, compilation, hosting, CDN delivery, or component-library distribution | [STATIC_ASSETS.md](static-assets/STATIC_ASSETS.md) | The affected source and build languages |
| SDKs and clients generated from an OpenAPI endpoint | [SDKs.md](sdk/SDKs.md) | Swift, TypeScript, Java, C#, Go, Python, or the generated language |
| Google Workspace or Editor add-ons | [GOOGLE_WORKSPACE.md](google-workspace/GOOGLE_WORKSPACE.md) | Apps Script/JavaScript, TypeScript, or the configured HTTP runtime language |
| Browser extensions for Chrome, Firefox, Safari, or compatible browsers | [BROWSER_EXTENSIONS.md](browser-extensions/BROWSER_EXTENSIONS.md) | TypeScript, JavaScript, HTML, CSS, and native wrapper code only when affected |
| Documentation and published project information | [DOCUMENTATION.md](DOCUMENTATION.md) | Natural language, plus changed code-example languages |

For a reusable browser component library, combine frontend and static asset guidance.
For a web application, packaging and serving may be combined or separate. The SaaS guide retains the existing combined examples.
Static hosting, including Cloudflare hosting, does not by itself select backend application guidance.
A native app and its public website select separate target guides within the same monolithic repository.
A SaaS may combine backend, browser, persistence, SDKs, docs, website, and optional native components.
A native SaaS client selects instructions/apps/APPS.md, instructions/saas/SAAS.md, instructions/sdk/SDKs.md, and its actual language for the changed integration.
Native clients use generated SDKs by default. Native presence, platforms, and SaaS-client behavior remain explicit choices.
A Python backend selects backend and Python guidance. A Go CLI selects tool and Go guidance.
Google Workspace and browser extensions are independent targets. Select their actual hosts and runtime from project facts.
An extension that consumes this repository's SaaS API also selects SaaS composition and SDK contract guidance.
A standalone extension does not automatically select a server backend, native app, or static website.
Existing native platform instructions cover Apple platforms. The SDK guide indexes existing API and language material.

## Select shared concerns

| Changed concern | Read |
| --- | --- |
| Stored data, files, transactions, schema changes, or persistence tests | [PERSISTENCE.md](PERSISTENCE.md), plus [SQL.md](sql/SQL.md) when SQL changes |
| User-facing behavior, validation, focus, state, or recovery | [UI_UX.md](UI_UX.md) |
| A particular field, component, editor, or workflow | Only the matching [UI_UX_COMPONENTS.md](UI_UX_COMPONENTS.md#select-component-profiles) profiles |
| Secrets, clipboard data, temporary storage, memory, swap, or crash dumps | [SECURITY_GUIDELINES.md](SECURITY_GUIDELINES.md#sensitive-data-lifecycle) and [SECRET_HANDLING.md](SECRET_HANDLING.md) |
| AI or ML inputs, retrieval, tools, models, or outputs | [AIML_SECURITY.md](AIML_SECURITY.md), plus general security |
| Tenant boundaries or application permissions | [SECURITY_GUIDELINES.md](SECURITY_GUIDELINES.md#tenant-isolation) and [ACCESS_CONTROL.md](ACCESS_CONTROL.md) |
| Browser keyboard bindings or shortcut tables | [KEYBOARD.md](frontend/KEYBOARD.md) |

## Select language guides

Select guides from the source files and boundaries that the task changes.
Use manifests and build scripts to confirm the language and runtime.
Code examples in this instruction repository do not select a language for the consuming project.

| Changed source or configuration | Read |
| --- | --- |
| C#, .NET, or C# in Razor views | [CSHARP.md](csharp/CSHARP.md) |
| Swift and native Apple target configuration | [SWIFT.md](swift/SWIFT.md) |
| Go source and module configuration | [GO.md](go/GO.md) |
| Rust source and Cargo configuration | [RUST.md](rust/RUST.md) |
| Java source and JVM build configuration | [JAVA.md](java/JAVA.md) |
| Python source and package configuration | [PYTHON.md](python/PYTHON.md) |
| JavaScript source and runtime configuration | [JAVASCRIPT.md](javascript/JAVASCRIPT.md) |
| Server-side Apps Script, including compiled TypeScript output | [APPS_SCRIPT.md](apps-script/APPS_SCRIPT.md), plus shared JavaScript and actual source-language rules |
| TypeScript source, declarations, and compiler configuration | [TYPESCRIPT.md](typescript/TYPESCRIPT.md) and its shared [JavaScript rules](javascript/JAVASCRIPT.md) |
| HTML markup and markup in templates or views | [HTML.md](html/HTML.md) |
| CSS stylesheets | [CSS.md](css/CSS.md) |
| SCSS source and Sass build configuration | [SCSS.md](scss/SCSS.md) and its shared [CSS rules](css/CSS.md) |
| SQL queries, schema changes, and migrations | [SQL.md](sql/SQL.md) |
| Shell scripts, Bash, and BATS tests | [SHELL.md](shell/SHELL.md) |

Read every language involved in the changed behavior, including embedded SQL, markup, or styles.
Among language guides, a C# API change may need only instructions/csharp/CSHARP.md. A Swift model change may need only instructions/swift/SWIFT.md.
A TypeScript component with HTML and SCSS changes needs the JavaScript, TypeScript, HTML, CSS, and SCSS guides.
Follow language links only when they match the selected languages. Read each selected section once per task.

Start with the selected guide's references, formatting, naming, and file organization sections.
Read its task sections as needed. Read design-pattern examples only for patterns selected during planning.
The shared topic guides remain authoritative for common rules. Their language indexes are references for the selected languages.
instructions/LANGUAGE.md governs natural-language writing and is separate from the programming-language guides.

For documentation-only changes, read instructions/LANGUAGE.md and instructions/DOCUMENTATION.md.
Read a programming-language guide when the task changes or verifies examples in that language.
Product, framework, and component reference files remain selected by the task under Development below.
In every shared guide, read framework-, platform-, and product-specific implementations only when the enabled component uses them.
A requirement inside a scoped example applies within that example. It does not select its framework for another component.
The shared rules still apply. For example, a Java backend uses Java runtime guidance and skips .NET implementations.

# Structure

The target selection above replaces a single repository-wide project label.
Use the consuming repository's README, source, manifests, and build scripts to select its configured model.
The selected target guide's stack and layout examples remain starting points for that model.
They do not authorize moving files or changing architecture.
For new components, follow [the named source convention](REPO.md#folder-and-file-structure) and the selected target guide.
Configured existing paths remain authoritative. Root test/ contains cross-component tests. Component test layouts follow their toolchain.

Prefer Allman braces throughout. Keep four-space indentation, no tabs, one type per file, and lines at most 120 characters.
Follow the syntax limits documented in `instructions/CODING_STYLE.md` rather than emitting invalid code.
Before writing code, read `instructions/CODING_STYLE.md`, `instructions/COMMENTING.md`, and `instructions/MARKERS.md` for shared construction rules.
For testing and logging work, read the shared topic guide and the matching sections in the selected language guides.

# Instructions

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
  2. **Pattern selection** - consult `instructions/GOF_PATTERNS.md` and select any GoF patterns that apply. Justify
     each choice against the Balance Checklist. If no pattern is needed, state
     "No pattern required - simple function/class suffices."
  3. **Interface design** - define the public interfaces (method signatures, DTOs) BEFORE thinking about implementation.
  4. **Layering check** - confirm that business logic is in services (not controllers),
     HTTP concerns are in controllers, cross-cutting concerns use middleware or filters.
     For native apps and tools, keep UI or CLI entry points thin and put processing logic in testable services or functions.
  5. **Review the plan** against applicable project conventions and the selected language guides.
     Use `instructions/CODING_STYLE.md` and `instructions/SECURITY_GUIDELINES.md`. Read `instructions/backend/API_GUIDELINES.md` for API work and relevant `instructions/PERFORMANCE.md` sections.
     Ensure the approach is idiomatic and low-risk.

+ **Test First (Red):** Write the tests BEFORE writing any implementation code. This is the "Red" phase of TDD.
  1. Write unit tests that describe the expected behaviour of the new code. Follow `instructions/TESTING.md` conventions
     (Arrange-Act-Assert, one assertion per test, descriptive names).
  2. For new interfaces or services, write tests against the interface contract.
  3. For bug fixes, write a test that reproduces the bug and currently fails.
  4. For refactorings, verify that existing tests pass as a baseline (per `instructions/MIGRATIONS.md` Phase 1).
     Fill coverage gaps to >=90% BEFORE refactoring.
  5. Run the tests - they MUST fail (Red). If they pass, the tests are not testing the new behaviour.

+ **Implement (Green):** Write the minimum code needed to make the failing tests pass. This is the "Green" phase of TDD.
  1. Focus on correctness, not elegance. Get the tests to pass with the simplest implementation.
  2. Apply the GoF patterns identified in the Plan step.
  3. Follow `instructions/CODING_STYLE.md` (Allman braces, 4-space indentation, one type per file, max 30-line methods, max 3 nesting levels, guard clauses).
  4. Add logging per `instructions/LOGGING.md`, comments per `instructions/COMMENTING.md`, and markers per `instructions/MARKERS.md`.
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

### Common requirements

Profile choices never remove these shared obligations. Apply each requirement to the work it describes.
The root managed block summarizes selected guides. This workflow retains the full common requirements.
Read the configured additional-instructions file before every task, including documentation-only work.

- Use instructions/LANGUAGE.md for writing style. Use only the programming-language guides selected above for code conventions.
- You must utilize the navigation markers defined in [MARKERS.md](MARKERS.md) in all generated code.
  See the Agent Knowledge Base section below for how to read and update `./agentknowledge/` every session.
  In additon, use the Git Log, CONVERSATION.md files, specifications in ./specs/ and language server plugins
  to locate code, decisions and more. Rely on grep and globbing only at the end.
- Always consult instructions/CODING_STYLE.md when writing code. This is important for maintainability.
- Always consult instructions/LOGGING.md so that you add appropriate logging configuration and log statements to all generated code.
- Always consult instructions/COMMENTING.md so that you add appropriate comments to all generated code.
- Always consult instructions/PRAGMATIC_PROGRAMMER.md for pragmatic engineering principles and instructions/PRAGMATIC_PROGRAMMER.checklist.md for a quick review.
- Always consult instructions/CODE_COMPLETE.md for software construction best practices and instructions/CODE_COMPLETE.checklist.md for a quick review.
- Always consult instructions/SECURITY_GUIDELINES.md so that you are aware of how to mitigate security concerns and do not introduce inadvertent security issues.
- **(CRITICAL)** Always consult instructions/TESTING.md when writing tests. Tests are written BEFORE implementation code (TDD "Red" phase). Having maintainable and comprehensive tests is the foundation of code quality. Without tests, refactoring is unsafe.
- Always consult instructions/LITERATE_ERRORS.md for how to construct error messages to be usable and meaningful to users
  and operators.
- Always make sure that all generated code includes copyright information following the instructions in
  instructions/COPYRIGHT_HEADER.md
- Generate a concise summary of changes for each set of changes and commit the Git code. Don't push yet.

### Requirements selected by the task

Use the enabled components and the changed behavior to select these requirements.
Read each applicable guide once. A reference to another target does not enable that target automatically.

- When dealing with secrets of any kind, especially user provided secrets, always consult instructions/SECRET_HANDLING.md
  to understand how to architect that properly.
- **(CRITICAL)** Always consult instructions/GOF_PATTERNS.md when designing new services, controllers, or significant features.
  Select patterns during the **Plan** step, not during implementation. Consult the "Usage Guidance in This Codebase"
  section for patterns already in use and anti-patterns to avoid. If the project supplies GOF_REFACTOR.md, consult its refactoring backlog.
- Always consult instructions/DOCUMENTATION.md when generating internal operator or external user facing documentation.
- Always consult instructions/MIGRATIONS.md when migrating from one stack to another such as Javascript to TypeScript, Python to .NET Core etc.
- Always consult instructions/frontend/FRONTEND.md when frontend code changes are involved.
- Always consult instructions/DELETION.md when adding new types of resources that users will use.
- For UI/UX work, read [UI_UX.md](UI_UX.md) and only the relevant component or keyboard references.
- Always consult instructions/backend/API_GUIDELINES.md when implementing new APIs.
- Always consult instructions/PERFORMANCE.md when implementing backends, frontends or APIs. It is important to keep performance in mind upfront.
- Always consult instructions/MIGRATIONS.md when refactoring or restructuring existing code, not just when migrating between stacks.
  The Golden Loop (baseline -> refactor -> verify) applies to all refactorings. Establish a test baseline
  before changing any code.
- When creating backend code, consult instructions/backend/BACKEND.md.
- For backend library selection, see [BACKEND.md](backend/BACKEND.md#backend-library-selection).
- For frontend library selection, see [FRONTEND.md](frontend/FRONTEND.md#frontend-library-selection).
- For browser component reuse, see [FRONTEND.md](frontend/FRONTEND.md#component-reuse-workflow).
- For resource URLs and deep links, consult instructions/RESTABLE_RESOURCES.md. Apply its shell messaging example only to that configured shell.
- Always consult instructions/LLM_TECHNIQUES.md and instructions/NON_LLM_AIML_TECHNIQUES.md to determine the best approach for infusing
  any AI or ML feature. It's important to choose the right AI or ML technique instead of one-shotting everything
  with LLMs. Make sure to consult instructions/AIML_SECURITY.md *every time* to make sure AI or ML features, especially
  those involving LLMs do not lead to system compromise or data exfiltration.
- When creating SDKs, consult instructions/sdk/SDKs.md.
- **For application authorization or resource sharing, consult instructions/ACCESS_CONTROL.md and the configured project model.**
  Native OS permissions and platform share sheets use instructions/apps/APPS.md. Application authorization work includes:
  - Defining new permissions and roles
  - Setting resource ownership
  - Adding permission checks to controllers
  - Integrating Share buttons in frontend
  - Writing authorization tests
- For storage changes, read [PERSISTENCE.md](PERSISTENCE.md).

# Agent Knowledge Base (CRITICAL)

The directory `./agentknowledge/` contains a machine-readable knowledge graph of the codebase.
See [KNOWLEDGE_ARCHITECTURE.md](KNOWLEDGE_ARCHITECTURE.md) for the full specification.

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
