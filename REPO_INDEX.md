<!-- AGENT: Repository indexing instructions for local per-user search. -->
# Local Repository Index (Per User)

This guide explains how to build and use a local SQLite index for fast repository search and analysis. The index is **not** committed to Git.

## 1) Purpose

The index speeds up:
- Searching for markers and concepts across the repository
- Locating entry points and dependencies
- Finding likely files for bug fixes and reviews

## 2) Storage Model

The index is stored in:

```
./local/repo-index.sqlite
```

This keeps it out of Git by default and avoids merge conflicts.

You may override the location using environment variables if required.

## 3) Scripts

- Python entry point: `scripts/repo-index.py`
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
python3 scripts/repo-index.py search \"@entrypoint\" --limit 50
```

## 5) Environment Variables

Optional environment variables:

```
_REPO_INDEX_ROOT=/path/to/repo
_REPO_INDEX_DIR=/path/to/index/dir
_REPO_INDEX_MAX_BYTES=1000000
_REPO_INDEX_EXTS=.cs,.ts,.js,.html,.css,.md,.sql,.json,.yml,.yaml,.sh,.ps1,.txt
_REPO_INDEX_EXCLUDED=.git,.vs,.obsidian,node_modules,bin,obj,coverage,dist,build,out,tmp,temp
```

## 6) Notes

- Files larger than `KNOBBY_REPO_INDEX_MAX_BYTES` are skipped.
- Only UTF-8 text files are indexed.
- Marker hints like `@entrypoint`, `@maps_to`, `⚓`, and `[[Concept]]` are captured in a dedicated column for fast filtering.
