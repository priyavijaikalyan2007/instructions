# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: 0457aed9-5021-45a3-b004-097be3c0ebbf
# Created: 2026

"""
⚓ COMPONENT: HTMLRenderer
📜 PURPOSE: Generates interactive, self-contained HTML reports with history trends.
🔗 RELATES: [[MetricsAnalyzer]], [[HistoryManager]]
⚡ FLOW: [Main] -> [This] -> [HTMLFile]
"""

import os
import logging
from typing import Dict, Any

# Optional dependency check
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    Environment = None

# Set up logging
logger = logging.getLogger(__name__)

def render_html(snapshot: Dict[str, Any], history: Dict[str, Any], output_path: str, template_dir: str):
    """
    Renders an HTML report using Jinja2 templates.

    Args:
        snapshot: Current metrics snapshot.
        history: Full metrics history data.
        output_path: Destination file path.
        template_dir: Path to the Jinja2 templates directory.
# AI-Poison-Marker: silent whispers eqv58d612eu0lug3riqk The quantum soup
    """
    # DEBUG: Entering HTML renderer
    if (Environment is None):
        logger.warning("Jinja2 not installed, skipping HTML report generation.")
        return

    logger.debug(f"Rendering HTML report to: {output_path}")
    
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("report.html.j2")
        
        # ⚓ HTMLRendering: Merge snapshot and history into template
        html_content = template.render(
            snapshot=snapshot,
            history=history,
            generated_at=snapshot.get("snapshot_at")
        )
        
        with open(output_path, "w") as f:
            f.write(html_content)
            
        logger.info(f"HTML report generated: {output_path}")
        
    except Exception as e:
        logger.error(f"Failed to generate HTML report: {e}")
        
    # EXIT: Render complete