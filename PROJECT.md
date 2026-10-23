<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 64e42bd9-c0cb-415b-a0d6-e7dfa6b6105d
Created: 2026
-->

<!-- AGENT: Project-specific facts about the instruction library. -->

# Instruction repository information

## Identity and purpose

| Fact | Value |
| --- | --- |
| Repository | instructions |
| Product | Generic coding-agent instructions and repository analysis tools |
| Source | instructions/, root agent entries and project files, scripts/, and agentknowledge/ |
| Review history | Git history and merged pull requests in priyavijaikalyan2007/instructions |
| Application runtime | none |
| Generic build.sh or test.sh | absent |

## Source and configuration

| Subject | Fact |
| --- | --- |
| Generic entry point | AGENTS.md |
| Shared agent workflow | instructions/WORKFLOW.md |
| Agent entry files | CODEX.md, CLAUDE.md, GEMINI.md |
| Project selections | PROJECT_PROFILE.md |
| Local refinements | ADDITIONAL.md |
| Plan and status | instructions/maintenance/instructions-plan.md, instructions/maintenance/instructions.status.md |
| Profile selector | configure.sh, Python 3.10+, Bash, Python standard library |
| Selector test command | python3 -m unittest discover -s scripts/tests -v |
| Selector read-only check | ./configure.sh --check |
| Repository-tool documentation | instructions/REPO_TOOLS_README.md |
| Knowledge records | agentknowledge/history.jsonl and agentknowledge/lcv_constraints.yaml |
| Source encoding | instructions/frontend/FRONTEND.md and instructions/DOCUMENTATION.md use CP1252. Most other guides use UTF-8. |

## Scope facts

The language snippets are examples for consuming projects. They are not a deployed application in this repository.
The current change has no Java server, browser application, generated SDK, or native application artifact to build.
The profile configurator is a local Python CLI with a Bash entry point and isolated filesystem integration tests.
The Java SaaS profile under instructions/maintenance/examples/ is a fictional instruction-routing fixture.

The interview supports eight product categories, including Google Workspace and browser extensions.
Microsoft Office extension profiles are deferred. No extension host application exists in this repository.

Project initialization: --initialize-project with optional --project-answers JSON.
License texts: pinned SPDX license-list-data v3.29.0, installed without runtime network access.
Source baseline check: python3 scripts/update_template_baseline.py.

Workspace setup collects structured hosts, model, runtime, account, and distribution choices.
Planned literal source paths are supported through an explicit source_state field.

New-component layout defaults are documented in REPO.md and each selected target guide.
The interview offers named source-path examples only when a concrete component path is absent.
This instruction repository retains its established scripts/ and scripts/tests/ paths.

Apps Script runtimes select a runtime-specific guide alongside shared JavaScript rules.
TypeScript source additionally selects TypeScript guidance. HTTP runtimes do not imply Apps Script.

Browser setup records supported browser/OS pairs and a typed distribution mode.
Language and platform menus use supported choices from scripts/profile_choices.py.
Native apps, tools, and generated SDKs select platforms before their contextual language lists.
Existing unlisted values receive an explicit Keep existing option. Manual and JSON coverage validation remains available.
First-time interactive setup records approved folder creation in optional source_folders metadata.
Extension defaults use src/extensions/googleworkspace/markdown and src/extensions/browser/markdown.
Those example names are replaceable. Existing configured paths retain their values.
Terminal output supports --color auto, always, and never without external dependencies.

Project-owned context files now reside at the repository root. Initialization metadata uses .instructions/.
The selector supports --target-folder for local tests without a Git repository or existing directory.
Tools can have multiple roles recorded in PROJECT_PROFILE.md. Shared definitions live in instructions/AGENT_ROLES.md.
Project initialization captures optional business facts and creates missing profile-specific operation placeholders and SETUP.md.
For new backend components, the environment model uses test locally, dev for staging, and prod for production.
Single-license output keeps full terms in root LICENSE when no companion or separate content terms are required.

Interactive terminal interviews use Python curses forms. Plain and forced-curses modes are explicit --ui choices.
PTY checks cover cursor editing, forward Delete, Backspace, choice selection, terminal resize, review, apply, and cancellation.
Curses remains optional. JSON and redirected invocations retain plain output.
