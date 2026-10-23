#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: d581b96d-375b-43c0-bfe9-21bfb1d0c487
# Created: 2026

# COMPONENT: Per-tool role configuration tests
# PURPOSE: Verify selectable roles, managed scope, and native entry preservation.
# RELATES: agent_roles.py, configure_instructions.py

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'configure-instructions.sh'


class AgentRolesTests(unittest.TestCase):
    """Keep repository role choices independent of model vendors and instruction discovery."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'repo'
        self.root.mkdir()
        (self.root / 'src').mkdir()
        self.answers = {'agent_roles': {'claude': ['implementation', 'testing'],
                        'codex': {'roles': ['planning', 'review'], 'notes': 'Review API boundaries.'},
                        'pi': ['implementation'], 'roo': ['review'], 'cline': ['testing'],
                        'antigravity': ['documentation']}, 'components': {'tool': dict(
                        enabled=True, source_paths=['src'], targets=['tools'], languages=['Go'], platforms=['Linux'],
                        deployment='CLI binary', saas_client=False, sdk_component='none')}}

    def run_cli(self, *flags, answers=True, input_text=None):
        command = ['bash', str(SCRIPT), '--root', str(self.root), *flags]
        if answers:
            path = Path(self.directory.name) / 'roles.json'
            path.write_text(json.dumps(self.answers))
            command.extend(['--answers', str(path)])
        return subprocess.run(command, input=input_text, text=True, capture_output=True, timeout=20)

    def test_assignments_are_project_owned_and_roles_are_shared(self):
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = (self.root / 'PROJECT_PROFILE.md').read_text()
        for text in ['## Agent roles', 'implementation, testing', 'planning, review', 'Review API boundaries.']:
            self.assertIn(text, profile)
        self.assertTrue((self.root / 'instructions/AGENT_ROLES.md').is_file())
        self.assertIn('AGENT_ROLES.md', (self.root / 'AGENTS.md').read_text())
        roo = (self.root / '.roo/rules/00-project-instructions.md').read_text()
        self.assertIn('PROJECT_PROFILE.md', roo)
        self.assertFalse((self.root / 'PI.md').exists())
        self.assertNotIn('YOU ARE NOT TO MODIFY', (self.root / 'CODEX.md').read_text())

    def test_role_dry_run_and_cancellation_do_not_write(self):
        for flags, answer in [(('--dry-run',), None), ((), 'no\n')]:
            result = self.run_cli(*flags, input_text=answer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((self.root / 'PROJECT_PROFILE.md').exists())

    def test_custom_entry_files_and_unspecified_role_assignments_are_preserved(self):
        (self.root / 'CLAUDE.md').write_text('Owner instructions.\n')
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.assertEqual((self.root / 'CLAUDE.md').read_text(), 'Owner instructions.\n')
        self.answers = {}
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('planning, review', (self.root / 'PROJECT_PROFILE.md').read_text())

    def test_invalid_role_assignments_fail_before_any_write(self):
        for value in [{'codex': ['made-up-role']}, {'../escape': ['review']},
                      {'claude': {'roles': ['review'], 'notes': 'bad\nline'}}, {'codex': []}]:
            with self.subTest(value=value):
                self.answers['agent_roles'] = value
                result = self.run_cli('--apply')
                self.assertEqual(result.returncode, 2)
                self.assertFalse((self.root / 'instructions').exists())

    def test_role_only_edit_and_clear_keep_component_selections(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.answers = {}
        result = self.run_cli('--apply', '--configure-agents', input_text='2\n3,5\nAPI review\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = (self.root / 'PROJECT_PROFILE.md').read_text()
        self.assertIn('API review', profile)
        self.assertIn('Languages: Go', profile)
        self.assertNotIn('| claude |', profile)
        self.answers = {'agent_roles': {}}
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.assertNotIn('| codex |', (self.root / 'PROJECT_PROFILE.md').read_text())
        self.assertTrue((self.root / '.roo/rules/00-project-instructions.md').is_file())

    def test_role_only_interview_does_not_repeat_product_questions(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        result = self.run_cli('--configure-agents', '--dry-run', answers=False, input_text='2\n3,5\n\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('Product numbers', result.stdout)

    def test_known_inherited_entry_is_neutralized_with_exact_backup(self):
        import sys
        sys.path.insert(0, str(SCRIPT.parent))
        from agent_roles import agent_entry_changes
        library = Path(self.directory.name) / 'neutral-library'
        library.mkdir()
        for name in ['CLAUDE.md', 'CODEX.md', 'GEMINI.md']:
            (library / name).write_text('Neutral pointer: AGENTS.md and PROJECT_PROFILE.md.\n')
        original = (SCRIPT.parents[1] / 'CODEX.md').read_bytes()
        (self.root / 'CODEX.md').write_bytes(original)
        changes = agent_entry_changes(self.root, '', library)
        self.assertEqual(changes['.instructions/template-backup/CODEX.md'], original)
        self.assertEqual(changes['CODEX.md'], (library / 'CODEX.md').read_bytes())
        self.assertEqual((self.root / 'CODEX.md').read_bytes(), original)

    def test_new_interview_collects_multiple_roles_for_each_selected_tool(self):
        lines = ['1,2', '2,6', '', '3,5', '', '6', 'src', '2', '2', 'CLI binary', 'yes']
        result = self.run_cli(answers=False, input_text='\n'.join(lines) + '\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = (self.root / 'PROJECT_PROFILE.md').read_text()
        self.assertIn('implementation, testing', profile)
        self.assertIn('planning, review', profile)
        self.assertNotIn('founder and dreamer', (self.root / 'CODEX.md').read_text())
        self.assertIn('Choose the work Claude Code should normally handle', result.stdout)
        self.assertIn('Choose the work Codex should normally handle', result.stdout)
        self.assertIn('Space selects several roles', result.stdout)
        self.assertIn('Optional project notes for Codex', result.stdout)
