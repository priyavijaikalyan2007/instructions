#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 96306e5c-6326-40eb-aa3a-7bc8e899c058
# Created: 2026

# COMPONENT: License selection tests
# PURPOSE: Verify exact terms, version choices, and separate content scopes.
# RELATES: scripts/license_selection.py

import hashlib
import io
from contextlib import redirect_stdout
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import license_selection as licenses


class LicenseSelectionTests(unittest.TestCase):
    """Validate bundled terms and application notices without accessing the network."""

    def test_catalog_bytes_match_pinned_sources(self):
        catalog = json.loads((licenses.LICENSE_ROOT / 'sources.json').read_text())
        for name, record in catalog.items():
            self.assertEqual(hashlib.sha256((licenses.LICENSE_ROOT / name).read_bytes()).hexdigest(), record['sha256'])
            self.assertIn('/v3.29.0/', record['source'])

    def test_gnu_variants_and_lgpl_companion_text(self):
        for identifier in ['GPL-2.0-only', 'GPL-2.0-or-later', 'GPL-3.0-only', 'GPL-3.0-or-later',
                           'LGPL-2.1-only', 'LGPL-2.1-or-later', 'LGPL-3.0-only', 'LGPL-3.0-or-later']:
            result = licenses.license_files({'software': [identifier]}, 'Example Owner', '2026')
            self.assertIn(identifier, result['LICENSE'].decode())
            terms = result.get(f'LICENSES/{identifier}.txt', result['LICENSE'])
            self.assertTrue(terms.endswith(licenses.term_bytes(identifier, 'Example Owner', '2026')))
            if identifier.startswith('LGPL-3.0'):
                self.assertIn('LICENSES/GPL-3.0-only.txt', result)

    def test_mit_fills_only_author_and_year(self):
        result = licenses.license_files({'software': ['MIT']}, 'Example Owner', '2026')
        expected = (licenses.LICENSE_ROOT / 'MIT.txt').read_text()
        expected = expected.replace('<year>', '2026').replace('<copyright holders>', 'Example Owner')
        self.assertTrue(result['LICENSE'].decode().endswith(expected))

    def test_single_license_keeps_full_terms_in_root_without_duplicate_folder(self):
        for identifier in ['MIT', 'Apache-2.0', 'GPL-3.0-or-later']:
            with self.subTest(identifier=identifier):
                result = licenses.license_files({'software': [identifier]}, 'Owner', '2026')
                self.assertEqual(set(result), {'LICENSE'})
                self.assertTrue(result['LICENSE'].endswith(licenses.term_bytes(identifier, 'Owner', '2026')))
                self.assertIn(identifier, result['LICENSE'].decode())

    def test_multiple_terms_retain_scoped_root_notice_and_license_directory(self):
        for choice in [{'software': ['MIT', 'Apache-2.0']},
                       {'software': ['MIT'], 'content': 'CC-BY-4.0', 'content_paths': ['docs']},
                       {'software': ['LGPL-3.0-only']}]:
            result = licenses.license_files(choice, 'Owner', '2026')
            self.assertTrue(any(path.startswith('LICENSES/') for path in result))
            self.assertIn('LICENSES/', result['LICENSE'].decode())

    def test_dual_interview_asks_exact_gnu_version_policy(self):
        with redirect_stdout(io.StringIO()), patch('builtins.input',
                                                 side_effect=['2,5', 'later', '2', 'docs, assets']):
            result = licenses.interview_license()
        self.assertEqual(result['software'], ['Apache-2.0', 'GPL-2.0-or-later'])
        self.assertEqual(result['content'], 'CC-BY-SA-4.0')
        self.assertEqual(result['content_paths'], ['docs', 'assets'])

    def test_pending_terms_do_not_claim_mit_for_new_code(self):
        result = licenses.license_files({'software': [], 'custom_terms': 'Commercial terms pending'}, 'Owner', '2026')
        self.assertIn('TODO', result['LICENSE'].decode())
        self.assertNotIn('SPDX-License-Identifier: MIT', result['LICENSE'].decode())
        self.assertIn('Commercial terms pending', result['LICENSE'].decode())
