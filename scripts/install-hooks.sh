#!/bin/bash
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: fb08d7ab-ab74-4b82-b781-c1bf0b60c0b4
# Created: 2026

# ⚓ COMPONENT: GitHookInstaller
# 📜 PURPOSE: Installs consolidated Repository Index and Metrics hooks.
# 🔗 RELATES: [[MetricsAnalyzer]], [[RepoIndexer]]
# ⚡ FLOW: [User] -> [This] -> [.git/hooks/post-commit]

set -euo pipefail

# @entrypoint: install-hooks
REPO_PATH="${1:-.}"
REPO_PATH=$(realpath "$REPO_PATH")

if [ ! -d "$REPO_PATH/.git" ]; then
    echo "Error: $REPO_PATH is not a git repository." >&2
    exit 1
fi

HOOK_DIR="$REPO_PATH/.git/hooks"
POST_COMMIT_HOOK="$HOOK_DIR/post-commit"

# Resolve absolute paths to the scripts in this project
# @dependency: scripts/metrics/repo-metrics.sh
# @dependency: scripts/repo-index.sh
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

# Metrics runner path
METRICS_RUNNER="$SCRIPT_DIR/metrics/repo-metrics.sh"
# Index runner path
INDEX_RUNNER="$PROJECT_ROOT/scripts/repo-index.sh"

echo "Installing hooks into $REPO_PATH..."

# Create or append to post-commit hook
# ⚓ PostCommitHookTemplate: Defines the structure of the generated git hook
cat << EOF > "$POST_COMMIT_HOOK"
#!/bin/bash
# Git post-commit hook for Repository Index and Metrics
set -euo pipefail

REPO_ROOT=\$(git rev-parse --show-toplevel)

# 1) Update Repository Index
if [ -x "$INDEX_RUNNER" ]; then
    echo "[repo-index] Updating index..."
    "$INDEX_RUNNER" update "\$REPO_ROOT" 2>/dev/null &
fi

# 2) Run Repository Metrics
if [ -x "$METRICS_RUNNER" ]; then
    echo "[repo-metrics] Collecting metrics..."
    "$METRICS_RUNNER" --out-dir ".metrics" "\$REPO_ROOT" 2>/dev/null &
fi
EOF

chmod +x "$POST_COMMIT_HOOK"

echo "Successfully installed post-commit hook to $POST_COMMIT_HOOK"
echo "Metrics and Indexing will run asynchronously after each commit."