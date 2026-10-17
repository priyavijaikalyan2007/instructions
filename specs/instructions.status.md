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

Updated: 17 October 2026.

## Current phase: language guides

Implementation and document checks are complete on `docs/language-guides` for review.
The commit remains local under the instruction not to push yet.
The earlier in-place updates remain merged into `main` at `7278ab3`.
The owner authorized this limited language split after reviewing that earlier phase.
Broader product/task folder reorganization remains deferred.

The new root-level guides cover C#, Swift, Go, Rust, Java, Python, JavaScript, TypeScript, HTML, CSS, SCSS, SQL, and shell scripts.
AGENTS.md selects guides from changed source and affected boundaries rather than loading every language.
TypeScript also reads JavaScript. SCSS also reads CSS.
Shared topic guides retain common policies and point to the selected language's details and examples.
LANGUAGE.md continues to govern natural-language writing.

The [current plan](./instructions-plan.md#current-plan-language-guide-extraction) defines the authorized scope.
The [review](./instructions-review.md#language-guide-extraction-on-17-october-2026) explains the extraction.
The [inventory](./instructions-source-inventory.md#language-extraction-snapshot-on-17-october-2026) records its baseline and source topics.

## Verification

All existing code blocks remain intact after normalization of outer Markdown indentation and trailing whitespace.
The coverage command block is split into three language-specific examples without changing its commands.
All 184 GoF examples remain in their matching language guides.
Existing topic paths, section anchors, source encodings, copyright headers, and append-only history remain intact.
Shared formatting rules, test-first guidance, and coverage thresholds remain unchanged.
Language dependencies and Markdown links pass checks.
The seven main shared topic guides shrink from 9,662 to 2,426 lines, a 74.9 percent reduction.

The earlier phase verified 115 pattern compiler/import checks, 25 behavior checks, and 15 other example checks.
Published unit-test and HMAC examples also passed in that phase.
This extraction preserves their code and does not claim a new application build or runtime test run.
Temporary extraction and validation scripts remain under /tmp.

## Previous phase

The owner authorized a direct merge and push on 16 October 2026 after PR creation was blocked during review.
Both local and remote branches reached `7278ab3` for that completed phase.
The public project descriptions and CDN/air-gap delivery corrections are included in that baseline.
All application source repositories remain unchanged by this phase.
