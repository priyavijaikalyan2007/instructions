#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 44d2c561-b9e1-43b6-ac4d-b08e0d09e7b9
# Created: 2026

# COMPONENT: Local target-folder setup tests
# PURPOSE: Verify repeatable setup without a remote repository or pre-existing target.
# RELATES: configure_instructions.py, project_initialization.py

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'configure.sh'


class TargetFolderTests(unittest.TestCase):
    """Exercise the full local setup and prove that rejected previews do not create a target."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'not-created/project'
        self.identity = dict(name='local-example', owner='Example Owner', year='2026', repository_url='none',
                             description='Local template trial', license={'software': ['MIT']})
        self.answers = {'components': {'tool': dict(enabled=True, source_paths=['src/tool/example'],
                        source_folders=['src/tool/example'], source_state='planned', targets=['tools'],
                        languages=['Go'], platforms=['Linux'], deployment='CLI binary',
                        saas_client=False, sdk_component='none')}}

    def run_cli(self, *flags, input_text=None, json_answers=True):
        command = ['bash', str(SCRIPT), '--target-folder', str(self.root), *flags]
        if json_answers:
            for flag, name, value in [('--project-answers', 'identity', self.identity),
                                       ('--answers', 'profile', self.answers)]:
                path = Path(self.directory.name) / f'{name}.json'
                path.write_text(json.dumps(value))
                command.extend([flag, str(path)])
        return subprocess.run(command, input=input_text, text=True, capture_output=True, timeout=20)

    def test_full_local_setup_creates_root_documents_without_git_or_github(self):
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        for path in ['PROJECT_PROFILE.md', 'PROJECT.md', 'ADDITIONAL.md', 'AGENTS.md',
                     '.instructions/INITIALIZATION.json', 'README.md', 'LICENSE',
                     'configure.sh', 'scripts/configure-instructions.sh', 'scripts/configure_instructions.py',
                     'scripts/profile_choices.py']:
            self.assertTrue((self.root / path).is_file(), path)
        self.assertTrue((self.root / 'src/tool/example').is_dir())
        self.assertFalse((self.root / '.git').exists())
        self.assertIn('Local template trial', (self.root / 'README.md').read_text())
        for name in ['README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md']:
            self.assertTrue((self.root / name).is_file())
            self.assertFalse((self.root / '.github' / name).exists())

    def test_dry_run_and_cancel_leave_missing_target_and_parent_absent(self):
        for flags, answer in [(('--dry-run',), None), ((), 'no\n')]:
            result = self.run_cli(*flags, input_text=answer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(self.root.parent.exists())

    def test_repeat_target_setup_preserves_project_owned_content(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        project = self.root / 'PROJECT.md'
        project.write_text('Owner facts.\n')
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.assertEqual(project.read_text(), 'Owner facts.\n')

    def test_interactive_local_dry_run_works_without_repository_url(self):
        lines = ['', 'Example Owner', '2026', '', 'Local trial', *[''] * 6, '1', '0', 'none',
                 '6', '', '', '2', '2', 'CLI binary']
        result = self.run_cli('--dry-run', input_text='\n'.join(lines) + '\n', json_answers=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('PROJECT_PROFILE.md', result.stdout)
        self.assertFalse(self.root.parent.exists())

    def test_installed_script_can_edit_and_check_its_local_target(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        renamed = self.root.with_name('project with spaces')
        self.root.rename(renamed)
        script = renamed / 'configure.sh'
        result = subprocess.run([str(script), '--root', str(renamed), '--check'], cwd=self.directory.name,
                                text=True, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_existing_unprofiled_local_folder_preserves_owner_documents(self):
        self.root.mkdir(parents=True)
        (self.root / 'PROJECT.md').write_text('Owner facts.\n')
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / 'PROJECT.md').read_text(), 'Owner facts.\n')

    def test_initialized_target_migrates_public_documents_and_completion_links(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        names = ['README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md']
        github = self.root / '.github'
        github.mkdir(exist_ok=True)
        readme = self.root / 'README.md'
        readme.write_text('Owner introduction.\n[Facts](../PROJECT.md)\n[Policy](CONTRIBUTING.md)\n')
        for name in names:
            (self.root / name).rename(github / name)
        setup = self.root / 'SETUP.md'
        text = setup.read_text()
        for name in names:
            text = text.replace('`' + name + '`', '`.github/' + name + '`')
        setup.write_text(text)
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(self.run_cli('--dry-run').returncode, 0)
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes()
                                  for p in self.root.rglob('*') if p.is_file()})
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Owner introduction.', readme.read_text())
        self.assertIn('[Facts](PROJECT.md)', readme.read_text())
        for name in names:
            self.assertTrue((self.root / name).is_file())
            self.assertFalse((github / name).exists())
            self.assertNotIn('.github/' + name, setup.read_text())

    def test_changed_license_is_rejected_in_repeat_target_mode(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        before = (self.root / 'LICENSE').read_bytes()
        self.identity['license'] = {'software': ['Apache-2.0']}
        self.assertEqual(self.run_cli('--apply').returncode, 2)
        self.assertEqual((self.root / 'LICENSE').read_bytes(), before)

    def test_target_mode_rejects_the_source_library_before_any_write(self):
        self.root = SCRIPT.parent
        result = self.run_cli('--apply', json_answers=False, input_text='')
        self.assertEqual(result.returncode, 2)
        self.assertIn('source instruction repository', result.stderr)

    def test_interactive_fact_corrections_keep_accepted_answers(self):
        lines = ['', 'Example Owner', 'bad-year', '2026', 'bad-url', 'none', 'Local trial',
                 'bad|users', 'Writers', *[''] * 5, '1', '0', 'none',
                 '6', '', '', '2', '2', 'CLI binary']
        result = self.run_cli('--dry-run', input_text='\n'.join(lines) + '\n', json_answers=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Writers', result.stdout)
        self.assertIn('Example Owner', result.stdout)
        self.assertFalse(self.root.exists())

    def test_invalid_answers_and_symlink_targets_do_not_create_parent(self):
        self.answers['components']['tool']['source_paths'] = ['../escape']
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.root.parent.exists())
        link = Path(self.directory.name) / 'linked'
        link.symlink_to(Path(self.directory.name), target_is_directory=True)
        self.root = link
        self.assertEqual(self.run_cli('--apply').returncode, 2)
