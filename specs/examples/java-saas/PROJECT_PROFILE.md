<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 4bdd4bc8-064a-4f26-af75-400e74183ec0
Created: 2026
-->

<!-- AGENT: Fictional enabled components for the Java, browser, SDK, and Apple reading test. -->

# Java SaaS routing fixture

This is a fictional profile for instruction-routing validation, not this repository's active configuration.
Paths below are relative to an imagined consuming repository. No application artifacts are supplied by this fixture.

## Project files

| Purpose | Path |
| --- | --- |
| Project facts | `PROJECT.md` |
| Additional instructions | `ADDITIONAL.md` |

## Project choices

- [x] SaaS product
- [ ] Enterprise browser shell example from SAAS.md
- [ ] Knobby authorization example from ACCESS_CONTROL.md
- [ ] Knobby deletion example from DELETION.md
- [ ] PostgreSQL/EF Core manual SQL example from PERSISTENCE.md
- [ ] Theme component-library example from STATIC_ASSETS.md

## Components

### backend

- [x] Enabled
- Source paths: `server/`, `Dockerfile`, `pom.xml`, `mvnw`
- Targets: backend
- Languages: Java
- Platforms: server
- SaaS client: no
- SDK component: none
- Deployment: container with browser output

### frontend

- [x] Enabled
- Source paths: `web/`, `package.json`
- Targets: frontend, static-assets
- Languages: TypeScript, JavaScript, HTML, CSS, SCSS
- Platforms: browser
- SaaS client: yes
- SDK component: generated-clients
- Deployment: served by the Java application container

### generated-clients

- [x] Enabled
- Source paths: `api/openapi.yaml`, `api/generator-config/`, `sdks/swift/`, `sdks/typescript/`
- Targets: sdks
- Languages: Swift, TypeScript
- Platforms: Apple operating systems, browser
- SaaS client: no
- SDK component: none
- Deployment: generated libraries

### apple-client

- [x] Enabled
- Source paths: `apps/apple/`
- Targets: apps
- Languages: Swift
- Platforms: iOS, iPadOS, macOS
- SaaS client: yes
- SDK component: generated-clients
- Deployment: native application targets

### website

- [ ] Enabled
- Source paths: `website/`
- Targets: websites, static-assets
- Languages: HTML, CSS
- Platforms: browser
- SaaS client: no
- SDK component: none
- Deployment: none

### tool

- [ ] Enabled
- Source paths: `tools/`
- Targets: tools
- Languages: Go
- Platforms: local operating systems
- SaaS client: no
- SDK component: none
- Deployment: none
