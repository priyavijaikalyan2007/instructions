<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 29624dda-d78a-4d2f-815a-fff69a6448bb
Created: 2026
-->

<!-- AGENT: Target routing and extracted existing guidance for cli tools and plugins. -->

# CLI tools and plugins

## Target scope

Command-line tools and CLI plugins. Existing material covers the tool stack, module layouts, local commands, output, and diagnostics.

## Topic references

| Work in scope | Existing guidance |
| --- | --- |
| Shared repository setup, commands, and source verification | [REPO.md](./REPO.md) |
| Persistent local data and files | [PERSISTENCE.md](./PERSISTENCE.md) |
| Language selection for the actual tool source | [AGENTS.md](./AGENTS.md#select-language-guides) |
| Go conventions | [GO.md](./GO.md) |
| Python conventions | [PYTHON.md](./PYTHON.md) |
| Existing Rust tool conventions | [RUST.md](./RUST.md) |
| Shell scripts and BATS | [SHELL.md](./SHELL.md) |
| Credential-provider boundary | [SECRET_HANDLING.md](./SECRET_HANDLING.md#native-clients-and-tools) |

## tool stack

- Go uses its configured `go.mod` toolchain and standard module layout. Rust uses Cargo and the declared Rust edition/toolchain.
- Python uses the project's interpreter, `pyproject.toml`, environment, and dependency lock policy.
- Keep argument parsing and process setup separate from testable processing logic.
- Keep machine-readable output on stdout and diagnostics on stderr. Document exit status, cancellation, and partial-output behavior.
- Bound memory, concurrency, and file operations. Preserve user data when processing fails.
- Add network services, databases, or native UI dependencies only when the tool's requirements need them.

## tool layouts

| Purpose | Go | Rust | Python |
| --- | --- | --- | --- |
| Manifest | `go.mod`, `go.sum` | `Cargo.toml`, configured `Cargo.lock` policy | `pyproject.toml`, project lockfile |
| Entry point | `cmd/<tool>/main.go` | `src/main.rs` | `src/<package>/__main__.py` |
| Processing code | `internal/<package>/` | `src/<module>/`, exposed through `src/lib.rs` | `src/<package>/` |
| Public reusable API | Dedicated package only when needed | Deliberate library exports in `src/lib.rs` | Deliberate package exports |
| Tests | Beside code as `*_test.go` | Module tests and `tests/` integration tests | `tests/` or the established colocated convention |
| Build output | Ignored `bin/` or `build/` | Ignored `target/` | Ignored `build/`, `dist/`, and environment directories |

Keep Go type files in the appropriate existing package. Register Rust type files in their parent module and set visibility deliberately.
Do not create a package or crate for every type merely to satisfy the file rule.

## Local development

Go, Rust, and Python tools use their documented module/package commands.

## CLI output and diagnostics

For command-line tools, keep machine-readable results on stdout and diagnostics on stderr unless the command contract states otherwise.
