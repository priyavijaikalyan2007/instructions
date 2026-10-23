#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 546d0178-a24f-4dcc-b20e-145f234256ef
# Created: 2026

# COMPONENT: Workspace interview integration tests
# PURPOSE: Verify product-specific setup and explicit planned scope through the public CLI.
# RELATES: workspace_profile.py, configure_instructions.py
# FLOW: Temporary repository -> interview or JSON -> preview, preservation, and guide assertions.

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'configure-instructions.sh'
PROFILE = 'PROJECT_PROFILE.md'


class WorkspaceProfileTests(unittest.TestCase):
    """Exercise first setup and repeat edits without remote Google operations."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'repo'
        self.root.mkdir()

    def run_cli(self, lines=None, answers=None, flags=()):
        """Run the real entry point with isolated input and bounded execution."""
        command = ['bash', str(SCRIPT), '--root', str(self.root), *flags]
        if answers is not None:
            path = Path(self.directory.name) / 'answers.json'
            path.write_text(json.dumps(answers))
            command.extend(['--answers', str(path)])
        if lines is not None and not (self.root / PROFILE).exists():
            lines = ['none', *lines]
        return subprocess.run(command, input=None if lines is None else '\n'.join(lines) + '\n',
                              text=True, capture_output=True, timeout=20)

    def docs_input(self, approval='yes'):
        """Select Docs Editor, personal testing, and planned source paths."""
        return ['7', '1', '1', '1', '1', '1,2,3,5',
                'src/docs/', 'yes', approval]

    def workspace_answers(self, **overrides):
        """Return an explicit typed setup for JSON and validation checks."""
        component = dict(enabled=True, targets=['google-workspace'], source_paths=['src/docs'],
                         source_state='planned', languages=['TypeScript', 'HTML', 'SCSS'],
                         platforms=['Google Docs'], deployment='Apps Script; test installation',
                         saas_client=False, sdk_component='none', workspace_model='editor',
                         workspace_runtime='apps-script', workspace_account='personal',
                         workspace_distribution='test')
        component.update(overrides)
        return {'components': {'workspace-extension': component}}

    def test_docs_setup_records_planned_scope_and_specific_build_guidance(self):
        result = self.run_cli(self.docs_input())
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = (self.root / PROFILE).read_text()
        for text in ['Workspace model: editor', 'Workspace runtime: apps-script', 'Workspace distribution: test',
                     'Platforms: Google Docs', 'Source state: planned',
                     'Languages: JavaScript, TypeScript, HTML, SCSS']:
            self.assertIn(text, profile)
        for text in ['appsscript.json', 'SCSS', 'HTML', 'clasp', 'Marketplace', 'OAuth']:
            self.assertIn(text, result.stdout)
        self.assertNotIn('Operating systems or platforms [', result.stdout)
        self.assertNotIn('Packaging or delivery [', result.stdout)
        self.assertTrue((self.root / 'src/docs').is_dir())
        self.assertEqual(self.run_cli(flags=['--check']).returncode, 0)

    def test_generated_scope_includes_each_language_and_excludes_future_hosts(self):
        result = self.run_cli(self.docs_input())
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = (self.root / 'AGENTS.md').read_text()
        for guide in ['google-workspace/GOOGLE_WORKSPACE.md', 'javascript/JAVASCRIPT.md',
                      'typescript/TYPESCRIPT.md', 'html/HTML.md', 'scss/SCSS.md', 'css/CSS.md']:
            self.assertIn(guide, agents)
        self.assertNotIn('backend/BACKEND.md', agents)
        self.assertNotIn('Gmail', (self.root / PROFILE).read_text())

    def test_gmail_workspace_http_records_backend_scope(self):
        lines = ['7', '2', '2', '2', '2', '2', '5', 'src/mail', 'yes', 'yes']
        result = self.run_cli(lines)
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = (self.root / PROFILE).read_text()
        self.assertIn('Workspace runtime: http', profile)
        self.assertIn('Workspace distribution: private', profile)
        self.assertIn('backend/BACKEND.md', (self.root / 'AGENTS.md').read_text())
        self.assertIn('card', result.stdout.lower())
        self.assertIn('HTTPS', result.stdout)
        self.assertNotIn('SCSS compilation', result.stdout)

    def test_invalid_editor_gmail_choice_is_explained_and_retried(self):
        lines = ['7', '2', '1', '2', '1', '1', '3', '2', 'src/mail', 'yes', 'no']
        result = self.run_cli(lines)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Editor add-ons support Docs, Sheets, Slides, and Forms', result.stdout)
        self.assertIn('public marketplace', result.stdout.lower())
        self.assertEqual(list(self.root.iterdir()), [])

    def test_personal_account_cannot_choose_domain_private_distribution(self):
        lines = self.docs_input('no')
        lines[4:5] = ['2', '1']
        result = self.run_cli(lines)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('organization account', result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_planned_json_dry_run_writes_nothing(self):
        result = self.run_cli(answers=self.workspace_answers(), flags=['--dry-run'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('planned source path', result.stderr)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_invalid_json_combinations_fail_before_writes(self):
        cases = [dict(workspace_runtime='http'), dict(platforms=['Gmail']),
                 dict(workspace_distribution='private'), dict(workspace_model='unknown'),
                 dict(workspace_account='unknown'), dict(source_state='typo'),
                 dict(source_paths=['../escape']), dict(source_paths=['src/*']),
                 dict(languages=['Python']), dict(workspace_runtime='')]
        for changes in cases:
            with self.subTest(changes=changes):
                result = self.run_cli(answers=self.workspace_answers(**changes), flags=['--apply'])
                self.assertEqual(result.returncode, 2)
                self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_paths_still_require_existence(self):
        result = self.run_cli(answers=self.workspace_answers(source_state='existing'), flags=['--apply'])
        self.assertEqual(result.returncode, 2)
        self.assertIn('source path does not exist', result.stderr)

    def test_repeated_interview_retains_choices_and_custom_notes(self):
        self.assertEqual(self.run_cli(self.docs_input()).returncode, 0)
        path = self.root / PROFILE
        path.write_text(path.read_text() + '\nOwner note: preserve this text.\n')
        before = path.read_bytes()
        result = self.run_cli([''] * 8)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(path.read_bytes(), before)
        self.assertIn('No changes.', result.stdout)

    def test_planned_symlink_is_rejected(self):
        (self.root / 'src').symlink_to(self.directory.name, target_is_directory=True)
        result = self.run_cli(answers=self.workspace_answers(), flags=['--apply'])
        self.assertEqual(result.returncode, 2)
        self.assertIn('Symlink', result.stderr)

    def test_forms_workspace_model_is_rejected(self):
        result = self.run_cli(answers=self.workspace_answers(
            platforms=['Google Forms'], workspace_model='workspace'), flags=['--apply'])
        self.assertEqual(result.returncode, 2)
        self.assertIn('Forms', result.stderr)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_planned_path_under_regular_file_is_rejected(self):
        (self.root / 'src').write_text('A file is not a source directory.')
        result = self.run_cli(answers=self.workspace_answers(), flags=['--apply'])
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / 'instructions').exists())

    def test_planned_source_scope_works_for_other_product_types(self):
        answers = self.workspace_answers()
        component = answers['components']['workspace-extension']
        for key in list(component):
            if key.startswith('workspace_'):
                del component[key]
        component.update(targets=['tools'], languages=['Go'], platforms=['macOS'])
        result = self.run_cli(answers=answers, flags=['--apply'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('tools/TOOLS.md', (self.root / 'AGENTS.md').read_text())

    def test_legacy_workspace_profile_remains_readable_with_setup_note(self):
        (self.root / 'src').mkdir()
        answers = self.workspace_answers(source_paths=['src'], source_state='existing')
        component = answers['components']['workspace-extension']
        for key in list(component):
            if key.startswith('workspace_'):
                del component[key]
        result = self.run_cli(answers=answers, flags=['--apply'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Workspace setup is legacy', result.stderr)
        self.assertEqual(self.run_cli(flags=['--check']).returncode, 0)

    def test_planned_scope_becomes_existing_when_sources_are_created(self):
        self.assertEqual(self.run_cli(answers=self.workspace_answers(), flags=['--apply']).returncode, 0)
        (self.root / 'src/docs').mkdir(parents=True)
        result = self.run_cli([''] * 7 + ['yes'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Source state: existing', (self.root / PROFILE).read_text())

    def test_javascript_cards_skip_typescript_and_stylesheet_build_steps(self):
        lines = ['7', '2', '2', '1', '1', '1', '1', 'src/mail', 'yes', 'no']
        result = self.run_cli(lines)
        self.assertEqual(result.returncode, 0, result.stderr)
        build = result.stdout.split('Build and packaging for these choices:', 1)[1]
        self.assertNotIn('Compile TypeScript', build)
        self.assertNotIn('SCSS compilation', build)

    def test_css_editor_does_not_require_scss_compilation(self):
        lines = self.docs_input('no')
        lines[5] = '1,3,4'
        result = self.run_cli(lines)
        self.assertEqual(result.returncode, 0, result.stderr)
        build = result.stdout.split('Build and packaging for these choices:', 1)[1]
        self.assertNotIn('SCSS compilation', build)

    def test_apps_script_runtime_selects_runtime_guide_for_javascript_and_typescript(self):
        for language in ['JavaScript', 'TypeScript']:
            with self.subTest(language=language):
                result = self.run_cli(answers=self.workspace_answers(languages=[language]), flags=['--apply'])
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('apps-script/APPS_SCRIPT.md', (self.root / 'AGENTS.md').read_text())

    def test_explicit_apps_script_aliases_select_javascript_and_runtime_guides(self):
        for language in ['Apps Script', 'Google Apps Script']:
            with self.subTest(language=language):
                answers = self.workspace_answers(languages=[language])
                for key in list(answers['components']['workspace-extension']):
                    if key.startswith('workspace_'):
                        del answers['components']['workspace-extension'][key]
                result = self.run_cli(answers=answers, flags=['--apply'])
                self.assertEqual(result.returncode, 0, result.stderr)
                agents = (self.root / 'AGENTS.md').read_text()
                self.assertIn('javascript/JAVASCRIPT.md', agents)
                self.assertIn('apps-script/APPS_SCRIPT.md', agents)

    def test_http_javascript_does_not_select_apps_script_runtime(self):
        answers = self.workspace_answers(workspace_model='workspace', workspace_runtime='http',
                                         languages=['JavaScript'], platforms=['Gmail'])
        result = self.run_cli(answers=answers, flags=['--apply'])
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = (self.root / 'AGENTS.md').read_text()
        self.assertIn('javascript/JAVASCRIPT.md', agents)
        self.assertIn('backend/BACKEND.md', agents)
        self.assertNotIn('apps-script/APPS_SCRIPT.md', agents)

    def test_check_requires_selected_apps_script_guide(self):
        self.assertEqual(self.run_cli(answers=self.workspace_answers(), flags=['--apply']).returncode, 0)
        guide = self.root / 'instructions/apps-script/APPS_SCRIPT.md'
        self.assertTrue(guide.exists())
        guide.unlink()
        result = self.run_cli(flags=['--check'])
        self.assertEqual(result.returncode, 2)
        self.assertIn('apps-script/APPS_SCRIPT.md', result.stderr)

    def test_switching_to_http_retires_runtime_scope_and_preserves_installed_guide(self):
        self.assertEqual(self.run_cli(answers=self.workspace_answers(), flags=['--apply']).returncode, 0)
        guide = self.root / 'instructions/apps-script/APPS_SCRIPT.md'
        self.assertTrue(guide.exists())
        original = guide.read_bytes()
        answers = self.workspace_answers(workspace_model='workspace', workspace_runtime='http',
                                         languages=['TypeScript'], platforms=['Gmail'])
        self.assertEqual(self.run_cli(answers=answers, flags=['--apply']).returncode, 0)
        self.assertNotIn('apps-script/APPS_SCRIPT.md', (self.root / 'AGENTS.md').read_text())
        self.assertEqual(guide.read_bytes(), original)

    def test_slash_language_names_select_both_guides_in_json(self):
        result = self.run_cli(answers=self.workspace_answers(languages=['Javascript/Typescript']), flags=['--apply'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('typescript/TYPESCRIPT.md', (self.root / 'AGENTS.md').read_text())
        self.assertNotIn('language coverage gap', result.stderr)


if __name__ == '__main__':
    unittest.main()
