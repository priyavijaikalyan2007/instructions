# AGENT: Helper utilities for repository indexing. Keep logic pure for unit tests.

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

DEFAULT_EXTENSIONS = {
    ".cs",
    ".ts",
    ".js",
    ".html",
    ".css",
    ".md",
    ".sql",
    ".json",
    ".yml",
    ".yaml",
    ".sh",
    ".ps1",
    ".txt",
}

DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".vs",
    ".obsidian",
    "node_modules",
    "bin",
    "obj",
    "coverage",
    "dist",
    "build",
    "out",
    "tmp",
    "temp",
}

LANGUAGE_BY_EXTENSION = {
    ".cs": "csharp",
    ".ts": "typescript",
    ".js": "javascript",
    ".html": "html",
    ".css": "css",
    ".md": "markdown",
    ".sql": "sql",
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".sh": "shell",
    ".ps1": "powershell",
    ".txt": "text",
}

MARKER_PATTERNS = [
    "@entrypoint",
    "@dependency",
    "@maps_to",
    "@agent:test",
    "@agent:security",
    "@agent:review",
    "@agent:refactor",
    "[[",
    "⚓",
]


def normalise_extensions(raw: Optional[str]) -> Sequence[str]:
    if not raw:
        return sorted(DEFAULT_EXTENSIONS)

    parts = [part.strip() for part in raw.split(",") if part.strip()]
    output = []

    for part in parts:
        if not part.startswith("."):
            output.append(f".{part}")
        else:
            output.append(part)

    return sorted(set(output))


def normalise_excluded_dirs(raw: Optional[str]) -> Sequence[str]:
    if not raw:
        return sorted(DEFAULT_EXCLUDED_DIRS)

    parts = [part.strip() for part in raw.split(",") if part.strip()]

    return sorted(set(parts))


def should_skip_path(path: Path, excluded_dirs: Iterable[str]) -> bool:
    for part in path.parts:
        if part in excluded_dirs:
            return True

    return False


def should_index_path(path: Path, included_exts: Iterable[str], excluded_dirs: Iterable[str]) -> bool:
    if path.is_dir():
        return False

    if path.is_symlink():
        return False

    if should_skip_path(path, excluded_dirs):
        return False

    if path.suffix.lower() not in set(included_exts):
        return False

    return True


def detect_language(path: Path) -> str:
    return LANGUAGE_BY_EXTENSION.get(path.suffix.lower(), "text")


def is_text_payload(payload: bytes) -> bool:
    if not payload:
        return True

    try:
        payload.decode("utf-8")
    except UnicodeDecodeError:
        return False

    return True


def read_text_file(path: Path, max_bytes: int) -> Optional[str]:
    size = path.stat().st_size

    if size > max_bytes:
        return None

    payload = path.read_bytes()

    if not is_text_payload(payload):
        return None

    return payload.decode("utf-8")


def extract_markers(text: str) -> List[str]:
    markers: List[str] = []

    for pattern in MARKER_PATTERNS:
        if pattern in text:
            markers.append(pattern)

    return markers


def hash_content(text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return digest


def resolve_repo_root(script_path: Path, override: Optional[str]) -> Path:
    if override:
        return Path(override).resolve()

    return script_path.resolve().parents[1]


def resolve_index_dir(repo_root: Path, override: Optional[str]) -> Path:
    if override:
        return Path(override).resolve()

    return repo_root / "local"


def get_env(name: str) -> Optional[str]:
    value = os.environ.get(name)

    if value is None:
        return None

    if not value.strip():
        return None

    return value.strip()
