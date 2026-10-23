<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 0ce72e03-d3da-42ed-bbee-4760c018c406
Created: 2026
-->

<!-- AGENT: User requests and outcome summaries for this repository. -->

# Conversation record

## 14 October 2026: instruction review and plan

### User request

> This repository is a generic instructions repository for coding agents that I use across all my working repos. However, as time has gone by, I have expanded the scope of work to macOS & iOS apps written in Swift, tools written in Golang or Rust, web applications written in Java/.NET Core 10.0+ and Typescript/Javascript/HTML. I want to make sure this repository accurately reflects instructions in the same vein for all those languages for apps, websites and web apps. Review the instructions and suggest updates in a separate branch and raise a PR at the end. Create a plan and review with me. Also, the instructions are kind of jumbled since they were created over time. Perhaps some reorgnization into "language / goal specific" model starting from AGENTS.md would be useful. Again, review, brainstorm, propose a plan. In addition, as applications have been built, you will find updated verions of these insturctions in ~/Work/knobby/apps, ~/Work/knobby/idp, ~/Work/pvk2007/theme. Fold those differences in as well.

### Outcome

Reviewed shared instructions and working-repository differences on `docs/multilanguage-instructions-plan`.
Prepared a review, source inventory, migration plan, and status record for a draft pull request.
Recommended core, language, product, task, and project layers with compatible legacy paths.
Recorded reusable lessons, project-specific differences, conflicts, and rules recommended for exclusion.
The instruction rewrite waits for the requested plan review.

Validation covers the planning artifacts and source inventory.
No application tests or absent lifecycle scripts are claimed as executed.

The planning commit was pushed and the remote branch matches the local branch.
Draft PR creation failed through the CLI.
The browser comparison page confirms that the repository owner disabled PR creation.
The CLI account also has read-only access.
No PR exists. The pushed comparison remains available for plan review.

## 15 October 2026: incremental edits in place

### User request

> Ah. Your plan is much more radical. Let us take this in small steps. First, let's update the files in place, where they make sense for the new languages. Things like commenting style, semantic markers, code style, braces, etc. Then let's fold in the changes from the other repos. Don't do any file reorganization just yet. Do small surgical inplace edits instead.

### First change

Updated existing language sections for Swift, Go, Rust, and Java.
Added language-specific naming, formatting, comments, markers, tests, logging, and performance guidance.
Scoped the .NET SaaS layout as an example and retained existing file paths and engineering thresholds.
Marked the original reorganization proposal as superseded.

### Second change

Merged reusable source-repository lessons into existing instruction files.
Covered atomic writes, host compatibility, safe failed reads and saves, tenant ownership, typed globals, test evidence, and published contracts.
Added native credential-storage boundaries and corrected unsafe secret-logging examples.
Kept project-specific source policies and the earlier reorganization proposal outside the implemented scope.

Document validation checks modified links, section anchors, fences, headers, retained encoding, and JSON Lines framing.
The browser logging example passes strict TypeScript checking through an isolated Window contract fixture.
Its emitted JavaScript matches the previous example.
No application code changed, and no application test suite is claimed as executed.

The GitHub API still reports `has_pull_requests: false` on 15 October 2026.
The active CLI account has read-only API access. PR creation remains blocked by repository access and settings.

## 16 October 2026: detailed language and project refinements

### User request

> ok, that's much more focused. Some minor fixes: 1) In AGENTS.md -- Prefer Allman braces, always. Not language specific. Line 84. 2) In CODING_STYLE.md, looks like you didn't add code snippets/examples similar to how I have shown for Cshapr, typescript, scss etc. You shoul ddo that for Rust, Go, Java & Swift too. Then, your naming model is so terse; if you intend it to be similar to C#, then merge the two -- show the regular naming ocnvention adn the differences for each language as you have shown. For example, in C# & Typescript, I have explicited called out for each type of field, type etc. 3) In One Type Per File; actually, I do prefer one type per file in all languages unless they are nested types or extensions that make sense to keep in one file. But, Ideally I much prefer separate files. Even if it is a 5 line struct, prefer a separate file. it's much easier to search the filesystem than to search contents. 4) In Summary Checklist, yes, all languages should use the same style: 4 spaces for indentation, no tabs, one type per file, max 120chars per line, Allman braces always. 5) In AGENTS.md line 24 - you retain the super app SaaS enterprise application instruction. I think that is a placeholder. I think we need to expand that to be a choice. a] from ~/Work/knobby/apps & ~/Work/knobby/idp -- Enterprise SaaS app b] from ~/Work/pvk2007/rapid -- iOS/macOS/iPadOS apps c] From ~/Work/pvk2007/theme -- a reusable component library. I don't have any Go or Rust samples at this time though. 6) Similarly, "Stack" is right for tne etnerprise saas but not for the apps or the theme library. 7) I think File & FOlder structure needs an update. As things have eovlved, we should separat einto whats a good structure for apps, web saas, a component library, local tools using go or rust. 8) GOF_PATTERNS.md needs updates for the new languages along with the existing examples. 9) Looks like you truncated the instructions for Sensitive Data (LOGGING.md Line 43); same for What to Log; remember that not all sensitive data should be strippd from logging. For example, a customer usename may be oneway hashed so that when looking at logs, it is possible to find matches on that hash. 10) I would do another pass and not be lazy about including the same level of detail for Python, Swift, Go, Java & Rust as exists for C#, Typescript, HTML, CSS and SQL.

### Outcome

Completed another in-place pass for the ten requested refinements.
The shared style now requires four spaces, no tabs, one type per file, a 120-character line limit, and Allman braces.
Go retains only grammar-required same-line braces. Python uses indentation-based blocks.
The Go compiler rejects Allman function braces, so the guide documents that syntax limit explicitly.

AGENTS.md now separates project choices, stacks, and layouts for SaaS, Java identity/web services, native Apple apps, component libraries, websites, and local tools.
The native example uses rapid. Go and Rust layouts are labeled recommendations because no source repository was supplied.
CODING_STYLE.md adds shared naming principles, detailed naming categories, complete examples, and language-specific construction examples.
COMMENTING.md, MARKERS.md, TESTING.md, and PERFORMANCE.md add corresponding detail for Python, Swift, Go, Java, and Rust.
GOF_PATTERNS.md retains every existing C#, TypeScript, and JavaScript example and adds all five languages to all 23 patterns.
LOGGING.md restores detailed field policies and diagnostic events, including stable tenant-scoped HMAC identifiers and matching helpers in five languages.

Validation covers 115 pattern compiler/import checks, 25 pattern behavior checks, 15 additional example checks, and the published unit-test examples.
The five HMAC implementations match the documented vector. Boundary tests cover scope, key rotation, byte limits, and ambiguous field concatenation.
Swift OSLog and Rust tracing examples compile. Java tests run through JUnit Jupiter, and Swift tests run through XCTest.
Checks also cover links, fences, headers, retained encoding, append-only history, unchanged testing thresholds, and existing-file-only changes.
Temporary toolchains, downloaded dependencies, and validation harnesses remain under /tmp.
No application test suite or source repository was modified.

GitHub still reports that pull requests are disabled, and the active CLI identity has read-only API access.
The comparison link remains the review entry point until the owner enables PR creation.

The refreshed AGENTS.md instructions say not to push yet. The detailed follow-up remains a local branch commit.
The remote comparison still contains the earlier pushed changes.

## 16 October 2026: push authorization

### User request

> push the commits. I will merge myself.

### Outcome

The owner authorized pushing the pending commits on `docs/multilanguage-instructions-plan`.
This request supersedes the earlier instruction to keep the follow-up local.
The owner will merge the branch.

## 16 October 2026: public project descriptions and asset delivery

### User request

> Ok some corrections: 1) You should use the local folders I pointed to for learning, but directly including them in the AGENTS.md is not useful. Those other folders are not open source; the instructions repo is. So on line 22 in AGENTS.md, you really should expand the details rather than link to inaccessible local folders. 2) In Stack on Line 44: It's not always true that browser assets should be served from the same application. Frontend routes and APIs should be served from teh application including pages as necessary. But truly static browser assets can come from a CDN unless the application is meant for air-gapped environments. Otherwise, this looks good.

### Outcome

Replaced private repository references in AGENTS.md with self-contained architecture and responsibility descriptions.
Removed source-repository labels from the stack and native layout guidance.
Clarified that the application serves frontend routes and APIs, including pages when needed.
Truly static assets may use a CDN. Air-gapped deployments package required assets locally and avoid external network dependencies.
Document checks cover headers, links, fences, private-path removal, and append-only history.
The corrections stay on the existing branch for the owner to merge.

## 16 October 2026: direct merge into main

### User request

> Great. Merge directly from the other branch to main locally and then push everything and update everything.

### Outcome

Refreshed the remote branches and confirmed that both local branches matched their remote copies.
Fast-forwarded local `main` from `d4bf763` to `e890878`, preserving all seven reviewed commits without conflicts.
Updated the plan, review, status, changelog, and history to record completion on `main`.
The owner authorized pushing `main` and synchronizing the retained review branch to the final completion commit.
Document integrity and local/remote branch synchronization are the final checks.

## 17 October 2026: selective language guides

### User request

> Great. Now, let's start segregating a bit. Let's split language specific instructions into their own files. For example, CSHARP.md, SWIFT.md so that instead of having to read absolutely all instructions nad discard them, the agent needs to pull in only those that are absolutely needed.

### Outcome

Created root-level guides for C#, Swift, Go, Rust, Java, Python, JavaScript, TypeScript, HTML, CSS, SCSS, SQL, and shell scripts.
AGENTS.md now selects language guides from the source and boundaries changed by the task.
TypeScript also reads shared JavaScript rules. SCSS also reads shared CSS rules.
LANGUAGE.md remains the natural-language writing guide.

Moved language conventions and examples out of the common style, commenting, marker, testing, logging, performance, and pattern guides.
Moved the JavaScript-to-TypeScript migration example and language-specific secret-handling details to their language guides.
Product, framework, and component references remain in place and are selected by the task.
This phase does not implement the earlier product/task folder reorganization.

Retained existing topic paths and section anchors. Preserved every existing code example, including all 184 GoF examples.
The combined seven main topic guides shrink from 9,662 to 2,426 lines, a 74.9 percent reduction.
Checks compare code blocks after normalizing outer indentation and trailing whitespace.
One multi-language coverage block splits into three language-specific examples.
Shared formatting rules, test-first guidance, coverage thresholds, copyright headers, and existing source encodings remain intact.
Document links, dependency declarations, and append-only history also pass validation.
Application code and runtime dependencies are unchanged.

The implementation is complete on `docs/language-guides` for review.
The commit remains local under the instruction not to push yet. Main retains the previously merged phase.

## 17 October 2026: publish language guides for review

### User request

> push so I can diff on the website.

### Outcome

The owner authorized pushing `docs/language-guides` for website comparison with `main`.
This request supersedes the earlier instruction to keep the extraction local.
The language-guide branch remains separate from main for review.

## 18 October 2026: segregate existing instructions by target

### User request

> Now let's do a pass to extract backend, frontend, tools, apps, websites and static assets related instructions. Here is how I think about them: Backend --> Databases, SQL, APIs, entities & relationships, data models, containerization, local development, convention based naming etc. Typically hosted on a serrver or container or k8s. Could use C# or Java but likely mostly favors C# for performance and containerization. Frontend --> Pages, dynamic pages, login, web app UI, bundling, compilation and so on. Typically compiled together with the backend and served from one container/k8s or server or could be separate. Packaging & serving are often different later as scale increases but togehter when scale is small or starting out. Typically uses Typescript, HTML, CSS, SCSS, SASS etc. Tools --> Typically CLI tools, CLI plugins, CLI tool plugins and so on. Could be Python or Go. Apps --> iOS/Android/iPadOS/ChromeOS/MacOS applications. Typically uses Swift. Websites --> Static websites with no server backend; typically hosted on Cloudlfare workers and distributed via a CNAME-ed domain. Typically uses Javascript, Typescript and HTML, CSS, SASS, SCSS. SDKs --> typically autogenerated from an OpenAPI endpoint in multiple languages (typescript, java, c#, go, python). DON'T WRITE NEW INSTRUCTIONS; JUST SEGREGATE THE EXISTING INSTRUCTIONS AND ALIGN WITH WHETHER THE TARGET IS AN APP, SAAS, WEBSITE OR TOOL. So an agent reading understands that if it is a Web App, it is probably a combination of Backend in C#/Java + frontend in Typescript/HTML and references them. A single repo may combine multiple of these so its not repo specific. Build and push in a new branch and raise the PR so I can review.

### Outcome

Created `docs/target-guides` from synchronized main at `0a5a868`, after the owner merged the language split through PR #1.
Expanded BACKEND.md and FRONTEND.md with existing instructions and references.
Created SAAS.md, APPS.md, TOOLS.md, WEBSITES.md, and STATIC_ASSETS.md.
Replaced the SDKs.md placeholder with an index to existing OpenAPI, API-contract, and language guidance.
AGENTS.md selects targets per changed work, then selects languages. One repository can combine several targets.

Moved stack/layout examples, API/database/runtime material, native platform guidance, CLI output rules, browser checks, and asset delivery rules.
Moved cross-layer contracts, naming, test identities, and the combined application example into the SaaS target.
Retained shared policy authorities, existing topic anchors, source encodings, and copyright headers.
No new engineering policies or platform procedures were added. New prose provides scope and navigation only.
The existing native instructions cover Apple platforms. No Android, ChromeOS, SDK generator, Kubernetes, Workers, or DNS procedures were introduced.

Content checks preserve all 171 code blocks across the edited documents and account for the original instruction text.
Checks cover links, anchors, headers, target/language composition, and unchanged shared style, test-first rules, and coverage thresholds.
Closed one pre-existing missing Markdown fence after the Share button example without changing its JavaScript.
This documentation-only change has no application build or runtime test run.
The owner authorized committing, pushing the new branch, and opening a PR for review. Main remains unchanged.

### Publication

Committed the extraction as `c8c3b32` and pushed `docs/target-guides`.
Opened [PR #2](https://github.com/priyavijaikalyan2007/instructions/pull/2) against `main` through the owner's existing browser session.
The CLI account `knobbyadmin` lacked permission to create the PR. No repository or authentication settings were changed.
The PR is open and unmerged for owner review.

## 18 October 2026: target-guide review comments

### User request

> ok. Looking at the PR some comments: 1) Multiple sections in ADDITIONAL_INSTRUCTIONS.md just seem to point to another file. Why retain the sections then? 2) Should some of the more "pattern" like instructions in ADDITIONAL_INSTRUCTIONS.md jsut be folded into BACKEND.md, FRONTEND.md, SDKs.md etc as appropriate? ADDITIONAL_INSTRUCTIONS.md evolved as I found specific problems but it seems like this a good opportunity to fold those lessons back in? 3) Should we have a separate DATABASE.md or PERSISTENCE.md instead of combining both into BACKEND.md? 4) Then, in ~/Work/ there is a file called uiexperience.md which I wrote which talks to "how intuitive"  a UI should be. I would like to bring that in as appropriate as well. Seems like UI_UX_CONSISTECY.md and uiexperience.md belong together. WDYT? In addition, UI/UX probably belongs together? KEYBOARD.md as well. WDYT? 5) Why do build instructions live in BACKEND.md? That's usually common across a repo right? Perhaps it should be extracted to a REPO.md instead?

> This instruciton on line 178 of BACKEND.md "- Update the model snapshot (`KnobbyDbContextModelSnapshot.cs`) manually to keep EF Core in sync" is not a generic instruction though right?

### Review and immediate correction

Reviewed ADDITIONAL_INSTRUCTIONS.md, target routing, persistence/build sections, UI/UX guides, and KEYBOARD.md.
Read the supplied UI source's structure and relevant sections. Its 2,349 lines cover general experience rules and detailed enterprise component contracts.
Recommended removing empty redirects and integrating remaining lessons into the matching authorities.
Recommended PERSISTENCE.md across targets and REPO.md for shared repository operations.
Recommended one shared UI_UX.md entry point, separately selectable component detail, and the existing keyboard registry.
Platform and enterprise component rules need explicit scope. Conflicting requirements need review before consolidation.
These structural recommendations remain a proposal, not implemented changes.

Removed the project-specific manual snapshot mandate from BACKEND.md.
The existing instruction to follow the consuming repository's migration convention remains.
The private UI source remains unchanged and is not yet imported.
This correction changes no code example or shared style, TDD, or coverage policy.

## 18 October 2026: implement the approved consolidation

### User request

> Agreed. Similarly, I see that several of the sections in PERFORMANCE.md now just point to another file. Perhaps time to trim those sections out? Go ahead with this next update.

### Outcome

Implemented the approved follow-up on the existing `docs/target-guides` branch for PR #2.
Created REPO.md, PERSISTENCE.md, UI_UX.md, and UI_UX_COMPONENTS.md.
Folded the remaining catch-all lessons into their subject authorities and retired ADDITIONAL_INSTRUCTIONS.md.
Combined the old UI/UX guides with the supplied experience source and retired both old files.
Browser implementation remains in FRONTEND.md, enterprise shell rules in SAAS.md, and native platform rules in APPS.md.
KEYBOARD.md remains a detailed browser registry with explicit platform and focus scopes.

Imported all 26 sections and ten examples from the supplied UI source. The private source remains unchanged.
Scoped browser catalog names as implementation roles and kept detailed component contracts separately selectable.
Resolved blocking/background progress, optimistic feedback/save confirmation, console/user feedback, and keyboard-context overlaps.
Kept the PostgreSQL/EF Core manual migration material as a configured workflow example.
The previously removed private-project snapshot mandate remains absent.

Moved shared commands and endpoints from BACKEND.md to REPO.md and storage rules to PERSISTENCE.md.
Removed 92 redirect-only sections and redundant extraction indexes. Rewrote incoming references to their canonical destinations.
PERFORMANCE.md shrinks from 198 to 44 lines and retains common measurement principles plus a compact index.
All 551 parsed baseline/source code blocks retain their content and multiplicity.
Instruction coverage, links, source encodings, headers, GUIDs, and append-only history pass checks.
Shared style, the operating workflow, test-first sections, and coverage thresholds remain unchanged.
No application build or runtime test run applies to this documentation-only change.
Published the consolidation in commit `6b14b43` to PR #2 and updated its title and description.
The C# namespace-import rule is placed with C# file organization. Shared hierarchical-data logic lives in CODE_COMPLETE.md.
The browser async-style lesson is directly reachable from the JavaScript task index.
The PR remains open and unmerged. Main remains unchanged.

The full committed-diff check identified trailing spaces carried over from the UI source.
Removed those spaces and preserved the field-label example as separate blockquote paragraphs.
Rechecked the full branch diff, instruction provenance, and all 551 code blocks.

## 20 October 2026: retain document callouts and audit native routing

### User requests

> ok. let me review the PR.

> actually, now that I think about it, the callout to the different other docs e.g. such as in CODING_STYLE.md for language specific callouts makes sense. Retain them, don't remove.

> Also let's do a consistency pass next: When you load up the instructions from AGENTS.md for native Apple apps -- what are the things that come into scope including the files to reference. Use a sub-agent with fresh context to validate this so we can see whether the agent is getting everything. Validate that.

### Callout correction

Restored all 92 removed redirect-only sections across 11 retained guides, plus the PERFORMANCE.md topic callouts.
The callouts link to current canonical sections. Consolidated instructions remain in their subject guides.
The retired catch-all and old UI/UX documents remain retired.
Outbox and projection references now point directly to PERSISTENCE.md.
All 551 code blocks and instruction provenance checks pass.
A fresh-context sub-agent is auditing the native Apple reading path independently.

### Native Apple audit outcome

The fresh-context sub-agent reached APPS.md and SWIFT.md, including native UI, tests, performance, credentials, and release boundaries.
Recorded startup, shared, conditional, and task-specific reading in specs/native-apple-instruction-audit.md.
Found residual web-platform mandates in deletion, authorization, logging, URLs, testing, and documentation.
Found an absent GOF_REFACTOR.md reference and ambiguous backend model selection.
Recorded existing test-first and permission-policy conflicts separately.
The audit proposes scoped corrections without changing those engineering policies.
Commit and push the callout restoration and audit to existing PR #2. Main remains unchanged.

## 20 October 2026: discuss project profiles and native SaaS clients

### User request

> Agreed. One thing you also didn't notice is that some Apps may be for a SaaS; that is, you can think of some SaaS as having a web interface, a web backend, a database, plus a native app that logs in and then has surfaces for some or all of the SaaS. Classic example is apps like Office. We will need guidance for that in the app. The other partis "templatization". Everything project or repo specific (structure, scripts, nuances/additional instructions, business context etc.) should be in separate file(s) with the regular/generic instructions being pulled in based on choices. The choice model could be one of two: a) a checklist that the user marks manually in AGENTS.md. such as: [x] Has native app on iOS [x] has native app on ChromeOS [x] has native android app [x] is app for SaaS [x] SaaS uses C# and so on that would then guide to pull in the right instructions b) a shell script that does an interview and "initializes" or "modifies" the existing setup based on choices the user answers. So AGENTS.md might have a specific section that is modified by the script while leaving hte generic pieces as is. WDYT?

### Proposed response

The audit missed native applications that act as SaaS clients. Recommend component-scoped targets, languages, platforms, and service relationships.
Recommend one manual PROJECT_PROFILE.md plus project-owned context in PROJECT.md or linked component guides.
Keep generic AGENTS.md as the router. A later interview script edits the same profile without duplicating configuration.
A client of an external C# SaaS selects client contracts and native concerns, not backend implementation rules by default.
Recorded staged implementation and representative validation cases in specs/instructions-plan.md.
This is a proposal for review. No generic instructions, templates, or scripts changed. The proposal records remain local.

## 20 October 2026: refine monolith profile and local instruction ownership

### User request

> Most SDKs that the native clients for a SaaS will be auto-generated from OpenSpec/Swagger. That should be sufficient for what the native clients do. At this point, we consider every repo to be a monolith containing the frontend, static, backend, docs, website, sdks and native clients. there is no need to bring into scope "other repos" at this time. I would limit PROJECT.md to refrence strictly project specific information, not instructions. As you said, keeping the instructions generic, selectable based on scope makes them easy to update, distribute and merge. The only thing we have to keep in mind is that sometimes, as work gets done, new patterns emerge that might need to get folded into the original instructions. A separate file named "ADDITIONAL.md" (or ADDITIONAL_INSTRUCTIONS.md) might be the place for that and calleed out explicitly in the project / repo config and agents config would be good. And also, a native SaaS client may never exist; that itself is a choice.

### Revised proposal

Keep all selected components within one monolithic repository. Native SaaS clients are optional.
Use generated SDKs as the normal native client integration boundary. Cross-repository coordination is outside scope.
PROJECT.md contains project facts only. PROJECT_PROFILE.md contains scope choices and explicit file references.
ADDITIONAL.md holds local instructions and emerging patterns, and is explicitly selected through the profile and AGENTS.md.
Propose reusable lessons for the authoritative generic guides, then remove redundant local copies after adoption.
Updated the current proposal and status. No generic rules, templates, or setup scripts changed. Records remain local.

## 20 October 2026: publish the revised proposal

### User requests

> great. did you update teh pr?

> push then so I can review.

### Outcome

Confirmed that the two proposal commits remained local, then pushed b9eaf24 and 35a6193 to docs/target-guides for PR #2.
The published proposal describes one monolithic repository, selectable components, optional native SaaS clients, generated SDKs, facts-only PROJECT.md, and local instructions in ADDITIONAL.md.
Templates, generic routing changes, and the interview script remain proposed, not implemented.
The commit-range whitespace check passed. The PR remains open and unmerged.

## 20 October 2026: review UI overlap and trace Java SaaS instructions

### User request

> ok. I see that you still have UX_UX.md, UI_UX_COMPONENTS.md, UI_UX_CONSISTENCY.md and one more related to UI_UX. I also think there is a UX_UI file somewhere. Are they all different data or are they similar and overlapping. Can you check? Once you are done with that, let's run through a test again: Which files would be read if I was building a "SaaS" in Java, deployed in a container with a frontend along with native clients on Apple operating systems?

### Outcome

Compared tracked main and PR branch files and confirmed PR statuses through GitHub.
UI_UX_CONSISTENCY.md and UX_UI_GUIDELINES.md are deleted in the PR, not retained alongside the replacement guides.
UI_UX.md, UI_UX_COMPONENTS.md, and KEYBOARD.md remain with distinct roles and some overlapping subjects. UX_UX.md is absent.
Found an always-dialog conflict in ERROR_DIALOG_COMPONENT.md and overlapping browser implementation rules.
Recorded a manual routing test for one containerized Java SaaS monolith with frontend and native Apple clients.
The route reaches major guides, but native SaaS composition, Swift SDK navigation, and several generic .NET assumptions remain incomplete.
The profile/configuration system remains proposed. This review changes no generic instructions.
Recorded the complete reading map and evidence in specs/ui-ux-and-java-saas-audit.md for PR review.

## 20 October 2026: implement profiles and clarify error surfaces

### User request

> On: "I found a real conflict: ERROR_DIALOG_COMPONENT.md requires dialogs whenever users need an error message. UI_UX.md instead requires inline field errors and more selective modal use. That needs correction." --Actually both make sense. Literate error dialogs make sense for operations that show no visible interface. For example, a "Save" butotn just saves teh resource. So an error dialog there makes sense. Howevre, a "form" has a visible interface which can show inline errors. Let's clarify the two if thats causing confusion. Both have their uses. On: "This test is a partial pass. The major guides are reachable, but:
>
> - SAAS.md still describes backend/browser composition without native clients.
> - SDKs.md lacks a Swift reference.
> - Broad backend sections still impose .NET tools and syntax on Java work.
> - The profile selector remains proposed, so this was a manual document trace.
> " - Let's go fix that.

### Outcome

Implemented manual PROJECT_PROFILE.md selection, facts-only PROJECT.md, and local ADDITIONAL.md with reusable templates.
AGENTS.md reads configured project files and limits target/language selection to affected enabled components.
Connected optional native SaaS clients to generated SDK guidance and added Swift to the SDK index.
Scoped .NET, Knobby, shell, and browser implementation examples so they do not select frameworks for unrelated components.
Clarified literate dialogs for failed commands without a suitable visible error surface, inline field errors, persistent form save errors, and background failure status.
Repaired the stray final error-dialog fence while preserving its two code examples.
Added a fictional Java SaaS profile and repeated validation with a fresh-context sub-agent.
The reviewer passes all ten cases after resolving its remaining scope and setup findings.
Broader document checks preserve all 559 counted code blocks, existing encodings and headers, operating workflow, and append-only history.
No new Markdown link defects were introduced. Existing external component-path defects are recorded separately.
The interview script remains deferred. No application runtime build or test is claimed.
Update PR #2 for owner review, without merging or changing main.

Published the implementation as b6bcd89 on docs/target-guides.
Updated PR #2 title to "docs: organize guides and add selectable project profiles" and rewrote its description around the implemented scope.
The PR links the validation report and Java SaaS fixture. It remains open and unmerged.

## 20 October 2026: directory and branch cleanup

### User requests

> ok phew. I merged the PR. Now some cleanup: I see that you put a lot of stuff into ./specs/. I think we really should keep all instructions in ./instructions/ and only CLAUDE.md, AGENTS.md, GEMINI.md and CODEX.md at the root. Everything that you currently keep in ./specs/ should really be under ./instructions/ so that we reserve ./specs/ for repostiroy / product actual specifications.

> Also, now I see several branches and 2 PRs. Is PR1 still valid? Can we clean up the merged branches or obsolte branches so we can continue with a clean repo?

> "docs/target-guides\npriyavijaikalyan2007\n \n7 minutes ago\n1\n0\n#2\ndocs/language-guides\npriyavijaikalyan2007\n \n3 days ago\n15\n0\n#1\ndocs/multilanguage-instructions-plan\npriyavijaikalyan2007\n \n4 days ago\n17\n0\n" Those are the brancehs and PRs I see.

### Outcome

Verified that PRs #1 and #2 are merged and closed, synchronized main at 9f16499, and removed the three fully merged local and remote branches.
Created docs/instructions-directory for owner review.
Moved shared instructions and reference assets into instructions/, project-owned context into instructions/project/, and all former specs instruction records into instructions/maintenance/.
Root AGENTS.md now routes to the full shared workflow in instructions/AGENTS.md. Only the four agent entry Markdown files remain at root.
GitHub landing and policy documents remain discoverable under .github/. LICENSE and NOTICE remain legal metadata.
Updated active paths and links while preserving every original code block, source encoding, moved GUID, and historical conversation input.
Reserved specs/ for actual product and repository specifications.

## 20 October 2026: reading trees and selector request

### User request

> once you are done, it would be nice to sort have a tree view of the relevant files. Something like how the "tree" commnad would produce. For each set of things: "native standalone app", "native app for saas", "saas with frontend", "static website", "cli tool". This should be recorded in README.md for this repo - so that as the author, I can walk through each set of files and validate myself whether the instructions make sense or need updates. After that let's work on the profile selector/modifier script.

### Outcome

Added a shared baseline and five scenario trees to instructions/README.md, linked from the GitHub landing README.
Trees distinguish direct and conditional reading, actual language choices, generated SDK boundaries, and optional native SaaS clients.
The author can compare each tree against the active profile and manually inspect its relevant guides.
The next step is a preview-first initializer/modifier for the same Markdown profile, without changing generic engineering policies.

## 20 October 2026: profile selector implementation

### Outcome for the preceding selector request

Implemented scripts/configure-instructions.sh and scripts/configure_instructions.py against the existing Markdown profile.
The interview initializes or modifies enabled components and actual scope facts. JSON answers support repeatable partial edits.
Preview and check modes are read-only. Applying changes requires an explicit CLI choice or --apply.
Missing shared guides and root entries are copied from this checkout. Existing generic guides remain unchanged.
Project facts and refinements are created only when absent, with fresh GUIDs and explicit unspecified facts.
Handwritten component notes, project-file bytes, and root AGENTS content outside the managed block remain intact.
Validation rejects malformed metadata, missing source paths, invalid SDK links, unsafe paths, symlinks, and conflicting project files before writes.
Missing language/platform coverage is reported without substituting unrelated language instructions.
Added 35 integration tests, including the five scenarios, real interview, repeated updates, cancellation, and preservation/error cases.
Tests were written and observed failing before their implementations. All tests now pass.
The repo profile check passes and a dry run reports No changes. Bash syntax and Python 3.10 grammar checks pass.
Directory integrity checks preserve the original 559 code blocks, source encodings, headers, and append-only history.
The ten added code blocks contain README trees and selector usage examples. No new Markdown link defects were introduced.
Removed inherited trailing whitespace from the relocated master and changed prose lines, without altering workflow rules.
Documented usage and filesystem/runtime limits in instructions/REPO.md and the selector validation report.
Prepare one review PR with separate directory, reading-map, and selector commits. The owner will merge.

Published the implementation in three commits: b5b1dbf for relocation, 9c8a49c for reading trees, and 9c20e8d for the selector.
Opened PR #3, "docs: organize instruction files and add profile configurator", from docs/instructions-directory into main.
The PR is open and unmerged. The owner will review and merge.
The GitHub CLI currently has read-only permissions, so the PR was created through the existing owner browser session.
Only main and the new review branch remain locally and remotely. The working tree is clean after publication records.

## 20 October 2026: script questions and product-category interview correction

### User requests and questions

> ok. does the interview script have a "dry run" mode so I can test it out without any changes?

> Got it. Also, what is this "instructions/maintenance/examples/" -- Seems to contain only one java-saas example?

> ok. when running the script, I see: "Is this a SaaS product? [no]: no
> Enable instruction-library? [yes]: " -- You should explain each option. I am not sure what I should answer for the second question? What does it even mean?

> Another one: "Targets: backend, frontend, saas, tools, apps, websites, static-assets, sdks, documentation
> instruction-library / Source paths [`*.md`, `instructions/`, `.github/`, `agentknowledge/`]: " -- Very opaque.

> what's the difference between "backend, frontend, saas" -- is there a SaaS without a backend or frontend?

> I would expect the options to be more like this: "1. SaaS (only webapp; includes backend, frontend and static assets), 2. SaaS with Native Clients (webapp including backend, frontend and static assets + native apps on selected targets OS-es), 3. Microservice (SaaS with no frontend or static assets; only backend which includes APIs, databases and OpenSpec/Swagger endpoint), 4. Native App, 5. Static Website, 6. CLI tools". That's roughly the set of possible categoris I think.

### Outcome

Explained that --dry-run previews the current or JSON-supplied profile without running the interview or writing files.
The full interview remains safe to try by declining the final apply prompt.
Explained that maintenance/examples/java-saas contains one fictional reading-test profile, not application source or active configuration.
No extra example files were added during that explanation.

PR #3 merged at 4312353. Synchronized main and created fix/profile-interview-guidance for this correction.
Replaced raw component enable questions and target codes with the six requested product categories.
The selector derives underlying guide scopes, shows the target repository, and explains each selected part and requested fact.
Compatible categories combine in one monolithic repository. Overlapping SaaS categories prompt for a corrected selection.
Existing profiles can retain their enabled scopes and SaaS relationships by accepting the current product selection.
Explained instruction-library as this repository's documentation scope and repository-tools as its local CLI scope.
Source prompts describe repository-relative files, folders, and patterns with examples.
Language, operating-system, and packaging prompts explain the expected values and retained defaults.
The native SaaS preset connects its clients to a single selected generated SDK when unambiguous.
Switching to standalone native clears its prior SaaS SDK link.
The Markdown and JSON contracts, dry-run behavior, validation, and write boundaries remain compatible.
Manual or JSON edits support advanced custom components and specialized SDK relationships.
Accepted equivalent defaults now retain the original field formatting rather than rewriting inline-code path values.
Separated interview presentation into scripts/profile_interview.py and registered its knowledge concepts.
All 44 tests pass after the new and revised interaction tests were observed failing before implementation.
The actual repository interview was exercised by retaining every default. It reports No changes.
Repo checks, Bash syntax, Python 3.10 grammar, line lengths, indentation, function sizes, and diff whitespace checks pass.
Updated setup instructions and validation records. Publish a focused follow-up PR for owner review without merging.

Published implementation ffefb5a on fix/profile-interview-guidance.
Opened PR #4, "fix: guide profile interviews with explained product categories", against main.
The PR is open and unmerged for owner review. Main remains at the synchronized PR #3 merge.

## 20 October 2026: approve the interview correction merge

### User request

> ok. I think we need some refactoring of the instructions. For now let's merge this PR and then we will continue.

### Scope and verification

The owner authorized merging PR #4 and continuing instruction refactoring in a later request.
PR #4 is mergeable without conflicts. No GitHub check runs or review blockers are reported.
Its implementation passed all 44 local tests before publication. This merge request changes no application or script behavior.
Record the approval in the PR, merge it, synchronize local main, and remove fully merged review branches.
Do not start further instruction refactoring during this request.


## 21 October 2026: scoped folders, preserved common rules, and expanded security

### User requests

> ok. good. the next set of reorganization is this: 1) I think now instructions/ itself is very large. Let's organize like this: instructions/<type>/ -- where <type> is something like backend which might include all backend related instructions, instructions/website/ which might include static website related instructions and so on. Common ones that cut across would still stay in instructions/. Language specific ones go into instructions/<language>/. WDYT Of this organization scheme? I am essentially trying to set this up so that by convention, its intuitive and easy to know what files to edit to refine instructions for a particular language or a particular target. brainstorm this part with me.

> This looks ok. Except the use of README.md repeatedly insidee each sub-folder. I would prefer the actual namme that we use now instead. So, saas/SAAS.md, apps/APPS.md and so on. It's much easier. I am also curious about what you did with the README_TEMPLATE.md? Did that become the REPO.md or PROJECT.md?

> Good. The generalization makes sense. One question I have: after the interview is done, are the rest of the unnecessary files deleted? How does this work? What if they are needed later? Then, I see that AGENTS.md "Development" section still references several instructions again. Should that become more specific based on teh choices?

> makes sense. be wary to not lose things that are common in there such as adherence to LANGUAGE.md etc. Also, there were two separate security related files: SECURITY_GUIDELINES.md and AIML related security. Did you check those two?

> Agreed. Go ahead. I also think that, when you work on security guideliness, you need to account for certain things: 1) Language specific guidelines if any such as being secure with SQL, secure with C# (using SecureString if supported and so on), AI ML Security (input segregation, sanitization etc.), HTML / Javascript security (using eval on external code, innerHTML sanitization and so on) etc. 2) You should also think about multi-tenant service security, clipboard data security, temporary storage security, swap storage security, marking sensitive sections in memory (where supported) etc. In other words, not just editing the existing guidance but also expanding on them as appropriate.

### Decisions and outcome

PR #4 previously merged at bc2bafc. Created refactor/scoped-guides-security from the clean main branch.
Moved 37 guides and reference files into target/language folders while retaining descriptive filenames.
Renamed the shared inner AGENTS.md to WORKFLOW.md. The root AGENTS.md remains the entry point.
Preserved all 31 Development requirements, including LANGUAGE.md, and grouped common and task-specific obligations.
Updated active links and README scenario trees. Generalized README_TEMPLATE.md without merging it into PROJECT.md or REPO.md.
The selector installs nested shared files, retains inactive guides, and excludes project records and maintenance fixtures.
The generated root block lists shared requirements and enabled target/language guides. The profile remains authoritative.
The --check mode rejects stale generated routing. Existing project-owned files and handwritten root content remain preserved.
General and AI security remain separate common guides. Added language security sections and target security routing.
Expanded tenant, clipboard, temporary-file, memory, swap, dump, logging, model, retrieval, and tool-execution controls.
Corrected SecureString recommendations, prompt-prefix guarantees, regex extraction, blanket personal-data filtering, and implied memory erasure.
All 50 selector tests pass. The Java SaaS/browser/Apple fixture routes correctly without selecting C#.
Link checks found no new defects. Headers, encodings, previous history, and non-security examples remain intact.
A .NET harness accepted three valid JSON responses, rejected 13 invalid responses, and verified buffer cleanup.
Other language and platform examples were reviewed but not all executed. See maintenance/scoped-guides-security-review.md for details.
Commit the verified changes locally. Do not push or merge during this update.


## 21 October 2026: extension profiles and combined publication

### User requests

> Great, I want to create guidance for new types of profiles: "Google Workspace Extensions", "Microsoft Office 365 / Microsoft Office Extensions" and "Browser Extensions (typically Chrome, Safari or Mozilla)". At least knobby.io envisages building a browser extension. Google Workspace extension I am building for making my own writing easier; Microsoft Office 365/App extensions we can skip for now. Add that, incorporate that into the profiles in the interview script and then commit push and merge everything to main. I will then be able to test things out in some test repos to see how things work e2e.

> continue

### Outcome and delivery scope

Added Google Workspace and browser extension guides, profile targets, interview choices, templates, and reading trees.
Choices 1 through 6 remain stable. Choice 7 selects Google Workspace. Choice 8 selects browser extensions.
The interview explains hosts, browsers, packaging, and optional SaaS relationships. Microsoft Office remains deferred.
Existing profiles retain intentionally unlinked SDKs when users accept their current selections.
All 55 tests pass. The repository profile check and dry run pass without generated changes.
Link and preservation checks report no new defects. No host extension runtime or store publication was tested.
The owner authorized pushing and merging this work together with the pending guide and security reorganization.
This authorization supersedes the previous local-only delivery scope. Merge through a pull request, then synchronize main.


## 21 October 2026: initialize copied projects and select licenses

### User requests

> Ok. Since this is a template repository, I created a new repository named utilextensions from the instructions repo and found some bugs. 1) The README.md, CONTRIBUTING.MD, LICENSE, CODEOFCONDUCT.md and SECURITY.md files reflect the details of the instructions repository, not hte new repository. The new repository should have placeholders with instructions that show what the new repo needs. How do we make that happen? I don't want to modify the same files in the instructions repo though.

> For license, you can ask for common license types: MIT, Apache, LGPL, GPL (2.0, 3.0), dual mode (like ElasticSearch), Creative Commons etc. and apply from that? Otherwise, this makes sense.

### Outcome

Implemented explicit new-project initialization in the existing profile configurator.
The source repository's .github/README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, and root LICENSE remain unchanged.
New policy templates collect project identity and leave unknown project decisions as visible TODOs.
Known inherited documents and records receive exact backups before replacement or removal.
Customized documents, history, and profile notes remain untouched. Conflicting licenses and symlinks stop before writes.
The generated documents honor custom project-facts and local-instruction paths.
The interview supports MIT, Apache 2.0, LGPL 2.1/3.0, GPL 2.0/3.0, AGPL 3.0, Elastic 2.0, and SSPL 1.0.
GNU choices require only or or-later. Multiple licenses use OR, with no product-name preset.
Creative Commons 4.0 variants and CC0 1.0 apply to explicit content paths.
Custom or undecided terms remain pending. Copied instruction material retains its MIT license and notices.
Pinned SPDX texts and hashes support offline setup. LGPL 3.0 includes its GPL 3.0 companion text.
A source-only maintenance command registers reviewed inherited-file hashes while retaining older versions.
All 77 tests pass, including execution from a copied repository, preview, cancellation, repeat runs, and generated links.
The actual utilextensions repository was not changed. Changes are prepared on feat/project-initialization for local review.

### Continuation

> continue now.

Completed the remaining template-link checks. No new link defects or preservation discrepancies remain.
Source policy files and LICENSE remain byte-identical. Commit the verified implementation on the local review branch.

## 21 October 2026: publish project initialization for testing

> great. yes, push the branch and raise the PR. I can try it out in a new repo again.

The owner authorized pushing feat/project-initialization and opening a pull request for review.
The implementation passed 77 tests. Publish the verified branch and leave the pull request unmerged for new-repository testing.

## 21 October 2026: Workspace-specific interview and planned source scope

### Request

> ok. Here is what happened when I ran this script on a new repository where I was going to build Google Docs extensions (and perhaps in the future Gmail, Sheets & Slides too). While the first choice makes sense, subsequent choices don't make sense for this particular option. Like, how would I distribute Google Docs Extensions? What assets etc. are required? How they are packaged, built and distributed. When I pick an option, everything ofr that option shoudl be covered right?

The user supplied this terminal transcript:

```text
vijaikalyan@vijakalyan-mbppro:~/Work/pvk2007/extensions$ ./scripts/configure-instructions.sh
This repository contains the instruction library's original project profile.
1. Initialize a new project: replace known inherited identity and policy files after preview.
2. Edit only instruction selections: preserve all repository documents.
Setup mode [2]: 1

Initialize documents for a new repository copied from the instruction template.
Known inherited originals will be backed up. Customized files will be preserved and reported.
Contribution rules, private contacts, and response targets remain TODOs for the project owner.
Repository name [extensions]:
Copyright owner [required]: Priya & Vijai Kalyan
Copyright year [2026]: 2026
HTTPS repository URL [required]: https://github.com/priyavijaikalyan2007/extensions
Project purpose [TODO: Describe this project and its users.]: Useful Google Workspace, Office and Browser extensions. ^[[D^[[D^[[D^[[D^[[D^[[D^[[

Choose the license for new project software. Read the bundled terms before publishing.
  1. MIT: Permissive terms with attribution and warranty disclaimer.
  2. Apache-2.0: Permissive terms with an express patent grant and notice requirements.
  3. LGPL-2.1: Lesser GPL version 2.1, commonly used for libraries.
  4. LGPL-3.0: Lesser GPL version 3.0, with GPLv3 companion terms.
  5. GPL-2.0: GPL version 2.0 copyleft terms.
  6. GPL-3.0: GPL version 3.0 copyleft terms.
  7. AGPL-3.0: Affero GPL version 3.0, including network-use source obligations.
  8. Elastic-2.0: Source-available terms with managed-service and other restrictions.
  9. SSPL-1.0: Source-available terms with service-source obligations.
  0. Undecided or custom/commercial terms: create a TODO, not a fabricated license.
For dual or multiple licensing, enter distinct numbers separated by commas.
Recipients may choose any listed license (OR). This does not combine their obligations (AND).
Elastic and SSPL are source-available choices, not OSI-approved open-source licenses.
Software license numbers [0]: 1

Content licensing applies to named documentation, artwork, or data paths.
Creative Commons recommends software-specific licenses for code. These choices apply only to content.
  0. No separate content license. Keep the project terms or pending decision.
  1. CC-BY-4.0
  2. CC-BY-SA-4.0
  3. CC-BY-ND-4.0
  4. CC-BY-NC-4.0
  5. CC-BY-NC-SA-4.0
  6. CC-BY-NC-ND-4.0
  7. CC0-1.0
BY: attribution. SA: share alike. NC: noncommercial. ND: no derivatives. CC0: public-domain dedication.
Content license [0]: 0
Configuring repository: /Users/vijaikalyan/Work/pvk2007/extensions
Profile: instructions/project/PROJECT_PROFILE.md
Creating a new profile.
Component identifiers are local names in this profile, not product types.
Guidance is selected automatically from your product choices and actual source languages.
Press Enter to keep a displayed current value. No files change until you approve the final preview.

Choose the product types that this repository contains:
  1. SaaS: Webapp with backend, browser frontend, and static assets.
  2. SaaS with Native Clients: The webapp plus native apps and generated SDKs.
  3. Microservice: Backend only: APIs, data access, and an OpenAPI/Swagger endpoint.
  4. Native App: Standalone application for selected operating systems.
  5. Static Website: Website and static assets without an application backend.
  6. CLI tools: Command-line tools or plugins for selected operating systems.
  7. Google Workspace Extensions: Workspace or Editor add-ons, such as a Google Docs writing assistant.
  8. Browser Extensions: Extensions for Chrome, Safari, Firefox, or selected compatible browsers.
SaaS describes the product. Backend means server-side work. Frontend means the browser UI.
The microservice choice includes no browser frontend or static assets.
Extensions can stand alone or combine with SaaS. Microsoft Office extensions are not included yet.
Combine compatible categories, such as 1, 5, 6 for a SaaS, public website, and CLI tools.
Product numbers, separated by commas: 7

Included parts: Google Workspace extension (workspace-extension)
Product selection changes instruction scope, not application source, folder structure, or deployments.

Component: workspace-extension (Google Workspace extension)
Host-integrated Workspace or Editor add-on behavior.
Covers: not configured yet
Name the host and add-on type, such as Google Docs (Editor add-on) or Gmail (Workspace add-on).
For packaging, record Apps Script or HTTP runtime and test, private, or Marketplace distribution.

Which existing files or folders belong to this part? Paths are relative to the selected repository.
Examples: src/server, apps/apple, web, scripts. A pattern such as *.md matches root Markdown files.
Use commas for several paths. These paths limit where the selected guidance applies.
Files or folders [required]: src/docs/, src/mail/

Enter the actual source languages used in this part, separated by commas.
Examples: Java, C#, Swift, Go, Rust, or Python. Browser code may use TypeScript, HTML, and SCSS.
Source languages [required]: Javascript/Typescript, HTML, SCSS

Enter the operating systems or consumer platforms, separated by commas.
Examples: iOS, iPadOS, macOS, Android, ChromeOS, Linux, or Windows. Use browser for a generated browser SDK.
Operating systems or platforms [required]: browser

Describe how this part is packaged or delivered. This records a fact and does not deploy anything.
Examples: container, served by the backend, CDN, native application, CLI binary, generated library, or none.
Packaging or delivery [required]: none
Configuration error: workspace-extension: source path does not exist: src/docs/
```

### Outcome

Added a dedicated Workspace interview for current hosts, model, runtime, account context, and distribution.
The interview explains compatible build output, runtime assets, host testing, OAuth, and Marketplace preparation.
Expanded the Workspace guide with linked build, packaging, test, and release checklists based on Google documentation.
Added explicit planned literal source paths without creating application directories or weakening existing-path checks.
Normalized JavaScript/TypeScript input and retained legacy profile compatibility with a setup note.
PR #6 was already merged. This correction uses fix/workspace-profile-interview from the updated origin/main.
The user's extensions repository was not accessed or modified. No Google build, installation, or publication was performed.

### Continuation

> try again

Continued the correction from its existing branch and test failures.
Fixed the remaining conditional build advice and completed the full verification before committing locally.

All 96 tests pass, including the complete copied-repository Docs setup.
Profile, dry-run, Markdown link, preservation, syntax, and whitespace checks pass.
The correction is committed locally. No push or merge was requested for this correction.

## 21 October 2026: additive source and test directory conventions

### Requests

> Great. Now, let's work on "recommended" folder structures. In my existing repositories I made the mistake of not setting things up well. So I want to fix that going forward. First, instructions already live in instructions/, specs in specs/, bug reports in bugreports/, playbooks in playbooks/, user facing docuemntation in docs/ etc. However, I want to make sure source code is in src/<type>. Example, if a repo has a native SaaS, with a native client and a web frontend along with SDKs, then we would want something like src/service/, src/service/static/, src/service/backend/ and src/service/frontend/, website at src/website/, apps at src/app/ and so on. Even if those options are not selected, adhering to this structgure enables additive enhancement over time. Brainstorm this with me and propose a folder structure setup that makes sense.

The proposed convention used src/<type>/<component-name>/, even for a single component.
The proposal kept toolchain-specific project structures inside that named component and preserved established layouts.
It separated static source from compiled output and kept optional components absent until needed.

> Thats actually quite good. I would call the root tests/ folder test/ simlar to src/. I agree on database ; perhaps that should be in src/service/database or src/database/ ? I agree with the rest and then include that in the per "profile" documentation about how things are setup as instructions. That way, once setup, the agents know where to place things by default.

### Outcome

Adopted root test/ for new cross-component tests and src/<type>/<component-name>/ for new product components.
The default database location is src/service/<service-name>/database/, beside backend/, frontend/, and static/.
An independently managed database can use src/database/<database-name>/ with explicit ownership.
ORM-required migration classes and snapshots remain in their backend project without duplicating the migration sequence.
Native and tool persistence stays with the app or tool.

REPO.md owns the common convention. Each target guide now documents its matching component layout.
The profile and project-facts templates link or record the relevant locations and exceptions.
The interview suggests named example paths only when no concrete source path is configured.
Users can replace example names and still must approve planned paths explicitly.
No application directories were created, and existing repository source paths were not moved.

All 101 tests pass, including accepted defaults across SaaS, native clients, SDKs, websites, tools, and extensions.
The source profile check and dry run pass. No new Markdown link defects were found.
Five existing layout-example groups changed intentionally. Other example content remains preserved.
Existing CP1252 frontend content remains byte-identical around the inserted layout section.
Commit locally on docs/recommended-layouts. No push or merge was requested.

### Publication request

> push and raise the PR please.

The owner authorized pushing docs/recommended-layouts and opening a pull request against main.
The verified implementation passed 101 tests. Leave the pull request unmerged for review.


## 21 October 2026: Apps Script runtime guidance

### Request

> ok. reviewed and merged. I think we are largely in good shape. One question - for the Google Workspace extensions, we might need to be writing Javascript & Appscript code. Do you have guidance for those languages?

The review found shared JavaScript guidance and Workspace lifecycle guidance, but no dedicated Apps Script runtime guide.
The proposed change added that guide, concrete examples, and runtime-based profile selection.

> good. go ahead.

### Outcome

Added instructions/apps-script/APPS_SCRIPT.md, layered on the shared JavaScript guide.
It distinguishes server Apps Script, browser-side HTML-service code, and local Node.js tooling.
It covers runtime syntax, file organization, callbacks, authorization, request validation, state, locks, quotas, logging, and testing.
Examples show Editor menus, pure text processing, sidebar communication, shared properties, batched Sheets reads, and structured logs.
Google's official documentation supports the runtime-specific facts.

Workspace apps-script runtimes now select Apps Script and JavaScript guidance for either JavaScript or TypeScript source.
Explicit Apps Script language labels select both guides, including in legacy profiles without structured runtime metadata.
HTTP JavaScript add-ons select backend and JavaScript guidance without selecting the Apps Script runtime guide.
Switching runtimes removes obsolete scope from AGENTS.md while preserving installed guide content.
The existing answer format and this repository's active profile remain unchanged.

All 106 selector tests pass. New routing cases failed before implementation.
Six JavaScript example blocks parse and pass controlled local host-stub checks.
Those checks cover validation, safe logging, menu callbacks, batching, lock failures, and sidebar errors.
They do not verify live Google authorization, host behavior, deployment, or quotas.
Local Markdown links and anchors pass. Existing code examples remain intact except the updated Workspace reading tree.
The CP1252 guides remain byte-identical. Source profile check and dry run pass without changing the active selection.
Commit locally on feat/apps-script-guidance. No push or publication was requested.


## 22 October 2026: product-specific browser setup and folder bootstrap

### Request

The owner supplied a new-repository interview transcript selecting Google Workspace and browser extensions.
Workspace prompts collected useful facts, but browser prompts requested generic languages, platforms, and delivery.
The owner entered browser as the platform and served by the backend as delivery.
The browser source scope of src/ also overlapped the Workspace source scope.
The owner requested extension conventions matching src/extensions/googleworkspace/markdown and creation of captured folders in new repositories.

> Also, it would be nice if the interview was properly formatted with well differentiated text (colors, etc.). You can also use ncurses if you prefer. The current one is very bland.

### Outcome

Added a dedicated browser interview with supported browser/OS pairs, distribution choices, and selected-browser build guidance.
The current preset covers Chrome/Edge desktop, Firefox desktop/Android, and Safari macOS/iOS/iPadOS.
It distinguishes developer tests, store distribution, and Firefox signed self-distribution.
The interview explains manifests, bundles, referenced assets, permissions, signing, listings, and release stages.
A backend API does not substitute for extension installation.
Legacy free-text profiles remain readable with a warning to rerun the browser interview.
The selector warns about overlapping literal Workspace and browser scope without forbidding intentional shared source.

Browser and Apps Script prompts now offer explained JavaScript and TypeScript presets.
UI presets default to JavaScript, HTML, and CSS. TypeScript, SCSS, script-only source, and custom lists remain selectable.
HTTP Workspace services retain their actual backend-language question.
Apps Script source labels remain specific to the Google runtime.

New extension defaults use src/extensions/googleworkspace/<extension-name>/ and src/extensions/browser/<extension-name>/.
The interview uses markdown as a replaceable example name and preserves concrete configured paths.
First-time interactive setup records approved missing folders in optional Source folders metadata.
Final apply creates only those folders and their parents. It generates no application files.
JSON/manual callers can select source_folders explicitly. Planned files remain separate from folder-creation metadata.
Existing-profile edits do not automatically add new folder-creation selections.
Dry runs, checks, cancellation, and invalid plans do not create directories.
Preflight rejects unsafe paths, symlinks, existing-file conflicts, and planned instruction-file conflicts.
Git does not retain empty directories. The saved metadata supports restoring them through another selector run.

Added semantic terminal colors for headings, options, defaults, warnings, results, and diffs.
The line-oriented interview uses no extra dependency. Color remains optional through --color auto/always/never.
Automatic mode honors NO_COLOR, TERM=dumb, and redirected output. Identity and license prompts share the same renderer.

Official platform documentation supports the browser delivery guidance.
Current Apple options include temporary macOS folder tests and App Store Connect packaging without local Xcode.
Native wrapper languages remain conditional on actual native-source edits.

All 127 tests pass, including 21 new tests for browser choices, combined setup, safe folder creation, and terminal presentation.
Copied-template initialization and existing-profile preservation checks pass.
Local Markdown links and anchors pass. Four extension path examples changed intentionally.
Other existing code blocks and both CP1252 documents remain preserved.
The active source profile check and dry run pass without changing AGENTS.md.
Commit locally on fix/extension-bootstrap-interview. No downstream repository or browser installation was changed.


### Publication and merge request

> right, raise the PR and then merge. I will create another repo and test the template.

The owner authorized pushing fix/extension-bootstrap-interview, creating a pull request, and merging it into main.
The branch includes the preceding Apps Script guide and the verified extension interview and bootstrap fixes.
All 127 tests passed. Source checks, template baseline, links, and terminal smoke tests also passed.
Use a normal pull-request merge after remote checks, then synchronize local main for the owner's next template test.


## 22 October 2026: root project context and local setup interview

### Requests

> Ok. I feel there are a number of problems with the placement of files and the content of files as well. 1) I think PROJECT_PROFILE.md and PROJECT.md both should be at the root of the repo. Interview script should move it there and update any references. That is, things that are project specific should be at the root and things that are generic/common should be in instructions/. Perhaps most of instructions/project/ should be that? 2) I think we should think about asking the user what "role" Claude, Codex, Gemini play. Perhaps the user uses something like PI or Roo or Cline which has different instructions. This will help tailor (if needed) different coding agents for differnt roles. For example, in some cases, I use Claude for writing code but in others Codex; I use Antigravity for other things. Each one plays a different role based on the repository. 3) I am tired of trying to create a repo and using the template repo to create it; can you make sure that the interview script has a "target folder" mode in which it can do the same setup but it can be a local temp directory that I can delete and retry? Helps me test locally instead.

The owner selected multiple roles per tool in the profile.

> Another bug: why is there a separate LICSENSES folder when there is already a LICENSE file at root?

> Some more fixes: 1) I think you should scaffold placeholder scripts. See ~/Work/knobby/apps and ~/Work/knobby/idp/ and ~/Work/pvk2007/rapid/ for the type of scripts that are easy adn common to setup and how they work. They don't have to "do" anything; just be generated and placed in there with examples on how to fail, how to log etc. For example, smoke.sh if needed, deploy.sh if needed, monitor.sh, logs.sh, build.sh, test.sh, clean.sh, migrate.sh, runsql.sh and so on. For anything with a backend, we can use a 3-environment model (test, dev and prod) where test is local machine, dev is staging deployment and prod is production. 2) You should print a list of files and instructions for what needs to be modified to actually make the setup ready adn relevant for that repo. 3) It might be good to interview the user about business context etc and include them directly in the gneerated PROJECT.md etc. WDYT?

> After thinking about this, I really think you should proper ncurses for the interview script; at this point its long, complex and has a lot of user input which deserves a proper interface. When I hit delete or something else in the terminal, it results in control characters. ncurses might take care of that with textboxes and such?

> great. commit, push, raise the PR and merge. I will test locally.

### Changes

Moved the five default project Markdown files to the root. Shared guides and templates remain under instructions/.
Legacy migration repairs active links and guide references while retaining historical record bytes and private file permissions.
Conflicting root and legacy files stop setup before writes. Custom context locations remain authoritative unless they collide with reserved files.
Initialization state and original-file backups use .instructions/.
The fictional Java routing example now models project files at its fixture root.

Added multiple project roles per coding tool and shared role definitions.
The tool entry files now point to AGENTS.md and the profile without fixed vendor roles.
Known inherited entries receive backups before replacement. Custom entries remain unchanged.
Roo receives its documented workspace pointer when selected. Other supported tools use their shared/native entry mechanism.
Role choices do not grant tool permissions or authorize delegation.

Added --target-folder for local setup without GitHub, Git, or a pre-existing target directory.
Interactive and JSON dry runs remain read-only. Approved setup installs its own setup tools for later edits.
The interview captures optional business facts and leaves unknown facts as TODOs.
Invalid identity and business facts can be corrected without repeating accepted answers.

Generated missing profile-specific operation placeholders and SETUP.md completion tasks.
Placeholders show logging, argument checks, and failure handling. They return 2 until implemented.
Backend scripts use test for local work, dev for staging, and prod for production.
Actual environments, commands, credentials, and application implementation remain project work.
A single software license keeps its full terms in root LICENSE. Multiple or companion texts retain LICENSES/.
Existing initialized legal files remain preserved.

Interactive terminals now use ncurses forms with text editing, selectable menus, scrolling help, and explicit cancellation.
The full preview precedes final approval. Plain mode remains available for automation or unsupported terminals.
The screen handles forward Delete, Backspace, cursor movement, Unicode, and resizing.
Curses restores terminal input modes when the interface closes or raises an exception.

### Publication

The owner explicitly authorized committing, pushing, opening a pull request, and merging it into main.
Publish the verified feature branch through the normal pull-request workflow, then synchronize local main.
No downstream application repository was modified. Private source identifiers and deployment commands were not copied into generic templates.


### Verification

The 127-test baseline passed before implementation. The expanded suite passes all 173 tests.
Real ncurses PTY checks verify forward Delete, Backspace, cursor edits, checkbox selection, resize, review, apply, and cancellation.
Normal input modes and erase bindings return after the interface closes.
macOS can retain its PENDIN bookkeeping flag after returning to canonical input. Functional terminal modes remain restored.
A complete Docs/browser setup passes through dry run, apply, copied-tool validation, and unchanged repeat configuration without Git.
Single-license output contains full root terms. Conditional operation scripts fail with TODO status until implemented.
Markdown links, active profile validation, read-only preview, inherited baselines, and source formatting checks pass.
Existing examples remain intact except the intentionally updated common reading tree.
The two CP1252 guides changed only default project-path tokens. Prior conversation bytes remain intact before this appended record.


## 22 October 2026: shorter setup entry point

User: Also, I think the instruction configuration script should just be called configure.sh or init.sh; not "configure-instructions.sh" -- too long.

User: Brevity is nice.

Response: Added root configure.sh, installed it in local targets, and updated current documentation. Retained the old launcher for compatibility. Verified local setup, paths with spaces, and the regression suite.

User: Ran the script. 1) Question 16 is unexplained nad has just "Available agent roles:" - what is it supposed to do? 2) Why is teh ifnal review or the "Setup result" page showing me diff style output? Is that useful for an end user or should it be formatter better for readability?

Response: Repeat the purpose and controls for every tool role question. Show readable setup summaries and completion steps in forms. Keep exact file changes available through F3 and preserve plain-mode diff output.


## 22 October 2026: root public documents

User: Great. That seems good. One final question: why do the files that are supposed to be in the repository root such as Create .github/CODE_OF_CONDUCT.md
  Create .github/CONTRIBUTING.md
  Create .github/README.md
  Create .github/SECURITY.md stored in a separate .github folder? The .github folder is supposed to be for Github specific stuff like Actions and such right? Placing them at the root immediately makes the landing page of any github repo created from these instructions usable on day 1. Plus, what is the different between what README.md would say and what PROJECT_PROFILE.md or PROJECT.md would say?

Response: GitHub supports the previous location, but root documents match the project convention. README introduces the product and first use. PROJECT holds detailed facts. PROJECT_PROFILE selects instruction scope and tool roles.

User: agree. please fix.

Response: Moved the source public documents to the root and updated initialization, completion links, and shared guidance. Existing setups preview safe moves and preserve customized text and permissions. Conflicts stop setup before writes. GitHub configuration remains in .github/.


## 23 October 2026: UI interview navigation

User: Ah. Foudn another bug. Let's say I want to revisit a previous question or move back and froth between questions in the interview, I should be abel to do that. But only in the UI version.

Response: Added UI-only F5 Back and F6 Next, with session drafts and existing field validation. Back from the pre-apply review revisits the last question. Earlier edits rebuild conditional questions and the final plan. Later matching answers require confirmation, and final approval is never replayed. Navigation locks before filesystem writes. Plain and JSON workflows remain sequential.


## 23 October 2026: contextual language and platform menus

User: I found some more issues. In multiple places such as tagret language selection, target platform selection etc. you ask for a comman separated free form input. Since this repository only supports specific languages and target platforms, best to present selection relevant options instead. That means, for example, if the target platforms are iOS, iPadOS and macOS, the target languages may present Swift along with TypeScript, HTML, CSS & SCSS (since those are common for websites). If tools is picked, then expanding to present Python or Go is useful.

Response: Replaced language and platform name entry with supported selection lists in UI and plain interviews. Native apps, CLI tools, and generated SDKs choose platforms before contextual source languages. Extensions choose individual script, markup, and stylesheet languages. Existing unlisted facts can be retained explicitly. Platform edits rebuild language checkboxes. Manual and JSON validation remains available, and local targets include the shared catalog. Regression tests and a real ncurses checkbox trial verify the changes.
