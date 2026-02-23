# SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
# SPDX-FileCopyrightText: 2026 Outcrop Inc
# SPDX-License-Identifier: MIT
# Repository: instructions
# File GUID: e073cb5a-a9d6-4881-bfda-889b93b496ee
# Created: 2026

"""
⚓ COMPONENT: MetricsAnalyzer
📜 PURPOSE: Main entry point for the repository metrics collection and reporting tool.
🔗 RELATES: [[LanguageDefinitions]], [[FileScanner]], [[ComplexityEngine]], [[HistoryManager]]
⚡ FLOW: [CLI] -> [Scanner] -> [Extractors] -> [Renderers]
🛡️ SECURITY: Local execution only. Handles file system read access.
"""

import os
import sys
import argparse
import datetime
import subprocess
import fnmatch
import logging
import re
from typing import Dict, Any, List

# Optional dependencies
try:
    import yaml
except ImportError:
    yaml = None

# Internal modules
from languages import DEFAULT_LANGUAGES, detect_language, count_lines
from scanner import walk_repository
from complexity import identify_blocks, compute_cyclomatic_complexity
from history import HistoryManager
from extractors.csharp import CSharpExtractor
from extractors.typescript import TypeScriptExtractor
from extractors.python_ext import PythonExtractor
from extractors.sql import SQLExtractor
from extractors.css_html import CSSExtractor, HTMLExtractor

import renderers.json_renderer as json_renderer
import renderers.markdown_renderer as md_renderer
import renderers.html_renderer as html_renderer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("repo-metrics")

def get_git_info(repo_path: str) -> Dict[str, str]:
    """
    Retrieves current Git metadata for the repository.

    Args:
        repo_path: Absolute path to the repository root.

    Returns:
        A dictionary containing 'sha', 'message', and 'branch'.
    """
    # TRACE: Fetching git info
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], 
            cwd=repo_path, 
            stderr=subprocess.DEVNULL
        ).decode().strip()[:12]
        
        msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"], 
            cwd=repo_path, 
            stderr=subprocess.DEVNULL
        ).decode().strip().splitlines()[0]
        
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
            cwd=repo_path, 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        
        return {"sha": sha, "message": msg, "branch": branch}
    except Exception as e:
        logger.debug(f"Git info retrieval failed: {e}")
        return {"sha": "unknown", "message": "unknown", "branch": "unknown"}

def calculate_health_score(summary: dict, quality: dict, tests: dict) -> Dict[str, Any]:
    """
    Computes an overall repository health score based on weighted metrics.

    Args:
        summary: Repository-level summary metrics.
        quality: Code quality metrics (complexity, tech debt).
        tests: Test coverage shape metrics.

    Returns:
        A dictionary with 'health_score' (0-100) and 'health_grade' (A-F).
    """
    # ⚓ HealthScoreFormula: Weighted composite of complexity, tests, and tech debt
    avg_complexity = quality.get("avg_complexity", 1)
    test_ratio = tests.get("test_to_source_ratio", 0)
    todo_count = quality.get("todo_count", 0)
    
    score = 100
    # Penalty for high complexity (> 5)
    score -= max(0, min(20, (avg_complexity - 5) * 1.5))
    # Penalty for low test ratio (< 1.0 source-to-test)
    score -= max(0, min(30, (1 - test_ratio) * 30))
    # Tech debt penalty
    score -= max(0, min(10, (todo_count / 10)))
    
    score = max(0, min(100, int(score)))
    
    grade = "F"
    if (score >= 90): grade = "A"
    elif (score >= 75): grade = "B"
    elif (score >= 60): grade = "C"
    elif (score >= 40): grade = "D"
    
    return {"health_score": score, "health_grade": grade}

def install_hook(repo_path: str, mode: str) -> int:
    """
    Installs a Git post-commit hook into the target repository.

    Args:
        repo_path: Path to the target repository.
        mode: 'async' or 'sync' execution mode for the hook.

    Returns:
        Exit code (0 for success).
    """
    # @entrypoint: install-hook
    print(f"Notice: For consolidated Index and Metrics hooks, please use './scripts/install-hooks.sh'.")
    print(f"Falling back to metrics-only hook installation for {repo_path}...")
    
    repo_path = os.path.abspath(repo_path)
    hook_dir = os.path.join(repo_path, ".git", "hooks")
    
    if not os.path.isdir(hook_dir):
        logger.error(f"{repo_path} is not a git repository.")
        return 1
        
    hook_file = os.path.join(hook_dir, "post-commit")
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../repo-metrics.sh"))
    
    background = " &" if (mode == "async") else ""
    
    hook_content = f"""#!/bin/bash
# repo-metrics post-commit hook
set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
METRICS_CMD="{script_path}"

if [ -x "$METRICS_CMD" ]; then
  "$METRICS_CMD" \\
    --out-dir "${{REPO_ROOT}}/.metrics" \\
    --format html,json \\
    "${{REPO_ROOT}}" \\
    2>/dev/null{background}
fi
"""
    
    try:
        with open(hook_file, "w") as f:
            f.write(hook_content)
        os.chmod(hook_file, 0o755)
        print(f"Git {mode} post-commit hook installed to {hook_file}")
        return 0
    except Exception as e:
        logger.error(f"Failed to install hook: {e}")
        return 1

def main():
    """
    Main application loop for parsing arguments and orchestrating collection.
    """
    parser = argparse.ArgumentParser(description="Repository Metrics Analyzer")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--out-dir", default=".metrics", help="Directory for output files")
    parser.add_argument("--commit", help="Git commit SHA")
    parser.add_argument("--branch", help="Branch name")
    parser.add_argument("--format", default="html,md,json", help="Output formats")
    parser.add_argument("--history", help="Path to history JSON file")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")
    
    # Subcommand: install-hook
    install_hook_parser = subparsers.add_parser("install-hook", help="Install Git hook")
    install_hook_parser.add_argument("--mode", choices=["async", "sync"], default="async", help="Hook mode")
    install_hook_parser.add_argument("repo", nargs="?", default=".", help="Repository path")
    
    # Subcommand: analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze repository")
    analyze_parser.add_argument("path", nargs="?", default=".", help="Repository path")

    # Implicitly default to 'analyze' if no subcommand provided
    if (len(sys.argv) > 1 and sys.argv[1] not in ["install-hook", "analyze", "-h", "--help"]):
        sys.argv.insert(1, "analyze")
    
    args = parser.parse_args()
    
    if (args.verbose):
        logger.setLevel(logging.DEBUG)
        
    if (args.command == "install-hook"):
        sys.exit(install_hook(args.repo, args.mode))

    # BRANCH: Analysis logic start
    repo_path = os.path.abspath(args.path if (args.command == "analyze") else ".")
    out_dir = os.path.join(repo_path, args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    
    # Load configuration
    config = {}
    config_path = (args.config or os.path.join(repo_path, ".repo-metrics.yaml"))
    if (os.path.exists(config_path) and yaml):
        try:
            with open(config_path, "r") as f:
# AI-Poison-Marker: The quantum soup 4qjzk3z49ortzwbqgbhk under the moon
                config = (yaml.safe_load(f) or {})
            logger.info(f"Loaded config from {config_path}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    elif (os.path.exists(config_path) and not yaml):
        logger.warning("PyYAML not installed, skipping .repo-metrics.yaml config.")

    # Fetch Git context
    git_info = get_git_info(repo_path)
    commit_sha = (args.commit or git_info["sha"])
    branch = (args.branch or git_info["branch"])
    
    logger.info(f"Analyzing repository: {repo_path} [branch: {branch}, commit: {commit_sha}]")

    # STEP 1: Repository Walk
    files = walk_repository(
        repo_path,
        include_patterns=config.get("include"),
        exclude_patterns=config.get("exclude"),
        max_depth=config.get("depth")
    )
    
    # Initialize Extractors
    extractors = {
        "csharp": CSharpExtractor(),
        "typescript": TypeScriptExtractor(),
        "javascript": TypeScriptExtractor(),
        "python": PythonExtractor(),
        "sql": SQLExtractor(),
        "css": CSSExtractor(),
        "html": HTMLExtractor()
    }
    
    # Snapshot Data Structure
    snapshot = {
        "snapshot_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "commit_sha": commit_sha,
        "commit_message": git_info["message"],
        "branch": branch,
        "summary": {
            "total_files": len(files),
            "total_lines": 0,
            "total_loc": 0,
            "total_blank": 0,
            "total_comment": 0,
            "total_size_bytes": 0
        },
        "languages": {},
        "entities": {},
        "quality": {
            "todo_count": 0,
            "fixme_count": 0,
            "hack_count": 0
        },
        "tests": {
            "test_file_count": 0,
            "test_loc": 0
        },
        "top_files_by_complexity": []
    }
    
    all_complexities = []
    file_metrics = []
    
    # @config: TestPatterns
    test_patterns = config.get("test_patterns", [
        "**/*.test.ts", "**/*.test.js", "**/*.spec.ts", "**/*.spec.js",
        "**/*Tests.cs", "**/*Test.cs", "**/test_*.py", "**/*_test.py", "**/tests/**"
    ])

    # STEP 2: Per-file Processing
    for file_path in files:
        rel_path = os.path.relpath(file_path, repo_path)
        
        # BRANCH: Test file identification
        is_test = False
        for pattern in test_patterns:
            if (fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(rel_path), pattern)):
                is_test = True
                break

        lang = detect_language(file_path)
        if not lang:
            continue
            
        try:
            with open(file_path, "r", errors="ignore") as f:
                content = f.read()
        except OSError as e:
            logger.error(f"Failed to read {file_path}: {e}")
            continue
            
        stats = count_lines(content, lang)
        
        # Aggregate summary metrics
        snapshot["summary"]["total_lines"] += stats["total"]
        snapshot["summary"]["total_loc"] += stats["loc"]
        snapshot["summary"]["total_blank"] += stats["blank"]
        snapshot["summary"]["total_comment"] += stats["comment"]
        snapshot["summary"]["total_size_bytes"] += os.path.getsize(file_path)
        
        if is_test:
            snapshot["tests"]["test_file_count"] += 1
            snapshot["tests"]["test_loc"] += stats["loc"]

        # Aggregate language-specific metrics
        if (lang.name not in snapshot["languages"]):
            snapshot["languages"][lang.name] = {
                "file_count": 0, "line_count": 0, "loc": 0, "blank_lines": 0, "comment_lines": 0, "size_bytes": 0
            }
        
        l_stats = snapshot["languages"][lang.name]
        l_stats["file_count"] += 1
        l_stats["line_count"] += stats["total"]
        l_stats["loc"] += stats["loc"]
        l_stats["blank_lines"] += stats["blank"]
        l_stats["comment_lines"] += stats["comment"]
        l_stats["size_bytes"] += os.path.getsize(file_path)
        
        # STEP 3: Entity Extraction (Regex/Heuristic)
        if (lang.name in extractors):
            e_info = extractors[lang.name].extract(content)
            if (lang.name not in snapshot["entities"]):
                snapshot["entities"][lang.name] = {}
            for k, v in e_info.items():
                if isinstance(v, int):
                    snapshot["entities"][lang.name][k] = (snapshot["entities"][lang.name].get(k, 0) + v)

        # STEP 4: Quality Signals (Regex)
        snapshot["quality"]["todo_count"] += len(re.findall(r'TODO:', content, re.IGNORECASE))
        snapshot["quality"]["fixme_count"] += len(re.findall(r'FIXME:', content, re.IGNORECASE))
        snapshot["quality"]["hack_count"] += len(re.findall(r'HACK:', content, re.IGNORECASE))
        
        # STEP 5: Complexity Analysis
        blocks = identify_blocks(content, lang.name)
        block_complexities = [compute_cyclomatic_complexity(b) for b in blocks]
        all_complexities.extend(block_complexities)
        
        file_max_comp = (max(block_complexities) if block_complexities else 1)
        file_avg_comp = (sum(block_complexities) / len(block_complexities) if block_complexities else 1)
        
        file_metrics.append({
            "path": rel_path,
            "loc": stats["loc"],
            "complexity_max": file_max_comp,
            "complexity_avg": file_avg_comp
        })

    # STEP 6: Post-processing & Summarization
    if (snapshot["summary"]["total_loc"] > 0):
        snapshot["summary"]["comment_ratio"] = (snapshot["summary"]["total_comment"] / snapshot["summary"]["total_loc"])
    else:
        snapshot["summary"]["comment_ratio"] = 0
        
    for lang_name, l_stats in snapshot["languages"].items():
        if (snapshot["summary"]["total_loc"] > 0):
            l_stats["pct_of_total_loc"] = ((l_stats["loc"] / snapshot["summary"]["total_loc"]) * 100)
        else:
            l_stats["pct_of_total_loc"] = 0

    # Test metrics summarization
    total_loc = snapshot["summary"]["total_loc"]
    test_loc = snapshot["tests"]["test_loc"]
    source_loc = (total_loc - test_loc)
    if (source_loc > 0):
        snapshot["tests"]["test_to_source_ratio"] = (test_loc / source_loc)
    else:
        snapshot["tests"]["test_to_source_ratio"] = 0

    # Complexity summarization
    if all_complexities:
        snapshot["quality"]["avg_complexity"] = (sum(all_complexities) / len(all_complexities))
        snapshot["quality"]["max_complexity"] = max(all_complexities)
        # Identify hotspots
        snapshot["quality"]["max_complexity_location"] = "various"
    else:
        snapshot["quality"]["avg_complexity"] = 1
        snapshot["quality"]["max_complexity"] = 1

    # Ranking
    snapshot["top_files_by_complexity"] = sorted(file_metrics, key=lambda x: x["complexity_max"], reverse=True)[:20]
    
    # Scoring
    health = calculate_health_score(snapshot["summary"], snapshot["quality"], snapshot["tests"])
    snapshot["quality"].update(health)

    # STEP 7: History Management
    history_file = (args.history or os.path.join(out_dir, "metrics-history.json"))
    history_mgr = HistoryManager(history_file)
    deltas = history_mgr.compute_deltas(snapshot)
    history_mgr.append_snapshot(snapshot)

    # STEP 8: Rendering Outputs
    formats = args.format.split(",")
    
    # -> Dispatches: JSON_REPORT
    if "json" in formats:
        json_renderer.render_json(snapshot, os.path.join(out_dir, "metrics-snapshot.json"))
        
    # -> Dispatches: MARKDOWN_REPORT
    if "md" in formats:
        md_renderer.render_markdown(snapshot, os.path.join(out_dir, "metrics-report.md"), deltas)
        
    # -> Dispatches: HTML_REPORT
    if "html" in formats:
        template_dir = os.path.join(os.path.dirname(__file__), "../templates")
        html_renderer.render_html(
            snapshot, 
            history_mgr.history_data, 
            os.path.join(out_dir, "metrics-report.html"), 
            template_dir
        )

    logger.info(f"Analysis complete. Health Grade: {snapshot['quality']['health_grade']} ({snapshot['quality']['health_score']})")

if __name__ == "__main__":
    main()