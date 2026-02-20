"""
⚓ COMPONENT: BaseExtractor
📜 PURPOSE: Base class and utilities for regex-based entity extraction.
🔗 RELATES: [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [SpecificExtractor] -> [This]
"""

import re
import logging
from typing import Dict, Any, List, Union

# Set up logging
logger = logging.getLogger(__name__)

class BaseExtractor:
    """
    Base class for language-specific entity extractors using regular expressions.
    """
    def __init__(self, language_name: str):
        """
        Initializes the extractor.

        Args:
            language_name: Name of the language this extractor targets.
        """
        self.language_name = language_name
        self.patterns: Dict[str, Union[str, List[str]]] = {}

    def extract(self, content: str) -> Dict[str, Any]:
        """
        Runs the defined patterns against the provided content.

        Args:
            content: The string content of the file.

        Returns:
            A dictionary of extracted counts or lists.
        """
        # TRACE: Starting extraction
        logger.debug(f"Running extractor for: {self.language_name}")
        
        results: Dict[str, Any] = {}
        for key, pattern in self.patterns.items():
            if isinstance(pattern, list):
                total = 0
                for p in pattern:
                    total += len(re.findall(p, content))
                results[key] = total
            else:
                results[key] = len(re.findall(pattern, content))
                
        return results

def get_unique_matches(pattern: str, content: str) -> List[str]:
    """
    Finds all unique matches for a pattern in the content.

    Args:
        pattern: The regex pattern to search for.
        content: The string content to search.

    Returns:
        A sorted list of unique matches.
    """
    matches = re.findall(pattern, content)
    return sorted(list(set(matches)))
