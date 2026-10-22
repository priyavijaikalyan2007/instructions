#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 967b45be-cc55-4d9c-aa18-24fa4a940c5b
# Created: 2026

# COMPONENT: Project license selection
# PURPOSE: Apply explicit license choices using pinned, unmodified legal texts.
# RELATES: project_initialization.py, instructions/templates/repository/licenses/
# FLOW: Interview or JSON -> validate exact identifiers -> scope notice and bundled terms.
# SECURITY: Use a fixed catalog and verify hashes. Never fetch or execute input during initialization.

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from terminal_ui import input, print


LICENSE_ROOT = Path(__file__).resolve().parents[1] / 'instructions/templates/repository/licenses'
SOFTWARE = {
    '1': ('MIT', 'Permissive terms with attribution and warranty disclaimer.'),
    '2': ('Apache-2.0', 'Permissive terms with an express patent grant and notice requirements.'),
    '3': ('LGPL-2.1', 'Lesser GPL version 2.1, commonly used for libraries.'),
    '4': ('LGPL-3.0', 'Lesser GPL version 3.0, with GPLv3 companion terms.'),
    '5': ('GPL-2.0', 'GPL version 2.0 copyleft terms.'),
    '6': ('GPL-3.0', 'GPL version 3.0 copyleft terms.'),
    '7': ('AGPL-3.0', 'Affero GPL version 3.0, including network-use source obligations.'),
    '8': ('Elastic-2.0', 'Source-available terms with managed-service and other restrictions.'),
    '9': ('SSPL-1.0', 'Source-available terms with service-source obligations.'),
}
CONTENT = ['CC-BY-4.0', 'CC-BY-SA-4.0', 'CC-BY-ND-4.0', 'CC-BY-NC-4.0',
           'CC-BY-NC-SA-4.0', 'CC-BY-NC-ND-4.0', 'CC0-1.0']
GNU = {value[0] for value in SOFTWARE.values() if 'GPL' in value[0]}
SOFTWARE_IDS = ({value[0] for value in SOFTWARE.values()} - GNU) | {
    name + suffix for name in GNU for suffix in ['-only', '-or-later']}


def choose(prompt: str, allowed: set[str], default: str = '') -> str:
    """Read a fixed choice, retaining the displayed default when present."""
    while True:
        answer = input(prompt).strip() or default
        if answer in allowed:
            return answer
        print('Choose one of: ' + ', '.join(sorted(allowed)))


def interview_software() -> list[str]:
    """Explain single and alternative licensing without assuming a product-specific preset."""
    print('\nChoose the license for new project software. Read the bundled terms before publishing.')
    for number, (identifier, explanation) in SOFTWARE.items():
        print(f'  {number}. {identifier}: {explanation}')
    print('  0. Undecided or custom/commercial terms: create a TODO, not a fabricated license.')
    print('For dual or multiple licensing, enter distinct numbers separated by commas.')
    print('Recipients may choose any listed license (OR). This does not combine their obligations (AND).')
    print('Elastic and SSPL are source-available choices, not OSI-approved open-source licenses.')
    while True:
        selected = [part.strip() for part in input('Software license numbers [0]: ').split(',')]
        selected = selected if selected != [''] else ['0']
        if selected == ['0']:
            return []
        if len(selected) == len(set(selected)) and set(selected) <= SOFTWARE.keys():
            break
        print('Use distinct listed numbers, or 0 alone for pending terms.')
    result = []
    for number in selected:
        identifier = SOFTWARE[number][0]
        if identifier in GNU:
            policy = choose(f'{identifier}: this version only, or this and later versions? [only/later]: ',
                            {'only', 'later'})
            identifier += '-only' if policy == 'only' else '-or-later'
        result.append(identifier)
    return result


def interview_license() -> dict:
    """Collect optional content licensing separately from software licensing."""
    result = {'software': interview_software()}
    if not result['software']:
        result['custom_terms'] = input('Pending license decision or custom terms to obtain [unspecified]: ').strip()
    print('\nContent licensing applies to named documentation, artwork, or data paths.')
    print('Creative Commons recommends software-specific licenses for code. These choices apply only to content.')
    print('  0. No separate content license. Keep the project terms or pending decision.')
    for number, identifier in enumerate(CONTENT, 1):
        print(f'  {number}. {identifier}')
    print('BY: attribution. SA: share alike. NC: noncommercial. ND: no derivatives. CC0: public-domain dedication.')
    answer = choose('Content license [0]: ', {str(n) for n in range(len(CONTENT) + 1)}, '0')
    if answer != '0':
        result['content'] = CONTENT[int(answer) - 1]
        result['content_paths'] = [p.strip() for p in input('Covered content paths, separated by commas: ').split(',')]
    return validate_license(result)


def validate_license(value: dict) -> dict:
    """Require exact supported terms and explicit content paths without guessing legal choices."""
    if not isinstance(value, dict) or set(value) - {'software', 'content', 'content_paths', 'custom_terms'}:
        raise ValueError('License must contain software, optional content/content_paths, or pending custom_terms.')
    software = value.get('software')
    if not isinstance(software, list) or not all(isinstance(item, str) for item in software):
        raise ValueError('license.software must be a list of exact license identifiers, or [] for pending terms.')
    if len(set(software)) != len(software) or not set(software) <= SOFTWARE_IDS:
        raise ValueError('Use distinct supported software identifiers, including GNU -only or -or-later suffixes.')
    content, paths = value.get('content'), value.get('content_paths', [])
    if content is not None and content not in CONTENT:
        raise ValueError('Select an exact supported Creative Commons identifier for content.')
    if not isinstance(paths, list) or bool(content) != bool(paths):
        raise ValueError('A content license requires explicit content_paths. Paths require a content license.')
    for path in paths:
        if (not isinstance(path, str) or not path.strip() or Path(path).is_absolute()
                or any(p in {'..', '.git', 'instructions', 'scripts', 'LICENSES'} for p in Path(path).parts)
                or path in {'.', '*', '**'} or any(c in path for c in '\n\r`<>\\')):
            raise ValueError('Content paths must name project content, not parent paths or inherited library files.')
    pending = value.get('custom_terms', '')
    if not isinstance(pending, str) or '\n' in pending or '\r' in pending or len(pending) > 500:
        raise ValueError('custom_terms must be a short, single-line pending decision.')
    if pending and software:
        raise ValueError('Custom/commercial terms need a separate review. Do not claim an incomplete dual license.')
    return {'software': software, 'content': content, 'content_paths': paths, 'custom_terms': pending}


def term_bytes(identifier: str, owner: str, year: str) -> bytes:
    """Verify pinned source bytes and fill only MIT's designated attribution placeholders."""
    name = identifier.replace('-or-later', '-only') + '.txt'
    records = json.loads((LICENSE_ROOT / 'sources.json').read_text())
    data = (LICENSE_ROOT / name).read_bytes()
    if hashlib.sha256(data).hexdigest() != records[name]['sha256']:
        raise ValueError(f'Bundled license checksum mismatch: {name}')
    if identifier == 'MIT':
        return data.decode().replace('<year>', year).replace('<copyright holders>', owner).encode()
    return data


def license_notice(choice: dict, owner: str, year: str) -> str:
    """State project scope and alternative terms without changing the bundled license documents."""
    lines = ['Project licensing', '', f'Copyright (c) {year} {owner}', '']
    if choice['software']:
        lines += ['New project software and documentation, except the content paths listed below,',
                  'are licensed under:', 'SPDX-License-Identifier: ' + ' OR '.join(choice['software']), '']
        if len(choice['software']) > 1:
            lines += ['You may choose any one of these licenses. These are alternatives, not cumulative terms.', '']
        lines += [f'Full terms: LICENSES/{identifier}.txt' for identifier in choice['software']]
    else:
        lines += ['TODO: Select and apply the license for new project software and documentation.',
                  'This file does not grant a license for that project material.', choice['custom_terms']]
    if choice['content']:
        lines += ['', 'Separate content license: ' + choice['content'],
                  'Covered paths: ' + ', '.join(choice['content_paths']),
                  'Full terms: LICENSES/' + choice['content'] + '.txt']
    lines += ['', 'Existing third-party notices and explicitly licensed files take precedence.',
              'The copied instruction library and tooling retain their MIT notices.',
              'See instructions/LICENSE and THIRD_PARTY_NOTICES.md.', '']
    return '\n'.join(lines)


def license_files(value: dict, owner: str, year: str) -> dict[str, bytes]:
    """Build all required terms, including GPLv3 for LGPLv3, without a network dependency."""
    choice = validate_license(value)
    identifiers = set(choice['software'])
    if choice['content']:
        identifiers.add(choice['content'])
    if any(identifier.startswith('LGPL-3.0') for identifier in identifiers):
        identifiers.add('GPL-3.0-only')
    if len(identifiers) == 1 and len(choice['software']) == 1:
        identifier = choice['software'][0]
        notice = license_notice(choice, owner, year).replace(
            f'Full terms: LICENSES/{identifier}.txt', 'Full license terms follow below.')
        return {'LICENSE': notice.encode() + b'\n' + term_bytes(identifier, owner, year)}
    result = {f'LICENSES/{identifier}.txt': term_bytes(identifier, owner, year)
              for identifier in sorted(identifiers)}
    result['LICENSE'] = license_notice(choice, owner, year).encode()
    return result
