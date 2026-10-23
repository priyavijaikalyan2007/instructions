#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 11eaf79b-092e-47fb-aeb2-eaa9eb74ef3c
# Created: 2026

# COMPONENT: Contextual profile selection tests
# PURPOSE: Verify supported choices, platform-dependent languages, and preserved project facts.
# RELATES: profile_choices.py, profile_interview.py, curses_interview.py

import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import profile_choices as choices


class ProfileChoiceTests(unittest.TestCase):
    """Keep new selections relevant without silently changing existing profiles."""

    def test_apple_native_languages_offer_swift_and_web_sources(self):
        options = choices.language_options('apps', ['iOS', 'iPadOS', 'macOS'])
        self.assertEqual(options, ['Swift', 'JavaScript', 'TypeScript', 'HTML', 'CSS', 'SCSS'])

    def test_android_native_choices_do_not_offer_apple_only_swift(self):
        self.assertEqual(choices.language_options('apps', ['Android', 'ChromeOS']),
                         ['Java', 'JavaScript', 'TypeScript', 'HTML', 'CSS', 'SCSS'])

    def test_tools_include_supported_cli_languages_without_web_markup(self):
        options = choices.language_options('tools', ['Windows'])
        self.assertTrue({'Python', 'Go', 'Rust', 'Shell'} <= set(options))
        self.assertFalse({'Swift', 'HTML', 'CSS', 'SCSS', 'Apps Script'} & set(options))

    def test_browser_frontend_and_website_share_actual_web_language_choices(self):
        for role in ['frontend', 'websites', 'static-assets']:
            with self.subTest(role=role):
                self.assertEqual(choices.language_options(role, ['browser']),
                                 ['JavaScript', 'TypeScript', 'HTML', 'CSS', 'SCSS'])

    def test_every_offered_language_has_installed_guidance(self):
        import configure_instructions as configurator
        for role in ['backend', 'frontend', 'apps', 'tools', 'sdks', 'custom']:
            for language in choices.language_options(role, ['iOS', 'Android', 'macOS']):
                with self.subTest(role=role, language=language):
                    self.assertIn(language.lower(), configurator.LANGUAGE_GUIDES)

    def test_platform_menu_retries_free_text_and_out_of_range_choices(self):
        with patch('builtins.input', side_effect=['iOS, macOS', '99', '1,2,3']), \
                patch('sys.stdout', new_callable=io.StringIO) as output:
            result = choices.select_platforms('apps', '')
        self.assertEqual(result, ['iOS', 'iPadOS', 'macOS'])
        self.assertIn('Choose the displayed numbers', output.getvalue())

    def test_language_menu_retries_free_text_and_deduplicates_choices(self):
        with patch('builtins.input', side_effect=['Swift', '1,3,4,6,1']), \
                patch('sys.stdout', new_callable=io.StringIO):
            result = choices.select_languages('apps', ['iOS'], '')
        self.assertEqual(result, ['Swift', 'TypeScript', 'HTML', 'SCSS'])

    def test_existing_case_and_aliases_become_numbered_defaults(self):
        with patch('builtins.input', return_value='') as ask, patch('sys.stdout', new_callable=io.StringIO):
            result = choices.select_languages('frontend', ['browser'], 'typescript, HTML, scss')
        self.assertEqual(result, ['TypeScript', 'HTML', 'SCSS'])
        self.assertIn('[2,3,5]', ask.call_args.args[0])

    def test_shared_parser_keeps_existing_non_javascript_json_spellings(self):
        self.assertEqual(choices.language_values('Bash, JAVA, Javascript/Typescript'),
                         ['Bash', 'JAVA', 'JavaScript', 'TypeScript'])

    def test_existing_unlisted_platform_requires_explicit_keep_or_replacement(self):
        with patch('builtins.input', side_effect=['']) as ask, patch('sys.stdout', new_callable=io.StringIO):
            result = choices.select_platforms('tools', 'configured development environments')
        self.assertEqual(result, ['configured development environments'])
        self.assertIn('[4]', ask.call_args.args[0])

    def test_existing_assets_without_source_languages_remain_explicitly_preservable(self):
        with patch('builtins.input', side_effect=['']), patch('sys.stdout', new_callable=io.StringIO):
            result = choices.select_languages('static-assets', ['browser'], 'none')
        self.assertEqual(result, ['none'])

    def test_existing_unlisted_languages_can_be_replaced_without_a_free_text_escape(self):
        with patch('builtins.input', side_effect=['3,1', '2']), \
                patch('sys.stdout', new_callable=io.StringIO) as output:
            result = choices.select_languages('workspace-cards', [], 'Kotlin')
        self.assertEqual(result, ['TypeScript'])
        self.assertIn('Keep existing', output.getvalue())
        self.assertIn('Select Keep existing alone', output.getvalue())

    def test_script_languages_require_executable_source(self):
        with patch('builtins.input', side_effect=['3,4', '2,3,5']), \
                patch('sys.stdout', new_callable=io.StringIO) as output:
            result = choices.select_languages('workspace-html', [], '')
        self.assertEqual(result, ['TypeScript', 'HTML', 'SCSS'])
        self.assertIn('Include JavaScript or TypeScript', output.getvalue())

    def test_template_placeholder_does_not_become_a_legacy_language_default(self):
        current = '<actual languages, such as JavaScript, TypeScript, HTML, CSS, or SCSS>'
        with patch('builtins.input', return_value=''), patch('sys.stdout', new_callable=io.StringIO):
            result = choices.select_languages('browser-extensions', [], current)
        self.assertEqual(result, ['JavaScript', 'HTML', 'CSS'])

    def test_sdk_languages_exclude_markup_and_use_consumer_platforms(self):
        self.assertEqual(choices.language_options('sdks', ['iOS', 'browser']),
                         ['Swift', 'JavaScript', 'TypeScript', 'C#', 'Java', 'Go', 'Python', 'Rust'])

    def test_fixed_browser_components_do_not_ask_for_operating_systems(self):
        with patch('builtins.input') as ask, patch('sys.stdout', new_callable=io.StringIO):
            self.assertEqual(choices.select_platforms('static-assets', ''), ['browser'])
        ask.assert_not_called()

    def test_native_cli_interview_resolves_numbered_platforms_before_languages(self):
        script = Path(__file__).resolve().parents[2] / 'configure.sh'
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / 'src').mkdir()
            lines = ['none', '4', 'src', '1,2,3', '1,3,4,6', 'native application', 'yes']
            result = subprocess.run(['bash', str(script), '--root', folder, '--ui', 'plain'],
                                    input='\n'.join(lines) + '\n', text=True, capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            profile = (Path(folder) / 'PROJECT_PROFILE.md').read_text()
            self.assertIn('Platforms: iOS, iPadOS, macOS', profile)
            self.assertIn('Languages: Swift, TypeScript, HTML, SCSS', profile)
            self.assertIn('swift/SWIFT.md', (Path(folder) / 'AGENTS.md').read_text())
