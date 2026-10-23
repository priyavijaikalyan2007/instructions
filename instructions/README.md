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
Project configuration and local refinements live at the repository root and remain project-owned during generic updates.
Setup state and backups live under .instructions/.
Instruction-maintenance plans, audits, and examples live under instructions/maintenance/.
The consuming repository's specs/ directory is reserved for its actual product and repository specifications.

This repository contains shared instructions for coding tools and optional project-specific role assignments.
Root PROJECT_PROFILE.md selects components, languages, and multiple roles per tool.
The neutral tool entry files reference AGENTS.md. Shared role definitions remain in instructions/AGENT_ROLES.md.

Instead of using a monolithic, single instruction file, the AGENTS.md file references multiple individual files for specific instructions. It also tells the agent how to clean, build, test and run the code.

These instructions cover Swift apps for macOS and iOS, Go and Rust tools, Java and .NET 10.0+ applications, and TypeScript/JavaScript/HTML projects.
Existing Python, SQL, CSS, and SCSS guidance also applies where those languages are used.
Read [REPO.md](REPO.md) for shared repository operations.
Select [PERSISTENCE.md](PERSISTENCE.md) for stored data and [UI_UX.md](UI_UX.md) for user-facing behavior.
Load only relevant [component profiles](UI_UX_COMPONENTS.md#select-component-profiles) and [keyboard details](frontend/KEYBOARD.md).

Some sections describe a .NET SaaS example. Apply those sections only when they match the changed target and project model.
Keep project-specific architecture, toolchain versions, and commands consistent with that repository's README and build configuration.

## Guide ownership and retained files

Common guides stay directly under `instructions/`. Target guides live under their target folder.
Language guides live under their language folder. Keep descriptive filenames, such as `apps/APPS.md` and `swift/SWIFT.md`.
The shared workflow is `instructions/WORKFLOW.md`. The root `AGENTS.md` remains the agent entry point.

The selector installs the full shared library, including unselected guides. It excludes project records and maintenance examples.
Changing a profile never deletes guides or application source. Select additional categories when they become relevant.
The profile remains authoritative. The selector derives its root links from those choices and preserves text outside its managed block.
Run the selector after manual profile edits. Use `--check` to detect outdated root links.
Generic guide upgrades remain a separate reviewed operation. Existing installed guides are preserved.
For an existing flat installation, review the relocation map before retiring old copies. The selector does not delete them.

## Project configuration

[WORKFLOW.md](WORKFLOW.md#load-project-configuration) reads the active PROJECT_PROFILE.md before selecting guides.
The profile identifies project facts and local refinements, then selects enabled components and their source languages.
PROJECT.md contains facts only. ADDITIONAL.md contains project-specific instructions and emerging lessons.
Root README.md introduces the product and explains first use. PROJECT.md holds its detailed project facts.
PROJECT_PROFILE.md records component scope and instruction selections. Link to details rather than duplicate them.
Root CONTRIBUTING.md, CODE_OF_CONDUCT.md, and SECURITY.md describe project policies.
Reserve .github/ for GitHub configuration, such as workflows and issue templates.

Use the [profile template](PROJECT_PROFILE_TEMPLATE.md), [facts template](PROJECT_TEMPLATE.md), and [refinement template](ADDITIONAL_TEMPLATE.md).
Follow [manual setup](REPO.md#manual-setup) or use the [profile selector](REPO.md#profile-selector) to initialize or modify selections.
Run `./configure.sh --root /path/to/project` from this checkout for the interview.
Interactive terminals use ncurses forms with editable fields, selection lists, scrolling help, and a final review.
Choose platforms before languages for native apps, CLI tools, and generated SDKs.
Language lists show supported choices for the selected component and platforms.
Use F5 Back and F6 Next to revisit UI questions. Edits rebuild dependent questions and require a fresh final review.
Use `--ui plain` for the line-oriented interface or `--ui curses` to require curses support.
Use `--check` for read-only validation and `--answers <json-file> --dry-run` to preview repeatable selections.
If you created a repository with GitHub's template feature, use [project initialization](REPO.md#initialize-a-repository-created-from-this-template).
Initialization replaces known inherited project documents and asks for licenses, business facts, and tool roles. It preserves customized files and backs up inherited originals.
Use `--target-folder /tmp/instructions-trial --dry-run` for a local interview without creating a repository or folder.
Remove `--dry-run` to repeat setup with a final preview and confirmation.
New projects receive missing operation placeholders and a SETUP.md checklist. Existing scripts are preserved.
Read [project scaffolding](PROJECT_SCAFFOLDING.md) before implementing those operations.
This repository's active profile describes the instruction library itself. Application examples do not enable application components here.
Generic instruction updates preserve project-owned profiles, facts, and refinements.

## Selective target reading

Start at [WORKFLOW.md](WORKFLOW.md#select-target-guides). Select targets for the changed work, then select its languages.
Targets describe the work. Languages describe the source. A repository can combine several targets and languages.
The target guides contain existing instructions and links to existing topic guides.

| Target | Guide | Existing material grouped here |
| --- | --- | --- |
| Backend | [BACKEND.md](backend/BACKEND.md) | APIs, runtime, containers, and backend service boundaries |
| Frontend | [FRONTEND.md](frontend/FRONTEND.md) | Browser pages, dynamic UI, login, components, and browser tests |
| SaaS or web application | [SAAS.md](saas/SAAS.md) | Backend, browser, generated SDK, and optional native composition, with cross-layer contracts |
| Tools | [TOOLS.md](tools/TOOLS.md) | CLI tools and plugins, module layouts, local commands, stdout, and stderr |
| Native apps | [APPS.md](apps/APPS.md) | Existing Apple platform, lifecycle, layout, performance, testing, and credential guidance |
| Static websites | [WEBSITES.md](website/WEBSITES.md) | Websites without an application backend and relevant browser references |
| Static assets | [STATIC_ASSETS.md](static-assets/STATIC_ASSETS.md) | Compilation, bundles, component-library distribution, CDN delivery, and static hosting |
| Google Workspace extensions | [GOOGLE_WORKSPACE.md](google-workspace/GOOGLE_WORKSPACE.md) | Workspace and Editor add-ons, host authorization, document changes, and distribution |
| Browser extensions | [BROWSER_EXTENSIONS.md](browser-extensions/BROWSER_EXTENSIONS.md) | Browser permissions, messaging, background lifecycle, packaging, and SaaS clients |
| SDKs | [SDKs.md](sdk/SDKs.md) | Index to existing OpenAPI contracts and language conventions |

A web application can combine C#/Java backend guidance and TypeScript/HTML frontend guidance.
A change to one side selects that side. A flow across both sides selects both.
The existing combined deployment examples remain available when packaging and serving share one application.
A component library combines frontend and static assets. A native app can share a repository with a separate static website.
The native material covers Apple platforms. This extraction adds no Android, ChromeOS, SDK generator, Kubernetes, or DNS procedures.

## Selective language reading

Start at [WORKFLOW.md](WORKFLOW.md#select-language-guides) and select guides for the files and boundaries the task changes.
Language guides live under instructions/<language>/. Each guide contains conventions and task examples for its language.
Common rules remain in the existing topic files, including style, comments, markers, testing, logging, performance, and patterns.
Read applicable topic sections together with the selected language guide. Follow other language links only when the task needs them.

| Language | Guide |
| --- | --- |
| C# | [CSHARP.md](csharp/CSHARP.md) |
| Swift | [SWIFT.md](swift/SWIFT.md) |
| Go | [GO.md](go/GO.md) |
| Rust | [RUST.md](rust/RUST.md) |
| Java | [JAVA.md](java/JAVA.md) |
| Python | [PYTHON.md](python/PYTHON.md) |
| JavaScript | [JAVASCRIPT.md](javascript/JAVASCRIPT.md) |
| Apps Script runtime | [APPS_SCRIPT.md](apps-script/APPS_SCRIPT.md), plus shared JavaScript rules |
| TypeScript | [TYPESCRIPT.md](typescript/TYPESCRIPT.md), plus shared JavaScript rules |
| HTML | [HTML.md](html/HTML.md) |
| CSS | [CSS.md](css/CSS.md) |
| SCSS | [SCSS.md](scss/SCSS.md), plus shared CSS rules |
| SQL | [SQL.md](sql/SQL.md) |
| Shell | [SHELL.md](shell/SHELL.md) |

For example, a Swift-only model change does not require C#, Java, or Rust instructions.
The file [LANGUAGE.md](LANGUAGE.md) continues to define natural-language writing style.
Shared guides hold common rules. Target and language guides select details for the changed work.

These instructrions are live. They are updated as and when new behaviors are encountered and need guidance.

The instructions in this repository are *horizontal* in nature. That is, they are about how to write reasonably good code in a clean, structured manner. These instructions should be combined with other instructions for architecture, code structure, do's and don'ts to get output that works.

These instructions are battle tested in my private side projects. I have found that the coding agents that I use do produce reasonably clean, well structured code. Lessons from specific problems are folded into the guide that owns the subject.
Shared workflow belongs in instructions/REPO.md, storage in instructions/PERSISTENCE.md, and interaction behavior in instructions/UI_UX.md.


## Recommended product source layout

For new components, use `src/<type>/<component-name>/` even when only one component exists.
The [shared folder convention](REPO.md#folder-and-file-structure) defines root responsibilities, database ownership, tests, and build output.
Each target guide provides its matching layout. Existing projects retain their configured paths.

```text
src/
    service/<service-name>/
        backend/
        frontend/
        static/
        database/
    website/<website-name>/
    app/<app-name>/
    sdk/<api-name>/
    extensions/
        googleworkspace/<extension-name>/
        browser/<extension-name>/
    tool/<tool-name>/
    library/<library-name>/
test/                              Tests spanning components
```

Create only currently needed directories. Unselected profiles reserve future locations by convention.
Database scripts normally belong to their owning service. Root test/ is singular, while component test folders follow their toolchain.
The interview suggests named example paths when no concrete component path is configured.
It preserves existing values and still requires explicit confirmation for absent planned paths.
First-time interactive setup previews and creates approved source folders after final approval.
Existing paths remain unchanged. Planned files require separate handling, as described in [REPO.md](REPO.md#planned-source-scope).

## Scenario reading trees

Use the common baseline with the tree for the work in scope.
Paths are relative to the consuming repository root. Bracketed conditions select a file only when that condition applies.
These trees show reading scope, not a required application directory layout.
Read relevant sections and examples, rather than every section in each linked guide.
An agent starts with its documented entry mechanism and AGENTS.md.
CODEX.md is a compatibility pointer. Codex normally loads AGENTS.md directly.
The profile identifies roles by host tool rather than model provider.

### Common baseline

```text
.
├── AGENTS.md
├── CLAUDE.md / GEMINI.md / CODEX.md       [tool entry or compatibility pointer]
├── PROJECT_PROFILE.md                   Components, languages, and tool roles
├── PROJECT.md                           Project and business facts
├── ADDITIONAL.md                        Local instructions and emerging lessons
├── CONVERSATION.md                      Prior context and session records, when present
├── CHANGELOG.md                         Project changes, when present
├── SETUP.md                             Project initialization checklist, when generated
├── .instructions/                       Initialization state and historical backups, when generated
└── instructions/
    ├── AGENT_ROLES.md                    Shared role definitions and tool entry guidance
    ├── PROJECT_SCAFFOLDING.md            [project setup or operation-script work]
    ├── WORKFLOW.md                       Shared workflow and guide selection
    ├── REPO.md                           Setup, commands, and scope selection
    ├── LANGUAGE.md
    ├── CODING_STYLE.md
    ├── COMMENTING.md
    ├── MARKERS.md
    ├── TESTING.md
    ├── LOGGING.md
    ├── SECURITY_GUIDELINES.md             Includes applicable language security sections
    ├── AIML_SECURITY.md                   [any AI or ML feature]
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
For documentation-only work, use the narrower reading path in WORKFLOW.md.

### Native standalone app

```text
instructions/
├── apps/
│   └── APPS.md
├── swift/
│   └── SWIFT.md  [Swift Apple targets]
├── UI_UX.md  [user-facing behavior]
├── UI_UX_COMPONENTS.md  [only matching control profiles]
├── PERSISTENCE.md  [stored files, data, or state]
├── sql/
│   └── SQL.md  [actual SQL changes]
├── SECRET_HANDLING.md  [credentials or tokens]
└── shell/
    └── SHELL.md  [changed shell scripts]
```

Use native controls, state restoration, accessibility, and test tools.
A standalone app does not select SaaS, backend, generated SDK, browser, or server authentication guidance by default.
Select the actual source language for other platforms. Missing platform-specific coverage remains an explicit gap.

### Native app for SaaS

```text
instructions/
├── apps/
│   └── APPS.md
├── swift/
│   └── SWIFT.md  [Swift Apple targets]
├── saas/
│   └── SAAS.md  Surface composition and client boundary
├── sdk/
│   └── SDKs.md  Generated SDK integration
├── backend/
│   └── API_GUIDELINES.md  API contract used by the client
├── UI_UX.md
├── UI_UX_COMPONENTS.md  [only matching control profiles]
├── SECRET_HANDLING.md  Sessions and native credential storage
├── PERSISTENCE.md  [local saved data or synchronization]
├── ACCESS_CONTROL.md  [application authorization changes]
├── RESTABLE_RESOURCES.md  [resource URLs or deep links]
└── shell/
    └── SHELL.md  [changed shell scripts]
```

The generated SDK is the normal client boundary. Native dialogs use the platform equivalent of literate error content.
A native-only task does not select server implementation merely because the server shares this repository.
A shared contract change adds affected backend and browser components from their trees.
Knobby authorization and browser-shell examples apply only when selected in the profile.

### SaaS with frontend

```text
instructions/
├── saas/
│   └── SAAS.md
├── backend/
│   ├── BACKEND.md
│   ├── API_GUIDELINES.md
│   └── BACKEND_LIBRARY_SELECTION.md  [backend dependency selection]
├── java/
│   └── JAVA.md  [Java backend]
├── csharp/
│   └── CSHARP.md  [C# backend]
├── frontend/
│   ├── FRONTEND.md
│   ├── KEYBOARD.md  [browser keyboard behavior]
│   ├── FRONTEND_LOGGING.md  [configured browser logging]
│   ├── FRONTEND_LIBRARY_SELECTION.md  [browser dependency selection]
│   ├── FRONTEND_SELECTION.md  [configured vanilla/Bootstrap stack]
│   └── ERROR_DIALOG_COMPONENT.md  [browser commands without an error surface]
├── typescript/
│   └── TYPESCRIPT.md  [TypeScript source]
├── javascript/
│   └── JAVASCRIPT.md  Shared browser language rules
├── html/
│   └── HTML.md
├── css/
│   └── CSS.md
├── scss/
│   └── SCSS.md  [SCSS source]
├── static-assets/
│   └── STATIC_ASSETS.md  Bundles and delivery
├── UI_UX.md
├── UI_UX_COMPONENTS.md  [only matching control profiles]
├── sdk/
│   └── SDKs.md  [generated client integration]
├── PERSISTENCE.md  [stored data and transactions]
├── sql/
│   └── SQL.md  [SQL source or schema]
├── SECRET_HANDLING.md  [server secrets or client tokens]
├── ACCESS_CONTROL.md  [application authorization changes]
├── DELETION.md  [resource deletion or retention]
└── RESTABLE_RESOURCES.md  [resource URLs]
```

Select the backend's actual language. Java does not select .NET implementation rules or DOTNETFX_SELECTION.md.
Use actual manifests, Dockerfile, and build scripts for container packaging facts. A container does not select a hosting provider.
Add the native SaaS tree only when an enabled native component is affected.
Add the static website tree only when the task changes that separate surface.

### Static website

```text
instructions/
├── website/
│   └── WEBSITES.md
├── static-assets/
│   └── STATIC_ASSETS.md
├── frontend/
│   ├── FRONTEND.md  Applicable browser standards and accessibility
│   ├── KEYBOARD.md  [browser keyboard interactions]
│   └── FRONTEND_LOGGING.md  [configured browser component logging]
├── html/
│   └── HTML.md
├── css/
│   └── CSS.md
├── scss/
│   └── SCSS.md  [SCSS source]
├── javascript/
│   └── JAVASCRIPT.md  [browser scripts]
├── typescript/
│   └── TYPESCRIPT.md  [TypeScript source]
├── UI_UX.md  [navigation and user-facing behavior]
└── UI_UX_COMPONENTS.md  [interactive controls]
```

A static website does not select backend, database, SaaS, or native-app implementation by default.
Read API guidance only when the website actually integrates an API.
Use the configured static delivery pipeline rather than assuming the example theme-library hosting model.

### CLI tool

```text
instructions/
├── tools/
│   └── TOOLS.md
├── python/
│   └── PYTHON.md  [Python source]
├── go/
│   └── GO.md  [Go source]
├── rust/
│   └── RUST.md  [Rust source]
├── shell/
│   └── SHELL.md  [shell entry points or scripts]
├── PERSISTENCE.md  [stored files, state, or data]
├── sql/
│   └── SQL.md  [actual SQL source]
├── SECRET_HANDLING.md  [credentials or secret providers]
├── sdk/
│   └── SDKs.md  [generated service-client integration]
└── backend/
    └── API_GUIDELINES.md  [service contracts changed or consumed]
```

Select the actual tool language. Other languages remain possible when the tool uses them.
Browser and native UI guides do not enter scope for ordinary CLI processing.
Use TOOLS.md for stdout, stderr, exit status, cancellation, and local data protection.

### Google Workspace extension

```text
instructions/
├── google-workspace/
│   └── GOOGLE_WORKSPACE.md
├── apps-script/
│   └── APPS_SCRIPT.md  [Apps Script runtime, including compiled TypeScript]
├── javascript/
│   └── JAVASCRIPT.md  [Apps Script or JavaScript source]
├── typescript/
│   └── TYPESCRIPT.md  [TypeScript source]
├── html/HTML.md      [HTML-service UI]
├── css/CSS.md        [custom styles]
├── UI_UX.md
├── PERSISTENCE.md   [stored settings or document state]
├── SECRET_HANDLING.md  [credentials]
├── AIML_SECURITY.md    [AI-assisted writing or other AI features]
├── saas/SAAS.md        [this repository's SaaS API integration]
├── sdk/SDKs.md         [SaaS integration or generated SDK work]
└── backend/BACKEND.md  [application-owned HTTP service implementation]
```

Use the common baseline too. Select the host's add-on model and the actual runtime language.
Apps Script runtime selection loads both Apps Script and JavaScript guidance. TypeScript source adds its own guide.
HTTP-based add-ons select backend and actual language guidance without automatically loading Apps Script.
Card-based UI does not require HTML or a browser component library.
A writing assistant does not require a backend or AI merely because it edits documents.

### Browser extension

```text
instructions/
├── browser-extensions/
│   └── BROWSER_EXTENSIONS.md
├── javascript/JAVASCRIPT.md
├── typescript/TYPESCRIPT.md  [TypeScript source]
├── html/HTML.md              [extension markup]
├── css/CSS.md                [styles]
├── UI_UX.md
├── frontend/KEYBOARD.md      [keyboard interactions]
├── static-assets/STATIC_ASSETS.md  [applicable build and bundle sections]
├── SECRET_HANDLING.md        [credentials]
├── AIML_SECURITY.md          [AI features]
├── saas/SAAS.md              [this repository's SaaS API integration]
├── sdk/SDKs.md               [SaaS integration or generated SDK work]
├── backend/API_GUIDELINES.md [consumed or changed service contracts]
├── apps/APPS.md              [native wrapper or native messaging work]
└── swift/SWIFT.md            [actual Swift source changes]
```

Use the common baseline too. Browser-specific manifests and packaging select the supported browsers, not unrelated application targets.
Microsoft Office extension guidance is deferred.

### Author review

Check the active profile choices before tracing a tree.
For each changed behavior, follow the applicable leaves and their linked sections.
Check that conditional examples match the project's actual language, platform, and configured architecture.
Record project-local lessons in ADDITIONAL.md and propose reusable refinements for the owning shared guide.

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
