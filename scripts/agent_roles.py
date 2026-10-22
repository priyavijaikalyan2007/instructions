#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 91091f6c-8190-4d61-87b2-c3b4344cfd51
# Created: 2026

# COMPONENT: Selectable coding-tool roles
# PURPOSE: Store project role assignments without assigning behavior by model vendor.
# RELATES: instructions/AGENT_ROLES.md, configure_instructions.py, PROJECT_PROFILE.md
# FLOW: Interview or JSON -> validated role table -> preserved native entry points.
# SECURITY: Role text defines task defaults, not tool permissions or automatic delegation.

from pathlib import Path
import re

from project_initialization import backup_original, is_inherited, safe_path
from terminal_ui import input, print


ROLES = ('general', 'implementation', 'planning', 'architecture', 'review', 'testing', 'security',
         'ux', 'documentation', 'operations', 'product')
ROLE_HELP = ('Work across the applicable roles.', 'Write and maintain code.', 'Define steps and acceptance checks.',
             'Design component boundaries and interfaces.', 'Review correctness and maintainability.',
             'Design and run relevant checks.', 'Review trust boundaries and sensitive data.',
             'Design and assess user interactions.', 'Write and maintain project documentation.',
             'Maintain build, release, and operational workflows.', 'Define user needs and product behavior.')
TOOLS = ('claude', 'codex', 'gemini', 'antigravity', 'pi', 'roo', 'cline')
TOOL_LABELS = ('Claude Code', 'Codex', 'Gemini CLI', 'Antigravity', 'Pi', 'Roo Code', 'Cline')
SECTION = re.compile(r'^## Agent roles\s*\n(.*?)(?=^## |\Z)', re.M | re.S)


def validate_assignments(assignments: dict) -> dict:
    """Validate role IDs and single-line notes before rendering any Markdown or entry path."""
    if not isinstance(assignments, dict):
        raise ValueError('agent_roles must be an object keyed by tool identifier.')
    result = {}
    for tool, value in assignments.items():
        if not isinstance(tool, str) or not re.fullmatch(r'[a-z][a-z0-9-]*', tool):
            raise ValueError(f'Invalid agent tool identifier: {tool!r}')
        item = {'roles': value, 'notes': ''} if isinstance(value, list) else value
        if not isinstance(item, dict) or set(item) - {'roles', 'notes'}:
            raise ValueError(f'{tool}: use a role list or roles and notes.')
        roles, notes = item.get('roles'), item.get('notes', '')
        if (not isinstance(roles, list) or not roles or any(role not in ROLES for role in roles)
                or len(set(roles)) != len(roles)):
            raise ValueError(f'{tool}: choose distinct known roles from instructions/AGENT_ROLES.md.')
        if not isinstance(notes, str) or any(ord(char) < 32 or char in '|`<>' for char in notes):
            raise ValueError(f'{tool}: notes must be one line without Markdown delimiters.')
        result[tool] = {'roles': roles, 'notes': notes.strip()}
    return result


def profile_agent_roles(profile: str) -> dict:
    """Read the optional project table and reject duplicate or malformed assignment rows."""
    matches = list(SECTION.finditer(profile))
    if len(matches) > 1:
        raise ValueError('Profile needs at most one Agent roles section.')
    if not matches:
        return {}
    result = {}
    for line in matches[0].group(1).splitlines():
        if not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if cells[0] == 'Tool' or set(cells[0]) <= {'-', ' ', ':'}:
            continue
        if len(cells) != 3 or cells[0] in result:
            raise ValueError('Agent roles table needs unique Tool, Roles, and Notes rows.')
        result[cells[0]] = {'roles': [part.strip() for part in cells[1].split(',')], 'notes': cells[2]}
    return validate_assignments(result)


def apply_agent_roles(profile: str, assignments: dict) -> str:
    """Replace only the role section while retaining component selections and project notes."""
    assignments = validate_assignments(assignments)
    lines = ['## Agent roles', '', 'Use [shared role definitions](instructions/AGENT_ROLES.md).', '',
             '| Tool | Roles | Notes |', '| --- | --- | --- |']
    lines.extend(f"| {tool} | {', '.join(item['roles'])} | {item['notes']} |"
                 for tool, item in assignments.items())
    if not assignments:
        lines.extend(['', 'No tool-specific roles are assigned. Follow the user task and shared workflow.'])
    section = '\n'.join(lines) + '\n\n'
    match = SECTION.search(profile)
    if match:
        return profile[:match.start()] + section + profile[match.end():]
    return profile.rstrip() + '\n\n' + section


def choose_numbers(prompt: str, count: int, default: str) -> list[int]:
    """Collect distinct menu choices and make empty assignment selection explicit."""
    while True:
        answer = input(f'{prompt} [{default}]: ').strip() or default
        if answer.lower() == 'none':
            return []
        parts = [part.strip() for part in answer.split(',')]
        if all(part.isdigit() and 1 <= int(part) <= count for part in parts) and len(set(parts)) == len(parts):
            return [int(part) - 1 for part in parts]
        print('Enter listed numbers separated by commas, or none.')


def interview_agent_roles(current: dict) -> dict:
    """Offer multiple roles per tool while retaining current assignments as displayed defaults."""
    print('\nChoose coding tools and their roles in this project:')
    print('One tool can have several roles. Roles guide work and do not change tool permissions.')
    for number, label in enumerate(TOOL_LABELS, 1):
        print(f'  {number}. {label}')
    print('  8. Other: enter a tool identifier and configure its instruction discovery manually.')
    print('Choose none to use the shared workflow without tool-specific roles.')
    default = ','.join(str(TOOLS.index(tool) + 1) for tool in current if tool in TOOLS) or 'none'
    selected = choose_numbers('Tool numbers', 8, default)
    tools = [TOOLS[number] if number < len(TOOLS) else input('Custom tool identifier: ').strip()
             for number in selected]
    if not selected:
        return {}
    result = {tool: item for tool, item in current.items() if tool not in TOOLS} if selected else {}
    for tool in tools:
        previous = current.get(tool, {'roles': ['general'], 'notes': ''})
        default_roles = ','.join(str(ROLES.index(role) + 1) for role in previous['roles'])
        explain_tool_roles(tool)
        choices = choose_numbers(f'{tool} role numbers', len(ROLES), default_roles)
        label = TOOL_LABELS[TOOLS.index(tool)] if tool in TOOLS else tool
        print(f'\nOptional project notes for {label}: describe local preferences, or leave this field unchanged.')
        print('Example: Review API changes before implementation. Notes do not grant permissions.')
        notes = input(f"{tool} project notes [{previous['notes']}]: ").strip() or previous['notes']
        result[tool] = {'roles': [ROLES[number] for number in choices], 'notes': notes}
    return validate_assignments(result)


def explain_tool_roles(tool: str) -> None:
    """Repeat role purpose and controls for each tool instead of relying on a previous screen."""
    label = TOOL_LABELS[TOOLS.index(tool)] if tool in TOOLS else tool
    print(f'\nChoose the work {label} should normally handle in this project.')
    print('These choices become default responsibilities in PROJECT_PROFILE.md. Your explicit task takes priority.')
    print('Select general for all applicable work, or select specific responsibilities.')
    print('For example, choose implementation and testing for a tool that writes and tests code.')
    print('In forms, Space selects several roles and Enter accepts. In plain mode, enter numbers separated by commas.')
    print('Roles do not launch tools, grant permissions, or assign work automatically.')
    for number, (role, help_text) in enumerate(zip(ROLES, ROLE_HELP), 1):
        print(f'  {number}. {role}: {help_text}')


def agent_entry_changes(root: Path, profile: str, library_root: Path) -> dict:
    """Install neutral pointers and back up known inherited entries while preserving custom files."""
    assignments = profile_agent_roles(profile)
    changes = {}
    for name in ['CLAUDE.md', 'CODEX.md', 'GEMINI.md']:
        source, destination = library_root / name, safe_path(root, name)
        data = source.read_bytes()
        if not destination.exists():
            changes[name] = data
        elif destination.read_bytes() != data and is_inherited(root, name):
            backup_original(root, name, changes)
            changes[name] = data
    if 'roo' in assignments:
        name = '.roo/rules/00-project-instructions.md'
        path = safe_path(root, name)
        if not path.exists():
            changes[name] = ('# Project instructions\n\nRead root AGENTS.md and PROJECT_PROFILE.md.\n'
                             'Use the roo role assignments and instructions/AGENT_ROLES.md.\n').encode()
    return changes
