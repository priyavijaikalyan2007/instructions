<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 734d8f6e-edba-4c0b-a50c-d936ef807daf
Created: 2026
-->

<!-- AGENT: Design and validation record for initializing repositories copied from this library. -->

# Project initialization

## Design

Add an explicit --initialize-project mode to the existing profile configurator.
Keep the source repository's README, contribution policy, conduct policy, security policy, and LICENSE unchanged.
Ask for project identity and license choices before the existing product interview.
Use --project-answers for reproducible identity and licensing input, separate from existing --answers profile input.
Support --dry-run, final cancellation, and repeat runs without overwriting project-owned files.
Replace only known inherited files. Back up those originals before replacement or removal.
Preserve customized files and report them. Reject conflicting license destinations before applying any changes.
Reset known inherited project facts and profile choices. Remove only known inherited maintenance and knowledge records.
Record initialization state so later runs preserve edits and do not silently relicense a project.
Preserve the original instruction-library MIT license independently of the project's selected terms.
Bundle exact license texts and provenance for offline use. Never generate legal terms from a language model.
Use SPDX identifiers, exact GNU versions and only/or-later choices, and explicit OR for alternative licenses.
Keep optional Creative Commons terms scoped to project content. Keep custom or undecided terms visibly pending.

No pattern required - simple functions suffice.
The CLI handles interaction and file application. Separate functions validate choices and build document plans.
No network request or Git mutation occurs during project initialization.

## Interfaces and files

- scripts/configure_instructions.py: CLI flags, initialization integration, preview and deletion preflight.
- scripts/project_initialization.py: identity validation, inherited-file detection, document and backup plans.
- scripts/license_selection.py: explained license interview, validation, exact text installation and scope notices.
- scripts/tests/test_project_initialization.py: public CLI and clone-preservation tests.
- scripts/tests/test_license_selection.py: catalog integrity, exact variants, OR expressions, and content scope tests.
- instructions/templates/repository/: editable policy templates, known inherited hashes, bundled license texts and sources.
- instructions/REPO.md: initialization commands, input schema, scope and preservation rules.
- instructions/README.md: initialization discovery.
- instructions/project/CONVERSATION.md, CHANGELOG.md, PROJECT.md: request, outcome, and facts.
- instructions/maintenance/project-initialization-review.md, instructions.status.md: design and verification.
- agentknowledge/concepts.yaml, decisions.yaml, history.jsonl: module ownership and append-only task record.

Public flags: --initialize-project and --project-answers PATH.
Project answers contain name, owner, repository_url, description, year, and license choices.
License choices contain software identifiers, optional content identifier and paths, and optional pending custom terms.
Plans map repository-relative paths to bytes or None for a verified inherited-file removal.

## Baseline

All 55 existing tests pass before implementation.

## Implementation details and verification

The implementation also changes scripts/profile_interview.py to identify the source repository by its Git origin.
The new scripts/update_template_baseline.py maintains recognized source-file hashes after reviewed source changes.
Existing path validation is shared through project_initialization.py rather than duplicated.
The generic README_TEMPLATE.md remains unchanged. The specialized generator template supplies output-specific policy links.
Policy TODOs defer unknown reporting contacts, contribution terms, and support promises without inventing facts.

New integration tests failed before implementation. The full suite now has 77 passing tests.
Tests cover copied-script execution, identity, exact inherited cleanup, customized-file preservation, and source-repository protection.
They also cover dry runs, cancellation, repeated setup, changed-license rejection, symlinks, backup conflicts, and existing license aliases.
Custom context paths and generated Markdown links are verified. GNU variants, LGPL companion terms, OR choices, and content scope are verified.
All bundled license bytes match pinned SPDX source checksums. Runtime initialization uses no network calls.
The source policies and root LICENSE are byte-identical to the main-branch baseline.
The actual utilextensions repository was not accessed or modified.

Initialization does not decide legal compatibility with project dependencies or create custom commercial terms.
The script applies explicit choices to new project material and preserves third-party and file-specific notices.
File replacement is atomic per file. The full multi-file operation is not transactional across filesystem failures.
Backups are written first. The completion record is written last.

Delivery: commit locally on feat/project-initialization. No push or merge was requested for this update.

Final checks: no new Markdown link defects or preservation discrepancies.
The active source profile passes --check, and --dry-run reports no changes.
Python 3.10 syntax, shell syntax, source line/function limits, and Git whitespace checks pass.

The SSPL source contains trailing whitespace. A license-folder .gitattributes preserves exact upstream bytes and disables only those whitespace checks.
