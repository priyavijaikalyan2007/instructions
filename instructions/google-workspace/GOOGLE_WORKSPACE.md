<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 95cc16d6-c276-4298-ab7b-5d96f10ec24c
Created: 2026
-->

<!-- AGENT: Google Workspace and Editor add-on guidance. Select only the configured hosts and runtime. -->

# Google Workspace extensions

Use this guide for add-ons integrated into Google Workspace applications.
The interview calls this target Google Workspace Extensions. Its profile value is `google-workspace`.
Record host applications, add-on type, runtime, account context, scopes, and distribution mode in the configured project-facts file.
Keep project-specific implementation rules in the configured additional-instructions file.

## Select the integration model

Google Workspace add-ons and Editor add-ons have different UI and runtime contracts.
Confirm the required host capabilities before choosing either model.
A writing assistant that edits selected Google Docs text needs different access from an add-on that only displays suggestions.

| Model | Guidance |
| --- | --- |
| Google Workspace add-on | Use the host's card-based UI and supported contextual events. Select Apps Script or a supported HTTP runtime. |
| Editor add-on | Use the editor's supported menus, dialogs, sidebars, and document APIs. Editor add-ons run in Apps Script. |
| Document-bound prototype | Record its attachment and installation limits. Do not assume that a bound script is a distributable add-on. |

Verify host and mobile support separately. Editor add-ons currently target desktop editors.
Do not emulate a Workspace host by injecting a browser extension unless that is the chosen product design.
See [Google add-on types](https://developers.google.com/workspace/add-ons/concepts/types).

## Select related guides

Common workflow, writing style, testing, logging, and security requirements remain applicable.

- Read [JavaScript](../javascript/JAVASCRIPT.md) for Apps Script or JavaScript source.
- Read [TypeScript](../typescript/TYPESCRIPT.md) when the repository compiles TypeScript.
- Read [HTML](../html/HTML.md) and [CSS](../css/CSS.md) for HTML-service sidebars or dialogs.
- Read [UI_UX.md](../UI_UX.md) and matching [component profiles](../UI_UX_COMPONENTS.md) for interaction behavior.
- Read [BACKEND.md](../backend/BACKEND.md) only for application-owned HTTP services changed by the task.
- Read [PERSISTENCE.md](../PERSISTENCE.md) for stored state and [SECRET_HANDLING.md](../SECRET_HANDLING.md) for credentials.
- Read [AIML_SECURITY.md](../AIML_SECURITY.md) whenever AI or ML processes text, documents, or suggestions.

Host-provided cards and controls do not require a browser component library or a separate web frontend.
Use HTML-service controls for supported custom editor UI. Preserve the host's sandbox and asynchronous callback model.
See [Google dialogs and sidebars](https://developers.google.com/apps-script/guides/dialogs).

## Runtime and structure

Preserve the existing layout. Keep host adapters thin and separate text-processing logic from Google service calls.
Use explicit request and response contracts between the UI, Apps Script functions, and any HTTP service.
Keep manifest source, build configuration, tests, and deployment configuration under version control.
Keep generated upload output distinct from editable source.

Apps Script uses Google's JavaScript environment. It is not a general Node.js or browser runtime.
Check supported APIs before adding a dependency that assumes Node modules, DOM access, or browser globals.
Compile and bundle TypeScript according to the configured toolchain before upload.
Verify exported callback names and manifest references in the resulting artifact.
Use the repository's configured `clasp` version and scripts when present.
See [V8 runtime](https://developers.google.com/apps-script/guides/v8-runtime)
and [clasp development](https://developers.google.com/apps-script/guides/clasp).

For an HTTP runtime, validate incoming authentication according to Google's current add-on protocol.
Verify token signature, audience, issuer, and applicable identity claims through supported libraries.
Do not trust an identity or document identifier merely because it appears in the request body.
Select the actual backend language and hosting configuration. Do not require Cloud Run or C# for every add-on.
See [HTTP runtime guidance](https://developers.google.com/workspace/add-ons/guides/alternate-runtimes).

## Permissions and account boundaries

Declare the minimum OAuth scopes needed for each operation. Review explicit manifest scopes before distribution.
Prefer current-document or contextual access when the host and feature support it.
Do not request whole-mailbox or whole-Drive access for a narrower operation.
Handle first authorization, denied scopes, revoked access, and administrator restrictions without destroying user input.
See [Workspace scopes](https://developers.google.com/workspace/add-ons/concepts/workspace-scopes).

Understand the identity under which each function and trigger runs.
A trigger or deployment can have different authorization behavior from an interactive user action.
Keep authorization-dependent work out of contexts that cannot obtain consent.
Test the configured account modes instead of assuming that the developer's account represents every user.
See [Apps Script authorization](https://developers.google.com/apps-script/guides/services/authorization).

Separate user-specific settings, shared project settings, and document state.
Do not treat script properties or client-visible HTML as a general secret vault.
Keep provider credentials out of source, UI responses, logs, and uploaded public artifacts.
Review project-editor access and storage access before storing any credential.
If the extension uses this repository's SaaS API, select [SAAS.md](../saas/SAAS.md) and [SDKs.md](../sdk/SDKs.md).
Google authorization does not establish SaaS tenant membership. Authorize that relationship on the service.
Use the generated SDK when suitable for the runtime. Record any direct-HTTP exception explicitly.

## Writing and document changes

Preserve the user's meaning, formatting, links, comments, and unaffected text.
Read only the content needed for the requested operation.
Show the proposed replacement and its destination before applying a substantive rewrite.
Separate generating a suggestion from applying it. Do not rewrite an entire document because a selection was unavailable.
Handle an empty selection, read-only document, changed selection, and concurrent edits explicitly.
Before applying a delayed result, verify that its source range still matches the intended text.
If that check fails, ask the user to review the current text instead of overwriting it.
Use supported batch or atomic update mechanisms where available. Provide a recovery path for partial changes.

For AI-assisted writing, identify what content will leave the host and which service receives it.
Treat document text as untrusted model input, including hidden instructions and pasted content.
Do not use a document instruction to expand permissions, send mail, or disclose unrelated content.
Apply the shared controls for sanitization, clipboard use, temporary storage, and sensitive diagnostic data.
Use actionable errors in the visible sidebar or card. Use an appropriate dialog when no visible error surface exists.

## Quotas and reliability

Bound document size, service calls, execution time, and retries.
Use batch reads and writes when supported. Keep expensive work out of repeated UI callbacks.
Handle duplicate events and interrupted work without applying the same document change twice.
Do not assume that a retried write failed merely because the caller did not receive its result.
Persist only the state needed to resume or detect a completed operation.
Check current quotas for the configured runtime and account type instead of copying fixed limits into the product.
See [Apps Script quotas](https://developers.google.com/apps-script/guides/services/quotas).

## Testing and distribution

Test pure text-processing code locally before exercising host APIs.
Use synthetic documents for integration tests. Avoid private writing in committed fixtures or snapshots.
Test formatting preservation, selection changes, denial and revocation, account switching, quota failures, and interrupted operations.
Exercise each supported host and add-on type through its actual test deployment.
A mocked Google service does not prove that authorization or document editing works in the host.
See [Workspace add-on testing](https://developers.google.com/workspace/add-ons/how-tos/testing-workspace-addons).

Keep local builds, Apps Script uploads, deployment creation, installation, OAuth verification, and Marketplace publication separate.
Verify project IDs, deployment IDs, versions, and the intended audience before changing a remote deployment.
Personal testing, domain-private distribution, and public Marketplace release require different preparation.
Use the current publication requirements for the chosen scope and distribution mode.
A repository push does not authorize an add-on upload, installation, or public release.
