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
- Read [Apps Script](../apps-script/APPS_SCRIPT.md) for the Apps Script runtime, including compiled TypeScript output.
- Read [TypeScript](../typescript/TYPESCRIPT.md) when the repository compiles TypeScript.
- Read [HTML](../html/HTML.md) and [CSS](../css/CSS.md) for HTML-service sidebars or dialogs.
- Read [UI_UX.md](../UI_UX.md) and matching [component profiles](../UI_UX_COMPONENTS.md) for interaction behavior.
- Read [BACKEND.md](../backend/BACKEND.md) only for application-owned HTTP services changed by the task.
- Read [PERSISTENCE.md](../PERSISTENCE.md) for stored state and [SECRET_HANDLING.md](../SECRET_HANDLING.md) for credentials.
- Read [AIML_SECURITY.md](../AIML_SECURITY.md) whenever AI or ML processes text, documents, or suggestions.

Host-provided cards and controls do not require a browser component library or a separate web frontend.
Use HTML-service controls for supported custom editor UI. Preserve the host's sandbox and asynchronous callback model.
See [Google dialogs and sidebars](https://developers.google.com/apps-script/guides/dialogs).

## Recommended source layout

Use `src/extensions/googleworkspace/<extension-name>/` for a new Workspace extension family.
Apply the [shared folder convention](../REPO.md#folder-and-file-structure). Preserve existing configured source paths.

```text
src/extensions/googleworkspace/<extension-name>/
    shared/                Pure processing code shared by this extension's host adapters
    docs/                  Google Docs host source and manifest, when selected
    gmail/                 Gmail host source and manifest, when selected
    sheets/                Google Sheets host source and manifest, when selected
    slides/                Google Slides host source and manifest, when selected
    assets/                Authored runtime images and Marketplace listing material
    test/                  Extension component tests, subject to the configured toolchain
```

Here docs/ names the Google Docs host. User documentation belongs in repository-root `docs/<extension-name>/.`
Use per-host projects when the add-on model requires them. One multi-host Workspace deployment can instead share its configured manifest.
Do not duplicate manifests solely to fill this example tree.
Keep build inputs, clasp configuration, and generation scripts with their actual deployment project.
Keep generated upload files in ignored output directories.
If the extension owns an HTTP service, place that server implementation under `src/service/<service-name>/backend/.`
The HTTP-backed extension's profile scope must cover both its extension configuration and its service source.
Separate profile components can express different languages or ownership boundaries.
Create host adapters only for selected current hosts. Keep future host directories absent until their work enters scope.
Use `playbooks/<extension-name>/` for installation and publication procedures and root test/ for cross-component workflows.

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

## Build and package

Start with the profile's current hosts, model, runtime, account context, and distribution choice.
Read this section for every Workspace implementation. Select only the applicable runtime and UI steps.
Record project IDs, commands, artifact paths, and release owners in the configured project-facts file.
Keep future Gmail, Sheets, or Slides support outside active scope until the owner selects that work.

For a Docs tool with a custom HTML sidebar, consider an Editor add-on.
For Gmail or shared card interfaces, consider a Workspace add-on.
Verify the required document operations before selecting the model.
Each Editor add-on extends one editor. Several Editor add-ons can share a Marketplace listing.
Keep their manifests, project IDs, build outputs, tests, and release versions distinguishable within this repository.
Share pure processing code where useful. Do not assume that one host adapter works in another host.
See [Google's integration comparison](https://developers.google.com/workspace/extend).

### Apps Script artifacts

1. Keep appsscript.json, source, dependency locks, and build configuration under version control.
2. Pin the build tools and clasp version.
3. Compile TypeScript and bundle supported dependencies into Apps Script-compatible JavaScript when those sources are used.
4. Preserve callable function names referenced by manifests, menus, triggers, and UI callbacks.
5. Copy the manifest and prepared code into a dedicated upload directory.
6. Configure clasp's root directory and ignore rules to include only the intended upload artifacts.
7. Inspect that directory before upload.

Exclude tests, development dependencies, private fixtures, credentials, and unrelated repository files from uploaded artifacts.
Do not assume clasp performs the repository's TypeScript or SCSS build.
Keep credentials outside tracked clasp configuration. Review the destination script ID before each upload.
Document local build, validation, upload, version creation, and deployment as separate repository commands.
See [clasp development](https://developers.google.com/apps-script/guides/clasp).

### Editor UI assets

Keep editable HTML, client scripts, and styles separate from generated output.
Compile client TypeScript for the HTML-service browser context, separately from server-side Apps Script code.
When SCSS is selected, compile it to CSS.
Package local client scripts and CSS in HTML-service files using script and style elements.
Keep included fragments separate when that improves maintenance. Verify their generated names and references.
Use asynchronous google.script.run calls for server operations and show pending, success, and failure states.
Test the HTML sandbox and any external HTTPS assets in the actual host.
See [HTML-service packaging](https://developers.google.com/apps-script/guides/html/best-practices).

A card-only Workspace add-on uses host-rendered widgets.
Do not add an HTML sidebar or a SCSS bundle merely because the host runs in a browser.
Host icons and card images can still require accessible HTTPS URLs.
Keep those runtime assets separate from Marketplace listing artwork.
See [Workspace manifests](https://developers.google.com/workspace/add-ons/concepts/manifests).

### HTTP artifacts

Build the configured service language into its declared server or container artifact.
Define the add-on manifest and HTTPS callback endpoints through the Workspace deployment configuration.
Keep an editable copy of that configuration in the repository.
Verify incoming Google identity tokens and return the required card response JSON.
Test timeout, retry, authorization, and response-schema failures through the actual host integration.
Record endpoint ownership and deployment identifiers in project facts.
Use [backend guidance](../backend/BACKEND.md) for this service.
Do not require a separate SaaS product, database, or web frontend unless the application needs one.
See [HTTP runtime setup](https://developers.google.com/workspace/add-ons/guides/alternate-runtimes).

## Distribution and release assets

Read this section for the selected audience, including projects that currently use test installation.
The interview records release intent. It does not grant permission to create remote resources or publish.

| Choice | Required preparation |
| --- | --- |
| Test installation | Use the model-specific developer test flow and permitted test accounts. A Marketplace listing is not required. |
| Private Marketplace | Use an eligible Workspace organization account. Confirm domain audience, administrator restrictions, and installation policy. |
| Public Marketplace | Prepare the listing, complete Marketplace review, and complete applicable OAuth verification before external distribution. |

Private distribution is an organization boundary, not a list of personal Gmail accounts.
Review audience before saving Marketplace visibility. Google currently prevents changing that choice afterward.
Use a standard Google Cloud project for Apps Script publication and configure the Marketplace SDK and OAuth consent.
Align declared scopes across code, manifest, consent configuration, and listing configuration.
For an Editor release, record the published script version. For a Workspace release, record the appropriate deployment ID.
See [publication preparation](https://developers.google.com/workspace/add-ons/how-tos/publish-add-on-overview).

### Marketplace material

Prepare the following material for private or public listings:

- Product name, descriptions, category, supported hosts, and accurate pricing information.
- Application icons, a listing card banner, and screenshots of the actual host integration.
- Support, privacy-policy, and terms-of-service pages at accessible URLs.
- Setup and administrator instructions when installation needs additional configuration.
- Test instructions and access details required by the current review process.

Use synthetic content in screenshots. Keep editable artwork separate from exported listing images.
Validate current image sizes, formats, branding rules, and required fields before submission.
Do not embed changing pixel dimensions in build assumptions without checking Google's requirements.
See [listing assets and support links](https://developers.google.com/workspace/marketplace/create-listing).

Record the chosen location for listing source and exported assets in project facts.
Include those paths in the extension component's source scope.
A listing image does not require enabling a generic static website or browser frontend component.
If this repository owns a separate support website, select that website as its own component.

### Verification and release sequence

1. Run local tests and inspect the built artifacts.
2. Upload the prepared Apps Script artifacts or deploy the configured HTTP service to the intended test environment.
3. Install the add-on through the selected model's test procedure.
4. Verify consent, host UI, document operations, error recovery, and account restrictions using synthetic data.
5. Verify runtime logos, image URLs, and external service boundaries.
6. Prepare the intended release version or deployment reference.
7. Review listing assets, policies, audience, and scopes.
8. Complete required verification and publication review before the authorized release.
9. Test installation and updates as a permitted user after publication.
10. Record the released version and the procedure for returning to the previous working version.

For Editor tests, select a test document, script version, and initial authorization state.
Exercise installation and enablement states. Document test-deployment limits for triggers and stored properties.
See [Editor testing](https://developers.google.com/workspace/add-ons/how-tos/testing-editor-addons)
and [Workspace testing](https://developers.google.com/workspace/add-ons/how-tos/testing-workspace-addons).
Keep build success, host-test success, OAuth verification, and Marketplace acceptance as separate recorded results.
