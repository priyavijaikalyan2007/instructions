<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: afbe3719-d54c-4674-b5ab-eeaedf71b35e
Created: 2026
-->

<!-- AGENT: Repository landing page pointing to the shared instruction library. -->

# Coding-agent instructions

The [instruction library](instructions/README.md) contains shared engineering guides, language conventions, and project setup templates.
Start with [AGENTS.md](AGENTS.md). The other root agent entries are CLAUDE.md, GEMINI.md, and CODEX.md.
The [scenario reading trees](instructions/README.md#scenario-reading-trees) show the relevant files for native apps, SaaS clients, web SaaS, websites, and CLI tools.
[Project configuration](instructions/REPO.md#project-configuration) selects the guides needed for each task.
The [profile selector](instructions/REPO.md#profile-selector) initializes or modifies the same Markdown selections through an interview or JSON input.
Project-owned files, including PROJECT_PROFILE.md, PROJECT.md, and ADDITIONAL.md, live at the root.
Setup state and backups live under .instructions/. Instruction maintenance records live under instructions/maintenance/.
The specs/ directory is reserved for actual product and repository specifications.

Repository policies remain available through [contributing](CONTRIBUTING.md), [code of conduct](CODE_OF_CONDUCT.md), and [security](SECURITY.md).

The three project documents serve different purposes:

| File | Purpose |
| --- | --- |
| README.md | Public introduction, first use, support, and links to documentation. |
| [PROJECT.md](PROJECT.md) | Detailed business and technical facts, architecture, constraints, and verified commands. |
| [PROJECT_PROFILE.md](PROJECT_PROFILE.md) | Component scope, languages, paths, delivery choices, and agent roles that select instructions. |

Keep detailed facts in PROJECT.md and link to them from README.md.
Keep project-wide policies at the root. Reserve .github/ for GitHub configuration.

To test the interview locally without creating a GitHub repository:

```bash
./configure.sh --target-folder /tmp/instructions-trial --dry-run
```

Remove --dry-run to create the reviewed setup after confirmation.
The ncurses interview records business facts, component choices, and multiple roles per coding tool.
It supports editable fields, keyboard selection, scrolling help, and a review before approval.
Language and platform fields use selection lists that match each component and its platforms.
Use F5 Back and F6 Next to revisit UI questions. Draft answers remain available during the session.
Use --ui plain for the line-oriented interface. Automation and redirected input keep plain output.
[Project scaffolding](instructions/PROJECT_SCAFFOLDING.md) explains generated script placeholders and the completion checklist.
