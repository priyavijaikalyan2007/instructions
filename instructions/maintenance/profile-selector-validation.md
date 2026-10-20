<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: d57dba49-335e-43c0-944a-378e49ee4602
Created: 2026
-->

<!-- AGENT: Evidence and limits for directory cleanup, reading trees, and the profile configurator. -->

# Profile selector validation

Validated on 20 October 2026 against merged main 9f16499.
The review branch is docs/instructions-directory. The owner merges the review PR.

## Directory and reading maps

The relocation accounts for 101 existing files.
Only AGENTS.md, CLAUDE.md, CODEX.md, and GEMINI.md remain as root Markdown files.
Root AGENTS.md routes to the full shared workflow under instructions/.
Repository policies and the GitHub landing README live under .github/.
LICENSE and NOTICE remain root legal metadata.
All former specs instruction records now live under instructions/maintenance/.
The root specs path remains reserved for actual product and repository specifications.

The author README contains the shared baseline and all five requested scenario trees.
Conditional leaves distinguish actual languages, changed concerns, optional native clients, and generated SDK boundaries.
The GitHub landing README links directly to those trees.

The baseline comparison preserves all 559 original parsed Markdown code blocks, per-file content, and order.
Ten new blocks contain six reading trees and four CLI or JSON usage examples.
Source encodings, moved GUIDs, reference binaries, existing script code, and historical input prefixes remain preserved.
Shared workflow comparison allows relocated references and removed trailing whitespace. Its policy wording remains unchanged.
The document check introduces no new Markdown link defects.
The 108 existing defects primarily reference external component distribution paths absent from this instructions checkout.
Those defects remain outside this change.

## Executed checks

| Check | Result |
| --- | --- |
| `python3 -m unittest discover -s scripts/tests -v` | All 35 tests pass |
| `./scripts/configure-instructions.sh --check` | Current repo profile passes |
| `./scripts/configure-instructions.sh --dry-run` | No changes |
| `bash -n scripts/configure-instructions.sh` | Pass |
| `/bin/bash scripts/configure-instructions.sh --check` | Pass |
| Python 3.10 grammar parse | Pass |
| New Python source line lengths, tabs, and function sizes | Pass |
| `git diff main --check` | Pass |

The runtime test environment uses Python 3.15.0 and Bash 5.3.20 on macOS.
Python 3.10 compatibility was checked through grammar parsing, not execution under a second interpreter.
The script requires no third-party Python packages, network access, Git commands, or application dependencies.
No common build.sh or test.sh exists in this repository.

## Test coverage by behavior

The tests invoke the public Bash entry point in isolated temporary repositories.
Tests were written and observed failing before implementation or correction.
The suite checks these behaviors:

- Initialize a standalone native profile and install missing guides and root entries.
- Preserve project facts, local refinements, installed guides, custom component notes, and root text outside the managed block.
- Preserve existing project-file encodings and profile line endings.
- Support custom project-file paths, partial JSON updates, repeated identical input, and the actual interactive interview.
- Keep previews, checks, cancelled confirmation, and rejected inputs free of writes.
- Reject unknown fields, duplicate identifiers, unresolved enabled values, empty lists, missing sources, and missing selected guides.
- Reject missing or disabled SDK references used by an enabled client.
- Reject malformed root routing, traversal, symlink destinations, project-file aliases, and directory/file conflicts.
- Report unsupported language and platform coverage while retaining the selected actual language.
- Select the expected guide names for standalone native, native SaaS, Java SaaS/frontend, static website, and Rust CLI scenarios.

The scenario checks validate profile routing output, not an application's source, build, or runtime behavior.
The previous fresh-context reviews remain recorded in [project-profile-validation.md](project-profile-validation.md).
No new fresh-context agent review is claimed for the selector implementation.

## Limits

Enabled source paths must already exist. The selector does not generate application directories or scaffolding.
The selector lists enabled target/language guides. Agents still narrow that set to the task and select shared concerns.
Scoped legacy-example checkboxes remain manual choices and are preserved by the interview.
Missing platform guidance remains a reported coverage gap.
Existing generic guides remain unchanged during setup. Generic updates require a separate reviewed operation.
Checks verify selected target/language guide files, not every transitive instruction link or project fact.
UTF-8 is required for the editable profile and root AGENTS document. Existing project facts and refinements retain their bytes.
File replacements are atomic individually. A filesystem failure can interrupt a multi-file apply.
Inspect a failed apply before retrying. The selector does not promise rollback across multiple files.

## Follow-up: product-category interview

PR #3 merged at 4312353 before this correction.
The owner found component identifiers, source paths, and target choices opaque.
The revised interview uses the six requested categories: SaaS, SaaS with Native Clients, Microservice,
Native App, Static Website, and CLI tools.
SaaS composition and generated SDK relationships are derived from those choices rather than presented as peer implementation targets.
Compatible categories combine in one repository. Existing profiles can retain their exact enabled scopes and relationships.

All 44 integration tests pass after the revised tests were observed failing before implementation.
The follow-up checks each category, combined SaaS/website/CLI selection, prompt explanations, local component names,
unchanged defaults, overlapping-choice recovery, and the native SaaS-to-standalone transition.
Switching to standalone native clears its prior SaaS SDK relationship, so disabled SDK references do not block the new profile.
Accepting equivalent defaults preserves existing field bytes, including inline-code formatting.
The original JSON/manual configuration contracts, dry-run semantics, validation, and write boundaries remain unchanged.
The six-category interview replaces the earlier component-by-component enable questions.
Advanced custom component additions and specialized SDK links remain available through manual edits and JSON input.

The current repository passes --check. Its --dry-run reports No changes.
Bash syntax, Python 3.10 grammar, source style, and diff whitespace checks pass.
No application source or release operation is part of this correction.
