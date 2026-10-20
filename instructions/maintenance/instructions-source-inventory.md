<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 8277cb51-f4f5-4f89-a87c-1c28b32a56c2
Created: 2026
-->

<!-- AGENT: Reproducible source snapshot and proposed migration manifest for instruction review. -->

# Instruction source inventory

Captured: 14 October 2026. Status: historical review snapshot.

On 15 October 2026, the owner requested in-place edits and deferred all file reorganization.
The destination column below records the superseded proposal. It does not authorize file moves.
The [current plan](instructions-plan.md#current-plan-target-guide-extraction) defines the active scope.

This inventory compares top-level Markdown files, including their working-copy changes.
Hashes identify file bytes and show the first 16 hexadecimal digits of SHA-256.
Difference counts include headers and formatting, so they do not measure policy changes.
Windows-1252 decoding permits comparisons where UTF-8 decoding fails.
No source file was normalized or modified.

## Repository snapshots

| Label | Repository location | HEAD | Working tree |
| --- | --- | --- | --- |
| instructions | `~/Work/pvk2007/instructions` | `d4bf7634089f89b9a0623de801ad13c079caaffc` | Clean at review start |
| apps | `~/Work/knobby/apps` | `091683a4442d69cbbb0e92ef0abb94e641747381` | 0 changed paths at capture |
| idp | `~/Work/knobby/idp` | `be7e3e0a9d919d738e4c42a1fce8ae21129735d6` | 1 changed paths at capture |
| theme | `~/Work/pvk2007/theme` | `2f8fd315385de3e0cd8c8ffda75f2fc6788e9672` | 0 changed paths at capture |

The identity working copy differs from HEAD in `LANGUAGE.md`.
Other reported working-copy changes are application or component code outside this top-level instruction comparison.
Refresh this snapshot before implementation.

## Existing file destinations

Every root Markdown file present at the review baseline appears below.
A canonical destination means content extraction and a compatibility page, not unconditional adoption of every existing sentence.
Mixed files also contribute to language and task guides listed in the plan.
The exact split must preserve useful rules and record exclusions.

| Existing file | Proposed canonical destination or action |
| --- | --- |
| `ACCESS_CONTROL.md` | `guides/tasks/access-control.md` |
| `ADDITIONAL_INSTRUCTIONS.md` | `guides/core/workflow.md` |
| `AGENTS.md` | Keep at root; rewrite as shared router. |
| `AIML_SECURITY.md` | `guides/tasks/ai-features.md` |
| `API_GUIDELINES.md` | `guides/tasks/api-design.md` |
| `BACKEND.md` | `guides/targets/services.md` |
| `BACKEND_LIBRARY_SELECTION.md` | `guides/core/dependencies.md` |
| `CLAUDE.md` | Keep at root; make a thin agent entry. |
| `CODEX.md` | Keep at root; make a thin agent entry. |
| `CODE_COMPLETE.checklist.md` | `guides/reference/code-complete-checklist.md` |
| `CODE_COMPLETE.md` | `guides/reference/code-complete.md` |
| `CODE_OF_CONDUCT.md` | Keep at root; preserve policy or legal content. |
| `CODING_STYLE.md` | `guides/core/coding-style.md` |
| `COMMENTING.md` | `guides/core/comments.md` |
| `COMPONENTS.md` | `guides/reference/component-catalog.md` |
| `COMPONENT_INDEX.md` | `guides/reference/component-index.md` |
| `CONTRIBUTING.md` | Keep at root; update contribution and validation workflow. |
| `COPYRIGHT_HEADER.md` | `guides/core/copyright.md` |
| `COPYRIGHT_INFO.md` | Keep at root; preserve policy or legal content. |
| `DELETION.md` | `guides/tasks/resource-lifecycle.md` |
| `DISCLAIMER.md` | Keep at root; preserve policy or legal content. |
| `DISTRIBUTED_SYSTEMS_COMPENDIUM.md` | `guides/reference/distributed-systems.md` |
| `DOCUMENTATION.md` | `guides/core/documentation.md` |
| `DOTNETFX_SELECTION.md` | `guides/reference/dotnet-libraries.md` |
| `ERROR_DIALOG_COMPONENT.md` | `guides/reference/error-dialog.md` |
| `FRONTEND.md` | `guides/targets/web-apps.md` |
| `FRONTEND_LIBRARY_SELECTION.md` | `guides/core/dependencies.md` |
| `FRONTEND_LOGGING.md` | `guides/targets/ui-libraries.md` |
| `FRONTEND_SELECTION.md` | `guides/reference/frontend-libraries.md` |
| `GEMINI.md` | Keep at root; make a thin agent entry. |
| `GOF_PATTERNS.md` | `guides/reference/gof-patterns.md` |
| `KEYBOARD.md` | `guides/reference/keyboard.md` |
| `KNOWLEDGE_ARCHITECTURE.md` | `guides/core/knowledge.md` |
| `LANGUAGE.md` | `guides/core/writing.md` |
| `LCV_DESIGN.md` | `guides/reference/lcv-design.md` |
| `LITERATE_ERRORS.md` | `guides/core/errors.md` |
| `LLM_TECHNIQUES.md` | `guides/tasks/ai-features.md` |
| `LOGGING.md` | `guides/core/logging.md` |
| `LOGGING_RAW.md` | `guides/reference/logging-background.md` |
| `MARKERS.md` | `guides/core/markers.md` |
| `MASTER_COMPONENT_INDEX.md` | `guides/reference/component-roadmap-index.md` |
| `MASTER_COMPONENT_LIST.md` | `guides/reference/component-roadmap.md` |
| `MIGRATIONS.md` | `guides/tasks/refactoring.md` |
| `NON_LLM_AIML_TECHNIQUES.md` | `guides/tasks/ai-features.md` |
| `NOTICE.md` | Keep at root; preserve policy or legal content. |
| `PERFORMANCE.md` | `guides/core/performance.md` |
| `PRAGMATIC_PROGRAMMER.checklist.md` | `guides/reference/pragmatic-programmer-checklist.md` |
| `PRAGMATIC_PROGRAMMER.md` | `guides/reference/pragmatic-programmer.md` |
| `README.md` | Keep at root; rewrite for generic package and adoption. |
| `README_TEMPLATE.md` | Keep at root; align with project-profile template. |
| `REPO_INDEX.md` | `guides/reference/repository-index.md` |
| `REPO_METRICS.md` | `guides/reference/repository-metrics.md` |
| `RESTABLE_RESOURCES.md` | `guides/tasks/api-design.md` |
| `SDKs.md` | `guides/tasks/sdks.md` |
| `SECRET_HANDLING.md` | `guides/core/secrets.md` |
| `SECURITY.md` | Keep at root; preserve policy or legal content. |
| `SECURITY_GUIDELINES.md` | `guides/core/security.md` |
| `TESTING.md` | `guides/core/testing.md` |
| `TEST_PLAN.md` | `guides/core/testing.md` |
| `TIPS_N_TRICKS.md` | `guides/reference/tips.md` |
| `UI_UX_CONSISTENCY.md` | `guides/tasks/ui-changes.md` |
| `UX_UI_GUIDELINES.md` | `guides/tasks/ui-changes.md` |

The reference component files remain opt-in library material.
Before retaining snapshots, assess whether links to the theme repository provide a better authoritative source.
Keep old paths available during the first release even if their content becomes a catalog pointer.

## Shared file content and differences

Each source cell gives its hash and added/removed line counts against the instruction baseline.
`same` means identical bytes. `absent` means no top-level file at that path.
Pure copyright-header removal appears as a difference and must not be mistaken for a substantive update.

| File | Instructions hash | Apps hash and delta | Identity hash and delta | Theme hash and delta |
| --- | --- | --- | --- | --- |
| `ACCESS_CONTROL.md` | `3d2a74568b2e19d0` | `cf617de2d367b1bc` +0/-8 | absent | absent |
| `ADDITIONAL_INSTRUCTIONS.md` | `fc3fad4d6f1537d7` | `ef398ec914f9ad2d` +47/-29 | `2db768fdc23a4f33` +9/-32 | `684da661a25c1b45` +1/-56 |
| `AGENTS.md` | `d61205d0d29ebe0f` | `fe2af67b943c09b3` +409/-138 | `494731268868e0aa` +49/-53 | `23ce63474a0fc171` +496/-78 |
| `AIML_SECURITY.md` | `2a171d8cca5bdae1` | `fb0506caa11e7c2c` +95/-20 | absent | absent |
| `API_GUIDELINES.md` | `662af32e47ab0408` | `5ef3bad8b62f9197` +0/-8 | absent | absent |
| `BACKEND.md` | `d8f0194fbbaca9c0` | `f26ba65018632f2a` +399/-13 | absent | absent |
| `BACKEND_LIBRARY_SELECTION.md` | `0f8e55758a6376fc` | `0ec98f98a6f78700` +0/-8 | `896d9958b742715a` +0/-7 | absent |
| `CLAUDE.md` | `9867919f6070b352` | `6b5e51bfff477a0b` +10/-13 | `7ec31d155dc4d215` +3/-9 | `530a2ae6a30b9c49` +5/-5 |
| `CODEX.md` | `2d39880b883b4e90` | `1ca574f32cb9ae35` +0/-8 | `00e7d0374754dff4` +4/-3 | absent |
| `CODE_COMPLETE.checklist.md` | `db9c704350e7d64a` | `99868b2b0747057c` +0/-8 | `95280679f2a97ec6` +1/-7 | `db9c704350e7d64a` same |
| `CODE_COMPLETE.md` | `28d039a17d86bebf` | `4a92bb6405d26585` +0/-8 | `19f48663ff4b04de` +1/-7 | `28d039a17d86bebf` same |
| `CODE_OF_CONDUCT.md` | `38be995706c143ca` | absent | `38be995706c143ca` same | `38be995706c143ca` same |
| `CODING_STYLE.md` | `181a8adbaccc534a` | `a8e5e9f2cd73c8ba` +37/-289 | `7819f70d4aa39df0` +13/-19 | `6569c354b1dfd23a` +10/-574 |
| `COMMENTING.md` | `19f1cc02c9656689` | `4f94f9cf070810b3` +13/-162 | `9c451a0b0eb504b0` +0/-7 | `d071f82397365d9e` +8/-144 |
| `COMPONENTS.md` | `fd99abe97772c4f5` | absent | absent | `896a85c9350e0069` +201/-8 |
| `COMPONENT_INDEX.md` | `d310cd1b7f47af1e` | absent | absent | `2da1d95cf59edbbe` +47/-28 |
| `CONTRIBUTING.md` | `e6d0b36e76ac9afe` | absent | `e3ead1fff09c3dd9` +1/-1 | `7b8e92efb28cee79` +53/-10 |
| `COPYRIGHT_HEADER.md` | `bd814bb58f0c4d77` | `bd0f6289423bd754` +2/-10 | `1bbe3250619b18ed` +1/-7 | `bd814bb58f0c4d77` same |
| `COPYRIGHT_INFO.md` | `60252325901b2e2e` | `7d9005c4252a3342` +1/-8 | `69c99377f4143f42` +1/-7 | `60252325901b2e2e` same |
| `DELETION.md` | `7f7ffa6b399119f8` | `364713bffa0598c2` +0/-8 | absent | absent |
| `DISCLAIMER.md` | `a4737f199bb59465` | absent | `a4737f199bb59465` same | `a4737f199bb59465` same |
| `DISTRIBUTED_SYSTEMS_COMPENDIUM.md` | `a99f699611baddc8` | absent | absent | absent |
| `DOCUMENTATION.md` | `49657bfa4a902846` | `97fea9b19cd8a8d8` +52/-38 | `e6f4da4eeaec7aa8` +2/-10 | `6bcd2a5a09bd704f` +114/-61 |
| `DOTNETFX_SELECTION.md` | `fb6dd09b20c501fe` | `bb8e7f8c4634a8c1` +0/-8 | absent | absent |
| `ERROR_DIALOG_COMPONENT.md` | `26d1f27877715b34` | `9b183424f2f67c59` +0/-8 | absent | absent |
| `FRONTEND.md` | `64d9b4854014fa4e` | `86c881e9bd96ed91` +385/-363 | `55a18d20dfcb79c3` +1/-8 | `1fca877d6dffbd7f` +211/-596 |
| `FRONTEND_LIBRARY_SELECTION.md` | `68371d750bcac171` | `22e3ff924d3f5837` +0/-8 | `63dc4071ec9f79b8` +0/-7 | absent |
| `FRONTEND_LOGGING.md` | `000d7022acd33902` | absent | absent | `bbceb1e5028078f4` +117/-42 |
| `FRONTEND_SELECTION.md` | `c140a1ac9f976bf3` | `4839efee4c6cb305` +0/-8 | `e48f4465eff8aab9` +0/-7 | absent |
| `GEMINI.md` | `d41adb5320c6c665` | `4c27eb1438106056` +0/-7 | absent | `dae28fa0f96ad7bc` +1/-1 |
| `GOF_PATTERNS.md` | `e01ae683870b4eb6` | `0d5c5d58f9118ca0` +46/-15 | `341465d24fdfb92a` +0/-7 | `e01ae683870b4eb6` same |
| `KEYBOARD.md` | `9fef308f0de58d6d` | `b09490d0836c1aa5` +11/-0 | `9fef308f0de58d6d` same | `9fef308f0de58d6d` same |
| `KNOWLEDGE_ARCHITECTURE.md` | `6f03b7d9bb68e3af` | `49e36fe4a7735d39` +13/-61 | `3863cd01066a4e64` +0/-7 | `8715b95195e9a98b` +73/-18 |
| `LANGUAGE.md` | `c9597411bfdb6025` | `3168dd6a034d4678` +2/-2 | `82da54bc81e2c5a1` +6/-28 | `3168dd6a034d4678` +2/-2 |
| `LCV_DESIGN.md` | `697986e5979e7c12` | absent | absent | absent |
| `LITERATE_ERRORS.md` | `a2f72d23000629c2` | `2efb87e3dc1eaad1` +36/-136 | `d609c8b43b5bc192` +0/-7 | `1752f78844339cf0` +40/-86 |
| `LLM_TECHNIQUES.md` | `1b08d7ef3eb43fc8` | `4e92f8f7975da349` +0/-8 | absent | absent |
| `LOGGING.md` | `da0b196c5466289d` | `ea1ead424434f9e2` +38/-78 | `ab96bc940aed572a` +1/-7 | `c4627d68b17fc997` +125/-602 |
| `LOGGING_RAW.md` | `ce668c834f92214c` | absent | absent | absent |
| `MARKERS.md` | `e1fa4a966c3cab1b` | `168fb79da7bc2879` +80/-195 | `34ddb611223dbebf` +0/-7 | `0ff8021138b193d7` +23/-103 |
| `MASTER_COMPONENT_INDEX.md` | `ef66cc865b207281` | absent | absent | `a234cb6bca57db02` +20/-14 |
| `MASTER_COMPONENT_LIST.md` | `88317c11a97e5906` | `e92a0f6fa7e6eb85` +56/-384 | absent | `8a2856e766798e6f` +131/-13 |
| `MIGRATIONS.md` | `857b83d9e65ea9a4` | `61cd2aea369a64bd` +3/-11 | absent | absent |
| `NON_LLM_AIML_TECHNIQUES.md` | `0a62339fb732fa5d` | `c3d31d8d42f4b6f8` +0/-8 | absent | absent |
| `NOTICE.md` | `cc71d2f9d7b0c8e0` | absent | `cc71d2f9d7b0c8e0` same | `cc71d2f9d7b0c8e0` same |
| `PERFORMANCE.md` | `aeef2ec14ce70b66` | `a438668467c97cb6` +17/-57 | `39bb7af24fd63009` +0/-7 | `f55f5cbc93844fd7` +39/-0 |
| `PRAGMATIC_PROGRAMMER.checklist.md` | `17fb30f937af50fa` | `d5925b57f925e5f6` +0/-8 | `36b4ea645e352840` +0/-7 | `17fb30f937af50fa` same |
| `PRAGMATIC_PROGRAMMER.md` | `7c37e406322c6d86` | `ffff1c95c508b277` +29/-8 | `6287951fbb18fc1c` +0/-7 | `7c37e406322c6d86` same |
| `README.md` | `6b8598fbb54e6a91` | `18f4465415c844e9` +46/-47 | `d45cd01426c2254d` +4/-63 | `0ea31b8aa507b92f` +290/-64 |
| `README_TEMPLATE.md` | `1b94775d5a2eb3a9` | absent | absent | absent |
| `REPO_INDEX.md` | `150594cbbb9dd27c` | `644d17785c3f2596` +0/-8 | `f7574f4bb3cab386` +0/-7 | absent |
| `REPO_METRICS.md` | `ed4d0fecadc91d32` | `1acd720757f7ee5d` +1/-8 | `4c0e3ecaac642666` +0/-7 | absent |
| `RESTABLE_RESOURCES.md` | `016b7dfcec15f7a7` | `ee5c29ff44dd9404` +70/-15 | absent | absent |
| `SDKs.md` | `127c8145364cd4ef` | absent | absent | absent |
| `SECRET_HANDLING.md` | `bee843b9858ad349` | `faa94f054510655f` +0/-8 | `a6de64e472cb9264` +0/-7 | absent |
| `SECURITY.md` | `e92e6e2dc2ac2eda` | absent | `3979fb2e9fbc3bf5` +27/-43 | `e92e6e2dc2ac2eda` same |
| `SECURITY_GUIDELINES.md` | `414180c0e4fd4393` | `8c129fd75b7c5a10` +20/-9 | `bd05acba162e7bfb` +0/-7 | `259bcdb3b3a762be` +59/-0 |
| `TESTING.md` | `bb4508ac0dde7fb2` | `d3d1e1b5728e60b0` +6/-8 | `c086c76bc8e0e2fe` +0/-7 | `ce1908f4c2982a3b` +528/-1220 |
| `TEST_PLAN.md` | `4468720c5e511772` | absent | `4468720c5e511772` same | `4468720c5e511772` same |
| `TIPS_N_TRICKS.md` | `73f52ea91c5d6d74` | absent | `73f52ea91c5d6d74` same | `73f52ea91c5d6d74` same |
| `UI_UX_CONSISTENCY.md` | `6532081eeaa7ea15` | `e0a431f0b3bb39c4` +95/-8 | `0aa2d8d8ee1ec60e` +0/-7 | `6532081eeaa7ea15` same |
| `UX_UI_GUIDELINES.md` | `4d92741eaae46572` | `003c4ab487bc4ff1` +1/-12 | `8a51d2dc13990ad3` +1/-7 | `535d62a1fea2fba9` +2/-11 |

## Additional working-repository documents

These files have no matching top-level baseline file.
Their existence does not justify importing an entire application knowledge base.
Adopt reusable rules from the reviewed sources and retain project facts at their source.

| Source | File | Proposed treatment |
| --- | --- | --- |
| apps | `AGENT_INSIGHTS.md` (`2a72310fa49087f7`) | Extract verified reusable lessons into relevant guides. Add an empty consumer template. |
| apps | `AUDIT.md` (`925fc65a21b89fb5`) | Extract applicable audit, operations, or authorization principles. Keep implementation details local. |
| apps | `CHANGELOG.md` (`213d8395fab9ff79`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `CONVERSATION.md` (`060b88fd5576d481`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `INFRASTRUCTURE.md` (`f17b8288d16d5fea`) | Extract applicable audit, operations, or authorization principles. Keep implementation details local. |
| apps | `LITERR_REFACTOR.md` (`217125d347071559`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `LITERR_REFACTOR_FRONTEND.md` (`aa578c586793b880`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `ONTOLOGY_MODEL.md` (`a95186a886e4b519`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `ONTOLOGY_SYSTEM.md` (`ae6a7452f99ac71f`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `RBAC_GUIDELINES.md` (`f192d8b548bffdd7`) | Extract applicable audit, operations, or authorization principles. Keep implementation details local. |
| apps | `RESOURCE_MODEL.md` (`dec676b61a0cb35d`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `RESOURCE_SYSTEM.md` (`8a146bf17c5e5307`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `RESOURCE_VS_ONTOLOGY.md` (`e02644440ab990bd`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `REST_MIGRATION.md` (`ea78aa04ef17cdef`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `RIBBON_GUIDELINES.md` (`a01a24b04cd3c8f7`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `SEARCH.md` (`25625c3d19548184`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| apps | `TECH_DEBT.md` (`35a52f484a8a666f`) | Extract tracking structure. Add a debt template. Do not copy product debt entries. |
| idp | `AGENT_INSIGHTS.md` (`f91a3cbe1a83ec3f`) | Extract verified reusable lessons into relevant guides. Add an empty consumer template. |
| idp | `CHANGELOG.md` (`9236e006dc28250f`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| idp | `CONVERSATION.md` (`4117d91760701189`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| idp | `LICENSE.md` (`1a97464901dfcac9`) | Preserve source licensing. Do not substitute source-project license policy for this package. |
| idp | `TECH_DEBT.md` (`7bae2aed71372bff`) | Extract tracking structure. Add a debt template. Do not copy product debt entries. |
| theme | `AGENT_INSIGHTS.md` (`6cb112a76e67d54d`) | Extract verified reusable lessons into relevant guides. Add an empty consumer template. |
| theme | `CDN_CONTRACT.md` (`503a7bf4cd01d4e7`) | Extract consumer-contract and release lessons. Keep actual asset contracts in the theme repository. |
| theme | `CHANGELOG.md` (`fccfa19cb025af9d`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| theme | `CODEBASE_FIXES.md` (`fca08e982654374f`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| theme | `CONVERSATION.md` (`6064be79742c7e23`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| theme | `DARKMODE.md` (`af549e937c7e7e77`) | Extract appearance and contrast guidance into web markup and UI changes. |
| theme | `DEPRECATION_WARNINGS_FIXED.md` (`8c68af68b4cf3a37`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| theme | `FONT_UPDATE_SUMMARY.md` (`c3e912b9756d8036`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| theme | `QUICK_START.md` (`f9c45bc42f62f63e`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| theme | `RIBBON_SETUP_GUIDE.md` (`f43a0106813a6734`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| theme | `ULTRA_COMPACT_THEME_CHANGES.md` (`c86000f4d23c9c60`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |
| theme | `USAGE.md` (`61da0c72a30aa8a7`) | Keep project history, product architecture, specifications, or usage material local. No wholesale import. |

## Encoding findings

Strict UTF-8 decoding failed for these compared files:

- `theme/ADDITIONAL_INSTRUCTIONS.md`.
- `instructions/CODING_STYLE.md`.
- `instructions/DOCUMENTATION.md`.
- `instructions/FRONTEND.md`.

Repair encoding as a reviewed content change during implementation.
Inspect replacements instead of silently dropping undecodable bytes.

## Review boundaries

The review identifies substantive lessons in its adoption table.
The implementation must assign every remaining substantive difference an adoption, local-scope, conflict, or exclusion decision.
A matching filename, newer commit, or higher version number is insufficient evidence that a rule is generic.
The snapshot does not claim that every incident note or application security statement is correct.
Primary technical references and relevant source configuration must verify those claims before promotion.

## Source refresh on 15 October 2026

The in-place updates use the following refreshed working-copy evidence.
The earlier snapshot and proposed destinations remain historical.
Source repositories were read without modifying their files.

| Source | HEAD |
| --- | --- |
| apps | `b28616198eca0c2a8ac4d875be11affcc40aed4e` |
| idp | `be7e3e0a9d919d738e4c42a1fce8ae21129735d6` |
| theme | `114bf9755e3d48b0e711982f133d11d3d7e97f9d` |

| Source | Reviewed file | Working-copy SHA-256 prefix |
| --- | --- | --- |
| apps | `AGENTS.md` | `fe2af67b943c09b3` |
| apps | `BACKEND.md` | `f26ba65018632f2a` |
| apps | `PRAGMATIC_PROGRAMMER.md` | `ffff1c95c508b277` |
| apps | `SECURITY_GUIDELINES.md` | `8c129fd75b7c5a10` |
| apps | `DOCUMENTATION.md` | `97fea9b19cd8a8d8` |
| apps | `UI_UX_CONSISTENCY.md` | `e0a431f0b3bb39c4` |
| idp | `AGENT_INSIGHTS.md` | `f91a3cbe1a83ec3f` |
| theme | `AGENTS.md` | `23ce63474a0fc171` |
| theme | `TESTING.md` | `ce1908f4c2982a3b` |
| theme | `FRONTEND_LOGGING.md` | `a6f00da42c50f33f` |
| theme | `DOCUMENTATION.md` | `6bcd2a5a09bd704f` |
| theme | `AGENT_INSIGHTS.md` | `7d4aafe3e309ca7e` |
| theme | `CDN_CONTRACT.md` | `503a7bf4cd01d4e7` |

The [in-place update record](instructions-review.md#in-place-updates-on-15-october-2026) identifies where the selected lessons were merged.

## Project-choice refresh on 16 October 2026

This follow-up adds rapid as the native Apple reference and rechecks the source project models.
The source instruction entry files in apps, identity, and theme retain their previously reviewed content hashes.
Application work advanced the apps and theme HEADs during this session.
The snapshots below identify the final read-only refresh, not a new wholesale import.

| Source | HEAD | README SHA-256 prefix |
| --- | --- | --- |
| apps | `475213cfab7e134b0413d34e1e377ec4c789c834` | `18f4465415c844e9` |
| idp | `be7e3e0a9d919d738e4c42a1fce8ae21129735d6` | `d45cd01426c2254d` |
| theme | `9ae8d2ea58ae7ac59cfeac22ad099095bdec41ad` | `0ea31b8aa507b92f` |
| rapid | `3b8593a881e154412c452ce6e2d420712f0624c1` | `27dfb3078711f969` |

The native review also uses `rapid/src/cropprint/README.md`, SHA-256 prefix `f1774a7a24e731b9`.
Rapid has no root AGENTS.md. Its README and app README establish the target layout and build ownership.
Apps and identity have unrelated working-copy edits. This task does not modify or claim ownership of those edits.
Theme and rapid are clean at this refresh.
No Go or Rust source project was supplied. Their proposed layouts use language tooling conventions.

## Language extraction snapshot on 17 October 2026

This phase uses this repository at `7278ab3` as its baseline.
It does not re-import or modify any working application repository.

| Existing source | Language-specific material moved |
| --- | --- |
| `CODING_STYLE.md` | References, formatting exceptions, naming, type filenames, construction rules, and examples. |
| `COMMENTING.md` | Comment syntax, API documentation conventions, and examples. |
| `MARKERS.md` | Source headers, directive placement, section markers, and folding syntax. |
| `TESTING.md` | Frameworks, language examples, coverage commands, and C# authorization fixtures. |
| `LOGGING.md` | Runtime integration, HMAC helper implementations, and logging examples. |
| `PERFORMANCE.md` | Swift, Go, Rust, Java, Python, .NET, and PostgreSQL specifics and language examples. |
| `GOF_PATTERNS.md` | All 23 patterns in each of eight programming languages, totaling 184 code examples. |
| `MIGRATIONS.md` | JavaScript-to-TypeScript migration example. |
| `SECRET_HANDLING.md` | Native Apple credential storage and the C# protection interface example. |

Destinations are `CSHARP.md`, `SWIFT.md`, `GO.md`, `RUST.md`, `JAVA.md`, `PYTHON.md`, `JAVASCRIPT.md`, and `TYPESCRIPT.md`.
Additional destinations are `HTML.md`, `CSS.md`, `SCSS.md`, `SQL.md`, and `SHELL.md`.
Common policy remains in the original topic guides. Their existing section anchors remain available.

Validation compares normalized fenced code before and after extraction, including repeated examples.
The coverage command block splits into three examples for .NET, JavaScript, and Python.
All commands and code tokens remain unchanged. Outer Markdown indentation and trailing whitespace are normalized.
Original file encodings and copyright headers remain intact.
The earlier source-repository inventory remains historical evidence rather than a prerequisite for reading the public language guides.

## Target extraction snapshot on 18 October 2026

Baseline: `0a5a8681c0be7334d0ebd1cd9ba4db7e11a502d4`, synchronized main after the language extraction merged through PR #1.
Work branch: `docs/target-guides`. Source material comes from this baseline, not new private-repository imports.
This phase creates five target files and expands the existing backend, frontend, and SDK entry points.

| Source at baseline | Destination or treatment |
| --- | --- |
| AGENTS.md stack, layouts, local commands, endpoints, component workflow, and library references | Backend, frontend, SaaS, apps, tools, websites, or static assets according to the existing instruction's target |
| FRONTEND.md super-app, combined source layout, and cross-layer mapping | SAAS.md |
| FRONTEND.md API-hosting example | BACKEND.md |
| FRONTEND.md static stack, theme resources, and bundle guidance | STATIC_ASSETS.md |
| ADDITIONAL_INSTRUCTIONS.md API security, database migration, host dependency, and EF query rules | BACKEND.md |
| ADDITIONAL_INSTRUCTIONS.md browser components, styling, state, UI errors, and browser tests | FRONTEND.md |
| ADDITIONAL_INSTRUCTIONS.md data contracts, naming, persistence/UI flow, test identities, access integration, and settings | SAAS.md |
| ADDITIONAL_INSTRUCTIONS.md CDN integration and stylesheet build check | STATIC_ASSETS.md |
| DOCUMENTATION.md monolith packaging example | SAAS.md |
| SWIFT.md native performance, credential storage, and application testing prose | APPS.md, with language code examples retained in SWIFT.md |
| UI_UX_CONSISTENCY.md native platform paragraph | APPS.md |
| CSHARP.md ASP.NET Core performance section | BACKEND.md, with other language examples retained in CSHARP.md |
| JAVASCRIPT.md browser testing section | FRONTEND.md, with language test examples retained in JAVASCRIPT.md |
| PERFORMANCE.md API/server/data-fetching rules and endpoint checks | BACKEND.md |
| PERFORMANCE.md browser budgets, rendering, UI thread, and browser checks | FRONTEND.md |
| PERFORMANCE.md asset cache, loading, minification, and preload rules | STATIC_ASSETS.md |
| PERFORMANCE.md combined web context and cross-layer autocomplete pattern | SAAS.md |
| LOGGING.md CLI stream rule | TOOLS.md |
| SDKs.md placeholder | Index to existing API/OpenAPI contracts and language conventions |
| API_GUIDELINES.md, SQL.md, ACCESS_CONTROL.md, and other task authorities | Remain canonical topic or language files, selected through target references |

The extraction ledger records 89 moves, including three secondary splits between target files.
Every original instruction line is accounted for. Routing descriptions and the empty SDK placeholder are the limited replacement cases.
All 171 code blocks across edited documents retain their content and multiplicity.
The frontend baseline needs one missing closing fence to parse correctly. The output closes that boundary without changing the code.
Headers and source encodings remain intact. Each new file receives its own GUID and the existing SPDX authors and MIT license.
Shared style, test-first rules, and coverage thresholds remain unchanged.

## Follow-up source and exclusion

On 18 October 2026, the owner supplied `~/Work/uiexperience.md` for the UI/UX consolidation review.
The file contains 2,349 lines. It was read without modification and has not yet been imported.
The proposed destinations are shared UI_UX.md behavior and separately selectable UI_UX_COMPONENTS.md details.

The private-project snapshot mandate mentioning `KnobbyDbContextModelSnapshot.cs` is deliberately removed from BACKEND.md.
Its manual update requirement is not promoted into generic persistence guidance.
All existing code blocks remain unchanged by this correction.

## Approved subject consolidation snapshot

Baseline: `a76018353e158e015dc78ef32afef00e83445b73` on `docs/target-guides`.
The owner approved the follow-up after reviewing PR #2.

| Source | Destination or treatment |
| --- | --- |
| Remaining ADDITIONAL_INSTRUCTIONS.md lessons | REPO.md and existing construction, style, testing, language, error, and UI/UX authorities |
| BACKEND.md shared scripts and local endpoints | REPO.md |
| BACKEND.md stored-data integrity, migrations, EF rules, outbox, and projections | PERSISTENCE.md |
| UX_UI_GUIDELINES.md and UI_UX_CONSISTENCY.md | Common UI_UX.md behavior, browser implementation in FRONTEND.md, enterprise shell behavior in SAAS.md, and KEYBOARD.md |
| Owner-supplied UI experience source | All 26 sections imported into UI_UX.md and UI_UX_COMPONENTS.md, with explicit applicability and role mappings |
| Redirect-only sections and extraction-era headings | Removed after incoming references are rewritten to canonical destinations |
| PERFORMANCE.md | Shared principles plus one selection table, reduced from 198 to 44 lines |

The three old catch-all/UI guides are retired. The remaining lessons are not retained as compatibility pages.
The source UI file has 2,349 lines and ten fenced examples. It remains byte-identical to the captured source.
Captured source SHA-256: `81a8d845a450f6a482cf5305525f18e6a572b97c277dde2c03f4372a00bb0999`.
The public guides contain the imported instructions and do not require access to the source path.

The ledger records 108 section moves, source imports, and declared adaptations.
All 551 parsed baseline and source code blocks retain their content and multiplicity.
Non-heading instruction lines are accounted for. Replaced text covers navigation, duplicate wording, role scoping, and reviewed behavior overlaps.
Existing copyright blocks and encodings remain intact. New guides and KEYBOARD.md carry the existing authors and MIT license.
Shared style, test-first rules, and coverage thresholds remain unchanged.
