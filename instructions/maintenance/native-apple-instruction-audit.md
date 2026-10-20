<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: b2ab2435-62a7-443e-8779-d79061011856
Created: 2026
-->

<!-- AGENT: Fresh-context audit of native Apple instruction selection, coverage, and scope conflicts. -->

# Native Apple instruction audit

Date: 20 October 2026.
Scope: `docs/target-guides`, after restoration of the document callouts, based on commit `794f76c`.
Method: a sub-agent started without the parent conversation and followed README.md, AGENTS.md, and their task references.
The parent checked the main findings against the source. This audit changed no engineering policy.

## Follow-up status

This document records the earlier audit before the routing corrections.
The [implementation validation](project-profile-validation.md) records the manual profile, native SaaS links, framework scopes, and error-placement clarification.
The findings below remain historical evidence. The later report identifies resolved cases and remaining boundaries.

## Result

The route reaches the native Apple and Swift instructions, but older shared mandates still create conflicting requirements.
A fresh agent receives the main native guidance. The agent must interpret some web-specific requirements to avoid applying them to native work.

The restored callouts help agents find the relevant language sections.
They do not require agents to read every language. AGENTS.md explicitly limits language reading to the changed work.

## Startup and common scope

Start with [README.md](../README.md), [AGENTS.md](../../AGENTS.md), and [REPO.md](../REPO.md).
Read the consuming project's README, relevant specifications, CONVERSATION.md, and Git history.
Read its knowledge records: concepts.yaml, entities.yaml, and decisions.yaml.
These startup requirements appear in AGENTS.md at lines 226–232 and 253–263.

This instruction checkout lacks the three named YAML records.
[KNOWLEDGE_ARCHITECTURE.md](../KNOWLEDGE_ARCHITECTURE.md), lines 98–99, addresses absent records.
Their absence does not authorize inventing application facts.

For native coding work, the shared baseline includes:

- [LANGUAGE.md](../LANGUAGE.md), [CODING_STYLE.md](../CODING_STYLE.md), [COMMENTING.md](../COMMENTING.md), and [MARKERS.md](../MARKERS.md).
- [LOGGING.md](../LOGGING.md), [TESTING.md](../TESTING.md), and [SECURITY_GUIDELINES.md](../SECURITY_GUIDELINES.md).
- [PRAGMATIC_PROGRAMMER.md](../PRAGMATIC_PROGRAMMER.md) and its [checklist](../PRAGMATIC_PROGRAMMER.checklist.md).
- [CODE_COMPLETE.md](../CODE_COMPLETE.md) and its [checklist](../CODE_COMPLETE.checklist.md).
- [COPYRIGHT_HEADER.md](../COPYRIGHT_HEADER.md) and [LITERATE_ERRORS.md](../LITERATE_ERRORS.md).
- [GOF_PATTERNS.md](../GOF_PATTERNS.md) during pattern selection for applicable design work.

AGENTS.md also requires RESTABLE_RESOURCES.md without a target condition.
It requires the absent GOF_REFACTOR.md during applicable planning work. Both issues appear below.

Shared formatting remains four spaces, no tabs, one type per file, and a maximum of 120 source characters per line.
Allman braces apply within the language's syntax limits. Swift examples and exceptions remain in SWIFT.md.
The existing test-first workflow and coverage requirements also remain in scope.

## Native target and language scope

Read [APPS.md](../APPS.md) and the relevant sections of [SWIFT.md](../SWIFT.md).
The native target covers:

- SwiftUI, AppKit, UIKit, and shared platform-independent logic.
- Xcode targets, deployment targets, architectures, schemes, signing, and capabilities.
- Existing app or Swift package layouts, target membership, and packaged resources.
- Native persistence, state restoration, permissions, lifecycle, and accessibility where affected.
- Launch time, responsiveness, memory, energy, cancellation, and lifecycle cleanup.
- Instruments, Xcode diagnostics, and relevant physical-device checks.
- Keychain storage for credentials and tokens that the client legitimately owns.
- Unit tests, XCTest UI tests, scene transitions, permission flows, and platform-specific layouts.
- Separate build, signing, archive, upload, submission, and release operations.

SWIFT.md adds references, naming, file organization, language constructs, comments, markers, folding, testing, coverage, logging, and selected pattern examples.
Its restored performance and secret callouts reach the native target sections.
A local app requires no server, database, login, or analytics by default.

## Conditional scope

The table describes intended task selection. The findings identify places where literal mandates exceed that selection.

| Changed concern | References and scope |
| --- | --- |
| Native UI behavior | [UI_UX.md](../UI_UX.md), plus only matching [UI_UX_COMPONENTS.md](../UI_UX_COMPONENTS.md) profiles. Native controls and accessibility APIs apply. |
| Stored data, document files, or save integrity | [PERSISTENCE.md](../PERSISTENCE.md), native lifecycle rules in APPS.md, and UI save safety when visible behavior changes. Read [SQL.md](../SQL.md) only when SQL changes. |
| Credentials or secrets | [SECRET_HANDLING.md](../SECRET_HANDLING.md#native-clients-and-tools), SWIFT.md, and APPS.md Keychain guidance. Backend envelope encryption has explicit server scope. |
| Performance | APPS.md performance guidance, with [PERFORMANCE.md](../PERFORMANCE.md) shared principles and relevant callouts. Native performance is already reached through APPS.md. |
| Refactoring or migration | [MIGRATIONS.md](../MIGRATIONS.md), including baseline and regression verification. |
| User or operator documentation | [DOCUMENTATION.md](../DOCUMENTATION.md) and LANGUAGE.md. A brand-scope issue remains below. |
| New resource types or deletion | [DELETION.md](../DELETION.md) is required by the current resource trigger. Its implementation mandates need narrower scope. |
| Authorization, sharing, or permissions | [ACCESS_CONTROL.md](../ACCESS_CONTROL.md) is required by the current trigger. Apple permissions and native sharing need distinction from server authorization. |
| Implementing APIs | [API_GUIDELINES.md](../API_GUIDELINES.md). Add backend, SaaS, or SDK guides only when the task changes those targets. |
| AI or machine learning | [LLM_TECHNIQUES.md](../LLM_TECHNIQUES.md), [NON_LLM_AIML_TECHNIQUES.md](../NON_LLM_AIML_TECHNIQUES.md), and [AIML_SECURITY.md](../AIML_SECURITY.md). |
| Shell or other source languages | Select each affected language guide. Editing a release script can select [SHELL.md](../SHELL.md). |
| A separate website or browser surface | Select frontend, website, static asset, and browser language guides for that surface. Native UI alone does not select them. |
| Build or release operations | REPO.md, APPS.md, the project's release scripts, and actual Xcode configuration. A build does not authorize submission or release. |

KEYBOARD.md is a browser registry. Native app shortcuts follow APPS.md and platform conventions.
Browser catalogs, Bootstrap, ARIA, and JavaScript options do not become native implementation requirements.
UI_UX.md at lines 20–23 and UI_UX_COMPONENTS.md at lines 14–18 state these boundaries.

## Task walkthroughs

| Task | Files and sections selected |
| --- | --- |
| Swift-only model change | Startup context, common coding baseline, APPS.md, and relevant SWIFT.md sections. Add persistence only for stored-data changes. Add MIGRATIONS.md for restructuring. |
| Native UI feature | Startup context, common coding baseline, APPS.md, SWIFT.md, UI_UX.md, and matching component profiles. Add storage, secrets, authorization, deletion, API, or AI guides only when relevant. |
| App release without source changes | Startup context, REPO.md release boundaries, APPS.md release guidance, project release scripts, and Xcode configuration. Add documentation or secrets guidance when affected. Source edits select their language and construction rules. |

A code-only model change should not require browser or backend implementation rules.
The next section shows why the current text does not guarantee that result.

## Findings and proposed corrections

The corrections below are proposals. This validation pass does not implement them.

| Priority | Verified finding | Proposed surgical correction |
| --- | --- | --- |
| High | AGENTS.md:190 requires DELETION.md for new resource types. DELETION.md:13–29 mandates Knobby trash behavior and SQL deletion columns. | Scope those implementation patterns to the declared platform. Preserve applicable deletion and recovery principles. |
| High | AGENTS.md:210–215 routes permissions and sharing to ACCESS_CONTROL.md. Its lines 13–28 and 330–338 prescribe Knobby services, tenant claims, and session cookies. | Distinguish server authorization from Apple platform permissions and native sharing. Scope the specific service architecture. |
| High | LOGGING.md:267–307 requires request identifiers and request/response behavior on every log line. Lines 210–226 require service configuration and deployment environments. | Qualify service/request rules and connect the existing native unified-logging route to shared requirements. |
| Medium | AGENTS.md:202 unconditionally requires RESTABLE_RESOURCES.md. Its lines 46–65 and 118–122 assume shell/iframe navigation messages. | Make URL guidance conditional on URL work. Scope shell messaging to applications that use that shell. |
| Medium | TESTING.md:75–83 uses browser automation for all end-to-end tests. Lines 496–500 direct benchmarking to BenchmarkDotNet. Native alternatives exist in APPS.md:82–90 and SWIFT.md:172–201. | Qualify browser and C# tool instructions and reference the existing Apple alternatives. |
| Medium | AGENTS.md:178–181 requires GOF_REFACTOR.md, but that file is absent. Markdown link checks do not detect this plain-text reference. | Correct or remove the stale reference after identifying its intended authority. |
| Medium | DOCUMENTATION.md:89–99 links hosting to SaaS and requires Knobby styling without a local scope condition. Native documentation reaches this guide through AGENTS.md:182. | Scope SaaS packaging and product branding to their configured project model. |
| Low | AGENTS.md:27 lists data models and entities under backend work without saying that they are backend-owned. | Clarify ownership so a local Swift model does not select backend guidance. |

Two shared workflow conflicts also need review:

- AGENTS.md:105–106 forbids implementation before a failing test. TESTING.md:23–37 permits exceptions.
- TESTING.md:286–289 requires permission before production fixes, including work that a user may already authorize.

These conflicts predate this audit. They are separate from missing Apple references.

## Coverage limits

The repository gives agents a native reading path, not a complete Apple release or persistence manual.
APPS.md delegates detailed release procedures to the consuming project's scripts and Xcode configuration.
It has no separate App Store Connect, notarization, provisioning, or privacy-manifest procedure.

Native storage guidance likewise delegates the actual storage design to the consuming project.
These are coverage limits rather than broken links. They do not justify inventing universal platform procedures.
A later routing correction can name expected project-owned guides while preserving each project's choices.

## Verification

The sub-agent used fresh context and performed a read-only audit. The parent restored callouts separately.
The main scope findings were checked against the current source after restoration.
Documentation checks preserve all 551 code blocks and account for instruction provenance.
Application builds, runtime tests, and live Apple service validation are outside this audit.
