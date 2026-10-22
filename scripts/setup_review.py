#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 8daf399c-cbb3-4378-a1a7-c646c72b08ad
# Created: 2026

# COMPONENT: Setup review presentation
# PURPOSE: Separate readable setup summaries from optional exact file changes.
# RELATES: configure_instructions.py, terminal_ui.py, curses_interview.py
# FLOW: Validated change plan -> summary and optional diff -> explicit approval.

import difflib
from pathlib import Path
import re


def scope_lines(profile: str) -> list[str]:
    """Present enabled components and per-tool responsibilities without Markdown scaffolding."""
    lines = []
    for match in re.finditer(r'^### ([^\n]+)\n(.*?)(?=^## |^### |\Z)', profile, re.M | re.S):
        name, body = match.groups()
        if '- [x] Enabled' not in body:
            continue
        lines.extend(['', 'Component: ' + name])
        for field in ['Targets', 'Source paths', 'Languages', 'Platforms', 'Deployment']:
            value = re.search(r'^- ' + field + r': (.+)$', body, re.M)
            if value:
                lines.append('  ' + field + ': ' + value.group(1).replace('`', ''))
    roles = re.search(r'^## Agent roles\n(.*?)(?=^## |\Z)', profile, re.M | re.S)
    if roles:
        assignments = []
        for line in roles.group(1).splitlines():
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) == 3 and re.fullmatch(r'[a-z][a-z0-9-]*', cells[0]):
                assignments.append('  ' + cells[0] + ': ' + cells[1] + (' — ' + cells[2] if cells[2] else ''))
        lines.extend(['', 'Agent responsibilities:', *(assignments or ['  No tool-specific roles.'])])
    return lines


def summary_lines(root: Path, changes: dict, folders: list[str], profile: str) -> list[str]:
    """Group installed library files and list owner-visible changes before approval."""
    if not changes and not folders:
        return ['No changes.']
    lines = ['Project: ' + str(root), '', 'Planned setup',
             f'{len(changes)} file changes and {len(folders)} new source folders.',
             'Existing customized files remain preserved unless an update is explicitly listed.']
    lines.extend(scope_lines(profile))
    lines.extend(['', 'Project files and setup tools:'])
    shared = [name for name in changes if name.startswith('instructions/')]
    tools = [name for name in changes if name.startswith('scripts/')]
    backups = [name for name in changes if name.startswith('.instructions/template-backup/')]
    for name, data in sorted(changes.items()):
        if name in shared or name in tools or name in backups:
            continue
        action = 'Remove inherited' if data is None else ('Update' if (root / name).exists() else 'Create')
        lines.append(action + ' ' + name)
    lines.extend([f'Install or update {len(shared)} shared instruction files.',
                  f'Install or update {len(tools)} setup support scripts.',
                  f'Preserve {len(backups)} inherited originals in .instructions/template-backup/.'])
    if folders:
        lines.extend(['', 'Source folders to create:', *['  ' + folder for folder in folders]])
    lines.extend(['', 'Setup selects instructions and creates placeholders. It does not build, deploy, or publish.',
                  'Complete the project checklist in SETUP.md when generated.',
                  'Press F3 for the complete file list and exact text changes. Approval follows this review.'])
    return lines


def detail_lines(root: Path, changes: dict) -> list[str]:
    """Retain exact diffs for every UTF-8 file and explain binary or other encoded changes."""
    lines = []
    for name, data in sorted(changes.items()):
        path = root / name
        action = 'Remove inherited' if data is None else ('Update' if path.exists() else 'Create')
        lines.extend(['', action + ' ' + name])
        try:
            before = path.read_text().splitlines(True) if path.exists() else []
            after = data.decode('utf-8').splitlines(True) if data is not None else []
        except UnicodeError:
            lines.append('Non-UTF-8 content. File bytes are preserved as supplied.')
            continue
        lines.extend(''.join(difflib.unified_diff(before, after, fromfile=name, tofile=name)).splitlines())
    return lines
