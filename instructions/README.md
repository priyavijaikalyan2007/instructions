<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 9a3b3546-8a9c-4f10-93b2-9c472094bc04
Created: 2026
-->

<!-- AGENT: Readme file describing this repository. -->

This is the shared instruction library overview. The four root agent entry files route to guides under instructions/.
Project configuration and local refinements live under instructions/project/ and remain project-owned during generic instruction updates.
Instruction-maintenance plans, audits, and examples live under instructions/maintenance/.
The consuming repository's specs/ directory is reserved for its actual product and repository specifications.

This repository contains instructions for coding agents, primarily Claude and Gemini. Each agent is asked to perform a different role.

The CLAUDE.md and GEMINI.md file reference AGENTS.md and then specify the role that the agent should play. AGENTS.md sets the main the context and the agent specific instructions set the roles.

Instead of using a monolithic, single instruction file, the AGENTS.md file references multiple individual files for specific instructions. It also tells the agent how to clean, build, test and run the code. 

These instructions cover Swift apps for macOS and iOS, Go and Rust tools, Java and .NET 10.0+ applications, and TypeScript/JavaScript/HTML projects.
Existing Python, SQL, CSS, and SCSS guidance also applies where those languages are used.
Read [REPO.md](REPO.md) for shared repository operations.
Select [PERSISTENCE.md](PERSISTENCE.md) for stored data and [UI_UX.md](UI_UX.md) for user-facing behavior.
Load only relevant [component profiles](UI_UX_COMPONENTS.md#select-component-profiles) and [keyboard details](KEYBOARD.md).

Some sections describe a .NET SaaS example. Apply those sections only when they match the changed target and project model.
Keep project-specific architecture, toolchain versions, and commands consistent with that repository's README and build configuration.

## Project configuration

[AGENTS.md](AGENTS.md#load-project-configuration) reads the active instructions/project/PROJECT_PROFILE.md before selecting guides.
The profile identifies project facts and local refinements, then selects enabled components and their source languages.
instructions/project/PROJECT.md contains facts only. instructions/project/ADDITIONAL.md contains project-specific instructions and emerging lessons.

Use the [profile template](PROJECT_PROFILE_TEMPLATE.md), [facts template](PROJECT_TEMPLATE.md), and [refinement template](ADDITIONAL_TEMPLATE.md).
Follow [manual setup](REPO.md#manual-setup) for a new project or edit an existing profile in place.
This repository's active profile describes the instruction library itself. Application examples do not enable application components here.
Generic instruction updates preserve project-owned profiles, facts, and refinements.

## Selective target reading

Start at [AGENTS.md](AGENTS.md#select-target-guides). Select targets for the changed work, then select its languages.
Targets describe the work. Languages describe the source. A repository can combine several targets and languages.
The target guides contain existing instructions and links to existing topic guides.

| Target | Guide | Existing material grouped here |
| --- | --- | --- |
| Backend | [BACKEND.md](BACKEND.md) | APIs, runtime, containers, and backend service boundaries |
| Frontend | [FRONTEND.md](FRONTEND.md) | Browser pages, dynamic UI, login, components, and browser tests |
| SaaS or web application | [SAAS.md](SAAS.md) | Backend, browser, generated SDK, and optional native composition, with cross-layer contracts |
| Tools | [TOOLS.md](TOOLS.md) | CLI tools and plugins, module layouts, local commands, stdout, and stderr |
| Native apps | [APPS.md](APPS.md) | Existing Apple platform, lifecycle, layout, performance, testing, and credential guidance |
| Static websites | [WEBSITES.md](WEBSITES.md) | Websites without an application backend and relevant browser references |
| Static assets | [STATIC_ASSETS.md](STATIC_ASSETS.md) | Compilation, bundles, component-library distribution, CDN delivery, and static hosting |
| SDKs | [SDKs.md](SDKs.md) | Index to existing OpenAPI contracts and language conventions |

A web application can combine C#/Java backend guidance and TypeScript/HTML frontend guidance.
A change to one side selects that side. A flow across both sides selects both.
The existing combined deployment examples remain available when packaging and serving share one application.
A component library combines frontend and static assets. A native app can share a repository with a separate static website.
The native material covers Apple platforms. This extraction adds no Android, ChromeOS, SDK generator, Kubernetes, or DNS procedures.

## Selective language reading

Start at [AGENTS.md](AGENTS.md#select-language-guides) and select guides for the files and boundaries the task changes.
Language guides live under instructions/. Each guide contains conventions and task examples for its language.
Common rules remain in the existing topic files, including style, comments, markers, testing, logging, performance, and patterns.
Read applicable topic sections together with the selected language guide. Follow other language links only when the task needs them.

| Language | Guide |
| --- | --- |
| C# | [CSHARP.md](CSHARP.md) |
| Swift | [SWIFT.md](SWIFT.md) |
| Go | [GO.md](GO.md) |
| Rust | [RUST.md](RUST.md) |
| Java | [JAVA.md](JAVA.md) |
| Python | [PYTHON.md](PYTHON.md) |
| JavaScript | [JAVASCRIPT.md](JAVASCRIPT.md) |
| TypeScript | [TYPESCRIPT.md](TYPESCRIPT.md), plus shared JavaScript rules |
| HTML | [HTML.md](HTML.md) |
| CSS | [CSS.md](CSS.md) |
| SCSS | [SCSS.md](SCSS.md), plus shared CSS rules |
| SQL | [SQL.md](SQL.md) |
| Shell | [SHELL.md](SHELL.md) |

For example, a Swift-only model change does not require C#, Java, or Rust instructions.
The file [LANGUAGE.md](LANGUAGE.md) continues to define natural-language writing style.
Shared guides hold common rules. Target and language guides select details for the changed work.

These instructrions are live. They are updated as and when new behaviors are encountered and need guidance. 

The instructions in this repository are *horizontal* in nature. That is, they are about how to write reasonably good code in a clean, structured manner. These instructions should be combined with other instructions for architecture, code structure, do's and don'ts to get output that works.

These instructions are battle tested in my private side projects. I have found that the coding agents that I use do produce reasonably clean, well structured code. Lessons from specific problems are folded into the guide that owns the subject.
Shared workflow belongs in instructions/REPO.md, storage in instructions/PERSISTENCE.md, and interaction behavior in instructions/UI_UX.md.


## Scenario reading trees

Use the common baseline with the tree for the work in scope.
Paths are relative to the consuming repository root. Bracketed conditions select a file only when that condition applies.
These trees show reading scope, not a required application directory layout.
Read relevant sections and examples, rather than every section in each linked guide.
An agent starts with its own entry file and AGENTS.md. It does not need every agent-specific entry file.

### Common baseline

```text
.
├── AGENTS.md
├── CLAUDE.md / CODEX.md / GEMINI.md       [the active agent's entry]
└── instructions/
    ├── project/
    │   ├── PROJECT_PROFILE.md            Enabled components and source paths
    │   ├── PROJECT.md                    Project facts
    │   ├── ADDITIONAL.md                 Local instructions and emerging lessons
    │   └── CONVERSATION.md               Prior context and session records
    ├── AGENTS.md                         Shared workflow and guide selection
    ├── REPO.md                           Setup, commands, and scope selection
    ├── LANGUAGE.md
    ├── CODING_STYLE.md
    ├── COMMENTING.md
    ├── MARKERS.md
    ├── TESTING.md
    ├── LOGGING.md
    ├── SECURITY_GUIDELINES.md
    ├── PERFORMANCE.md                    Relevant workload sections
    ├── LITERATE_ERRORS.md
    ├── COPYRIGHT_HEADER.md
    ├── CODE_COMPLETE.md
    ├── CODE_COMPLETE.checklist.md
    ├── PRAGMATIC_PROGRAMMER.md
    ├── PRAGMATIC_PROGRAMMER.checklist.md
    ├── GOF_PATTERNS.md                    [applicable design work]
    ├── MIGRATIONS.md                      [refactoring or migration]
    └── DOCUMENTATION.md                   [documentation or public contracts]
```

Read existing project knowledge records and relevant product specifications when the task needs them.
Actual product specifications remain in specs/. Instruction-maintenance records remain in instructions/maintenance/.
For documentation-only work, use the documented narrower reading path in AGENTS.md.

### Native standalone app

```text
instructions/
├── APPS.md
├── SWIFT.md                              [Swift Apple targets]
├── UI_UX.md                              [user-facing behavior]
├── UI_UX_COMPONENTS.md                   [only matching control profiles]
├── PERSISTENCE.md                        [stored files, data, or state]
├── SQL.md                                [actual SQL changes]
├── SECRET_HANDLING.md                    [credentials or tokens]
└── SHELL.md                              [changed shell scripts]
```

Use native controls, state restoration, accessibility, and test tools.
A standalone app does not select SaaS, backend, generated SDK, browser, or server authentication guidance by default.
Select the actual source language for other platforms. Missing platform-specific coverage remains an explicit gap.

### Native app for SaaS

```text
instructions/
├── APPS.md
├── SWIFT.md                              [Swift Apple targets]
├── SAAS.md                               Surface composition and client boundary
├── SDKs.md                               Generated SDK integration
├── API_GUIDELINES.md                     API contract used by the client
├── UI_UX.md
├── UI_UX_COMPONENTS.md                   [only matching control profiles]
├── SECRET_HANDLING.md                    Sessions and native credential storage
├── PERSISTENCE.md                        [local saved data or synchronization]
├── ACCESS_CONTROL.md                    [application authorization changes]
├── RESTABLE_RESOURCES.md                 [resource URLs or deep links]
└── SHELL.md                              [changed shell scripts]
```

The generated SDK is the normal client boundary. Native dialogs use the platform equivalent of literate error content.
A native-only task does not select server implementation merely because the server shares this repository.
A shared contract change adds affected backend and browser components from their trees.
Knobby authorization and browser-shell examples apply only when selected in the profile.

### SaaS with frontend

```text
instructions/
├── SAAS.md
├── BACKEND.md
├── JAVA.md                               [Java backend]
├── CSHARP.md                             [C# backend]
├── API_GUIDELINES.md
├── FRONTEND.md
├── TYPESCRIPT.md                         [TypeScript source]
├── JAVASCRIPT.md                         Shared browser language rules
├── HTML.md
├── CSS.md
├── SCSS.md                               [SCSS source]
├── STATIC_ASSETS.md                      Bundles and delivery
├── UI_UX.md
├── UI_UX_COMPONENTS.md                   [only matching control profiles]
├── KEYBOARD.md                           [browser keyboard behavior]
├── FRONTEND_LOGGING.md                   [configured browser logging]
├── SDKs.md                               [generated client integration]
├── PERSISTENCE.md                        [stored data and transactions]
├── SQL.md                                [SQL source or schema]
├── SECRET_HANDLING.md                    [server secrets or client tokens]
├── ACCESS_CONTROL.md                    [application authorization changes]
├── DELETION.md                           [resource deletion or retention]
├── RESTABLE_RESOURCES.md                 [resource URLs]
├── BACKEND_LIBRARY_SELECTION.md          [backend dependency selection]
├── FRONTEND_LIBRARY_SELECTION.md         [browser dependency selection]
├── FRONTEND_SELECTION.md                 [configured vanilla/Bootstrap stack]
└── ERROR_DIALOG_COMPONENT.md             [browser commands without an error surface]
```

Select the backend's actual language. Java does not select .NET implementation rules or DOTNETFX_SELECTION.md.
Use actual manifests, Dockerfile, and build scripts for container packaging facts. A container does not select a hosting provider.
Add the native SaaS tree only when an enabled native component is affected.
Add the static website tree only when the task changes that separate surface.

### Static website

```text
instructions/
├── WEBSITES.md
├── STATIC_ASSETS.md
├── FRONTEND.md                           Applicable browser standards and accessibility
├── HTML.md
├── CSS.md
├── SCSS.md                               [SCSS source]
├── JAVASCRIPT.md                         [browser scripts]
├── TYPESCRIPT.md                         [TypeScript source]
├── UI_UX.md                              [navigation and user-facing behavior]
├── UI_UX_COMPONENTS.md                   [interactive controls]
├── KEYBOARD.md                           [browser keyboard interactions]
└── FRONTEND_LOGGING.md                   [configured browser component logging]
```

A static website does not select backend, database, SaaS, or native-app implementation by default.
Read API guidance only when the website actually integrates an API.
Use the configured static delivery pipeline rather than assuming the example theme-library hosting model.

### CLI tool

```text
instructions/
├── TOOLS.md
├── PYTHON.md                             [Python source]
├── GO.md                                 [Go source]
├── RUST.md                               [Rust source]
├── SHELL.md                              [shell entry points or scripts]
├── PERSISTENCE.md                        [stored files, state, or data]
├── SQL.md                                [actual SQL source]
├── SECRET_HANDLING.md                    [credentials or secret providers]
├── SDKs.md                               [generated service-client integration]
└── API_GUIDELINES.md                     [service contracts changed or consumed]
```

Select the actual tool language. Other languages remain possible when the tool uses them.
Browser and native UI guides do not enter scope for ordinary CLI processing.
Use TOOLS.md for stdout, stderr, exit status, cancellation, and local data protection.

### Author review

Check the active profile choices before tracing a tree.
For each changed behavior, follow the applicable leaves and their linked sections.
Check that conditional examples match the project's actual language, platform, and configured architecture.
Record project-local lessons in instructions/project/ADDITIONAL.md and propose reusable refinements for the owning shared guide.

## Agent Knowledge Base

The `agentknowledge/` directory contains a machine-readable knowledge graph that agents use to orient themselves. See [KNOWLEDGE_ARCHITECTURE.md](KNOWLEDGE_ARCHITECTURE.md) for the full specification.

### Bootstrapping

On first use, the directory is empty (or contains only example files like `lcv_constraints.yaml`). Agents are expected to populate these files as they work:

| File | Purpose | Format |
|------|---------|--------|
| `concepts.yaml` | Maps business terms to anchor code locations | YAML list of `{name, definition, anchor_file, related}` |
| `entities.yaml` | Maps data models to code files and database tables | YAML list of `{name, table, file, description, related}` |
| `decisions.yaml` | Architectural Decision Records (ADRs) | YAML list of `{id, title, date, status, context, files}` |
| `history.jsonl` | Append-only log of agent tasks and changes | One JSON object per line: `{date, task, files, summary}` |
| `user_profile.yaml` | Per-user agent preferences (gitignored if personal) | YAML key-value pairs |

### Agent Workflow

1. **Session Start** — Read all files in `agentknowledge/` to orient. Use `concepts.yaml` to locate code instead of blind searching. Check `decisions.yaml` before proposing alternative approaches.
2. **During Work** — Consult the knowledge base before asking "Where is X?"
3. **Session End** — Update files if your work changed the codebase meaningfully:
   - Created a new service/controller/module → add to `concepts.yaml`
   - Created or modified a data model → add to `entities.yaml`
   - Made an architectural decision → add to `decisions.yaml`
   - Completed any significant task → append to `history.jsonl`

### Rules

- **Never delete** existing entries — only add or update.
- **Never rewrite** `history.jsonl` — it is append-only.
- Keep concept names in PascalCase and stable; other files may reference them.
- If a decision is superseded, set its `status` to `Superseded` and reference the replacement ADR id.

### Optional: Runtime SQLite

For complex queries (e.g., "Find all components related to Auth modified in the last week"), agents can load the YAML/JSONL files into an ephemeral in-memory SQLite database, query with SQL, and act on the results. This gives SQL power for analysis with Git-mergeable text for storage.

## Disclaimer

This project is a personal endeavor of the individual contributors and is provided on an "as-is" basis. It is not sponsored, authorized, endorsed, maintained, indemnified by, or in any way officially affiliated with any past, present, or future employer of the contributors — including but not limited to Google IT Services India Pvt Ltd, Alphabet Inc., Microsoft R&D India Ltd, and Microsoft Corporation, or any of their subsidiaries or affiliates. All trademarks and registered trademarks are the property of their respective owners. Use of employer names is solely for identification purposes and does not imply any association or endorsement.
