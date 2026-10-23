<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 2b0e3dc6-0e8f-41ed-9f98-710da2efb911
Created: 2026
-->

<!-- AGENT: Supported interview choices, design boundaries, and verification. -->

# Contextual profile choices

The owner requested relevant language and platform selections instead of comma-separated free-text names.
Apple native targets should offer Swift and relevant web source languages. CLI tools should offer Python, Go, and other supported choices.

## Design and implementation

No pattern required. Small catalog and selection functions fit the existing interview boundaries.
Keep component orchestration in profile_interview.py and terminal rendering in the existing curses interface.
Use the same numbered choices in plain mode. Preserve the existing Markdown and JSON answer contracts.

Collect native, CLI, and SDK platforms before their languages.
Use a shared guide map and contextual catalogs so every new language selection has instruction coverage.
Select browser and Workspace hosts through their existing specialized menus.
Select Apps Script source languages individually. Require executable JavaScript or TypeScript alongside optional markup and styles.
Use backend language choices for Workspace HTTP services.

Keep unlisted existing facts through an explicit, exclusive Keep existing selection option.
Require replacement selections to use listed values. Preserve the shared JSON parser's existing spelling behavior.
Keep source paths and packaging descriptions as editable project facts.
Changing platforms rebuilds the language menu through the existing UI history mechanism.
Existing coverage warnings remain applicable. Menu inclusion does not prove framework or generator compatibility.

The shared module exposes these functions:

- select_platforms(role, current) returns platform names from the selected menu or explicit prior facts.
- language_options(role, platforms) returns the supported language choices for the component.
- select_languages(role, platforms, current) returns selected language names.
- choose_many(label, options, defaults, multiple=True) validates numbered choices for both terminal modes.
- language_values(value) retains the established profile and JSON language parser.

Changed implementation files are scripts/profile_choices.py, scripts/profile_interview.py, scripts/workspace_profile.py,
scripts/browser_profile.py, and scripts/configure_instructions.py.
Tests cover the catalog, product composition, extension choices, UI navigation, local targets, initialization, roles, and terminal modes.
Documentation changes cover README.md, PROJECT.md, instructions/README.md, instructions/REPO.md, and this review.
Conversation, changelog, knowledge records, and inherited-template hashes record the change.

## Verification

The baseline contained 195 passing tests. New regressions first failed on missing choices and generic interview behavior.
Tests verify Apple and Android menus, CLI and SDK choices, invalid input, existing values, and platform changes through UI history.
The shared parser retains its existing JSON behavior. Local target installation includes the catalog module.

A real ncurses trial selected iOS, iPadOS, and macOS through arrow keys and Space.
The next checklist offered Swift, JavaScript, TypeScript, HTML, CSS, and SCSS.
The trial selected Swift, TypeScript, HTML, and SCSS and verified the generated profile and source folder.
The trial also verified backward navigation, rebuilt review, apply, locked results, and terminal restoration.
No target files existed before final approval.

The final regression suite contains 213 passing tests.
Profile validation, the unchanged-profile dry run, template baseline, source formatting, and whitespace checks pass.
