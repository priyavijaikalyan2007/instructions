#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 79f39b4e-d1fd-4c36-8215-c81175cdba60
# Created: 2026

# COMPONENT: New project initialization tests
# PURPOSE: Verify real CLI setup, inherited content removal, and project-owned content preservation.
# RELATES: scripts/project_initialization.py, scripts/license_selection.py

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


LIBRARY = Path(__file__).resolve().parents[2]
SCRIPT = LIBRARY / 'scripts/configure-instructions.sh'
PROFILE = 'PROJECT_PROFILE.md'


class ProjectInitializationTests(unittest.TestCase):
    """Exercise copied repositories without changing the instruction library or using the network."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'utilextensions'
        self.root.mkdir()
        self.identity = {'name': 'utilextensions', 'owner': 'Example Owner', 'year': '2026',
                         'repository_url': 'https://github.com/example/utilextensions',
                         'description': 'Writing tools', 'license': {'software': ['MIT']}}
        self.profile = {'components': {'extension': {
            'enabled': True, 'source_paths': ['src'], 'targets': ['browser-extensions'],
            'languages': ['TypeScript'], 'platforms': ['Chrome'], 'saas_client': False,
            'sdk_component': 'none', 'deployment': 'browser package'}}}
        (self.root / 'src').mkdir()

    def run_cli(self, *flags, identity=True, input_text=None):
        """Run initialization with JSON selections through the public entry point."""
        command = ['bash', str(SCRIPT), '--root', str(self.root), '--initialize-project', *flags]
        if identity:
            path = Path(self.directory.name) / 'project.json'
            path.write_text(json.dumps(self.identity))
            command.extend(['--project-answers', str(path)])
        path = Path(self.directory.name) / 'profile.json'
        path.write_text(json.dumps(self.profile))
        command.extend(['--answers', str(path)])
        return subprocess.run(command, text=True, input=input_text, capture_output=True, timeout=20)

    def inherit(self):
        """Reproduce GitHub template copying without its Git metadata."""
        for folder in ['instructions', '.github', 'agentknowledge', 'scripts']:
            if (LIBRARY / folder).exists():
                shutil.copytree(LIBRARY / folder, self.root / folder, ignore=shutil.ignore_patterns('__pycache__'))
        for name in ['LICENSE', 'AGENTS.md', 'CLAUDE.md', 'CODEX.md', 'GEMINI.md',
                     'PROJECT_PROFILE.md', 'PROJECT.md', 'ADDITIONAL.md', 'CONVERSATION.md', 'CHANGELOG.md',
                     'configure.sh', 'README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md']:
            shutil.copy2(LIBRARY / name, self.root / name)

    def snapshot(self):
        """Capture bytes to detect writes during preview, cancellation, and errors."""
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_initialize_copy_replaces_policies_and_resets_library_profile(self):
        self.inherit()
        original = (self.root / 'README.md').read_bytes()
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('utilextensions', (self.root / 'README.md').read_text())
        self.assertNotIn('Enterprise Bootstrap', (self.root / 'CONTRIBUTING.md').read_text())
        self.assertNotIn('48-72', (self.root / 'SECURITY.md').read_text())
        self.assertNotIn('instruction-library', (self.root / PROFILE).read_text())
        self.assertNotIn('refactor/scoped-guides', (self.root / 'PROJECT.md').read_text())
        self.assertEqual((self.root / '.instructions/template-backup/README.md').read_bytes(), original)
        self.assertFalse((self.root / 'agentknowledge/history.jsonl').exists())
        self.assertFalse((self.root / 'CONVERSATION.md').exists())
        self.assertEqual((self.root / 'instructions/LICENSE').read_bytes(), (LIBRARY / 'LICENSE').read_bytes())

    def test_dry_run_and_cancel_write_nothing(self):
        self.inherit()
        before = self.snapshot()
        for flags, answer in [(('--dry-run',), None), ((), 'no\n')]:
            result = self.run_cli(*flags, input_text=answer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.snapshot(), before)

    def test_legacy_inherited_public_documents_are_replaced_at_root_with_backups(self):
        self.inherit()
        github = self.root / '.github'
        github.mkdir(exist_ok=True)
        names = ['README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md']
        originals = {name: (self.root / name).read_bytes() for name in names}
        for name in names:
            (self.root / name).rename(github / name)
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in names:
            self.assertTrue((self.root / name).is_file())
            self.assertFalse((github / name).exists())
            self.assertEqual((self.root / '.instructions/template-backup' / name).read_bytes(), originals[name])
        self.assertIn('utilextensions', (self.root / 'README.md').read_text())

    def test_repeat_preserves_edits_and_custom_files(self):
        self.inherit()
        custom = self.root / 'CONTRIBUTING.md'
        custom.write_text('Our contribution process\n')
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(custom.read_text(), 'Our contribution process\n')
        self.assertIn('Preserve customized', result.stdout)
        readme = self.root / 'README.md'
        readme.write_text('Project overview edited by owner\n')
        before = self.snapshot()
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_custom_license_is_not_overwritten(self):
        (self.root / 'LICENSE').write_text('Custom existing license\n')
        before = self.snapshot()
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2)
        self.assertIn('LICENSE', result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_changed_license_requires_separate_review(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        before = self.snapshot()
        self.identity['license']['software'] = ['Apache-2.0']
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.snapshot(), before)

    def test_symlink_destination_fails_before_any_write(self):
        self.identity['license'] = {'software': ['MIT', 'Apache-2.0']}
        outside = Path(self.directory.name) / 'outside'
        outside.mkdir()
        (self.root / 'LICENSES').symlink_to(outside, target_is_directory=True)
        before = self.snapshot()
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(list(outside.iterdir()), [])

    def test_dual_license_and_cc_content_are_explicit(self):
        self.identity['license'] = {'software': ['MIT', 'Apache-2.0'],
                                    'content': 'CC-BY-SA-4.0', 'content_paths': ['docs']}
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        license_text = (self.root / 'LICENSE').read_text()
        self.assertIn('MIT OR Apache-2.0', license_text)
        self.assertIn('CC-BY-SA-4.0', license_text)
        self.assertIn('docs', license_text)
        self.assertTrue((self.root / 'LICENSES/Apache-2.0.txt').is_file())

    def test_unsafe_or_ambiguous_answers_fail_without_writes(self):
        cases = [{'software': ['GPL']}, {'software': ['MIT', 'MIT']},
                 {'software': ['CC-BY-4.0']}, {'software': ['MIT'], 'content': 'CC-BY-4.0'},
                 {'software': ['MIT'], 'content': 'CC-BY-4.0', 'content_paths': ['../outside']}]
        for choice in cases:
            self.identity['license'] = choice
            result = self.run_cli('--apply')
            self.assertEqual(result.returncode, 2, choice)
            self.assertEqual(self.snapshot(), {})

    def test_running_copied_script_uses_new_project_interview(self):
        self.inherit()
        script = self.root / 'scripts/configure-instructions.sh'
        command = ['bash', str(script), '--root', str(self.root)]
        answers = '\n'.join(['1', '', 'Example Owner', '2026',
                             'https://github.com/example/utilextensions', 'Writing tools', *[''] * 6,
                             '1', '0', 'none', '8', '1', '2', '1', '2', 'src', 'yes'])
        result = subprocess.run(command, input=answers, text=True, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("This is the instruction library's own repository", result.stdout)
        self.assertIn('utilextensions', (self.root / 'README.md').read_text())

    def test_copied_script_initializes_docs_with_absent_source_paths(self):
        self.inherit()
        command = ['bash', str(self.root / 'scripts/configure-instructions.sh'), '--root', str(self.root)]
        answers = ['1', '', 'Example Owner', '2026', 'https://github.com/example/utilextensions',
                   'Writing tools', *[''] * 6, '1', '0', 'none', '7', '1', '1', '1', '1',
                   '1,2,3,5', 'src/docs', 'yes', 'yes']
        result = subprocess.run(command, input='\n'.join(answers) + '\n', text=True,
                                capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Workspace model: editor', (self.root / PROFILE).read_text())
        self.assertIn('Source state: planned', (self.root / PROFILE).read_text())
        self.assertTrue((self.root / 'src/docs').is_dir())
        self.assertTrue((self.root / '.instructions/INITIALIZATION.json').exists())

    def test_source_detection_does_not_require_installed_git(self):
        import sys
        from unittest.mock import patch
        sys.path.insert(0, str(SCRIPT.parent))
        from project_initialization import is_source_repository
        (self.root / '.git').mkdir()
        with patch('project_initialization.subprocess.run', side_effect=FileNotFoundError):
            self.assertFalse(is_source_repository(self.root))

    def test_source_detection_does_not_treat_a_nested_target_as_the_library(self):
        import sys
        from unittest.mock import patch
        sys.path.insert(0, str(SCRIPT.parent))
        from project_initialization import is_source_repository
        (self.root / '.git').mkdir()
        child = self.root / 'local-trial'
        child.mkdir()
        reply = subprocess.CompletedProcess([], 0, stdout='git@github.com:priyavijaikalyan2007/instructions.git\n')
        with patch('project_initialization.subprocess.run', return_value=reply):
            self.assertTrue(is_source_repository(self.root))
            self.assertFalse(is_source_repository(child))

    def test_source_repository_initialization_is_rejected(self):
        self.root = LIBRARY
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2)
        self.assertIn('source instruction repository', result.stderr)

    def test_custom_records_and_profile_notes_are_preserved(self):
        self.inherit()
        profile = self.root / PROFILE
        profile.write_text(profile.read_text() + '\nOwner notes must survive.\n')
        history = self.root / 'agentknowledge/history.jsonl'
        history.write_text(history.read_text() + '{"task":"Project work"}\n')
        before = history.read_bytes()
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Owner notes must survive.', profile.read_text())
        self.assertEqual(history.read_bytes(), before)

    def test_new_project_with_pending_license_can_initialize(self):
        self.identity['license'] = {'software': []}
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('TODO', (self.root / 'LICENSE').read_text())
        self.assertTrue((self.root / 'instructions/LICENSE').is_file())

    def test_dry_run_without_answers_has_no_interview_or_writes(self):
        result = self.run_cli('--dry-run', identity=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn('--project-answers', result.stderr)
        self.assertEqual(self.snapshot(), {})

    def test_backup_conflict_aborts_without_writes(self):
        self.inherit()
        backup = self.root / '.instructions/template-backup/README.md'
        backup.parent.mkdir(parents=True)
        backup.write_text('Unrelated earlier backup')
        before = self.snapshot()
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.snapshot(), before)

    def test_existing_license_alias_blocks_conflicting_license(self):
        (self.root / 'LICENSE.md').write_text('Existing project license')
        before = self.snapshot()
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.snapshot(), before)

    def test_custom_project_file_locations_are_respected(self):
        self.inherit()
        profile = self.root / PROFILE
        profile.write_text(profile.read_text().replace('PROJECT.md', 'docs/PROJECT.md')
                           .replace('ADDITIONAL.md', 'docs/LOCAL.md'))
        (self.root / 'docs').mkdir()
        facts = self.root / 'docs/PROJECT.md'
        facts.write_text('Actual project facts\n')
        (self.root / 'docs/LOCAL.md').write_text('Actual local instructions\n')
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('docs/PROJECT.md', (self.root / 'README.md').read_text())
        self.assertEqual(facts.read_text(), 'Actual project facts\n')

    def test_generated_documents_link_to_existing_files(self):
        import re
        from urllib.parse import unquote
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        documents = list((self.root / '.github').glob('*.md'))
        documents.extend(self.root.glob('*.md'))
        for path in documents:
            for target in re.findall(r'\]\(<?([^\s)>]+)>?\)', path.read_text()):
                if target.startswith(('https:', 'http:', '#')):
                    continue
                resolved = path.parent / unquote(target.split('#')[0])
                self.assertTrue(resolved.exists(), f'{path.name}: {target}')
