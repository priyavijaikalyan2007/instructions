#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 9690720d-578b-43a0-bf2b-faa20bb2ab86
# Created: 2026

# COMPONENT: Profile-specific project scaffold
# PURPOSE: Generate safe operation placeholders and a project-owned completion checklist.
# RELATES: configure_instructions.py, instructions/PROJECT_SCAFFOLDING.md
# FLOW: Selected components -> missing operation scripts -> setup checklist and next steps.
# SECURITY: Preserve owner files. Placeholders never build, delete, deploy, publish, or access databases.

from pathlib import Path
import re
import uuid

from project_layout import safe_path
from terminal_ui import print


TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / 'instructions/templates/scripts'
ACTIONS = {'build': 'Build selected components and prepare their configured outputs.',
           'test': 'Run configured component and cross-component tests.',
           'clean': 'Remove only verified generated output owned by this project.',
           'run': 'Start selected components for development.',
           'smoke': 'Check configured critical paths in the selected target.',
           'deploy': 'Deploy prepared artifacts to an explicitly configured destination.',
           'monitor': 'Monitor configured service health and runtime signals.',
           'logs': 'Read configured service logs with sensitive-data controls.',
           'migrate': 'Apply reviewed database migrations for the selected service.',
           'runsql': 'Execute a reviewed SQL file against the selected database.',
           'package': 'Package configured components for their delivery channels.'}
EXTRA_ACTIONS = {'backend': {'run', 'smoke', 'deploy', 'monitor', 'logs', 'migrate', 'runsql'},
                 'saas': {'run', 'smoke', 'deploy', 'monitor', 'logs', 'migrate', 'runsql'},
                 'frontend': {'run', 'smoke'}, 'websites': {'run', 'smoke', 'deploy'},
                 'google-workspace': {'package', 'deploy', 'smoke'},
                 'browser-extensions': {'package', 'deploy', 'smoke'},
                 'apps': {'run', 'package'}, 'tools': {'run', 'package'}, 'sdks': {'package'}}


def selected_targets(profile: str) -> set[str]:
    """Read only enabled component targets from the profile's Components section."""
    region = re.search(r'^## Components\s*\n(.*?)(?=^## |\Z)', profile, re.M | re.S)
    targets = set()
    for block in re.split(r'^### ', region.group(1) if region else '', flags=re.M):
        if not re.search(r'^- \[[xX]\] Enabled\s*$', block, re.M):
            continue
        match = re.search(r'^- Targets: (.+)$', block, re.M)
        if match:
            targets.update(part.strip().strip('`') for part in match.group(1).split(','))
    return targets


def selected_actions(targets: set[str]) -> list[str]:
    """Add operation entry points by selected behavior without choosing a cloud or build tool."""
    if not targets - {'documentation'}:
        return []
    actions = {'build', 'test', 'clean'}
    for target in targets:
        actions.update(EXTRA_ACTIONS.get(target, set()))
    return [name for name in ACTIONS if name in actions]


def operation_script(action: str, backend: bool, project: str) -> bytes:
    """Render a self-contained shell placeholder with explicit help and non-successful default execution."""
    arguments = ('    if [[ $# -gt 1 ]]; then\n'
                 "        fail 'Use one environment: test, dev, or prod.' 2\n    fi\n"
                 '    local target_environment="${1:-test}"\n'
                 '    case "$target_environment" in\n'
                 '        test|dev|prod) ;;\n'
                 "        *) fail 'Unknown environment. Use test, dev, or prod.' 2 ;;\n    esac\n"
                 '    local environment_label=" in ${target_environment}"') if backend else (
                 '    if [[ $# -gt 0 ]]; then\n'
                 "        fail 'This placeholder accepts only --help.' 2\n    fi\n"
                 '    local environment_label=""')
    values = {'PROJECT': project, 'GUID': str(uuid.uuid4()), 'ACTION': action, 'PURPOSE': ACTIONS[action],
              'USAGE': ' [test|dev|prod]' if backend else '', 'ARGUMENTS': arguments,
              'ENVIRONMENT_HELP': 'test = local machine. dev = staging deployment. prod = production.' if backend
              else 'Configure project-specific options when you implement this operation.'}
    text = (TEMPLATE_ROOT / 'operation.sh.template').read_text()
    for key, value in values.items():
        text = text.replace('@@' + key + '@@', value)
    return text.encode()


def readiness_steps(context_paths: dict, actions: list[str]) -> list[tuple[str, str]]:
    """Name each project file and the decisions needed before real use."""
    paths = {template: path for path, template in context_paths.items()}
    steps = [('PROJECT_PROFILE.md', 'Confirm source paths, languages, delivery choices, and tool roles.'),
             (paths['PROJECT_TEMPLATE.md'], 'Complete business facts, architecture, commands, and environments.'),
             (paths['ADDITIONAL_TEMPLATE.md'], 'Record local refinements and project-specific exceptions.'),
             ('README.md', 'Write verified prerequisites, installation steps, and first-use instructions.'),
             ('CONTRIBUTING.md', 'Set contribution and validation rules.'),
             ('CODE_OF_CONDUCT.md', 'Set conduct rules and private reporting contacts.'),
             ('SECURITY.md', 'Set private vulnerability contacts and supported-version policy.'),
             ('LICENSE', 'Review the selected terms and copyright ownership.'),
             ('THIRD_PARTY_NOTICES.md', 'Add project dependency notices and verify attribution.')]
    steps.extend((action + '.sh', ACTIONS[action] + ' Replace the TODO with verified commands.')
                 for action in actions)
    return steps


def setup_document(context_paths: dict, actions: list[str], backend: bool) -> bytes:
    """Record a project-owned completion checklist rather than a claim that the setup is ready."""
    lines = ['<!--',
             'SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>',
             'SPDX-FileCopyrightText: 2026 Outcrop Inc', 'SPDX-License-Identifier: MIT',
             'File GUID: ' + str(uuid.uuid4()), 'Created: 2026', '-->', '',
             '<!-- AGENT: Project-owned setup completion checklist. -->', '', '# Project setup checklist', '',
             'This setup selects instructions and creates placeholders. It does not build or deploy the product.',
             'Complete these items before treating the project as ready.', '', '## Files to complete', '']
    for path, instruction in readiness_steps(context_paths, actions):
        lines.append(f'- [ ] `{path}`: {instruction}')
    lines += ['', '## Operation scripts', '', 'Run ./build.sh --help for usage when build.sh is present.',
              'Unimplemented operations log a TODO and exit with status 2. Help exits with status 0.',
              'Use status 1 for a failed operation. Report success only after actual work completes.',
              'Preserve owner implementations. Route root operations to the selected components.',
              'Add the actual options, prerequisites, credentials source, and output paths before implementation.']
    if backend:
        lines += ['', '## Backend environments', '', '| Name | Meaning | Configuration |', '| --- | --- | --- |',
                  '| test | local machine | TODO: Local services and database |',
                  '| dev | staging deployment | TODO: Staging destinations and secret references |',
                  '| prod | production | TODO: Production destinations and release approval rules |', '',
                  'These names define the model. No environment or credentials were provisioned.',
                  'Examples: ./build.sh test, ./smoke.sh dev, ./logs.sh prod.',
                  'Before enabling deployments or SQL, validate the target and document access and recovery.']
    return ('\n'.join(lines) + '\n').encode()


def scaffolding_changes(root: Path, profile: str, context_paths: dict) -> dict[str, bytes]:
    """Create only missing placeholders and leave existing operation scripts and checklists untouched."""
    targets = selected_targets(profile)
    actions = selected_actions(targets)
    backend = bool(targets & {'backend', 'saas'})
    project = re.search(r'^Repository: (.+)$', profile, re.M)
    changes = {action + '.sh': operation_script(action, backend, project.group(1) if project else root.name)
               for action in actions if not safe_path(root, action + '.sh').exists()}
    if not safe_path(root, 'SETUP.md').exists():
        changes['SETUP.md'] = setup_document(context_paths, actions, backend)
    return changes


def print_readiness(profile: str, context_paths: dict) -> None:
    """Keep completion work visible even when an owner preserves an existing checklist."""
    print('\nNext steps: complete these project files before real use:')
    for path, instruction in readiness_steps(context_paths, selected_actions(selected_targets(profile))):
        print(f'  {path}: {instruction}')
    print('  SETUP.md: Review the checklist and record completion. Setup has not verified a build or deployment.')
