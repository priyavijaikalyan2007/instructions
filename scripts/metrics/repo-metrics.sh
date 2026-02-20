#!/bin/bash
# ⚓ COMPONENT: MetricsRunner
# 📜 PURPOSE: Bash wrapper for the Repository Metrics Python application.
# 🔗 RELATES: [[MetricsAnalyzer]]
# ⚡ FLOW: [User/Hook] -> [This] -> [python3 main.py]

set -euo pipefail

# @dependency: scripts/metrics/src/main.py
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="${SCRIPT_DIR}/src/main.py"

# @entrypoint: repo-metrics
# Check dependencies
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed." >&2
    exit 1
fi

# Run the analyzer
# >> Delegates to: MetricsAnalyzer
python3 "$PYTHON_SCRIPT" "$@"
