<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: a1c7e3d0-5f28-4b91-9e6a-2d4f8c0b7a15
Created: 2026
-->

<!-- AGENT: Guidelines for building SDKs in multiple languages. -->

# SDK Development Guidelines

## Target scope

SDK work, including multi-language clients generated from an OpenAPI endpoint. This index links existing API-contract and language material.
Use the source layout below with the linked API contracts and language conventions.

## Topic references

| Work in scope | Existing guidance |
| --- | --- |
| Shared repository work and artifact verification | [REPO.md](../REPO.md) |
| Internal module type compatibility | [CODE_COMPLETE.md](../CODE_COMPLETE.md#direct-type-compatibility) |
| OpenAPI documentation contract | [API_GUIDELINES.md](../backend/API_GUIDELINES.md#8-documentation) |
| Resource names, request/response fields, errors, and versioning | [API_GUIDELINES.md](../backend/API_GUIDELINES.md) |
| Consumer API and artifact contracts | [DOCUMENTATION.md](../DOCUMENTATION.md#verified-facts-and-published-contracts) |
| Swift conventions | [SWIFT.md](../swift/SWIFT.md) |
| Native client behavior and lifecycle | [APPS.md](../apps/APPS.md#native-saas-clients) |
| SaaS surface composition | [SAAS.md](../saas/SAAS.md#surface-selection) |
| TypeScript conventions | [TYPESCRIPT.md](../typescript/TYPESCRIPT.md) |
| Java conventions | [JAVA.md](../java/JAVA.md) |
| C# conventions | [CSHARP.md](../csharp/CSHARP.md) |
| Go conventions | [GO.md](../go/GO.md) |
| Python conventions | [PYTHON.md](../python/PYTHON.md) |

## Recommended source layout

Use `src/sdk/<api-name>/` for clients of one API contract, including clients introduced after the service ships.
Apply the [shared folder convention](../REPO.md#folder-and-file-structure). Preserve established generator paths in existing repositories.

```text
src/sdk/<api-name>/
    generator/             Pinned generator version, options, templates, and generation scripts
    swift/                 Swift package and its component tests
    typescript/            TypeScript package and its component tests
    java/                  Java package and its component tests
    csharp/                C# package and its component tests
    go/                    Go module and its component tests
    python/                Python package and its component tests
```

Create only selected language outputs. Preserve each package's required internal source, resource, and test layout.
Keep handwritten code distinguishable from generated code within each package.
Record whether generated files are tracked or recreated by the build. Never replace their generation inputs with manual output edits.
Use one authoritative API specification, either source or verified service-generated output.
Do not maintain a separate handwritten copy of that contract per SDK language.
A release snapshot can be retained when its provenance and update process are explicit.
Keep published integrator documentation under docs/ and tests spanning the service and SDKs under root test/.
Each SDK can ship independently without moving its source directory.

## Generated native clients

Most native SaaS clients use SDKs generated from the API specification and Swagger tooling.
Use that generated client as the normal API boundary. Additional handwritten client abstractions are not required by default.
Read the configured specification, generator version, options, and output mapping before changing generation or client integration.
Use the documented generation command rather than editing generated output as a substitute for its source contract.

Select the languages of affected outputs and consumers. A Swift SDK change selects instructions/swift/SWIFT.md, not every SDK language.
Check request/response names, types, errors, and authentication integration against the actual generated contract.
A changed API contract selects affected browser and native consumers in the same repository.
Project-specific generator settings and output paths belong in PROJECT.md or referenced configuration files.
App-side sessions, credential storage, lifecycle, and error presentation remain in instructions/apps/APPS.md and the shared UI/error guides.


## Security scope

Apply [general security](../SECURITY_GUIDELINES.md) and the selected language security sections.
Select clipboard, temporary storage, sensitive memory, and tenant-isolation controls when the changed behavior uses them.
For any AI or ML feature, also apply [AIML_SECURITY.md](../AIML_SECURITY.md).
