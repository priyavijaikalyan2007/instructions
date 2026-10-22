#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: f9bde609-f54e-486a-a13c-e8a8311477d0
# Created: 2026

# COMPONENT: Project root migration tests
# PURPOSE: Verify root ownership and lossless migration through the public CLI.
# RELATES: project_layout.py, configure_instructions.py

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'configure-instructions.sh'
PROJECT_FILES = ['PROJECT_PROFILE.md', 'PROJECT.md', 'ADDITIONAL.md', 'CONVERSATION.md', 'CHANGELOG.md']


class ProjectLayoutTests(unittest.TestCase):
    """Keep project-owned files distinct from installed shared instructions."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'repo'
        self.root.mkdir()
        (self.root / 'src').mkdir()
        self.answers = {'components': {'tool': dict(enabled=True, source_paths=['src'], targets=['tools'],
                        languages=['Go'], platforms=['Linux'], deployment='CLI binary',
                        saas_client=False, sdk_component='none')}}

    def run_cli(self, answers=None, *flags, input_text=None):
        command = ['bash', str(SCRIPT), '--root', str(self.root), *flags]
        if answers is not None:
            path = Path(self.directory.name) / 'answers.json'
            path.write_text(json.dumps(answers))
            command.extend(['--answers', str(path)])
        return subprocess.run(command, input=input_text, text=True, capture_output=True, timeout=20)

    def seed_legacy(self):
        self.assertEqual(self.run_cli(self.answers, '--apply').returncode, 0)
        folder = self.root / 'instructions/project'
        folder.mkdir(exist_ok=True)
        for name in PROJECT_FILES:
            source = self.root / name
            if source.exists():
                source.rename(folder / name)
        profile = folder / 'PROJECT_PROFILE.md'
        text = profile.read_text()
        for name in ['PROJECT.md', 'ADDITIONAL.md']:
            text = text.replace(f'`{name}`', f'`instructions/project/{name}`')
        text = text.replace('](instructions/REPO.md#', '](../REPO.md#')
        text = text.replace('](instructions/AGENT_ROLES.md)', '](../AGENT_ROLES.md)')
        profile.write_text(text)
        (folder / 'PROJECT.md').write_text('Owner facts: preserve café.\n\n[Style](../CODING_STYLE.md)\n')
        (folder / 'ADDITIONAL.md').write_text('Owner instruction: preserve this rule.\n')
        (folder / 'CONVERSATION.md').write_text('Historical path: instructions/project/PROJECT.md\n')
        (folder / 'CHANGELOG.md').write_text('Project release history.\n')

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_new_configuration_places_project_files_at_root(self):
        result = self.run_cli(self.answers, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ['PROJECT_PROFILE.md', 'PROJECT.md', 'ADDITIONAL.md']:
            self.assertTrue((self.root / name).is_file())
        self.assertFalse((self.root / 'instructions/project/PROJECT_PROFILE.md').exists())
        agents = (self.root / 'AGENTS.md').read_text()
        self.assertIn('Read `PROJECT_PROFILE.md`', agents)
        self.assertNotIn('instructions/project/', agents)

    def test_legacy_apply_moves_custom_documents_and_repairs_relative_links(self):
        self.seed_legacy()
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('preserve café', (self.root / 'PROJECT.md').read_text())
        self.assertIn('[Style](instructions/CODING_STYLE.md)', (self.root / 'PROJECT.md').read_text())
        self.assertEqual((self.root / 'ADDITIONAL.md').read_text(), 'Owner instruction: preserve this rule.\n')
        self.assertIn('Historical path: instructions/project/PROJECT.md', (self.root / 'CONVERSATION.md').read_text())
        for name in PROJECT_FILES:
            self.assertTrue((self.root / name).is_file())
            self.assertFalse((self.root / 'instructions/project' / name).exists())
        self.assertEqual(self.run_cli(None, '--check').returncode, 0)

    def test_migration_dry_run_cancel_and_check_do_not_write(self):
        self.seed_legacy()
        before = self.snapshot()
        for flags, answer in [(('--dry-run',), None), ((), 'no\n')]:
            result = self.run_cli({}, *flags, input_text=answer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.snapshot(), before)
        result = self.run_cli(None, '--check')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.snapshot(), before)

    def test_conflicting_root_and_legacy_files_stop_before_writes(self):
        self.seed_legacy()
        (self.root / 'PROJECT.md').write_text('A different root document.\n')
        before = self.snapshot()
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn('conflict', result.stderr.lower())
        self.assertEqual(self.snapshot(), before)

    def test_custom_context_paths_remain_authoritative(self):
        self.assertEqual(self.run_cli(self.answers, '--apply').returncode, 0)
        profile = self.root / 'PROJECT_PROFILE.md'
        text = profile.read_text().replace('`PROJECT.md`', '`local/facts.md`')
        profile.write_text(text)
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / 'local/facts.md').is_file())
        self.assertIn('`local/facts.md`', profile.read_text())

    def test_migration_updates_active_guide_references_without_replacing_custom_guidance(self):
        self.seed_legacy()
        guide = self.root / 'instructions/WORKFLOW.md'
        guide.write_text('Owner rule. Read instructions/project/PROJECT_PROFILE.md.\n')
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(guide.read_text(), 'Owner rule. Read PROJECT_PROFILE.md.\n')

    def test_migration_rebases_angle_links_with_spaces_and_reference_links(self):
        self.seed_legacy()
        (self.root / 'instructions/Style Notes.md').write_text('Style notes.\n')
        facts = self.root / 'instructions/project/PROJECT.md'
        facts.write_text('[Style](<../Style Notes.md>)\n\n[guide]: ../CODING_STYLE.md\n')
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (self.root / 'PROJECT.md').read_text()
        self.assertIn('[Style](<instructions/Style Notes.md>)', text)
        self.assertIn('[guide]: instructions/CODING_STYLE.md', text)

    def test_migration_preserves_private_project_file_permissions(self):
        self.seed_legacy()
        (self.root / 'instructions/project/PROJECT.md').chmod(0o600)
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / 'PROJECT.md').stat().st_mode & 0o777, 0o600)

    def test_legacy_state_and_backups_move_to_hidden_project_metadata(self):
        self.seed_legacy()
        folder = self.root / 'instructions/project'
        (folder / 'INITIALIZATION.json').write_text('{"version":1,"project":{}}\n')
        backup = folder / 'template-backup/original.md'
        backup.parent.mkdir()
        backup.write_text('Exact backup bytes.\n')
        backup.chmod(0o600)
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        state = self.root / '.instructions/INITIALIZATION.json'
        self.assertEqual(state.read_bytes(), b'{"version":1,"project":{}}\n')
        original_backup = self.root / '.instructions/template-backup/original.md'
        self.assertEqual(original_backup.read_bytes(), b'Exact backup bytes.\n')
        self.assertFalse((folder / 'INITIALIZATION.json').exists())
        self.assertEqual((self.root / '.instructions/template-backup/original.md').stat().st_mode & 0o777, 0o600)

    def seed_public_documents(self):
        self.assertEqual(self.run_cli(self.answers, '--apply').returncode, 0)
        github = self.root / '.github'
        github.mkdir(exist_ok=True)
        (github / 'README.md').write_text('Owner overview.\n[Policy](CONTRIBUTING.md)\n[Facts](../PROJECT.md)\n')
        (github / 'CONTRIBUTING.md').write_text('Owner policy.\n[Guide](../instructions/REPO.md)\n')
        (github / 'CODE_OF_CONDUCT.md').write_text('Owner conduct policy.\n')
        (github / 'SECURITY.md').write_text('Private reporting instructions.\n')
        (github / 'SECURITY.md').chmod(0o600)
        (github / 'workflows').mkdir()
        (github / 'workflows/build.yml').write_text('name: Keep this workflow\n')

    def test_public_documents_move_with_custom_content_links_and_permissions(self):
        self.seed_public_documents()
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ['README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md']:
            self.assertTrue((self.root / name).is_file())
            self.assertFalse((self.root / '.github' / name).exists())
        self.assertIn('[Policy](CONTRIBUTING.md)', (self.root / 'README.md').read_text())
        self.assertIn('[Facts](PROJECT.md)', (self.root / 'README.md').read_text())
        self.assertIn('[Guide](instructions/REPO.md)', (self.root / 'CONTRIBUTING.md').read_text())
        self.assertEqual((self.root / 'SECURITY.md').stat().st_mode & 0o777, 0o600)
        self.assertEqual((self.root / '.github/workflows/build.yml').read_text(), 'name: Keep this workflow\n')
        before = self.snapshot()
        self.assertEqual(self.run_cli({}, '--apply').returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_public_document_preview_cancel_and_check_preserve_files(self):
        self.seed_public_documents()
        before = self.snapshot()
        for flags, answer in [(('--dry-run',), None), ((), 'no\n')]:
            result = self.run_cli({}, *flags, input_text=answer)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.run_cli(None, '--check').returncode, 2)
        self.assertEqual(self.snapshot(), before)

    def test_public_document_source_scope_follows_the_move(self):
        self.seed_public_documents()
        profile = self.root / 'PROJECT_PROFILE.md'
        text = profile.read_text().replace('Source paths: src', 'Source paths: .github/README.md')
        profile.write_text(text.replace('Targets: tools', 'Targets: documentation').replace('Languages: Go',
                                                                                       'Languages: none'))
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Source paths: README.md', profile.read_text())
        self.assertEqual(self.run_cli(None, '--check').returncode, 0)

    def test_public_document_conflict_and_symlink_abort_before_writes(self):
        self.seed_public_documents()
        destination = self.root / 'README.md'
        destination.write_text('Different root overview.\n')
        before = self.snapshot()
        self.assertEqual(self.run_cli({}, '--apply').returncode, 2)
        self.assertEqual(self.snapshot(), before)
        destination.unlink()
        destination.symlink_to(self.root / 'PROJECT.md')
        before = self.snapshot()
        self.assertEqual(self.run_cli({}, '--apply').returncode, 2)
        self.assertEqual(self.snapshot(), before)

    def test_public_documents_cannot_be_repurposed_as_project_context(self):
        self.assertEqual(self.run_cli(self.answers, '--apply').returncode, 0)
        profile = self.root / 'PROJECT_PROFILE.md'
        profile.write_text(profile.read_text().replace('`PROJECT.md`', '`README.md`'))
        (self.root / 'README.md').write_text('Public introduction.\n')
        before = self.snapshot()
        result = self.run_cli({}, '--apply')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.snapshot(), before)
