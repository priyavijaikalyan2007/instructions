#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 62767d1f-d17c-4c25-baad-30613034e002
# Created: 2026

# COMPONENT: Browser interview regression tests
# PURPOSE: Verify concrete browser choices through the public CLI without browser deployment.
# RELATES: browser_profile.py, profile_interview.py

import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'configure-instructions.sh'
PROFILE = 'PROJECT_PROFILE.md'


class BrowserProfileTests(unittest.TestCase):
    """Exercise browser, language, release, and combined-product selections."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / 'repo'
        self.root.mkdir()

    def run_cli(self, lines=None, answers=None, flags=()):
        command = ['bash', str(SCRIPT), '--root', str(self.root), *flags]
        if answers is not None:
            path = Path(self.directory.name) / 'answers.json'
            path.write_text(json.dumps(answers))
            command.extend(['--answers', str(path)])
        if lines is not None and not (self.root / PROFILE).exists():
            lines = ['none', *lines]
        return subprocess.run(command, input=None if lines is None else '\n'.join(lines) + '\n',
                              text=True, capture_output=True, timeout=20)

    def browser_answers(self, **overrides):
        component = dict(enabled=True, targets=['browser-extensions'], source_paths=['src/extensions/browser/markdown'],
                         source_state='planned', languages=['TypeScript', 'HTML', 'CSS'],
                         platforms=['Chrome on macOS'], browser_targets=['chrome-macos'],
                         browser_distribution='store', deployment='Chrome Web Store',
                         saas_client=False, sdk_component='none')
        component.update(overrides)
        return {'components': {'browser-extension': component}}

    def test_browser_interview_records_browsers_platforms_and_store_delivery(self):
        result = self.run_cli(['8', '1,3', '2', '2', '2', '2,3,4', '', 'yes', 'yes'])
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = (self.root / PROFILE).read_text()
        for value in ['Browser targets: chrome-macos, firefox-macos', 'Browser distribution: store',
                      'Languages: TypeScript, HTML, CSS', 'Chrome Web Store', 'Mozilla Add-ons',
                      'src/extensions/browser/markdown']:
            self.assertIn(value, profile)
        for value in ['manifest.json', 'ZIP', 'icons', 'screenshots', 'privacy', 'web-ext', 'unpacked']:
            self.assertIn(value, result.stdout)
        for value in ['Operating systems or platforms [', 'Packaging or delivery [', 'Examples: Java, C#']:
            self.assertNotIn(value, result.stdout)
        self.assertNotIn('backend/BACKEND.md', (self.root / 'AGENTS.md').read_text())
        self.assertEqual(self.run_cli(flags=['--check']).returncode, 0)

    def test_combined_docs_browser_setup_has_independent_created_scopes(self):
        lines = ['7,8', '1', '1', '1', '3', '1', 'src/extensions/googleworkspace/markdown', 'yes',
                 '1', '2', '2', '2', 'src/extensions/browser/markdown', 'yes', 'yes']
        result = self.run_cli(lines)
        self.assertEqual(result.returncode, 0, result.stderr)
        for value in ['src/extensions/googleworkspace/markdown', 'src/extensions/browser/markdown']:
            self.assertTrue((self.root / value).is_dir())
        agents = (self.root / 'AGENTS.md').read_text()
        self.assertIn('apps-script/APPS_SCRIPT.md', agents)
        self.assertIn('browser-extensions/BROWSER_EXTENSIONS.md', agents)
        self.assertNotIn('scss/SCSS.md', agents)
        self.assertNotIn('backend/BACKEND.md', agents)
        self.assertIn('Create source folder', result.stdout)

    def test_safari_explains_wrapper_signing_assets_and_apple_distribution(self):
        result = self.run_cli(['8', '4', '1,2,3', '2', '1', '', 'yes', 'yes'])
        self.assertEqual(result.returncode, 0, result.stderr)
        for value in ['Xcode', 'Apple', 'sign', 'App Store', 'macOS', 'iOS', 'iPadOS']:
            self.assertIn(value, result.stdout)
        profile = (self.root / PROFILE).read_text()
        self.assertIn('safari-macos, safari-ios, safari-ipados', profile)
        self.assertNotIn('Languages: Swift', profile)

    def test_firefox_self_distribution_requires_signing(self):
        result = self.run_cli(['8', '3', '2,4', '3', '1', '', 'yes', 'no'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('signed XPI', result.stdout)
        self.assertIn('Android', result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_javascript_default_does_not_select_typescript_or_scss(self):
        result = self.run_cli(['8', '1', '2', '1', '', '', 'yes', 'yes'])
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = (self.root / 'AGENTS.md').read_text()
        self.assertIn('javascript/JAVASCRIPT.md', agents)
        self.assertNotIn('typescript/TYPESCRIPT.md', agents)
        self.assertNotIn('scss/SCSS.md', agents)
        self.assertIn('JavaScript: runs in the extension', result.stdout)
        self.assertIn('TypeScript: compiles to JavaScript', result.stdout)

    def test_chrome_cannot_select_firefox_only_self_distribution(self):
        result = self.run_cli(['8', '1', '2', '3', '2', '2', '', 'yes', 'no'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Firefox choice', result.stdout)
        self.assertIn('Chrome Web Store', result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_browser_language_prompt_rejects_free_text_source(self):
        result = self.run_cli(['8', '1', '2', '1', 'Apps Script', '1', '', 'yes', 'no'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Choose the displayed numbers', result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_invalid_browser_json_fails_before_any_writes(self):
        cases = [dict(browser_targets=['chrome-ios']), dict(browser_distribution='served by the backend'),
                 dict(browser_distribution='self-hosted'), dict(languages=['Python']),
                 dict(platforms=['browser']), dict(browser_targets=[])]
        for values in cases:
            with self.subTest(values=values):
                result = self.run_cli(answers=self.browser_answers(**values), flags=['--apply'])
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertEqual(list(self.root.iterdir()), [])

    def test_json_and_repeat_edits_preserve_typed_browser_selection(self):
        self.assertEqual(self.run_cli(answers=self.browser_answers(), flags=['--apply']).returncode, 0)
        result = self.run_cli(['', '', '', '', '', '', 'yes', 'no'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Browser targets: chrome-macos', (self.root / PROFILE).read_text())

    def test_overlapping_extension_scopes_receive_a_narrowing_warning(self):
        answers = self.browser_answers(source_paths=['src'])
        answers['components']['workspace-extension'] = dict(
            enabled=True, source_paths=['src/extensions/googleworkspace/markdown'], source_state='planned',
            targets=['google-workspace'], languages=['JavaScript'], platforms=['Google Docs'],
            workspace_model='editor', workspace_runtime='apps-script', workspace_account='personal',
            workspace_distribution='test', deployment='Apps Script', saas_client=False, sdk_component='none')
        result = self.run_cli(answers=answers, flags=['--dry-run'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('source scopes overlap', result.stderr)
        self.assertIn('src/extensions/browser/', result.stderr)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_legacy_browser_metadata_is_preserved_with_a_specific_warning(self):
        answers = self.browser_answers()
        component = answers['components']['browser-extension']
        del component['browser_targets']
        del component['browser_distribution']
        component.update(platforms=['browser'], deployment='served by the backend')
        result = self.run_cli(answers=answers, flags=['--apply'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('browser interview', result.stderr.lower())
        self.assertIn('Deployment: served by the backend', (self.root / PROFILE).read_text())
