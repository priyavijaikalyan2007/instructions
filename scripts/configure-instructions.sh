#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: b6c66ae1-6de3-40f1-abd8-10e5d809a670
# Created: 2026

# COMPONENT: Instruction profile entry point
# PURPOSE: Forward quoted arguments to the standard-library Python configurator.
# RELATES: configure_instructions.py, instructions/REPO.md
# FLOW: CLI arguments -> Python interview/editor.

set -euo pipefail

script_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "${script_directory}/configure_instructions.py" "$@"
