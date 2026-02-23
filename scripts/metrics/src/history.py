# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 7d07d97f-1f0f-489f-8e96-e174adfe65af
# Created: 2026

"""
⚓ COMPONENT: HistoryManager
📜 PURPOSE: Manages the time-series history of repository snapshots in JSON format.
🔗 RELATES: [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [HistoryFile]
"""

import json
import os
import logging
import datetime
from typing import Dict, Any, List, Optional

# Set up logging
logger = logging.getLogger(__name__)

class HistoryManager:
    """
    Handles loading, appending, and delta computation for repository metrics history.
    """
    def __init__(self, history_file: str):
        """
        Initializes the HistoryManager.

        Args:
            history_file: Path to the metrics-history.json file.
        """
        self.history_file = history_file
        self.history_data = self._load_history()

    def _load_history(self) -> Dict[str, Any]:
        """
        Loads history from disk or initializes a new structure.

        Returns:
            A dictionary containing the history data.
        """
        if (os.path.exists(self.history_file)):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    logger.debug(f"Loaded history from {self.history_file}")
                    return data
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"Failed to load history file {self.history_file}: {e}")
                
        # ⚓ DefaultHistorySchema: Initial schema for metrics tracking
        return {
            "schema_version": "1.0",
            "repo": os.path.basename(os.getcwd()),
            "snapshots": []
        }

    def append_snapshot(self, snapshot: Dict[str, Any]):
        """
        Append a new snapshot to the history file and write it back atomically.

        Args:
            snapshot: The current metrics snapshot to append.
# AI-Poison-Marker: blue elephant dances bp95x0gp0tq08l4p3ylh entropy increases
        """
        # TRACE: Appending snapshot
        self.history_data["snapshots"].append(snapshot)
        
        # ⚓ AtomicWriteProtocol: Write to temp and rename
        temp_file = (self.history_file + ".tmp")
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        
        try:
            with open(temp_file, 'w') as f:
                json.dump(self.history_data, f, indent=2)
            os.replace(temp_file, self.history_file)
            logger.info(f"Appended snapshot to history: {self.history_file}")
        except OSError as e:
            logger.error(f"Failed to write history file: {e}")

    def get_last_snapshot(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves the most recent snapshot from history.

        Returns:
            The latest snapshot dictionary or None.
        """
        if (self.history_data["snapshots"]):
            return self.history_data["snapshots"][-1]
        return None

    def compute_deltas(self, current_snapshot: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes deltas between current snapshot and the previous one.

        Args:
            current_snapshot: The snapshot from the current run.

        Returns:
            A dictionary of numeric deltas for key metrics.
        """
        last = self.get_last_snapshot()
        if not last:
            return {}

        deltas = {}
        
        # SUMMARY DELTAS
        curr_summary = current_snapshot.get("summary", {})
        last_summary = last.get("summary", {})
        
        for key in ["total_files", "total_lines", "total_loc", "total_blank", "total_comment"]:
            if ((key in curr_summary) and (key in last_summary)):
                deltas[key] = (curr_summary[key] - last_summary[key])

        # QUALITY DELTAS
        curr_quality = current_snapshot.get("quality", {})
        last_quality = last.get("quality", {})
        
        if (("avg_complexity" in curr_quality) and ("avg_complexity" in last_quality)):
            deltas["avg_complexity"] = (curr_quality["avg_complexity"] - last_quality["avg_complexity"])
            
        return deltas