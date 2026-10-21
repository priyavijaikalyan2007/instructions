<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: ac1f4467-68fc-4137-a805-1f47b737a128
Created: 2026
-->

<!-- AGENT: Common security obligations and task-specific routing for every language and target. -->

# Security guidelines

Apply this guide to every component. Select the sections that match the data, runtime, and trust boundaries being changed.
Read [SECRET_HANDLING.md](SECRET_HANDLING.md) for credentials and [AIML_SECURITY.md](AIML_SECURITY.md) for every AI or ML feature.
Language-specific controls live in the selected language guide. General security requirements remain applicable when that guide omits a topic.

## Shared principles

- Identify protected data, trusted actors, external inputs, and possible misuse before implementation.
- Validate data at each trust boundary, including imported files, database content, internal APIs, and generated output.
- Deny access by default. Grant only the permissions required for the operation.
- Enforce authorization where the operation occurs. Client-side checks provide interface behavior, not access control.
- Use maintained security libraries and platform services. Do not implement custom cryptography or authentication protocols.
- Bound request size, parsing depth, decompression, concurrency, execution time, and output volume.
- Keep security dependencies and runtime versions supported. Review dependency provenance and security updates.
- Test failures and hostile inputs as well as successful operations.

Validation checks the expected format and meaning. Encoding protects a particular output context.
Sanitization removes disallowed content when the product intentionally accepts rich input.
These controls serve different purposes. A sanitized value still requires authorization and safe handling at its destination.

## Select implementation guidance

| Changed implementation | Read |
| --- | --- |
| C#/.NET and EF Core | [C# security](csharp/CSHARP.md#security) |
| Java and JVM services | [Java security](java/JAVA.md#security) |
| Swift and native Apple targets | [Swift security](swift/SWIFT.md#security) |
| Go services or tools | [Go security](go/GO.md#security) |
| Rust services or tools | [Rust security](rust/RUST.md#security) |
| Python services or tools | [Python security](python/PYTHON.md#security) |
| SQL, query builders, migrations, database roles | [SQL security](sql/SQL.md#security), [PERSISTENCE.md](PERSISTENCE.md) |
| JavaScript or TypeScript | [JavaScript security](javascript/JAVASCRIPT.md#security), [TypeScript security](typescript/TYPESCRIPT.md#security) |
| Apps Script server callbacks and Google service access | [Apps Script security](apps-script/APPS_SCRIPT.md#security), plus JavaScript security |
| HTML and browser delivery | [HTML security](html/HTML.md#security), [frontend security](frontend/FRONTEND.md#security-boundaries) |
| CSS or SCSS | [CSS security](css/CSS.md#security), [SCSS security](scss/SCSS.md#security) |
| Shell commands or scripts | [Shell security](shell/SHELL.md#security) |

## Tenant isolation

Derive tenant context from verified identity and current membership. Treat a tenant identifier supplied by the client as a request to authorize.
Require resource ownership checks for reads, writes, bulk operations, exports, and administrative actions.
Carry verified tenant context into jobs, events, search, caches, object storage, and generated downloads.
Include tenant identity in keys and authorization decisions. Clear request context before reusing pooled resources.
Separate system administration from tenant administration. Audit explicit support access and impersonation.
Apply quotas per tenant and caller so one tenant cannot consume shared capacity without limits.
Test missing context, forged identifiers, tenant switching, stale membership, and cross-tenant references.
Use the project's configured access model alongside [ACCESS_CONTROL.md](ACCESS_CONTROL.md).
These boundaries follow [OWASP tenant isolation guidance](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html).

Database policies supplement application checks. Verify isolation through the real application role, including pooled connections.
For PostgreSQL, owners normally bypass row policies. Superusers and roles with `BYPASSRLS` bypass them too.
Review `USING`, `WITH CHECK`, role grants, and any privileged functions together.
Test foreign-key and uniqueness behavior for cross-tenant relationships and unintended disclosure.
See [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

## Sensitive data lifecycle

Identify where sensitive data enters, is copied, is stored, and is removed.
Include clipboard history, temporary files, backups, caches, swap, crash dumps, logs, and third-party telemetry.
Use platform credential stores or managed secret services for credentials. Keep keys separate from encrypted content.
Use short-lived credentials where practical. Define rotation, revocation, and access auditing.
Do not place secrets in URLs, source, build artifacts, command-line arguments, or diagnostic messages.
Environment variables are a delivery mechanism, not a vault. Limit inherited exposure and diagnostic collection.
See [OWASP secret management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).

### Clipboard data

Copy sensitive data only after an explicit user action. Explain that copying can expose data to other software or synchronized devices.
Avoid background clipboard reads and clipboard logging.
Use platform expiry, local-device restrictions, and sensitive-content markers when available.
A marker or masked preview does not encrypt clipboard data or revoke another application's copy.
When clearing a clipboard, check that it still contains the content this application placed there.
Do not overwrite newer user content. Treat clearing as best effort because clipboard managers can retain copies.

UIKit offers `localOnly: true` to prevent Handoff sharing and `expirationDate` to expire pasteboard items.
These options do not make the clipboard private to the application.
See [Apple pasteboard options](https://developer.apple.com/documentation/uikit/uipasteboard/setobjects(_:localonly:expirationdate:)-3h3iz).
Android's `EXTRA_IS_SENSITIVE` marks a sensitive preview. It does not add access protection to the clipboard data.
See [Android ClipDescription](https://developer.android.com/reference/android/content/ClipDescription#EXTRA_IS_SENSITIVE).
Other platforms require their own supported controls. Do not assume UIKit behavior on macOS or browser clipboards.

### Temporary files and caches

Prefer streaming when temporary persistence is unnecessary.
If a temporary file is required, create it atomically through the platform's secure temporary-file API.
Use an application-controlled directory and restrictive permissions from creation, before writing sensitive bytes.
Do not construct a predictable name and then open it. Avoid symlink and path-substitution races.
Use private directories, exclusive creation, and descriptor-based operations where supported.
Bound file size and lifetime. Clean up on success, cancellation, failure, and application restart.
Do not put plaintext credentials in temporary filenames or shared caches.
For sensitive content, use approved encrypted storage and exclude unnecessary backup or synchronization copies.
Deleting a file does not guarantee erasure from snapshots, journals, flash storage, or backups.
For example, Python's [tempfile APIs](https://docs.python.org/3/library/tempfile.html) provide secure creation and cleanup mechanisms.

### Memory, swap, and crash dumps

Keep plaintext lifetimes short and avoid unnecessary copies. Use controlled mutable buffers when the API permits them.
Clear owned buffers through a documented secure-zeroing primitive before reuse or release.
A variable assignment, garbage collection, disposal, or ordinary memory clearing does not prove that all copies were erased.
Serialization, immutable strings, registers, framework buffers, and garbage collectors can retain additional copies.

Where required by the threat model, use bounded locked allocations through a maintained native library.
Check lock failures and platform limits. Choose an explicit failure policy when locking is required.
Exclude sensitive allocations from dumps where supported. Configure crash collection to avoid secret-bearing process memory.
Libsodium provides guarded allocations, locking, zeroing, and supported dump-exclusion controls.
Its documentation explains limits and possible failures. See [secure memory](https://doc.libsodium.org/memory_management).
On Windows, [VirtualLock](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtuallock)
prevents successfully locked pages from being written to the pagefile while locked.
This does not protect other copies, hibernation images, or data already written elsewhere.

On Linux, `mlock` keeps successfully locked pages resident until unlocked.
`madvise(..., MADV_DONTDUMP)` excludes the selected range from core dumps. It does not prevent swapping.
Keep sensitive native allocations page-aligned where the API requires it and check every return value.
See [mlock](https://man7.org/linux/man-pages/man2/mlock.2.html) and [madvise](https://man7.org/linux/man-pages/man2/madvise.2.html).

Memory pinning prevents relocation. It does not imply page locking, encryption, or exclusion from dumps.
There is no portable annotation that makes an arbitrary managed object secret or unswappable.
Use documented APIs for the actual platform. Record unsupported protections and residual exposure.
Do not claim resistance to a compromised operating system or privileged debugger.

Confirm swap, pagefile, hibernation, and dump policies in the deployment environment.
Use approved encryption for persistent system storage, including swap where supported.
Do not change host-wide swap or dump settings automatically. Record required configuration as deployment facts.
Containers share host memory facilities. A container alone does not prove that its memory never reaches disk.
Linux `tmpfs` can use swap. See the [kernel tmpfs documentation](https://www.kernel.org/doc/html/latest/filesystems/tmpfs.html).

### Logs and diagnostic correlation

Follow [LOGGING.md](LOGGING.md) for useful, bounded diagnostic events.
Retain authorized correlation data without exposing raw passwords, tokens, keys, or unrestricted payloads.
Use an approved stable pseudonym when matching a customer across events is necessary.
For guessable identifiers, prefer a keyed hash over a plain unsalted hash.
Scope keys and retention to the required correlation domain. Restrict access to keys and logs.
Pseudonyms remain sensitive identifiers. Hashing does not make records anonymous.
Avoid logging clipboard contents, decrypted buffers, full prompts, or raw exception objects that can contain secrets.

## Services, browsers, and infrastructure

Use the configured identity framework and current authentication policies. Require secure transport for sensitive exchanges.
Protect cookie-authenticated state changes against cross-site request forgery. Restrict origins and credentialed cross-origin access.
Use explicit request models to prevent mass assignment. Return only fields authorized for the caller.
Configure browser headers at the serving layer. Match Content Security Policy and framing policy to required integrations.
See [frontend security](frontend/FRONTEND.md#security-boundaries) for browser sinks and delivery controls.

For server-side URL fetching, constrain destinations and permitted schemes.
Validate resolved addresses, including IPv6 and metadata services, at connection time through an appropriate network control.
Disable automatic redirects or revalidate each destination. Address DNS rebinding and alternate address representations.
An `http` or `https` prefix alone does not make a destination safe.
Use network egress restrictions where application checks cannot enforce the boundary reliably.
See [OWASP SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).

Keep object storage private by default. Separate service credentials from deployment and migration privileges.
Protect infrastructure state and build logs because they can contain secrets.
Run containers with the required privileges only. Limit mounts, writable paths, capabilities, and resource consumption.
Treat application authorization as necessary even when infrastructure is isolated.

## Verification

- Test authorization through actual endpoints and database roles, including cross-tenant negative cases.
- Test injection attempts at SQL, HTML, shell, file, deserialization, and model-output boundaries.
- Verify temporary-file permissions, cancellation cleanup, and startup recovery.
- Verify clipboard expiry and replacement behavior on each supported platform.
- Exercise unavailable memory controls, lock failures, and production crash-report configuration.
- Inspect logs and artifacts for secrets while preserving required diagnostic correlation.
- Record which guarantees were tested, which depend on deployment, and which the runtime cannot provide.
