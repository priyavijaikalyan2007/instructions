<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: a6b8ba6a-527a-4a55-8782-e619765ae2b0
Created: 2026
-->

<!-- AGENT: Chrome, Firefox, and Safari extension guidance with optional SaaS integration. -->

# Browser extensions

Use this guide for packaged browser extensions. The profile target is `browser-extensions`.
Record supported browsers, operating systems, minimum versions, manifest versions, permissions, and distribution modes as project facts.
A browser extension can stand alone or provide a surface for the same repository's SaaS product.
Its browser permissions and installation lifecycle differ from a normal website.

## Select related guides

Common workflow, writing style, testing, logging, and security requirements remain applicable.
Read [JavaScript](../javascript/JAVASCRIPT.md), [TypeScript](../typescript/TYPESCRIPT.md), [HTML](../html/HTML.md),
and [CSS](../css/CSS.md) only for the actual source languages.
Use [UI_UX.md](../UI_UX.md) and relevant [keyboard guidance](../frontend/KEYBOARD.md) for user interaction.
Read applicable [static asset](../static-assets/STATIC_ASSETS.md) build sections for bundles and packaged resources.
Extension packaging rules take priority over ordinary website CDN examples.

For a SaaS integration, read [SAAS.md](../saas/SAAS.md), [SDKs.md](../sdk/SDKs.md),
and the relevant [API contract](../backend/API_GUIDELINES.md).
Select backend implementation only when the task changes it.
For a Safari app wrapper or native messaging host, read [APPS.md](../apps/APPS.md) and the actual native language guide.
A Safari JavaScript-only change does not automatically select Swift implementation work.

## Browser compatibility and execution

Keep browser-specific manifest generation and adapters explicit. Share feature logic where APIs have equivalent behavior.
Verify API support for each browser and minimum version rather than assuming that all WebExtensions APIs are identical.
Document unsupported features and avoid silent permission expansion as a compatibility workaround.
See [Mozilla cross-browser development](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Build_a_cross_browser_extension).

Chrome Manifest V3 uses an extension service worker for background work.
Register event listeners correctly, persist necessary state, and tolerate worker termination and restart.
Do not depend on global variables surviving or on DOM APIs existing in the worker.
Bundle executable code with the extension. Do not download scripts or evaluate server responses as code.
See [Chrome service worker basics](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/basics).

Firefox's background model can differ from Chrome's, including Manifest V3 event-page support.
Select the manifest fields supported by each targeted browser version.
Test background startup, shutdown, message delivery, and state recovery on each browser.
See [Mozilla background manifest reference](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/background).

Safari adds Apple packaging and permission behavior to the web extension model.
Read the current Safari conversion, app-wrapper, and distribution requirements for the targeted Apple platforms.
Do not assume that a Chrome archive is an installable Safari release.
Keep signing, notarization, store submission, and release distinct from local extension builds.
See [Safari web extensions](https://developer.apple.com/documentation/safariservices/safari-web-extensions)
and [Safari distribution](https://developer.apple.com/documentation/safariservices/distributing-your-safari-web-extension).

## Recommended source layout

Use `src/extensions/browser/<extension-name>/` for a new browser extension family.
Apply the [shared folder convention](../REPO.md#folder-and-file-structure). Preserve existing configured layouts.

```text
src/extensions/browser/<extension-name>/
    background/            Background handlers and worker source
    content/               Page content scripts and injected styles
    ui/                    Popup, options, and side-panel source
    shared/                Logic shared within this extension
    manifests/             Source manifests or browser-specific manifest inputs
    assets/                Authored icons and store-listing material
    test/                  Browser extension component tests, subject to toolchain conventions
    safari/                Apple wrapper project, only when Safari packaging requires one
```

Keep package manifests, locks, and build scripts with the extension project.
Keep generated browser archives and assembled manifests in ignored build or distribution output.
A source manifest can retain a tool-required filename or location within this component.
Place a separate native companion application under `src/app/<app-name>/` when the product has one.
Do not duplicate a Safari extension wrapper as a companion app merely to populate both directories.
Use root test/ for workflows spanning the extension, SaaS, SDKs, or native companion.
Keep user guides under `docs/<extension-name>/` and publication procedures under `playbooks/<extension-name>/.`

## Structure and boundaries

Preserve the repository's layout. Keep popup or side-panel UI, content scripts, background handlers, and shared logic distinguishable.
Keep source manifests and generated browser packages separate.
Expose narrow operations across messages instead of a generic privileged command runner.
Keep business logic testable without a browser. Isolate browser APIs behind small adapters where useful.
Do not add native messaging, broad host access, or a backend unless the feature requires it.

Content scripts share access to page content even when their JavaScript environment is isolated.
Treat the page DOM, page messages, selected text, URLs, and inserted markup as untrusted.
Isolate injected styles and clean up observers, listeners, and injected elements when the feature stops.
Support navigation and single-page updates without attaching duplicate handlers.
Avoid reading unrelated forms, credentials, or background tabs.
See [Chrome content scripts](https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts).

## Permissions and messaging security

Request only the APIs and hosts needed for the feature.
Prefer explicit activation and optional permissions where the supported browser API permits them.
Explain why access is needed at the time of the user action.
Handle denied or revoked permissions and restricted pages without failing the whole extension.
Do not default to all-site access for a feature that works on selected sites.
See [Chrome permissions](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions).

Validate message type, payload shape, size, sender identity, and sender context before privileged work.
Check the sender's expected tab, frame, URL, or extension identity as appropriate to that message contract.
An extension ID alone does not prove that page-derived data is safe.
Do not let content-script messages choose arbitrary network destinations, files, native commands, or credentials.
Keep external messaging disabled unless an explicit integration requires it.
Do not send secrets or unrelated privileged data back into page-accessible contexts.
See [Chrome message security](https://developer.chrome.com/docs/extensions/develop/concepts/messaging#security_considerations).

Use `textContent` for plain text. Sanitize intentional rich HTML using the selected language security guidance.
Keep the extension Content Security Policy restrictive. Do not weaken it to support `eval` or remote executable code.
Review web-accessible resources so internal extension files are not exposed without a need.
Apply [general security](../SECURITY_GUIDELINES.md) to clipboard, temporary storage, memory, and diagnostic collection.

## Accounts, storage, and SaaS

An installed extension is a public client. Do not embed SaaS signing secrets or service-wide provider credentials in its package.
Use the supported authentication flow and validate redirect destinations and state.
Keep authentication logic in the intended privileged context. Avoid copying tokens into content scripts or the page DOM.
The service must validate the user, tenant, resource, and operation independently of the extension.
Use the generated SDK for the configured service contract when appropriate.

Separate account and tenant state in caches, pending operations, preferences, and stored records.
Clear the relevant local state on sign-out or account changes. Reauthorize queued work before sending it.
Browser storage and synchronized extension settings are not general credential vaults.
Choose storage access levels, synchronization, retention, and deletion deliberately.
Avoid retaining page content when the operation can process it transiently.
Check background-context storage support and browser partitioning behavior.
See [Chrome storage behavior](https://developer.chrome.com/docs/extensions/develop/concepts/storage-and-cookies).

A local extension can operate without login or a backend.
If AI assists with writing or page content, also apply [AIML_SECURITY.md](../AIML_SECURITY.md).
Show what content is sent to a provider and obtain the consent required by the product's data policy.
Treat page content as untrusted instructions. It cannot authorize tool actions or transmission of unrelated information.

## Interaction and reliability

Make activation, current site access, account state, and pending work visible.
For writing assistance, preview proposed text and preserve the original selection until the user applies the result.
Recheck the destination before inserting delayed output. Avoid replacing text that changed while the request ran.
Support keyboard access and the configured host shortcuts without intercepting unrelated typing.
Use inline errors where the popup or panel provides an error surface.
Provide a persistent recovery path when a short-lived popup closes before an operation completes.

Bound messages, queued work, retries, storage, and network timeouts.
Handle offline mode, duplicate messages, worker restart, tab closure, navigation, and extension updates.
Make retries safe for service mutations. Do not repeat an operation solely because its response was lost.
Version stored data and message contracts when updates can leave older state or content scripts active.

## Testing and release

Test processing logic independently, then exercise actual extension contexts and messaging boundaries.
Test permission denial, restricted pages, malicious messages, sign-out, tenant switching, and revoked server access.
Test worker restart, navigation, offline recovery, repeated activation, and upgrades from prior stored state.
Use synthetic page content in fixtures and screenshots.
Verify the built manifest and package for every supported browser. Inspect packaged files for secrets and unused permissions.
Run browser-specific extension validation and store lint tools where available.
A passing ordinary web-page test does not validate an installed extension.

Keep unpacked installation, signed packaging, store submission, publication, and rollout separate.
Check current Chrome Web Store, Mozilla Add-ons, and Apple policies before distribution.
Keep version changes, privacy disclosures, permission changes, and release notes consistent with the actual package.
Use the configured signing and upload process. A repository merge does not authorize an extension-store release.

## Build, assets, and distribution

Use the [browser interview](../REPO.md#product-specific-browser-setup) to select browser/OS pairs and an installation channel.
Keep runtime delivery separate from API hosting. Serving pages or APIs from a backend does not install an extension.
Keep component scope under src/extensions/browser/<extension-name>/ unless existing project paths differ.

Compile TypeScript and SCSS only when they are editable source languages.
Include generated JavaScript and CSS, required HTML, icons, locale files, and referenced resources in the prepared package.
Keep executable extension code local to the package. Review the final manifest and permission set for each browser.
Store generated archives in ignored output. Keep authored manifests, build configuration, and release artwork in source control.

| Selected destination | Local verification | Distribution artifact and work |
| --- | --- | --- |
| Chrome desktop | Load a trusted unpacked build and test actual extension contexts | ZIP for Chrome Web Store, plus listing and privacy information |
| Edge desktop | Load the unpacked build in Edge and verify its supported APIs | ZIP for Microsoft Edge Add-ons through Partner Center |
| Firefox desktop or Android | Use the matching browser, web-ext, and real device tests where applicable | Mozilla-signed XPI through Add-ons or self-distribution |
| Safari on Apple platforms | Use the supported temporary-folder or app-based test flow for the selected target | Apple app packaging, signing, and the selected Apple distribution process |

Chrome's ordinary public distribution uses the Chrome Web Store.
Chrome self-hosting has platform and enterprise-policy restrictions. Do not offer a backend download as universal installation.
See [Chrome distribution](https://developer.chrome.com/docs/extensions/how-to/distribute).
Edge has its own submission and listing process. See [Edge publication](https://learn.microsoft.com/en-us/microsoft-edge/extensions/publish/publish-extension).

Firefox release distribution requires Mozilla signing, including self-distributed extensions.
Keep self-distribution installation and update instructions separate from a public Add-ons listing.
See [Mozilla signing and distribution](https://extensionworkshop.com/documentation/publish/signing-and-distribution-overview/).
Verify Android APIs and behavior separately from desktop Firefox.
See [Firefox Android development](https://extensionworkshop.com/documentation/develop/developing-extensions-for-firefox-for-android/).

Current Safari supports temporary extension-folder tests on macOS without creating an app project.
Verify that the minimum supported Safari version provides that test flow.
For app packaging, use Xcode or the Safari Web Extension Packager in App Store Connect.
The web packager can prepare builds for TestFlight and App Store submission without local Xcode.
Keep native-language scope conditional on actual wrapper-source changes.
See [Safari extension options](https://developer.apple.com/documentation/safariservices/safari-web-extensions)
and [App Store Connect packaging](https://developer.apple.com/documentation/safariservices/packaging-and-distributing-safari-web-extensions-with-app-store-connect).

For store releases, prepare actual screenshots, required icons, descriptions, support information, and privacy-policy URLs.
Check current store artwork specifications rather than copying fixed dimensions between stores.
Declare permissions and data handling accurately. Supply review access or instructions when authentication is required.
Keep developer registration, signing, upload, review, publication, and rollout separate from local compilation.
Use playbooks/<extension-name>/ for the project's exact commands, account facts, and release procedures.
