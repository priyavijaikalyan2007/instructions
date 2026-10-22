#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 4d44aaf6-915f-4c4c-b278-5dce96b9afeb
# Created: 2026

# COMPONENT: Project configuration entry point
# PURPOSE: Configure project instructions from any working directory.
# RELATES: scripts/configure_instructions.py, instructions/REPO.md
# FLOW: CLI arguments -> Python interview/editor.

set -euo pipefail

repository_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${repository_directory}/scripts/configure_instructions.py" "$@"
