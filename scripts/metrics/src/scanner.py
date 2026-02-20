"""
⚓ COMPONENT: FileScanner
📜 PURPOSE: Recursively walks a repository to find and filter files for analysis.
🔗 RELATES: [[MetricsAnalyzer]], [[LanguageDefinitions]]
⚡ FLOW: [Main] -> [This] -> [FileSystem]
"""

import os
import fnmatch
import logging
from typing import List, Optional, Set, Dict

# Set up logging
logger = logging.getLogger(__name__)

def is_binary(file_path: str) -> bool:
    """
    Sample the first 8KB of a file to check if it's binary.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        True if the file appears to be binary, False otherwise.
    """
    # TRACE: Checking if file is binary
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(8192)
            # ⚓ BinaryDetectionHeuristic: Presence of null byte in first 8KB
            if b"\x00" in chunk:
                return True
    except (OSError, UnicodeDecodeError) as e:
        logger.debug(f"Error reading file {file_path} for binary check: {e}")
        return True
        
    return False

def walk_repository(
    repo_path: str,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    max_depth: Optional[int] = None
) -> List[str]:
    """
    Walk the repository and return a list of files matching the filters.

    Args:
        repo_path: Root directory of the repository.
        include_patterns: List of glob patterns to include.
        exclude_patterns: List of glob patterns to exclude.
        max_depth: Maximum directory depth to traverse.

    Returns:
        A list of absolute file paths matching the criteria.
    """
    # DEBUG: Entering repository walk
    logger.debug(f"Walking repository at: {repo_path}")

    if include_patterns is None:
        include_patterns = ["*"]
        
    if exclude_patterns is None:
        # @config: DefaultExcludePatterns
        exclude_patterns = [
            "**/node_modules/**",
            "**/bin/**",
            "**/obj/**",
            "**/.git/**",
            "**/dist/**",
            "**/build/**",
            "**/coverage/**",
            "**/*.min.js",
            "**/*.min.css"
        ]

    matched_files = []
    
    def matches_any(path: str, patterns: List[str]) -> bool:
        """Helper to match a path against a list of glob patterns."""
        for pattern in patterns:
            if (fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern)):
                return True
        return False

    base_depth = repo_path.rstrip(os.path.sep).count(os.path.sep)

    for root, dirs, files in os.walk(repo_path):
        # Apply depth limit
        current_depth = (root.count(os.path.sep) - base_depth)
        
        # BRANCH: Depth limit check
        if ((max_depth is not None) and (current_depth > max_depth)):
            dirs[:] = [] # Stop recursion
            continue

        # Prune excluded directories
        rel_root = os.path.relpath(root, repo_path)
        if rel_root == ".":
            rel_root = ""
            
        # Update dirs in-place to avoid walking into excluded paths
        dirs[:] = [d for d in dirs if not matches_any(os.path.join(rel_root, d), exclude_patterns)]

        for file in files:
            rel_file_path = os.path.join(rel_root, file)
            
            # BRANCH: Check excludes
            if matches_any(rel_file_path, exclude_patterns):
                continue
                
            # BRANCH: Check includes
            if not matches_any(rel_file_path, include_patterns):
                continue
                
            full_path = os.path.join(root, file)
            
            # BRANCH: Skip binary files
            if not is_binary(full_path):
                matched_files.append(full_path)
            else:
                logger.debug(f"Skipping binary file: {rel_file_path}")
                
    # EXIT: Return list of matched files
    logger.info(f"Walk complete. Found {len(matched_files)} files.")
    return matched_files
