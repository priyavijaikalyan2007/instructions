<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 7ebb41e5-4828-41a3-9194-90cd4cb69e59
Created: 2026
-->

<!-- AGENT: Shared repository setup, commands, source verification, and session workflow. -->

# Repository work

Read this guide for repository setup, build/test/run commands, source verification, and session records.
Use [AGENTS.md](./AGENTS.md#select-target-guides) to select targets and languages for the changed work.
Backend containers, native signing, and static bundle delivery remain in their target guides.

## Build and release boundaries

A build or test command does not authorize deployment, signing-key export, app-store submission, or release.

## Build, test, and run

Use the following commands when the consuming repository provides these scripts.
Otherwise, use its documented build and test commands for the configured toolchain.

### Clean
```bash
./clean.sh
```

### Build
```bash
./build.sh
```

### Test
```bash
./test.sh
```

### Run
```bash
./run.sh
```

### Deploy
```bash
./redeploy.sh
```

## Local endpoints and dependencies

Read the consuming repository's README, launch configuration, and scripts for ports, health checks, and local dependencies.
The SaaS, identity service, component demo, and website may each use different endpoints.
Native apps and local tools need no listening port unless their design explicitly includes a service.
Use configured local credentials. Never copy example credentials into a deployed environment.

## Folder and file structure

Preserve the consuming repository's established layout. Use the selected target guide's examples when a new project needs a layout.
Keep specifications in `specs/`, operator guides in `playbooks/`, and user/integrator documentation in `docs/` where those conventions apply.
Keep one type per source file, including short structs. See `CODING_STYLE.md` for nested-type and extension exceptions.

## Context efficiency

- **"Read once, cite forever; research before you edit."**
- **Cite, don't re-read.** If you have already read a file in the current session, refer to it by `path:line` (e.g., `frontend/component-studio.html:142`) instead of re-reading it. Only re-`Read` when:
  1. The file has been edited since you last read it (by you or a hook), OR
  2. You need lines outside the range you previously read, OR
  3. Enough turns have passed that the content was likely compressed out of context.
  When you do re-read a partial range, use `offset` and `limit` — never re-read a whole file to grab one function.
- **Read tightly.** Prefer `Grep` with `-n` and small `-C` context (2–5 lines) over `Read` of an entire file. Reserve full `Read` for files under ~300 lines, or when you genuinely need the whole picture (e.g., understanding a class structure end-to-end).
- **Read before edit; research before modify.** Before `Edit`/`Write` on a file, you must have read it in this session. Before modifying a function's signature or behaviour, `Grep` for all callers (by symbol name) so you know the blast radius. Editing blind causes failed edits, rollbacks, and rework — all of which cost more tokens than the upfront read.
- **Target prompts to exact locations.** When delegating to subagents or describing work, name the file and line range (`In api/Services/AuthService.cs lines 80–140, the ValidateToken method...`). This prevents the subagent from re-discovering what you already know.
- **Trust prior context within a session.** Do not re-verify file contents you just edited — `Edit`/`Write` would have errored if it failed. The harness tracks file state for you.

## Source and contract verification

- Edit source files rather than generated or copied build output. Confirm the source/output mapping before changing an unfamiliar file.
- Verify dependency APIs against the version actually shipped. Check the host runtime before adding a replacement for an existing service.
- Stage only files that belong to the task. Preserve unrelated working-tree changes and useful failure evidence.
- Record accepted quality deviations with a reason, owner, resolution plan, and review trigger in the project's existing tracking record.
- Treat measured counts as dated evidence. Record the file set, counting rule, command, and known exclusions.

## Clarifying questions

When any aspect of a task is unclear or ambiguous, ask clarifying questions before proceeding. Present the various choices or interpretations you see. It is better to ask questions than to make potentially incorrect assumptions.

## User configuration

When the product already provides user-configurable settings (e.g., AI provider/model, API keys, tenant/workspace settings), **do not hardcode or assume defaults**. Always:
- Use the existing configuration surfaces and stored settings.
- If a required configuration is missing or ambiguous, **ask the user** rather than choosing a model/provider or behavior unilaterally.
- Document any fallback behavior explicitly and only after confirmation.

## Conversation records

You must always update `CONVERSATION.md` with a brief description of changes made after each set of changes. This file serves as organizational and agentic memory tracking the evolution of the product. Do not skip this step.

## Commit records

You must always commit all changes to `git` with a concise description of changes made after each set of changes. This ensures that work is not lost.
