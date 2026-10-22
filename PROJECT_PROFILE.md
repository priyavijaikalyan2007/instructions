<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: efb0aaaa-3be1-41ba-b486-70b9f2eb92e5
Created: 2026
-->

<!-- AGENT: Active component selections for this generic instruction repository. -->

# Instruction repository profile

## Project files

| Purpose | Path |
| --- | --- |
| Project facts | `PROJECT.md` |
| Additional instructions | `ADDITIONAL.md` |

## Project choices

- [ ] SaaS product
- [ ] Enterprise browser shell example from instructions/saas/SAAS.md
- [ ] Knobby authorization example from instructions/ACCESS_CONTROL.md
- [ ] Knobby deletion example from instructions/DELETION.md
- [ ] PostgreSQL/EF Core manual SQL example from instructions/PERSISTENCE.md
- [ ] Theme component-library example from instructions/static-assets/STATIC_ASSETS.md

## Components

### instruction-library

- [x] Enabled
- Source paths: `*.md`, `instructions/`, `agentknowledge/`
- Targets: documentation
- Languages: none
- Platforms: none
- SaaS client: no
- SDK component: none
- Deployment: none

### repository-tools

- [x] Enabled
- Source paths: `configure.sh`, `scripts/`
- Targets: tools
- Languages: Python, Shell
- Platforms: configured development environments
- SaaS client: no
- SDK component: none
- Deployment: local tooling

## Agent roles

No tool-specific roles are assigned. Follow the user task and shared workflow.
