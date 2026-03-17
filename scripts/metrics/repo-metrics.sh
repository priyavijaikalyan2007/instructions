#!/bin/bash
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 294f9237-e48c-4fa3-91be-180fbbffd3d5
# Created: 2026

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