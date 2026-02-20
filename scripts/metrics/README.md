<!-- AGENT: Detailed documentation for the Metrics Analyzer component. -->
# ⚓ MetricsAnalyzer: Documentation

`repo-metrics` is a standalone CLI tool that scans a source code repository and emits structured metrics covering codebase size, composition, entity counts, API surface, database schema, test coverage shape, and software quality indicators.

## 1. Features

- **Fast & Standalone:** Zero external dependencies for collection.
- **Language Aware:** Supports C#, TS/JS, Python, HTML, CSS, SQL, and more.
- **Trend Tracking:** Accumulates history in `metrics-history.json`.
- **Rich Reports:** Generates HTML, Markdown, and JSON outputs.
- **Git Integration:** Easy to use as a post-commit hook.

## 2. Installation

1. Clone this repository.
2. Ensure you have Python 3.11+ installed.
3. (Optional) Install dependencies for advanced features:
   ```bash
   pip install pyyaml jinja2
   ```

## 3. Usage

<!-- @entrypoint: manual-run -->
Run the analysis on any repository:
```bash
./scripts/metrics/repo-metrics.sh [REPO_PATH]
```

### Options

- `--format html,md,json`: Output formats (default: all).
- `--out-dir DIR`: Directory for output files (default: .metrics/).
- `--verbose`: Print progress to stderr.

### Git Hook Integration

To automatically run metrics on every commit:
```bash
./scripts/metrics/repo-metrics.sh install-hook [REPO_PATH]
```
*Note: For a unified setup with search indexing, use `scripts/install-hooks.sh` instead.*

## 4. Configuration

You can customize the tool by creating a `.repo-metrics.yaml` file in your repository root.

```yaml
# @config: output_dir
output_dir: .metrics/
include:
  - "**/*"
exclude:
  - "**/node_modules/**"
  - "**/bin/**"
```

## 5. Metrics Collected

- **Size:** Lines of code, blank lines, comments, file sizes.
- **Intelligence:** Classes, interfaces, methods, imports per language.
- **Quality:** Cyclomatic complexity, TODO/FIXME counts, health score.
- **Surface:** API endpoints, database tables, test-to-source ratio.
