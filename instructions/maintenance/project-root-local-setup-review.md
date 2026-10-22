<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 7bf66379-18a6-4079-8c23-c119c69fb112
Created: 2026
-->

<!-- AGENT: Plan and verification record for project-owned root files, selectable agent roles, and local setup. -->

# Project ownership and local setup

## Plan

Move PROJECT_PROFILE.md, PROJECT.md, ADDITIONAL.md, CONVERSATION.md, and CHANGELOG.md to the root.
Keep common guides and copyable templates in instructions/.
Move project initialization state and backups into .instructions/.
Preserve custom project-file locations. Migrate only recognized default locations.
Preview migration alongside configuration changes. Keep dry runs, cancellation, and validation failures read-only.
Preserve customized document bytes except applicable path/link updates. Stop on conflicting root and legacy documents.
Retain historical prose and record the migration instead of rewriting past decisions.

Select coding tools and optional multiple roles per tool in the root profile.
Keep generic role definitions in instructions/AGENT_ROLES.md.
Use host-tool identities rather than guessing from model vendors.
Replace the source library's fixed vendor-role assignments with neutral entry points.
Preserve customized downstream entry files and migrate known inherited entry files with backups.
Keep AGENTS.md authoritative. Create only necessary verified adapters, such as Roo workspace rules.
Do not create credentials, change tool permissions, install agents, or claim that role text enforces a sandbox.
Support Claude Code, Codex, Gemini CLI, Antigravity, Pi, Roo Code, Cline, and custom tool identifiers.
Offer --configure-agents for later role edits. Retain unspecified role sections on ordinary profile edits.

Add --target-folder PATH for a complete local setup without Git, GitHub, or a pre-existing folder.
Allow an explicit repository URL of none and retain TODOs where later project facts are unavailable.
Do not create the target until final approval. Never reset or delete existing application source.
Support interactive dry-run interviews and JSON answers for repeatable local tests.
Preserve --root compatibility for existing callers.

No pattern required - focused functions and data tables suffice.
Keep the CLI orchestration separate from layout migration, role parsing/rendering, and tool-entry generation.
Interfaces: layout_changes(root, check=False) -> dict, read_project_bytes(root, relative) -> bytes | None,
canonical_profile(text) -> str, interview_agent_roles(current) -> dict, apply_agent_roles(profile, assignments) -> str,
agent_entry_changes(root, profile) -> dict, and validated_root(path, allow_missing=False) -> Path.
Keep the existing component JSON schema. Add only optional agent_roles at the top level.

Files: scripts/project_layout.py, scripts/agent_roles.py, scripts/configure_instructions.py,
scripts/profile_interview.py, scripts/project_initialization.py, scripts/update_template_baseline.py,
scripts/tests/test_project_layout.py, scripts/tests/test_agent_roles.py, scripts/tests/test_target_folder.py,
all existing scripts/tests/test_*.py files with profile paths or interactive fixtures,
AGENTS.md, CLAUDE.md, CODEX.md, GEMINI.md, the five moved project documents,
instructions/AGENT_ROLES.md, instructions/WORKFLOW.md, instructions/REPO.md, instructions/README.md,
instructions/PROJECT_PROFILE_TEMPLATE.md, instructions/PROJECT_TEMPLATE.md,
instructions/templates/repository/TEMPLATES.md, instructions/templates/repository/README.md,
instructions/templates/repository/PROJECT.md, instructions/templates/repository/inherited-files.json,
.github/README.md, active shared-guide project-path references, agentknowledge/concepts.yaml,
agentknowledge/decisions.yaml, agentknowledge/history.jsonl, and this record.

## Verification plan

Establish the 127-test baseline. Write failing public-CLI tests before implementation.
Cover root generation, customized legacy migration, links, conflicts, state/backups, and repeat edits.
Cover role selection, multiple roles, custom notes, native adapters, and existing-entry preservation.
Cover absent/empty local targets, interactive and JSON initialization, no repository URL, dry runs, cancellation,
existing files, unsafe destinations, copied scripts, and repeatability without Git.
Retain all prior browser, Workspace, licensing, source-folder, and terminal tests.
Check current shared references, Markdown links, profile checks, source encoding, and inherited-file baselines.
Verify agent discovery against official tool documentation. Keep custom-tool auto-loading limits explicit.

## Added scope from the owner

Single-license output should keep complete terms in root LICENSE.
Retain LICENSES/ when several terms or companion texts are required. Preserve existing initialized legal files.

Scaffold profile-specific root operation scripts with logging, failure handling, usage, and implementation placeholders.
Use test for local work, dev for staging, and prod for production when a backend exists.
Do not copy private service identifiers, credentials, cloud choices, or application commands from learning repositories.
Preserve existing scripts. Unimplemented operations must return failure rather than suggest that a build or release passed.
Generate root SETUP.md and print file-specific completion steps after the preview and apply.
Collect optional users, problem, value, scope, success criteria, and constraints during identity setup.
Store answers as project facts. Leave unknown answers as explicit TODOs.

Additional files: scripts/project_scaffolding.py, scripts/project_context.py, scripts/tests/test_project_scaffolding.py,
instructions/PROJECT_SCAFFOLDING.md, instructions/templates/scripts/operation.sh.template,
scripts/license_selection.py, scripts/tests/test_license_selection.py, and the repository document templates.
Interfaces: scaffolding_changes(root, profile, context_paths) -> dict,
readiness_steps(context_paths, script_names) -> list, and validate_context(value) -> dict.
Tests precede these additions. Cover script failure status, help, environment names, private-data exclusion,
custom script preservation, contextual facts, and read-only previews.

Additional preservation checks cover private project-file permissions, angle and reference links,
reserved SETUP.md collisions, current guide reference substitutions, optional Git detection,
and license changes in repeated target-folder mode.
The Java routing fixture follows the new root layout. Its historical audit includes a dated location correction.

## Curses interview interface

The owner requested a full curses interface after terminal editing exposed control characters.
Use Python's optional standard curses module, backed by ncurses on the tested macOS environment.
Keep plain mode for automation, redirected input, unsupported terminals, and explicit --ui plain.
Use --ui auto by default and offer --ui curses to require a supported interactive terminal.
Keep the existing profile, initialization, validation, preview, and apply contracts.
Use editable text fields, keyboard-selectable menus, scrolling context, a full review view, and explicit cancellation.
Use curses.wrapper to restore terminal settings after success, cancellation, or exceptions.
Read a Unicode character or ncurses key event. Never place escape sequences or control characters in answers.
Keep credentials outside this interview. Support resizing and monochrome terminals.

Files: scripts/interview_widgets.py, scripts/curses_interview.py, scripts/interview_cancelled.py,
scripts/terminal_ui.py, scripts/configure_instructions.py, scripts/tests/test_interview_widgets.py,
scripts/tests/test_curses_interview.py, scripts/tests/test_terminal_ui.py, and current CLI documentation.
Interfaces: TextBuffer(value=''), TextBuffer.edit(key), menu_options(lines, prompt) -> list,
InterviewScreen.write(text), InterviewScreen.ask(prompt) -> str, InterviewScreen.finish(),
and run_interview_ui(callback, mode, interactive) -> int.
No pattern required - separate screen, widget, and orchestration functions suffice.
Add failing widget and public CLI tests first. Verify actual terminal keys, cancellation, restoration, and local setup through a PTY.

## Verification outcome

All 173 tests pass, including existing product, licensing, preservation, and terminal tests.
Real PTY setup verifies forward Delete, Backspace, cursor navigation, checkbox selection, resize, review, and apply.
A public CLI PTY test verifies explicit cancellation and restored functional terminal settings.
macOS PENDIN is excluded from exact flag comparison because the kernel sets this input-redraw bookkeeping flag on return.
Interactive fact correction preserves accepted answers. Plain mode and redirected automation remain covered.
The full Docs/browser trial validates generated files, copied tools, source folders, roles, business facts, and repeatability.
Active profile check, dry run, template baseline, Markdown links, and source-format checks pass.
Existing code examples remain unchanged except the updated root reading tree.
The CP1252 guides retain their encoding and differ only in default project-path tokens.
Historical record bytes precede the appended current outcome without rewriting past findings.
The owner authorized a commit, push, pull request, and merge. No remote permissions or tool credentials are changed.


## 22 October 2026: launcher and review refinement

Use root configure.sh for initialization and profile edits. Retain the previous launcher for compatibility.
Local setup installs both entries. Role questions repeat the purpose and controls for each selected tool.
Forms show a grouped change summary. F3 exposes complete file details and exact text changes.
Results show apply status and completion steps. Plain mode retains diffs.

Validation: 176 tests pass. A real ncurses trial verified two tool role screens, F3 inspection,
return to summary, explicit approval, readable results, cursor editing, resize, and terminal restoration.


## 22 October 2026: public documents at the root

Plan: Move README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, and SECURITY.md from .github/ to the root.
Update project_initialization.py, project_layout.py, project_scaffolding.py, configure_instructions.py,
update_template_baseline.py, their tests, active repository guides, document templates, and session records.
Keep workflow and issue configuration under .github/. Preserve existing policy text except local links.
Reuse layout_changes(root, check) and extend rebase_links(text, source_root) for known public-document moves.
Retain dry-run, cancellation, conflict, symlink, permission, and inherited-backup protections.
No pattern required. Existing functions cover this change. CLI orchestration remains separate from file planning.
Explain README as the public introduction, PROJECT as detailed facts, and PROJECT_PROFILE as scope configuration.
Verify fresh setup, copied templates, initialized legacy migration, links, preservation, and the full test suite.

Validation: All 183 tests pass. Active root and guide Markdown file links resolve.
Policy text remains unchanged except the moved contribution policy license link.
Fresh local setup and copied-template initialization produce root public documents.
Initialized legacy setups repair checklist and source-scope references without losing owner edits.
Dry runs, cancellation, conflicts, symlinks, inherited backups, and private file permissions are covered.
Source profile checks, read-only preview, and formatting checks pass.
