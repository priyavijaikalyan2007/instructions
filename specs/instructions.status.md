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

Updated: 16 October 2026.

The owner requested surgical edits in place and deferred file reorganization.
The accepted updates are merged into `main` from `docs/multilanguage-instructions-plan`.
The merge was a fast-forward and preserved every reviewed commit.
The review branch is retained for history.
The first commit extends language conventions within existing instruction files.
The second change folds in selected reusable lessons from apps, identity, and theme.
Existing testing thresholds remain unchanged.
No files were moved, renamed, or added during this follow-up.

The [current plan](./instructions-plan.md#current-plan-surgical-edits-in-place) defines the authorized scope.
The [review](./instructions-review.md) and [inventory](./instructions-source-inventory.md) retain the original evidence.
Their proposed file moves are superseded and must not be implemented.

The detailed follow-up completes the owner's ten requested refinements within the existing files.
It adds shared style rules, project choices and layouts, detailed examples, all 23 GoF patterns, and correlation-safe logging.

Validation passes for 115 pattern compiler/import checks, 25 behavior checks, and 15 other example checks.
Published unit-test examples pass for Python, Swift, Go, Rust, and Java.
All five HMAC helpers match the documented vector. Swift OSLog and Rust tracing examples compile.
Document checks retain existing file encodings, headers, test-first rules, and coverage thresholds.
Temporary validation tools and dependencies remain under /tmp.
Application code and test suites are outside this documentation-only change.

The public-use correction replaces private project references in AGENTS.md with self-contained architecture descriptions.
The application serves frontend routes and APIs, including pages when needed.
Truly static assets may use a CDN. Air-gapped deployments package required assets locally without external network dependencies.
The correction preserves the existing layout and shared style rules.

PR creation was blocked during review by the repository setting.
On 16 October 2026, the owner authorized a direct local merge into `main` and a push of the completed work.
This request replaces the earlier plan for the owner to merge the branch.
The direct merge completes the review workflow without a PR.
The owner authorized publishing `main` and synchronizing the retained review branch.
Document integrity and branch synchronization are checked before completion.
Keep all four source repositories read-only.
