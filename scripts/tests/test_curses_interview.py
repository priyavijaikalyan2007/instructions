#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: eb01994e-6b06-46f4-886e-bac8ee59e098
# Created: 2026

# COMPONENT: Curses interface boundary tests
# PURPOSE: Keep automation plain and prevent forced interactive UI from mutating a non-terminal target.
# RELATES: terminal_ui.py, configure_instructions.py

from pathlib import Path
import subprocess
import importlib.util
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'configure-instructions.sh'


class CursesInterviewTests(unittest.TestCase):
    """Exercise UI mode selection through the public entry point."""

    def test_explicit_plain_mode_retains_interview_and_cancellation(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([str(SCRIPT), '--root', directory, '--ui', 'plain'],
                                    input='none\n6\nsrc/tool/example\nyes\n2\n2\nCLI binary\nno\n',
                                    text=True, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Cancelled', result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_forced_curses_requires_a_terminal_before_any_write(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([str(SCRIPT), '--root', directory, '--ui', 'curses'],
                                    input='', text=True, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 2)
            self.assertIn('terminal', result.stderr.lower())
            self.assertEqual(list(Path(directory).iterdir()), [])

    @unittest.skipUnless(sys.platform != 'win32' and importlib.util.find_spec('curses'), 'requires POSIX curses')
    def test_real_terminal_cancellation_restores_input_modes_without_writes(self):
        import fcntl
        import os
        import pty
        import struct
        import termios
        with tempfile.TemporaryDirectory() as directory:
            master, slave = pty.openpty()
            self.addCleanup(os.close, master)
            self.addCleanup(os.close, slave)
            fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 30, 100, 0, 0))
            before = termios.tcgetattr(slave)
            process = subprocess.Popen([str(SCRIPT), '--root', directory, '--ui', 'curses'],
                                       stdin=slave, stdout=slave, stderr=slave,
                                       env=dict(os.environ, TERM='xterm-256color'))
            self.addCleanup(lambda: process.kill() if process.poll() is None else None)
            self.read_until(master, process, b'Project setup')
            os.write(master, b'\x1b[17~')
            self.read_until(master, process, b'Product numbers')
            os.write(master, b'\x1b[15~')
            self.read_until(master, process, b'Tool numbers')
            os.write(master, b'\x1b')
            self.read_until(master, process, b'Cancel project setup?')
            os.write(master, b'\x1bOB\n')
            self.read_until(master, process, b'Cancelled. No files changed.')
            self.assertEqual(process.wait(timeout=5), 0)
            after = termios.tcgetattr(slave)
            # macOS sets PENDIN as kernel bookkeeping when canonical input resumes.
            before[3] &= ~getattr(termios, 'PENDIN', 0)
            after[3] &= ~getattr(termios, 'PENDIN', 0)
            self.assertEqual(after, before)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def read_until(self, descriptor, process, expected):
        """Bound real terminal waits and preserve received output as evidence when a screen fails."""
        import os
        import select
        import time
        output = bytearray()
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if select.select([descriptor], [], [], 0.05)[0]:
                output.extend(os.read(descriptor, 65536))
                if expected in output:
                    return bytes(output)
            if process.poll() is not None:
                break
        self.fail(f'Missing terminal screen {expected!r}: {output.decode(errors="replace")}')
