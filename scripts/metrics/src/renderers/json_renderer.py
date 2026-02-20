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
