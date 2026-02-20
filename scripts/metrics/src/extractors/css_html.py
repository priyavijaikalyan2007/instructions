"""
⚓ COMPONENT: WebExtractor
📜 PURPOSE: Extracts entities from CSS and HTML, including rule sets, variables, and component references.
🔗 RELATES: [[BaseExtractor]], [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [FrontendMetrics]
"""

import re
import logging
from typing import Dict, Any
from . import BaseExtractor, get_unique_matches

# Set up logging
logger = logging.getLogger(__name__)

class CSSExtractor(BaseExtractor):
    """
    Entity extractor for CSS, SCSS, and Less files.
    """
    def __init__(self):
        """Initializes the CSS extractor with style-specific patterns."""
        super().__init__("css")
        self.patterns = {
            "rule_sets": r'[^{]+\{',
            "variables": r'(--[\w-]+|\$[\w-]+)',
            "media_queries": r'@media\s+[^{]+\{',
            "keyframes": r'@keyframes\s+\w+',
            "imports": r'@import\s+[\'"](.+)[\'"]'
        }

    def extract(self, content: str) -> Dict[str, Any]:
        """
        Extracts CSS metadata including unique variables.

        Args:
            content: The stylesheet content.

        Returns:
            Dictionary of metrics.
        """
        # DEBUG: Starting CSS extraction
        results = super().extract(content)
        
        # ⚓ StyleInventory: Track unique variables and custom properties
        variables = re.findall(self.patterns["variables"], content)
        results["variables_count"] = len(set(variables))
        results["variables"] = sorted(list(set(variables)))
        
        return results

class HTMLExtractor(BaseExtractor):
    """
    Entity extractor for HTML and template files (Razor, JSX, etc.).
    """
    def __init__(self):
        """Initializes the HTML extractor with tag-based patterns."""
        super().__init__("html")
        self.patterns = {
            "templates": r'<\w+', 
            "component_references": r'<([A-Z]\w+|[\w-]+-[\w-]+)', 
            "script_tags": r'<script\b',
            "style_tags": r'<style\b',
            "form_elements": r'<form\b'
        }

    def extract(self, content: str) -> Dict[str, Any]:
        """
        Extracts HTML metadata including custom component references.

        Args:
            content: The HTML or template content.

        Returns:
            Dictionary of metrics.
        """
        # DEBUG: Starting HTML extraction
        results = super().extract(content)
        
        # ⚓ ComponentTracking: Identify use of custom tags/components
        components = re.findall(self.patterns["component_references"], content)
        results["component_references_count"] = len(set(components))
        results["component_references"] = sorted(list(set(components)))
        
        return results
