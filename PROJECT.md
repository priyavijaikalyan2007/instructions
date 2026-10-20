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
| Source | Root Markdown guides, scripts/, specs/, and agentknowledge/ |
| Current review branch | docs/target-guides |
| Review | PR #2 in priyavijaikalyan2007/instructions |
| Application runtime | none |
| Generic build.sh or test.sh | absent |

## Source and configuration

| Subject | Fact |
| --- | --- |
| Generic entry point | AGENTS.md |
| Agent entry files | CODEX.md, CLAUDE.md, GEMINI.md |
| Project selections | PROJECT_PROFILE.md |
| Local refinements | ADDITIONAL.md |
| Plan and status | specs/instructions-plan.md, specs/instructions.status.md |
| Repository-tool documentation | scripts/REPO_TOOLS_README.md |
| Knowledge records | agentknowledge/history.jsonl and agentknowledge/lcv_constraints.yaml |
| Source encoding | FRONTEND.md and DOCUMENTATION.md use CP1252. Most other guides use UTF-8. |

## Scope facts

The language snippets are examples for consuming projects. They are not a deployed application in this repository.
The current change has no Java server, browser application, generated SDK, or native application artifact to build.
The Java SaaS profile under specs/examples/ is a fictional instruction-routing fixture.
