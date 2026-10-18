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
