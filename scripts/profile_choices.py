#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: b21b7845-784c-4682-a12b-9c457bd7e893
# Created: 2026

# COMPONENT: Supported profile choices
# PURPOSE: Select known platforms and source languages through context-specific numbered menus.
# RELATES: profile_interview.py, workspace_profile.py, browser_profile.py, configure_instructions.py
# FLOW: Component role -> platforms -> relevant languages -> existing profile answer contract.

import re

from terminal_ui import input, print


# Canonical guide lookup also serves JSON validation and generated routing.
LANGUAGE_GUIDES = {
    'c#': ['csharp/CSHARP.md'], 'swift': ['swift/SWIFT.md'], 'go': ['go/GO.md'], 'rust': ['rust/RUST.md'],
    'java': ['java/JAVA.md'], 'python': ['python/PYTHON.md'], 'javascript': ['javascript/JAVASCRIPT.md'],
    'typescript': ['typescript/TYPESCRIPT.md', 'javascript/JAVASCRIPT.md'], 'html': ['html/HTML.md'],
    'css': ['css/CSS.md'], 'scss': ['scss/SCSS.md', 'css/CSS.md'], 'sql': ['sql/SQL.md'],
    'shell': ['shell/SHELL.md'], 'bash': ['shell/SHELL.md'],
    'apps script': ['javascript/JAVASCRIPT.md', 'apps-script/APPS_SCRIPT.md'],
    'google apps script': ['javascript/JAVASCRIPT.md', 'apps-script/APPS_SCRIPT.md'],
}
SCRIPT_LANGUAGES = ['JavaScript', 'TypeScript']
WEB_LANGUAGES = SCRIPT_LANGUAGES + ['HTML', 'CSS', 'SCSS']
SERVICE_LANGUAGES = ['C#', 'Java', 'Go', 'Rust', 'Python', 'JavaScript', 'TypeScript', 'SQL', 'Shell']
TOOL_LANGUAGES = ['Python', 'Go', 'Rust', 'C#', 'Java', 'JavaScript', 'TypeScript', 'Shell']
SDK_LANGUAGES = ['C#', 'Java', 'Go', 'Python', 'Rust']
APPLE_PLATFORMS = {'iOS', 'iPadOS', 'macOS'}
PLATFORMS = {
    'apps': ['iOS', 'iPadOS', 'macOS', 'Android', 'ChromeOS'],
    'tools': ['macOS', 'Linux', 'Windows'],
    'sdks': ['browser', 'iOS', 'iPadOS', 'macOS', 'Android', 'ChromeOS', 'Linux', 'Windows', 'server'],
}
FIXED_PLATFORMS = {'backend': 'server', 'frontend': 'browser', 'websites': 'browser',
                   'static-assets': 'browser', 'documentation': 'none'}


def language_values(value: str) -> list[str]:
    """Preserve the existing JSON parser's JavaScript aliases and unrelated literal language names."""
    aliases = {'js': 'JavaScript', 'javascript': 'JavaScript', 'ts': 'TypeScript', 'typescript': 'TypeScript'}
    result = []
    for item in value.split(','):
        item = item.strip().strip('`').strip()
        parts = re.split(r'\s*/\s*', item)
        parts = parts if all(part.lower() in aliases for part in parts) else [item]
        for part in parts:
            name = aliases.get(part.lower(), part)
            if name and name not in result:
                result.append(name)
    return result


def choose_many(label: str, options: list[str], defaults: list[str], multiple: bool = True) -> list[str]:
    """Require listed numbers in plain mode and expose the same options as curses checkboxes."""
    print('\n' + label + ':')
    for number, option in enumerate(options, 1):
        print(f'  {number}. {option}')
    default = ','.join(str(options.index(value) + 1) for value in defaults if value in options)
    while True:
        kind = 'numbers' if multiple else 'number'
        answer = input(f'{label} {kind} [{default or "required"}]: ').strip() or default
        numbers = [value.strip() for value in answer.split(',')]
        valid = all(value.isdigit() and 1 <= int(value) <= len(options) for value in numbers)
        if valid and (multiple or len(numbers) == 1):
            return list(dict.fromkeys(options[int(value) - 1] for value in numbers))
        print('Choose the displayed numbers. Select only targets that you will test now.')


def select_supported(label: str, options: list[str], current: list[str], fallback: list[str]) -> list[str]:
    """Retain unlisted existing facts explicitly rather than dropping them or accepting arbitrary new values."""
    options = list(options)
    current = [value for value in current if value and '<' not in value]
    keep = 'Keep existing selection: ' + ', '.join(current)
    defaults = current or fallback
    if set(current) - set(options):
        print('Some existing values are outside this menu. Keep them explicitly or choose replacements.')
        options.append(keep)
        defaults = [keep]
    while True:
        selected = choose_many(label, options, defaults)
        if keep not in selected:
            return selected
        if len(selected) == 1:
            return current
        print('Select Keep existing alone, or select replacement values from the list.')


def select_platforms(role: str, current: str) -> list[str]:
    """Collect consumer platforms before choosing native, tool, or generated-client languages."""
    existing = [value.strip().strip('`') for value in current.split(',') if value.strip()]
    if role in FIXED_PLATFORMS:
        result = existing if existing and '<' not in current else [FIXED_PLATFORMS[role]]
        print('Platform retained: ' + ', '.join(result))
        return result
    options = PLATFORMS.get(role, PLATFORMS['sdks'])
    names = {value.lower(): value for value in options}
    existing = [names.get(value.lower(), value) for value in existing]
    print('\nChoose the operating systems or consumer platforms for this component.')
    if role == 'apps':
        print('Detailed native app guidance covers Apple platforms. Android and ChromeOS have partial coverage.')
    return select_supported('Target platforms', options, existing, [])


def language_options(role: str, platforms: list[str]) -> list[str]:
    """Limit new selections to supported languages relevant to the component and its consumers."""
    selected = set(platforms)
    if role == 'apps':
        native = (['Swift'] if selected & APPLE_PLATFORMS else [])
        native += ['Java'] if selected & {'Android', 'ChromeOS'} else []
        return native + WEB_LANGUAGES
    if role == 'tools':
        return TOOL_LANGUAGES + (['Swift'] if selected & {'macOS', 'Linux'} else [])
    if role == 'sdks':
        return (['Swift'] if selected & APPLE_PLATFORMS else []) + SCRIPT_LANGUAGES + SDK_LANGUAGES
    if role == 'backend':
        return SERVICE_LANGUAGES
    if role in {'frontend', 'websites', 'static-assets', 'workspace-html', 'browser-extensions'}:
        return WEB_LANGUAGES
    if role == 'workspace-cards':
        return SCRIPT_LANGUAGES
    return ['C#', 'Swift', 'Go', 'Rust', 'Java', 'Python', *WEB_LANGUAGES, 'SQL', 'Shell', 'Apps Script']


def select_languages(role: str, platforms: list[str], current: str) -> list[str]:
    """Offer actual source languages, not runtime output, and retain explicit prior selections."""
    current = '' if '<' in current else current
    options = language_options(role, platforms)
    names = {value.lower(): value for value in options}
    names['bash'] = 'Shell'
    existing = [names.get(value.lower(), value) for value in language_values(current)]
    print('\nSelect actual source languages used in this component. Choose only files inside its source scope.')
    print('Select separate website or frontend components for their own source paths.')
    print('Selected platforms: ' + (', '.join(platforms) or 'host-managed runtime'))
    scripted = role in {'workspace-html', 'workspace-cards', 'browser-extensions'}
    defaults = ['JavaScript', 'HTML', 'CSS'] if scripted and role != 'workspace-cards' else ['JavaScript']
    defaults = defaults if scripted else []
    while True:
        result = select_supported('Source languages', options, existing, defaults)
        executable = {'JavaScript', 'TypeScript', 'Apps Script', 'Google Apps Script'}
        if role == 'browser-extensions':
            executable = {'JavaScript', 'TypeScript'}
        if not scripted or set(result) & executable:
            return result
        print('Include JavaScript or TypeScript for executable source. Markup and styles alone cannot run an add-on.')
