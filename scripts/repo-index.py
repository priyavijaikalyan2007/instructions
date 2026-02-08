#!/usr/bin/env python3
# AGENT: Local repository indexer for fast search and analysis.

from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple

from repo_index_lib import (
    detect_language,
    extract_markers,
    get_env,
    hash_content,
    normalise_excluded_dirs,
    normalise_extensions,
    read_text_file,
    resolve_index_dir,
    resolve_repo_root,
    should_index_path,
)

DEFAULT_MAX_BYTES = 1_000_000


CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS files (
    path TEXT PRIMARY KEY,
    size_bytes INTEGER NOT NULL,
    modified_utc TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    language TEXT NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS file_fts USING fts5(
    path,
    content,
    markers,
    tokenize = 'unicode61'
);
"""


def build_index(db_path: Path, repo_root: Path, max_bytes: int) -> Tuple[int, int]:
    included_exts = normalise_extensions(get_env("_REPO_INDEX_EXTS"))
    excluded_dirs = normalise_excluded_dirs(get_env("_REPO_INDEX_EXCLUDED"))

    if db_path.exists():
        raise RuntimeError("Index already exists. Use rebuild or clear.")

    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.executescript(CREATE_TABLES_SQL)

        files_indexed = 0
        files_skipped = 0

        for path in repo_root.rglob("*"):
            if not should_index_path(path, included_exts, excluded_dirs):
                continue

            try:
                content = read_text_file(path, max_bytes)
            except OSError:
                files_skipped += 1
                continue

            if content is None:
                files_skipped += 1
                continue

            metadata = path.stat()
            language = detect_language(path)
            markers = ";".join(extract_markers(content))
            digest = hash_content(content)
            relative_path = str(path.relative_to(repo_root))
            modified_utc = datetime.fromtimestamp(metadata.st_mtime, tz=timezone.utc).isoformat()

            conn.execute(
                "INSERT OR REPLACE INTO files (path, size_bytes, modified_utc, sha256, language) VALUES (?, ?, ?, ?, ?)",
                (
                    relative_path,
                    metadata.st_size,
                    modified_utc,
                    digest,
                    language,
                ),
            )

            conn.execute(
                "INSERT INTO file_fts (path, content, markers) VALUES (?, ?, ?)",
                (relative_path, content, markers),
            )

            files_indexed += 1

    return (files_indexed, files_skipped)


def rebuild_index(db_path: Path, repo_root: Path, max_bytes: int) -> Tuple[int, int]:
    if db_path.exists():
        db_path.unlink()

    return build_index(db_path, repo_root, max_bytes)


def clear_index(db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()


def get_status(db_path: Path) -> Tuple[int, int]:
    if not db_path.exists():
        return (0, 0)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM files")
        files = int(cursor.fetchone()[0])

        cursor = conn.execute("SELECT COUNT(*) FROM file_fts")
        fts_rows = int(cursor.fetchone()[0])

    return (files, fts_rows)


def search_index(db_path: Path, query: str, limit: int) -> List[Tuple[str, str]]:
    if not db_path.exists():
        return []

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "SELECT path, snippet(file_fts, 1, '[', ']', '...', 20) FROM file_fts WHERE file_fts MATCH ? LIMIT ?",
            (query, limit),
        )
        return [(row[0], row[1]) for row in cursor.fetchall()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local repository index for fast search.")
    parser.add_argument("command", choices=["build", "rebuild", "clear", "status", "search"])
    parser.add_argument("query", nargs="?", default=None)
    parser.add_argument("--limit", type=int, default=20)

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    script_path = Path(__file__)

    repo_root = resolve_repo_root(script_path, get_env("_REPO_INDEX_ROOT"))
    index_dir = resolve_index_dir(repo_root, get_env("_REPO_INDEX_DIR"))
    db_path = index_dir / "repo-index.sqlite"

    max_bytes_raw = get_env("_REPO_INDEX_MAX_BYTES")
    max_bytes = int(max_bytes_raw) if max_bytes_raw else DEFAULT_MAX_BYTES

    try:
        if args.command == "build":
            indexed, skipped = build_index(db_path, repo_root, max_bytes)
            print(f"Indexed {indexed} files. Skipped {skipped} files.")
            print(f"Index location: {db_path}")
        elif args.command == "rebuild":
            indexed, skipped = rebuild_index(db_path, repo_root, max_bytes)
            print(f"Indexed {indexed} files. Skipped {skipped} files.")
            print(f"Index location: {db_path}")
        elif args.command == "clear":
            clear_index(db_path)
            print("Index removed.")
        elif args.command == "status":
            files, fts_rows = get_status(db_path)
            print(f"Index location: {db_path}")
            print(f"Files indexed: {files}")
            print(f"FTS rows: {fts_rows}")
        elif args.command == "search":
            if not args.query:
                raise RuntimeError("Search requires a query string.")

            results = search_index(db_path, args.query, args.limit)
            if not results:
                print("No matches found.")
                return 0

            for path, snippet in results:
                print(f"{path}: {snippet}")
        else:
            raise RuntimeError("Unknown command.")
    except RuntimeError as exc:
        print(str(exc))
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
