<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 52d49c9d-6be3-4e8c-bbf6-9286ddf26a8a
Created: 2026
-->

<!-- AGENT: Copyable manual component selections and project file references. -->

# Project profile template

Active configuration filename: PROJECT_PROFILE.md. Template source: PROJECT_PROFILE_TEMPLATE.md.
Copy it to PROJECT_PROFILE.md, complete the values, and check each enabled component.
Keep project facts in PROJECT.md and local instructions in ADDITIONAL.md.
Read [REPO.md](./REPO.md#project-configuration) for the selection rules and setup procedure.

## Project files

| Purpose | Path |
| --- | --- |
| Project facts | `PROJECT.md` |
| Additional instructions | `ADDITIONAL.md` |

## Project choices

- [ ] SaaS product
- [ ] Enterprise browser shell example from SAAS.md
- [ ] Knobby authorization example from ACCESS_CONTROL.md
- [ ] Knobby deletion example from DELETION.md
- [ ] PostgreSQL/EF Core manual SQL example from PERSISTENCE.md
- [ ] Theme component-library example from STATIC_ASSETS.md

## Components

Each component needs a unique identifier. Duplicate a component section when platforms or languages need separate scopes.
Check Enabled only for components present in this repository.
Replace angle-bracket values. Use `none` when a field does not apply.

### backend

- [ ] Enabled
- Source paths: `<backend source and configuration paths>`
- Targets: backend
- Languages: `<Java, C#, or the actual source languages>`
- Platforms: server
- SaaS client: no
- SDK component: none
- Deployment: `<container, server, or configured mode>`

### frontend

- [ ] Enabled
- Source paths: `<browser source paths>`
- Targets: frontend, static-assets
- Languages: `<actual browser source languages>`
- Platforms: browser
- SaaS client: `<yes or no>`
- SDK component: `<SDK identifier or none>`
- Deployment: `<served by application, separate static delivery, or configured mode>`

### sdk

- [ ] Enabled
- Source paths: `<API specification, generator configuration, and output paths>`
- Targets: sdks
- Languages: `<generated output languages affected by the task>`
- Platforms: `<consumer platforms>`
- SaaS client: no
- SDK component: none
- Deployment: generated library

### native-client

- [ ] Enabled
- Source paths: `<native source and target configuration paths>`
- Targets: apps
- Languages: `<actual source languages>`
- Platforms: `<iOS, iPadOS, macOS, Android, ChromeOS, or actual platforms>`
- SaaS client: `<yes or no>`
- SDK component: `<SDK identifier or none>`
- Deployment: native application

### website

- [ ] Enabled
- Source paths: `<static website source paths>`
- Targets: websites, static-assets
- Languages: `<actual website source languages>`
- Platforms: browser
- SaaS client: no
- SDK component: none
- Deployment: `<configured static hosting>`

### documentation

- [ ] Enabled
- Source paths: `<documentation source paths>`
- Targets: documentation
- Languages: none
- Platforms: none
- SaaS client: no
- SDK component: none
- Deployment: `<configured documentation delivery or none>`

### tool

- [ ] Enabled
- Source paths: `<tool source and configuration paths>`
- Targets: tools
- Languages: `<actual tool languages>`
- Platforms: `<supported operating systems>`
- SaaS client: no
- SDK component: none
- Deployment: `<CLI binary, package, or configured mode>`
