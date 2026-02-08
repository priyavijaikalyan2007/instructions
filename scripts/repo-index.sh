#!/usr/bin/env bash
# AGENT: Wrapper for the local repository indexer.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "python3 is required but not found." >&2
    exit 1
fi

"$PYTHON_BIN" "$SCRIPT_DIR/repo-index.py" "$@"
