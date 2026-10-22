#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: e9f6f841-0fac-45d0-8d65-a69ce71f054b
# Created: 2026

# COMPONENT: Setup review presentation tests
# PURPOSE: Keep end-user summaries readable and exact changes available separately.
# RELATES: setup_review.py, curses_interview.py, terminal_ui.py

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from setup_review import summary_lines, detail_lines


class SetupReviewTests(unittest.TestCase):
    """Verify that summaries explain scope and preserve optional exact change inspection."""

    def test_review_groups_installed_files_and_explains_selected_scope(self):
        profile = ("## Components\n\n### writer\n- [x] Enabled\n"
                   "- Targets: browser-extensions\n- Languages: TypeScript, HTML\n"
                   "- Source paths: `src/extensions/browser/writer`\n- Deployment: Chrome Web Store\n"
                   "## Agent roles\n| Tool | Roles | Notes |\n| --- | --- | --- |\n"
                   "| codex | implementation, review | Check API boundaries. |\n")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'PROJECT.md').write_text('Owner facts.\n')
            changes = {'PROJECT.md': b'Updated facts.\n', 'PROJECT_PROFILE.md': profile.encode(),
                       'instructions/typescript/TYPESCRIPT.md': b'Shared guidance.\n',
                       'configure.sh': b'entry', 'scripts/tool.py': b'tool'}
            lines = summary_lines(root, changes, ['src/extensions/browser/writer'], profile)
            text = '\n'.join(lines)
            for expected in ['writer', 'TypeScript', 'Chrome Web Store', 'codex', 'implementation, review',
                             'Update PROJECT.md', '1 shared instruction files', 'F3']:
                self.assertIn(expected, text)
            self.assertNotIn('@@', text)
            self.assertNotIn('+++', text)
            details = '\n'.join(detail_lines(root, changes))
            self.assertIn('-Owner facts.', details)
            self.assertIn('+Updated facts.', details)

    def test_removed_files_and_no_changes_are_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertIn('No changes.', summary_lines(root, {}, [], ''))
            lines = summary_lines(root, {'old.md': None}, [], '')
            self.assertIn('Remove inherited old.md', lines)

    def test_forms_keep_exact_changes_optional_and_results_readable(self):
        from curses_interview import InterviewScreen
        import terminal_ui
        screen = InterviewScreen.__new__(InterviewScreen)
        screen.lines, screen.pending, screen.details = [], ['Previous question'], []
        screen.review = Mock()
        with patch.object(terminal_ui, 'ACTIVE_SCREEN', screen):
            self.assertTrue(terminal_ui.present_preview(['Create PROJECT.md'], ['@@ diff @@', '+facts']))
            self.assertEqual(screen.pending, ['Create PROJECT.md'])
            self.assertEqual(screen.details, ['@@ diff @@', '+facts'])
            screen.pending = []
            terminal_ui.print('Applied 1 file changes and created 0 source folders.')
            terminal_ui.print('Next steps: complete PROJECT.md and SETUP.md.')
            screen.finish()
        result = '\n'.join(screen.review.call_args.args[1])
        self.assertIn('Applied', result)
        self.assertIn('Next steps', result)
        self.assertNotIn('@@', result)
