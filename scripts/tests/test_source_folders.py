#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: cec7128a-7a19-4e82-b138-cfc315cdad80
# Created: 2026

# COMPONENT: Source-folder bootstrap tests
# PURPOSE: Verify previewed folder creation and preflight path protection through the CLI.
# RELATES: source_folders.py, configure_instructions.py

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'configure-instructions.sh'
PROFILE = 'PROJECT_PROFILE.md'


class SourceFolderTests(unittest.TestCase):
    """Keep source paths distinct from approved directory-creation metadata."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'repo'
        self.root.mkdir()
        self.component = dict(enabled=True, targets=['tools'], source_paths=['src/tool/helper'],
                              source_folders=['src/tool/helper'], source_state='planned', languages=['Go'],
                              platforms=['macOS'], deployment='CLI binary', saas_client=False, sdk_component='none')

    def run_cli(self, *flags, input_text=None):
        path = Path(self.directory.name) / 'answers.json'
        path.write_text(json.dumps({'components': {'helper': self.component}}))
        return subprocess.run(['bash', str(SCRIPT), '--root', str(self.root), '--answers', str(path), *flags],
                              input=input_text, text=True, capture_output=True, timeout=20)

    def test_apply_creates_only_approved_source_folders_and_parents(self):
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'src/tool/helper').is_dir())
        self.assertEqual(list((self.root / 'src/tool/helper').iterdir()), [])
        self.assertIn('Create source folder src/tool/helper', result.stdout)
        self.assertIn('Source folders: src/tool/helper', (self.root / PROFILE).read_text())
        self.assertFalse((self.root / 'src/app').exists())

    def test_dry_run_and_cancellation_create_no_files_or_directories(self):
        for flags, answer in [(('--dry-run',), None), ((), 'no\n')]:
            result = self.run_cli(*flags, input_text=answer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Create source folder', result.stdout)
            self.assertEqual(list(self.root.iterdir()), [])

    def test_planned_file_is_not_created_as_a_directory(self):
        self.component.update(source_paths=['src/main.go'], source_folders=[])
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'src').exists())

    def test_unselected_component_creates_no_source_folder(self):
        self.component['enabled'] = False
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'src').exists())

    def test_invalid_folder_plans_fail_before_writes(self):
        for folders in [['../escape'], ['.git/hooks'], ['src/*'], ['unselected'], ['src/tool/helper', 'AGENTS.md']]:
            with self.subTest(folders=folders):
                self.component['source_folders'] = folders
                result = self.run_cli('--apply')
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertEqual(list(self.root.iterdir()), [])

    def test_folder_conflict_with_planned_instruction_file_fails_before_writes(self):
        self.component.update(source_paths=['AGENTS.md/child'], source_folders=['AGENTS.md/child'])
        result = self.run_cli('--apply')
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_file_and_symlink_conflicts_fail_before_writes(self):
        (self.root / 'occupied').write_text('preserve')
        (self.root / 'linked').symlink_to(Path(self.directory.name))
        for path in ['occupied/child', 'occupied', 'linked/child']:
            with self.subTest(path=path):
                self.component.update(source_paths=[path], source_folders=[path])
                result = self.run_cli('--apply')
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertEqual((self.root / 'occupied').read_text(), 'preserve')
                self.assertFalse((self.root / PROFILE).exists())

    def test_deleted_bootstrapped_folder_fails_read_only_check(self):
        self.assertEqual(self.run_cli('--apply').returncode, 0)
        (self.root / 'src/tool/helper').rmdir()
        result = subprocess.run(['bash', str(SCRIPT), '--root', str(self.root), '--check'],
                                text=True, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertFalse((self.root / 'src/tool/helper').exists())
