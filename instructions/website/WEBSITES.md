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
| Shared repository commands | [REPO.md](../REPO.md) |
| Applicable UI/UX behavior | [UI_UX.md](../UI_UX.md) |
| Shared browser standards | [FRONTEND.md](../frontend/FRONTEND.md#11-standards-compliance) |
| Browser accessibility and usability | [FRONTEND.md](../frontend/FRONTEND.md#13-accessibility-and-usability) |
| Browser compatibility | [FRONTEND.md](../frontend/FRONTEND.md#18-browser-compatibility) |
| Browser security considerations | [FRONTEND.md](../frontend/FRONTEND.md#19-security-considerations) |
| Static assets and hosting | [STATIC_ASSETS.md](../static-assets/STATIC_ASSETS.md) |
| Existing documentation publication checks | [DOCUMENTATION.md](../DOCUMENTATION.md#verified-facts-and-published-contracts) |

## Recommended source layout

For a new website, use `src/website/<website-name>/`, including a website that accompanies a native app or SaaS.
Apply the [shared folder convention](../REPO.md#folder-and-file-structure). Preserve existing configured source paths.

```text
src/website/<website-name>/
    content/               Editable site content, when the site uses a content pipeline
    frontend/              Templates, scripts, styles, and assets processed by the build
    static/                Authored files copied directly without compilation
    test/                  Website component tests, subject to the toolchain's required spelling
    scripts/               Website-specific automation
```

Keep the site's manifests and framework configuration at its project root.
Use the framework's internal source layout when it differs from this example. Record that mapping in project facts.
Generate publishable output into ignored build or distribution directories.
Keep canonical user-documentation source under root docs/ when the website publishes that documentation.
Copy or transform that source during the website build instead of maintaining a second editable copy.
Use `deploy/<website-name>/` for repository-wide hosting configuration.
A support or documentation website remains distinct from the application's browser UI.

## website and browser guidance

- A static website may use HTML and CSS with no backend or JavaScript.
- Use the project's asset and delivery pipeline. Apply API guidance only when the website actually calls or serves APIs.
- Use TypeScript for non-trivial browser scripting. Move inline JavaScript beyond ten lines into a TypeScript module.
- Apply browser component rules to browser UIs. Native apps use platform controls and their declared design conventions.


## Security scope

Apply [general security](../SECURITY_GUIDELINES.md) and the selected language security sections.
Select clipboard, temporary storage, sensitive memory, and tenant-isolation controls when the changed behavior uses them.
For any AI or ML feature, also apply [AIML_SECURITY.md](../AIML_SECURITY.md).
