<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 67e23e41-5420-47f3-baee-febb4536654b
Created: 2026
-->

<!-- AGENT: Scope, validation, and publication record for extension profile support. -->

# Extension profiles

## Plan

Add independent Google Workspace and browser extension targets without enabling Microsoft Office guidance.
Keep choices 1 through 6 stable. Add choice 7 for Google Workspace and choice 8 for browser extensions.
Use existing profile fields for host applications, browsers, actual languages, source paths, and deployment facts.
Ask whether each extension consumes this repository's SaaS API when a SaaS category is selected.
Keep standalone extensions independent of backend, native app, or static website implementation.
Retain the current JSON and Markdown contracts. Existing unselected guides remain installed.

No pattern required - simple functions suffice.
The public CLI flags do not change. New target values are google-workspace and browser-extensions.
The interview owns presentation and product selection. The configurator owns validation and guide routing.
Use existing SDK relationship validation rather than creating a separate extension integration model.

## Files

- instructions/google-workspace/GOOGLE_WORKSPACE.md
- instructions/browser-extensions/BROWSER_EXTENSIONS.md
- scripts/profile_interview.py
- scripts/configure_instructions.py
- scripts/tests/test_configure_instructions.py
- instructions/PROJECT_PROFILE_TEMPLATE.md
- instructions/WORKFLOW.md
- instructions/README.md
- instructions/REPO.md
- instructions/saas/SAAS.md
- instructions/project/PROJECT.md
- instructions/project/CONVERSATION.md
- instructions/project/CHANGELOG.md
- instructions/maintenance/instructions.status.md
- instructions/maintenance/extension-profiles-review.md
- agentknowledge/concepts.yaml
- agentknowledge/history.jsonl

## Baseline and validation

All 50 existing tests passed before changes.
New interview, routing, SaaS relationship, cancellation, and dry-run checks failed before implementation.
Primary sources are linked from the new guides. Product requirements and deployment details remain project-owned.
All 55 tests pass, including standalone extensions, SaaS integration, cancellation, JSON preview, and missing-guide checks.
A regression test also confirms that accepting an existing profile does not link an intentionally unlinked SDK.
The active repository passes --check. Its --dry-run reports no changes.
Shell syntax, Python 3.10 syntax compatibility, and git diff whitespace checks pass.
Link, heading, header, and example checks report no new defects against the recorded baseline.
Existing unrelated link defects remain documented in scoped-guides-security-review.md.
No browser or Workspace extension was installed or executed. No marketplace publication was attempted.

## Publication scope

The owner explicitly authorized committing, pushing, and merging both this change and the pending guide/security reorganization.
Use a pull request for the combined review branch, then synchronize local main with the merged remote revision.
Git history and the merged pull request provide the final delivery record.
