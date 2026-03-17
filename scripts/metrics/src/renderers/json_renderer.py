# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: d2d423f4-34ab-4bee-ba8c-c920e4df8f54
# Created: 2026

"""
⚓ COMPONENT: JSONRenderer
📜 PURPOSE: Serializes metrics snapshots to JSON files.
🔗 RELATES: [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [JSONFile]
"""

import json
import os
import logging

# Set up logging
logger = logging.getLogger(__name__)

def render_json(snapshot: dict, output_path: str):
    """
    Writes the metrics snapshot to a formatted JSON file.

    Args:
        snapshot: The metrics data dictionary.
        output_path: Destination file path.
    """
    # DEBUG: Rendering JSON
    logger.debug(f"Rendering JSON snapshot to: {output_path}")
    
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(snapshot, f, indent=2)
        logger.info(f"JSON report generated: {output_path}")
    except OSError as e:
        logger.error(f"Failed to write JSON report: {e}")