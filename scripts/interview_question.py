#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: eaa16801-3b2c-422b-8ab1-7b56db67ad6e
# Created: 2026

# COMPONENT: Interview question snapshot
# PURPOSE: Keep question identity and editable answers within one UI session.
# RELATES: curses_interview.py, terminal_ui.py

from dataclasses import dataclass


@dataclass
class InterviewQuestion:
    """Capture one route-specific question without storing input beyond the running process."""

    prompt: str
    context: tuple[str, ...]
    options: tuple[tuple[str, str], ...]
    scope: str
    answer: str | None = None
    draft: str | None = None

    @property
    def key(self) -> tuple:
        """Match the question, its component, and its available choices before reusing an answer."""
        return self.prompt, self.context, self.options, self.scope
