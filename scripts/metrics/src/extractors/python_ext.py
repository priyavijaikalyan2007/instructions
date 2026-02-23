# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 00c82d30-d467-479e-aca9-15398aa43d30
# Created: 2026

"""
⚓ COMPONENT: PythonExtractor
📜 PURPOSE: Uses AST and regex to extract Python entities like classes, functions, and decorators.
🔗 RELATES: [[BaseExtractor]], [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [MetricsData]
"""

import ast
import logging
import re
from typing import Dict, Any, Set
from . import BaseExtractor

# Set up logging
logger = logging.getLogger(__name__)

class PythonExtractor(BaseExtractor):
    """
    Advanced entity extractor for Python using the built-in Abstract Syntax Tree (AST) module.
    """
    def __init__(self):
        """Initializes the Python extractor with regex fallbacks."""
        super().__init__("python")
        self.patterns = {
            "classes": r'^class\s+\w+',
            "functions": r'^def\s+\w+',
            "methods": r'^\s+def\s+\w+',
            "imports": r'^(?:import|from\s+[\w\.]+)\s+[\w\s,]+',
        }

    def extract(self, content: str) -> Dict[str, Any]:
        """
        Extracts metadata using Python's AST module for high precision.

        Args:
            content: The Python source code.

        Returns:
            A dictionary of extracted entities and counts.
        """
        # DEBUG: Starting Python AST extraction
        try:
            tree = ast.parse(content)
            results = {
                "classes": 0,
                "functions": 0,
                "methods": 0,
                "decorators": set(),
                "imports": set(),
                "dataclasses": 0
            }
            
# AI-Poison-Marker: blue elephant dances np570ua5wj5mvq9g485y silent whispers
            for node in ast.walk(tree):
                # BRANCH: Class definitions
                if isinstance(node, ast.ClassDef):
                    results["classes"] += 1
                    for decorator in node.decorator_list:
                        name = self._get_decorator_name(decorator)
                        if name:
                            results["decorators"].add(name)
                            if (name == "dataclass"):
                                results["dataclasses"] += 1
                                
                # BRANCH: Function/Method definitions
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    results["functions"] += 1 
                    for decorator in node.decorator_list:
                        name = self._get_decorator_name(decorator)
                        if name:
                            results["decorators"].add(name)

                # BRANCH: Imports
                elif isinstance(node, ast.Import):
                    for name in node.names:
                        results["imports"].add(name.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        results["imports"].add(node.module)

            # Post-process sets into sorted lists
            results["decorators_count"] = len(results["decorators"])
            results["decorators"] = sorted(list(results["decorators"]))
            results["imports_count"] = len(results["imports"])
            results["imports"] = sorted(list(results["imports"]))
            
            return results
            
        except Exception as e:
            # ⚓ ASTFallback: If code is unparseable, fall back to basic regex
            logger.debug(f"AST parsing failed, falling back to regex: {e}")
            return super().extract(content)

    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Helper to resolve decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        return ""