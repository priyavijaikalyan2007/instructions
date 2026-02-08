<!-- AGENT: Repository indexing instructions for local per-user search. -->
# Local Repository Index (Per User)

This guide explains how to build and use a local SQLite index for fast repository search and analysis. The index is **not** committed to Git.

## 1) Purpose

The index speeds up:
- Searching for markers and concepts across the repository
- Locating entry points and dependencies
- Finding likely files for bug fixes and reviews
- Querying by language, marker type, or annotation

## 2) Storage Model

The index is stored in:

```
./local/repo-index.sqlite
```

This keeps it out of Git by default (the `local/` directory is in `.gitignore`) and avoids merge conflicts.

You may override the location using environment variables if required.

## 3) Scripts

- Python entry point: `scripts/repo-index.py`
- Library module: `scripts/repo_index_lib.py`
- Bash wrapper: `scripts/repo-index.sh`

Use either script. The wrapper calls `python3` and passes arguments through.

## 4) Commands

Build the index:
```bash
python3 scripts/repo-index.py build
```

Rebuild (delete then build):
```bash
python3 scripts/repo-index.py rebuild
```

Incremental update (re-index only files changed since the last build):
```bash
python3 scripts/repo-index.py update
```

Clear the index:
```bash
python3 scripts/repo-index.py clear
```

Show status:
```bash
python3 scripts/repo-index.py status
```

Search:
```bash
python3 scripts/repo-index.py search "@entrypoint" --limit 50
```

## 5) Environment Variables

Optional environment variables:

```
_REPO_INDEX_ROOT=/path/to/repo
_REPO_INDEX_DIR=/path/to/index/dir
_REPO_INDEX_MAX_BYTES=1000000
_REPO_INDEX_EXTS=.cs,.ts,.js,.html,.css,.md,.sql,.json,.yml,.yaml,.sh,.ps1,.txt,.py,.csproj,.sln,.xml,.razor,.cshtml
_REPO_INDEX_EXCLUDED=.git,.vs,.obsidian,node_modules,bin,obj,coverage,dist,build,out,tmp,temp,wwwroot,local
```

## 6) When to Rebuild

Rebuild the index after any of the following:
- A marker migration pass (see `MARKER_MIGRATION.md`)
- Major code restructuring or file renames
- Adding a new sub-application or module
- Pulling significant changes from the remote

For day-to-day changes, use `update` instead of `rebuild` to re-index only modified files.

## 7) What Gets Indexed

### File Extensions
All text files matching the configured extensions are indexed. The default set covers: `.cs`, `.ts`, `.js`, `.html`, `.css`, `.md`, `.sql`, `.json`, `.yml`, `.yaml`, `.sh`, `.ps1`, `.txt`, `.py`, `.csproj`, `.sln`, `.xml`, `.razor`, `.cshtml`.

### Marker Extraction
The indexer captures markers from both `MARKERS.md` and `COMMENTING.md`:

| Category | Patterns |
|----------|----------|
| Navigation | `@entrypoint`, `@dependency`, `@maps_to`, `@config`, `@middleware`, `@background` |
| Flow | `Dispatches:`, `Handles:`, `Delegates to:` |
| Agent work | `@agent:test`, `@agent:security`, `@agent:review`, `@agent:refactor` |
| Concepts | `[[`, `⚓` |
| Annotations | `TODO`, `FIXME`, `BUG`, `BUGFIX`, `HACK`, `PERF`, `SECURITY`, `DEPRECATED` |

## 8) Search Examples

Basic marker search:
```bash
python3 scripts/repo-index.py search "@entrypoint" --limit 20
```

Find all files related to a concept:
```bash
python3 scripts/repo-index.py search "TaxCalculation"
```

Find security-sensitive code:
```bash
python3 scripts/repo-index.py search "SECURITY"
```

Find TODO items:
```bash
python3 scripts/repo-index.py search "TODO" --limit 100
```

Find files that map to a database table:
```bash
python3 scripts/repo-index.py search "@maps_to"
```

## 9) Notes

- Files larger than `_REPO_INDEX_MAX_BYTES` (default 1 MB) are skipped.
- Only UTF-8 text files are indexed.
- Marker hints like `@entrypoint`, `@maps_to`, `⚓`, `[[Concept]]`, `TODO`, `SECURITY`, etc. are captured in a dedicated column for fast filtering.
- The index complements but does not replace the knowledge base in `./agentknowledge/`. Use the index for full-text search; use the knowledge base for structured concept and decision queries.
