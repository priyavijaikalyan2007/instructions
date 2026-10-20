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
The [review](./instructions-review.md) explains the evidence and proposed policy changes.

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

The [source inventory](./instructions-source-inventory.md) maps every existing root Markdown file to its proposed destination or retention decision.
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
The [fresh-context native audit](./native-apple-instruction-audit.md) records the requested consistency validation.
Its policy corrections remain proposals. The earlier callout-removal plan is superseded.

## Proposal: project profiles and native SaaS clients

Status: proposed for owner review on 20 October 2026. No router, template, or setup script changes are implemented.

The previous native audit missed applications that act as SaaS clients.
SAAS.md currently describes backend/frontend composition and must eventually include native client relationships.
SaaS is a product relationship, not a requirement that each client repository contain backend or browser code.

Use three separate concerns:

- AGENTS.md and shared guides contain reusable routing and engineering instructions.
- PROJECT_PROFILE.md records explicit choices for each component, including paths, targets, platforms, languages, and service relationships.
- PROJECT.md records business context, actual architecture, directory structure, commands, environments, release procedures, and local constraints.

PROJECT.md may link existing README, specifications, runbooks, and component-owned guides instead of duplicating them.
Large repositories may need separate local files per component. Those files describe project facts, not copies of generic instructions.
Project facts select configured behavior. Local constraints and exceptions must be explicit rather than silently overriding shared policy.

Recommend a manually editable profile first, with an interview script later as another editor of the same profile.
Keep profile choices out of the generic AGENTS.md body. A small bootstrap region can reference the profile and project context.
Do not keep independent checkbox, generated-reference, and script-configuration copies of the same choices.
The script should preserve handwritten context, show its proposed diff, and make repeated identical runs produce no changes.
It should initialize and modify instruction setup without changing application code or deployment state.

Represent components separately from products and service relationships.
For example, a local iOS/Swift component can consume a SaaS API whose C# backend lives elsewhere.
That client task selects native, Swift, client-contract, authentication, and applicable shared concerns.
It does not select backend implementation or database migrations merely because the remote service uses C#.
A repository containing both components selects both when a task changes both sides.
Language selection remains attached to actual component source, not assumed from an operating system.

The native SaaS client profile should route to existing generic rules where possible.
Proposed coverage includes sign-in/out and session renewal, native token storage, server-enforced authorization, API/SDK compatibility, and user-facing network/session failures.
Select account/tenant/workspace transitions, synchronization, offline behavior, and local cache cleanup only where the product supports those capabilities.
Do not assume every SaaS client needs offline editing, background synchronization, a tenant model, or a browser login implementation.
Browser shell, SQL, authorization-service, branding, directory, and deployment specifics belong to declared project context or clearly scoped examples.

Proposed implementation order:

1. Agree on the profile fields, component relationships, and ownership of local context.
2. Prototype manual templates and routing for a standalone Apple app, a native SaaS client, and a mixed SaaS repository.
3. Apply the audited scope corrections and separate product-specific facts from reusable rules.
4. Validate representative tasks using agents with fresh context. Include external-service clients and unsupported platform-guide combinations.
5. Add the interview script against the same profile model after manual selection works.

Coverage gaps must remain explicit. Selecting Android or ChromeOS does not imply that detailed platform guidance already exists.
No pattern required for this proposal. Script interfaces and implementation details remain for a later approved design.
