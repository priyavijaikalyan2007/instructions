<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 65a3fdcb-7dd5-4d30-b9e8-6930a0056650
Created: 2026
-->

<!-- AGENT: Shared role definitions. Project assignments belong in root PROJECT_PROFILE.md. -->

# Coding-tool roles

Read root AGENTS.md and PROJECT_PROFILE.md before work.
Use the profile row for your host tool, such as Codex or Roo Code.
A model provider does not identify the host tool.
One tool can have several roles. Different tools can share a role.
If no role is assigned, follow the user task and the shared workflow.
Explicit user requests can change the role needed for a task.

Role assignments describe expected work. They do not grant permissions or authorize delegation, publication, or destructive actions.
Apply the selected target, language, security, and completion rules in every role.
Keep project-specific duties and notes in the profile. Keep project facts in PROJECT.md and local refinements in ADDITIONAL.md.

## Role definitions

| Role | Expected work |
| --- | --- |
| general | Perform the roles needed for the user task. |
| implementation | Write and maintain code from agreed requirements and applicable instructions. |
| planning | Define the work, dependencies, acceptance checks, and sequence before implementation. |
| architecture | Design component boundaries, interfaces, data flows, and technical tradeoffs. |
| review | Assess correctness, maintainability, regressions, and adherence to applicable instructions. |
| testing | Design and run meaningful checks. Report failures and verification limits. |
| security | Assess trust boundaries, permissions, tenant isolation, and the sensitive-data lifecycle. |
| ux | Design and assess user interactions, accessibility, clarity, and recovery. |
| documentation | Write and maintain user, developer, and operational documentation. |
| operations | Maintain build, packaging, release, deployment, and operational workflows. |
| product | Define user needs, product behavior, scope, and acceptance criteria. |

Select roles by responsibility rather than by brand. A review assignment alone does not request implementation.
If assigned roles conflict with the task, follow the explicit request and state material limits.
Do not assume another tool completed its work. Verify the available evidence.

## Instruction entry points

AGENTS.md remains the shared entry point. Its managed block selects common and task-specific guides.
The interview records roles in PROJECT_PROFILE.md. Re-run setup with --configure-agents to edit those assignments.
An ordinary profile edit preserves existing assignments. JSON can replace them through the optional agent_roles object.
An empty agent_roles object clears tool-specific assignments.

[Codex reads AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
CODEX.md is a compatibility pointer and is not a default Codex instruction filename.
[Claude Code reads CLAUDE.md](https://code.claude.com/docs/en/memory).
The installed CLAUDE.md and GEMINI.md point to the shared entry point without assigning vendor-specific roles.

[Cline supports AGENTS.md](https://docs.cline.bot/customization/cline-rules).
[Antigravity supports workspace AGENTS.md and GEMINI.md](https://www.antigravity.google/docs/rules/).
For [Roo Code workspace rules](https://roocodeinc.github.io/Roo-Code/features/custom-instructions/), setup creates
.roo/rules/00-project-instructions.md when Roo is selected and that file is absent.
[Pi loads project context files from the working directory and its parents](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md#context-files).
Use its supported AGENTS.md entry. Setup does not create PI.md.
Custom tools need their documented entry mechanism. Setup does not invent tool-specific filenames.

Setup preserves customized entry files. It backs up recognized inherited entries before replacing them with neutral pointers.
Removing a role assignment does not delete a tool entry file. Installed pointers still lead to the current profile.
Setup does not install tools, change global settings, or configure credentials.
