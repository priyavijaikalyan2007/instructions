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
    warnings = ('Note:', 'Configuration error:', 'These source paths', 'Cancelled', 'Preserve customized',
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
    lines = text.splitlines(keepends=True)
    rendered = ''.join(styled(line, role, stream) if (role := line_role(line.rstrip())) else line for line in lines)
    builtins.print(rendered, **kwargs)


def input(prompt: str = '') -> str:
    """Highlight the prompt and its current default without requiring cursor control."""
    text = re.sub(r'\[[^\]]*\]', lambda match: styled(match.group(), 'warning'), prompt)
    return builtins.input(styled(text, 'prompt'))
