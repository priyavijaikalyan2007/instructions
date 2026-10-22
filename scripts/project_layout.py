#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: bb2403af-1231-4b04-977f-b9f90e08b082
# Created: 2026

# COMPONENT: Project-owned file layout
# PURPOSE: Preview safe migration from legacy project paths to root-owned context and hidden setup state.
# RELATES: configure_instructions.py, project_initialization.py
# FLOW: Read current or legacy bytes -> repair active links -> detect conflicts -> return a write plan.
# SECURITY: Reject symlink paths, parent traversal, and conflicting destinations before any mutation.

from pathlib import Path
import posixpath
import re


PROJECT_FILES = ('PROJECT_PROFILE.md', 'PROJECT.md', 'ADDITIONAL.md', 'CONVERSATION.md', 'CHANGELOG.md')
PUBLIC_DOCUMENTS = ('README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md')
PROFILE_PATH = 'PROJECT_PROFILE.md'
STATE_PATH = '.instructions/INITIALIZATION.json'
BACKUP_ROOT = '.instructions/template-backup/'
LEGACY_ROOT = 'instructions/project/'
LEGACY_PATHS = {name: LEGACY_ROOT + name for name in PROJECT_FILES}
LEGACY_PATHS[STATE_PATH] = LEGACY_ROOT + 'INITIALIZATION.json'
LEGACY_PATHS.update({name: '.github/' + name for name in PUBLIC_DOCUMENTS})


def safe_path(root: Path, value: str) -> Path:
    """Resolve a repository-relative path without traversing symlinks or parent paths."""
    path = Path(value)
    if not value or path.is_absolute() or '..' in path.parts or '.git' in path.parts:
        raise ValueError(f'Unsafe repository path: {value!r}')
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'Symlink paths are not supported: {value}')
    return current


def existing_project_path(root: Path, relative: str) -> Path:
    """Prefer the canonical location while recognizing only the previous default layout."""
    path = safe_path(root, relative)
    legacy = LEGACY_PATHS.get(relative)
    if relative.startswith(BACKUP_ROOT):
        legacy = LEGACY_ROOT + 'template-backup/' + relative[len(BACKUP_ROOT):]
    if not path.exists() and legacy:
        return safe_path(root, legacy)
    return path


def canonical_profile(text: str) -> str:
    """Replace default project references without altering custom context locations."""
    for name, legacy in LEGACY_PATHS.items():
        text = text.replace(legacy, name)
    return text


def rebase_target(target: str, source_root: str = LEGACY_ROOT) -> str:
    """Move a local link target while retaining URI schemes, anchors, and angle-delimited paths."""
    angled = target.startswith('<') and target.endswith('>')
    value = target[1:-1] if angled else target
    if value.startswith(('#', '/')) or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', value):
        return target
    path, separator, anchor = value.partition('#')
    path = canonical_profile(posixpath.normpath(posixpath.join(source_root, path)))
    result = path + (separator + anchor if separator else '')
    return '<' + result + '>' if angled else result


def rebase_links(text: str, source_root: str = LEGACY_ROOT) -> str:
    """Keep inline and reference links valid when an active document moves to the root."""
    def replace(match):
        return match.group(1) + rebase_target(match.group(2), source_root)
    text = re.sub(r'(\]\()(<[^>\n]+>|[^\s)]+)', replace, text)
    return re.sub(r'(^ {0,3}\[[^\]\n]+\]:[ \t]*)(<[^>\n]+>|[^\s]+)', replace, text, flags=re.M)


def migrated_bytes(relative: str, data: bytes) -> bytes:
    """Repair active documents while preserving the exact bytes of historical records and setup state."""
    if relative in PUBLIC_DOCUMENTS:
        return canonical_profile(rebase_links(data.decode('utf-8'), '.github/')).encode('utf-8')
    if relative not in {'PROJECT_PROFILE.md', 'PROJECT.md', 'ADDITIONAL.md'}:
        return data
    return canonical_profile(rebase_links(data.decode('utf-8'))).encode('utf-8')


def read_project_bytes(root: Path, relative: str) -> bytes | None:
    """Read a canonical project file through its legacy location without writing a migration."""
    path = existing_project_path(root, relative)
    if not path.exists():
        return None
    data = path.read_bytes()
    return migrated_bytes(relative, data) if path != safe_path(root, relative) else data


def migration_pairs(root: Path) -> dict[str, str]:
    """Include only known project defaults and explicit legacy backup files."""
    pairs = dict(LEGACY_PATHS)
    backup = safe_path(root, LEGACY_ROOT + 'template-backup')
    if backup.exists():
        for path in backup.rglob('*'):
            safe_path(root, path.relative_to(root).as_posix())
            if path.is_file():
                pairs[BACKUP_ROOT + path.relative_to(backup).as_posix()] = path.relative_to(root).as_posix()
    return pairs


def active_reference_changes(root: Path) -> dict[str, bytes]:
    """Repair only default path tokens in active guides, preserving encodings and custom rules."""
    changes = {}
    paths = list(safe_path(root, 'instructions').rglob('*.md'))
    paths.extend(path for path in root.glob('*.md') if path.name not in {'CONVERSATION.md', 'CHANGELOG.md'})
    for path in paths:
        relative = path.relative_to(root).as_posix()
        if any(part in {'project', 'maintenance', 'templates'} for part in path.relative_to(root).parts):
            continue
        safe_path(root, relative)
        original = path.read_bytes()
        data = original
        for name, legacy in LEGACY_PATHS.items():
            data = data.replace(legacy.encode(), name.encode())
        if data != original:
            changes[relative] = data
    return changes


def layout_changes(root: Path, check: bool = False) -> dict[str, bytes | None]:
    """Plan moves only after checking every source and destination for conflicts."""
    changes = {}
    for destination, source in migration_pairs(root).items():
        old, new = safe_path(root, source), safe_path(root, destination)
        if not old.exists():
            continue
        original = old.read_bytes()
        data = migrated_bytes(destination, original)
        if new.exists() and (not new.is_file() or new.read_bytes() not in {original, data}):
            raise ValueError(f'Project layout conflict: {source} and {destination}. Resolve both before setup.')
        changes[destination] = data
        changes[source] = None
    if changes:
        changes.update({name: data for name, data in active_reference_changes(root).items() if name not in changes})
    if check and changes:
        raise ValueError('Project files need root-layout migration. Run setup to preview the moves.')
    return changes
