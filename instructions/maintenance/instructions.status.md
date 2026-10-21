<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 5484def9-0307-4c48-b717-4579374090b1
Created: 2026
-->

<!-- AGENT: Current scope, verification, and next action for the shared instruction updates. -->

# Instruction repository status

Updated: 20 October 2026.

## Current phase: interview correction complete, merge approved

PR #3 merged at 4312353. Local main is synchronized with that merge.
The active correction branch is fix/profile-interview-guidance.
The owner found the raw component identifiers, target codes, and source-path prompts opaque.
The revised interview starts with six requested product categories and explains their included parts.
It selects underlying guides automatically, shows the target repository, and explains each requested project fact.
Existing profile names remain local identifiers. Defaults retain their formatting and current choices when accepted.
All 44 selector tests pass, including each category, combined categories, clear prompts, and SaaS-to-standalone switching.
[PR #4](https://github.com/priyavijaikalyan2007/instructions/pull/4) is open for owner review.
The implementation is ffefb5a on fix/profile-interview-guidance. The owner authorized its merge on 20 October 2026.

## Completed phase: directory cleanup, reading trees, and profile selector

PRs #1, #2, and #3 are merged and closed.
Shared instructions live in instructions/, project-owned context in instructions/project/, and maintenance records in instructions/maintenance/.
Root AGENTS.md routes to instructions/AGENTS.md. The other root entries are CLAUDE.md, CODEX.md, and GEMINI.md.
The README contains the shared baseline and five scenario reading trees.
The original selector supports interview and JSON input, previews, read-only checks, and preservation of project-owned content.
The initial implementation passed 35 tests and retained all 559 original code blocks.
Validation and follow-up results are in [profile-selector-validation.md](profile-selector-validation.md).

## Completed phase: subject consolidation

The approved follow-up merged through [PR #2](https://github.com/priyavijaikalyan2007/instructions/pull/2).

AGENTS.md selects shared repository work, target, shared concern, and language independently.
REPO.md holds common commands and session workflow. PERSISTENCE.md holds storage integrity and configured database examples.
UI_UX.md combines general interaction guidance. UI_UX_COMPONENTS.md keeps detailed profiles separately selectable.
KEYBOARD.md remains the browser shortcut registry, scoped by focus and platform.
The old catch-all and two old UI/UX guides are retired. Their lessons and links have canonical homes.
The owner reversed the callout cleanup on 20 October. Language and target callouts are restored, including PERFORMANCE.md topic sections.
Consolidated instructions remain in their canonical guides.

The [approved plan](instructions-plan.md#approved-follow-up-consolidate-subject-guides) defines the scope.
The [review](instructions-review.md#approved-consolidation-on-18-october-2026) records scope and overlap resolutions.
The [inventory](instructions-source-inventory.md#approved-subject-consolidation-snapshot) records source provenance.

## Verification

All 551 parsed code blocks are preserved, including ten examples from the supplied UI source.
All 26 source sections are imported. Instruction-line checks account for moved and adapted material.
Local links, incoming references, source encodings, copyright headers, new GUIDs, and append-only history pass checks.
Shared style, the operating workflow, test-first rules, and coverage thresholds remain unchanged.
The supplied UI source remains unchanged. Public instructions do not require that private file.
This documentation-only change has no application build or runtime test run.
Temporary validation artifacts remain under `/tmp/target-guide-consolidation/`.

## Current phase: language guides

The language phase is complete and merged through PR #1 at `0a5a868`.
It created 13 root-level language guides and preserved all 184 GoF examples.
TypeScript also reads JavaScript. SCSS also reads CSS. LANGUAGE.md remains the natural-language writing guide.

## Previous phase

The in-place instruction updates remain merged at `7278ab3`.
The owner authorized that direct merge and push on 16 October 2026.
Application source repositories remain unchanged by the instruction extraction phases.

## PR review follow-up

The owner approved the proposed cleanup and requested removal of empty performance sections.
That approved follow-up is implemented above. The earlier project-specific EF snapshot mandate remains removed.

## Native Apple validation

A fresh-context sub-agent audited the path from AGENTS.md after callout restoration.
The [audit](native-apple-instruction-audit.md) lists startup, shared, native, and conditional reading for three task types.
The native route works, but shared web-platform mandates, a missing planning reference, and workflow conflicts remain.
Proposed corrections are recorded for review. This pass changes no engineering policy.

## Current phase: manual project profiles and scoped SaaS clients

The manual profile and templates are implemented and pushed as b6bcd89 on docs/target-guides for PR #2.
The PR title and description now reflect the implemented profile and validation scope.
AGENTS.md reads PROJECT_PROFILE.md, the configured facts-only PROJECT.md, and the configured local ADDITIONAL.md.
Enabled component paths and changed behavior select targets, languages, platforms, and shared concerns.
Native SaaS clients are optional and normally use generated SDKs. Swift is indexed in SDKs.md.
The interview script remains deferred. No cross-repository coordination is introduced.

Failed commands without a suitable visible error surface use literate dialogs.
Visible forms use inline errors or a persistent summary. Native interfaces use platform presentation.
Framework and product examples now have explicit applicability conditions.

The [validation report](project-profile-validation.md) records all ten fresh-context reading/error cases as passing.
All 559 code blocks counted across the broader Markdown baseline remain unchanged.
No new Markdown link defects were introduced. Existing encoding, headers, workflow, and append-only history checks pass.
The prior audits remain dated evidence with pointers to this follow-up.
The older TDD-exception and production-fix permission-policy conflicts remain outside this change.
No application build or runtime test is claimed for these documentation changes.


## 21 October 2026: scoped guide reorganization

PR #4 merged at bc2bafc before this work. Branch: refactor/scoped-guides-security.
Completed target/language folders, WORKFLOW routing, preserved common rules, generalized README template, and security expansion.
Validation: 50 selector tests, live profile check and dry run, preserved examples/headers/history, and zero new link defects.
The .NET security harness accepted 3 valid responses and rejected 13 invalid responses.
See scoped-guides-security-review.md for the move map, policy changes, preservation evidence, and test limits.
Changes are committed locally for review. No push or merge is part of this update.


## 21 October 2026: extension profiles ready for merge

Added Google Workspace and browser extension guides, profile targets, interview choices, templates, and reading trees.
Choices 1 through 6 remain stable. Choice 7 selects Google Workspace. Choice 8 selects browser extensions.
The interview explains hosts, browsers, packaging, and optional SaaS relationships. Microsoft Office remains deferred.
Existing profiles retain intentionally unlinked SDKs when users accept their current selections.
All 55 tests pass. The repository profile check and dry run pass without generated changes.
Link and preservation checks report no new defects. No host extension runtime or store publication was tested.
The owner authorized pushing and merging this work together with the pending guide and security reorganization.
This authorization supersedes the previous local-only delivery scope. Merge through a pull request, then synchronize main.


## 21 October 2026: copied-project initialization

Implemented explicit new-project initialization in the existing profile configurator.
The source repository's .github/README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, and root LICENSE remain unchanged.
New policy templates collect project identity and leave unknown project decisions as visible TODOs.
Known inherited documents and records receive exact backups before replacement or removal.
Customized documents, history, and profile notes remain untouched. Conflicting licenses and symlinks stop before writes.
The generated documents honor custom project-facts and local-instruction paths.
The interview supports MIT, Apache 2.0, LGPL 2.1/3.0, GPL 2.0/3.0, AGPL 3.0, Elastic 2.0, and SSPL 1.0.
GNU choices require only or or-later. Multiple licenses use OR, with no product-name preset.
Creative Commons 4.0 variants and CC0 1.0 apply to explicit content paths.
Custom or undecided terms remain pending. Copied instruction material retains its MIT license and notices.
Pinned SPDX texts and hashes support offline setup. LGPL 3.0 includes its GPL 3.0 companion text.
A source-only maintenance command registers reviewed inherited-file hashes while retaining older versions.
All 77 tests pass, including execution from a copied repository, preview, cancellation, repeat runs, and generated links.
The actual utilextensions repository was not changed. Changes are prepared on feat/project-initialization for local review.
