<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 3fa4a3ee-0dc0-44b5-a2a0-d58e0edecaee
Created: 2026
-->

<!-- AGENT: Target routing and extracted existing guidance for static websites. -->

# Static websites

## Target scope

Static websites without an application backend. Browser source and static delivery guidance are selected separately.

## Topic references

| Work in scope | Existing guidance |
| --- | --- |
| Shared repository commands | [REPO.md](REPO.md) |
| Applicable UI/UX behavior | [UI_UX.md](UI_UX.md) |
| Shared browser standards | [FRONTEND.md](FRONTEND.md#11-standards-compliance) |
| Browser accessibility and usability | [FRONTEND.md](FRONTEND.md#13-accessibility-and-usability) |
| Browser compatibility | [FRONTEND.md](FRONTEND.md#18-browser-compatibility) |
| Browser security considerations | [FRONTEND.md](FRONTEND.md#19-security-considerations) |
| Static assets and hosting | [STATIC_ASSETS.md](STATIC_ASSETS.md) |
| Existing documentation publication checks | [DOCUMENTATION.md](DOCUMENTATION.md#verified-facts-and-published-contracts) |

## website and browser guidance

- A static website may use HTML and CSS with no backend or JavaScript.
- Use the project's asset and delivery pipeline. Apply API guidance only when the website actually calls or serves APIs.
- Use TypeScript for non-trivial browser scripting. Move inline JavaScript beyond ten lines into a TypeScript module.
- Apply browser component rules to browser UIs. Native apps use platform controls and their declared design conventions.
