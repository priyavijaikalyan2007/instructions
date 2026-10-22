<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 900dbe3a-84ae-4204-9eaa-b8b721ea6341
Created: 2026
-->

<!-- AGENT: Agent knowledge base architecture using YAML/JSONL with optional SQLite for complex queries. -->

# Agent Knowledge Base Architecture

To optimize agent performance, we utilize a **Structured Local Knowledge Base** rooted in the repository. 
This supplements `CONVERSATION.md` or `./specs/*.md` files which are the human readable versions with a
machine-readable, queryable structure that agents can ingest quickly at the start of each session.

---

## 1. The Challenge

- **Markdown files** are hard to query ("Find all bugs in module X").
- **SQLite binaries** cannot be checked into Git (merge conflicts).
- **Remote databases** add dependency and complexity.
- **Git log** is verbose and hard to parse for specific changes.
- Agents need fast orientation when starting a new session.

## 2. The Solution: "Git-Native" Knowledge Graph

We use **Structured Text (YAML/JSONL)** files that agents read directly. These are source-of-truth files that agents
can ingest into working memory for complex querying during their session.

### 2.1 Directory Structure

All knowledge artifacts reside in the folder `./agentknowledge/`:

```
./agentknowledge/
├── concepts.yaml       # Dictionary of domain terms and code locations
├── decisions.yaml      # Architectural Decision Records (ADRs) lightweight format
├── entities.yaml       # Map of Data Entities or Data Models to Code Files (if applicable)
└── history.jsonl       # Append-only log of tasks, changes, bugs and fixes.
└── user_profile.yaml   # Per-user preferences (Ignored by Git if personal)
```

### 2.2 File Formats

#### `concepts.yaml` (The Glossary)
Maps business terms to their "Anchor" locations (see `instructions/MARKERS.md`).
```yaml
- name: "TaxCalculation"
  definition: "Logic for computing VAT and Sales Tax."
  anchor_file: "src/Services/TaxService.cs"
  related: ["Invoice", "Currency"]
```

#### `decisions.yaml` (The "Why")

Tracks why design and architectural choices were made.

```yaml
- id: "ADR-001"
  title: "Use AES-256-GCM for Secrets"
  date: "2026-02-01"
  status: "Accepted"
  context: "Need strong encryption for API keys."
```

#### `history.jsonl` (The Memory)

An append-only log of what agents have done. One JSON object per line. Much easier to grep than git log.

```json
{"date": "2026-02-01", "task": "fix_login_bug", "files": ["Login.tsx"], "summary": "Fixed null check."}
{"date": "2026-02-02", "task": "add_secret_encryption", "files": ["SecretService.cs"], "summary": "Implemented AES-GCM."}
```

---

## 3. The "Runtime SQLite" Workflow

When an agent needs to perform complex analysis (e.g., "Find all components related to 'Auth' modified in the last week"), 
it should:

1.  **Read** the files in `./agentknowledge/`.
2.  **(Optional) Load** them into an ephemeral SQLite table structure in memory (or a temp file).
3.  **Query** the data using SQL.
4.  **Act** on the results.

This gives us the **power of SQL** for analysis with the **merge-ability of Text** for storage.

---

## 4. Instructions for Agents

### Session Start — Read

Read the knowledge files that exist. If this is a new repository, use the README and the schemas here to bootstrap only relevant records.
Do not invent application models or architectural decisions to fill an empty file.

At the beginning of every session, read these files to orient yourself:

1. `agentknowledge/concepts.yaml` — Locate code by concept name.
2. `agentknowledge/decisions.yaml` — Understand past architectural choices before proposing alternatives.
3. `agentknowledge/history.jsonl` — Understand recent changes.

### Session End — Update

Before your final commit, update these files if your work changed the codebase meaningfully:

| Trigger | Action |
|---------|--------|
| Created a new component | Add a concept entry to `concepts.yaml`. |
| Modified a data model or interface | Add or update an entry in `entities.yaml`. |
| Made a design or architectural decision | Add an ADR entry to `decisions.yaml`. |
| Completed any significant task | Append a JSON line to `history.jsonl`. |

### Rules

- **Consult First:** Before asking "Where is X?", grep `concepts.yaml`.
- **Never delete** existing entries — only add or update.
- **Never rewrite** `history.jsonl` — it is append-only.
- Append JSON Lines through a JSON serializer, with exactly one object and one terminating newline per record.
- Check the existing final newline before appending. Parse the resulting records to detect malformed JSON or merged lines.
- Validate modified YAML through a safe YAML parser when available. State explicitly when a format check did not run.
- Keep concept names in PascalCase and stable; other files may reference them.
- If a decision is superseded, set its `status` to `Superseded` and add the replacement ADR id.


