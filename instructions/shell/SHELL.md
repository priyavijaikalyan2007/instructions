<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 843af16f-5748-4962-b56a-ad994310f7d8
Created: 2026
-->

<!-- AGENT: Shell conventions and task examples; load only when this language is in scope. -->

# Shell instructions

Read this guide when the task changes Shell source or its language-specific build and test configuration.
Examples in instruction documents do not make a language part of the consuming project.
Start with references, formatting, naming, and file organization when those sections exist.
Read task sections as needed. Read pattern examples only for patterns selected during planning.
Shared policies remain in the topic guides. Read only the topics that apply to the task.
Do not weaken a shared requirement because this guide omits it.

Shared rules: [Style](../CODING_STYLE.md), [Comments](../COMMENTING.md), [Markers](../MARKERS.md), [Testing](../TESTING.md), [Logging](../LOGGING.md), [Performance](../PERFORMANCE.md), [Patterns](../GOF_PATTERNS.md).

Apply [shared style](../CODING_STYLE.md), including Allman braces, four-space indentation, and one type per file.
Use only the grammar exceptions stated in this guide.
If an example shows several top-level types, put each type in its own file in production.
Examples may omit surrounding project types or test fixtures. Use the repository's configured dependencies and contracts.

Read by task: [Construction](#construction), [Testing](#testing).

## Construction

Use the interpreter declared by the script and the consuming repository's build conventions.
Shell control flow uses its own keywords. Do not insert C-style control-flow braces.
The BATS examples below require the BATS runner rather than a plain Bash invocation.

## Testing

Test shell scripts using BATS (Bash Automated Testing System):

```bash
#!/usr/bin/env bats

@test "backup script creates timestamped file" {
    run ./backup.sh /tmp/test-data
    [ "$status" -eq 0 ]
    [ -f "/tmp/backups/test-data-$(date +%Y%m%d).tar.gz" ]
}

@test "backup script fails gracefully for missing directory" {
    run ./backup.sh /nonexistent/path
    [ "$status" -eq 1 ]
    [[ "$output" == *"Directory not found"* ]]
}
```


## Security

Apply [general security](../SECURITY_GUIDELINES.md), especially process arguments, temporary files, and diagnostic exposure.
Quote variable expansions and use arrays for argument lists where the shell supports them.
Do not use `eval`, `source`, or command substitution to execute untrusted text.
Validate executable paths and flags. Use `--` to end options when the command supports it.
Disable command tracing around credentials. Keep secrets out of shell history and process arguments.
Create temporary files atomically through the platform's `mktemp`, with a restrictive umask and cleanup trap.
Verify portability before using flags. Cleanup traps do not run after every termination or power failure.
Never delete a derived path unless its ownership and expected scope are established.
