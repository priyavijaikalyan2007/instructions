<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 7d583940-7141-4392-a58a-71786da3f8e0
Created: 2026
-->

<!-- AGENT: Evidence and recommendations for the shared instruction repository. -->

# Instruction review

Review date: 14 October 2026. Status: proposal for owner review.

The repository needs a shared foundation plus guides selected by language, product, and task.
Its current entry point describes one enterprise SaaS application, so agents inherit assumptions that do not fit other projects.
The proposed structure preserves engineering discipline and adds explicit scope to each rule.

## Scope and evidence

This review compares this repository against the working copies of `knobby/apps`, `knobby/idp`, and `pvk2007/theme`.
The [source inventory](./instructions-source-inventory.md) records commit identifiers, content hashes, differences, and proposed destinations.
Every top-level Markdown file participates in the inventory.
The review examines the main routing documents, shared engineering guides, and significant additions in the working repositories.
It does not audit application code or verify the security of those applications.

The instruction repository was clean at the start, at commit `d4bf763`.
All three source repositories contain local changes.
The identity repository includes an uncommitted `LANGUAGE.md` change, which the inventory treats as working-copy evidence.
Source repositories remain read-only throughout this work.
Changes found there are candidates for adoption, not instructions that govern this repository.

No Swift, Go, or Rust application repository was supplied.
Their guides therefore need official documentation and later trials against real projects.
The identity repository supplies Java extension experience, which does not establish a standard architecture for all Java web applications.

## Findings

| Finding | Evidence | Proposed change |
| --- | --- | --- |
| The root describes a specific SaaS architecture. | `AGENTS.md`, Structure, Stack, Folder Structure, and Local Endpoints. | Move topology, database, hosting, directories, and commands into a project profile. |
| Some required inputs do not exist. | The three required knowledge YAML files, `GOF_REFACTOR.md`, and root lifecycle scripts are absent. | Distinguish required shipped guides, optional project records, and template placeholders. |
| Test requirements conflict. | `AGENTS.md` requires strict test-first work. `TESTING.md`, When TDD Is Not Feasible, permits implementation first. | Define one workflow and explicit rules for behavior changes, refactors, exploration, and documentation. |
| Style rules assume a small set of languages. | `CODING_STYLE.md` specifies four spaces, Allman braces, and one type per file. | Keep common readability rules and move formatting and naming into language guides. |
| Language coverage is uneven. | `TESTING.md` and `PERFORMANCE.md` focus on .NET, TypeScript, Python, and PostgreSQL. | Add Swift, Go, Rust, and Java guidance for construction, tests, security, and performance. |
| Browser policy leaks into unrelated work. | The root requires a particular remote component catalog before UI work. | Select a design system in the project profile and scope browser catalogs to their consumers. |
| Documentation assumes one delivery model. | `DOCUMENTATION.md` requires monolith packaging, Knobby branding, component demos, and media placeholders. | Separate shared writing rules from app, website, library, and operator documentation. |
| Agent roles contain project policy. | `CODEX.md` and `GEMINI.md` assign particular roles. The identity copy further restricts Codex to security reports. | Use thin agent entry files and choose review roles explicitly in the project profile. |
| Extra rules obscure their owners. | `ADDITIONAL_INSTRUCTIONS.md` repeats rules from testing, security, UI, migrations, and dependencies. | Move each rule to one authoritative guide and leave an index at the old path. |
| Source revisions conflict. | Apps says both push immediately and do not push yet. Migration sequence widths also differ across repositories. | Preserve local choices in profiles and flag unresolved policy choices. |
| Some text and links need repair. | Several root Markdown files fail strict UTF-8 decoding. `GOF_REFACTOR.md` is referenced but absent. | Validate encoding, links, section anchors, routing, and examples. |
| Reference catalogs can become stale. | This repository copies catalogs that the theme repository continues to change. | Link to a declared authoritative source and record verification dates where snapshots remain useful. |

`LANGUAGE.md` governs written communication.
Programming-language guides need a separate name and directory so agents cannot confuse these two purposes.
The root copy also includes recent writing changes, so replacing it with an older working-repository copy would lose guidance.

## Changes to fold into the shared guides

The following table identifies reusable lessons and the limits that should accompany them.
Source locations refer to headings in the working copies captured by the inventory.

| Source | Lesson to adopt | Destination and scope |
| --- | --- | --- |
| Apps `AGENTS.md`, Build Output Directories. Theme insights, Generated Files. | Edit source files and verify which paths the build generates. | Core workflow. Record actual source/output paths in each project. |
| Apps `AGENTS.md`, Work Tracking and Verify claims. | Keep one authoritative work record, explain accepted deviations, and measure numerical claims. | Core tracking. Configure the tracker instead of requiring a particular GitHub board. |
| Apps `PRAGMATIC_PROGRAMMER.md`, degraded behavior. | Distinguish empty data from failed reads. Failed loads must not authorize destructive saves or report success. | Core errors and UI changes. Preserve explicit, safe degraded modes without banning unrelated writes globally. |
| Apps `AGENTS.md`, tenant-owned reads and object authorization. | Check ownership as well as role. Test reads, writes, caches, and background paths across tenants. | Access-control task and service target. Use language-specific examples separately. |
| Apps `SECURITY_GUIDELINES.md`, fail-closed authorization. | Missing permission data denies access. The server remains the authority. | Core security and access control. |
| Apps `BACKEND.md`, Transactional Dual-Write and Consistency Approaches. | Commit related database writes atomically. Define recovery and delivery guarantees when writes span stores or services. | Services and data migrations. Choose transactions, outbox, or reconciliation from the required guarantee. |
| Apps `UI_UX_CONSISTENCY.md`, Auto-Save and Shell Coordination. | Await saves, handle failed saves, and preserve state across navigation and lifecycle changes. | UI changes and app targets. Adapt lifecycle events to each platform. |
| Apps `RESTABLE_RESOURCES.md`, Dual-Path Deep Linking. | Test fresh launches and navigation within a running app through the same resource-loading contract. | Web apps and Apple apps. Keep iframe message names and query shapes local. |
| Apps `DOCUMENTATION.md`, One fact, one home. | Cite one source for each claim. Separate user guidance, operator procedures, and control evidence. | Core documentation. |
| Apps `AGENTS.md`, Technical Debt Tracking. | Record a deviation, its reason, its owner, and a concrete resolution plan. | Core tracking and a debt template. |
| Identity `AGENT_INSIGHTS.md`, host runtime and provided-scope dependencies. | Confirm host APIs and dependency ownership against the runtime actually shipped. | Java guide and release operations. Keep Keycloak dependency details optional. |
| Identity insights, exact artifact and production entrypoint. | Reproduce failures using the exact artifact and launch path. Test environmental explanations against evidence. | Release operations and core testing. |
| Identity `SECURITY.md`. | Define security reporting scope and operational ownership. | Repository security policy and project template. Avoid promises of complete attack resistance. |
| Identity insights, design-system delivery mechanism. | Verify how a dependency is delivered before designing its integration. | Core dependencies and UI changes. |
| Theme `AGENTS.md`, No Fabricated Reads. | Failed components must refuse authoritative reads instead of returning plausible values that a caller could persist. | Core errors, UI libraries, and UI changes. |
| Theme `TESTING.md`, sections 2.5–2.9 and Fleet Conformance Gate. | Prove that tests reach their subject. Test the classifier behind counts and use browsers for layout and resource behavior. | Core testing, TypeScript, and UI libraries. |
| Theme `TESTING.md`, Confirm a Surprising Measurement. Apps `AGENTS.md`, Verify claims. | Distinguish measured results from estimates and unexecuted checks. Confirm unexpected measurements through an independent method. | Core workflow, testing, and documentation. |
| Theme `TESTING.md`, Test the artifact. | Verify published bundles and consumer-facing APIs, not only source modules. | UI libraries and release operations. |
| Theme `AGENTS.md`, JSON serializer rule. | Append JSON Lines through a serializer and validate every record. | Core knowledge. Preserve existing history. |
| Theme `AGENTS.md`, browser globals. | Declare public browser APIs and avoid assertions that bypass their types. | TypeScript guide. Keep a central declaration file a project choice. |
| Theme `FRONTEND_LOGGING.md`, Which document governs. | Declare the governing guide for each subsystem and let the host own its logging pipeline. | Core logging and UI libraries. Keep the actual logger mechanism local. |
| Theme `DOCUMENTATION.md`, Publishing a new document. | Check discovery, navigation, build inclusion, and publication paths. | Core documentation and release operations. |
| Theme `SECURITY_GUIDELINES.md`, scene documents. | Treat generated documents as untrusted input. Allowlist actions, validate before execution, and bound resource use. | AI features and UI changes. |
| Theme `PERFORMANCE.md`, Dynamic UI. | Budget resource use, release resources, and test capture/restore behavior. | UI libraries and app targets. Keep specific caps local. |
| Theme `CDN_CONTRACT.md` and insights, cross-repository contracts. | Define consumer contracts, change producer and consumer in order, and state update versus pinning tradeoffs. | Core dependencies, UI libraries, and release operations. |
| Theme insights, safe Git staging and evidence. | Stage only task files, retain failure evidence, and verify the actual remote branch after a requested push. | Core workflow. |
| Apps and theme insights, theme tokens. | Use shared tokens, pair foreground/background colors, and verify contrast in supported appearance modes. | Web markup and UI changes. Use native platform appearance APIs for Apple apps. |

## Rules to scope, resolve, or exclude

The newest copy should not win automatically.
Some additions encode a product decision, a local incident, or an unresolved contradiction.
The shared repository should preserve the lesson without imposing the original product's implementation.

| Candidate | Recommended treatment |
| --- | --- |
| Exact domains, realm names, environment names, role vocabulary, ports, credentials, and deployment topology. | Keep in project profiles. Shared rules require a documented naming grammar and boundary validation. |
| Immediate pushes, mandatory issue creation, and fixed agent roles. | Make project choices. The active user request controls external actions. |
| Automatic session cleaning. | Exclude as a universal requirement. Cleaning can remove evidence or disrupt other work. |
| SQL-only migrations and four-digit versus six-digit sequence numbers. | Require reproducible migrations. Keep the migration system and sequence convention local. |
| Customer-key audit policy and copied legal retention periods. | Retain key-lifecycle and evidence-integrity concerns. Require project-specific retention and key policy instead of copying legal conclusions. |
| Random gibberish comments in the apps copyright guide. | Exclude. Preserve SPDX headers and meaningful navigation markers. |
| Treating absent `LICENSE.md` as proof that code is proprietary. | Check `LICENSE`, `LICENSE.md`, and declared project policy. Do not infer licensing terms from one missing filename. |
| Blanket Allman formatting and class-oriented design patterns. | Scope formatting by language and project configuration. Use patterns when they reduce complexity. |
| A universal 90% coverage threshold and one assertion per test. | Propose project-set coverage thresholds and one behavior per test. Related assertions can verify that behavior together. |
| Requiring a failed test for every refactor or document edit. | Preserve passing behavior baselines for refactors. Use document checks for prose changes. |
| Banning every fallback or every write during any outage. | Protect affected state and declare degraded behavior. A safe logging fallback need not disable independent application writes. |
| One CDN, logger, form contract, canvas contract, or component count. | Keep library contracts in an optional integration guide. Promote only their reusable safety properties. |
| Static HTML websites forced into an API-backed application model. | Allow static delivery. Apply API rules when the website actually uses APIs. |
| Statements that agents cannot capture screenshots or generate media. | Base verification requirements on available tools and state any actual limitation. |
| Browser cross-origin claims in incident notes. | Verify platform behavior before promotion. Do not copy broad claims about `postMessage` from one integration incident. |
| Live advisory checks, patch status, runtime versions, and framework APIs. | Consult current primary sources during relevant work. Keep project toolchain pins authoritative. |
| Writing differences in apps and identity `LANGUAGE.md`. | Preserve the root's approved marker and callout sections pending review. Resolve narrower analogy wording and vocabulary guidance explicitly. |

These policy changes require owner review before implementation.
Existing strict rules remain unchanged in this planning branch.

## Language and product coverage

Each language guide should cover naming, formatting, API design, errors, concurrency, resource ownership, dependencies, tests, security, and performance.
Each product guide should add lifecycle, delivery, user experience, and integration checks.
Tool versions, supported operating systems, and framework choices belong in project configuration.

| Guide | Specific coverage to add |
| --- | --- |
| Swift | Value/reference semantics, optionals, protocols, structured concurrency, actor isolation, cancellation, resource ownership, package tests, and Apple test tools. |
| Go | `gofmt`, package boundaries, small consumer interfaces, explicit errors, contexts, goroutine lifetime, race tests, fuzzing, and vulnerability checks. |
| Rust | Cargo, `rustfmt`, Clippy, ownership, borrowing, `Result`/`Option`, panic boundaries, unsafe invariants, feature combinations, and async runtime choices. |
| Java | Project JDK/toolchain, Maven or Gradle wrapper, package design, null handling, resource cleanup, concurrency, serialization, and host/runtime compatibility. |
| C# and .NET | .NET 10.0+ scope, pinned SDK, nullable references, async cancellation, dependency scopes, API boundaries, persistence, and configured test platforms. |
| TypeScript | Strict checking, runtime validation, declared browser APIs, lifecycle cleanup, package/bundle contracts, and tests at browser boundaries. |
| JavaScript | Existing-project support, module and runtime compatibility, linting, checked JavaScript where useful, and explicit migration triggers. |
| HTML, CSS, and SCSS | Semantic markup, accessibility, progressive enhancement, theme tokens, responsive layout, browser security, and visual verification. |
| Python | Preserve existing script guidance. Do not remove supported repository tooling while adding the requested languages. |
| macOS and iOS apps | SwiftUI/AppKit/UIKit as appropriate, state, persistence, document safety, permissions, Keychain, accessibility, app lifecycle, and distribution. |
| Websites | Static and generated sites, navigation, content, forms, metadata, assets, accessibility, and delivery without an assumed backend. |
| Web applications | Browser/server boundaries, auth, state, saves, deep links, offline behavior where relevant, and integration tests. |
| Services and command-line tools | Configuration, cancellation, signals, stdout/stderr, exit status, bounded work, persistence, and release artifacts. |
| UI libraries | Public contracts, discovery, events, cleanup, appearance modes, consumer tests, bundles, and publication. |

## Primary references

These references establish starting points, not a claim that the future guides are complete.
Detailed framework instructions need verification during implementation.

- [Swift API design guidelines](https://www.swift.org/documentation/api-design-guidelines/) support language-specific API conventions.
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) identify the native platform guidance to consult.
- [Swift Testing](https://developer.apple.com/documentation/testing) identifies Apple's current testing documentation.
- [Effective Go](https://go.dev/doc/effective_go) documents Go conventions, including formatting and interfaces.
- [Go security](https://go.dev/doc/security/) documents the role of `govulncheck`.
- [Rust style guide](https://doc.rust-lang.org/style-guide/) and [Clippy usage](https://doc.rust-lang.org/clippy/usage.html) cover formatting and lint checks.
- [JDK 21 documentation](https://docs.oracle.com/en/java/javase/21/) matches the supplied identity project's declared JDK baseline.
- [.NET testing](https://learn.microsoft.com/en-us/dotnet/core/testing/) distinguishes test platforms from frameworks.
- [TypeScript strict mode](https://www.typescriptlang.org/tsconfig/strict.html) documents the strict-checking group and its upgrade implications.

Several Apple documentation pages require JavaScript and were not fully readable through the text browser.
Their detailed requirements remain to be checked during implementation through a supported documentation view.
