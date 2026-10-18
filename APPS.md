<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: a3f7737c-e2af-4dde-9200-0d7f4a48d718
Created: 2026
-->

<!-- AGENT: Target routing and extracted existing guidance for native applications. -->

# Native applications

## Target scope

Native application work includes iOS, Android, iPadOS, ChromeOS, and macOS targets.
The existing platform instructions below cover Apple applications.

## Topic references

| Work in scope | Existing guidance |
| --- | --- |
| Shared repository setup and commands | [REPO.md](./REPO.md) |
| Storage integrity | [PERSISTENCE.md](./PERSISTENCE.md) |
| Common interaction and save safety | [UI_UX.md](./UI_UX.md) |
| Selected native control behavior profiles | [UI_UX_COMPONENTS.md](./UI_UX_COMPONENTS.md) |
| Apple language and runtime rules | [SWIFT.md](./SWIFT.md) |
| Existing shared save and navigation safety | [UI_UX.md](./UI_UX.md#save-and-navigation-safety) |
| Native and server secret boundaries | [SECRET_HANDLING.md](./SECRET_HANDLING.md#native-clients-and-tools) |

## Apple platform stack

- Use Swift and the project's SwiftUI, AppKit, or UIKit targets. Share platform-independent logic without duplicating it across targets.
- Read the Xcode project and build scripts for deployment targets, SDKs, architectures, schemes, signing, and capabilities.
- Use native persistence and state restoration. A local app does not require a server, database, login, or analytics by default.
- Test platform permissions, document access, app lifecycle, accessibility, and platform-specific layouts where affected.
- Treat building, signing, archiving, uploading, submitting for review, and releasing as separate operations.
- Follow the repository's release scripts. Keep private signing material and service credentials out of source and app bundles.

## native application layout

For a repository with several native applications, use `src/<app-name>/` when a new layout is needed.
Give each application its own build, tests, and documentation.

```text
src/<app-name>/
    Shared/            Swift logic and resources shared between platform targets
    <AppName>/         macOS application entry point, views, and platform adapters
    <AppName>Mobile/   iOS/iPadOS entry point, views, and platform adapters
    <AppName>Tests/    Unit and integration tests
    <AppName>.xcodeproj/  Targets, schemes, build settings, and project membership
    Testing/           Manual regression plans and nonprivate sample data
    AppStore/          Product metadata, review notes, and media plans
    scripts/           App-specific build, archive, signing, and upload procedures
    build/             Generated artifacts, excluded from source control
src/web/               Public website, when this repository also owns one
```

For a Swift package, use `Sources/<Target>/` and `Tests/<Target>Tests/` with `Package.swift` instead of inventing an Xcode layout.
Adding a source file also requires checking target membership and resource packaging.

## Local development

For native apps, use the app-specific build modes and Xcode schemes documented by the repository.

## Apple performance guidance

For Swift apps, measure launch time, UI responsiveness, memory, and energy use. Keep blocking work off the main actor.

- Measure cold launch, document opening, scrolling, export latency, memory, and energy on supported devices.
- Use Instruments and Xcode diagnostics to investigate the measured bottleneck rather than guessing from source size.
- Keep UI changes on the main actor and expensive processing off the UI path.
- Cancel obsolete work when a user changes documents or scenes. Bound decoded-image and temporary-buffer memory.
- Release observers, timers, and security-scoped access at their owning lifecycle boundary.
- Compare simulator results with physical-device results when graphics, memory pressure, thermal limits, or signing can change behavior.

## Apple credential storage

For native macOS/iOS clients, use [Keychain services](https://developer.apple.com/documentation/security/keychain-services) for credentials and tokens the client legitimately owns.
Do not store those values in `UserDefaults`, ordinary files, source code, or logs.

## Apple application testing

Use XCTest UI tests for native application flows, accessibility, and lifecycle behavior.

Test supported deployment targets and cancellation, persistence, and state restoration where affected.

Keep shared-model tests independent of platform views. Use native UI tests for scene transitions, permission flows, and iPad layouts.

Exercise signed-device behavior separately when sandboxing, entitlements, or file access can differ from the simulator.

## Apple UI conventions

For native macOS/iOS apps, use the project's SwiftUI, AppKit, or UIKit conventions and platform-appropriate controls and keyboard shortcuts.
Use native state restoration and persistence rather than browser storage APIs.
