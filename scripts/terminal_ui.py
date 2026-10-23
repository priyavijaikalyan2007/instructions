#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: e8666472-1d8a-42e9-974a-d2f3519f0f70
# Created: 2026

# COMPONENT: Line-oriented terminal presentation
# PURPOSE: Distinguish interview roles while preserving readable plain-text automation.
# RELATES: configure_instructions.py, profile_interview.py, license_selection.py
# FLOW: Existing text -> semantic style -> optional ANSI rendering -> terminal stream.

import builtins
import os
import re
import sys


COLOR_MODE = 'auto'
ACTIVE_SCREEN = None
RESET = '\033[0m'
STYLES = {'heading': '\033[1;36m', 'choice': '\033[36m', 'prompt': '\033[1m',
          'warning': '\033[33m', 'success': '\033[32m', 'added': '\033[32m', 'removed': '\033[31m'}


def set_color_mode(mode: str) -> None:
    """Set the explicit CLI mode before the interview starts."""
    global COLOR_MODE
    COLOR_MODE = mode


def color_enabled(stream) -> bool:
    """Keep redirected output and terminals requesting plain text free of escape sequences."""
    if COLOR_MODE != 'auto':
        return COLOR_MODE == 'always'
    return ('NO_COLOR' not in os.environ and os.environ.get('TERM') != 'dumb'
            and bool(getattr(stream, 'isatty', lambda: False)()))


def styled(text: str, role: str, stream=None) -> str:
    """Apply one semantic color without changing the underlying words."""
    if not color_enabled(stream or sys.stdout):
        return text
    return STYLES[role] + text + RESET


def line_role(text: str) -> str:
    """Recognize existing line-oriented headings, menu choices, status, and diff lines."""
    if re.match(r'^\s+\d+\.', text):
        return 'choice'
    warnings = ('Invalid value:', 'Note:', 'Configuration error:', 'These source paths', 'Cancelled',
                'Preserve customized',
                'Choose one of the displayed', 'Enter an actual', 'Re-enter', 'Include JavaScript',
                'Self-distributed signed XPI packages are a Firefox choice')
    if text.startswith(warnings):
        return 'warning'
    if text.startswith(('Applied ', 'Profile check passed', 'No changes.')):
        return 'success'
    if text.startswith('+'):
        return 'added'
    if text.startswith('-') and not text.startswith('- '):
        return 'removed'
    if text.endswith(':') or text.startswith(('Component:', 'Configuring repository:', 'Create source folder')):
        return 'heading'
    return ''


def print(*values, **kwargs) -> None:
    """Style terminal lines while preserving print's separator, destination, and newline behavior."""
    stream = kwargs.get('file') or sys.stdout
    separator = kwargs.pop('sep', ' ')
    text = separator.join(str(value) for value in values)
    if ACTIVE_SCREEN is not None:
        ACTIVE_SCREEN.write(text)
        return
    lines = text.splitlines(keepends=True)
    rendered = ''.join(styled(line, role, stream) if (role := line_role(line.rstrip())) else line for line in lines)
    builtins.print(rendered, **kwargs)


def input(prompt: str = '') -> str:
    """Highlight the prompt and its current default without requiring cursor control."""
    if ACTIVE_SCREEN is not None:
        return ACTIVE_SCREEN.ask(prompt)
    text = re.sub(r'\[[^\]]*\]', lambda match: styled(match.group(), 'warning'), prompt)
    return builtins.input(styled(text, 'prompt'))


def present_preview(summary: list[str], details: list[str]) -> bool:
    """Use a readable primary review in forms while preserving plain CLI diffs."""
    if ACTIVE_SCREEN is None:
        return False
    ACTIVE_SCREEN.pending = []
    ACTIVE_SCREEN.details = details
    ACTIVE_SCREEN.write('\n'.join(summary))
    return True


def lock_navigation() -> None:
    """Prevent UI replay once an approved operation can create, replace, or remove files."""
    if ACTIVE_SCREEN is not None:
        ACTIVE_SCREEN.navigation_locked = True


def interactive_requested(args) -> bool:
    """Use forms only when this invocation can ask a person for identity, selections, or approval."""
    if args.check:
        return False
    interview = not args.answers and (not args.dry_run or bool(args.target_folder))
    confirmation = not args.dry_run and not args.apply
    return bool(args.configure_agents or interview or confirmation)


def run_plain(callback):
    """Retain stream-friendly output and optional line editing when forms are unavailable."""
    if sys.stdin.isatty():
        try:
            import readline  # noqa: F401 - importing enables Python input's platform line editor.
        except ImportError:
            pass
    return callback()


def run_interview_ui(callback, mode: str, interactive: bool):
    """Select ncurses for interactive terminals and retain plain output for automation."""
    terminal = sys.stdin.isatty() and sys.stdout.isatty() and os.environ.get('TERM') != 'dumb'
    if not interactive or mode == 'plain':
        return run_plain(callback)
    if not terminal:
        if mode == 'curses':
            raise ValueError('The curses interview requires an interactive terminal. Use --ui plain for streams.')
        return run_plain(callback)
    try:
        import curses
        curses.setupterm()
    except Exception as error:
        if mode == 'curses':
            raise ValueError('The curses interface is unavailable. Use --ui plain or a Python with curses.') from error
        return run_plain(callback)
    return run_curses(callback, curses)


def run_curses(callback, curses):
    """Restore terminal state on every exit and never repeat an operation after a callback failure."""
    from curses_interview import InterviewScreen
    global ACTIVE_SCREEN
    session = None

    def execute(screen):
        nonlocal session
        global ACTIVE_SCREEN
        session = InterviewScreen(screen, color_enabled(sys.stdout))
        ACTIVE_SCREEN = session
        try:
            return session.run(callback)
        finally:
            ACTIVE_SCREEN = None

    result = curses.wrapper(execute)
    builtins.print(session.summary())
    return result
