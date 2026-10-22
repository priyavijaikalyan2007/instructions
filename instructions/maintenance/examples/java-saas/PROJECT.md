<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: dc749fea-1a3f-4403-9f21-eba9d6c2f87e
Created: 2026
-->

<!-- AGENT: Facts-only description of the fictional routing scenario. -->

# Java SaaS fixture facts

## Scenario

This fixture represents one monolithic repository with a Java backend, browser frontend, generated SDKs, and Apple clients.
The backend and browser output share one application container.
The Apple targets produce separate native artifacts within the same repository.
The SDKs are generated from api/openapi.yaml using the configured generator files.

## Known and unspecified facts

| Fact | Value |
| --- | --- |
| Backend language | Java |
| Build family | Maven wrapper |
| Java web framework | unspecified |
| Database engine | unspecified |
| Browser source | TypeScript, JavaScript, HTML, CSS, SCSS |
| Native source | Swift |
| Native platforms | iOS, iPadOS, macOS |
| SDK output languages | Swift and TypeScript |
| Container definition | Dockerfile |
| Website and local tools | disabled |
| Enterprise shell and Knobby examples | not selected |
| Real source or application artifacts | not included in this instruction-routing fixture |
