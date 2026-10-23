#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 9039dbf7-c1dd-41f5-9948-ac1a955780bc
# Created: 2026

# COMPONENT: Interview revisit signal
# PURPOSE: Request UI replay before the filesystem write boundary.
# RELATES: curses_interview.py, terminal_ui.py

class InterviewRevisit(Exception):
    """Carry an explicit UI navigation destination without restarting on unrelated failures."""

    def __init__(self, index: int):
        """Identify the visited question to edit."""
        super().__init__(index)
        self.index = index
