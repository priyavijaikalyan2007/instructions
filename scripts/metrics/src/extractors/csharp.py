"""
⚓ COMPONENT: CSharpExtractor
📜 PURPOSE: Extracts C#-specific entities like namespaces, classes, methods, and EF models.
🔗 RELATES: [[BaseExtractor]], [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [MetricsData]
"""

import re
import logging
from typing import Dict, Any
from . import BaseExtractor, get_unique_matches

# Set up logging
logger = logging.getLogger(__name__)

class CSharpExtractor(BaseExtractor):
    """
    Entity extractor for C# source code using regular expressions.
    """
    def __init__(self):
        """Initializes the C# extractor with relevant regex patterns."""
        super().__init__("csharp")
        self.patterns = {
            "namespaces": r'\bnamespace\s+([\w\.]+)',
            "classes": r'\bclass\s+\w+',
            "interfaces": r'\binterface\s+\w+',
            "structs": r'\bstruct\s+\w+',
            "records": r'\brecord\s+\w+',
            "enums": r'\benum\s+\w+',
            # Heuristic for method detection
            "methods": r'(?:public|private|internal|protected|static|async|override|virtual)?\s+\w+(?:<.+>)?\s+\w+\s*\(.*\)\s*(?:\s*\{|=>)',
            "properties": r'(?:public|private|internal|protected|static)?\s+\w+\s+\w+\s*\{\s*(?:get|set|init);?\s*\}',
            "constructors": r'\b(?:public|private|internal|protected)?\s+(\w+)\s*\(.*\)\s*(?::\s*(?:base|this)\(.*\))?\s*\{',
            "delegates": r'\bdelegate\s+\w+\s+\w+\s*\(.*\)',
            "events": r'\bevent\s+\w+\s+\w+',
            "using_directives": r'\busing\s+([\w\.]+);',
            "ef_dbsets": r'DbSet<\w+>\s+\w+',
        }

    def extract(self, content: str) -> Dict[str, Any]:
        """
        Extracts C# metadata including unique namespaces and EF entities.

        Args:
            content: The file content.

        Returns:
            Dictionary of extracted counts and lists.
        """
        # DEBUG: Starting C# extraction
        results = super().extract(content)
        
        # ⚓ UniqueCountLogic: Filter for unique occurrences where applicable
        results["namespaces"] = len(set(re.findall(self.patterns["namespaces"], content)))
        results["using_directives"] = len(set(re.findall(self.patterns["using_directives"], content)))
        
        # @maps_to: EntityFrameworkSchema
        ef_entities = re.findall(r'DbSet<(\w+)>', content)
        results["ef_entities"] = sorted(list(set(ef_entities)))
        results["ef_entities_count"] = len(results["ef_entities"])
        
        return results
