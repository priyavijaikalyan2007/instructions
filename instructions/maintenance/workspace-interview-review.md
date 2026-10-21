<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 658d1fd0-2f67-440f-b360-735f68ba5368
Created: 2026
-->

<!-- AGENT: Plan and validation record for product-specific Workspace setup. -->

# Workspace interview correction

## Plan

Replace generic Workspace platform and delivery questions with explained, compatible choices.
Collect current hosts, Editor or Workspace model, Apps Script or HTTP runtime, account context, and distribution.
Explain build output, host UI assets, test installation, and Marketplace preparation for those choices.
Keep possible future hosts outside active selections. Retain existing custom profile notes.
Permit explicitly planned literal source paths without creating directories or weakening existing-path checks.
Normalize JavaScript/TypeScript input so both language guides enter scope.

No pattern required - simple functions suffice.
The interview returns component field updates. Validation remains independent of terminal interaction.
The configurator owns preview and writes. New Workspace code performs no network or deployment actions.

Files: scripts/workspace_profile.py, scripts/profile_interview.py, scripts/configure_instructions.py,
scripts/tests/test_workspace_profile.py, scripts/tests/test_configure_instructions.py,
scripts/tests/test_project_initialization.py,
instructions/google-workspace/GOOGLE_WORKSPACE.md, instructions/REPO.md,
instructions/PROJECT_PROFILE_TEMPLATE.md, instructions/WORKFLOW.md,
instructions/project/CONVERSATION.md, instructions/project/CHANGELOG.md, instructions/project/PROJECT.md,
agentknowledge/concepts.yaml, agentknowledge/decisions.yaml, agentknowledge/history.jsonl,
this record, and instructions/templates/repository/inherited-files.json.

Interfaces: interview_workspace(values: dict) -> dict and validate_workspace(values: dict) -> list[str].
Optional profile fields record Workspace model, runtime, account, and distribution.
An optional Source state field accepts existing or planned. Omission retains existing-path validation.
Legacy Workspace profiles remain readable and report missing structured setup choices for review.

## Validation plan

The baseline has 77 passing tests. Add failing CLI tests before implementation.
Cover Docs Editor setup on absent paths, Gmail cards, HTTP runtime, private/public/test delivery,
incompatible host/runtime choices, JSON validation, retained defaults, dry run, cancellation, and safe paths.
Check generated scope links and source-library policy preservation. No live Google deployment is in scope.


## Implementation and validation

New CLI tests reproduced the missing-path failure and generic interview behavior before implementation.
The Workspace interview now records typed choices and explains matching build and release work.
JavaScript-only cards skip TypeScript compilation. CSS-only Editor UI skips SCSS compilation.
The full copied-repository interview covers initialization, MIT selection, Docs Editor setup, and absent source paths.
Legacy profiles remain readable. Existing notes and unchanged defaults survive later edits.
Unsafe paths, symlinks, missing existing paths, invalid host/runtime combinations, and invalid private distribution fail before writes.
Source state applies to every component type. Missing literal paths require explicit planned scope.
The source repository's policies and LICENSE remain unchanged. The user's extensions repository remains untouched.
No live Google host build, installation, verification, or publication was performed.

All 96 tests pass. The source profile check passes, and its dry run reports no changes.
Markdown link and preservation checks report no new defects.
Python 3.10 syntax, function size, line length, shell syntax, and Git whitespace checks pass.
The inherited-file baseline is current. Commit locally without pushing.
