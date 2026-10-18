<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 5484def9-0307-4c48-b717-4579374090b1
Created: 2026
-->

<!-- AGENT: Current scope, verification, and next action for the shared instruction updates. -->

# Instruction repository status

Updated: 18 October 2026.

## Current phase: subject consolidation

The approved follow-up is implemented, verified, and pushed on `docs/target-guides` for [PR #2](https://github.com/priyavijaikalyan2007/instructions/pull/2).
Main remains unchanged while the owner reviews the PR.

AGENTS.md selects shared repository work, target, shared concern, and language independently.
REPO.md holds common commands and session workflow. PERSISTENCE.md holds storage integrity and configured database examples.
UI_UX.md combines general interaction guidance. UI_UX_COMPONENTS.md keeps detailed profiles separately selectable.
KEYBOARD.md remains the browser shortcut registry, scoped by focus and platform.
The old catch-all and two old UI/UX guides are retired. Their lessons and links have canonical homes.
PERFORMANCE.md shrinks from 198 to 44 lines. The consolidation removes 92 redirect-only sections across affected guides.

The [approved plan](./instructions-plan.md#approved-follow-up-consolidate-subject-guides) defines the scope.
The [review](./instructions-review.md#approved-consolidation-on-18-october-2026) records scope and overlap resolutions.
The [inventory](./instructions-source-inventory.md#approved-subject-consolidation-snapshot) records source provenance.

## Verification

All 551 parsed code blocks are preserved, including ten examples from the supplied UI source.
All 26 source sections are imported. Instruction-line checks account for moved and adapted material.
Local links, incoming references, source encodings, copyright headers, new GUIDs, and append-only history pass checks.
Shared style, the operating workflow, test-first rules, and coverage thresholds remain unchanged.
The supplied UI source remains unchanged. Public instructions do not require that private file.
This documentation-only change has no application build or runtime test run.
Temporary validation artifacts remain under `/tmp/target-guide-consolidation/`.

## Current phase: language guides

The language phase is complete and merged through PR #1 at `0a5a868`.
It created 13 root-level language guides and preserved all 184 GoF examples.
TypeScript also reads JavaScript. SCSS also reads CSS. LANGUAGE.md remains the natural-language writing guide.

## Previous phase

The in-place instruction updates remain merged at `7278ab3`.
The owner authorized that direct merge and push on 16 October 2026.
Application source repositories remain unchanged by the instruction extraction phases.

## PR review follow-up

The owner approved the proposed cleanup and requested removal of empty performance sections.
That approved follow-up is implemented above. The earlier project-specific EF snapshot mandate remains removed.
