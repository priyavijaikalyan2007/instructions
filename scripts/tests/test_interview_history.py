#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 29b93ee7-ddce-4349-b06e-7a555abccab1
# Created: 2026

# COMPONENT: Interview history tests
# PURPOSE: Preserve drafts without trusting stale answers after earlier edits.
# RELATES: interview_history.py, interview_question.py

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from interview_history import InterviewHistory
from interview_question import InterviewQuestion


class InterviewHistoryTests(unittest.TestCase):
    """Verify navigation state independently of terminal drawing and project writes."""

    def question(self, prompt, scope='', options=()):
        return InterviewQuestion(prompt, ('Help for ' + prompt,), options, scope)

    def seed(self):
        history = InterviewHistory()
        for prompt, answer in [('First', 'one'), ('Second', 'two'), ('Third', 'three')]:
            index, _, _ = history.visit(self.question(prompt))
            history.accept(index, answer)
        return history

    def test_unchanged_answers_survive_backward_and_forward_navigation(self):
        history = self.seed()
        history.rewind(1)
        _, first, replay = history.visit(self.question('First'))
        self.assertTrue(replay)
        self.assertEqual(first.answer, 'one')
        index, second, replay = history.visit(self.question('Second'))
        self.assertFalse(replay)
        self.assertEqual(second.draft, 'two')
        history.accept(index, 'two')
        _, third, replay = history.visit(self.question('Third'))
        self.assertFalse(replay)
        self.assertEqual(third.draft, 'three')

    def test_changed_answer_requires_later_reconfirmation_but_retains_matching_drafts(self):
        history = self.seed()
        history.rewind(0)
        index, _, _ = history.visit(self.question('First'))
        history.accept(index, 'changed')
        _, second, replay = history.visit(self.question('Second'))
        self.assertFalse(replay)
        self.assertIsNone(second.answer)
        self.assertEqual(second.draft, 'two')

    def test_changed_branch_does_not_reuse_another_components_answer(self):
        history = InterviewHistory()
        index, _, _ = history.visit(self.question('Languages', 'workspace', (('1', 'JavaScript'),)))
        history.accept(index, '1')
        history.rewind(0)
        _, question, replay = history.visit(self.question('Languages', 'native', (('1', 'Swift'),)))
        self.assertFalse(replay)
        self.assertIsNone(question.draft)
        self.assertIsNone(question.answer)

    def test_unsubmitted_field_draft_survives_revisit(self):
        history = self.seed()
        history.save_draft(2, 'unfinished edit')
        history.rewind(1)
        history.visit(self.question('First'))
        history.visit(self.question('Second'))
        _, third, _ = history.visit(self.question('Third'))
        self.assertEqual(third.answer, 'three')
        self.assertEqual(third.draft, 'unfinished edit')

    def test_missing_replay_answer_opens_the_question_instead_of_skipping_it(self):
        history = InterviewHistory()
        history.visit(self.question('First'))
        history.rewind(1)
        _, question, replay = history.visit(self.question('First'))
        self.assertFalse(replay)
        self.assertIsNone(question.answer)
