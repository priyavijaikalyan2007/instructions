#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: b5f1b4aa-7121-4126-9943-04f7f0c05c96
# Created: 2026

# COMPONENT: Project bootstrap verification
# PURPOSE: Exercise usable placeholders, environment selection, completion steps, and captured business facts.
# RELATES: project_scaffolding.py, project_initialization.py

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'configure-instructions.sh'


class ProjectScaffoldingTests(unittest.TestCase):
    """Verify generated project entry points without performing builds or remote operations."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'project'
        self.identity = dict(name='example', owner='Example Owner', year='2026', repository_url='none',
                             description='A useful product.', license={'software': ['MIT']}, business_context=dict(
                             users='Technical writers', problem='Manual document cleanup', value='Less editing time',
                             scope='Docs and browser extensions', success_criteria='Fewer manual changes',
                             constraints='Works offline where possible'))
        self.component = dict(enabled=True, source_paths=['src/service/core/backend'],
                              source_folders=['src/service/core/backend'], source_state='planned', targets=['backend'],
                              languages=['Java'], platforms=['server'], deployment='container', saas_client=False,
                              sdk_component='none')

    def run_cli(self, *flags, input_text=None):
        command = ['bash', str(SCRIPT), '--target-folder', str(self.root), *flags]
        for flag, name, value in [('--project-answers', 'identity', self.identity),
                                   ('--answers', 'profile', {'components': {'component': self.component}})]:
            path = Path(self.directory.name) / f'{name}.json'
            path.write_text(json.dumps(value))
            command.extend([flag, str(path)])
        return subprocess.run(command, input=input_text, text=True, capture_output=True, timeout=20)

    def test_backend_has_common_scripts_and_three_documented_environments(self):
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ['build', 'test', 'clean', 'run', 'smoke', 'deploy', 'monitor', 'logs', 'migrate', 'runsql']:
            script = self.root / f'{name}.sh'
            self.assertTrue(script.is_file(), name)
            self.assertTrue(script.stat().st_mode & 0o111, name)
            self.assertEqual(subprocess.run(['bash', '-n', str(script)], capture_output=True).returncode, 0)
            run = subprocess.run([str(script)], capture_output=True, text=True, timeout=5)
            self.assertEqual(run.returncode, 2, name)
            self.assertIn('TODO', run.stderr)
        setup = (self.root / 'SETUP.md').read_text()
        for text in ['test', 'local machine', 'dev', 'staging', 'prod', 'production', 'build.sh', 'PROJECT.md']:
            self.assertIn(text, setup)
        self.assertIn('SETUP.md', result.stdout)
        self.assertIn('Next steps', result.stdout)

    def test_business_context_is_rendered_as_facts_without_changing_shared_guides(self):
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        project = (self.root / 'PROJECT.md').read_text()
        for value in self.identity['business_context'].values():
            self.assertIn(value, project)
        self.assertIn('Technical writers', (self.root / 'README.md').read_text())
        self.assertEqual((self.root / 'instructions/REPO.md').read_bytes(),
                         (SCRIPT.parents[1] / 'instructions/REPO.md').read_bytes())

    def test_placeholder_environment_help_and_invalid_input_do_no_work(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        script = self.root / 'deploy.sh'
        for environment in ['test', 'dev', 'prod']:
            run = subprocess.run([str(script), environment], capture_output=True, text=True, timeout=5)
            self.assertEqual(run.returncode, 2)
            self.assertIn(environment, run.stderr)
        self.assertEqual(subprocess.run([str(script), '--help'], capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run([str(script), 'unknown'], capture_output=True).returncode, 2)
        self.assertEqual(subprocess.run([str(script), 'prod', 'extra'], capture_output=True).returncode, 2)

    def test_dry_run_cancel_and_existing_scripts_are_preserved(self):
        for flags, answer in [(('--dry-run',), None), ((), 'no\n')]:
            result = self.run_cli(*flags, input_text=answer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(self.root.exists())
        self.root.mkdir()
        script = self.root / 'build.sh'
        script.write_text('#!/bin/bash\n# Owner implementation\nexit 0\n')
        script.chmod(0o755)
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.assertIn('Owner implementation', script.read_text())
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        self.assertIn('Owner implementation', script.read_text())

    def test_standalone_targets_skip_database_scripts_and_keep_relevant_entry_points(self):
        self.component.update(source_paths=['src/tool/example'], source_folders=['src/tool/example'], targets=['tools'],
                              languages=['Go'], platforms=['Linux'], deployment='CLI binary')
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'build.sh').is_file())
        self.assertTrue((self.root / 'package.sh').is_file())
        for name in ['migrate.sh', 'runsql.sh', 'deploy.sh', 'monitor.sh', 'logs.sh']:
            self.assertFalse((self.root / name).exists(), name)

    def test_setup_checklist_cannot_overwrite_a_configured_facts_file(self):
        self.root.mkdir()
        template = SCRIPT.parents[1] / 'instructions/PROJECT_PROFILE_TEMPLATE.md'
        profile = self.root / 'PROJECT_PROFILE.md'
        profile.write_text(template.read_text().replace('`PROJECT.md`', '`SETUP.md`'))
        before = profile.read_bytes()
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(self.root.iterdir()), [profile])
        self.assertEqual(profile.read_bytes(), before)

    def test_invalid_business_context_fails_before_any_write(self):
        for context in [{'users': 'bad\nline'}, {'unknown': 'Something'}, {'users': ['not text']}]:
            self.identity['business_context'] = context
            result = self.run_cli('--apply')
            self.assertEqual(result.returncode, 2)
            self.assertFalse(self.root.exists())
