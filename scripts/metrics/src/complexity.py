# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 84473682-8e8f-4c0b-894d-8ced66ecc829
# Created: 2026

"""
⚓ COMPONENT: ComplexityEngine
📜 PURPOSE: Computes cyclomatic complexity and identifies code blocks for analysis.
🔗 RELATES: [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [MetricsOutput]
"""

import re
import logging
from typing import Dict, List, Optional

# Set up logging
logger = logging.getLogger(__name__)

def compute_cyclomatic_complexity(text: str) -> int:
    """
    Compute cyclomatic complexity for a block of code based on a regex pattern.
    
    The algorithm starts at 1 and adds 1 for each decision point.

    Args:
        text: The string content of the code block.

    Returns:
        The calculated cyclomatic complexity as an integer.
    """
    # ⚓ ComplexityAlgorithm: Baseline decision-point counting
    complexity = 1
    
    # Decisions patterns for C#, TS/JS, Python, Go, CSS/SCSS
    patterns = [
        r'\bif\b',
        r'\belse\s+if\b|\belif\b',
        r'\bfor\b',
        r'\bforeach\b',
        r'\bwhile\b',
        r'\bcase\b',
        r'\bcatch\b',
        r'&&|\band\b',
        r'\|\||\bor\b',
        r'\?(?!\?)',   # ternary (not null-coalescing)
        r'\?\?'        # null-coalescing
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        complexity += len(matches)
        
    return complexity

def identify_blocks(content: str, language: str) -> List[str]:
    """
    Segment content into logical blocks (functions/methods) for complexity analysis.

    Args:
        content: The full content of the file.
        language: The language identifier to select the appropriate heuristic.

    Returns:
        A list of string blocks, each representing a function or method.
    """
    # TRACE: Identifying blocks
    logger.debug(f"Identifying blocks for language: {language}")
    
    blocks = []
    
    # BRANCH: Python indentation-based blocks
    if language in ["python"]:
        lines = content.splitlines()
        current_block = []
        in_block = False
        base_indent = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
                
            indent = (len(line) - len(line.lstrip()))
            
            # Heuristic: Function or method definition
            if (stripped.startswith("def ") or stripped.startswith("async def ")):
                if in_block:
                    blocks.append("\n".join(current_block))
                current_block = [line]
                in_block = True
                base_indent = indent
            elif in_block:
                if indent > base_indent:
                    current_block.append(line)
                else:
                    blocks.append("\n".join(current_block))
                    current_block = []
                    in_block = False
                    
        if current_block:
            blocks.append("\n".join(current_block))
            
    # BRANCH: Brace-delimited blocks (C#, TS, JS, Go, CSS)
    elif language in ["csharp", "typescript", "javascript", "go", "css"]:
        # Regex to find starting positions of functions/classes
        if language == "csharp":
            # public void MyMethod(args) {
            pattern = r'(?:public|private|internal|protected|static|async|override|virtual)?\s+\w+(?:<.+>)?\s+\w+\s*\(.*\)\s*\{'
        elif language in ["typescript", "javascript"]:
            # function myFunc() { or const myFunc = () => {
            pattern = r'(?:function\s+\w+\s*\(.*\)|(?:\w+\s*=\s*(?:\(.*\)|[\w\s,]+)\s*=>))\s*\{'
        elif language == "go":
            # func MyFunc() {
            pattern = r'func\s+(?:\(.*\)\s+)?\w+\s*\(.*\)\s*(?:\(.*\)\s+)?\{'
        elif language == "css":
            # selector {
            pattern = r'[^{]+\{'
        else:
            pattern = r'\{' # Fallback
            
        for match in re.finditer(pattern, content, re.MULTILINE):
            start = match.start()
            # ⚓ BraceMatchingHeuristic: Simple stack-based brace matching
            brace_count = 0
            end = -1
            for i in range(start, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = (i + 1)
                        break
            if end != -1:
                blocks.append(content[start:end])
                
    # BRANCH: SQL procedural blocks
    elif language in ["sql"]:
        pattern = r'\bCREATE\s+(?:PROCEDURE|FUNCTION|TRIGGER)\b'
        for match in re.finditer(pattern, content, re.IGNORECASE):
            # Take from start of procedure to end of file as a simple heuristic
            blocks.append(content[match.start():])
            
    # BRANCH: Default (skip for documentation or data files)
    else:
        pass
        
    return blocks