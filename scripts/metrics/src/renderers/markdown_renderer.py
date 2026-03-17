# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 18a0d99d-e351-4bad-ae33-e946e7fa4719
# Created: 2026

"""
⚓ COMPONENT: MarkdownRenderer
📜 PURPOSE: Generates human-readable Markdown summaries of repository metrics.
🔗 RELATES: [[MetricsAnalyzer]]
⚡ FLOW: [Main] -> [This] -> [MarkdownFile]
"""

import os
import logging
from typing import Dict, Any

# Set up logging
logger = logging.getLogger(__name__)

def render_markdown(snapshot: Dict[str, Any], output_path: str, deltas: Dict[str, Any] = None):
    """
    Renders a metrics summary in Markdown format.

    Args:
        snapshot: The metrics data for the current commit.
        output_path: Destination file path.
        deltas: Optional dictionary of changes since the previous run.
    """
    # DEBUG: Rendering Markdown
    logger.debug(f"Rendering Markdown report to: {output_path}")
    
    summary = snapshot.get("summary", {})
    quality = snapshot.get("quality", {})
    
    lines = [
        f"# Repository Metrics — {snapshot.get('commit_sha', 'N/A')} ({snapshot.get('branch', 'N/A')}) — {snapshot.get('snapshot_at', 'N/A')}",
        "",
        "## Summary",
        "| Metric | Value | Δ vs prev |",
        "| :--- | :--- | :--- |"
    ]
    
    def get_delta_str(key: str) -> str:
        """Internal helper to format delta strings."""
        if ((not deltas) or (key not in deltas)):
            return "N/A"
        val = deltas[key]
        return f"{'+' if val > 0 else ''}{val}"

    # Build summary table
    lines.append(f"| Files | {summary.get('total_files', 0)} | {get_delta_str('total_files')} |")
    lines.append(f"| Lines | {summary.get('total_lines', 0)} | {get_delta_str('total_lines')} |")
    lines.append(f"| LOC | {summary.get('total_loc', 0)} | {get_delta_str('total_loc')} |")
    lines.append(f"| Comment Ratio | {summary.get('comment_ratio', 0):.2f} | N/A |")
    
    # Build language breakdown table
    lines.extend([
        "",
        "## Language Breakdown",
        "| Language | Files | LOC | % |",
        "| :--- | :--- | :--- | :--- |"
    ])
    
    languages = snapshot.get("languages", {})
    for lang, data in sorted(languages.items(), key=lambda x: x[1].get("loc", 0), reverse=True):
        lines.append(f"| {lang} | {data.get('file_count', 0)} | {data.get('loc', 0)} | {data.get('pct_of_total_loc', 0):.1f}% |")
        
    # Build quality section
    lines.extend([
        "",
        "## Code Quality",
        f"- **Health Score:** {quality.get('health_score', 0)} ({quality.get('health_grade', 'N/A')})",
        f"- **Avg Complexity:** {quality.get('avg_complexity', 0):.2f}",
        f"- **Max Complexity:** {quality.get('max_complexity', 0)} at {quality.get('max_complexity_location', 'N/A')}",
        f"- **TODO Count:** {quality.get('todo_count', 0)}",
    ])
    
    # Build hotspot table
    lines.extend([
        "",
        "## Top Files by Complexity",
        "| File | LOC | Avg Complexity |",
        "| :--- | :--- | :--- |"
    ])
    
    top_complexity = snapshot.get("top_files_by_complexity", [])
    for f in top_complexity[:10]:
        lines.append(f"| {f.get('path', 'N/A')} | {f.get('loc', 0)} | {f.get('complexity_avg', 0):.2f} |")
        
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        logger.info(f"Markdown report generated: {output_path}")
    except OSError as e:
        logger.error(f"Failed to write Markdown report: {e}")
        
    # EXIT: Render complete