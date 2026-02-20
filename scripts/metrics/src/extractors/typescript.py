"""
⚓ COMPONENT: TypeScriptExtractor
📜 PURPOSE: Extracts TS/JS-specific entities like classes, hooks, components, and imports.
🔗 RELATES: [[BaseExtractor]], [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [MetricsData]
"""

import re
import logging
from typing import Dict, Any
from . import BaseExtractor, get_unique_matches

# Set up logging
logger = logging.getLogger(__name__)

class TypeScriptExtractor(BaseExtractor):
    """
    Entity extractor for TypeScript and JavaScript code using heuristics and regex.
    """
    def __init__(self):
        """Initializes the TS/JS extractor with common patterns."""
        super().__init__("typescript")
        self.patterns = {
            "classes": r'\bclass\s+\w+',
            "interfaces": r'\binterface\s+\w+',
            "types": r'\btype\s+\w+',
            "enums": r'\benum\s+\w+',
            "functions": r'(?:function\s+\w+\s*\(.*\)|(?:\w+\s*=\s*(?:\(.*\)|[\w\s,]+)\s*=>))',
            "hooks": r'\buse[A-Z]\w+',
            "exports_named": r'\bexport\s+(?:const|let|var|class|function|type|interface|enum)\b',
            "exports_default": r'\bexport\s+default\b',
            "imports": r'\bimport\s+.*from\s+[\'"](.+)[\'"]'
        }

    def extract(self, content: str) -> Dict[str, Any]:
        """
        Extracts JS/TS metadata including React component detection.

        Args:
            content: The file content.

        Returns:
            Dictionary of metrics.
        """
        # DEBUG: Starting TS extraction
        results = super().extract(content)
        
        # ⚓ ImportTracking: Log unique module dependencies
        imports = re.findall(self.patterns["imports"], content)
        results["imports_count"] = len(set(imports))
        results["imports"] = sorted(list(set(imports)))
        
        # ⚓ ReactComponentHeuristic: Detect functions returning JSX
        react_components = re.findall(
            r'(?:(?:class|function|const)\s+([A-Z]\w+).*(?:return\s*\(?\s*<|=>\s*\(?\s*<))', 
            content
        )
        results["react_components"] = len(set(react_components))
        
        return results
