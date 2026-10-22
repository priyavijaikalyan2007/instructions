#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: e7319d0f-e56b-44cd-aa04-7499d6a55a17
# Created: 2026

# COMPONENT: Source-folder bootstrap planning
# PURPOSE: Validate explicitly selected folders before preview or any filesystem writes.
# RELATES: configure_instructions.py, profile_interview.py
# FLOW: Enabled component metadata -> safe literal folders -> conflict checks -> missing-directory plan.
# SECURITY: Reject symlinks, out-of-scope folders, and conflicts with existing or planned files.

from pathlib import Path

from project_initialization import safe_path


def metadata_paths(value: str) -> list[str]:
    """Read optional Markdown path lists without treating blank metadata as a path."""
    return [part.strip().strip('`').strip() for part in value.split(',') if part.strip()]


def validate_source_folder(root: Path, name: str, scope: list[str], file_changes: dict) -> Path:
    """Require a literal source-scope entry that can coexist with the complete write plan."""
    path = safe_path(root, name)
    if any(character in name for character in '*?[]') or Path(name) not in {Path(value) for value in scope}:
        raise ValueError(f'Source folder must be a literal selected source path: {name}')
    for candidate in [path, *path.parents]:
        if candidate.exists() and not candidate.is_dir():
            raise ValueError(f'Source folder conflicts with an existing file: {name}')
        if candidate == root:
            break
    for relative in file_changes:
        destination = safe_path(root, relative)
        if destination == path or destination in path.parents:
            raise ValueError(f'Source folder conflicts with a planned instruction file: {name}')
    return path


def plan_source_folders(root: Path, components: list[dict], file_changes: dict, check: bool = False) -> list[str]:
    """Plan only explicit enabled folders. Leave planned files and unmatched scope untouched."""
    folders = set()
    for component in components:
        if not component['enabled']:
            continue
        scope = metadata_paths(component['source_paths'])
        for name in metadata_paths(component.get('source_folders', '')):
            path = validate_source_folder(root, name, scope, file_changes)
            if not path.exists():
                if check:
                    raise ValueError(f'Missing source folder: {name}. Rerun the configurator to preview creation.')
                folders.add(str(path.relative_to(root)))
    return sorted(folders)


def extension_scope_overlap(browser: str, workspace: str) -> bool:
    """Compare literal scopes without interpreting wildcard patterns as directories."""
    if any(character in browser + workspace for character in '*?[]'):
        return False
    left, right = Path(browser), Path(workspace)
    return left == right or left in right.parents or right in left.parents


def source_scope_warnings(components: list[dict]) -> list[str]:
    """Explain broad extension scope without forbidding intentionally shared source."""
    browser_paths, workspace_paths = set(), set()
    for component in components:
        if not component['enabled']:
            continue
        targets = metadata_paths(component['targets'])
        if 'browser-extensions' in targets:
            browser_paths.update(metadata_paths(component['source_paths']))
        if 'google-workspace' in targets:
            workspace_paths.update(metadata_paths(component['source_paths']))
    if any(extension_scope_overlap(browser, workspace) for browser in browser_paths for workspace in workspace_paths):
        return ['Browser and Workspace source scopes overlap. Prefer separate src/extensions/browser/<name>/ '
                'and src/extensions/googleworkspace/<name>/ scopes unless shared source is intentional.']
    return []
