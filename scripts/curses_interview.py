#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 192b6a48-fb70-4a6e-9ca0-71ce4aa58ef3
# Created: 2026

# COMPONENT: Curses project interview
# PURPOSE: Present editable fields, selectable choices, scrollable help, and a review before approval.
# RELATES: terminal_ui.py, interview_widgets.py, interview_cancelled.py
# FLOW: Buffered interview messages -> form -> existing answer contract -> preview -> confirmation.
# SECURITY: Keep terminal control keys out of answers. Cancel before writes and restore the terminal via wrapper.

import curses
import re
import textwrap

from interview_cancelled import InterviewCancelled
from interview_widgets import TextBuffer, menu_options, prompt_default


class InterviewScreen:
    """Render the existing interview as terminal forms while keeping its processing outside the UI."""

    def __init__(self, screen, colors: bool = True):
        """Enable ncurses key decoding and retain the complete session for on-screen review."""
        self.screen = screen
        self.lines, self.pending, self.previous_context, self.cached_menu = [], [], [], []
        self.step, self.scroll, self.menu_prompt = 0, 0, ''
        self.colors = colors and curses.has_colors()
        screen.keypad(True)
        if self.colors:
            curses.use_default_colors()
            for number, color in enumerate([curses.COLOR_CYAN, curses.COLOR_YELLOW,
                                             curses.COLOR_GREEN, curses.COLOR_RED], 1):
                curses.init_pair(number, color, -1)
        curses.set_escdelay(100)

    def write(self, text: str) -> None:
        """Buffer output rather than mixing ordinary print calls with the active curses screen."""
        lines = re.sub(r'\x1b\[[0-9;]*m', '', text).splitlines()
        self.lines.extend(lines)
        self.pending.extend(lines)

    def put(self, row: int, column: int, text: str, style: int = 0) -> None:
        """Clip to the current screen and tolerate a resize between measuring and drawing."""
        rows, columns = self.screen.getmaxyx()
        if 0 <= row < rows and 0 <= column < columns - 1:
            try:
                self.screen.addnstr(row, column, text, columns - column - 1, style)
            except curses.error:
                pass

    def style(self, line: str) -> int:
        """Distinguish guidance, warnings, and diff changes without requiring color."""
        if not self.colors:
            return curses.A_NORMAL
        number = 2 if line.startswith(('Note:', 'TODO', 'Preserve', 'Configuration error', 'Invalid value:')) else 1
        if line.startswith('+'):
            number = 3
        elif line.startswith('-') and not line.startswith('- '):
            number = 4
        return curses.color_pair(number)

    def dimensions_ready(self) -> bool:
        """Wait for usable dimensions without discarding the current answer on resize."""
        rows, columns = self.screen.getmaxyx()
        if rows >= 18 and columns >= 60:
            return True
        self.screen.erase()
        self.put(0, 0, 'Resize to at least 60 columns and 18 rows. Esc cancels setup.')
        self.screen.refresh()
        if self.screen.get_wch() == '\x1b':
            raise InterviewCancelled()
        return False

    def wrapped(self, lines: list[str]) -> list[str]:
        """Wrap long explanations and paths while retaining every line for scrolling."""
        width = max(1, self.screen.getmaxyx()[1] - 4)
        return [part for line in lines for part in (textwrap.wrap(line.expandtabs(4), width) or [''])]

    def heading(self, title: str) -> None:
        """Draw the common screen title and rule."""
        self.screen.erase()
        self.put(0, 1, title, curses.A_BOLD | self.style('Heading'))
        self.put(1, 1, '-' * (self.screen.getmaxyx()[1] - 3))

    def review(self, title: str, lines: list[str]) -> None:
        """Show the complete explanation or change preview before returning to the current form."""
        offset = 0
        while True:
            if not self.dimensions_ready():
                continue
            self.heading(title)
            rows, _ = self.screen.getmaxyx()
            wrapped = self.wrapped(lines)
            height = rows - 5
            offset = max(0, min(offset, max(0, len(wrapped) - height)))
            for index, line in enumerate(wrapped[offset:offset + height], 2):
                self.put(index, 2, line, self.style(line))
            self.put(rows - 2, 1, 'Up/Down or PgUp/PgDn scroll | Home/End | Enter returns | Esc returns')
            self.screen.refresh()
            key = self.screen.get_wch()
            if key in {'\n', '\r', '\x1b', curses.KEY_ENTER}:
                return
            offset = self.review_offset(key, offset, height, len(wrapped))

    def review_offset(self, key, offset: int, height: int, length: int) -> int:
        """Handle review navigation without treating keystrokes as project input."""
        changes = {curses.KEY_UP: -1, curses.KEY_DOWN: 1, curses.KEY_PPAGE: -height, curses.KEY_NPAGE: height}
        if key == curses.KEY_HOME:
            return 0
        if key == curses.KEY_END:
            return length
        return offset + changes.get(key, 0)

    def confirm_cancel(self) -> None:
        """Require an explicit choice before discarding a long, unwritten interview."""
        cancel = False
        while True:
            self.heading('Cancel project setup?')
            self.put(3, 2, 'No setup changes have been applied. Discard this interview?')
            self.put(5, 2, '[ Keep editing ]' if not cancel else '  Keep editing  ')
            self.put(6, 2, '[ Cancel setup ]' if cancel else '  Cancel setup  ')
            self.put(8, 2, 'Up/Down select | Enter confirms | Esc keeps editing')
            self.screen.refresh()
            key = self.screen.get_wch()
            if key == '\x1b':
                return
            if key in {curses.KEY_UP, curses.KEY_DOWN, '\t', ' '}:
                cancel = not cancel
            if key in {'\n', '\r', curses.KEY_ENTER}:
                if cancel:
                    raise InterviewCancelled()
                return

    def form_context(self, prompt: str) -> tuple[list[str], list[tuple[str, str]]]:
        """Use the current step's guidance and retain the role menu for consecutive tool assignments."""
        context = self.pending or self.previous_context
        options = menu_options(self.pending, prompt)
        if not options and (prompt == self.menu_prompt or 'role numbers' in prompt):
            options = self.cached_menu
        if options:
            self.cached_menu, self.menu_prompt = options, prompt
        self.previous_context, self.pending = context, []
        return context, options

    def draw_form(self, prompt: str, context: list[str], options: list, field: TextBuffer, selected: int) -> None:
        """Lay out a scrolling explanation, choice list, editable field, and keyboard controls."""
        self.heading(f'Project setup | Question {self.step}')
        rows, _ = self.screen.getmaxyx()
        title = self.wrapped([prompt])[:3]
        for index, line in enumerate(title, 2):
            self.put(index, 2, line, curses.A_BOLD)
        start = 3 + len(title)
        content = self.wrapped([line for line in context if not re.match(r'^\s+\d+\.', line)])
        height = max(1, min(7, (rows - start - 8) // 2)) if options else max(1, rows - start - 8)
        self.scroll = max(0, min(self.scroll, max(0, len(content) - height)))
        for index, line in enumerate(content[self.scroll:self.scroll + height], start):
            self.put(index, 2, line, self.style(line))
        self.draw_options(options, field, selected, start + height + 1, rows - 7)
        self.put(rows - 3, 1, 'Enter next | Up/Down choices | Space select | Left/Right edit | Ctrl+U clear')
        self.put(rows - 2, 1, 'PgUp/PgDn help | F2 full review | Home/End edit | Esc cancel')
        self.draw_field(field, rows)
        self.screen.refresh()

    def draw_options(self, options: list, field: TextBuffer, selected: int, start: int, stop: int) -> None:
        """Keep the highlighted choice visible when a menu exceeds the available screen height."""
        height = max(1, stop - start)
        offset = max(0, selected - height + 1)
        chosen = {item.strip() for item in field.value.split(',')}
        for index, (value, label) in enumerate(options[offset:offset + height], offset):
            marker = '[x]' if value in chosen else '[ ]'
            style = curses.A_REVERSE if index == selected else curses.A_NORMAL
            self.put(start + index - offset, 2, f'{marker} {value or "keep"}. {label}', style)

    def draw_field(self, field: TextBuffer, rows: int) -> None:
        """Scroll long answers horizontally while preserving the complete field value."""
        columns = self.screen.getmaxyx()[1]
        width = max(1, columns - 6)
        offset = max(0, field.cursor - width + 1)
        self.put(rows - 6, 1, '+' + '-' * (columns - 4) + '+')
        self.put(rows - 5, 1, '| ' + field.value[offset:offset + width].ljust(width) + ' |')
        self.put(rows - 4, 1, '+' + '-' * (columns - 4) + '+')
        try:
            self.screen.move(rows - 5, min(columns - 2, 3 + field.cursor - offset))
        except curses.error:
            pass

    def toggle_choice(self, field: TextBuffer, value: str, multiple: bool) -> TextBuffer:
        """Support checkbox lists, exclusive pending/none choices, and single-choice menus."""
        if not multiple:
            return TextBuffer(value)
        selected = [part.strip() for part in field.value.split(',') if part.strip()]
        if value in {'none', '', '0'}:
            return TextBuffer(value)
        selected = [part for part in selected if part not in {'none', '0'}]
        selected.remove(value) if value in selected else selected.append(value)
        return TextBuffer(','.join(selected))

    def edit_key(self, key, field: TextBuffer) -> None:
        """Normalize ncurses navigation keys and common terminal erase characters."""
        keys = {curses.KEY_LEFT: 'left', curses.KEY_RIGHT: 'right', curses.KEY_HOME: 'home',
                curses.KEY_END: 'end', curses.KEY_BACKSPACE: 'backspace', curses.KEY_DC: 'delete',
                '\x7f': 'backspace', '\b': 'backspace', '\x01': 'home', '\x05': 'end',
                '\x15': 'clear', '\x17': 'delete-word'}
        if key in keys:
            field.edit(keys[key])
        elif isinstance(key, str):
            field.edit(key)

    def ask(self, prompt: str) -> str:
        """Present one editable question and return only its literal answer to existing validation."""
        self.step, self.scroll = self.step + 1, 0
        context, options = self.form_context(prompt)
        field = TextBuffer(prompt_default(prompt))
        selected = next((index for index, (value, _) in enumerate(options) if value == field.value), 0)
        multiple = bool(re.search(r'\bnumbers\b', prompt, re.I))
        if prompt.startswith('Apply these changes?'):
            self.review('Review planned changes | Enter continues to approval', context)
        while True:
            if not self.dimensions_ready():
                continue
            self.draw_form(prompt, context, options, field, selected)
            key = self.screen.get_wch()
            if key in {'\n', '\r', curses.KEY_ENTER}:
                answer = field.value or (options[selected][0] if options and not multiple else '')
                self.lines.append(prompt + answer)
                return answer
            selected, field = self.form_key(key, options, field, selected, multiple)

    def form_key(self, key, options: list, field: TextBuffer, selected: int,
                 multiple: bool) -> tuple[int, TextBuffer]:
        """Route choice navigation, help, and editing without executing or storing terminal control sequences."""
        if key == '\x1b':
            self.confirm_cancel()
        elif key == curses.KEY_F2:
            self.review('Interview review | Enter returns to the current answer', self.lines)
        elif key in {curses.KEY_PPAGE, curses.KEY_NPAGE}:
            self.scroll += -5 if key == curses.KEY_PPAGE else 5
        elif options and key in {curses.KEY_UP, curses.KEY_DOWN}:
            selected = (selected + (-1 if key == curses.KEY_UP else 1)) % len(options)
            if not multiple:
                field = TextBuffer(options[selected][0])
        elif options and key == ' ':
            field = self.toggle_choice(field, options[selected][0], multiple)
        else:
            self.edit_key(key, field)
        return selected, field

    def finish(self) -> None:
        """Keep the result and completion instructions available until the user closes the interface."""
        self.review('Setup result | Enter closes the interface', self.pending or self.lines)

    def summary(self) -> str:
        """Leave a concise result in the normal terminal after curses restores the screen."""
        prefixes = ('Applied ', 'Cancelled.', 'No changes.', 'Profile check passed.')
        return next((line for line in reversed(self.lines) if line.startswith(prefixes)),
                    'Preview complete. No apply operation was reported.')
