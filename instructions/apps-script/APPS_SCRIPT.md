<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 45c6dd25-89c0-4c45-a287-4672dd38dd65
Created: 2026
-->

<!-- AGENT: Apps Script runtime rules layered on shared JavaScript conventions. -->

# Apps Script instructions

Read this guide for server code executed by Google Apps Script, including compiled TypeScript output.
Read [JavaScript](../javascript/JAVASCRIPT.md) for shared language conventions.
Read [TypeScript](../typescript/TYPESCRIPT.md) when TypeScript is the editable source.
An HTTP-based Workspace add-on selects its actual backend language instead of this runtime guide.
Browser code in an HTML-service sidebar follows browser JavaScript, HTML, and CSS guidance.

Use [GOOGLE_WORKSPACE.md](../google-workspace/GOOGLE_WORKSPACE.md) for host selection, manifests, authorization, packaging, testing, and distribution.
Common [style](../CODING_STYLE.md), [comments](../COMMENTING.md), [markers](../MARKERS.md), and [testing](../TESTING.md) rules still apply.
Read task sections as needed. Examples illustrate contracts rather than a complete publishable add-on.

## Runtime boundaries

Apps Script V8 is a Google-managed JavaScript runtime. It provides neither a complete browser environment nor Node.js.
Use Google services for host operations and `UrlFetchApp` for supported outbound HTTP requests.
Server code cannot assume `window`, `document`, `process`, `fetch`, or JavaScript timer APIs exist.
Uploaded Apps Script does not support ES module imports or exports.
Transform local modules through the configured build when necessary.

Private class fields, such as `#document`, and static class field declarations are unsupported in Apps Script V8.
Use ordinary fields with encapsulation conventions, closures, or functions as the design requires.
These runtime restrictions override incompatible generic JavaScript examples.
Check dependencies against [Google's V8 runtime guide](https://developers.google.com/apps-script/guides/v8-runtime).

| Execution boundary | Available facilities | Guidance |
| --- | --- | --- |
| Server Apps Script | Google services and Apps Script globals | Return explicit, serializable results to UI callbacks. |
| HTML-service browser UI | DOM, browser APIs, `google.script.run` | Treat server calls as asynchronous and validate responses. |
| Local build and tests | Configured Node.js tools and test runner | Keep development-only dependencies outside uploaded runtime code. |

Use promises where the runtime and API support them.
Google service calls remain synchronous. `Promise.all` does not make those calls run concurrently.
Do not return an unresolved promise through a callback that requires a serialized result.

## Naming and file organization

Use four spaces, no tabs, Allman braces, and a maximum of 120 characters per line.
Apply the [JavaScript grammar exceptions](../javascript/JAVASCRIPT.md) only where the grammar requires them.
Prefer named functions for host callbacks. Preserve names referenced by menus, triggers, manifests, and browser callers.

| Element | Convention | Example |
| --- | --- | --- |
| Classes and named data types | PascalCase | `WritingPreferences` |
| Public functions and methods | camelCase | `analyzeWriting` |
| Required host callbacks | Exact Google callback name | `onOpen`, `onInstall` |
| Server helpers hidden from `google.script.run` | camelCase with trailing underscore | `countWords_` |
| Parameters, locals, and properties | camelCase | `selectedText`, `wordCount` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_INPUT_CODE_UNITS` |
| Ordinary private fields | Existing non-`#` convention | `_preferences` |
| Host service names and members | Preserve the Google API spelling | `PropertiesService.getUserProperties()` |

An underscore suffix hides a function from `google.script.run`. It does not authorize callers of public functions.
See [HTML-service communication](https://developers.google.com/apps-script/guides/html/communication).

Use one top-level type per editable file, even for a short type.
Keep nested types or closely related extensions together only when that grouping makes sense.
Separate host adapters, pure processing, and browser UI code.
For a new extension, use the [Workspace component layout](../google-workspace/GOOGLE_WORKSPACE.md#recommended-source-layout).

Google stores server script files as `.gs` and HTML-service files as `.html`.
Local `.js` or `.ts` filenames depend on the configured build and upload mapping.
Keep the editable source separate from generated upload output.
Bundling can combine source files in a generated artifact without changing the editable one-type-per-file rule.
Keep required callbacks visible to Apps Script after bundling. Do not assume a module export makes a callback available.

Use JSDoc for public contracts, side effects, and expected failures.
Use ordinary comments for semantic markers. Apply the configured copyright header to editable source.
Do not put comments in `appsscript.json`, which must remain valid JSON.
The following manifest excerpt selects the runtime. It does not define a complete add-on manifest or its scopes.

```json
{
    "runtimeVersion": "V8"
}
```

## Editor callbacks and authorization

Use Editor callbacks only for an Editor add-on or a compatible document-bound script.
A card-based Workspace add-on uses its configured event handlers instead.
Keep automatic startup callbacks small. Do not send document content or perform privileged work during menu creation.

Simple triggers have authorization restrictions. Do not assume that `onOpen` can call every service available after user authorization.
Identity can also be unavailable during a trigger execution.
Installable triggers run under their creator's account, which may differ from the person who caused the event.
Web handlers have different rules. Do not apply every simple-trigger restriction to `doGet` or `doPost`.
See [simple triggers](https://developers.google.com/apps-script/guides/triggers),
[installable triggers](https://developers.google.com/apps-script/guides/triggers/installable),
and the [Editor authorization lifecycle](https://developers.google.com/workspace/add-ons/concepts/editor-auth-lifecycle).

This Google Docs Editor example creates a menu and opens a sidebar after a user action.
`Sidebar` refers to a deployed HTML-service file. Preserve that name in the build output.

```javascript
/** Create the Editor add-on menu without accessing document content. */
function onOpen(event)
{
    DocumentApp.getUi()
        .createAddonMenu()
        .addItem("Open writing assistant", "showWritingSidebar")
        .addToUi();
}

/** Initialize the menu when the Editor installation event invokes this callback. */
function onInstall(event)
{
    onOpen(event);
}

/** Open the configured sidebar after the user selects the menu item. */
function showWritingSidebar()
{
    const sidebar = HtmlService.createHtmlOutputFromFile("Sidebar")
        .setTitle("Writing assistant");
    DocumentApp.getUi().showSidebar(sidebar);
}
```

## Request contracts and pure processing

Validate each public server entry point. Browser-side validation does not protect the server.
Authorize document and account access before reading or changing Google resources.
Use the host event contract when the callback receives an event rather than an application request.
Keep text processing independent of Google services so local tests can exercise it directly.

This example accepts text explicitly supplied by the caller. It does not read or change a document.
The 20,000-code-unit bound is an illustrative application limit, not a Google quota.
The token counter counts whitespace-separated tokens. It is not a language-aware word counter.
`logAnalysisSummary_` is defined in the logging section below.

```javascript
const MAX_INPUT_CODE_UNITS = 20000;

/**
 * Analyze caller-supplied text without retaining its content.
 * @param {{text: string}} request Text to analyze.
 * @returns {{operationId: string, wordCount: number}} Safe analysis result.
 * @throws {Error} If the request does not meet the application contract.
 */
function analyzeWriting(request)
{
    validateWritingRequest_(request);
    const operationId = Utilities.getUuid();
    const wordCount = countWords_(request.text);
    logAnalysisSummary_(operationId, wordCount);
    const result =
    {
        operationId,
        wordCount
    };
    return result;
}

function validateWritingRequest_(request)
{
    if (!request || typeof request !== "object" || Array.isArray(request) ||
        typeof request.text !== "string" || request.text.length > MAX_INPUT_CODE_UNITS)
    {
        throw new Error("Enter text within the supported input limit.");
    }
}

function countWords_(text)
{
    const trimmedText = text.trim();
    return trimmedText.length === 0 ? 0 : trimmedText.split(/\s+/u).length;
}
```

For Google Docs operations, identify whether the request concerns a selection, the active tab, or the whole document.
Do not replace a missing selection with the entire document without an explicit product requirement.
Preserve text structure, formatting, and the user's current editing context when applying a change.
See [document tab handling](https://developers.google.com/apps-script/guides/docs/tabs).

## HTML-service communication

`google.script.run` calls are asynchronous. Independent requests can complete in a different order from their start order.
Use success and failure handlers. Send primitives, supported plain objects, or arrays through the boundary.
Do not return Google service objects, functions, circular structures, or `Date` objects.
See the [communication contract](https://developers.google.com/apps-script/guides/html/communication).

Wrap this callback API once when the browser component uses `async/await`.
Keep the following functions in browser-side source included by the configured HTML-service build.

```javascript
function requestWritingAnalysis(request)
{
    return new Promise(function(resolve, reject)
    {
        google.script.run
            .withSuccessHandler(resolve)
            .withFailureHandler(reject)
            .analyzeWriting(request);
    });
}

async function refreshWritingSummary(text, statusElement, submitButton)
{
    if (submitButton.disabled)
    {
        return;
    }
    submitButton.disabled = true;
    try
    {
        const result = await requestWritingAnalysis({ text });
        if (!result || !Number.isSafeInteger(result.wordCount) || result.wordCount < 0)
        {
            throw new Error("Invalid analysis response.");
        }
        statusElement.textContent = "Token count: " + result.wordCount;
    }
    catch
    {
        statusElement.textContent = "Analysis failed. Try again. Your text is unchanged.";
    }
    finally
    {
        submitButton.disabled = false;
    }
}
```

The disabled button prevents overlapping submissions through this control.
For automatic analysis, track request versions and ignore stale responses instead of blocking all edits.
Preserve user input after failure. Use inline errors where the form provides a visible error surface.
Use [literate errors](../LITERATE_ERRORS.md) and the applicable [UI guidance](../UI_UX.md) for recovery and accessibility.

## State and concurrent executions

Use [PERSISTENCE.md](../PERSISTENCE.md) when a feature stores state.
Select the property store by the intended ownership boundary.

| Store | Intended scope | Example |
| --- | --- | --- |
| Script properties | Shared script configuration | Nonsecret feature configuration |
| User properties | Current user's script preferences | Preferred writing style |
| Document properties | Shared document state where the deployment supports it | Add-on document schema version |
| Cache | Replaceable temporary results | A repeated lookup result |

Properties store strings. Validate parsed values and handle missing or unavailable stores.
Do not treat script properties as private per-user storage.
See [property stores](https://developers.google.com/apps-script/guides/properties).
Cache entries can disappear. Do not use cache as the only copy of durable state or an authorization decision.

Use a lock for a shared read-modify-write operation that concurrent executions could corrupt.
Select a script, document, or user lock according to the actual shared resource.
Keep lock ownership short and release it in `finally`.
The following example allocates a nonsecret script-wide sequence. It is not a complete idempotency or transaction system.
The one-second wait is an example application choice, not a platform requirement.

```javascript
function nextOperationSequence_()
{
    const lock = LockService.getScriptLock();
    if (!lock.tryLock(1000))
    {
        throw new Error("Another operation is active. Try again.");
    }
    try
    {
        const properties = PropertiesService.getScriptProperties();
        const previous = Number(properties.getProperty("operationSequence") || "0");
        if (!Number.isSafeInteger(previous) || previous < 0 || previous >= Number.MAX_SAFE_INTEGER)
        {
            throw new Error("The operation sequence needs repair.");
        }
        const next = previous + 1;
        properties.setProperty("operationSequence", String(next));
        return next;
    }
    finally
    {
        lock.releaseLock();
    }
}
```

Do not hold a lock during remote calls or user interaction.
An Apps Script lock does not stop a person or an external application from editing a document.
If a locked operation buffers spreadsheet writes, flush those writes before releasing the lock.
See [Lock](https://developers.google.com/apps-script/reference/lock/lock).

## Service calls and quotas

Minimize Google service round trips. Read a batch, process values locally, and write a batch when changes are required.
Use the narrowest range or document scope that satisfies the operation.
Do not read an entire mailbox, spreadsheet, or Drive tree for a small change.

This Sheets-only example reads one column once. It does not overwrite cells or formulas.
The caller must provide an authorized sheet and a positive, bounded row count.

```javascript
function countFilledLabels_(sheet, rowCount)
{
    const values = sheet.getRange(1, 1, rowCount, 1).getDisplayValues();
    return values.reduce(function(count, row)
    {
        return count + (row[0].trim().length > 0 ? 1 : 0);
    }, 0);
}
```

For writes, preserve formulas, formatting, and concurrent user changes unless the feature explicitly replaces them.
Avoid service calls inside per-cell loops.
See [Apps Script best practices](https://developers.google.com/apps-script/guides/support/best-practices).

Check current [quotas and limits](https://developers.google.com/apps-script/guides/services/quotas) for the account and service.
Keep work bounded. Handle partial progress and quota failures without silently duplicating changes.
Retry only appropriate transient failures. Bound retries and preserve idempotency before repeating a write.
Do not retry a permission failure or an invalid request as though it were a temporary outage.
For longer workflows, record progress and design explicit resumable work rather than an unbounded loop.

## Logging

Apply [LOGGING.md](../LOGGING.md), including its sensitive-data policy and approved pseudonymous identity handling.
Use Apps Script's `console` facilities through the project's logging wrapper.
Record operation IDs, safe event names, durations, and useful result counts.
Do not log document text, email bodies, access tokens, or raw host events by default.
The example logs only an operation identifier and a token count.

```javascript
function logAnalysisSummary_(operationId, wordCount)
{
    const entry =
    {
        event: "writing-analysis-complete",
        operationId,
        wordCount
    };
    console.info(JSON.stringify(entry));
}
```

Confirm which execution log or Cloud Logging destination the deployed project uses.
Do not assume a local console test proves that production logs arrive or meet retention requirements.
See [Apps Script logging](https://developers.google.com/apps-script/guides/logging).

## Security

Apply [general security](../SECURITY_GUIDELINES.md), [JavaScript security](../javascript/JAVASCRIPT.md#security),
and [secret handling](../SECRET_HANDLING.md).
Declare the minimum OAuth scopes for actual operations and review consent when those operations change.
Check authorization at the public callback boundary before accessing host resources.
Do not treat a user-supplied document ID, email address, or helper naming convention as proof of access.
See [service authorization](https://developers.google.com/apps-script/guides/services/authorization).

Treat document text, email content, host events, and remote results as untrusted input.
Render plain text with `textContent`. Sanitize permitted HTML through the established sanitizer before insertion.
Do not evaluate document text or remote code with `eval` or `Function`.
Keep credentials outside browser-delivered HTML and generated public assets.
Script properties are not a dedicated secret vault. Apply the configured secret-storage and access policy.
For AI-assisted processing, apply [AIML_SECURITY.md](../AIML_SECURITY.md) before sending content to a model or tool.
Record consent, retention, and data-transfer rules in project facts and applicable product requirements.

## Testing

Test pure processing locally through the configured JavaScript or TypeScript test runner.
Wrap Google services at host boundaries and use controlled test doubles for unit tests.
Do not invent a DOM or Node API in a server test that makes unsupported runtime code appear valid.

Cover these cases where the feature uses the corresponding behavior:

- Empty, malformed, oversized, and Unicode input.
- Denied authorization, revoked scopes, and unavailable host context.
- Safe browser rendering, callback failure, and stale response handling.
- Property-store absence, invalid stored values, lock contention, and lock release after failure.
- Quota failures, partial writes, repeated requests, and safe retries.
- Deployed callback names, manifest references, and absence of unsupported module syntax.

Run actual host tests for menus, sidebars or cards, selections, document tabs, and the relevant authorization lifecycle.
Keep local stub results separate from verified Google host behavior.
Use the [Workspace build and publication guidance](../google-workspace/GOOGLE_WORKSPACE.md#build-and-package)
for artifact inspection, test installation, account checks, and distribution gates.
