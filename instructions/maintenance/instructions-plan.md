<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 9363fbba-e59d-4a14-aa8c-3f9cf8c33d52
Created: 2026
-->

<!-- AGENT: Active target extraction plan, completed language and in-place phases, and superseded broader reorganization. -->

# Instruction migration plan

Status: consolidation and restored document callouts are verified for PR #2 as of 20 October 2026.
The language guide phase merged through PR #1 at `0a5a868`.
The earlier in-place updates merged into main on 16 October 2026.
The original reorganization proposal was superseded on 15 October 2026.

## Current plan: target guide extraction

The owner authorized target segregation on 18 October 2026 and explicitly prohibited new engineering instructions.
Move existing target-specific material and add routing descriptions and references only.
Select targets by changed work and combine targets within one repository when needed.
Keep language selection independent from target selection.

1. Expand `BACKEND.md` and `FRONTEND.md` using existing material and topic references.
2. Create `SAAS.md`, `APPS.md`, `TOOLS.md`, `WEBSITES.md`, and `STATIC_ASSETS.md` as target-specific homes.
3. Replace the `SDKs.md` placeholder with an index to existing API/OpenAPI and language guidance.
4. Extract target material from `AGENTS.md`, `FRONTEND.md`, `PERFORMANCE.md`, `DOCUMENTATION.md`, and `ADDITIONAL_INSTRUCTIONS.md`.
5. Extract existing native-app, browser-testing, and backend-performance material from `SWIFT.md`, `JAVASCRIPT.md`, and `CSHARP.md`.
6. Move the existing CLI logging rule from `LOGGING.md` and native UI scope from `UI_UX_CONSISTENCY.md`.
7. Add target selection to `AGENTS.md` and describe target/language composition in `README.md`.
8. Preserve instruction text, examples, shared policies, source encodings, headers, and existing topic anchors.
9. Verify provenance for moved material, code preservation, links, anchors, and target/language routing.
10. Update the existing plan, review, inventory, status, changelog, conversation, and history.
11. Commit and push `docs/target-guides`, then open a PR against `main` for review.

The SDK file contains no existing generator procedures. Native platform instructions cover Apple platforms.
This extraction does not add SDK generation, Kubernetes, Android, ChromeOS, Workers, or DNS configuration procedures.
No pattern required - this is documentation segregation with no runtime code or interface changes.

Implementation and local checks are complete on `docs/target-guides`.
The extraction records 89 moved blocks, including three secondary target splits.
All 171 code blocks across the edited documents remain intact after the existing normalization rules.
One missing frontend fence is repaired without changing its JavaScript.
The branch is pushed. [PR #2](https://github.com/priyavijaikalyan2007/instructions/pull/2) is open for owner review.
The PR remains unmerged.


## Approved follow-up: consolidate subject guides

The owner approved this follow-up and requested removal of empty PERFORMANCE.md sections.
Implement on `docs/target-guides` and update PR #2. Do not merge.
Existing repository text and the supplied UI experience source are the instruction sources.
New text defines scope, navigation, and the resolution of overlaps. It does not add unrelated policy.

1. Create REPO.md, PERSISTENCE.md, UI_UX.md, and UI_UX_COMPONENTS.md.
2. Fold ADDITIONAL_INSTRUCTIONS.md into REPO.md, CODE_COMPLETE.md, PRAGMATIC_PROGRAMMER.md, CODING_STYLE.md, TESTING.md, LITERATE_ERRORS.md, CSHARP.md, JAVASCRIPT.md, and UI_UX.md.
3. Move shared commands and endpoints from BACKEND.md into REPO.md. Move storage rules and examples into PERSISTENCE.md.
4. Combine UX_UI_GUIDELINES.md and UI_UX_CONSISTENCY.md with applicable supplied UI behavior. Retire the old files and ADDITIONAL_INSTRUCTIONS.md.
5. Scope enterprise shell rules in SAAS.md and browser implementation rules in FRONTEND.md. Retain KEYBOARD.md as a focused reference.
6. Import the supplied UI common behavior into UI_UX.md and selectable component details into UI_UX_COMPONENTS.md.
7. Trim PERFORMANCE.md to shared principles and a compact topic index. Remove empty target-extraction sections and update their incoming links.
8. Update AGENTS.md, README.md, BACKEND.md, FRONTEND.md, APPS.md, TOOLS.md, WEBSITES.md, STATIC_ASSETS.md, SDKs.md, DOCUMENTATION.md, SWIFT.md, SQL.md, and affected references.
9. Resolve overlapping progress, optimistic-save, keyboard, help, and platform rules through the supplied UI behavior and existing target scope.
10. Verify instruction provenance, code-block preservation, Markdown links, guide selection, encodings, headers, and unchanged testing/style requirements.
11. Update the existing plan, review, inventory, status, conversation, changelog, and append-only history. Commit and push to PR #2.

No pattern required - this is documentation consolidation without runtime code or public interface changes.
The validation baseline is `a760183`. The private UI source remains unchanged.

Implementation is complete. REPO.md, PERSISTENCE.md, UI_UX.md, and UI_UX_COMPONENTS.md now hold their respective concerns.
ADDITIONAL_INSTRUCTIONS.md and the two old UI/UX guides are retired. Their lessons and incoming links have canonical destinations.
PERFORMANCE.md shrinks from 198 to 44 lines. Shared topic and target guides no longer keep empty redirect sections.
Validation preserves 551 code blocks, including all ten examples from the supplied UI source.
All 26 source sections and their non-heading instruction lines are accounted for, with recorded scope and overlap resolutions.
Shared style, the AGENTS.md operating workflow, test-first guidance, and coverage thresholds remain intact.
Published the consolidation in commit `6b14b43` to PR #2.
The PR title and description now reflect the final structure and validation. The owner will review and merge.


## Current plan: language guide extraction

The owner authorized a limited language split on 17 October 2026.
Keep the existing topic guides as the authority for common rules.
Move language-specific instructions and examples into root-level language guides.
The earlier product/task folder reorganization remains outside this change.

1. Create `CSHARP.md`, `SWIFT.md`, `GO.md`, `RUST.md`, `JAVA.md`, `PYTHON.md`, `JAVASCRIPT.md`, and `TYPESCRIPT.md`.
2. Create `HTML.md`, `CSS.md`, `SCSS.md`, `SQL.md`, and `SHELL.md` for their existing syntax and examples.
3. Extract language sections from `CODING_STYLE.md`, `COMMENTING.md`, `MARKERS.md`, `TESTING.md`, `LOGGING.md`, `PERFORMANCE.md`, and `GOF_PATTERNS.md`.
4. Move the language-specific migration example and secret-handling details from `MIGRATIONS.md` and `SECRET_HANDLING.md`.
5. Add explicit language selection to `AGENTS.md` and explain selective reading in `README.md`.
6. Retain common policies, established topic paths, section anchors, source encodings, and all existing examples.
7. Verify extraction completeness, link targets, headings, copyright headers, and append-only history.
8. Update this plan, the status, review, source inventory, changelog, conversation, and task history.

TypeScript reads the shared JavaScript runtime rules. SCSS reads the shared CSS rules.
Other languages do not require unrelated language guides.
No pattern required - this change reorganizes documentation without introducing runtime code or interfaces.
Use a separate branch, `docs/language-guides`, for this phase.

## Current plan: surgical edits in place

This earlier phase completed on 16 October 2026. The language extraction above is the active plan.

The owner requested smaller steps and no file reorganization.
Keep existing instruction files, paths, and engineering thresholds.
Apply language-specific conventions within the existing sections, then merge selected reusable lessons from the working repositories.
The original proposal below is historical context and does not authorize reorganization or broader testing-policy changes.

1. Update language conventions in the existing files.
   Files: `README.md`, `AGENTS.md`, `CODING_STYLE.md`, `COMMENTING.md`, `MARKERS.md`, `GOF_PATTERNS.md`, `MIGRATIONS.md`, `TESTING.md`, `LOGGING.md`, and `PERFORMANCE.md`.
2. Fold in reusable lessons from apps, identity, and theme.
   Files: `ADDITIONAL_INSTRUCTIONS.md`, `PRAGMATIC_PROGRAMMER.md`, `BACKEND.md`, `SECURITY_GUIDELINES.md`, `KNOWLEDGE_ARCHITECTURE.md`, `DOCUMENTATION.md`, `TESTING.md`, `CODING_STYLE.md`, `UI_UX_CONSISTENCY.md`, `LOGGING.md`, `FRONTEND_LOGGING.md`, `SECRET_HANDLING.md`, and `PERFORMANCE.md`.
3. Update existing planning and progress records.
   Files: this plan, the review, source inventory, status, `CONVERSATION.md`, `CHANGELOG.md`, and `agentknowledge/history.jsonl`.
4. Validate the diff and commit each focused change.
   Check added links, fences, headers, history records, retained encoding, and the absence of renamed or deleted files.
5. Publish the accepted changes through the owner-authorized direct merge into `main`.
   PR creation was blocked during review. The owner replaced that workflow with a local merge and push.
   Synchronize the retained review branch and verify local and remote commit IDs.

No pattern required - simple function/class suffices.
This change edits documentation only and introduces no runtime interfaces, services, or data models.
The source repositories remain read-only.
No validator framework, guide directories, templates, or application code are part of this change.
Existing test-first requirements and coverage thresholds are not changed.

## Detailed follow-up accepted on 15 October 2026

Complete the ten requested refinements within existing files.
Keep the shared style consistent and document only syntax-required exceptions.
Use separate types even when they contain only a few lines.
Add detailed names and runnable examples for Python, Swift, Go, Rust, and Java.
Add the five languages beside the existing examples for all 23 GoF patterns.
Restore logging detail and show safe identifier correlation without removing useful events.
Choose stacks and layouts from apps, identity, rapid, and theme. Label proposed tool layouts as recommendations.

Files: `AGENTS.md`, `CODING_STYLE.md`, `COMMENTING.md`, `MARKERS.md`, `GOF_PATTERNS.md`, `MIGRATIONS.md`, `TESTING.md`, `LOGGING.md`, and `PERFORMANCE.md`.
Update the existing plan, review, inventory, status, conversation, changelog, and history records.
Check the actual document examples through compilers, native test runners, and targeted behavior probes.
Keep verification fixtures and dependency downloads outside the repository.
No application build, file reorganization, or new tracked validation framework is needed.

## Historical proposal

Use `AGENTS.md` as a short entry point that selects guidance from independent layers.
Keep project architecture and commands in a project profile.
Preserve old instruction paths during migration so existing repositories can adopt the changes in stages.
The [review](instructions-review.md) explains the evidence and proposed policy changes.

## Proposed structure

```text
AGENTS.md                       Shared entry point and routing procedure
CLAUDE.md / GEMINI.md / CODEX.md  Thin agent entry files
PROJECT_INSTRUCTIONS.md         This repository's own documentation/tooling profile
guides/
  README.md                     Canonical routing table and scope rules
  core/                         Shared engineering and writing rules
  languages/                    Programming-language conventions
  targets/                      Product and platform requirements
  tasks/                        Guidance selected by the work requested
  reference/                    Detailed patterns, catalogs, and background
templates/
  AGENTS.project.md             Entry-point example for a consuming repository
  project-profile.md            Architecture, tools, commands, and local policy
  agent-insights.md              Template for verified local lessons
  tech-debt.md                   Deviation, owner, resolution, and review trigger
  agentknowledge/               Empty, documented knowledge-file templates
specs/                          This repository's review, plan, and status records
```

The folder name `languages` refers to programming languages.
The existing `LANGUAGE.md` becomes a compatibility entry for the shared writing guide.
Reference guides remain available without forcing every agent to read them for every task.

## Alternatives considered

| Option | Benefit | Cost or limitation |
| --- | --- | --- |
| Add more sections to the existing root files. | Small initial migration. | More unconditional reading and more contradictions between technologies. |
| Create a complete instruction set for every stack. | Each project gets a familiar package. | Security, testing, and workflow rules become duplicate copies that drift. |
| Compose core, language, product, task, and project guidance. | Reuses common rules while preserving local choices. | Needs explicit routing and validation. Recommended. |

Start with Markdown routing rather than a generator or custom configuration language.
A generator would add installation, versioning, and debugging work before the instruction structure proves useful.
If later adoption needs automation, add it against the reviewed structure.

## Routing and precedence

The shared entry point should direct agents to read the consuming project's README and project profile first.
Agents then read core rules and select every applicable language, product, and task guide.
For mixed projects, selection follows the files and boundaries changed rather than one label for the whole repository.
Examples inside instruction documents must not count as evidence that a project uses that language.

The project profile records the configured toolchains, source paths, output paths, commands, dependencies, and delivery model.
Build manifests and scripts verify those facts.
The profile also names local testing thresholds, design systems, tracking tools, and agent roles.
If guidance conflicts, the agent identifies the conflict and applies the controlling instruction hierarchy.
Shared text cannot override higher-priority agent instructions or an explicit user request.

Within this instruction package, an explicit project exception takes precedence over its shared default.
Language guides govern syntax and formatter behavior.
Product and task guides add scoped requirements without silently weakening core security or data-integrity rules.
Exceptions name their scope, reason, owner, and verification method.
Unresolved conflicts that change behavior or risk go to the owner for a decision.

Guide folders are documentation, so agents must read selected files explicitly.
The design must not assume that a tool automatically applies an `AGENTS.md` outside the source file's directory hierarchy.
Each consumer entry point must resolve paths correctly for copied instructions or a Git submodule.

## Guide contracts

Every guide will state its purpose, activation condition, governing references, mandatory rules, checks, and limits.
Each guide will link to the authoritative home of shared rules instead of repeating them.
Project examples will be labeled as examples and will not supply default credentials or production commands.
No new application interfaces, controllers, services, or data models are proposed.

No pattern required - simple function/class suffices.
For this documentation design, linked guides and a routing table suffice.
The future validator needs ordinary functions, not a class hierarchy or a Gang of Four pattern.
Application layering rules belong in the applicable product and language guides.

## Planned file changes

The [source inventory](instructions-source-inventory.md) maps every existing root Markdown file to its proposed destination or retention decision.
These destinations form the initial migration manifest.
Each relocated root instruction remains a compatibility page with its existing filename.
Referenced section anchors need corresponding headings and links during the compatibility period.

The implementation will add these canonical guides:

| Folder | Files |
| --- | --- |
| `guides/core/` | `workflow.md`, `coding-style.md`, `security.md`, `secrets.md`, `testing.md`, `logging.md`, `errors.md`, `comments.md`, `markers.md`, `dependencies.md`, `documentation.md`, `knowledge.md`, `tracking.md`, `performance.md`, `writing.md`, `copyright.md` |
| `guides/languages/` | `swift.md`, `go.md`, `rust.md`, `java.md`, `csharp.md`, `typescript.md`, `javascript.md`, `web-markup.md`, `python.md` |
| `guides/targets/` | `apple-apps.md`, `websites.md`, `web-apps.md`, `services.md`, `cli-tools.md`, `ui-libraries.md` |
| `guides/tasks/` | `api-design.md`, `access-control.md`, `audit.md`, `data-migrations.md`, `refactoring.md`, `resource-lifecycle.md`, `ai-features.md`, `sdks.md`, `ui-changes.md`, `release-operations.md` |
| `guides/` | `README.md` |
| `templates/` | `AGENTS.project.md`, `project-profile.md`, `agent-insights.md`, `tech-debt.md` |
| `templates/agentknowledge/` | `concepts.yaml`, `entities.yaml`, `decisions.yaml`, `history.jsonl` |
| `scripts/` | `check-instructions.py` |
| `tests/` | `test_check_instructions.py` |
| `.github/workflows/` | `instructions.yml` |

Reference destinations appear in the inventory because they preserve existing detailed material.
New task guides extract policy from current files and the adoption table in the review.
The API guide remains framework-neutral, while language guides contain implementation examples.
The Java guide supports the configured framework instead of choosing Spring, Quarkus, or another framework for every project.
The Apple guide covers macOS and iOS differences without treating one UI framework as mandatory.

The implementation will also modify `AGENTS.md`, `README.md`, `README_TEMPLATE.md`, `CLAUDE.md`, `GEMINI.md`, `CODEX.md`, and `ADDITIONAL_INSTRUCTIONS.md`.
Root policy files listed for relocation will become compatibility pages.
`PROJECT_INSTRUCTIONS.md` will describe this repository as documentation and tooling, not an application.
`CONTRIBUTING.md` will explain guide scope, provenance, review, and validation.
`CONVERSATION.md`, `CHANGELOG.md`, `specs/instructions.status.md`, and `agentknowledge/history.jsonl` will record progress.

Update `agentknowledge/concepts.yaml` when the validator becomes a shared module.
Record the approved instruction architecture in `agentknowledge/decisions.yaml` at implementation time.
Initialize `agentknowledge/entities.yaml` as an empty documented list because this repository has no application data models.
Preserve `agentknowledge/lcv_constraints.yaml`, legal files, existing tooling, and the STE reference PDF.
Do not relocate script documentation, external project records, or source application code.

## Implementation sequence

1. Review the structure and policy choices in this proposal.
   Owner decisions authorize the instruction rewrite and settle the choices listed below.
2. Refresh source hashes and classify any changes since this review.
   Record each adopted rule's source and resolve conflicts before migration.
3. Write failing validator tests before validator implementation.
   Cover broken links, missing guides, malformed history, routing errors, and invalid encoding.
4. Implement the validator against its tested contract.
   Record existing repository defects separately from new failures during the staged migration.
5. Write core guides and the repository profile.
   Preserve required engineering controls while removing application-specific assumptions.
6. Write language, product, and task guides.
   Apply official language conventions and the reviewed working-repository lessons.
7. Move detailed references and add compatibility pages.
   Preserve provenance, useful content, old paths, and referenced anchors.
8. Add consumer templates and routing examples.
   Verify copied-folder and submodule layouts in temporary fixture projects.
9. Validate routing, examples, links, compatibility, and scope.
   Compare the finished guides against the migration manifest and source adoption table.
10. Update records and the draft pull request.
    Mark the PR ready after the approved scope passes its checks.

The implementation uses separate commits for validation, shared policy, language/product coverage, and compatibility.
The same branch and draft PR can hold those commits after owner review.
The three working repositories remain reference sources.
Their adoption of the finished package is a separate change.

## Validator interface and tests

The proposed command is `python3 scripts/check-instructions.py --root <repository>`.
The command prints file-specific diagnostics and returns zero when validation passes.
It returns nonzero for invalid instructions or unreadable required input.
The validator uses Python's standard library so this repository needs no application runtime or package installation.

The validator will check local Markdown links and referenced fragments outside code blocks.
It will distinguish active links from template placeholders and examples.
It will parse JSON Lines records and check required fields.
Knowledge templates will use a deliberately narrow YAML subset, which the validator will check and document.
The validator will not claim to parse arbitrary YAML without a real YAML parser.

Unit tests will exercise valid and invalid fixtures for each check.
Negative fixtures must prove that every gate can fail for the defect it names.
Guide completeness checks verify the migration manifest and required scope sections.
They do not claim to prove prose quality, legal accuracy, or application security.
Review remains necessary for those properties.

## Acceptance checks

| Check | Expected result |
| --- | --- |
| Entry-point size and scope. | `AGENTS.md` targets about 100–150 lines and contains no assumed application stack, credentials, or deployment topology. |
| Swift macOS/iOS app. | Select core, Swift, Apple apps, and relevant tasks. Do not require browser components or SQL. |
| Go command-line tool. | Select core, Go, CLI, and relevant tasks. Use Go formatting and project commands. |
| Rust command-line tool. | Select core, Rust, CLI, and relevant tasks. Do not impose service/controller layers. |
| Java web application. | Select core, Java, web apps/services, frontend languages when changed, and applicable API/auth tasks. |
| .NET 10.0+ web application. | Select core, C#, web apps/services, changed frontend languages, and applicable tasks. |
| Static HTML website. | Select core, web markup, websites, and relevant UI/release tasks. Do not require a backend. |
| Existing JavaScript project. | Select JavaScript and the relevant product guide. Do not force an unrelated migration. |
| TypeScript component library. | Select TypeScript, web markup where needed, UI libraries, and consumer/publication checks. |
| Mixed Swift/Rust project. | Select both languages and verify their boundary without imposing one language's syntax on the other. |
| Behavior change or bug fix. | A relevant test fails for the expected reason before implementation and passes afterward. |
| Refactor. | Establish a passing behavior baseline and close relevant coverage gaps before changes. |
| Documentation edit. | Validate links, examples, routing, encoding, and affected records without artificial behavior tests. |
| Consumer installation. | Copy and submodule fixtures resolve every required guide and project-profile path. |
| Compatibility. | Every retained root path and referenced legacy anchor reaches its canonical guide. |
| Provenance. | Every substantive source difference has an adoption, local-scope, conflict, or exclusion decision. |
| CI and artifacts. | Validator and unit tests pass locally and in CI. Source examples do not imply that all language toolchains ran here. |

Before implementation, review the plan against coding style, security, API, performance, testing, documentation, and migration conventions.
Use the reviewed exceptions where current generic rules conflict with the approved multi-language design.
The repository has no `test.sh`, so the proposal does not claim that the existing full-suite command ran.

## Decisions for the owner

The following defaults are recommendations, not implemented policy changes:

| Decision | Recommendation |
| --- | --- |
| Organization. | Adopt the composed structure and retain legacy entry paths for the first release. |
| Testing. | Keep test-first behavior changes, use passing refactor baselines, and validate non-code work by its actual risks. |
| Coverage and assertions. | Set coverage thresholds per project and require one behavior per test rather than one assertion. |
| Formatting. | Preserve current C#/TypeScript conventions where configured. Use native formatters for Go and Rust and declared styles for Swift and Java. |
| External actions. | Remove conflicting universal push rules. Follow the active request and each project's declared policy. |
| UI reuse. | Require the project's declared design system. Keep the Knobby catalog integration optional. |
| Versions. | Pin supported toolchains per project. Cover .NET 10.0+ without assuming that every newer version is already supported. |
| Rollout. | Complete this shared-repository PR first, then adopt it through separate PRs in consuming repositories. |

The owner can approve the defaults together or change individual rows.
Implementation waits for this review because the request explicitly asks to review the plan first.

## Review update: retain callouts and validate Apple routing

The owner reversed the callout removal on 20 October 2026.
Restore language and target callouts while keeping consolidated instructions in their canonical homes.
The [fresh-context native audit](native-apple-instruction-audit.md) records the requested consistency validation.
Its policy corrections remain proposals. The earlier callout-removal plan is superseded.

## Proposal: project profiles and native SaaS clients

Status: manual profile, templates, and routing corrections implemented on 20 October 2026. The interview script remains deferred.
This revision replaces the earlier proposal for service relationships across repositories.

Treat every consuming repository as one monolith with selectable components.
Possible components include frontend, static assets, backend, persistence, documentation, website, generated SDKs, and native clients.
Native clients are optional. A SaaS can have no native client, one native platform, or several native platforms.
No cross-repository discovery, ownership model, or coordination is in scope.
Select component paths, platforms, languages, and capabilities within that repository.
Task scope determines which selected components and guides the agent actually reads.

Separate reusable instructions, project configuration, project facts, and local refinements:

| File | Responsibility |
| --- | --- |
| AGENTS.md and shared guides | Generic entry point, engineering rules, scope selection, and links to the configured project files. |
| PROJECT_PROFILE.md | Component choices, source paths, platforms, languages, capabilities, and explicit context/refinement file references. |
| PROJECT.md | Strictly project-specific information, such as business context, architecture facts, directory structure, configured commands, and environment names. No behavioral instructions. |
| ADDITIONAL.md | Project-specific instructions, nuances, and emerging engineering lessons that are not yet reflected in the shared guides. |

Use one canonical local refinement file, ADDITIONAL.md, rather than maintaining both possible filenames.
The profile explicitly identifies PROJECT.md and ADDITIONAL.md. AGENTS.md explicitly requires reading the configured refinement file.
Project facts may link existing specifications and source manifests without duplicating them.
Command values are configuration facts. Rules about how agents execute commands belong in generic guides or ADDITIONAL.md.
Generic instruction updates must preserve the profile, facts, and local refinement files.

Most native SaaS clients consume SDKs generated from the API specification and Swagger tooling.
That generated SDK is the normal API integration boundary. Do not assume an additional handwritten client abstraction is needed.
Keep generator configuration and output paths in project configuration or project facts.
Select SDK guidance and affected languages when the task changes generation, contracts, or generated-client integration.
Native app guidance still covers app-side session behavior, secure credential storage, and user-facing failures where applicable.
Do not assume offline editing, background synchronization, tenants, or a native client at all.
SAAS.md should describe the optional combination of browser, backend, database, SDK, and native surfaces.
APPS.md should identify the native SaaS client choice without imposing browser implementation rules.

Recommend a manually editable profile first, with an interview script later as another editor of the same profile.
Keep configuration choices in one place. A small AGENTS.md bootstrap section references the configured files.
Avoid independent checkbox, generated-reference, and script-configuration copies of the same choices.
The script should preserve handwritten context and refinements, show its proposed diff, and produce no changes for repeated identical answers.
It initializes or modifies instruction configuration without changing application code or deployment state.

ADDITIONAL.md also preserves lessons found during implementation.
For a reusable lesson, propose a generalized update to the authoritative shared guide.
Remove private product details from that proposed generic rule while retaining the applicable constraint and reasoning.
After the shared rule is adopted, remove or shorten a redundant local instruction while preserving any remaining project nuance.
Local lessons do not silently modify or distribute the shared instruction source.

Proposed implementation order:

1. Agree on component selections and the division between profile, facts, and refinements.
2. Prototype manual configuration and templates for a standalone Apple app, a SaaS without native clients, and a SaaS with native clients.
3. Apply the audited scope corrections and separate project-specific facts and instructions from generic rules.
4. Validate representative tasks using agents with fresh context, including disabled components and missing platform-guide coverage.
5. Add the interview script against the same profile after manual selection works.

Coverage gaps remain explicit. Selecting Android or ChromeOS does not imply that detailed platform guidance already exists.
No pattern required for this proposal. Script interfaces and implementation details remain for a later approved design.

## Implementation: error surfaces and selectable project scope

Authorized on 20 October 2026 after the Java SaaS routing review.
Implement the manual profile now. The interview script remains a later step, as previously proposed.

1. Clarify operation dialogs versus inline form errors in ERROR_DIALOG_COMPONENT.md, UI_UX.md, UI_UX_COMPONENTS.md, LITERATE_ERRORS.md, FRONTEND.md, and SAAS.md.
2. Add PROJECT_PROFILE_TEMPLATE.md, PROJECT_TEMPLATE.md, and ADDITIONAL_TEMPLATE.md. Add the instruction repository's own PROJECT_PROFILE.md, PROJECT.md, and ADDITIONAL.md.
3. Add profile reading and scope selection to AGENTS.md and REPO.md. Document setup in README.md.
4. Update SAAS.md, APPS.md, and SDKs.md for optional native SaaS clients and generated Swift SDK integration.
5. Scope framework-specific rules in API_GUIDELINES.md, BACKEND.md, BACKEND_LIBRARY_SELECTION.md, FRONTEND_LIBRARY_SELECTION.md, FRONTEND_SELECTION.md, SECURITY_GUIDELINES.md, LOGGING.md, TESTING.md, PERSISTENCE.md, STATIC_ASSETS.md, DOCUMENTATION.md, ACCESS_CONTROL.md, DELETION.md, and RESTABLE_RESOURCES.md.
6. Preserve language callouts, existing examples, copyright headers, and source encodings. Retain shared engineering policies outside the requested applicability corrections.
7. Add a reviewable Java SaaS profile example and rerun the reading-path and error-surface cases. Update the prior audit with its correction status.
8. Update CHANGELOG.md, CONVERSATION.md, specs/instructions.status.md, and append-only history. Commit and push to PR #2.

Profile contract: explicit project/refinement paths, project choices, and enabled components with source paths, targets, languages, platforms, SDK links, and deployment facts.
PROJECT.md contains facts only. ADDITIONAL.md contains local instructions and emerging lessons. Generic guides retain reusable rules.
No runtime API changes are involved. No design pattern is required for document routing and configuration templates.
Validation uses document integrity checks and task reading cases rather than application runtime tests.

### Implementation outcome

Implemented the manual profile and three project-owned file roles, with templates and an active profile for this instruction repository.
Added a fictional Java SaaS fixture and [validation report](project-profile-validation.md).
Clarified operation dialogs versus visible form errors and native platform presentation.
Connected optional native SaaS clients to their generated SDKs, including Swift.
Scoped .NET, Knobby, shell, and browser catalog implementations without removing navigation callouts or code examples.
The fresh-context reviewer passes all ten routing/error cases after the identified refinements.
The interview script and older TDD/permission-policy conflicts remain outside this implementation.

## Directory cleanup after PR #2

Authorized on 20 October 2026. PR #1 and PR #2 are merged and closed.
All three completed review branches have no commits outside main and are removed locally and remotely.
The cleanup uses docs/instructions-directory, based on synchronized main at 9f16499.

1. Keep AGENTS.md, CLAUDE.md, GEMINI.md, and CODEX.md as the four root Markdown entry files.
2. Move shared guides, templates, reference assets, and tooling manuals into instructions/.
3. Move all existing specs/ review records and fixtures into instructions/maintenance/, preserving their internal layout.
4. Move active project configuration, facts, refinements, conversation, and changelog into instructions/project/.
5. Put repository policies and a landing-page pointer in .github/. Keep LICENSE and NOTICE as legal metadata.
6. Update links and active path instructions without changing code examples or historical user input.
7. Verify file preservation, headers, encodings, links, active profiles, root inventory, and the reserved specs/ location.
8. Commit, push one cleanup branch, and open a new review PR. Do not merge.

All files in the captured move map are in scope, plus the four entry files and affected incoming references.
No runtime interfaces change. No design pattern is required for this file relocation.
Keep the operating workflow and shared engineering policies unchanged except for their relocated paths.

## Profile selector/modifier implementation

Authorized by the owner's reading-tree request on 20 October 2026.
The README trees are committed separately from the directory cleanup.

Files to create: scripts/configure-instructions.sh, scripts/configure_instructions.py,
and scripts/tests/test_configure_instructions.py.
Files to update: instructions/REPO.md, instructions/README.md, .github/README.md,
instructions/maintenance/instructions-plan.md, instructions/maintenance/instructions.status.md,
instructions/project/PROJECT.md, instructions/project/CHANGELOG.md,
instructions/project/CONVERSATION.md, and agentknowledge/history.jsonl.

No pattern required - simple functions suffice. The script edits Markdown configuration, not application architecture.
Keep CLI input/output separate from parsing, validation, preview, and filesystem writes.
No HTTP or service layer is involved.

Public CLI: configure-instructions.sh [--root PATH] [--answers JSON] [--dry-run | --apply | --check].
With no answer file or read-only flag, interview the user about component selections and actual source facts.
JSON answers use saas_product and a components object keyed by stable component identifier.
Component fields are enabled, source_paths, targets, languages, platforms, saas_client, sdk_component, and deployment.
Omitted fields preserve existing values. An unknown field is an error rather than a silent omission.
Manual profile edits remain supported. The Markdown profile remains the single source of truth.

1. Write failing end-to-end tests for initialization, modification, preservation, validation, and read-only behavior.
2. Implement the Python standard-library editor and a Bash forwarding wrapper.
3. Preview changed configuration and the managed AGENTS block before the user applies the plan.
4. Copy missing generic guides and root entries, preserving existing guides and project-owned files.
5. Validate enabled fields, unique identifiers, target names, source paths, project paths, and SDK references before writes.
6. Report missing language/platform guide coverage without substituting Apple or browser instructions.
7. Reject paths outside the target repository, symlink destinations, and malformed managed blocks.
8. Verify repeatability, custom components, handwritten content, disabled template values, and invalid-input no-write behavior.
9. Document setup, modification, JSON input, and check commands. Record actual test outcomes.

Project facts are never inferred from language examples. Missing facts remain explicitly unspecified.
Initialization does not create application directories or modify application code, Git, deployments, or credentials.
Generic guide updates remain a separate operation. Existing generic guides are preserved.

### Selector outcome

Implemented the Bash entry, standard-library Python editor, and 35 integration tests.
Added instructions/maintenance/profile-selector-validation.md to record checks and limits.
Initialization and modification share the existing Markdown profile.
The interview, JSON updates, preview, explicit apply, and read-only check are available.
Preservation and rejection cases pass, including legacy-encoded facts and aliased project-file paths.
Shared workflow wording remains unchanged apart from relocated paths and trailing whitespace.

## Follow-up: explain the profile interview

PR #3 merged at 4312353. Base this correction on synchronized main in fix/profile-interview-guidance.
The owner found component identifiers, target codes, and source-path prompts opaque.
The owner also asked how SaaS differs from backend and frontend.

Files: scripts/configure_instructions.py, scripts/tests/test_configure_instructions.py,
instructions/REPO.md, instructions/maintenance/instructions-plan.md,
instructions/maintenance/instructions.status.md, instructions/maintenance/profile-selector-validation.md,
instructions/project/PROJECT.md, instructions/project/CHANGELOG.md,
instructions/project/CONVERSATION.md, and agentknowledge/history.jsonl.

No pattern required - simple functions suffice. Keep terminal presentation separate from profile parsing and writes.
Retain the JSON and Markdown contracts. Add human-readable interview context and numeric target selection.
SaaS remains a product-level composition choice. Preserve older explicit saas target values for compatibility.
Do not add SaaS to the component-choice menu or change enabled components automatically.

1. Write failing CLI tests for repository context, component descriptions, field help, numeric targets, and retained defaults.
2. Explain SaaS and show the selected repository/profile before asking project questions.
3. Explain each component using its configured targets and covered paths, including custom identifiers.
4. Explain every editable field and provide examples at its prompt.
5. Show numbered target descriptions without offering SaaS as a peer component type.
6. Preserve existing Markdown field lines when the user accepts equivalent defaults.
7. Run the full selector suite and read-only repo checks, document the interaction, commit, push, and open a follow-up PR.

### Revised interview design after the product-category clarification

The owner's six product categories replace the proposed low-level target menu above.
Add scripts/profile_interview.py for product selection and terminal explanations.
Keep Markdown/JSON parsing and filesystem writes in configure_instructions.py.
The UI receives parsed components and returns the existing answer-document shape.
No new profile schema or application architecture policy is required.

Offer: SaaS webapp, SaaS with native clients, backend-only microservice, standalone native app,
static website, and CLI tools. Allow compatible combinations for a monolithic repository.
Select backend, frontend, static-assets, apps, websites, tools, and SDK guidance behind those choices.
SaaS composition remains a product flag, not a separate component question.
Explain custom component names as local profile labels. Ask only for the selected parts' actual project facts.
Preserve custom content, existing defaults, and the JSON/manual routes.
The earlier prompt-text tests will be updated to match this revised interaction, then observed failing before implementation.

### Product-category outcome

Implemented the revised six-category interview in scripts/profile_interview.py.
Added agentknowledge/concepts.yaml for the new shared interview module and its core editor relationship.
The editor receives the existing answer-document shape. No Markdown or JSON schema migration is required.
All 44 tests pass, including category composition, default preservation, and standalone transition from native SaaS.
The actual library interview reports No changes after every current value is retained.
The setup guide and validation report describe category choices, automatic target selection, advanced configuration, and write boundaries.
