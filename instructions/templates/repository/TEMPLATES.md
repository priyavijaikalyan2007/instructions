<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 2ae7dbb0-a792-40fa-be21-a96c26933e73
Created: 2026
-->

<!-- AGENT: Repository-document template ownership, license provenance, and source baseline maintenance. -->

# Repository document templates

These files generate project-owned documents during explicit project initialization.
They do not replace the instruction repository's own README, contribution policy, conduct policy, security policy, or LICENSE.
The existing instructions/README_TEMPLATE.md remains the general outline for writing a project overview manually.
The README template here adds concrete policy and configuration links for the initializer's output locations.
The initializer places README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, and SECURITY.md at the repository root.
Reserve .github/ for GitHub configuration. Keep one repository landing README rather than a competing .github/README.md.
README.md provides the public introduction and first-use instructions. PROJECT.md holds detailed project facts.
PROJECT_PROFILE.md records instruction selections, component scope, platforms, delivery choices, and agent roles.
Link to authoritative details instead of repeating them across these files.

Templates use Python string.Template placeholders. Project values do not execute as code.
Generated Markdown keeps template attribution and receives a new file GUID and repository identity.
Visible TODOs require project decisions, such as reporting contacts and support commitments.
Existing file-specific license notices remain applicable to generated policy scaffolding.
The selected project license governs new project material according to the scope stated in the generated root LICENSE.

## License choices

The interview supports these exact families:

- MIT and Apache-2.0.
- LGPL-2.1 and LGPL-3.0, each with an explicit only or or-later choice.
- GPL-2.0 and GPL-3.0, each with an explicit only or or-later choice.
- AGPL-3.0, with the same version choice.
- Elastic-2.0 and SSPL-1.0 as source-available options.
- Multiple software licenses joined by OR, allowing the recipient to choose one.
- CC-BY, CC-BY-SA, CC-BY-ND, CC-BY-NC, CC-BY-NC-SA, and CC-BY-NC-ND, all version 4.0.
- CC0-1.0 for separately selected content.
- Pending custom or undecided terms, recorded as a TODO without inventing a license grant.

Creative Commons selections require named content paths. They do not automatically apply to application source.
This follows the [Creative Commons guidance on software](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software).
This selector does not infer license compatibility from dependencies or replace existing third-party terms.

OR means a choice of terms, rather than a requirement to satisfy every listed license.
See [SPDX license expressions](https://spdx.github.io/spdx-spec/v2.3.1/SPDX-license-expressions/).
There is no Elasticsearch preset. Its source and distribution choices differ, as described in [Elastic's licensing FAQ](https://www.elastic.co/pricing/faq/licensing).
Custom commercial alternatives require supplied, reviewed terms. The initializer records those as pending.

## Bundled legal texts

The licenses directory contains exact texts from SPDX license-list-data release v3.29.0.
[sources.json](licenses/sources.json) records each pinned source URL and SHA-256 checksum.
The initializer verifies these checksums before use. It makes no network requests.
The local .gitattributes preserves legal-text line endings and upstream trailing whitespace, including the SSPL source text.
GNU only and or-later selections share the same version's legal text. The application notice records the selected version policy.
LGPL 3.0 also installs GPL 3.0 because LGPL 3.0 incorporates those terms.
MIT replaces only the designated year and copyright-holder placeholders.
Other legal texts, including their explanatory examples and original copyright notices, remain unchanged.
License texts keep their own copying permissions and are not relabeled with this repository's source-code headers.

The generated root LICENSE records project scope and the selected identifiers.
A single software license keeps its full terms in root LICENSE.
Multiple alternatives, separate content terms, and required companions use LICENSES/<identifier>.txt. THIRD_PARTY_NOTICES.md explains the copied library's separate attribution.
INSTRUCTION_LIBRARY_LICENSE.txt preserves the source library's MIT text for installation as instructions/LICENSE.

## Recognizing inherited files

inherited-files.json records known complete-file hashes for source-specific documents and records.
The initializer replaces or removes a file only when its entire content matches a registered version.
Customized files remain untouched. Conflicting license files stop initialization before writes.
Originals are backed up under .instructions/template-backup/ before replacements and removals.
The backup is historical material. It does not supply active project facts or agent instructions.

When source-specific documents or records change:

1. Review the changes as instruction-library content.
2. Run `python3 scripts/update_template_baseline.py --apply` in the source repository.
3. Review the manifest changes.
4. Run `python3 scripts/update_template_baseline.py` to check completeness.
5. Commit the manifest with the source changes.

The maintenance command preserves older registered hashes and rejects downstream repositories.
Never register a consuming project's edited content as an inherited source version.

Project facts and refinements default to root PROJECT.md and ADDITIONAL.md.
Optional business_context answers populate project facts and the generated README.
Missing operation placeholders and SETUP.md are project-owned. See instructions/PROJECT_SCAFFOLDING.md.
