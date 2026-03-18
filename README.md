<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 9a3b3546-8a9c-4f10-93b2-9c472094bc04
Created: 2026
-->

<!-- AGENT: Readme file describing this repository. -->

**NOTE**: Replace this file with the README_TEMPLATE.md file for your project. This file can be safely removed since AGENTS.md already references the appropriate instruction files.

This repository contains instructions for coding agents, primarily Claude and Gemini. Each agent is asked to perform a different role.

The CLAUDE.md and GEMINI.md file reference AGENTS.md and then specify the role that the agent should play. AGENTS.md sets the main the context and the agent specific instructions set the roles.

Instead of using a monolithic, single instruction file, the AGENTS.md file references multiple individual files for specific instructions. It also tells the agent how to clean, build, test and run the code. 

The instructions in this repository assume a particular technology stack. You should make a copy of these instructions (or fork or consume as a git submodule) and modify them to match your setup. 

These instructrions are live. They are updated as and when new behaviors are encountered and need guidance. 

The instructions in this repository are *horizontal* in nature. That is, they are about how to write reasonably good code in a clean, structured manner. These instructions should be combined with other instructions for architecture, code structure, do's and don'ts to get output that works.

These instructions are battle tested in my private side projects. I have found that the coding agents that I use do produce reasonably clean, well structured code. However, as I continue to work with them, I continued to encounter odd choices that I keep adding. Such one-off fixes go into ADDITIONAL_INSTRUCTIONS.md.

## Agent Knowledge Base

The `agentknowledge/` directory contains a machine-readable knowledge graph that agents use to orient themselves. See [KNOWLEDGE_ARCHITECTURE.md](./KNOWLEDGE_ARCHITECTURE.md) for the full specification.

### Bootstrapping

On first use, the directory is empty (or contains only example files like `lcv_constraints.yaml`). Agents are expected to populate these files as they work:

| File | Purpose | Format |
|------|---------|--------|
| `concepts.yaml` | Maps business terms to anchor code locations | YAML list of `{name, definition, anchor_file, related}` |
| `entities.yaml` | Maps data models to code files and database tables | YAML list of `{name, table, file, description, related}` |
| `decisions.yaml` | Architectural Decision Records (ADRs) | YAML list of `{id, title, date, status, context, files}` |
| `history.jsonl` | Append-only log of agent tasks and changes | One JSON object per line: `{date, task, files, summary}` |
| `user_profile.yaml` | Per-user agent preferences (gitignored if personal) | YAML key-value pairs |

### Agent Workflow

1. **Session Start** — Read all files in `agentknowledge/` to orient. Use `concepts.yaml` to locate code instead of blind searching. Check `decisions.yaml` before proposing alternative approaches.
2. **During Work** — Consult the knowledge base before asking "Where is X?"
3. **Session End** — Update files if your work changed the codebase meaningfully:
   - Created a new service/controller/module → add to `concepts.yaml`
   - Created or modified a data model → add to `entities.yaml`
   - Made an architectural decision → add to `decisions.yaml`
   - Completed any significant task → append to `history.jsonl`

### Rules

- **Never delete** existing entries — only add or update.
- **Never rewrite** `history.jsonl` — it is append-only.
- Keep concept names in PascalCase and stable; other files may reference them.
- If a decision is superseded, set its `status` to `Superseded` and reference the replacement ADR id.

### Optional: Runtime SQLite

For complex queries (e.g., "Find all components related to Auth modified in the last week"), agents can load the YAML/JSONL files into an ephemeral in-memory SQLite database, query with SQL, and act on the results. This gives SQL power for analysis with Git-mergeable text for storage.

## Disclaimer

This project is a personal endeavor of the individual contributors and is provided on an "as-is" basis. It is not sponsored, authorized, endorsed, maintained, indemnified by, or in any way officially affiliated with any past, present, or future employer of the contributors — including but not limited to Google IT Services India Pvt Ltd, Alphabet Inc., Microsoft R&D India Ltd, and Microsoft Corporation, or any of their subsidiaries or affiliates. All trademarks and registered trademarks are the property of their respective owners. Use of employer names is solely for identification purposes and does not imply any association or endorsement.

