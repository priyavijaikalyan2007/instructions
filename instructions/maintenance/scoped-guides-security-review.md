<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 2a385089-bebb-46fb-9f60-ba72ef0d35fa
Created: 2026
-->

<!-- AGENT: Approved reorganization scope, preservation map, and validation record. -->

# Scoped guide reorganization and security review

## Plan and interfaces

Move target and language guides to their owning folders. Preserve common obligations and descriptive filenames.
Update all active links, scenario trees, profile maps, and installation behavior.
Generalize README_TEMPLATE.md while preserving its separate purpose from PROJECT.md and REPO.md.
Expand security by data lifecycle, language, runtime, tenant boundary, and AI feature.
Keep all historical records intact. Record policy corrections separately from relocation.

No pattern required - simple functions suffice.
The CLI flags and Markdown/JSON profile schemas remain unchanged.
`routing_block(guides)` derives root navigation. `missing_shared_guides(root)` plans safe recursive installation.
The CLI retains orchestration. Pure selection and routing helpers remain separate from filesystem writes.

Baseline: all 44 selector integration tests passed before edits.
Four new tests failed before implementation for nested copying, selected routing, stale routing, and retained inactive guides.
The existing shared-path collision test then exposed a recursive-layout gap. Extend reserved paths before accepting this migration.

## Moved files

| Previous path | Canonical path |
| --- | --- |
| `instructions/BACKEND.md` | `instructions/backend/BACKEND.md` |
| `instructions/API_GUIDELINES.md` | `instructions/backend/API_GUIDELINES.md` |
| `instructions/BACKEND_LIBRARY_SELECTION.md` | `instructions/backend/BACKEND_LIBRARY_SELECTION.md` |
| `instructions/DISTRIBUTED_SYSTEMS_COMPENDIUM.md` | `instructions/backend/DISTRIBUTED_SYSTEMS_COMPENDIUM.md` |
| `instructions/FRONTEND.md` | `instructions/frontend/FRONTEND.md` |
| `instructions/KEYBOARD.md` | `instructions/frontend/KEYBOARD.md` |
| `instructions/FRONTEND_LOGGING.md` | `instructions/frontend/FRONTEND_LOGGING.md` |
| `instructions/ERROR_DIALOG_COMPONENT.md` | `instructions/frontend/ERROR_DIALOG_COMPONENT.md` |
| `instructions/FRONTEND_LIBRARY_SELECTION.md` | `instructions/frontend/FRONTEND_LIBRARY_SELECTION.md` |
| `instructions/FRONTEND_SELECTION.md` | `instructions/frontend/FRONTEND_SELECTION.md` |
| `instructions/COMPONENTS.md` | `instructions/frontend/COMPONENTS.md` |
| `instructions/COMPONENT_INDEX.md` | `instructions/frontend/COMPONENT_INDEX.md` |
| `instructions/MASTER_COMPONENT_INDEX.md` | `instructions/frontend/MASTER_COMPONENT_INDEX.md` |
| `instructions/MASTER_COMPONENT_LIST.md` | `instructions/frontend/MASTER_COMPONENT_LIST.md` |
| `instructions/SAAS.md` | `instructions/saas/SAAS.md` |
| `instructions/APPS.md` | `instructions/apps/APPS.md` |
| `instructions/WEBSITES.md` | `instructions/website/WEBSITES.md` |
| `instructions/TOOLS.md` | `instructions/tools/TOOLS.md` |
| `instructions/SDKs.md` | `instructions/sdk/SDKs.md` |
| `instructions/STATIC_ASSETS.md` | `instructions/static-assets/STATIC_ASSETS.md` |
| `instructions/CSHARP.md` | `instructions/csharp/CSHARP.md` |
| `instructions/DOTNETFX_SELECTION.md` | `instructions/csharp/DOTNETFX_SELECTION.md` |
| `instructions/DOTNETFX.csv` | `instructions/csharp/DOTNETFX.csv` |
| `instructions/DOTNETCOREFRAMEWORKS.csv` | `instructions/csharp/DOTNETCOREFRAMEWORKS.csv` |
| `instructions/SWIFT.md` | `instructions/swift/SWIFT.md` |
| `instructions/GO.md` | `instructions/go/GO.md` |
| `instructions/RUST.md` | `instructions/rust/RUST.md` |
| `instructions/JAVA.md` | `instructions/java/JAVA.md` |
| `instructions/PYTHON.md` | `instructions/python/PYTHON.md` |
| `instructions/JAVASCRIPT.md` | `instructions/javascript/JAVASCRIPT.md` |
| `instructions/TYPESCRIPT.md` | `instructions/typescript/TYPESCRIPT.md` |
| `instructions/HTML.md` | `instructions/html/HTML.md` |
| `instructions/CSS.md` | `instructions/css/CSS.md` |
| `instructions/SCSS.md` | `instructions/scss/SCSS.md` |
| `instructions/SQL.md` | `instructions/sql/SQL.md` |
| `instructions/SHELL.md` | `instructions/shell/SHELL.md` |
| `instructions/AGENTS.md` | `instructions/WORKFLOW.md` |

## Other edited files

Active Markdown references in common guides, root AGENTS.md, project facts/profile, and Java SaaS fixtures follow the move map.
README.md contains updated scenario trees. REPO.md documents retention and regeneration.
README_TEMPLATE.md contains a generalized overview template.
Scripts changed: scripts/configure_instructions.py and scripts/tests/test_configure_instructions.py.
Security changes: SECURITY_GUIDELINES.md, AIML_SECURITY.md, SECRET_HANDLING.md, and selected language/target guides.
Session records: project/CONVERSATION.md, project/CHANGELOG.md, maintenance/instructions.status.md, and agentknowledge/history.jsonl.

## Development requirement preservation

Every previous Development bullet remains in WORKFLOW.md, grouped by applicability.
The configured additional-instructions file remains required before each task.

| Group | Retained requirements |
| --- | --- |
| Common | LANGUAGE, markers, knowledge records, style, logging, comments, pragmatic principles, construction, general security, testing, copyright, commits |
| Design and change | GoF patterns, project refactoring backlog, migration baseline, documentation, performance |
| Target | Backend, frontend, SDK, native platform permissions, library selection, browser reuse |
| Shared concern | Secrets, deletion, UI, APIs, deep links, literate errors, AI/ML approaches and security, authorization, persistence |

## Security policy changes

General and AI security remain separate common files. AI security is mandatory whenever AI behavior changes.
Language security belongs in the language guide. Shared data-lifecycle controls remain in SECURITY_GUIDELINES.md.
Replace product-specific AI findings with generic checks and scoped illustrative examples.
Correct claims that prompt prefixes enforce security, regex extraction validates JSON, or discarded strings erase memory.
Document SecureString limitations rather than requiring it for new .NET code.
Retain diagnostic correlation with approved pseudonymous identifiers and restricted logging.

## Validation

All 50 selector integration tests pass. The four behavior tests failed before implementation.
Two additional regression checks cover a nested destination symlink and the full Java SaaS/Apple fixture.
The current repository passes --check. Its --dry-run reports No changes.
Python 3.10 grammar, four-space source indentation, 120-character source lines, and 30-line function limits pass.
Bash syntax and Git whitespace checks pass.

All 37 source moves retain their original copyright headers and GUIDs. Both CSV files remain byte-identical.
All 31 previous Development bullets remain, with updated guide paths and applicability grouping.
Every original fenced example outside README.md and the two deliberately revised security guides remains present.
The README trees changed to reflect the new hierarchy. The security examples changed as documented below.
Markdown path and heading checks found zero new broken links against the baseline.
The checker reports 109 existing defects, primarily component reference links and one prior heading defect.
Historical conversation, changelog, and JSONL records retain their prior bytes as a prefix.

A temporary .NET 10 harness compiled and exercised the exact new JSON-validation fragment.
It accepted three valid responses and rejected 13 malformed or invalid cases, including duplicate properties and trailing content.
The same harness verified owned-buffer cleanup through CryptographicOperations.ZeroMemory.
Other language snippets received syntax/API review but were not all compiled or run on their target operating systems.
No native application, Java service, container, provider integration, or platform memory-protection behavior was executed.

## Security changes by previous section

| Previous guidance | Current treatment |
| --- | --- |
| General input validation, least privilege, authorization | Retained in common principles and tenant isolation |
| ASP.NET Identity, transport, DTOs, deserialization | Scoped to C# and configured backend identity |
| EF Core raw SQL and field projection | Retained with parameterized example in C# |
| React rendering, CSP, object merging, dependencies | JavaScript, HTML, frontend security, and common dependency requirements |
| Terraform secrets, private storage, SSRF | Common infrastructure controls, with stronger SSRF boundaries |
| Python, Java, Go, Swift, Rust pitfalls | Expanded in each language guide, with realistic memory limits |
| Fixed AI endpoint counts and vulnerability file/line claims | Removed from generic policy. Prior versions remain in Git history |
| Fixed AI character, token, graph, rate, and alert limits | Replaced with mandatory bounded controls and project-owned values |
| XML delimiters and non-overridable prompt prefixes | Replaced with structured segregation plus external enforcement and explicit limitations |
| Regex JSON extraction and silently repaired confidence | Replaced with strict complete-response parsing and rejection tests |
| English refusal prefixes and blanket email filtering | Replaced with provider status handling and authorized data policy |
| Raw exception logging and generic retry-only errors | Sanitized diagnostics plus useful controlled recovery messages |
| Named AI framework hooks and model self-review | Version-checked integration and supplemental evaluation, never authorization guarantees |
| Browser AI rendering | Plain text by default, reviewed rich-content sanitization and export checks |

Primary-source links appear beside the relevant security guidance.
Source review includes Microsoft, Apple, Android, PostgreSQL, Python, Go, Oracle, TypeScript, RustCrypto,
Linux documentation, libsodium, OWASP, and NIST.
Security policy expansion is intentional. It is not described as a content-only relocation.
