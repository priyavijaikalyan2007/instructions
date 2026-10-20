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
| Source | instructions/, the four root agent entries, scripts/, .github/, and agentknowledge/ |
| Current review branch | docs/instructions-directory |
| Merged review | PR #1 and PR #2 in priyavijaikalyan2007/instructions |
| Application runtime | none |
| Generic build.sh or test.sh | absent |

## Source and configuration

| Subject | Fact |
| --- | --- |
| Generic entry point | AGENTS.md |
| Shared agent workflow | instructions/AGENTS.md |
| Agent entry files | CODEX.md, CLAUDE.md, GEMINI.md |
| Project selections | instructions/project/PROJECT_PROFILE.md |
| Local refinements | instructions/project/ADDITIONAL.md |
| Plan and status | instructions/maintenance/instructions-plan.md, instructions/maintenance/instructions.status.md |
| Repository-tool documentation | instructions/REPO_TOOLS_README.md |
| Knowledge records | agentknowledge/history.jsonl and agentknowledge/lcv_constraints.yaml |
| Source encoding | instructions/FRONTEND.md and instructions/DOCUMENTATION.md use CP1252. Most other guides use UTF-8. |

## Scope facts

The language snippets are examples for consuming projects. They are not a deployed application in this repository.
The current change has no Java server, browser application, generated SDK, or native application artifact to build.
The Java SaaS profile under instructions/maintenance/examples/ is a fictional instruction-routing fixture.
