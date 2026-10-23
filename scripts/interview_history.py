#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 30519b98-7945-424c-aac4-a7d93dad634a
# Created: 2026

# COMPONENT: Interview question history
# PURPOSE: Preserve session drafts and require fresh confirmation after earlier edits.
# RELATES: curses_interview.py, terminal_ui.py

from interview_question import InterviewQuestion


class InterviewHistory:
    """Manage a visited question route and matching drafts without filesystem side effects."""

    def __init__(self):
        """Start with no saved answers or replay permission."""
        self.questions: list[InterviewQuestion] = []
        self.drafts: dict[tuple, str] = {}
        self.position, self.replay_until = 0, 0

    def visit(self, question: InterviewQuestion) -> tuple[int, InterviewQuestion, bool]:
        """Return a matching snapshot and replay only accepted questions before the chosen destination."""
        index = self.position
        self.position += 1
        if index < len(self.questions) and self.questions[index].key == question.key:
            question = self.questions[index]
        else:
            del self.questions[index:]
            question.draft = self.drafts.get(question.key)
            self.questions.append(question)
            self.replay_until = min(self.replay_until, index)
        replay = index < self.replay_until and question.answer is not None
        if not replay:
            self.replay_until = min(self.replay_until, index)
        return index, question, replay

    def accept(self, index: int, answer: str) -> None:
        """Invalidate later accepted answers after an edit while retaining matching drafts for confirmation."""
        question = self.questions[index]
        if question.answer is not None and question.answer != answer:
            del self.questions[index + 1:]
        question.answer = answer
        self.save_draft(index, answer)

    def save_draft(self, index: int, value: str) -> None:
        """Preserve an unfinished field without treating it as a validated answer."""
        question = self.questions[index]
        question.draft = value
        self.drafts[question.key] = value

    def rewind(self, index: int) -> None:
        """Replay earlier accepted answers until the requested visited question becomes editable."""
        if not 0 <= index <= len(self.questions):
            raise ValueError('Choose a question already visited in this interview.')
        self.position, self.replay_until = 0, index
