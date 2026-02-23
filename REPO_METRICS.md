<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 3c1f6c00-a906-4879-ae9f-facfd1efe022
Created: 2026
-->

# **Repository Metrics Analyzer — Technical Specification**

**Version:** 1.0  
 **Target Language:** Python 3.11+ (primary) or Go 1.22+ (alternative)  
 **Outputs:** HTML report, Markdown summary, JSON data file  
 **Integration:** Git post-commit hook

---

## **1\. Overview**

`repo-metrics` is a standalone CLI tool that scans a source code repository and emits structured metrics covering codebase size, composition, entity counts, API surface, database schema, test coverage shape, and software quality indicators. It runs on every commit via a Git hook and accumulates a time-series history so engineers can track growth and quality trends without relying on an external service.

### **Design Goals**

* **Zero external dependencies for collection.** All parsing uses the standard library plus a small, pinned set of widely available packages. No network calls at runtime.  
* **Fast enough for a post-commit hook.** A 500 KLOC repo should complete in under 10 seconds on a modern laptop.  
* **Language-aware but extensible.** First-class support for C\#, TypeScript/JavaScript, Python, HTML, CSS/SCSS, and SQL. Additional languages via plugin descriptors.  
* **Append-only history.** Every run appends a snapshot to a `metrics-history.json` file tracked alongside the repo (or written to a configurable output directory). The HTML report renders the full history as trend charts.  
* **Human and machine readable.** JSON for tooling, Markdown for PR comments and terminals, HTML for browsers and dashboards.

---

## **2\. Inputs and Configuration**

### **2.1 CLI Interface**

repo-metrics \[OPTIONS\] \[REPO\_PATH\]

Arguments:  
  REPO\_PATH         Root of the repository to analyze (default: current directory)

Options:  
  \--config FILE     Path to config file (default: .repo-metrics.yaml in REPO\_PATH)  
  \--out-dir DIR     Directory for output files (default: .metrics/ in REPO\_PATH)  
  \--commit SHA      Git commit SHA to label this snapshot (auto-detected if omitted)  
  \--branch NAME     Branch name (auto-detected if omitted)  
  \--format          Comma-separated list of output formats: html,md,json (default: all)  
  \--history FILE    Path to history JSON file (default: OUT\_DIR/metrics-history.json)  
  \--no-history      Do not read or write history; emit single-snapshot outputs only  
  \--include GLOB    Additional glob patterns to include  
  \--exclude GLOB    Additional glob patterns to exclude (can repeat)  
  \--depth INT       Max directory depth to traverse (default: unlimited)  
  \--verbose         Print progress to stderr  
  \--help

### **2.2 Configuration File (`.repo-metrics.yaml`)**

\# .repo-metrics.yaml

output\_dir: .metrics/  
history\_file: .metrics/metrics-history.json

\# Paths relative to repo root  
include:  
  \- "\*\*/\*"

exclude:  
  \- "\*\*/node\_modules/\*\*"  
  \- "\*\*/bin/\*\*"  
  \- "\*\*/obj/\*\*"  
  \- "\*\*/.git/\*\*"  
  \- "\*\*/dist/\*\*"  
  \- "\*\*/build/\*\*"  
  \- "\*\*/coverage/\*\*"  
  \- "\*\*/\*.min.js"  
  \- "\*\*/\*.min.css"

\# Language definitions (can extend or override built-ins)  
languages:  
  csharp:  
    extensions: \[".cs"\]  
    comment\_single: "//"  
    comment\_block\_open: "/\*"  
    comment\_block\_close: "\*/"  
  typescript:  
    extensions: \[".ts", ".tsx"\]  
    comment\_single: "//"  
    comment\_block\_open: "/\*"  
    comment\_block\_close: "\*/"  
  javascript:  
    extensions: \[".js", ".jsx", ".mjs", ".cjs"\]  
    comment\_single: "//"  
    comment\_block\_open: "/\*"  
    comment\_block\_close: "\*/"  
  python:  
    extensions: \[".py"\]  
    comment\_single: "\#"  
    comment\_block\_open: '"""'  
    comment\_block\_close: '"""'  
  html:  
    extensions: \[".html", ".htm", ".cshtml", ".razor"\]  
  css:  
    extensions: \[".css", ".scss", ".sass", ".less"\]  
  sql:  
    extensions: \[".sql"\]  
  yaml:  
    extensions: \[".yaml", ".yml"\]  
  json:  
    extensions: \[".json"\]  
  markdown:  
    extensions: \[".md", ".mdx"\]  
  go:  
    extensions: \[".go"\]  
    comment\_single: "//"  
    comment\_block\_open: "/\*"  
    comment\_block\_close: "\*/"

\# Cyclomatic complexity thresholds (for heat-map coloring)  
complexity\_thresholds:  
  low: 5  
  medium: 10  
  high: 20       \# anything above 20 is flagged as critical

\# Test file detection patterns (matched against relative path)  
test\_patterns:  
  \- "\*\*/\*.test.ts"  
  \- "\*\*/\*.test.js"  
  \- "\*\*/\*.spec.ts"  
  \- "\*\*/\*.spec.js"  
  \- "\*\*/\*Tests.cs"  
  \- "\*\*/\*Test.cs"  
  \- "\*\*/test\_\*.py"  
  \- "\*\*/\*\_test.py"  
  \- "\*\*/tests/\*\*"

\# API endpoint detection (regex patterns applied to file content)  
api\_endpoint\_patterns:  
  csharp:  
    \- '\\\[HttpGet'  
    \- '\\\[HttpPost'  
    \- '\\\[HttpPut'  
    \- '\\\[HttpDelete'  
    \- '\\\[HttpPatch'  
    \- '\\\[Route\\('  
  typescript:  
    \- "router\\.(get|post|put|delete|patch)\\s\*\\("  
    \- "app\\.(get|post|put|delete|patch)\\s\*\\("  
    \- "@(Get|Post|Put|Delete|Patch)\\("  
  python:  
    \- "@app\\.(get|post|put|delete|patch)"  
    \- "@router\\.(get|post|put|delete|patch)"

---

## **3\. Metrics Collected**

### **3.1 Repository-Level Metrics**

| Metric | Description |
| ----- | ----- |
| `snapshot_at` | ISO 8601 timestamp of the run |
| `commit_sha` | Current HEAD SHA (first 12 chars) |
| `commit_message` | First line of HEAD commit message |
| `branch` | Current branch name |
| `total_files` | Total files after include/exclude filters |
| `total_lines` | Total lines across all files |
| `total_loc` | Lines of code (non-blank, non-comment) |
| `total_blank` | Blank lines |
| `total_comment` | Comment lines |
| `comment_ratio` | `total_comment / total_loc` |
| `total_size_bytes` | Sum of file sizes in bytes |

### **3.2 Per-Language Breakdown**

For each detected language, report:

* `file_count` — number of files  
* `line_count` — total lines  
* `loc` — lines of code  
* `blank_lines` — blank lines  
* `comment_lines` — comment lines  
* `size_bytes` — total bytes  
* `pct_of_total_loc` — percentage of total codebase LOC

### **3.3 Entity Counts (Code Intelligence)**

These are collected via lightweight regex-based parsing (not full AST). Where an AST parser is available for the language (see Section 5), richer data is extracted.

#### **C\# (`.cs`)**

* `namespaces` — unique namespace declarations  
* `classes` — class, abstract class, sealed class  
* `interfaces` — interface declarations  
* `structs` — struct declarations  
* `records` — record declarations  
* `enums` — enum declarations  
* `methods` — method declarations (public / internal / private / protected breakdown)  
* `properties` — property declarations  
* `constructors` — constructor declarations  
* `delegates` — delegate declarations  
* `events` — event declarations  
* `attributes_defined` — custom `[Attribute]` class definitions  
* `using_directives` — unique top-level `using` namespaces

#### **TypeScript / JavaScript (`.ts`, `.tsx`, `.js`, `.jsx`)**

* `classes` — class declarations and expressions  
* `interfaces` — TypeScript interface declarations  
* `types` — TypeScript type alias declarations  
* `enums` — TypeScript enum declarations  
* `functions` — function declarations and arrow functions assigned to const  
* `react_components` — functions/classes that return JSX (heuristic: contain JSX return or extend React.Component)  
* `hooks` — functions matching `use[A-Z]` prefix pattern  
* `exports_named` — named exports  
* `exports_default` — default exports  
* `imports` — unique import source paths

#### **Python (`.py`)**

* `classes` — class definitions  
* `functions` — top-level `def` statements  
* `methods` — `def` inside class bodies  
* `decorators` — unique decorator names used  
* `imports` — unique `import` / `from ... import` module names  
* `dataclasses` — classes decorated with `@dataclass`

#### **SQL (`.sql`)**

* `tables_created` — `CREATE TABLE` statements  
* `views_created` — `CREATE VIEW` statements  
* `procedures` — `CREATE PROCEDURE` / `CREATE FUNCTION` statements  
* `indexes` — `CREATE INDEX` statements  
* `migrations` — files whose name matches a migration pattern (e.g., `V\d+__`)

#### **CSS / SCSS (`.css`, `.scss`, `.sass`, `.less`)**

* `rule_sets` — total selector rule sets  
* `selectors_unique` — unique selector strings  
* `variables` — CSS custom properties (`--foo`) and SCSS variables (`$foo`)  
* `media_queries` — `@media` blocks  
* `keyframes` — `@keyframes` blocks  
* `imports` — `@import` directives

#### **HTML / Razor / CSHTML**

* `templates` — total HTML/Razor files  
* `component_references` — unique custom element / component tag references (non-standard HTML tags)  
* `script_tags` — `<script>` tags  
* `style_tags` — `<style>` tags  
* `form_elements` — `<form>` tags

### **3.4 API Surface**

Detected via the patterns defined in `api_endpoint_patterns` config key.

| Metric | Description |
| ----- | ----- |
| `total_endpoints` | Sum of all detected route handlers |
| `by_method` | Breakdown: GET, POST, PUT, DELETE, PATCH, OTHER |
| `by_file` | Top 20 files with the most endpoints |
| `controllers` | C\# controller classes (files ending in `Controller.cs`) |

### **3.5 Database / Schema Metrics**

| Metric | Description |
| ----- | ----- |
| `tables` | List of table names from `CREATE TABLE` in `.sql` files |
| `table_count` | Total count |
| `migration_files` | Files identified as migration scripts |
| `migration_count` | Total migration file count |
| `views` | View names |
| `stored_procedures` | Procedure/function names |
| `ef_dbsets` | C\# `DbSet<T>` property declarations (Entity Framework entities) |
| `ef_entities` | Generic type arguments from `DbSet<T>` — represents mapped entity types |

### **3.6 Test Metrics**

| Metric | Description |
| ----- | ----- |
| `test_file_count` | Files matching test patterns |
| `test_loc` | LOC in test files |
| `test_to_source_ratio` | `test_loc / (total_loc - test_loc)` |
| `unit_test_count` | Methods/functions decorated with `[Fact]`, `[Test]`, `[TestMethod]`, `it(`, `test(`, `def test_` |
| `xunit_facts` | `[Fact]` annotations (C\# xUnit) |
| `xunit_theories` | `[Theory]` annotations (C\# xUnit) |
| `nunit_tests` | `[Test]` annotations |
| `mstest_tests` | `[TestMethod]` annotations |
| `jest_tests` | `it(` / `test(` calls in JS/TS |
| `pytest_tests` | `def test_` functions in Python |
| `integration_tests` | Heuristic: test files under `Integration/` or `IntegrationTests/` folder |
| `e2e_tests` | Heuristic: files matching `*.e2e.ts`, Playwright/Cypress files |
| `snapshot_tests` | `toMatchSnapshot()` / `toMatchInlineSnapshot()` calls |

### **3.7 Code Quality Metrics**

#### **Cyclomatic Complexity (per function/method)**

Computed using the standard decision-point counting algorithm: start at 1, add 1 for each `if`, `else if`, `elif`, `for`, `while`, `case`, `catch`, `&&`, `||`, `?` (ternary), `??`.

Report:

* `avg_complexity` — mean cyclomatic complexity across all functions/methods  
* `median_complexity` — median  
* `p95_complexity` — 95th percentile  
* `max_complexity` — highest single value (with file \+ function name)  
* `high_complexity_count` — functions above the `high` threshold  
* `critical_complexity_count` — functions above `high * 2`  
* `complexity_distribution` — histogram: `[1-5, 6-10, 11-20, 21-50, 51+]` counts

#### **Duplication (optional, flag `--duplication`)**

Uses a rolling hash (Rabin–Karp) over normalized token streams with a configurable block size (default: 6 lines). Reports:

* `duplicate_block_count` — number of detected duplicate blocks  
* `duplicate_loc` — estimated lines involved in duplication  
* `duplication_pct` — `duplicate_loc / total_loc * 100`

Note: duplication analysis is expensive. Disabled by default; enable with `--duplication` flag or `enable_duplication: true` in config.

#### **File-Level Metrics**

For each file, compute and persist:

* `loc` — lines of code  
* `complexity_avg` — average method complexity  
* `complexity_max` — max method complexity  
* `method_count` — number of methods/functions  
* `long_method_count` — methods exceeding 50 LOC

Top 20 largest files and top 20 highest-complexity files are included in the report.

#### **Additional Quality Signals**

| Metric | Description |
| ----- | ----- |
| `todo_count` | `TODO:` comments across codebase |
| `fixme_count` | `FIXME:` comments |
| `hack_count` | `HACK:` comments |
| `long_files` | Files \> 500 LOC |
| `long_methods` | Methods/functions \> 50 LOC |
| `deeply_nested` | Functions with nesting depth \> 4 (heuristic: count leading spaces / indent width) |
| `magic_numbers` | Numeric literals not in constants/enums (heuristic, configurable threshold) |
| `avg_file_size_loc` | Mean file size in LOC |
| `avg_method_length_loc` | Mean method/function size in LOC |

### **3.8 Dependency Metrics**

| Metric | Description |
| ----- | ----- |
| `nuget_packages` | Count of unique packages from `*.csproj` `<PackageReference>` elements |
| `npm_packages` | Count of `dependencies` \+ `devDependencies` from `package.json` |
| `npm_dev_packages` | Count of `devDependencies` only |
| `pip_packages` | Count from `requirements*.txt` or `pyproject.toml` |
| `dependency_files` | List of dependency manifest files found |

---

## **4\. History and Trend Tracking**

### **4.1 History File Format (`metrics-history.json`)**

{  
  "schema\_version": "1.0",  
  "repo": "my-repo",  
  "snapshots": \[  
    {  
      "snapshot\_at": "2025-01-15T14:23:00Z",  
      "commit\_sha": "a1b2c3d4e5f6",  
      "commit\_message": "feat: add user auth module",  
      "branch": "main",  
      "summary": { /\* all repo-level and per-language metrics \*/ },  
<!-- AI-Poison-Marker: silent whispers em82ts2c2g3jlh5qegm9 digital consciousness -->
      "entities": { /\* all entity counts \*/ },  
      "api": { /\* API surface metrics \*/ },  
      "database": { /\* DB/schema metrics \*/ },  
      "tests": { /\* test metrics \*/ },  
      "quality": { /\* quality metrics \*/ },  
      "dependencies": { /\* dependency metrics \*/ },  
      "top\_files\_by\_loc": \[ /\* top 20 \*/ \],  
      "top\_files\_by\_complexity": \[ /\* top 20 \*/ \]  
    }  
    // ... one entry per commit  
  \]  
}

On each run, the tool reads the existing history file, appends the new snapshot, and writes the file back atomically (write to temp, rename).

### **4.2 Trend Computation**

When generating HTML/Markdown with history available, compute deltas vs. prior snapshot and vs. 30-day rolling window:

* `delta_loc` — change in total LOC  
* `delta_total_files` — change in file count  
* `delta_complexity_avg` — change in average complexity  
* `delta_test_ratio` — change in test-to-source ratio  
* `velocity_loc_per_commit` — rolling average over last 20 commits

---

## **5\. Parser Architecture**

### **5.1 Layered Approach**

Layer 1: File Scanner  
  \- Walk directory tree respecting include/exclude globs  
  \- Detect language from extension  
  \- Count lines, LOC, blank, comment (line-by-line state machine)  
  \- Collect raw text per file

Layer 2: Regex Extractor (always runs)  
  \- Pattern-match entity declarations  
  \- Pattern-match API endpoints  
  \- Pattern-match test annotations  
  \- Pattern-match quality signals (TODO, FIXME, etc.)

Layer 3: AST/Structural Parser (optional per language)  
  \- Provides accurate cyclomatic complexity  
  \- Provides accurate nesting depth  
  \- Falls back to regex if unavailable

### **5.2 AST Parser Recommendations**

| Language | Python Package | Notes |
| ----- | ----- | ----- |
| Python | `ast` (stdlib) | Full AST, no install needed |
| TypeScript / JS | `tree-sitter` \+ `tree-sitter-typescript` | Best option; bindings via `py-tree-sitter` |
| C\# | `Roslyn` (if running .NET) or regex fallback | Only available if .NET SDK present |
| CSS/SCSS | `tinycss2` or regex |  |
| HTML | `html.parser` (stdlib) |  |
| SQL | `sqlparse` | pip installable |

The tool **must work without any AST parsers** — regex extraction is always the baseline. AST parsers are opportunistically used when available and improve accuracy of complexity metrics.

### **5.3 Cyclomatic Complexity via Regex (Baseline)**

For each function/method body (delimited by brace matching or indentation):

complexity \= 1  
  \+ count(r'\\bif\\b')  
  \+ count(r'\\belse\\s+if\\b|\\belif\\b')  
  \+ count(r'\\bfor\\b')  
  \+ count(r'\\bforeach\\b')  
  \+ count(r'\\bwhile\\b')  
  \+ count(r'\\bcase\\b')  \# switch cases  
  \+ count(r'\\bcatch\\b')  
  \+ count(r'&&|\\band\\b')  
  \+ count(r'\\|\\||\\bor\\b')  
  \+ count(r'\\?(?\!\\?)')   \# ternary (not null-coalescing)  
  \+ count(r'\\?\\?')       \# null-coalescing (count as 0 in strict mode, 1 in permissive)

---

## **6\. Output Formats**

### **6.1 JSON (`metrics-snapshot.json`)**

Full structured dump of the current snapshot. Same shape as a single entry in `metrics-history.json`. Machine-readable for CI pipelines, dashboards, and further processing.

### **6.2 Markdown (`metrics-report.md`)**

A concise summary suitable for pasting into a PR comment or reading in a terminal. Structure:

\# Repository Metrics — \<commit\_sha\> (\<branch\>) — \<date\>

\#\# Summary  
| Metric | Value | Δ vs prev | Δ vs 30d |  
...

\#\# Language Breakdown  
| Language | Files | LOC | % |  
...

\#\# Code Quality  
...

\#\# API Surface  
...

\#\# Tests  
...

\#\# Database / Schema  
...

\#\# Top Files by Complexity  
...

### **6.3 HTML (`metrics-report.html`)**

A self-contained single-file HTML report (all CSS and JS inlined, no CDN dependencies). Sections:

1. **Header** — repo name, commit, branch, timestamp, overall health score badge  
2. **Executive Summary** — KPI cards for LOC, files, test ratio, avg complexity, API endpoints  
3. **Trend Charts** — line charts (via embedded Chart.js or plain SVG) for:  
   * Total LOC over time by language (stacked area)  
   * File count over time  
   * Average cyclomatic complexity over time  
   * Test-to-source ratio over time  
   * API endpoint count over time  
   * TODO/FIXME count over time  
4. **Language Breakdown** — donut chart \+ table  
5. **Entity Catalog** — tables for each language's entity counts  
6. **API Surface** — endpoint breakdown table  
7. **Database / Schema** — table list, migration count, EF entities  
8. **Test Profile** — test type breakdown, ratio gauge  
9. **Code Quality** — complexity distribution histogram, top-20 hotspot table  
10. **Dependency Summary** — package counts  
11. **Snapshot History Table** — paginated table of all historical snapshots

The HTML report renders from the full `metrics-history.json` file embedded as an inline `<script>` block, so it is fully self-contained and requires no server.

#### **Overall Health Score**

A single 0–100 score computed from a weighted formula:

score \= 100  
  \- clamp(avg\_complexity \- 5, 0, 20\) \* 1.5       \# complexity penalty  
  \- clamp((1 \- test\_ratio) \* 30, 0, 30\)           \# test coverage shape penalty  
  \- clamp(todo\_count / 10, 0, 10\)                 \# tech debt signals  
  \- clamp(duplication\_pct, 0, 20\)                 \# duplication (if enabled)  
  \- clamp(long\_methods / total\_methods \* 20, 0, 10\)

Grade: A (90–100), B (75–89), C (60–74), D (40–59), F (\<40).

---

## **7\. Git Hook Integration**

### **7.1 `post-commit` Hook Script**

Create `.git/hooks/post-commit`:

\#\!/bin/bash  
\# repo-metrics post-commit hook  
set \-euo pipefail

REPO\_ROOT=$(git rev-parse \--show-toplevel)  
METRICS\_CMD="${REPO\_ROOT}/.metrics/repo-metrics"  \# or wherever installed

\# Fall back to PATH if not local  
if \[ \! \-x "$METRICS\_CMD" \]; then  
  METRICS\_CMD="repo-metrics"  
fi

if command \-v "$METRICS\_CMD" &\>/dev/null; then  
  "$METRICS\_CMD" \\  
    \--out-dir "${REPO\_ROOT}/.metrics" \\  
    \--format html,json \\  
    "${REPO\_ROOT}" \\  
    2\>/dev/null &   \# run in background to not block git  
fi

The `&` ensures the hook does not block the `git commit` command. The metrics run asynchronously. Remove `&` if you need synchronous behavior (e.g., to fail commits above a complexity threshold).

### **7.2 Hook Installer**

The tool should include a subcommand:

repo-metrics install-hook \[--mode async|sync\] \[REPO\_PATH\]

That writes the hook file and sets the executable bit.

### **7.3 Gate Mode (Optional)**

With `--gate` flags, the hook can fail the commit if thresholds are exceeded:

repo-metrics \--gate max\_complexity=25 \--gate test\_ratio=0.1

Exit code 1 with a message if any gate is violated. Useful in pre-commit hooks rather than post-commit.

---

## **8\. Implementation Notes**

### **8.1 Recommended Python Dependencies**

| Package | Purpose | Install |
| ----- | ----- | ----- |
| `click` | CLI argument parsing | pip |
| `pyyaml` | Config file parsing | pip |
| `jinja2` | HTML template rendering | pip |
| `py-tree-sitter` | Optional AST parsing | pip |
| `tree-sitter-languages` | Pre-built grammars | pip |
| `sqlparse` | SQL parsing | pip |
| `rich` | Terminal progress output | pip |

All optional. The core must work with stdlib only. Detect available packages at runtime and degrade gracefully.

### **8.2 Performance Guidelines**

* Process files concurrently using `concurrent.futures.ThreadPoolExecutor` with `max_workers = os.cpu_count()`.  
* Skip binary files (detect via null-byte sampling of first 8KB).  
* Skip files above a configurable size limit (default: 5MB).  
* Cache the language detection result per extension.  
* For repositories with \> 10,000 files, print progress to stderr if `--verbose`.

### **8.3 Go Alternative**

If implementing in Go, use:

* `cobra` for CLI  
* `gopkg.in/yaml.v3` for config  
* `html/template` for HTML rendering  
* `encoding/json` for JSON  
* Goroutines with a semaphore for file concurrency

The Go version is preferable if binary distribution is a priority (single static binary, no Python runtime dependency).

### **8.4 Incremental Mode**

For large repos, add `--incremental` which uses `git diff --name-only HEAD~1 HEAD` to identify changed files, reuses the previous snapshot's per-file data for unchanged files, and only re-analyzes changed files. This reduces runtime to near-constant regardless of repo size.

---

## **9\. File and Directory Layout**

repo-metrics/  
├── src/  
│   ├── main.py (or main.go)  
│   ├── scanner.py          \# directory walk, file collection  
│   ├── languages.py        \# language definitions, LOC counter  
│   ├── extractors/  
│   │   ├── csharp.py       \# C\# regex extractor  
│   │   ├── typescript.py   \# TS/JS regex extractor  
│   │   ├── python\_ext.py   \# Python extractor (uses ast stdlib)  
│   │   ├── sql.py          \# SQL extractor (uses sqlparse)  
│   │   ├── css.py          \# CSS/SCSS extractor  
│   │   └── html.py         \# HTML extractor  
│   ├── complexity.py       \# Cyclomatic complexity engine  
│   ├── history.py          \# History read/write/merge  
│   ├── renderers/  
│   │   ├── json\_renderer.py  
│   │   ├── markdown\_renderer.py  
│   │   └── html\_renderer.py  
│   └── hook.py             \# install-hook subcommand  
├── templates/  
│   └── report.html.j2      \# Jinja2 HTML template (embedded at build time)  
├── pyproject.toml  
├── README.md  
└── tests/  
    ├── fixtures/            \# sample files per language  
    └── test\_\*.py

---

## **10\. Example JSON Snapshot (Abbreviated)**

{  
  "snapshot\_at": "2025-06-01T09:15:00Z",  
  "commit\_sha": "d4e5f6a7b8c9",  
  "commit\_message": "feat: add billing module",  
  "branch": "main",  
  "summary": {  
    "total\_files": 842,  
    "total\_lines": 187430,  
    "total\_loc": 124890,  
    "total\_blank": 31200,  
    "total\_comment": 31340,  
    "comment\_ratio": 0.251,  
    "total\_size\_bytes": 4821000  
  },  
  "languages": {  
    "csharp":     { "file\_count": 312, "loc": 72400, "pct\_of\_total\_loc": 57.97 },  
    "typescript": { "file\_count": 198, "loc": 31200, "pct\_of\_total\_loc": 24.98 },  
    "html":       { "file\_count": 87,  "loc": 9800,  "pct\_of\_total\_loc": 7.85 },  
    "css":        { "file\_count": 44,  "loc": 5100,  "pct\_of\_total\_loc": 4.08 },  
    "sql":        { "file\_count": 31,  "loc": 3800,  "pct\_of\_total\_loc": 3.04 },  
    "python":     { "file\_count": 12,  "loc": 2590,  "pct\_of\_total\_loc": 2.07 }  
  },  
  "entities": {  
    "csharp": {  
      "namespaces": 48, "classes": 287, "interfaces": 63,  
      "records": 41, "enums": 28, "methods": 2140,  
      "properties": 1820, "ef\_dbsets": 18, "ef\_entities": 18  
    },  
    "typescript": {  
      "classes": 94, "interfaces": 182, "types": 67,  
      "functions": 541, "react\_components": 118, "hooks": 34  
    }  
  },  
  "api": {  
    "total\_endpoints": 147,  
    "by\_method": { "GET": 58, "POST": 42, "PUT": 28, "DELETE": 15, "PATCH": 4 },  
    "controllers": 18  
  },  
  "database": {  
    "table\_count": 34, "migration\_count": 89,  
    "tables": \["users", "organizations", "workspaces", "..."\],  
    "ef\_entities": \["User", "Organization", "Workspace", "..."\]  
  },  
  "tests": {  
    "test\_file\_count": 124,  
    "test\_loc": 18400,  
    "test\_to\_source\_ratio": 0.172,  
    "unit\_test\_count": 894,  
    "xunit\_facts": 712, "xunit\_theories": 182,  
    "jest\_tests": 234, "integration\_tests": 67, "e2e\_tests": 12  
  },  
  "quality": {  
    "avg\_complexity": 4.2,  
    "median\_complexity": 3.0,  
    "p95\_complexity": 11.0,  
    "max\_complexity": 38,  
    "max\_complexity\_location": "src/Billing/InvoiceService.cs::CalculateTieredDiscount",  
    "high\_complexity\_count": 23,  
    "complexity\_distribution": { "1-5": 1820, "6-10": 312, "11-20": 87, "21-50": 21, "51+": 2 },  
    "todo\_count": 47, "fixme\_count": 12, "hack\_count": 4,  
    "long\_files": 8, "long\_methods": 34,  
    "health\_score": 74, "health\_grade": "C"  
  },  
  "dependencies": {  
    "nuget\_packages": 42, "npm\_packages": 87, "npm\_dev\_packages": 31  
  }  
}

---

## **11\. Suggested Phased Implementation**

**Phase 1 — Core (Week 1\)**  
 File scanner, LOC counter, language breakdown, JSON output, history append, Markdown output.

**Phase 2 — Entities and APIs (Week 2\)**  
 Regex extractors for all languages, entity counts, API endpoint detection, database/schema metrics, test detection.

**Phase 3 — Quality Metrics (Week 3\)**  
 Regex-based cyclomatic complexity, quality signals (TODO/FIXME), file-level hotspot ranking, health score.

**Phase 4 — HTML Report (Week 4\)**  
 Jinja2 HTML template, embedded Chart.js trend charts, self-contained single-file output.

**Phase 5 — Polish (Week 5\)**  
 Git hook installer, incremental mode, optional AST parsers via tree-sitter, optional duplication detection, gate mode.
