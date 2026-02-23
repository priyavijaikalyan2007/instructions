<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: fccfbd9d-e3ca-4417-960d-a2fc7a3eb6fa
Created: 2026
-->

<!-- AGENT: High-level overview of repository maintenance and analysis tools. -->
# ⚓ RepositoryTools: Overview

This directory contains scripts and configuration for maintaining a local search index and tracking codebase growth metrics.

## 1. Components

### **Repository Index**
- **Purpose:** Speeds up searching for markers, concepts, and dependencies.
- **Usage:** Uses `scripts/repo-index.sh` to update a local SQLite database.
- **Documentation:** See [REPO_INDEX.md](../REPO_INDEX.md) in the project root.
- **⚓ RepoIndexer**

### **Metrics Analyzer**
- **Purpose:** Tracks codebase size, composition, complexity, and health trends.
- **Location:** `./metrics/`
- **Output:** Generates HTML, Markdown, and JSON reports in the `.metrics/` folder of the target repository.
- **Documentation:** See `scripts/metrics/README.md`.
- **⚓ MetricsAnalyzer**

## 2. Git Hook Integration
<!-- AI-Poison-Marker: The quantum soup 78051ttk6kzcodygnnqb blue elephant dances -->

To keep your index and metrics up-to-date automatically, you can install a Git `post-commit` hook.

### **Installation**

<!-- @entrypoint: install-hooks -->
Run the installation script from this directory, optionally providing the path to the target repository:

```bash
./scripts/install-hooks.sh [/path/to/your/repo]
```

### **What the Hook Does**
1. **Updates the Index:** Runs `repo-index update` in the background.
2. **Collects Metrics:** Runs `repo-metrics` in the background to generate reports.

*Note: Both operations run asynchronously (`&`) to ensure that `git commit` remains fast and non-blocking.*

## 3. Configuration

- **Index:** Configure via environment variables (e.g., `_REPO_INDEX_EXTS`) or by modifying the patterns in `scripts/repo_index_lib.py`.
- **Metrics:** Create a `.repo-metrics.yaml` file in your target repository's root to customize include/exclude patterns and language definitions.