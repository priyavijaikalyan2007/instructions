<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: f7847b51-eaad-46a4-a640-8056ab58b11d
Created: 2026
-->

<!-- AGENT: Plan and verification record for extension-specific interviews and approved source-folder creation. -->

# Extension interview and bootstrap

## Plan

Replace generic browser questions with explained browser, operating-system, and distribution selections.
Record structured browser targets and distribution while retaining legacy profiles with explicit coverage warnings.
Show selected-browser build, local-test, store, asset, and signing requirements.
Keep application backends separate from installed extension packages.
Offer explained JavaScript and TypeScript presets for browser and Apps Script source.
Use CSS in the default UI preset. Keep SCSS and custom language lists available.
Preserve HTTP Workspace language selection and existing concrete project paths.

Use src/extensions/googleworkspace/<extension-name>/ and src/extensions/browser/<extension-name>/ for new extension defaults.
Keep existing paths authoritative. Do not move downstream source.
During first-time interactive setup, identify missing literal source paths explicitly as folders before approval.
Record those paths in optional Source folders metadata. JSON callers can provide source_folders explicitly.
Keep planned files and patterns distinct from folder-creation instructions.
Preview folder creation and perform it only after final apply approval.
Validate symlinks, repository boundaries, files, and planned file conflicts before any writes.
Keep dry runs, checks, cancellation, and validation errors read-only.
Create only selected folders and their parents. Do not scaffold application code or publish extensions.

No pattern required. Data tables and focused functions suffice.
The interview returns the existing component-answer shape with optional browser and source-folder fields.
Browser profile interface: interview_browser(values: dict) -> dict and validate_browser(values: dict) -> list[str].
Source folder interface: plan_source_folders(root, components, file_changes, check=False) -> list[str].
The configurator owns orchestration, validation, preview, and writes. Browser facts stay in browser_profile.py.
Shared extension source presets stay in workspace_profile.py alongside existing language normalization.
Source-folder planning stays independent of interview and deployment logic.

Files: scripts/browser_profile.py, scripts/source_folders.py, scripts/profile_interview.py,
scripts/workspace_profile.py, scripts/configure_instructions.py,
scripts/tests/test_browser_profile.py, scripts/tests/test_source_folders.py,
scripts/tests/test_workspace_profile.py, scripts/tests/test_configure_instructions.py,
scripts/tests/test_project_initialization.py, instructions/REPO.md, instructions/WORKFLOW.md,
instructions/README.md, instructions/PROJECT_PROFILE_TEMPLATE.md,
instructions/google-workspace/GOOGLE_WORKSPACE.md, instructions/browser-extensions/BROWSER_EXTENSIONS.md,
instructions/project/PROJECT.md, instructions/project/CONVERSATION.md, instructions/project/CHANGELOG.md,
agentknowledge/concepts.yaml, agentknowledge/decisions.yaml, agentknowledge/history.jsonl,
instructions/templates/repository/inherited-files.json, and this record.

## Terminal presentation

Use a shared terminal renderer for headings, choices, prompts, warnings, success, and preview diffs.
Keep the existing line-oriented interview and keyboard input. A full-screen interface is unnecessary here.
Offer --color auto, always, and never. Respect NO_COLOR and TERM=dumb in automatic mode.
Automatically retain plain text for redirected output. Apply styles to identity and license questions too.
Add scripts/terminal_ui.py and scripts/tests/test_terminal_ui.py.
Update scripts/license_selection.py and scripts/project_initialization.py to use the shared renderer.

## Verification plan

Run the 106-test baseline. Write failing public-CLI tests before implementation.
Reproduce the combined Docs and browser setup with narrow, independent source paths.
Cover browser/OS compatibility, local and store delivery, Firefox self-distribution, legacy preservation,
language presets, Safari guidance, invalid JSON, repeat edits, and generated guide selection.
Cover approved directory creation, dry runs, cancellation, planned files, wildcard rejection,
symlinks, conflicts with existing and planned files, and unselected components.
Check copied-template initialization end to end without changing the user's extensions repository.
Verify official browser distribution sources and new Markdown links.
Preserve existing code examples, source encodings, and the source repository's active profile.


## Results

The baseline was 106 passing tests. New valid browser and folder cases failed before implementation.
The complete suite now passes 127 tests, including 21 new regression tests.
Combined Docs/browser setup selects separate guides, creates approved folders, and avoids unrelated backend and SCSS scope.
Browser choices and distribution validation reject unsupported pairs and Firefox-only delivery on other browsers.
Legacy browser profiles remain readable with a specific migration warning.
Literal overlapping extension scopes receive a narrowing warning. Intentional shared source remains allowed.

Folder creation covers first interactive setup and copied-template initialization.
Dry runs and cancellation leave files and directories untouched.
Checks are read-only and detect missing configured folders.
Planned files remain absent. Unselected components create no source folder.
Preflight rejects symlinks, repository escapes, unmatched patterns, out-of-scope creation, and file conflicts.
Repeat edits preserve selected browser facts and project-owned notes.

Forced terminal colors differentiate headings, choices, prompts, defaults, and preview output.
Captured output, --color never, NO_COLOR, and TERM=dumb remain plain text in automatic mode.
Identity and licensing use the same renderer. No full-screen or third-party dependency was added.
Four pseudo-terminal smoke runs verified automatic colors, NO_COLOR, TERM=dumb, and --color never.
Each run exercised actual menus, folder previews, and cancellation without filesystem changes.

Current official Chrome, Mozilla, Microsoft, and Apple documentation supports release guidance.
Safari guidance includes temporary macOS folder tests and App Store Connect packaging alongside Xcode.
Local links and anchors pass. Four extension-layout/path examples changed intentionally.
Other existing code blocks remain preserved. Existing CP1252 documents remain byte-identical.
The source profile check and dry run pass without changing the active AGENTS.md block.
Six core modules pass Python 3.10 grammar, four-space indentation, 120-character lines, and 30-line function limits.
These tests validate local setup and routing. They do not claim browser-host or store-release verification.
