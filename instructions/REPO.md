<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 7ebb41e5-4828-41a3-9194-90cd4cb69e59
Created: 2026
-->

<!-- AGENT: Shared repository setup, commands, source verification, and session workflow. -->

# Repository work

Read this guide for repository setup, build/test/run commands, source verification, and session records.
Use [WORKFLOW.md](WORKFLOW.md#select-target-guides) to select targets and languages for the changed work.
Backend containers, native signing, and static bundle delivery remain in their target guides.

## Project configuration

The manual profile is PROJECT_PROFILE.md. AGENTS.md reads it before target and language selection.
Its Project files table declares the project-facts file and the local additional-instructions file.
Resolve configured paths from the consuming repository root.
Those default to PROJECT.md and ADDITIONAL.md. Both declared files must exist before dependent work.

PROJECT.md contains project-specific facts: purpose, structure, configured commands, versions, and environment names.
README.md introduces the project to users and contributors, with installation, first-use, support, and documentation links.
PROJECT_PROFILE.md records components, languages, paths, delivery choices, and agent roles to select applicable instructions.
Keep detailed facts authoritative in PROJECT.md and link to them from README.md when needed.
ADDITIONAL.md contains local instructions, explicit exceptions, and emerging lessons.
Keep generic rules in their subject guides. Preserve project-owned files when updating generic instructions.
An instruction that is reusable across projects can be proposed for its generic guide, then shortened locally after adoption.

### Instruction layout

Keep common guides and templates under instructions/.
Keep target and language guides under their named folders, retaining descriptive filenames.
Keep AGENTS.md, CLAUDE.md, GEMINI.md, and CODEX.md as the root instruction entry files.
Store PROJECT_PROFILE.md, PROJECT.md, ADDITIONAL.md, CONVERSATION.md, and CHANGELOG.md at the repository root.
Store README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, and SECURITY.md at the root.
Reserve .github/ for GitHub configuration, such as workflows and issue templates.
Setup previews moves from the previous .github/ document locations and repairs relative Markdown links.
Customized document content and permissions remain preserved. Conflicting root and previous files require resolution before setup proceeds.
Dry runs, cancellation, and --check leave files unchanged. Workflows and other GitHub configuration stay in .github/.
Store setup state and inherited backups under .instructions/.
Keep SETUP.md and root operation scripts project-owned.
Store instruction-library plans, audits, and examples under instructions/maintenance/.
Reserve specs/ for the consuming repository's actual product and repository specifications.
Preserve root project files and .instructions/ when distributing or updating generic guides.
Use the configured context paths when an established project uses custom locations.

### Manual setup

1. Copy instructions/PROJECT_PROFILE_TEMPLATE.md to PROJECT_PROFILE.md when no profile exists.
2. Copy instructions/PROJECT_TEMPLATE.md to the configured project-facts path when that file is absent.
3. Copy instructions/ADDITIONAL_TEMPLATE.md to the configured additional-instructions path when that file is absent.
4. Replace placeholder values for enabled components and project files with verified facts.
5. Check Enabled for each current component. Mark absent literal source paths as planned when necessary.
6. Record the component's source paths, targets, languages, platforms, SDK relationship, and deployment mode.
7. Check only the project choices that match the actual architecture.
8. Verify project-file paths and enabled component paths against the consuming repository.
9. Adjust copied profile links to resolve from the repository root.
10. Assign each copied file a new GUID according to instructions/COPYRIGHT_HEADER.md.

Unchecked example components may retain template placeholders. They do not select guides or require source paths.
For an existing setup, edit its profile and local files in place. Preserve handwritten content and local refinements.
Use the [profile selector](#profile-selector) to interview or update the same profile. Manual selection requires no script or external dependency.

### Selection contract

Components use unique identifiers and an Enabled checkbox. Unchecked components do not select guides.
Targets are backend, frontend, saas, tools, apps, websites, static-assets, sdks, documentation, google-workspace, and browser-extensions.
Use the target and language tables in WORKFLOW.md to resolve those names to generic guides.

Intersect enabled component paths with the files and behavior changed by the task.
Read the matching target and language sections, then add shared concerns for that behavior.
For a generated SDK contract change, include affected consumers and their languages.
For native SaaS integration, add instructions/saas/SAAS.md and instructions/sdk/SDKs.md without loading unrelated server implementation details.
For a native layout-only change, use the app, Swift, and relevant UI guides.
For a backend packaging-only change, use the backend, build/runtime, and actual container configuration.
Container deployment does not select Kubernetes, Cloud Run, or a static hosting provider by itself.
A missing platform guide is a coverage gap, not permission to substitute Swift or browser instructions for another platform.

The checked examples in Project choices select scoped legacy implementations, not additional components or languages.
For missing profiles, infer existing scope from source and manifests. Do not initialize a profile during unrelated work.
Report profile/source disagreements before work that depends on the disputed choice.

## Build and release boundaries

A build or test command does not authorize deployment, signing-key export, app-store submission, or release.

## Build, test, and run

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

## Local endpoints and dependencies

Read the consuming repository's README, launch configuration, and scripts for ports, health checks, and local dependencies.
The SaaS, identity service, component demo, and website may each use different endpoints.
Native apps and local tools need no listening port unless their design explicitly includes a service.
Use configured local credentials. Never copy example credentials into a deployed environment.

## Folder and file structure

Use these defaults for new repositories and newly introduced components.
Preserve configured layouts in existing components. Folder guidance alone does not authorize a migration.
Record actual paths in the profile and project facts. Keep project-specific exceptions in the configured additional-instructions file.

### Named component convention

Place product source under `src/<type>/<component-name>/`, including a repository with only one component.
Extensions use `src/extensions/<ecosystem>/<extension-name>/`, with googleworkspace and browser as the current ecosystems.
Use stable, descriptive, lowercase names separated by hyphens.
Use the same name when adding a component's tests, documentation, build output, and deployment configuration.
Do not put a language name at the type level. Select the language within its component.
Different component types can share a product name without sharing a build or deployment.

| Component | Default source location | Target guide |
| --- | --- | --- |
| SaaS or backend service | `src/service/<service-name>/` | [SaaS](saas/SAAS.md#combined-layout), [backend](backend/BACKEND.md#service-source-layout) |
| Native application family | `src/app/<app-name>/` | [Apps](apps/APPS.md#native-application-layout) |
| Static website | `src/website/<website-name>/` | [Websites](website/WEBSITES.md#recommended-source-layout) |
| Generated API clients | `src/sdk/<api-name>/` | [SDKs](sdk/SDKs.md#recommended-source-layout) |
| CLI application or plugin | `src/tool/<tool-name>/` | [Tools](tools/TOOLS.md#tool-layouts) |
| Workspace or browser extension | `src/extensions/<ecosystem>/<extension-name>/` | [Workspace](google-workspace/GOOGLE_WORKSPACE.md#recommended-source-layout), [browser](browser-extensions/BROWSER_EXTENSIONS.md#recommended-source-layout) |
| Deliberately reusable library | `src/library/<library-name>/` | [Component libraries](static-assets/STATIC_ASSETS.md#component-library-layout) |

Types describe component responsibility. They do not enable every language or instruction associated with that type.
A microservice follows the service convention without a frontend or static directory.
A native app follows the app convention whether it stands alone or consumes this repository's SaaS API.
Keep browser frontend and static source beneath their owning service or website.

### Repository roots

```text
instructions/                  Shared instructions and project-owned instruction configuration
agentknowledge/                Code navigation, decisions, and task history
specs/                         Product and repository requirements and designs
bugreports/                    Reproductions and issue evidence
playbooks/                     Development, operations, deployment, and recovery procedures
docs/                          User, administrator, and integrator documentation
src/                           Product source, resources, manifests, and component build inputs
test/                          Automated tests spanning components and their nonprivate fixtures
scripts/                       Repository-wide automation
deploy/                        Deployment and infrastructure definitions
build/                         Ignored intermediate output, grouped by component
dist/                          Ignored distributable artifacts, grouped by component
```

Keep the four agent entry files and repository-wide public documents at the root.
Root workspace manifests, lockfiles, configuration files, and entry scripts can remain where their tools require them.
A root script orchestrates components. Keep component-specific scripts with their component.
Use `test/` for new repository-wide tests. Tool-required `tests/`, `Tests/`, and `src/test/` remain valid inside components.
Preserve existing root `tests/` until a separate migration is approved.
Use component names beneath docs/, specs/, bugreports/, playbooks/, test/, and deploy/ when several components need separate records.
Keep user documentation in docs/. Copy it into generated packages or published websites when needed.
Machine-readable API contracts are source or verified generated output. Product specifications remain in specs/.

### Additive setup

Create only selected components and the directories that their current work needs.
An unused conventional location is reserved by the rule. It does not require an empty directory or placeholder source file.
When adding a component, use its named location and update the profile before dependent work.
When creating a new folder within a component, follow its owning target and language guides.
Keep package manifests, component tests, resources, and build configuration with that component.

Language-layout examples are relative to the owning project or package unless they explicitly name the repository root.
A Rust tool can therefore use `src/tool/importer/src/main.rs`.
A Swift package can use `src/library/document-core/Sources/<Target>/` and `Tests/<Target>Tests/`.
Keep Java source and tests under its project-relative src/main/java/ and src/test/java/ conventions.
Do not rename tool-required folders to enforce a different spelling.
Keep one type per source file, including short structs. See [CODING_STYLE.md](CODING_STYLE.md) for exceptions.

### Service database ownership

Keep a service's editable database scripts under `src/service/<service-name>/database/`.
Use migrations/, schema/, and seeds/ only when the configured migration workflow needs them.
Keep entities, ORM mappings, repositories, and business logic under backend/.
If an ORM requires migration classes or snapshots inside its backend project, retain that tool-required location.
Do not maintain duplicate migrations in backend/ and database/ for the same schema change.
Record migration ownership, paths, commands, and ordering in project facts.

Reserve `src/database/<database-name>/` for a database component with an independent build or migration lifecycle and an explicit owner.
Do not introduce it merely because several services use one database server.
Keep database infrastructure configuration in deploy/. Keep database files, backups, credentials, and production dumps outside tracked source.
Native app and tool persistence remains with its owning app or tool.
See [PERSISTENCE.md](PERSISTENCE.md#database-source-ownership) for migration and storage details.

### Source assets and generated output

Keep frontend code and imported UI assets under the owning frontend/ directory.
Use its sibling static/ only for authored files copied directly without compilation.
A file imported and processed by the frontend build belongs with that frontend's source assets.
Compiled JavaScript, compiled CSS, and assembled public files belong in ignored build output, not editable static/ source.
The build may copy that output into a framework-required directory such as wwwroot/.
Directory location does not determine serving. Package assets locally or deliver them through a CDN according to the deployment model.

Keep generated SDK code distinguishable from generator settings and handwritten adapters.
Record whether generated SDK source is tracked. Recreate ignored generated source through the documented generation command.
Use build/ and dist/ for repository-wide outputs. Allow ignored component-local target/, bin/, obj/, .build/, or equivalent tool output.
Preserve existing configured mappings. Do not mix generated output with authored source or commit it without an explicit artifact policy.

## Context efficiency

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

## Source and contract verification

- Edit source files rather than generated or copied build output. Confirm the source/output mapping before changing an unfamiliar file.
- Verify dependency APIs against the version actually shipped. Check the host runtime before adding a replacement for an existing service.
- Stage only files that belong to the task. Preserve unrelated working-tree changes and useful failure evidence.
- Record accepted quality deviations with a reason, owner, resolution plan, and review trigger in the project's existing tracking record.
- Treat measured counts as dated evidence. Record the file set, counting rule, command, and known exclusions.

## Clarifying questions

When any aspect of a task is unclear or ambiguous, ask clarifying questions before proceeding. Present the various choices or interpretations you see. It is better to ask questions than to make potentially incorrect assumptions.

## User configuration

When the product already provides user-configurable settings (e.g., AI provider/model, API keys, tenant/workspace settings), **do not hardcode or assume defaults**. Always:
- Use the existing configuration surfaces and stored settings.
- If a required configuration is missing or ambiguous, **ask the user** rather than choosing a model/provider or behavior unilaterally.
- Document any fallback behavior explicitly and only after confirmation.

## Conversation records

You must always update `CONVERSATION.md` with a brief description of changes made after each set of changes. This file serves as organizational and agentic memory tracking the evolution of the product. Do not skip this step.

## Commit records

You must always commit all changes to `git` with a concise description of changes made after each set of changes. This ensures that work is not lost.

## Profile selector

Run the selector from this instruction-library checkout. Use Python 3.10 or later and Bash.
The target repository must exist. Source paths normally must exist.
For new work, explicitly select [planned source scope](#planned-source-scope) for absent literal paths.
The selector uses the same Markdown profile as manual setup. It does not create a second configuration system.

### Interview and modify

```bash
./configure.sh --root /path/to/project
```

The interview starts with these product categories:

| Choice | Product category | Parts selected automatically |
| --- | --- | --- |
| 1 | SaaS | Backend, browser frontend, and static assets |
| 2 | SaaS with Native Clients | The webapp, generated SDKs, and native apps for selected operating systems |
| 3 | Microservice | Backend APIs, data access, and OpenAPI/Swagger contracts, without browser frontend or static assets |
| 4 | Native App | Standalone native application for selected operating systems |
| 5 | Static Website | Website and static assets, without an application backend |
| 6 | CLI tools | Command-line tools and plugins |
| 7 | Google Workspace Extensions | Workspace or Editor add-ons for selected host applications |
| 8 | Browser Extensions | Packaged extensions for selected browsers and operating systems |

Combine compatible choices in one repository. For example, 1, 5, 6 selects a SaaS, public website, and CLI tools.
Choose only one of 1, 2, and 3 because those categories overlap.
SaaS describes the product composition. Backend means server-side work. Frontend means the browser UI in this profile.
The interview selects the underlying guide targets automatically rather than asking for internal target codes.
These choices configure instruction scope. They do not create application structure or change its architecture.

The opening screen shows the selected repository and whether its profile already exists.
For an existing profile, press Enter at the product question to retain enabled parts and their current SaaS relationships.
Choosing new categories can disable previously selected parts in the profile. Their source files and recorded notes remain intact.
Existing documentation and unrecognized custom scopes remain preserved.

The interview explains each selected part before collecting its source paths, platforms, languages, and packaging facts.
Paths are relative to the selected repository. Supply files, folders, or matching patterns, separated by commas.
For absent literal paths, the interview offers planned scope before continuing.
Each prompt explains its meaning and gives examples. Press Enter to retain a displayed current value.
Language and platform fields use supported selection lists. In the UI, use arrows and Space to select choices.
In plain mode, enter the displayed numbers. Select several numbers when the field permits multiple choices.
Native apps, CLI tools, and SDKs collect platforms first. Their language lists reflect those platforms and component roles.
Browser components retain their browser platform. Workspace and browser extensions retain their specific host and browser menus.
Project paths and packaging descriptions remain editable facts.
In the UI, press F5 for Back and F6 or Enter for Next. Text cursor arrows retain their editing behavior.
Back saves the current field as a session draft. Next submits the field through its normal validation.
After an earlier answer changes, confirm later answers again. Matching questions retain drafts, and conditional questions are rebuilt.
Press F5 from the final review to edit the last question. Review the rebuilt plan before approving it.
Read-only result screens also allow Back. Navigation ends when approved setup starts writing files.
Drafts exist only during the current UI session. Plain mode and JSON operation remain sequential.
For a new component without a concrete source path, Enter accepts the suggested named location.
Example names such as core, companion, and writing-assistant are replaceable before accepting the path.
The defaults follow [the named component convention](#named-component-convention).
A missing suggested path still requires explicit planned-source confirmation.
Accepting unchanged defaults preserves existing Markdown formatting, including quoted path values.
Use manual profile edits or JSON answers for separate custom components and specialized SDK relationships.
The SaaS-with-native-clients choice links clients to a single selected generated SDK component when that link is unambiguous.
For several SDK components, retain a valid configured link or set the relationship through manual or JSON configuration.
The interview preserves the existing scoped-example checkboxes. Edit those manually when the actual project requires an example.

### Language and platform choices

Select only languages used within the component's source scope. Separate frontend and website components keep their own selections.
TypeScript source selects shared JavaScript guidance automatically. SCSS source also selects CSS guidance.
These references do not mean that compiled JavaScript or CSS must be selected as source languages.

| Component | Language choices |
| --- | --- |
| Backend or Workspace HTTP service | C#, Java, Go, Rust, Python, JavaScript, TypeScript, SQL, Shell |
| Browser frontend, website, or static assets | JavaScript, TypeScript, HTML, CSS, SCSS |
| Native Apple app | Swift and the web languages used within that component |
| Android or ChromeOS app | Java and the web languages used within that component |
| CLI tools | Python, Go, Rust, C#, Java, JavaScript, TypeScript, Shell. Swift is also available for macOS or Linux. |
| Generated SDKs | C#, Java, Go, Python, Rust, JavaScript, TypeScript. Swift is also available for Apple consumers. |
| Apps Script custom HTML UI or browser extension | JavaScript, TypeScript, HTML, CSS, SCSS |
| Apps Script host-rendered cards | JavaScript, TypeScript |

Native app platforms include iOS, iPadOS, macOS, Android, and ChromeOS.
Detailed native guidance covers Apple platforms. Android and ChromeOS selections retain the existing partial-coverage warning.
CLI platforms include macOS, Linux, and Windows. SDK platforms describe the consumers, including browsers and servers.
Language choices identify available instruction coverage. They do not verify framework compatibility or generator support.

Existing values outside a menu receive a labeled Keep existing selection option.
Select that option alone, or select replacement values. Setup does not silently remove project facts.
Manual profiles and JSON answers retain their existing validation and coverage warnings.
After a platform change, review the rebuilt language choices before final approval.
The choice catalog and guide mapping live in scripts/profile_choices.py.

Component identifiers are local profile names. They are not additional product categories.
In this instruction repository, instruction-library means documentation and instruction files. repository-tools means the local CLI scripts.
To configure an application, point --root at that application repository rather than this instruction-library checkout.

The selector previews profile and root AGENTS changes, lists additions, and asks before applying them.
The forms review summarizes selected components, tool roles, project files, shared guides, and source folders.
Press F3 to inspect the complete file list and exact text changes. The result screen shows status and next steps.
Plain mode retains diff output for terminal inspection and automation.
Answer no to cancel without writes.
To inspect the installed selections without an interview, use these commands:

```bash
./configure.sh --root /path/to/project --dry-run
./configure.sh --root /path/to/project --check
```

The dry run previews missing files and leaves existing selections unchanged.
The check validates installed configuration, configured project files, enabled source paths, SDK references, routing, and selected target/language guide files.
A check reports missing files instead of installing them.
Neither command writes files. A successful check does not validate application builds or every transitive instruction link.

### Local target folders

Use --target-folder to create a test setup without GitHub or a Git repository:

```bash
./configure.sh --target-folder /tmp/instructions-trial --dry-run
./configure.sh --target-folder /tmp/instructions-trial
```

The first command interviews and previews without creating the target or its missing parents.
The second command repeats the interview and creates the reviewed setup after confirmation.
Use a new folder for another clean trial. Existing project files and custom scripts are preserved.
Enter none for an unavailable repository URL. Setup does not run git init, create remotes, or contact services.
The target receives shared guides, neutral agent entries, project documents, and a copy of the setup tools.
You can then run its own `./configure.sh`. Its --check validates configuration, not application readiness.
The previous `scripts/configure-instructions.sh` entry remains available for existing commands.
Use --project-answers identity.json and --answers selections.json for repeatable noninteractive trials.
With --dry-run, those files preview the exact inputs. Replace --dry-run with --apply to apply them.

### Tool roles

First-time interviews offer Claude Code, Codex, Gemini CLI, Antigravity, Pi, Roo Code, Cline, and a custom tool identifier.
Select several roles per tool. Role definitions stay in [AGENT_ROLES.md](AGENT_ROLES.md).
Assignments and project-specific notes stay in root PROJECT_PROFILE.md.
A host tool determines the assignment. The selected model provider does not determine it.
Role assignments do not grant permissions or authorize delegation.

Edit only those assignments with this command:

```bash
./configure.sh --root /path/to/project --configure-agents
```

Existing component selections stay unchanged. Ordinary product interviews preserve existing role assignments.
JSON accepts the optional agent_roles object:

```json
{
    "agent_roles": {
        "claude": ["implementation", "testing"],
        "codex": {"roles": ["planning", "review"], "notes": "Review API boundaries."},
        "roo": ["review"]
    }
}
```

Omit agent_roles to preserve its table. Use an empty object to clear tool-specific assignments.
Setup creates a Roo workspace pointer only when needed. Custom tools require their documented instruction mechanism.
Setup preserves custom entry files. It does not install tools or modify global tool settings.

### Root project migration

Earlier installations stored project files under instructions/project/.
The updated selector previews moving the five default project Markdown files to the root.
It also moves initialization state and backups to .instructions/.
Custom context paths remain authoritative. Conflicting root and legacy files stop setup before writes.
Active document links and default project references are repaired. Historical conversation and changelog bytes remain intact.
Existing active generic guides receive only default project-path substitutions during this migration.
Dry runs and cancellation preserve all files. --check reports a required migration without applying it.
Generic policy upgrades remain a separate reviewed operation.

### Repeatable selections

Save explicit selections in a JSON answer file when an interview is unsuitable.
The answer file is input to the editor. The generated Markdown profile remains the active configuration.
Use these field names and types:

```json
{
    "saas_product": false,
    "components": {
        "native-client": {
            "enabled": true,
            "source_paths": ["src/app/companion"],
            "targets": ["apps"],
            "languages": ["Swift"],
            "platforms": ["iOS", "iPadOS", "macOS"],
            "saas_client": false,
            "sdk_component": "none",
            "deployment": "native application"
        }
    }
}
```

Replace the example path with an existing source path.
To preview and then apply the same answers, use these commands:

```bash
./configure.sh --root /path/to/project --answers /path/to/answers.json --dry-run
./configure.sh --root /path/to/project --answers /path/to/answers.json --apply
```

Omitted components and fields retain their existing values. Unknown JSON fields are errors.
New component identifiers need complete values before their Enabled choice can be true.
For a native SaaS client, select SaaS product and set saas_client to true.
Normally, sdk_component names an enabled component whose targets include sdks.
Use none only for an explicit integration choice without a configured SDK component. The selector reports that gap for review.
An SDK can generate several languages. It remains a separate selectable component even when no native client exists.

The output lists selected target and language guides. Narrow that set to the task and add the applicable shared concerns.
The selector reports absent language or native-platform coverage. It does not substitute Swift for Android or ChromeOS.
Use the [README trees](README.md#scenario-reading-trees) to inspect common and conditional reading.

### Preservation and write boundaries

Initialization copies missing shared files from instructions/ and missing neutral root agent entries.
It excludes the source repository's project/ and maintenance/ directories.
Missing project-owned files use fresh template GUIDs. Unknown project facts remain explicitly unspecified.
The selector preserves installed shared guides, custom component notes, project facts, and local refinements.
The selector edits selected Markdown fields, optional role assignments, and the marked root AGENTS block.
Recognized inherited agent entries receive neutral pointers after an exact backup. Custom entries remain unchanged.
Existing text outside that block remains unchanged. Malformed blocks require manual repair before configuration.
Manual profiles remain editable without the script.

Configured project-file paths resolve from the target repository root. Custom safe paths remain unchanged.
Project facts and refinements need separate Markdown files. They cannot replace shared guides, root entries, or SETUP.md.
Paths cannot escape the repository, enter .git, or traverse symlinks.
Repeated identical selections produce no changes after initialization.
Application code, deployments, credentials, and Git state remain unchanged.
Approved source folders and missing project script placeholders can be created during project initialization.
Existing generic guides remain installed. Legacy root-layout migration repairs only default project-path references.
Each file replacement is atomic. A filesystem failure can interrupt a multi-file apply, so inspect the reported error and retry.
Generic guide upgrades remain a separate reviewed operation.

The CLI returns 0 for a successful check, preview, apply, no-change result, or cancelled confirmation.
It returns 2 for invalid input, missing required configuration, or a filesystem error.

### Retained guides and generated scope

The selector copies missing shared files recursively, including currently unselected guides.
It excludes instructions/project/ and instructions/maintenance/ from the shared copy.
Project facts and local instructions are initialized separately and preserved after creation.
Changing selections never removes source or guide files.

The root managed block lists common obligations and the enabled target and language guides.
The profile is the source of those selections. Narrow the list further for each task.
After manual profile edits, run the selector to regenerate the block. The --check mode detects stale routing.
The --dry-run mode previews the regenerated block without writing files.
Existing guide updates and removal of superseded flat copies require a separate reviewed migration.

### Extension selections

Choose 7 for a Google Workspace or Editor add-on. Record its host and add-on type in Platforms.
Record Apps Script or HTTP runtime and the distribution mode in Packaging or delivery.
Apps Script and Google Apps Script language labels select both Apps Script and JavaScript guidance.
Select TypeScript when that is the actual source compiled by the project.

Choose 8 for browser extensions. Record browsers and operating systems, such as Chrome, Firefox, or Safari on macOS and iOS.
Combine an extension with a SaaS category when the repository contains both.
The interview asks whether each selected extension consumes this repository's SaaS API.
A Google account or browser account alone does not select SaaS-client behavior.
When unambiguous, a selected SaaS client links to the enabled generated SDK component.
Use manual or JSON configuration for multiple SDK relationships or an explicit direct-HTTP integration.
Retaining an existing profile preserves intentionally unlinked SDKs unless the relationship changes explicitly.
Microsoft Office extensions remain deferred and have no selectable preset.

## Initialize a repository created from this template

GitHub template creation copies repository files. It does not replace their project identity.
The profile selector offers initialization when it recognizes an inherited instruction-library profile.
You can also request initialization explicitly:

```bash
./configure.sh --initialize-project --root /path/to/new-repository
```

Run the updated script from this library or from a new clone that includes it.
Initialization requires Python 3.10+ and Bash. Git is optional for local-folder setup.
For an older clone, use this library's current script with --root pointing to that clone.
The initializer refuses to initialize the source instructions repository itself.
The source repository's own README, contribution policy, conduct policy, security policy, and LICENSE remain unchanged.

The interview collects repository identity, copyright ownership, licenses, business context, tool roles, and component choices.
Business questions cover users, their problem, expected value, scope, success criteria, and constraints.
Unanswered questions remain TODOs in project-owned files. JSON accepts these facts through optional business_context.
Unknown contribution rules, reporting contacts, support targets, and commands remain visible TODOs.
The existing product interview still selects targets and languages.
Existing source paths must exist. Explicitly planned literal paths may be absent and produce a configuration note.
First-time interactive setup can create explicitly approved source folders after the final preview.
It does not generate application files or invent build commands. JSON callers select folders through source_folders.

### Generated project documents

- Root README.md, which introduces the project and provides its repository landing page.
- Root CONTRIBUTING.md, CODE_OF_CONDUCT.md, and SECURITY.md.
- LICENSE containing the full terms when one software license needs no additional texts.
- LICENSES/ for multiple alternatives, separate content licenses, or required companion terms.
- THIRD_PARTY_NOTICES.md and instructions/LICENSE for copied instruction-library attribution.
- Root PROJECT_PROFILE.md and configured project facts and refinements, normally PROJECT.md and ADDITIONAL.md.
- SETUP.md, a project-owned completion checklist.
- Missing root operation scripts selected by the profile.
- .instructions/INITIALIZATION.json, which records completed initialization and licensing choices.

Tool roles come from PROJECT_PROFILE.md. Neutral entry files point to the same profile and shared role definitions.
The managed AGENTS scope is regenerated from selected components. Custom entry files remain project-owned.
Custom context paths remain authoritative. Generated links follow those paths.
Generated policy scaffolding retains its file-specific template attribution.
New application material uses the selected project terms, subject to existing third-party notices.

### Licensing choices

Select MIT, Apache 2.0, LGPL 2.1 or 3.0, GPL 2.0 or 3.0, AGPL 3.0, Elastic 2.0, or SSPL 1.0.
GNU choices require an explicit version-only or version-or-later decision.
Select several software licenses to offer alternatives joined by OR.
A product name such as Elasticsearch does not identify one universal license arrangement.
Select the exact alternatives that the project owner intends to offer.

A single software license keeps its complete legal text in root LICENSE, below the scope notice.
Multiple terms use a root scope notice and LICENSES/ for the separate texts.
LGPL 3.0 retains its GPL 3.0 companion text. Existing initialized license files are preserved.
Creative Commons offers a separate content choice, including the six 4.0 variants and CC0 1.0.
Record the paths covered by that content choice. Existing third-party and explicit file notices still take precedence.
Undecided or custom commercial terms remain pending until the owner supplies the actual terms.
The initializer never fabricates commercial terms or silently relicenses existing project work.
Read [the template and license catalog](templates/repository/TEMPLATES.md) for sources and exact behavior.

### Preview and repeatable input

Use --project-answers for identity and license choices. Use --answers for the existing component-selection JSON contract.
For example, project.json can contain:

```json
{
    "name": "utilextensions",
    "owner": "Example Owner",
    "year": "2026",
    "repository_url": "https://github.com/example/utilextensions",
    "description": "Writing tools and browser extensions",
    "license": {
        "software": ["MIT", "Apache-2.0"],
        "content": "CC-BY-SA-4.0",
        "content_paths": ["docs", "assets/art"]
    }
}
```

These values illustrate the input shape. They are not selections for the user's project.
Use an empty software list for an undecided license. An optional custom_terms string describes the pending decision.
Omit content and content_paths when no separate content license applies.

```bash
./configure.sh --root /path/to/new-repository \
    --initialize-project --project-answers project.json --answers profile.json --dry-run
```

The dry run lists every planned creation, replacement, backup, and removal. It shows policy, license, profile, and root-routing diffs.
A dry run never writes files. With --root, it reads current selections without an interview.
Explicit --configure-agents starts a role interview.
With --target-folder, a dry run can interview a new project without creating the folder.
Noninteractive initialization dry runs require --project-answers and --answers.
Replace --dry-run with --apply to apply the reviewed inputs without an interactive confirmation.
Without either option, the script requests confirmation after the preview. Cancellation writes nothing.

### Preservation and inherited history

Initialization recognizes inherited files by registered whole-file hashes, including supported earlier template versions.
It backs up exact inherited originals under .instructions/template-backup/ before replacing or removing them.
It resets an unchanged inherited profile and generates new project facts and local-instruction placeholders.
It removes unchanged source-library conversation, changelog, maintenance, and knowledge records from their active locations.
Customized records and documents remain untouched and are reported for manual review.
The backup is excluded from active project instructions. Retain it until you verify the initialization result.

Unknown license files, conflicting backups, and symlink destinations stop the operation before any writes.
Validation completes before application. Each file replacement is atomic, but the entire multi-file operation is not a transaction.
If a filesystem failure interrupts application, inspect the backups and partial changes before retrying.
The completion record is written last.

Repeat initialization preserves project documents and rejects changed identity or license answers.
Review later identity or licensing changes separately. Ordinary profile edits never replace project documents.
Shared instruction updates remain a separate reviewed operation. Initialization preserves installed shared guides.


## Product-specific Workspace setup

The Google Workspace interview asks for current hosts, add-on model, runtime, account context, and distribution.
It replaces generic operating-system and packaging questions for that component.
Editor add-ons use Apps Script. Workspace add-ons can use Apps Script or an HTTP service.
Private Marketplace distribution requires an eligible Workspace organization account.
Personal testing and public Marketplace distribution remain separate choices.

The interview explains build output, UI assets, OAuth, host testing, and release preparation for the selected model.
Read the linked [Workspace lifecycle guidance](google-workspace/GOOGLE_WORKSPACE.md#build-and-package) when implementing that component.
Host cards do not automatically select a browser frontend. An HTTP runtime selects backend guidance for its service.
The apps-script runtime selects [APPS_SCRIPT.md](apps-script/APPS_SCRIPT.md) and shared JavaScript rules, regardless of source language.
TypeScript selects its own guide too. JavaScript/TypeScript input selects both language guides.
An HTTP runtime does not select Apps Script guidance solely because the source is JavaScript or TypeScript.
Keep future host integrations out of the active selection until their work starts.

The profile records these optional fields for Workspace components:

| JSON key | Markdown label | Values |
| --- | --- | --- |
| workspace_model | Workspace model | editor, workspace |
| workspace_runtime | Workspace runtime | apps-script, http |
| workspace_account | Workspace account | personal, organization |
| workspace_distribution | Workspace distribution | test, private, public |

Use all four fields together. Platforms names the selected Google hosts.
Languages records editable source languages. Deployment summarizes the intended runtime and distribution.
Unknown remote IDs, build commands, and release contacts belong in project facts until confirmed.
Legacy profiles without these fields remain readable and report the missing structured choices.
Rerun the interview to configure those choices. Existing component notes remain intact.
When components need different models or release scopes, use separate component sections through Markdown or JSON configuration.
The interactive product choice creates one Workspace component initially and edits all enabled Workspace components on later runs.

## Planned source scope

A new repository can select instructions before its application source exists.
After a missing path, the interview offers explicit planned scope and shows that choice in the preview.
First-time interactive setup treats approved missing paths as folders and records optional Source folders metadata.
Use a future file's parent folder as interactive scope. Existing files can remain individual source paths.
Only approved source folders and their parents are created after final apply approval.
Application files are not generated. Dry runs, checks, cancellation, and validation failures create no folders.
Existing-profile edits retain planned paths without automatically requesting new directory creation.
JSON and manual profiles can select folders explicitly through source_folders or Source folders.
Each folder must match a literal source path in the same enabled component.
An empty source_folders list clears that selection. Planned files need no Source folders entry.
Folder creation rejects symlinks, paths outside the repository, and conflicts with existing or planned instruction files.
Git does not track empty folders. Rerun the selector to restore configured empty folders after cloning.
The optional Source state field accepts existing or planned. JSON input uses source_state.
When the field is absent, validation requires existing paths, as before.
Unmatched patterns remain errors. Use literal paths such as src/extensions/googleworkspace/markdown for planned work.
Unsafe paths, symlinks, and paths beneath regular files remain errors in either mode.

For example, a new Docs component can contain:

```text
- Source paths: src/extensions/googleworkspace/markdown
- Source folders: src/extensions/googleworkspace/markdown
- Source state: planned
- Targets: google-workspace
- Languages: TypeScript, HTML, SCSS
- Platforms: Google Docs
- Workspace model: editor
- Workspace runtime: apps-script
- Workspace account: personal
- Workspace distribution: test
```

Retain the component's Enabled, SaaS client, SDK component, and Deployment fields when using this excerpt.
A successful profile check validates configuration. It does not prove that planned source or a deployable add-on exists.
An empty bootstrapped folder does not mean that application source exists or a build passed.
Keep Source state: planned until implementation exists. Then update the state through the profile or JSON.
Older planned profiles without Source folders can still accept the interview's detected existing-path state.

## Product-specific browser setup

The browser interview collects browsers, operating systems for each browser, distribution, and actual source languages.
The current preset covers Chrome and Edge desktop, Firefox desktop and Android, and Safari on selected Apple platforms.
Select current targets only. Other browsers and delivery models require separately verified project configuration.

The language menu explains JavaScript execution and TypeScript compilation.
Select individual script, markup, and stylesheet languages from the checklist.
Script-only selections are valid. Include JavaScript or TypeScript for executable source.
Apps Script is a separate Google runtime, not a browser extension source language.
The Workspace interview uses the same selections for its Apps Script runtime.
HTTP Workspace services use the backend-language selection list.

| Profile field | JSON field | Values |
| --- | --- | --- |
| Browser targets | browser_targets | Browser/OS pairs, such as chrome-macos, firefox-android, safari-ios |
| Browser distribution | browser_distribution | test, store, self-hosted |

Platforms summarizes the selected pairs. Deployment summarizes the selected installation channel.
Self-hosted in this preset means Mozilla-signed Firefox XPI distribution, not a generic backend hosting mode.
For different distribution modes, use separate component sections.
Older free-text browser profiles remain readable and receive a warning to rerun the browser interview.

Read [browser build and distribution guidance](browser-extensions/BROWSER_EXTENSIONS.md#build-assets-and-distribution).
The interview explains manifests, compiled bundles, packaged assets, local tests, stores, signing, and listing requirements.
An extension that calls an API still needs an installed extension package.
Source defaults are src/extensions/browser/markdown and src/extensions/googleworkspace/markdown.
Replace the example name. Keep each extension's profile scope narrow and independent.
The selector warns when literal Workspace and browser scopes overlap, such as a browser scope of src/.
Shared source remains allowed when that overlap is intentional.

## Terminal presentation

Interactive terminals use ncurses forms through Python's optional curses module.
This covers project facts, licenses, tool roles, product choices, and final approval.
Text boxes support cursor movement, Delete, Backspace, Home, End, Ctrl+A, Ctrl+E, Ctrl+U, and Ctrl+W.
Long answers scroll within the text box. Terminal key sequences do not become project facts.
Correct invalid identity and business facts in the current field. Accepted answers remain available.

Use Up and Down to move through choices. Use Space to select checkboxes and Enter to continue.
For numeric menus, you can also edit the selected values directly in the text box.
Use PgUp and PgDn to scroll field guidance. Use F2 to review all interview messages.
The full change review appears before the final approval question. Approval defaults to no.
Esc opens a cancellation choice before apply. A result view remains available after completion.
Terminal resize preserves the current answer. Small windows request at least 60 columns and 18 rows.
Curses restores terminal modes after normal completion, explicit cancellation, and exceptions.

Use these presentation modes:

| Option | Behavior |
| --- | --- |
| --ui auto | Use curses for an interactive terminal. Use plain output for automation and unsupported terminals. |
| --ui curses | Require curses for an interview. Report unavailable terminal support before setup writes. |
| --ui plain | Use the line-oriented interview explicitly. |

Python curses support is optional. Setup does not install terminal packages.
On supported macOS and Unix Python builds, it provides the ncurses interface without a separate UI dependency.
See [Python's curses documentation](https://docs.python.org/3/library/curses.html) for platform availability.
Plain mode remains available when curses is missing, TERM=dumb, or input or output is redirected.
JSON apply and check commands remain suitable for scripts.

Use --color auto for terminal detection, --color never for monochrome, or --color always to force supported colors.
Automatic color selection honors NO_COLOR and redirected output.
Monochrome curses still uses terminal screen-control codes. Redirected auto mode emits plain stream output.
Labels and selection markers retain meaning without color.

## Project scaffold and readiness

Initialization creates missing profile-specific operation scripts and root SETUP.md.
Read [PROJECT_SCAFFOLDING.md](PROJECT_SCAFFOLDING.md) for the script selection and implementation contract.
Scripts provide usage, logging, argument checks, and failure examples. Their project operations remain TODOs.
Existing script implementations remain unchanged. Selecting another target adds its missing entry scripts.

For backend work, use test for the local machine, dev for staging, and prod for production.
These are environment names, not provisioned resources. Record actual destinations and secret references in project facts.
Keep credentials out of source, script arguments, and logs.
The preview prints file-specific completion steps. SETUP.md records the same tasks for later review.
A successful selector check does not mean that placeholder scripts build, test, deploy, or validate the application.

### Business-context answers

Add an optional business_context member to the project identity JSON. These values are facts rather than instruction selections:

```json
{
    "users": "Technical writers",
    "problem": "Repeated manual document cleanup",
    "value": "Less editing time",
    "scope": "Google Docs and browser extensions",
    "success_criteria": "Fewer manual formatting steps",
    "constraints": "No service backend in the initial release"
}
```

This example is the member value, not a complete project-answers file.
The required identity and license fields still apply. Complete unknown facts in PROJECT.md after setup.
The recorded initialization identity is preserved on repeats. Later changes to project facts remain project-owned edits.
