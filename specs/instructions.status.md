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

## Current phase: target guides

Implementation and local document checks are complete on `docs/target-guides` for review.
The owner authorized a new branch, push, and PR. Main remains at `0a5a868`.
Review the [target-guide comparison](https://github.com/priyavijaikalyan2007/instructions/compare/main...docs/target-guides).

AGENTS.md selects target guides for the changed work, then selects the actual languages.
Backend, frontend, SaaS, native apps, CLI tools, static websites, static assets, and SDK references have separate entry points.
A repository can combine several targets. Static sites and tools do not inherit a SaaS backend by default.
Existing instruction text is relocated. New prose provides scope and routing, not new engineering policy.

The [current plan](./instructions-plan.md#current-plan-target-guide-extraction) defines this phase.
The [review](./instructions-review.md#target-guide-extraction-on-18-october-2026) explains scope and limits.
The [inventory](./instructions-source-inventory.md#target-extraction-snapshot-on-18-october-2026) records sources and destinations.

## Verification

The extraction accounts for 89 moves and preserves all 171 code blocks across the edited documents.
Checks cover content conservation, Markdown links, old anchors, encodings, headers, target/language routes, and append-only history.
Shared style, test-first rules, and coverage thresholds remain unchanged.
One existing missing Markdown fence is closed without changing its JavaScript example.
Temporary validation artifacts remain under `/tmp/target-guide-extraction/`.
This documentation-only change has no application build or runtime test run.

The existing native material covers Apple platforms. SDKs.md was a placeholder and now indexes existing contracts and conventions.
No Android, ChromeOS, SDK generator, Kubernetes, Workers, or DNS procedures were added.
Existing conflicting recommendations remain unchanged for a separate review.

## Current phase: language guides

The language phase is complete and merged through PR #1 at `0a5a868`.
It created 13 root-level language guides and preserved all 184 GoF examples.
TypeScript also reads JavaScript. SCSS also reads CSS. LANGUAGE.md remains the natural-language writing guide.

## Previous phase

The in-place instruction updates remain merged at `7278ab3`.
The owner authorized that direct merge and push on 16 October 2026.
Application source repositories remain unchanged by the instruction extraction phases.
