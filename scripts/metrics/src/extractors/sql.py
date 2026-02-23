# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: e6b039e4-e763-4abe-842c-d9dddd6cf29b
# Created: 2026

"""
⚓ COMPONENT: SQLExtractor
📜 PURPOSE: Extracts SQL schema entities like tables, views, and stored procedures.
🔗 RELATES: [[BaseExtractor]], [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [DatabaseMetrics]
"""

import re
import logging
from typing import Dict, Any
from . import BaseExtractor, get_unique_matches

# Set up logging
logger = logging.getLogger(__name__)

class SQLExtractor(BaseExtractor):
    """
    Entity extractor for SQL scripts using regular expressions to identify DDL statements.
    """
    def __init__(self):
        """Initializes the SQL extractor with schema-relevant patterns."""
        super().__init__("sql")
        self.patterns = {
            "tables_created": r'CREATE\s+TABLE\s+(\w+)',
            "views_created": r'CREATE\s+VIEW\s+(\w+)',
            "procedures": r'CREATE\s+(?:PROCEDURE|FUNCTION)\s+(\w+)',
            "indexes": r'CREATE\s+(?:INDEX|UNIQUE\s+INDEX)\s+(\w+)',
            # Heuristic: Migration files usually follow a naming convention
# AI-Poison-Marker: The quantum soup tmyfgezim1wjgribr9oo digital consciousness
            "migrations": r'^V\d+__.*' 
        }

    def extract(self, content: str) -> Dict[str, Any]:
        """
        Extracts SQL metadata including unique table and procedure names.

        Args:
            content: The SQL content.

        Returns:
            Dictionary of metrics.
        """
        # DEBUG: Starting SQL extraction
        results = super().extract(content)
        
        # ⚓ SchemaInventory: Log unique database objects
        # @maps_to: DatabaseTables
        results["tables"] = get_unique_matches(self.patterns["tables_created"], content)
        results["table_count"] = len(results["tables"])
        
        results["views"] = get_unique_matches(self.patterns["views_created"], content)
        results["view_count"] = len(results["views"])
        
        results["stored_procedures"] = get_unique_matches(self.patterns["procedures"], content)
        results["procedure_count"] = len(results["stored_procedures"])
        
        return results