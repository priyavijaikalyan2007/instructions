<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 1ad4b9c3-2864-42ef-a2fc-39bab319b12a
Created: 2026
-->

<!-- AGENT: Generic operation-script scaffolding and project readiness contract. -->

# Project scaffolding

Project initialization creates missing root operation scripts for enabled components.
The scripts contain usage, argument checks, timestamped logging, and failure examples.
They do no application work until the project implements the TODOs.
Root SETUP.md and the terminal preview identify the files that need project decisions and verified commands.
Existing script implementations and customized setup checklists remain project-owned.
Changing a profile can add missing scripts. Setup never deletes existing scripts when a target is disabled.

## Select operation scripts

| Enabled target | Root operation placeholders |
| --- | --- |
| Any application, service, extension, website, SDK, or tool | build.sh, test.sh, clean.sh |
| Backend or SaaS | run.sh, smoke.sh, deploy.sh, monitor.sh, logs.sh, migrate.sh, runsql.sh |
| Browser frontend | run.sh, smoke.sh |
| Static website | run.sh, smoke.sh, deploy.sh |
| Google Workspace or browser extension | package.sh, deploy.sh, smoke.sh |
| Native application or CLI tool | run.sh, package.sh |
| Generated SDK | package.sh |
| Documentation only | No application-operation placeholders |

Combined profiles use the union of the applicable scripts.
Root scripts act as entry points for the monolithic repository. Delegate actual work to configured component commands when appropriate.
Select components explicitly when one operation could affect several services, apps, websites, or extension hosts.
Record the actual command and output paths in project facts after implementing each operation.
Mark inapplicable operations in SETUP.md. Do not invent a database, cloud destination, or packaging tool to fill a placeholder.
A Workspace deployment can mean a prepared Apps Script upload. A browser deployment can mean release preparation for its selected channel.
Keep build, upload, test installation, and publication distinct according to the selected target guide.

## Backend environment model

| Environment | Meaning |
| --- | --- |
| test | The developer's local machine and local services |
| dev | A staging deployment used before production |
| prod | The production deployment |

Backend placeholders accept one positional environment, such as ./smoke.sh dev. The default is test.
Unknown environments and extra arguments fail before work.
These names establish a convention. Setup does not provision infrastructure, credentials, databases, or secret stores.
Record actual service, database, and runtime configuration in PROJECT.md or its configured equivalent.
Keep credentials in the project's chosen secret mechanism.
Before implementing deployment or SQL, document target validation, access controls, and recovery.
Preserve established project scripts and environment mappings until an explicit migration changes them.

## Script contract

Use Bash with strict error handling. Resolve resources from the script's location rather than the caller's working directory.
Keep four-space indentation and function braces on separate lines.
Quote expansions and use arrays for command arguments. Never execute user input through eval.
Log a UTC timestamp, level, and useful message. Exclude credentials, raw sensitive values, and command traces that expose them.
The unexpected-error handler reports the script line without printing command arguments.

Use these exit statuses:

- 0 means that help completed or implemented work succeeded.
- 1 means that an implemented operation failed.
- 2 means that usage is invalid or the operation still needs configuration.

Run a placeholder with --help to inspect its expected use.
A normal placeholder execution reports the TODO and returns 2. It must not imply a successful build, test, cleanup, or release.
Replace the TODO only after confirming the actual toolchain and component commands.
Log success after the operation and its required checks pass.
Keep clean.sh limited to verified generated outputs. Keep database and deployment operations tied to an explicit target.
Read [Shell guidance](shell/SHELL.md), [logging](LOGGING.md), and [security](SECURITY_GUIDELINES.md) when implementing scripts.

## Complete the project setup

The interview can capture users, their problem, expected value, initial scope, success criteria, and constraints.
These answers become facts in the configured PROJECT.md and the project README. Unanswered questions remain TODOs.
Keep generic instructions under instructions/. Put local refinements in the configured ADDITIONAL.md.

Complete SETUP.md and the listed project documents before declaring the setup ready.
Replace policy contacts and support commitments with decisions from the project owner.
Implement and verify selected script operations. A successful selector --check validates instruction configuration only.
Preserved custom files can contain old project identity or commands. Review the reported preserved files manually.
Selecting a license does not complete dependency attribution, policy contacts, application implementation, or release configuration.
