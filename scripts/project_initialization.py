#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 818ec5ae-84f1-424a-b459-38f6dd69851f
# Created: 2026

# COMPONENT: New project initialization
# PURPOSE: Replace known template identity while preserving customized project content and upstream notices.
# RELATES: configure_instructions.py, license_selection.py, instructions/templates/repository/
# FLOW: Explicit initialization -> identity -> known-file comparison -> backed-up document plan.
# SECURITY: Reject source-repository initialization, symlinks, unknown license replacement, and silent relicensing.

from __future__ import annotations

from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
from string import Template
import subprocess
import uuid

from terminal_ui import input, print
from project_context import context_values, interview_context, validate_context

from project_layout import (BACKUP_ROOT, PROFILE_PATH, STATE_PATH, LEGACY_PATHS, PROJECT_FILES, PUBLIC_DOCUMENTS,
                            existing_project_path, read_project_bytes, safe_path)
from license_selection import interview_license, license_files, validate_license


TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / 'instructions/templates/repository'
DOCUMENTS = {name: name for name in (*PUBLIC_DOCUMENTS, 'THIRD_PARTY_NOTICES.md')}


def inherited_files() -> dict:
    """Read the explicit versioned allowlist of template-owned files and their known hashes."""
    return json.loads((TEMPLATE_ROOT / 'inherited-files.json').read_text())


def is_inherited(root: Path, relative: str) -> bool:
    """Match complete file bytes rather than names, snippets, or guessed project identity."""
    path = existing_project_path(root, relative)
    if not path.is_file():
        return False
    known = inherited_files()
    hashes = known.get(relative, []) + known.get(LEGACY_PATHS.get(relative, ''), [])
    return hashlib.sha256(path.read_bytes()).hexdigest() in hashes


def is_source_repository(root: Path) -> bool:
    """Recognize the library's origin without contacting GitHub or printing remote credentials."""
    if not (root / '.git').exists():
        return False
    try:
        result = subprocess.run(['git', '-C', str(root), 'config', '--get', 'remote.origin.url'],
                                capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return False
    return bool(re.search(r'[:/]priyavijaikalyan2007/instructions(?:\.git)?/?$', result.stdout.strip(), re.I))


def validate_identity_field(key: str, text: str) -> str:
    """Validate one project fact so the interview can correct it without discarding accepted answers."""
    if (not isinstance(text, str) or not text.strip() or len(text) > 500
            or any(ord(char) < 32 or char in '`<>|\\' for char in text)):
        raise ValueError(f'Project {key} needs a nonempty single line without Markdown delimiters.')
    if key == 'name' and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', text):
        raise ValueError('Project name must use letters, digits, dots, underscores, or hyphens.')
    if key == 'year' and not re.fullmatch(r'[0-9]{4}', text):
        raise ValueError('Project year must contain four digits.')
    if key == 'repository_url' and text != 'none' and not re.fullmatch(
            r'https://[A-Za-z0-9.-]+(?::[0-9]+)?/[^\s?#]+', text):
        raise ValueError('repository_url must be none or an HTTPS repository URL '
                         'without credentials, query, or fragment.')
    return text


def validate_identity(value: dict) -> dict:
    """Validate project metadata before it enters Markdown, notices, or initialization state."""
    keys = {'name', 'owner', 'year', 'repository_url', 'description', 'license'}
    if not isinstance(value, dict) or not keys <= set(value) or set(value) - keys - {'business_context'}:
        raise ValueError('Project answers require name, owner, year, repository_url, description, and license.')
    for key in keys - {'license'}:
        validate_identity_field(key, value[key])
    result = {**value, 'license': validate_license(value['license'])}
    if 'business_context' in value:
        result['business_context'] = validate_context(value['business_context'])
    return result


def ask_identity_field(key: str, label: str, default: str) -> str:
    """Keep the current field editable after a validation error and retain all other accepted facts."""
    while True:
        answer = input(f'{label} [{default or "required"}]: ').strip() or default
        try:
            return validate_identity_field(key, answer)
        except ValueError as error:
            print(f'Invalid value: {error}')
            default = answer


def interview_identity(root: Path, local: bool = False) -> dict:
    """Collect facts, leaving policy commitments as guided placeholders rather than guesses."""
    print('\nInitialize documents for a new repository copied from the instruction template.')
    print('Known inherited originals will be backed up. Customized files will be preserved and reported.')
    print('Contribution rules, private contacts, and response targets remain TODOs for the project owner.')
    defaults = {'name': root.name, 'owner': '', 'year': str(date.today().year),
                'repository_url': 'none' if local else '', 'description': 'TODO: Describe this project and its users.'}
    labels = {'name': 'Repository name', 'owner': 'Copyright owner', 'year': 'Copyright year',
              'repository_url': 'HTTPS repository URL', 'description': 'Project purpose'}
    if local:
        print('Local setup needs no Git or GitHub repository. Use none for a repository URL you do not have yet.')
    values = {}
    for key, default in defaults.items():
        values[key] = ask_identity_field(key, labels[key], default)
    values['business_context'] = interview_context()
    values['license'] = interview_license()
    return validate_identity(values)


def prepare_initialization(root: Path, args) -> dict | None:
    """Load an explicit setup request or explain the choice when an inherited profile is detected."""
    if (not args.initialize_project and not args.answers and not args.check and not args.dry_run
            and is_inherited(root, PROFILE_PATH) and not is_source_repository(root)):
        print('This repository contains the instruction library\'s original project profile.')
        print('1. Initialize a new project: replace known inherited identity and policy files after preview.')
        print('2. Edit only instruction selections: preserve all repository documents.')
        answer = input('Setup mode [2]: ').strip() or '2'
        if answer not in {'1', '2'}:
            raise ValueError('Choose setup mode 1 or 2.')
        args.initialize_project = answer == '1'
    if not args.initialize_project:
        return None
    if is_source_repository(root):
        raise ValueError('Project initialization is disabled for the source instruction repository. Use --root.')
    state = existing_project_path(root, STATE_PATH)
    if state.exists():
        previous = json.loads(state.read_text())
        if previous.get('version') != 1:
            raise ValueError('Unsupported initialization state version.')
        supplied = json.loads(args.project_answers.read_text()) if args.project_answers else previous['project']
        if validate_identity(supplied) != previous['project']:
            raise ValueError('Project is already initialized. Review identity or LICENSE changes separately.')
        print('Project already initialized. Preserve project-owned documents.')
        return None
    if args.project_answers:
        return validate_identity(json.loads(args.project_answers.read_text()))
    if args.dry_run and not args.target_folder:
        raise ValueError('--initialize-project --dry-run requires --project-answers. No interview or writes occurred.')
    return interview_identity(root, bool(args.target_folder))


def render_document(template: str, identity: dict, links: dict) -> bytes:
    """Keep template attribution while assigning the generated document its own repository and file identity."""
    text = (TEMPLATE_ROOT / template).read_text()
    text = text.replace('Repository: instructions', 'Repository: ' + identity['name'])
    text = text.replace('SPDX-License-Identifier: MIT',
                        f"SPDX-FileCopyrightText: {identity['year']} {identity['owner']}\nSPDX-License-Identifier: MIT")
    text = re.sub(r'File GUID: [\w-]+', 'File GUID: ' + str(uuid.uuid4()), text, count=1)
    values = {key: value for key, value in identity.items() if key != 'license'}
    return Template(text).substitute(values | context_values(identity) | links).encode()


def backup_original(root: Path, relative: str, changes: dict) -> None:
    """Retain an exact original before modifying an inherited document or removing an inherited record."""
    original = existing_project_path(root, relative).read_bytes()
    backup = BACKUP_ROOT + relative
    existing = safe_path(root, backup)
    legacy = safe_path(root, 'instructions/project/template-backup/' + relative)
    if not existing.exists() and legacy.exists():
        existing = legacy
    if existing.exists() and existing.read_bytes() != original:
        raise ValueError(f'Existing backup differs: {backup}. Preserve it and resolve the conflict manually.')
    if not existing.exists():
        changes[backup] = original


def plan_document(root: Path, relative: str, data: bytes, changes: dict, strict: bool = False) -> None:
    """Replace only absent or recognized source documents. Unknown legal terms stop the entire operation."""
    path = existing_project_path(root, relative)
    if not path.exists():
        changes[relative] = data
    elif path.read_bytes() == data:
        return
    elif is_inherited(root, relative):
        backup_original(root, relative, changes)
        changes[relative] = data
    elif strict:
        raise ValueError(f'Preserve customized {relative}. Review existing licensing before initialization.')
    else:
        print(f'Preserve customized {relative}. Complete its project details manually.')


def plan_record_cleanup(root: Path, changes: dict, protected: set[str]) -> None:
    """Remove only exact inherited records. Backups remain outside active project and knowledge paths."""
    prefixes = ('instructions/maintenance/', 'agentknowledge/')
    records = set(PROJECT_FILES) - {PROFILE_PATH}
    protected = protected | {LEGACY_PATHS.get(name, name) for name in protected}
    for relative in set(inherited_files()) | records:
        if relative in protected or not (relative.startswith(prefixes) or relative in records):
            continue
        if is_inherited(root, relative):
            backup_original(root, relative, changes)
            changes[relative] = None
            if relative in LEGACY_PATHS and safe_path(root, LEGACY_PATHS[relative]).exists():
                changes[LEGACY_PATHS[relative]] = None
        elif safe_path(root, relative).exists():
            print(f'Preserve customized {relative}. Review inherited history manually.')


def project_documents(context_paths: dict) -> dict:
    """Respect project-owned context locations and reject collisions with policy documents."""
    result = dict(DOCUMENTS)
    for relative, template in context_paths.items():
        if relative in result:
            raise ValueError(f'Project context conflicts with generated policy: {relative}')
        result[relative] = template.replace('_TEMPLATE', '')
    return result


def document_links(relative: str, context_paths: dict) -> dict:
    """Render links relative to each generated file, including relocated project facts."""
    paths = {template.replace('_TEMPLATE.md', '').lower(): name for name, template in context_paths.items()}
    paths.update({'profile': PROFILE_PATH, 'agents': 'AGENTS.md', 'license': 'LICENSE'})
    parent = str(Path(relative).parent)
    return {name + '_link': os.path.relpath(path, parent) for name, path in paths.items()}


def check_license_aliases(root: Path) -> None:
    """Prevent conflicting grants when an established project uses another common license filename."""
    for name in ['LICENSE.md', 'LICENSE.txt', 'COPYING', 'COPYING.md', 'COPYING.txt']:
        if safe_path(root, name).exists():
            raise ValueError(f'Preserve existing {name}. Review existing licensing before creating LICENSE.')


def initialization_changes(root: Path, identity: dict | None, context_paths: dict) -> dict[str, bytes | None]:
    """Plan project documents and local state without modifying source policies or shared guides."""
    if identity is None:
        return {}
    check_license_aliases(root)
    changes = {}
    for relative, template in project_documents(context_paths).items():
        links = document_links(relative, context_paths)
        plan_document(root, relative, render_document(template, identity, links), changes)
    for relative, data in license_files(identity['license'], identity['owner'], identity['year']).items():
        plan_document(root, relative, data, changes, strict=True)
    upstream = (TEMPLATE_ROOT / 'INSTRUCTION_LIBRARY_LICENSE.txt').read_bytes()
    plan_document(root, 'instructions/LICENSE', upstream, changes, strict=True)
    plan_record_cleanup(root, changes, set(context_paths))
    if is_inherited(root, PROFILE_PATH):
        backup_original(root, PROFILE_PATH, changes)
    changes[STATE_PATH] = (json.dumps({'version': 1, 'project': identity}, indent=2) + '\n').encode()
    return changes
