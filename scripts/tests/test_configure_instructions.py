#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 79945832-3359-4cdc-9a43-c84656c6c8cb
# Created: 2026

# COMPONENT: Profile selector integration tests
# PURPOSE: Verify preservation, selection, validation, and preview through the public shell entry point.
# RELATES: scripts/configure_instructions.py, instructions/REPO.md
# FLOW: Temporary repository -> CLI process -> file and diagnostic assertions.

import json
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "configure-instructions.sh"
PROFILE = "instructions/project/PROJECT_PROFILE.md"


class ConfigureInstructionsTests(unittest.TestCase):
    """Exercise the real CLI using isolated repositories and no network access."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name) / "repository"
        self.root.mkdir()
        (self.root / "src").mkdir()
        self.answers = Path(self.directory.name) / "answers.json"

    def run_cli(self, answers=None, *flags, input_text=None):
        """Return the CLI process result, optionally supplying a JSON update."""
        command = ["bash", str(SCRIPT), "--root", str(self.root), *flags]
        if answers is not None:
            self.answers.write_text(json.dumps(answers))
            command.extend(["--answers", str(self.answers)])
        return subprocess.run(command, input=input_text, text=True, capture_output=True, timeout=20)

    def native_answers(self):
        """Describe a standalone Swift component without inventing build commands."""
        return {"components": {"native-client": {
            "enabled": True,
            "source_paths": ["src"],
            "targets": ["apps"],
            "languages": ["Swift"],
            "platforms": ["iOS", "macOS"],
            "saas_client": False,
            "sdk_component": "none",
            "deployment": "native application",
        }}}

    def initialize(self):
        result = self.run_cli(self.native_answers(), "--apply")
        self.assertEqual(result.returncode, 0, result.stderr)

    def snapshot(self):
        """Capture file bytes so a read-only or rejected operation cannot hide writes."""
        return {str(p.relative_to(self.root)): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_initialize_installs_profile_and_required_guides(self):
        self.initialize()
        self.assertTrue(all((self.root / p).is_file() for p in [
            PROFILE, "AGENTS.md", "instructions/AGENTS.md", "instructions/SWIFT.md",
            "instructions/project/PROJECT.md", "instructions/project/ADDITIONAL.md",
            "CLAUDE.md", "CODEX.md", "GEMINI.md",
        ]))

    def test_dry_run_has_no_writes(self):
        before = self.snapshot()
        result = self.run_cli(self.native_answers(), "--dry-run")
        self.assertTrue(result.returncode == 0 and self.snapshot() == before)

    def test_preview_shows_profile_and_root_changes(self):
        result = self.run_cli(self.native_answers(), "--dry-run")
        self.assertTrue(PROFILE in result.stdout and "instructions:managed:start" in result.stdout)

    def test_check_accepts_initialized_profile(self):
        self.initialize()
        result = self.run_cli(None, "--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_check_does_not_modify_files(self):
        self.initialize()
        before = self.snapshot()
        self.run_cli(None, "--check")
        self.assertEqual(self.snapshot(), before)

    def test_repeated_answers_are_byte_identical(self):
        self.initialize()
        before = self.snapshot()
        self.run_cli(self.native_answers(), "--apply")
        self.assertEqual(self.snapshot(), before)

    def test_preserves_project_facts_refinements_and_existing_guides(self):
        self.initialize()
        paths = ["instructions/project/PROJECT.md", "instructions/project/ADDITIONAL.md",
                 "instructions/SWIFT.md"]
        for path in paths:
            with (self.root / path).open("a") as stream:
                stream.write("\nHandwritten content stays.\n")
        before = {path: (self.root / path).read_bytes() for path in paths}
        self.run_cli({"components": {"native-client": {"platforms": ["macOS"]}}}, "--apply")
        self.assertEqual({path: (self.root / path).read_bytes() for path in paths}, before)

    def test_preserves_root_instructions_outside_managed_block(self):
        (self.root / "AGENTS.md").write_text("# Local instructions\n\nPreserve this rule.\n")
        self.initialize()
        self.assertTrue((self.root / "AGENTS.md").read_text().startswith(
            "# Local instructions\n\nPreserve this rule.\n"))

    def test_preserves_custom_components_and_notes(self):
        self.initialize()
        with (self.root / PROFILE).open("a") as stream:
            stream.write("\n### custom-audit\n\n- [ ] Enabled\n- Local note: preserve exactly.\n")
        self.run_cli({"components": {"native-client": {"platforms": ["macOS"]}}}, "--apply")
        self.assertIn("### custom-audit\n\n- [ ] Enabled\n- Local note: preserve exactly.",
                      (self.root / PROFILE).read_text())

    def test_invalid_target_rejected_before_any_write(self):
        answers = self.native_answers()
        answers["components"]["native-client"]["targets"] = ["unknown-target"]
        result = self.run_cli(answers, "--apply")
        self.assertTrue(result.returncode == 2 and self.snapshot() == {})

    def test_missing_sdk_reference_is_rejected(self):
        answers = self.native_answers()
        answers["saas_product"] = True
        answers["components"]["native-client"].update(saas_client=True, sdk_component="missing-sdk")
        result = self.run_cli(answers, "--apply")
        self.assertTrue(result.returncode == 2 and "SDK" in result.stderr)

    def test_disabling_used_sdk_is_rejected_without_writes(self):
        answers = self.native_answers()
        answers["saas_product"] = True
        answers["components"]["native-client"].update(saas_client=True, sdk_component="sdk")
        answers["components"]["sdk"] = {
            "enabled": True, "source_paths": ["src"], "targets": ["sdks"], "languages": ["Swift"],
            "platforms": ["iOS"], "deployment": "generated library",
        }
        self.assertEqual(self.run_cli(answers, "--apply").returncode, 0)
        before = self.snapshot()
        result = self.run_cli({"components": {"sdk": {"enabled": False}}}, "--apply")
        self.assertTrue(result.returncode == 2 and self.snapshot() == before)

    def test_reports_missing_platform_guide_without_adding_swift(self):
        answers = self.native_answers()
        answers["components"]["native-client"].update(languages=["Kotlin"], platforms=["Android"])
        result = self.run_cli(answers, "--apply")
        self.assertTrue(result.returncode == 0 and "coverage gap" in result.stderr
                        and "Languages: Kotlin" in (self.root / PROFILE).read_text())

    def test_missing_source_path_is_rejected(self):
        answers = self.native_answers()
        answers["components"]["native-client"]["source_paths"] = ["missing-source"]
        result = self.run_cli(answers, "--apply")
        self.assertTrue(result.returncode == 2 and "source" in result.stderr.lower())

    def test_path_traversal_is_rejected(self):
        answers = self.native_answers()
        answers["components"]["native-client"]["source_paths"] = ["../outside"]
        result = self.run_cli(answers, "--apply")
        self.assertTrue(result.returncode == 2 and self.snapshot() == {})

    def test_symlink_destination_is_rejected(self):
        outside = Path(self.directory.name) / "outside"
        outside.mkdir()
        (self.root / "instructions").symlink_to(outside, target_is_directory=True)
        result = self.run_cli(self.native_answers(), "--apply")
        self.assertTrue(result.returncode == 2 and list(outside.iterdir()) == [])

    def test_unknown_answer_field_is_rejected(self):
        result = self.run_cli({"componnets": {}}, "--apply")
        self.assertTrue(result.returncode == 2 and "Unknown" in result.stderr)

    def test_malformed_managed_block_is_rejected(self):
        (self.root / "AGENTS.md").write_text("Local rule\n<!-- instructions:managed:start -->\n")
        before = self.snapshot()
        result = self.run_cli(self.native_answers(), "--apply")
        self.assertTrue(result.returncode == 2 and self.snapshot() == before)

    def test_duplicate_component_is_rejected(self):
        self.initialize()
        with (self.root / PROFILE).open("a") as stream:
            stream.write("\n### native-client\n\n- [ ] Enabled\n")
        result = self.run_cli(None, "--check")
        self.assertTrue(result.returncode == 2 and "Duplicate" in result.stderr)

    def test_check_missing_profile_does_not_initialize(self):
        result = self.run_cli(None, "--check")
        self.assertTrue(result.returncode == 2 and self.snapshot() == {})

    def test_cancel_after_interview_writes_nothing(self):
        result = self.run_cli(None, input_text="4\nsrc\nSwift\nmacOS\nnative application\nno\n")
        self.assertTrue(result.returncode == 0 and "cancel" in result.stdout.lower()
                        and self.snapshot() == {})

    def test_check_requires_root_routing(self):
        self.initialize()
        (self.root / "AGENTS.md").unlink()
        result = self.run_cli(None, "--check")
        self.assertTrue(result.returncode == 2 and "AGENTS.md" in result.stderr)

    def test_check_requires_nonempty_routing(self):
        self.initialize()
        (self.root / "AGENTS.md").write_text("Handwritten instructions without library routing.\n")
        result = self.run_cli(None, "--check")
        self.assertEqual(result.returncode, 2)

    def test_custom_project_paths_are_preserved(self):
        self.initialize()
        profile_path = self.root / PROFILE
        text = profile_path.read_text().replace("instructions/project/PROJECT.md", "local/facts.md")
        text = text.replace("instructions/project/ADDITIONAL.md", "local/refinements.md")
        profile_path.write_text(text)
        result = self.run_cli({}, "--apply")
        self.assertTrue(result.returncode == 0 and (self.root / "local/facts.md").is_file()
                        and (self.root / "local/refinements.md").is_file())

    def test_project_path_cannot_point_at_shared_guide(self):
        self.initialize()
        profile_path = self.root / PROFILE
        profile_path.write_text(profile_path.read_text().replace(
            "instructions/project/PROJECT.md", "instructions/SWIFT.md"))
        result = self.run_cli(None, "--check")
        self.assertEqual(result.returncode, 2)

    def test_enabling_component_via_interview(self):
        answers = ["4", "src", "Swift", "macOS", "native application", "yes"]
        result = self.run_cli(None, input_text="\n".join(answers) + "\n")
        self.assertTrue(result.returncode == 0 and "- Languages: Swift" in (self.root / PROFILE).read_text())

    def test_interview_explains_repository_specific_component_names(self):
        profile = self.root / PROFILE
        profile.parent.mkdir(parents=True)
        source = SCRIPT.parents[1] / PROFILE
        text = source.read_text().replace('`*.md`, `instructions/`, `.github/`, `agentknowledge/`', '`src`')
        text = text.replace('`scripts/`', '`src`')
        profile.write_text(text)
        result = self.run_cli(None, input_text="\n" * 7 + "no\n")
        expected = [str(self.root), "existing profile", "local names", "instruction-library",
                    "Documentation", "instruction files", "Covers:"]
        self.assertTrue(result.returncode == 0 and all(value in result.stdout for value in expected))

    def test_interview_explains_every_enabled_component_field(self):
        answers = ["4", "src", "Swift", "macOS", "native application", "no"]
        result = self.run_cli(None, input_text="\n".join(answers) + "\n")
        expected = ["relative to the selected repository", "selected automatically", "actual source languages",
                    "operating systems", "standalone", "packaged or delivered", "Press Enter to keep"]
        self.assertTrue(result.returncode == 0 and all(value in result.stdout for value in expected))

    def test_interview_accepts_numbered_native_app_choice(self):
        answers = ["4", "src", "Swift", "macOS", "native application", "yes"]
        result = self.run_cli(None, input_text="\n".join(answers) + "\n")
        self.assertTrue(result.returncode == 0 and "- Targets: apps" in (self.root / PROFILE).read_text())

    def test_product_menu_matches_six_requested_categories(self):
        answers = ["4", "src", "Swift", "macOS", "native application", "no"]
        result = self.run_cli(None, input_text="\n".join(answers) + "\n")
        expected = ["1. SaaS", "2. SaaS with Native Clients", "3. Microservice", "4. Native App",
                    "5. Static Website", "6. CLI tools", "SaaS describes the product"]
        self.assertTrue(result.returncode == 0 and all(value in result.stdout for value in expected))

    def test_accepting_defaults_retains_profile_bytes(self):
        self.initialize()
        path = self.root / PROFILE
        path.write_text(path.read_text().replace("- Source paths: src", "- Source paths: `src`"))
        before = self.snapshot()
        result = self.run_cli(None, input_text="\n" * 5)
        self.assertTrue(result.returncode == 0 and "No changes." in result.stdout and self.snapshot() == before)

    def test_product_categories_select_expected_parts_and_sdk_relationships(self):
        scenarios = [
            ("1", ["src", "Java", "container", "src", "TypeScript, HTML, SCSS", "same container"],
             {"backend", "frontend"}),
            ("2", ["src", "Java", "container", "src", "TypeScript, HTML", "same container",
                   "src", "Swift, TypeScript", "iOS, browser", "generated library",
                   "src", "Swift", "iOS, macOS", "native application"],
             {"backend", "frontend", "sdk", "native-client"}),
            ("3", ["src", "Java", "container"], {"backend"}),
            ("4", ["src", "Swift", "macOS", "native application"], {"native-client"}),
            ("5", ["src", "HTML, CSS", "static hosting"], {"website"}),
            ("6", ["src", "Go", "macOS, Linux", "CLI binary"], {"tool"}),
        ]
        for category, values, expected in scenarios:
            with self.subTest(category=category):
                result = self.run_cli(None, input_text="\n".join([category, *values, "no"]) + "\n")
                self.assertEqual(result.returncode, 0, result.stderr)
                headings = {line.split("Component: ")[1].split(" (", 1)[0]
                            for line in result.stdout.splitlines() if line.startswith("Component: ")}
                self.assertEqual(headings, expected)
                if category == "2":
                    self.assertIn("Uses generated SDK: sdk", result.stdout)

    def test_combines_saas_website_and_cli_without_extra_component_questions(self):
        answers = ["1, 5, 6", "src", "Java", "container", "src", "TypeScript, HTML", "same container",
                   "src", "HTML, CSS", "static hosting", "src", "Python", "macOS", "CLI package", "yes"]
        result = self.run_cli(None, input_text="\n".join(answers) + "\n")
        self.assertTrue(result.returncode == 0 and "Enable " not in result.stdout
                        and "Source paths:" in (self.root / PROFILE).read_text())

    def test_switching_native_saas_to_standalone_removes_sdk_relationship(self):
        answers = self.native_answers()
        answers["saas_product"] = True
        answers["components"]["native-client"].update(saas_client=True, sdk_component="sdk")
        answers["components"]["sdk"] = {
            "enabled": True, "source_paths": ["src"], "targets": ["sdks"], "languages": ["Swift"],
            "platforms": ["iOS"], "deployment": "generated library",
        }
        self.assertEqual(self.run_cli(answers, "--apply").returncode, 0)
        result = self.run_cli(None, input_text="4\n\n\n\n\nyes\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = (self.root / PROFILE).read_text()
        native = profile.split("### native-client", 1)[1].split("###", 1)[0]
        self.assertTrue("- SaaS client: no" in native and "- SDK component: none" in native)

    def test_overlapping_saas_choices_are_explained_before_reprompt(self):
        answers = ["1, 2", "4", "src", "Swift", "macOS", "native application", "no"]
        result = self.run_cli(None, input_text="\n".join(answers) + "\n")
        self.assertTrue(result.returncode == 0 and "categories overlap" in result.stdout
                        and self.snapshot() == {})

    def test_partial_update_preserves_crlf_and_component_notes(self):
        self.initialize()
        path = self.root / PROFILE
        text = path.read_text().replace("- Platforms: iOS, macOS", "- Platforms: iOS, macOS\n\nNative note.")
        path.write_bytes(text.replace("\n", "\r\n").encode())
        result = self.run_cli({"components": {"native-client": {"platforms": ["macOS"]}}}, "--apply")
        self.assertTrue(result.returncode == 0 and b"- Platforms: macOS\r\n\r\nNative note.\r\n" in path.read_bytes())

    def test_unsafe_project_path_rejected_without_writes(self):
        self.initialize()
        path = self.root / PROFILE
        path.write_text(path.read_text().replace("instructions/project/PROJECT.md", "../outside.md"))
        before = self.snapshot()
        result = self.run_cli({}, "--apply")
        self.assertTrue(result.returncode == 2 and self.snapshot() == before)

    def test_json_field_typo_is_not_silently_ignored(self):
        result = self.run_cli({"components": {"native-client": {"platfroms": ["macOS"]}}}, "--apply")
        self.assertTrue(result.returncode == 2 and self.snapshot() == {})

    def test_empty_manual_targets_are_rejected(self):
        self.initialize()
        path = self.root / PROFILE
        path.write_text(path.read_text().replace("- Targets: apps", "- Targets: ,,,"))
        self.assertEqual(self.run_cli(None, "--check").returncode, 2)

    def test_empty_manual_source_paths_are_rejected(self):
        self.initialize()
        path = self.root / PROFILE
        path.write_text(path.read_text().replace("- Source paths: src", "- Source paths: ,,,"))
        self.assertEqual(self.run_cli(None, "--check").returncode, 2)

    def test_check_requires_selected_language_guide(self):
        self.initialize()
        (self.root / "instructions/SWIFT.md").unlink()
        result = self.run_cli(None, "--check")
        self.assertTrue(result.returncode == 2 and "SWIFT.md" in result.stderr)

    def test_existing_project_file_encoding_is_preserved(self):
        self.initialize()
        facts = self.root / "instructions/project/PROJECT.md"
        facts.write_bytes(b"Project facts with legacy encoding: \x96 retain these bytes.\n")
        before = facts.read_bytes()
        result = self.run_cli({}, "--apply")
        self.assertTrue(result.returncode == 0 and facts.read_bytes() == before)

    def test_project_paths_cannot_alias_each_other_or_name_directories(self):
        self.initialize()
        path = self.root / PROFILE
        original = path.read_text()
        variants = [
            original.replace("instructions/project/ADDITIONAL.md", "instructions/project/./PROJECT.md"),
            original.replace("instructions/project/PROJECT.md", "src/context.md"),
        ]
        (self.root / "src/context.md").mkdir()
        for text in variants:
            with self.subTest(text=text):
                path.write_text(text)
                before = self.snapshot()
                result = self.run_cli({}, "--apply")
                self.assertTrue(result.returncode == 2 and self.snapshot() == before)

    def test_five_requested_scenarios_select_only_their_guides(self):
        cases = [
            ("standalone", False, {"native": (["apps"], ["Swift"])},
             {"APPS.md", "SWIFT.md"}),
            ("native-saas", True, {"native": (["apps"], ["Swift"]), "generated": (["sdks"], ["Swift"])},
             {"APPS.md", "SWIFT.md", "SAAS.md", "SDKs.md"}),
            ("saas-frontend", True, {"server": (["backend"], ["Java"]),
                                     "browser": (["frontend", "static-assets"], ["TypeScript", "HTML", "SCSS"])},
             {"SAAS.md", "BACKEND.md", "JAVA.md", "FRONTEND.md", "STATIC_ASSETS.md", "TYPESCRIPT.md",
              "JAVASCRIPT.md", "HTML.md", "SCSS.md", "CSS.md"}),
            ("website", False, {"site": (["websites", "static-assets"], ["JavaScript", "HTML", "CSS"])},
             {"WEBSITES.md", "STATIC_ASSETS.md", "JAVASCRIPT.md", "HTML.md", "CSS.md"}),
            ("cli", False, {"command": (["tools"], ["Rust"])}, {"TOOLS.md", "RUST.md"}),
        ]
        for name, saas, scopes, expected in cases:
            with self.subTest(name=name):
                components = {key: {
                    "enabled": True, "source_paths": ["src"], "targets": targets,
                    "languages": languages, "platforms": ["macOS"], "saas_client": name == "native-saas"
                    and key == "native", "sdk_component": "generated" if name == "native-saas"
                    and key == "native" else "none", "deployment": "configured",
                } for key, (targets, languages) in scopes.items()}
                result = self.run_cli({"saas_product": saas, "components": components}, "--dry-run")
                self.assertEqual(result.returncode, 0, result.stderr)
                selected = result.stdout.splitlines()[0].split(": ", 1)[1].split(", ")
                self.assertEqual(set(selected), expected)


if __name__ == "__main__":
    unittest.main()
