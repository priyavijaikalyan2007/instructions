#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 4638f6f4-14a2-47e9-8979-08056ccdc1e6
# Created: 2026

# COMPONENT: Interview editing behavior tests
# PURPOSE: Validate useful text editing and menu discovery independently of terminal dimensions.
# RELATES: interview_widgets.py, curses_interview.py

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from interview_widgets import TextBuffer, menu_options, prompt_default


class InterviewWidgetTests(unittest.TestCase):
    """Keep terminal key events separate from the user's literal project facts."""

    def test_delete_backspace_navigation_and_unicode_preserve_literal_text(self):
        field = TextBuffer('Priyaa')
        field.edit('backspace')
        field.edit('home')
        field.edit('delete')
        field.edit('P')
        field.edit('end')
        for key in ' café':
            field.edit(key)
        self.assertEqual(field.value, 'Priya café')
        field.edit('left')
        field.edit('backspace')
        self.assertEqual(field.value, 'Priya caé')

    def test_long_text_and_word_deletion_do_not_store_terminal_control_codes(self):
        field = TextBuffer('one two three')
        field.edit('delete-word')
        self.assertEqual(field.value, 'one two ')
        for key in ['\x1b', '\x7f', '\x00', '\t', '\n']:
            field.edit(key)
        self.assertEqual(field.value, 'one two ')
        field.edit('clear')
        for key in 'src/extensions/googleworkspace/markdown':
            field.edit(key)
        self.assertEqual(field.value, 'src/extensions/googleworkspace/markdown')

    def test_default_values_are_editable_without_inserting_prompt_labels(self):
        self.assertEqual(prompt_default('Name [example]: '), 'example')
        for prompt in ['Paths [required]: ', 'Facts [TODO]: ', 'Products [keep existing]: ', 'Choices: ', 'Version [only/later]: ']:
            self.assertEqual(prompt_default(prompt), '')

    def test_menus_include_numbered_choices_and_boolean_defaults(self):
        lines = ['Choose products:', '  1. SaaS: Webapp', '  6. CLI tools: Command-line programs']
        self.assertEqual(menu_options(lines, 'Product numbers: '), [('1', 'SaaS: Webapp'),
                                                                  ('6', 'CLI tools: Command-line programs')])
        self.assertEqual(menu_options([], 'Apply these changes? [no]: '), [('yes', 'Yes'), ('no', 'No')])
        self.assertEqual(menu_options(lines, 'Source paths [required]: '), [])
        self.assertEqual(menu_options(lines, 'Project notes [no]: '), [])
        tools = menu_options(['  1. Claude Code', 'Choose none for shared roles.'], 'Tool numbers [none]: ')
        self.assertIn(('none', 'No tool-specific assignments'), tools)

    def test_license_version_and_setup_mode_use_explicit_single_choice_menus(self):
        self.assertEqual(menu_options([], 'GPL-3.0: version policy [only/later]: '),
                         [('only', 'This version only'), ('later', 'This and later versions')])
        self.assertEqual(menu_options(['1. Initialize project', '2. Edit selections'], 'Setup mode [2]: '),
                         [('1', 'Initialize project'), ('2', 'Edit selections')])
