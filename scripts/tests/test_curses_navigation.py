#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 1aa9b804-faa4-40b7-adad-a270b297a3fe
# Created: 2026

# COMPONENT: Curses question navigation tests
# PURPOSE: Exercise real field editing and replay without terminal drawing or project writes.
# RELATES: curses_interview.py, terminal_ui.py, configure_instructions.py

import argparse
import curses
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from curses_interview import InterviewScreen
import terminal_ui


class CursesNavigationTests(unittest.TestCase):
    """Verify Back, Next, changed branches, fresh approval, and write boundaries."""

    def session(self, keys):
        screen = Mock()
        screen.getmaxyx.return_value = (30, 100)
        screen.get_wch.side_effect = keys
        with patch('curses_interview.curses.set_escdelay'):
            session = InterviewScreen(screen, False)
        session.draw_form = Mock()
        session.finish = Mock()
        return session

    def run_session(self, session, callback):
        with patch.object(terminal_ui, 'ACTIVE_SCREEN', session):
            return session.run(callback)

    def test_back_and_next_keep_unsubmitted_edits(self):
        keys = [curses.KEY_F6, '\x15', *'draft', curses.KEY_F5, curses.KEY_F6, curses.KEY_F6]
        session = self.session(keys)
        def interview():
            first = terminal_ui.input('First [one]: ')
            second = terminal_ui.input('Second [two]: ')
            return first, second
        self.assertEqual(self.run_session(session, interview), ('one', 'draft'))
        self.assertEqual(session.history.questions[1].draft, 'draft')

    def test_changing_product_rebuilds_conditional_questions(self):
        keys = [curses.KEY_F6, curses.KEY_F6, curses.KEY_F5, curses.KEY_F5,
                '\x15', *'native', curses.KEY_F6, curses.KEY_F6, curses.KEY_F6]
        session = self.session(keys)
        def interview():
            product = terminal_ui.input('Product [web]: ')
            language = terminal_ui.input('Web language [TypeScript]: ' if product == 'web'
                                         else 'Native language [Swift]: ')
            delivery = terminal_ui.input('Delivery [container]: ' if product == 'web' else 'Delivery [app]: ')
            return product, language, delivery
        self.assertEqual(self.run_session(session, interview), ('native', 'Swift', 'app'))
        self.assertNotIn('TypeScript', [question.answer for question in session.history.questions])

    def test_back_from_final_review_requires_fresh_approval_and_writes_once(self):
        keys = [curses.KEY_F6, curses.KEY_F5, '\x15', *'new', curses.KEY_F6,
                curses.KEY_F6, '\x15', *'yes', curses.KEY_F6]
        session = self.session(keys)
        written = []
        def interview():
            name = terminal_ui.input('Name [old]: ')
            terminal_ui.print('Review project ' + name)
            if terminal_ui.input('Apply these changes? [no]: ') == 'yes':
                terminal_ui.lock_navigation()
                written.append(name)
            return name
        self.assertEqual(self.run_session(session, interview), 'new')
        self.assertEqual(written, ['new'])
        self.assertTrue(session.navigation_locked)
        session.navigate_back()
        self.assertTrue(session.navigation_locked)

    def test_callback_failure_is_not_retried(self):
        session = self.session([])
        def fail():
            terminal_ui.lock_navigation()
            raise OSError('Write failed')
        callback = Mock(side_effect=fail)
        with self.assertRaises(OSError):
            self.run_session(session, callback)
        callback.assert_called_once()
        self.assertTrue(session.navigation_locked)

    def test_read_only_result_can_return_to_the_last_answer(self):
        session = self.session([curses.KEY_F6, curses.KEY_F6, curses.KEY_F5,
                                '\x15', *'edited', curses.KEY_F6, '\n'])
        session.finish = InterviewScreen.finish.__get__(session)
        answers = []
        def interview():
            first = terminal_ui.input('First [one]: ')
            second = terminal_ui.input('Second [two]: ')
            answers.append((first, second))
            return second
        self.assertEqual(self.run_session(session, interview), 'edited')
        self.assertEqual(answers, [('one', 'two'), ('one', 'edited')])

    def test_next_keeps_existing_input_validation(self):
        session = self.session(['\x15', *'bad', curses.KEY_F6, '\x15', *'2027', curses.KEY_F6,
                                curses.KEY_F5, '\x15', *'2028', curses.KEY_F6, curses.KEY_F6])
        invalid = []
        def interview():
            while True:
                year = terminal_ui.input('Year [2026]: ')
                if year.isdigit():
                    break
                invalid.append(year)
                terminal_ui.print('Invalid value: enter a year.')
            terminal_ui.input('Purpose [Tool]: ')
            return year
        self.assertEqual(self.run_session(session, interview), '2028')
        self.assertTrue(invalid)

    def test_replay_starts_with_fresh_command_arguments(self):
        import configure_instructions as configurator
        args = argparse.Namespace(color='never', ui='auto', check=False, answers=None, dry_run=False,
                                  apply=False, configure_agents=False, target_folder=None, initialize_project=False)
        observed = []
        def configure(current):
            observed.append(current.initialize_project)
            current.initialize_project = True
            return 0
        def rerun(callback, *unused):
            callback()
            return callback()
        with patch.object(configurator, 'arguments', return_value=args), \
                patch.object(configurator, 'configure_project', side_effect=configure), \
                patch.object(configurator, 'run_interview_ui', side_effect=rerun):
            self.assertEqual(configurator.main(), 0)
        self.assertEqual(observed, [False, False])

    def test_platform_edit_rebuilds_language_checkboxes_before_accepting_answers(self):
        from profile_choices import select_languages, select_platforms
        keys = ['1', curses.KEY_F6, '1', curses.KEY_F6, curses.KEY_F5, curses.KEY_F5,
                '\x15', '4', curses.KEY_F6, '1', curses.KEY_F6, curses.KEY_F6]
        session = self.session(keys)
        def interview():
            platforms = select_platforms('apps', '')
            languages = select_languages('apps', platforms, '')
            terminal_ui.input('Delivery [native application]: ')
            return platforms, languages
        self.assertEqual(self.run_session(session, interview), (['Android'], ['Java']))
        options = session.history.questions[1].options
        self.assertIn(('1', 'Java'), options)
        self.assertNotIn(('1', 'Swift'), options)
