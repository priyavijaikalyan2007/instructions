<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: b2075088-9db4-41a0-b4a2-3e8323432921
Created: 2026
-->

<!-- AGENT: Design and verification record for Apps Script runtime guidance and profile routing. -->

# Apps Script guidance

## Plan

Add instructions/apps-script/APPS_SCRIPT.md as runtime guidance layered on the shared JavaScript conventions.
Keep Workspace product, host, build, and distribution guidance in GOOGLE_WORKSPACE.md.
Document supported syntax, file organization, callbacks, authorization, service boundaries, state, quotas, logging, and tests.
Include concrete examples for Editor callbacks, pure processing, sidebar communication, batching, properties, and locks.
Keep HTML-service browser APIs separate from server-side Apps Script APIs.
Verify changing platform facts against official Google documentation.

Select the guide for explicit Apps Script language values and for the apps-script Workspace runtime.
Do not select it for ordinary JavaScript or TypeScript HTTP services.
Retain existing profile compatibility and guide-preservation behavior.

No pattern required - simple functions suffice.
The selector derives guide names from validated metadata. It does not execute JavaScript or call Google services.
Interface: workspace_runtime_guides(values: dict) -> set[str], called for Workspace components after validation.
The answer-document shape remains unchanged.

Files: instructions/apps-script/APPS_SCRIPT.md, scripts/configure_instructions.py,
scripts/tests/test_workspace_profile.py, instructions/google-workspace/GOOGLE_WORKSPACE.md,
instructions/javascript/JAVASCRIPT.md, instructions/WORKFLOW.md, instructions/README.md,
instructions/REPO.md, instructions/SECURITY_GUIDELINES.md, instructions/LOGGING.md,
instructions/project/CONVERSATION.md, instructions/project/CHANGELOG.md, instructions/project/PROJECT.md,
agentknowledge/decisions.yaml, agentknowledge/history.jsonl,
instructions/templates/repository/inherited-files.json, and this record.

## Verification plan

The baseline is 101 passing tests. Add failing CLI routing tests before implementation.
Cover JavaScript and TypeScript Apps Script runtimes, explicit Apps Script aliases, HTTP exclusion,
missing selected guides, runtime changes, and installed-guide preservation.
Check syntax and deterministic example behavior locally with Node and controlled Google API stubs.
Local stubs do not verify real Google authorization, quotas, deployment, or host integration.
Check all new links and preserve existing examples and encoding.


## Results

All 106 selector tests pass. New routing tests failed before implementation.
Apps Script runtimes select the guide for JavaScript and TypeScript source. Explicit language aliases also select it.
HTTP JavaScript excludes the runtime guide. Missing selected guides fail the check.
Switching to HTTP preserves the installed guide while removing its managed scope link.
The active source-repository profile check and dry run pass without changing AGENTS.md.
Changed Python files parse with Python 3.10 grammar.

All six JavaScript example blocks parse. The manifest excerpt parses as JSON.
Code samples use four spaces, no tabs, at most 120 characters per line, and functions below 30 lines.
Controlled Node host stubs verify Editor callbacks, input validation, token counts, safe summary logs,
batched Sheets reads, property sequences, lock contention, release after failure, and sidebar success and failure paths.
These checks do not claim real Apps Script runtime compatibility, host authorization, deployment, or quota verification.

Local Markdown links and anchors pass. Existing code blocks remain unchanged except the Workspace reading-tree update.
Both existing CP1252 documents remain byte-identical.
The guide links official Google documentation for changing platform facts.
No Google account, application source, deployment, or downstream repository was changed.
