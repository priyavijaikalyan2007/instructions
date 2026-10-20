<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: f0dd4891-b52b-4a4a-bf3a-2bb78f0fd334
Created: 2026
-->

<!-- AGENT: UI guide overlap review and manual routing test for Java SaaS with native Apple clients. -->

# UI guide review and Java SaaS routing test

Date: 20 October 2026.
Reviewed branch: docs/target-guides at 281d3be, the current PR #2 head before this report.
Method: inspect tracked branch and main files, verify PR file statuses, compare UI subjects, and follow current AGENTS.md references.
This is a manual instruction-routing test. It does not run an application, an installer, or a generated project profile.
No generic instruction changed during this review.

## Follow-up status

This document records the earlier audit before the routing corrections.
The [implementation validation](project-profile-validation.md) records the manual profile, native SaaS links, framework scopes, and error-placement clarification.
The findings below remain historical evidence. The later report identifies resolved cases and remaining boundaries.

## Current UI guide inventory

The PR file list contains both added and deleted files. It does not mean that all listed guides remain after merging.
GitHub's PR file-status response agrees with the local Git trees.

| File | PR branch | Main before merging | Role |
| --- | --- | --- | --- |
| UI_UX.md | Added | Absent | Common interaction behavior, validation, focus, state, feedback, recovery, and acceptance criteria. |
| UI_UX_COMPONENTS.md | Added | Absent | Detailed behavior profiles for fields, editors, grids, trees, overlays, and workflows. |
| KEYBOARD.md | Modified | Present | Detailed enterprise browser shortcut registry and focus scopes. |
| UI_UX_CONSISTENCY.md | Deleted | Present | Former styling, layout, state, feedback, save, and lifecycle instructions. |
| UX_UI_GUIDELINES.md | Deleted | Present | Former design principles, appearance, interaction, accessibility, and component guidance. |
| UX_UX.md | Absent | Absent | No tracked file under this name in either reviewed tree. |

The consolidation moved common behavior from the old guides into UI_UX.md.
Browser implementation examples moved to FRONTEND.md. Enterprise shell layout moved to SAAS.md.
Detailed component behavior moved to UI_UX_COMPONENTS.md, while keyboard tables remain in KEYBOARD.md.
The prior consolidation checks account for source instructions and code examples.

UI_UX.md:780 conditionally references a project-owned UI_UX_EXPERIENCES.md.
That file does not exist in this instruction checkout. The reference is conditional, not a fourth supplied guide.
The proposed project profile and ADDITIONAL.md model can later make such project-owned refinements explicit.

## Different roles with remaining overlap

The retained files have different intended responsibilities, but they are not wholly independent.
A component profile should specialize the common baseline rather than redefine it.
A library reference should explain the actual component API rather than own general interaction policy.

| Subject | Overlapping locations | Assessment |
| --- | --- | --- |
| Keyboard and focus | UI_UX.md:225–265, UI_UX_COMPONENTS.md:998–1006 and 1083–1094, KEYBOARD.md:27–90 | Common behavior, component behavior, and exact bindings are useful layers. Link the shared rule instead of restating it when no specialization exists. |
| Saving and state | UI_UX.md:339–354 and 639–691, UI_UX_COMPONENTS.md:854–864, FRONTEND.md:1038 onward | Profiles add visible form states, while frontend contains the browser storage implementation. Some repetition remains within the baseline itself. |
| Feedback and progress | UI_UX.md:317–337 and 576–635, FRONTEND.md:1007–1017, SAAS.md:237–246 | Browser and shell rules specialize common feedback. Repeated thresholds and modal choices can drift without one policy owner. |
| Error handling | UI_UX.md:513–572, ERROR_DIALOG_COMPONENT.md:12 and 175–179, FRONTEND.md:960 and 1017 | A real conflict remains. The component specification says to always show a dialog when the user needs an error. Shared guidance places field errors inline and limits modal use. |
| Components | UI_UX_COMPONENTS.md:20–38, COMPONENTS.md:7 onward, ERROR_DIALOG_COMPONENT.md:14 onward | Profiles define required behavior. COMPONENTS.md documents browser assets and factories. The error-dialog file supplies an additional design and implementation specification. |
| Product shell | SAAS.md:65–101 and 198–246, FRONTEND.md:216–247 | The generic SaaS route still carries specific browser-shell and Bootstrap assumptions. These need explicit selection under the proposed model. |

The ErrorDialog conflict is in a retained legacy specification, not a surviving copy of either deleted UI/UX guide.
LITERATE_ERRORS.md:175–186 describes browser modal rendering without a native rendering reference in that section.
Its general error-message contract remains useful to both Java and Swift.

Recommended ownership is UI_UX.md for common policy, selected component profiles for specialization, and KEYBOARD.md for browser bindings.
FRONTEND.md and APPS.md own platform implementation. Component catalogs own selected library APIs.
Retain navigation callouts as requested. Resolve conflicting normative text separately from removing duplicate prose.
This review proposes those corrections without deleting or changing any guide.

## Scenario and assumptions

One monolithic repository contains a Java SaaS backend, a browser frontend, and native Apple SaaS clients.
The server-side application and frontend assets use the configured container packaging.
Native Apple clients remain separate application targets and build artifacts within the same repository.
They use generated SDKs from the API specification as their normal service boundary.

For the reading map, assume Swift Apple targets and a TypeScript, HTML, CSS, and optional SCSS frontend.
The prompt does not specify the Java framework, database engine, frontend framework, or SDK generator.
Confirm those facts from manifests and build configuration. Do not infer Keycloak, PostgreSQL, or an additional handwritten client layer.
A container does not select Kubernetes, Cloud Run, or Cloudflare instructions by itself.

## Startup and shared reading

Start with [README.md](../README.md), [AGENTS.md](../../AGENTS.md), and [REPO.md](../REPO.md).
Read the consuming repository's existing knowledge records, CONVERSATION.md, relevant specifications, and Git history.
Use KNOWLEDGE_ARCHITECTURE.md for knowledge-record structure and absent-record handling.

For construction across the scenario, the common reading set is:

- [LANGUAGE.md](../LANGUAGE.md), [CODING_STYLE.md](../CODING_STYLE.md), [COMMENTING.md](../COMMENTING.md), and [MARKERS.md](../MARKERS.md).
- [TESTING.md](../TESTING.md), [LOGGING.md](../LOGGING.md), [SECURITY_GUIDELINES.md](../SECURITY_GUIDELINES.md), and [PERFORMANCE.md](../PERFORMANCE.md).
- [PRAGMATIC_PROGRAMMER.md](../PRAGMATIC_PROGRAMMER.md) and its [checklist](../PRAGMATIC_PROGRAMMER.checklist.md).
- [CODE_COMPLETE.md](../CODE_COMPLETE.md) and its [checklist](../CODE_COMPLETE.checklist.md).
- [LITERATE_ERRORS.md](../LITERATE_ERRORS.md) and [COPYRIGHT_HEADER.md](../COPYRIGHT_HEADER.md).
- [GOF_PATTERNS.md](../GOF_PATTERNS.md) for applicable design work, with only selected language and pattern examples.

The current AGENTS.md also unconditionally references RESTABLE_RESOURCES.md and conditionally requires the absent GOF_REFACTOR.md.
These known routing issues remain. Shared rules do not require reading every linked language example.

## Selected target and language files

The table gives the combined reading set for work across all described components.
A narrower task selects only affected rows and sections.

| Work | Files and source configuration |
| --- | --- |
| SaaS composition and cross-surface contracts | [SAAS.md](../SAAS.md). Its current scope still describes only backend/frontend composition. |
| Java backend and container runtime | [BACKEND.md](../BACKEND.md), [JAVA.md](../JAVA.md), actual Dockerfile and packaging configuration, Maven or Gradle wrapper, runtime configuration, and build scripts. |
| API and generated SDK contract | [API_GUIDELINES.md](../API_GUIDELINES.md), [SDKs.md](../SDKs.md), API specification, and actual generator configuration. Select Swift and browser-language sections for generated clients in those languages. |
| Browser frontend | [FRONTEND.md](../FRONTEND.md), [TYPESCRIPT.md](../TYPESCRIPT.md), shared [JAVASCRIPT.md](../JAVASCRIPT.md), [HTML.md](../HTML.md), and [CSS.md](../CSS.md). Add [SCSS.md](../SCSS.md) when SCSS exists. |
| Bundles and static asset delivery | [STATIC_ASSETS.md](../STATIC_ASSETS.md), configured asset build and server output mapping. Do not assume the library-specific hosting example. |
| Apple clients | [APPS.md](../APPS.md), [SWIFT.md](../SWIFT.md), Xcode or Swift package configuration, target membership, schemes, capabilities, and affected release scripts. |
| UI behavior across browser and native surfaces | [UI_UX.md](../UI_UX.md), with only matching [UI_UX_COMPONENTS.md](../UI_UX_COMPONENTS.md) profiles. |
| Browser keyboard and logging behavior | [KEYBOARD.md](../KEYBOARD.md) and [FRONTEND_LOGGING.md](../FRONTEND_LOGGING.md). Native clients use native platform conventions and Swift logging sections. |

There is no separate container guide in this routing path.
BACKEND.md contains deployment and resource boundaries. JAVA.md contains toolchain, packaged runtime, profiling, and resource guidance.
The actual Dockerfile and launch configuration supply the project facts.

## Conditional references

| Concern that changes | Additional files |
| --- | --- |
| Stored data, transactions, or local client persistence | [PERSISTENCE.md](../PERSISTENCE.md). Add [SQL.md](../SQL.md) for actual SQL work. Apply engine-specific sections only to the configured engine. |
| Sign-in credentials, tokens, or server secrets | [SECRET_HANDLING.md](../SECRET_HANDLING.md), with native storage selected through APPS.md and SWIFT.md. |
| Application authorization, ownership, or sharing | [ACCESS_CONTROL.md](../ACCESS_CONTROL.md). Its current Knobby-specific implementation assumptions remain a finding. |
| New resource types, deletion, or retention | [DELETION.md](../DELETION.md). Its current platform-specific requirements remain a finding. |
| Dependency selection | [BACKEND_LIBRARY_SELECTION.md](../BACKEND_LIBRARY_SELECTION.md), or [FRONTEND_LIBRARY_SELECTION.md](../FRONTEND_LIBRARY_SELECTION.md) and [FRONTEND_SELECTION.md](../FRONTEND_SELECTION.md) for browser work. |
| Browser component reuse | FRONTEND.md component workflow and the selected component catalog/reference. COMPONENTS.md and ERROR_DIALOG_COMPONENT.md are specific references, not universal native prerequisites. |
| User/operator documentation or published contracts | [DOCUMENTATION.md](../DOCUMENTATION.md), with configured delivery and branding. |
| Refactoring or migration | [MIGRATIONS.md](../MIGRATIONS.md). |
| Changed shell scripts | [SHELL.md](../SHELL.md). A container alone does not select shell guidance. |
| Separate static website work | [WEBSITES.md](../WEBSITES.md), plus the affected browser and asset guides. A SaaS browser frontend alone does not select this target. |
| AI features | [LLM_TECHNIQUES.md](../LLM_TECHNIQUES.md), [NON_LLM_AIML_TECHNIQUES.md](../NON_LLM_AIML_TECHNIQUES.md), and [AIML_SECURITY.md](../AIML_SECURITY.md). |
| Component distribution or consumer-artifact testing | [TEST_PLAN.md](../TEST_PLAN.md) where its library-specific checks apply. |

C#, Go, Rust, Python, and unrelated SDK languages are not selected solely because examples or links mention them.
DOTNETFX_SELECTION.md does not apply to a Java-only backend.
If SDK regeneration actually changes other language outputs, select those affected language guides for that task.

## Walkthroughs within this monolith

| Task | Target and language reading beyond the shared baseline |
| --- | --- |
| Change a Java endpoint without changing its contract | BACKEND.md, JAVA.md, API_GUIDELINES.md, and relevant persistence/security sections. |
| Change a contract used by browser and Apple clients | Backend, API, SDK, Java, frontend, browser languages, app, and Swift guides for the affected code. Check actual generator output and integrations. |
| Change only an iPad layout | APPS.md, SWIFT.md, UI_UX.md, matching profiles, and native tests. Backend and Java implementation do not enter scope merely because they share the repository. |
| Change container packaging only | REPO.md, BACKEND.md, relevant JAVA.md build/runtime sections, and actual packaging files. Native UI profiles do not enter scope. |

## Test result and unresolved gaps

Result: partial pass. The current route finds the major target and language guides, but it does not provide consistent scope throughout.
The project-profile selector, PROJECT.md template, ADDITIONAL.md template, and interview script remain proposals, not implemented features.
They cannot be counted as successful current routing.

| Finding | Evidence and consequence |
| --- | --- |
| Native SaaS composition is not encoded | SAAS.md:16 defines backend/frontend composition. APPS.md links neither SAAS.md nor SDKs.md. A fresh agent must combine those concerns from the task. |
| Swift SDK navigation is missing | SDKs.md:28–32 lists TypeScript, Java, C#, Go, and Python, but omits Swift. AGENTS.md still provides a direct Swift route. |
| Generic backend sections contain .NET mandates | BACKEND.md:117–166 includes ASP.NET middleware, Task.WhenAll, GreenDonut, dotnet profilers, and C# attributes under broader headings. |
| SaaS examples can impose the wrong implementation | SAAS.md:65 onward mandates the browser super-app shell. Line 160 names appsettings.json as backend configuration, which does not describe general Java configuration. |
| UI references still overlap and conflict | The error-dialog specification mandates dialogs beyond the cases selected by UI_UX.md. Browser implementation and common policies repeat related requirements. |
| Shared native conflicts remain | The earlier [Apple audit](native-apple-instruction-audit.md) records service logging, browser test tools, platform permissions, deletion, branding, and workflow conflicts. |
| Required planning file remains absent | GOF_REFACTOR.md is referenced in plain text by AGENTS.md but does not exist in the checkout. |

The next implementation pass should apply the approved configuration model and scope corrections, then repeat this test from fresh context.
This report does not claim that the unimplemented selector or generic-rule corrections already work.
