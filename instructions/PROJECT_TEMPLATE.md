<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 1b940f12-5763-4806-96f5-f5500b41c570
Created: 2026
-->

<!-- AGENT: Facts-only template for the consuming project. -->

# Project information template

## Identity and business context

| Fact | Value |
| --- | --- |
| Project name | `<name>` |
| Purpose | `<problem and intended outcome>` |
| Users | `<intended users>` |
| Business context | `<relevant product and business facts>` |

## Architecture and structure

| Component | Source paths | Framework or runtime | Relationships |
| --- | --- | --- | --- |
| `<component identifier>` | `<paths>` | `<configured versions>` | `<in-repository interfaces>` |

## Configured path facts

| Fact | Value |
| --- | --- |
| Service and database ownership | `<service names, database source paths, migration owner, or none>` |
| Tool-required migration paths | `<backend project paths or none>` |
| Component test locations | `<actual paths>` |
| Cross-component test locations | `<root test/ paths or existing configured paths>` |
| Editable static source | `<direct-copy source paths or none>` |
| Frontend source and output mapping | `<configured input and generated output paths or none>` |
| Generated artifact policy | `<ignored or tracked outputs and their generation commands>` |
| Established layout exceptions | `<recorded paths and decision references or none>` |

## Build and environment facts

| Component | Build command | Test command | Configuration |
| --- | --- | --- | --- |
| `<component identifier>` | `<actual command or none>` | `<actual command or none>` | `<manifest and environment names>` |

## SDK and delivery facts

| Fact | Value |
| --- | --- |
| API specification | `<source path or none>` |
| SDK generator | `<configured tool and version or none>` |
| Generator configuration | `<path or none>` |
| Generated outputs | `<paths or none>` |
| Container build and launch | `<configuration paths or none>` |
| Native targets and schemes | `<configuration paths or none>` |
| Release documentation | `<project-owned guide paths or none>` |
| Design system and component catalog | `<configured reference or none>` |

## References

| Subject | Source |
| --- | --- |
| Product requirements | `<specification paths>` |
| Architecture decisions | `<decision records>` |
| Operator information | `<project-owned references>` |
