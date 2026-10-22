#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 04d5762d-cb60-4610-a40c-7608e8f21d9a
# Created: 2026

# COMPONENT: Interview cancellation
# PURPOSE: Distinguish an explicit pre-apply cancellation from invalid input or filesystem errors.
# RELATES: curses_interview.py, configure_instructions.py


class InterviewCancelled(Exception):
    """Signal an explicit cancellation while the interview still holds an unwritten change plan."""
