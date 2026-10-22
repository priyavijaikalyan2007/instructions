<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: b3f2bb2c-c5d6-49b9-8277-3726a948da36
Created: 2026
-->

<!-- AGENT: Verified reading cases for manual component profiles and error presentation. -->

# Project profile and error-surface validation

Date: 20 October 2026.
Baseline: 3d79b38 before this implementation. Validation covers the working changes prepared for PR #2.

## Implemented scope

AGENTS.md now reads the manual PROJECT_PROFILE.md and its configured project-facts and local instruction files.
PROJECT.md holds facts. ADDITIONAL.md holds local refinements and emerging lessons.
The enabled components, their source paths, and changed behavior determine the selected guides.
The interview script remains deferred. No script is required for manual selection.

The [profile template](../PROJECT_PROFILE_TEMPLATE.md), [facts template](../PROJECT_TEMPLATE.md), and [refinement template](../ADDITIONAL_TEMPLATE.md) support consuming repositories.
This instruction repository has its own active documentation/tooling profile. Application examples do not enable application work here.
The [Java SaaS fixture](examples/java-saas/PROJECT_PROFILE.md) supplies the fictional consuming-project profile for the reading tests.
Its paths represent one monolithic repository. It contains no buildable application artifacts.

## Fresh-context reading tests

A sub-agent started without the parent conversation and read the entry point, fixture, and actual generic guides.
The first review found remaining browser catalog, shell persistence, and setup-placeholder ambiguities.
Those findings were corrected. The sub-agent rechecked the files and reported all ten cases passing.

| Case | Result | Expected selection or behavior |
| --- | --- | --- |
| Full Java backend, browser frontend, and Apple clients | Pass | SAAS.md, BACKEND.md, FRONTEND.md, STATIC_ASSETS.md, APPS.md, SDKs.md, and affected Java, Swift, and browser languages. Add relevant shared concerns. |
| iPad layout only | Pass | APPS.md, SWIFT.md, UI_UX.md, matching component profiles, and native tests. No unrelated backend or generated-client implementation. |
| Container packaging only | Pass | REPO.md, BACKEND.md, relevant JAVA.md runtime sections, and actual packaging files. Add SHELL.md only when scripts change. |
| Shared API contract | Pass | API_GUIDELINES.md, SDKs.md, producer/consumer targets as affected, and generated Swift/TypeScript language guidance. |
| Apple component disabled | Pass | Exclude Apple app implementation. A separately enabled Swift SDK still selects Swift guidance when its output changes. |
| Standalone Swift app, SaaS client=no | Pass | APPS.md, SWIFT.md, and relevant shared concerns. No automatic SaaS, SDK, server, login, or database requirement. |
| Canvas Save failure without a suitable error surface | Pass | Literate operation-error dialog. Native apps use platform dialogs. |
| Form field validation failure | Pass | Inline field errors and a summary when needed. |
| Form save failure | Pass | Form error summary or persistent operation-status area, with input retained. |
| Background failure | Pass | Persistent failure state in the established status surface, with escalation when immediate user action is required. |

The reading cases establish guide applicability, not runtime correctness of a future application.
Java framework, database engine, and generator settings still come from the consuming project's actual configuration.

## Integrity checks

The temporary checker compares the complete pre-edit and post-edit Markdown example sets, including content and multiplicity.
All 559 counted code blocks are preserved. This count includes script README examples and the two existing error-dialog examples.
The older consolidation's 551 count excluded the malformed error-dialog file and non-root documentation.
The stray final fence in ERROR_DIALOG_COMPONENT.md is repaired without changing either example.

Local Markdown files and incoming references introduce no new file or heading-link defects.
The broader scan records 113 pre-existing link defects, mostly component-library paths absent from this instruction checkout.
Those existing references were not changed by this task.

Existing file encodings, copyright headers, and GUIDs remain intact. New files have unique GUIDs and AGENT markers.
The operating workflow and shared coverage thresholds remain unchanged.
The history log remains append-only. Whitespace checks pass.

Profile checks cover required local file paths, enabled fields, recognized targets, source paths, and SDK-component references.
The active repository profile selects documentation and local repository tools.
The fixture selects Java backend, browser frontend, generated clients, and Apple clients.
Disabling the Apple component and leaving placeholders in disabled template components both pass.

## Remaining boundaries

The interview script is a future step, not an implemented feature.
Android and ChromeOS selection still requires actual platform guidance from the consuming project where coverage is absent here.
The older TDD-exception and production-fix permission-policy conflicts remain outside this routing correction.
This documentation change does not claim application builds, runtime tests, container execution, or App Store validation.

## 22 October 2026: project-file locations

The Java fixture now keeps its project files at the fixture root, matching current setup output.
Its scenario and prior validation findings remain unchanged.
