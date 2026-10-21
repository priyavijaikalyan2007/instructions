<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 33ee9430-de4b-472b-945a-3cc3070d3bc6
Created: 2026
-->

<!-- AGENT: Plan and validation record for additive component directory defaults. -->

# Recommended component layouts

## Plan

Adopt src/<type>/<component-name>/ for new product components.
Use root test/ for tests that span components. Preserve each toolchain's internal test conventions.
Keep service-owned database artifacts under src/service/<service-name>/database/.
Keep ORM-required migration classes beside their owning backend project when tooling requires that location.
Reserve src/database/<database-name>/ for a deliberately independent database component with a recorded owner.
Do not introduce a global shared-database directory for ordinary service persistence.

Make REPO.md authoritative for the common convention and root directory responsibilities.
Add practical layouts to each target guide and align persistence, testing, and profile templates.
The interview should suggest conventional paths only when no concrete path exists.
Preserve configured paths, explicit answers, dry-run behavior, and planned-source confirmation.
Do not create application folders or move existing source.

No pattern required - simple functions suffice.
The interview owns suggestions. The existing configurator still validates, previews, and writes profile selections.
Public interface: source_path_default(values: dict, role: str) -> str.
The answer-document contract and enabled-target selection remain unchanged.

Files to modify: instructions/REPO.md, instructions/README.md, instructions/WORKFLOW.md,
instructions/PERSISTENCE.md, instructions/TESTING.md, instructions/PROJECT_PROFILE_TEMPLATE.md,
instructions/PROJECT_TEMPLATE.md, instructions/saas/SAAS.md, instructions/backend/BACKEND.md,
instructions/frontend/FRONTEND.md, instructions/apps/APPS.md, instructions/tools/TOOLS.md,
instructions/website/WEBSITES.md, instructions/sdk/SDKs.md, instructions/static-assets/STATIC_ASSETS.md,
instructions/google-workspace/GOOGLE_WORKSPACE.md, instructions/browser-extensions/BROWSER_EXTENSIONS.md,
scripts/profile_interview.py, scripts/tests/test_configure_instructions.py,
instructions/project/CONVERSATION.md, instructions/project/CHANGELOG.md, instructions/project/PROJECT.md,
agentknowledge/decisions.yaml, agentknowledge/history.jsonl,
instructions/templates/repository/PROJECT.md, instructions/templates/repository/inherited-files.json, and this record.

## Validation plan

Establish the existing 96-test baseline. Add failing public-CLI tests before changing interview behavior.
Cover accepted default paths for SaaS with native clients, independent products, and extensions.
Verify explicit path overrides, existing-profile preservation, cancellation, and absent-directory behavior.
Check Markdown files and anchors against the main-branch baseline.
Verify that only intended layout examples change and that CP1252 source encoding survives.
Run the full CLI suite, profile check, dry run, baseline check, and Git whitespace checks before a local commit.


## Results

All 101 tests pass. New tests failed before source-path suggestions were implemented.
The source profile check and dry run pass. Existing-profile preservation tests remain green.
No new Markdown link defects were found.
Layout examples changed intentionally in REPO, SaaS, backend, apps, and component-library guides.
Other previously recorded examples remain present. Existing frontend CP1252 content is preserved byte for byte.
The accepted layout is documented as generic guidance, with project paths and exceptions retained as project-owned facts.
No source migration, directory scaffolding, deployment, or publication was performed.
