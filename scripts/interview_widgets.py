#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 2ce39063-3941-46d7-b77d-376210bcbdc4
# Created: 2026

# COMPONENT: Interview field and menu values
# PURPOSE: Edit literal Unicode answers without recording terminal key sequences.
# RELATES: curses_interview.py, terminal_ui.py
# FLOW: Normalized key -> text edit or choice -> existing interview validation.

import re


def prompt_default(prompt: str) -> str:
    """Extract an editable default while excluding labels that require an actual answer."""
    match = re.search(r'\[([^\]]*)\]:?\s*$', prompt)
    value = match.group(1) if match else ''
    labels = {'required', 'keep existing', 'unspecified', 'only/later'}
    return '' if value.startswith('TODO') or value in labels else value


def menu_options(lines: list[str], prompt: str) -> list[tuple[str, str]]:
    """Recognize existing numbered menus and yes/no questions without changing their validation contract."""
    if '[only/later]' in prompt:
        return [('only', 'This version only'), ('later', 'This and later versions')]
    if '?' in prompt and prompt_default(prompt) in {'yes', 'no'}:
        return [('yes', 'Yes'), ('no', 'No')]
    if not (re.search(r'\bnumbers?\b', prompt, re.I) or 'source languages' in prompt.lower()
            or prompt.startswith(('Content license', 'Setup mode'))):
        return []
    result = [(match.group(1), match.group(2)) for line in lines
              if (match := re.match(r'^\s*(\d+)\.\s+(.+)$', line))]
    if result and prompt.startswith('Tool numbers'):
        result.append(('none', 'No tool-specific assignments'))
    if result and 'keep existing' in prompt:
        result.append(('', 'Keep current product components'))
    return result


class TextBuffer:
    """Store one editable answer and cursor. Control keys are operations rather than answer content."""

    def __init__(self, value: str = ''):
        """Start at the end of the current value, ready to accept or edit the default."""
        self.value = value
        self.cursor = len(value)

    def edit(self, key: str) -> None:
        """Apply a normalized navigation or deletion key, or insert one printable Unicode character."""
        moves = {'home': 0, 'end': len(self.value), 'left': max(0, self.cursor - 1),
                 'right': min(len(self.value), self.cursor + 1)}
        if key in moves:
            self.cursor = moves[key]
        elif key == 'clear':
            self.value, self.cursor = '', 0
        elif key == 'backspace' and self.cursor:
            self.value = self.value[:self.cursor - 1] + self.value[self.cursor:]
            self.cursor -= 1
        elif key == 'delete':
            self.value = self.value[:self.cursor] + self.value[self.cursor + 1:]
        elif key == 'delete-word':
            prefix = re.sub(r'\S+\s*$', '', self.value[:self.cursor])
            self.value, self.cursor = prefix + self.value[self.cursor:], len(prefix)
        elif len(key) == 1 and key.isprintable() and len(self.value) < 2000:
            self.value = self.value[:self.cursor] + key + self.value[self.cursor:]
            self.cursor += 1
