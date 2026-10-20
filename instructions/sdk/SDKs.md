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
Existing guidance is limited to those linked contracts and conventions.

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

## Generated native clients

Most native SaaS clients use SDKs generated from the API specification and Swagger tooling.
Use that generated client as the normal API boundary. Additional handwritten client abstractions are not required by default.
Read the configured specification, generator version, options, and output mapping before changing generation or client integration.
Use the documented generation command rather than editing generated output as a substitute for its source contract.

Select the languages of affected outputs and consumers. A Swift SDK change selects instructions/swift/SWIFT.md, not every SDK language.
Check request/response names, types, errors, and authentication integration against the actual generated contract.
A changed API contract selects affected browser and native consumers in the same repository.
Project-specific generator settings and output paths belong in instructions/project/PROJECT.md or referenced configuration files.
App-side sessions, credential storage, lifecycle, and error presentation remain in instructions/apps/APPS.md and the shared UI/error guides.


## Security scope

Apply [general security](../SECURITY_GUIDELINES.md) and the selected language security sections.
Select clipboard, temporary storage, sensitive memory, and tenant-isolation controls when the changed behavior uses them.
For any AI or ML feature, also apply [AIML_SECURITY.md](../AIML_SECURITY.md).
