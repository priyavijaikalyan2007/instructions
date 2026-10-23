#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: b0137fbb-0c74-4d9d-84d2-3f41f62aaec0
# Created: 2026

# COMPONENT: Terminal presentation tests
# PURPOSE: Keep terminal styling optional and captured output readable.
# RELATES: terminal_ui.py, configure_instructions.py

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'configure-instructions.sh'


class TerminalUiTests(unittest.TestCase):
    """Verify terminal modes through an actual cancelled interview."""

    def run_cli(self, *flags, env=None):
        with tempfile.TemporaryDirectory() as directory:
            environment = dict(os.environ)
            environment.pop('NO_COLOR', None)
            environment.update(env or {})
            result = subprocess.run(['bash', str(SCRIPT), '--root', directory, *flags],
                                    input='none\n4\nsrc/app/example\nyes\n3\n1\nnative application\nno\n',
                                    text=True, capture_output=True, env=environment, timeout=20)
            self.assertEqual(list(Path(directory).iterdir()), [])
            return result

    def test_forced_color_differentiates_choices_prompts_and_headings(self):
        result = self.run_cli('--color', 'always')
        self.assertEqual(result.returncode, 0, result.stderr)
        for code in ['\x1b[1;36m', '\x1b[36m', '\x1b[33m', '\x1b[0m']:
            self.assertIn(code, result.stdout)

    def test_captured_output_and_no_color_remain_plain_text(self):
        for flags, env in [((), {}), (('--color', 'never'), {}), ((), {'NO_COLOR': '1'}),
                           ((), {'TERM': 'dumb'})]:
            with self.subTest(flags=flags, env=env):
                result = self.run_cli(*flags, env=env)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn('\x1b[', result.stdout + result.stderr)
                self.assertIn('Product numbers', result.stdout)
