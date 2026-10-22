#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: f005d5da-649c-44eb-9011-73a3a48d98fb
# Created: 2026

# COMPONENT: Template baseline maintenance
# PURPOSE: Register reviewed source-file hashes without forgetting earlier template versions.
# RELATES: project_initialization.py, instructions/templates/repository/inherited-files.json
# FLOW: Source repository -> compare known inherited files -> check or explicit apply.
# SECURITY: Only source repository use is allowed. Never run this to approve downstream custom content.

import argparse
import hashlib
import json
from pathlib import Path

from project_initialization import is_source_repository


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'instructions/templates/repository/inherited-files.json'
FOLDERS = ['.github', 'instructions/project', 'instructions/maintenance', 'agentknowledge']


def updated_manifest() -> dict:
    """Add source versions while retaining all previously registered byte hashes."""
    result = json.loads(MANIFEST.read_text())
    paths = [ROOT / name for name in ['LICENSE', 'AGENTS.md', 'CLAUDE.md', 'CODEX.md', 'GEMINI.md']]
    paths.extend(ROOT / name for name in ['PROJECT_PROFILE.md', 'PROJECT.md', 'ADDITIONAL.md',
                                        'CONVERSATION.md', 'CHANGELOG.md', 'README.md', 'CONTRIBUTING.md',
                                        'CODE_OF_CONDUCT.md', 'SECURITY.md'] if (ROOT / name).is_file())
    for folder in FOLDERS:
        paths.extend(path for path in (ROOT / folder).rglob('*') if path.is_file())
    for path in sorted(paths):
        if path.is_symlink():
            raise ValueError(f'Source baseline must not contain symlinks: {path.relative_to(ROOT)}')
        relative = path.relative_to(ROOT).as_posix()
        if '/template-backup/' in relative or path.name == 'INITIALIZATION.json':
            raise ValueError('Source repository contains downstream initialization records. Resolve them first.')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        result[relative] = sorted(set(result.get(relative, [])) | {digest})
    return dict(sorted(result.items()))


def main() -> int:
    """Validate freshness by default or register the reviewed source state with --apply."""
    parser = argparse.ArgumentParser(description='Check or update recognized source-template file versions.')
    parser.add_argument('--apply', action='store_true', help='register current reviewed source files')
    args = parser.parse_args()
    if not is_source_repository(ROOT):
        parser.error('Run this maintenance command only in the source instructions repository.')
    text = json.dumps(updated_manifest(), indent=2) + '\n'
    if text == MANIFEST.read_text():
        print('Template baseline is current.')
        return 0
    if args.apply:
        MANIFEST.write_text(text)
        print('Template baseline updated. Review and commit the manifest.')
        return 0
    print('Template baseline is stale. Review source changes, then run with --apply.')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
