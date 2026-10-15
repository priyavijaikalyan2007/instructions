<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 9363fbba-e59d-4a14-aa8c-3f9cf8c33d52
Created: 2026
-->

<!-- AGENT: Proposed structure, migration steps, and acceptance checks awaiting owner review. -->

# Instruction migration plan

Status: original reorganization proposal superseded on 15 October 2026.

## Current plan: surgical edits in place

The owner requested smaller steps and no file reorganization.
Keep existing instruction files, paths, and engineering thresholds.
Apply language-specific conventions within the existing sections, then merge selected reusable lessons from the working repositories.
The original proposal below is historical context and does not authorize reorganization or broader testing-policy changes.

1. Update language conventions in the existing files.
   Files: `README.md`, `AGENTS.md`, `CODING_STYLE.md`, `COMMENTING.md`, `MARKERS.md`, `GOF_PATTERNS.md`, `MIGRATIONS.md`, `TESTING.md`, `LOGGING.md`, and `PERFORMANCE.md`.
2. Fold in reusable lessons from apps, identity, and theme.
   Files: `ADDITIONAL_INSTRUCTIONS.md`, `PRAGMATIC_PROGRAMMER.md`, `BACKEND.md`, `SECURITY_GUIDELINES.md`, `KNOWLEDGE_ARCHITECTURE.md`, `DOCUMENTATION.md`, `TESTING.md`, `CODING_STYLE.md`, and `UI_UX_CONSISTENCY.md`.
3. Update existing planning and progress records.
   Files: this plan, the review, source inventory, status, `CONVERSATION.md`, `CHANGELOG.md`, and `agentknowledge/history.jsonl`.
4. Validate the diff and commit each focused change.
   Check added links, fences, headers, history records, retained encoding, and the absence of renamed or deleted files.
5. Push the branch and check PR access.
   Create the PR if access permits. Record the actual result.

No pattern required - simple function/class suffices.
This change edits documentation only and introduces no runtime interfaces, services, or data models.
The source repositories remain read-only.
No validator framework, guide directories, templates, or application code are part of this change.
Existing test-first requirements and coverage thresholds are not changed.

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
