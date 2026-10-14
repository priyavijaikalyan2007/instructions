<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 5484def9-0307-4c48-b717-4579374090b1
Created: 2026
-->

<!-- AGENT: Current state and next action for the instruction repository reorganization. -->

# Instruction repository status

Updated: 14 October 2026.

The review and migration proposal are complete and await owner review.
The branch is `docs/multilanguage-instructions-plan`.
The draft PR contains planning documents only.
Existing instruction policy remains unchanged.

The [review](./instructions-review.md) records findings and reusable lessons from the three working repositories.
The [plan](./instructions-plan.md) defines scope, file changes, routing, tests, compatibility, and owner decisions.
The [inventory](./instructions-source-inventory.md) records source snapshots and migration destinations.

After owner review, implement the agreed structure on this branch and update the draft PR.
Do not treat proposed policy changes as approved instructions.
Refresh source hashes before implementation because the working repositories contain local changes.
Keep those repositories read-only during this shared-repository change.
