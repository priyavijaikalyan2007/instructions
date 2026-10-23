<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 5dc2c03a-cb40-4513-86a2-a7eeabef0d97
Created: 2026
-->

<!-- AGENT: UI-only interview navigation design and verification record. -->

# Interview navigation

The owner requested backward and forward question navigation in the UI interview only.

Add F5 Back and F6 Next to forms. Preserve drafts and accepted answers within the current session.
Back from the pre-apply review revisits the last question. Next uses the existing validation rules.
Changed earlier answers require confirmation of later answers. Rebuild conditional questions and the final plan.
Plain mode, JSON inputs, and redirected operation stay sequential.

## Design

Use a small history object with question snapshots. This follows the Memento intent without a general framework.
Keep processing in existing interview functions. Keep keyboard control and replay orchestration in the UI boundary.
Replay only cached, matching earlier answers from a fresh argument namespace before returning to the chosen question.
Match prompts, context, menus, and component scope. Retain later drafts for confirmation when their context still matches.
Never reuse final approval. Lock navigation before the first filesystem mutation.
Catch only an explicit revisit signal. Do not restart after validation, cancellation, or write failures.

Interfaces: InterviewQuestion stores a prompt, context, options, scope, accepted answer, and draft.
InterviewHistory.visit(question), accept(index, answer), and rewind(index) manage the current route.
InterviewScreen.run(callback) handles explicit revisit requests. lock_navigation() marks the write boundary.

Files: interview_question.py, interview_history.py, interview_revisit.py, curses_interview.py, terminal_ui.py,
configure_instructions.py, navigation tests, setup-tool installation, current CLI documentation, and session records.

Verification: establish the existing test baseline, reproduce missing navigation, test preserved drafts and changed branches,
verify final approval and write-once behavior, then test real ncurses navigation and run the full regression suite.

## Verification

The baseline contained 183 passing tests. Navigation and history regressions raise the suite to 195 tests.
Real ncurses trials verified F5 Back, F6 Next, preserved unfinished drafts, a changed license branch,
back from final review, rebuilt delivery facts, explicit apply, and locked navigation after writes.
The target remained absent until approval. Cancellation after backward navigation restored terminal input modes.
Existing Delete, Backspace, checkbox, resize, F3 detail, and local installation checks also passed.
The implementation remains within existing CLI and rendering boundaries. No general workflow framework was added.
