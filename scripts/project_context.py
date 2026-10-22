#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: ae37c6cf-bad4-4628-9223-64efe0988653
# Created: 2026

# COMPONENT: Project business facts
# PURPOSE: Collect optional context without treating unknown facts as instructions.
# RELATES: project_initialization.py, instructions/templates/repository/PROJECT.md
# FLOW: Optional interview or JSON -> validated facts -> project-owned documents.

from terminal_ui import input, print


CONTEXT_FIELDS = {'users': 'Intended users', 'problem': 'Problem this project solves',
                  'value': 'Expected user or business value', 'scope': 'Initial product scope',
                  'success_criteria': 'Success criteria', 'constraints': 'Known constraints or exclusions'}


def validate_context(value: dict) -> dict:
    """Accept only named, single-line facts that are safe to place in Markdown tables."""
    if not isinstance(value, dict) or set(value) - CONTEXT_FIELDS.keys():
        raise ValueError('business_context supports users, problem, value, scope, success_criteria, and constraints.')
    for key, text in value.items():
        if (not isinstance(text, str) or len(text) > 1000
                or any(ord(char) < 32 or char in '`<>|\\' for char in text)):
            raise ValueError(f'business_context.{key} must be one line without Markdown delimiters.')
    return {key: text.strip() for key, text in value.items()}


def ask_context_field(key: str, label: str) -> str:
    """Correct an invalid fact in place rather than discarding the rest of the business interview."""
    default = ''
    while True:
        answer = input(f'{label} [{default or "TODO"}]: ').strip() or default
        try:
            return validate_context({key: answer})[key]
        except ValueError as error:
            print(f'Invalid value: {error}')
            default = answer


def interview_context() -> dict:
    """Explain optional facts and retain unanswered questions as visible completion work."""
    print('\nDescribe the business context for PROJECT.md:')
    print('These are project facts, not coding instructions. Press Enter to leave an answer as a TODO.')
    return {key: ask_context_field(key, label) for key, label in CONTEXT_FIELDS.items()}


def context_values(identity: dict) -> dict:
    """Provide explicit placeholders for missing facts without inventing a product strategy."""
    context = identity.get('business_context', {})
    return {key: context.get(key) or 'TODO: ' + label for key, label in CONTEXT_FIELDS.items()}
