<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: ec85a879-dc11-40ca-9fc1-f1bcb7df4053
Created: 2026
-->

<!-- AGENT: Additional security controls for all AI and ML features, including models, retrieval, and tools. -->

# AI and ML security

Read this guide whenever a task adds or changes an AI or ML feature.
Apply [general security](SECURITY_GUIDELINES.md), [secret handling](SECRET_HANDLING.md), and the selected language guides as well.
Use [LLM_TECHNIQUES.md](LLM_TECHNIQUES.md) and [NON_LLM_AIML_TECHNIQUES.md](NON_LLM_AIML_TECHNIQUES.md) to select an approach.
These controls apply to local models, external providers, browser integrations, native clients, services, and tools.
A model's output is untrusted input to the rest of the application.

## Define the actual exposure

Record model providers, versions, data classes, retention, trust boundaries, and enabled tools in project facts.
Keep project-specific endpoints, limits, findings, and remediation paths in project records.
Do not copy another project's endpoint counts, vulnerability locations, or fixed quotas into generic policy.

Evaluate each applicable category from the [OWASP LLM Top 10 (2025)](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/).
Record a reason when a category does not apply. Revisit that decision when features change.

| Risk | Review question |
| --- | --- |
| Prompt injection | Can supplied or retrieved content change the requested operation? |
| Sensitive information disclosure | Can outputs, traces, or provider requests reveal protected information? |
| Supply chain | Can model artifacts, dependencies, prompts, or remote code change without review? |
| Data and model poisoning | Can untrusted examples or feedback influence training or retrieval? |
| Improper output handling | Can generated content reach an executable or privileged destination? |
| Excessive agency | Can the model perform actions beyond the caller's authority? |
| System prompt leakage | Does the design depend on prompts remaining confidential? |
| Vector and embedding weaknesses | Can retrieval expose another user's data or accept poisoned content? |
| Misinformation | Can unsupported output cause a consequential decision or action? |
| Unbounded consumption | Can requests exhaust tokens, time, storage, memory, or money? |

## Input segregation and sanitization

Keep application instructions separate from user requests and untrusted content through supported message roles or typed fields.
Treat retrieved documents, tool responses, images, OCR text, audio transcripts, metadata, and conversation history as untrusted content.
Do not promote a role or tool identity supplied by a client into a trusted system message.
Validate roles and reconstruct history from authorized server-side records where available.
If using delimiters, encode delimiter characters and label content provenance. Delimiters help structure a prompt but cannot enforce authority.

A fixed prefix, repeated warning, keyword filter, or model safety judgment cannot guarantee protection from prompt injection.
Do not store credentials or rely on secret authorization rules inside system prompts.
Enforce permissions, destinations, and tool limits outside the model.
Test direct injection, retrieved-content injection, encoded payloads, and multilingual variants.
See [OWASP prompt injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).

### Boundary validation

- Validate the expected request shape before constructing the model request.
- Bound text bytes, tokens, attachments, image dimensions, audio duration, and parsed structure size.
- Bound individual history turns and total history. Include retrieved context in the total budget.
- Reject unsupported roles, output formats, encodings, and tool names.
- Normalize text only when the input contract permits it. Preserve meaningful whitespace and international text.
- Reject or escape disallowed control characters for the destination instead of silently changing all user content.
- Use sanitization appropriate to the output sink. HTML sanitization is not a defense against prompt injection.
- Treat filtering as one signal. Record false positives and bypasses without storing unrestricted sensitive payloads.

The following C# fragment illustrates a configured limit. The hosting application owns the value and validation response.

```csharp
// SECURITY: Reject invalid requests before sending data to a provider.
if (string.IsNullOrWhiteSpace(request.Command) || request.Command.Length > limits.MaxCommandCharacters)
{
    return this.BadRequest(new { error = "Enter a command within the displayed length limit." });
}
```

For structured inputs, bound object counts, nesting, references, and aggregate size before expensive analysis.
For example, a graph requires limits for nodes, edges, labels, and valid endpoint references.
Keep these values in the project's validated configuration or named constants. Explain limits in the interface.

### User customization

Keep privileged instructions application-controlled. Offer approved templates or bounded user preferences when customization is required.
Treat free-form preferences as untrusted requests. They cannot change permissions, tool scope, or data-access policy.
A user preference must not replace the application's system role.
A generated summary of prior conversation remains untrusted. It does not gain authority because the application stored it.

## Provider and data boundaries

Send only data needed for the task and permitted for the configured provider.
Check retention, training use, region, subprocessors, and deletion requirements against the project's data policy.
Use the provider's supported credential header or authentication mechanism. Keep credentials out of URLs and prompts.
Store provider credentials through [SECRET_HANDLING.md](SECRET_HANDLING.md).
Do not embed service-wide credentials in native clients, websites, or distributed tools.
Use the authorized backend or a documented delegated access flow when shared credentials are required.

Redact or pseudonymize personal data when the operation does not require its identity.
Do not remove necessary authorized identifiers solely because they match an email or phone-number pattern.
Apply the actual data policy to both inputs and outputs. Pattern scanners can miss secrets and flag legitimate content.

Scope conversations, retrieval, embeddings, caches, files, and audit records to the caller and authorized tenant.
Authorize documents before they enter a model context. Post-generation filtering cannot undo disclosure to the provider.
Recheck membership when accessing retained conversations or retrieval results.
Test cache collisions, cross-tenant identifiers, stale permissions, and deletion of retained data.
Use the isolation rules in [SECURITY_GUIDELINES.md](SECURITY_GUIDELINES.md#tenant-isolation).

Local inference does not remove storage risks. Include model caches, prompts, temporary files, swap, and diagnostic dumps in the data lifecycle.
Use the [sensitive-data controls](SECURITY_GUIDELINES.md#sensitive-data-lifecycle) for these copies.

## Resource limits and cost controls

Apply request limits before model execution. Enforce caller, tenant, and shared-service limits where those identities exist.
Use validated identity rather than a freely supplied user identifier as the limiter key.
Coordinate limits across replicas when a process-local limiter cannot enforce the service budget.

| Resource | Required control |
| --- | --- |
| Request data | Byte, token, attachment, and structure limits |
| Generation | Maximum output tokens, wall time, and streaming bytes |
| Conversation | Maximum turns and aggregate context |
| Tools | Maximum calls, depth, concurrency, and execution time |
| Retries | Bounded count, backoff, cancellation, and total budget |
| Cost | Per-operation and aggregate allowance, accounting, and alerting |
| Local models | Memory, accelerator capacity, queue length, and concurrent work |

Reject invalid or excessive client limits. Cap valid requested limits at the configured server maximum.
Do not truncate security instructions or discard authorization context to fit a token budget.
Stop downstream work on cancellation when supported. Document provider billing and cancellation limits.
Record token use and duration without retaining full prompt content by default.
Thresholds are project settings, not universal numbers copied from examples.

For C# services, use the configured ASP.NET Core rate-limiting middleware and appropriate distributed enforcement.
For other services, use the configured runtime's equivalent controls. A native client limit supplements server enforcement.

## Output validation

### Structured output

Request a defined output schema when the provider supports it. Validate the result independently before use.
Parse the complete response through a strict parser. Do not extract arbitrary braces through a regular expression.
Reject malformed, truncated, extra, or mismatched content. Bound parser input size and depth.
Validate required fields, exact types, allowed values, numeric ranges, and relationships.
Check referenced resources through application authorization before acting on them.
Do not replace an invalid value with a plausible value that silently changes the result's meaning.

The following C# fragment illustrates a bounded classification response using `System.Text.Json`.
The host must cap response bytes before parsing. `JsonDocument.Parse` validates syntax, not the application's full schema.

```csharp
// SECURITY: Accept exactly the documented shape. Return a controlled validation failure to the caller.
using var document = JsonDocument.Parse(aiResponse, new JsonDocumentOptions { MaxDepth = 4 });
var root = document.RootElement;
if (root.ValueKind != JsonValueKind.Object || root.EnumerateObject().Count() != 2)
{
    throw new JsonException("Unexpected classification shape.");
}

if (!root.TryGetProperty("label", out var label) || label.ValueKind != JsonValueKind.String ||
    !allowedLabels.Contains(label.GetString()!) ||
    !root.TryGetProperty("confidence", out var confidence) ||
    confidence.ValueKind != JsonValueKind.Number || !confidence.TryGetDouble(out var score) ||
    !double.IsFinite(score) || score < 0 || score > 1)
{
    throw new JsonException("Invalid classification fields.");
}
```

This exact two-field check rejects additional and duplicate properties as well as missing fields.
For larger contracts, use a maintained schema validator configured to reject unknown fields and duplicate names.
Test valid responses, missing fields, duplicates, unexpected fields, non-finite or out-of-range numbers, and trailing content.
Use equivalent validation in Java, Swift, Python, Go, Rust, and TypeScript rather than adding a C# runtime dependency.

### Browser rendering and exports

Treat generated markup, Markdown, links, and files as untrusted content.
Use `textContent` for plain text. For intentional rich HTML, sanitize the final rendered HTML with a maintained allowlist-based sanitizer.
Validate link schemes and destinations. Restrict embedded content and event handlers.
Apply the same controls to previews, exports, downloaded reports, and native web views.
See [JavaScript security](javascript/JAVASCRIPT.md#security) and [HTML security](html/HTML.md#security).

```typescript
// SECURITY: Display generated text without interpreting markup.
resultElement.textContent = modelResponse.text;

// Unsafe: do not insert modelResponse.text directly through innerHTML.
```

### Refusals and incomplete results

Use the provider's documented status, refusal, and completion fields where available.
Handle refusals, safety blocks, partial streams, timeouts, and malformed responses as distinct controlled outcomes.
English phrases such as "I cannot" are not a reliable classifier across languages or providers.
Do not treat a refusal detector as an authorization control.
Keep incomplete output from triggering an operation. Explain whether retrying or changing input can help.

### Tools and generated code

Allow only tools and arguments approved for the operation. Authorize each execution independently of the model's request.
Validate targets, paths, recipients, and network destinations immediately before use.
For consequential actions, use the product's required confirmation flow and bind approval to the exact proposed action.
Do not let the model reinterpret an approval as permission for a different action.

Run generated code only in the approved isolated execution environment.
Restrict filesystem access, network egress, credentials, runtime, and resource budgets.
A container with privileged access or host mounts is not an adequate isolation claim.
Reauthorize tool results before exposing them to the caller.
Treat tool descriptions, responses, and persistent agent memory as untrusted inputs.
See [OWASP AI agent security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html).

## Model and data integrity

Track model and dataset provenance, licenses, versions, hashes, and approved sources.
Verify artifacts before loading them. Do not enable remote model code or unsafe deserialization merely to load a downloaded model.
Separate untrusted feedback from approved training examples. Review transformations and data-source access.
Protect training, validation, and evaluation datasets from unauthorized changes and overlap that invalidates evaluation.
Evaluate poisoning, evasion, privacy leakage, and model extraction where the feature exposes those risks.
Apply access controls and query budgets to embeddings and model endpoints.
Record uncertainty and test decisions using representative inputs, including adversarial cases.
See [NIST adversarial machine learning taxonomy](https://csrc.nist.gov/pubs/ai/100/2/e2025/final).

## Errors, monitoring, and verification

Return useful error codes and recovery steps through [LITERATE_ERRORS.md](LITERATE_ERRORS.md).
Do not return raw provider exceptions, stack traces, prompts, or credentials.
Expose configuration problems only to callers authorized to change that configuration.
Log sanitized operational details through [LOGGING.md](LOGGING.md), using correlation identifiers when necessary.

Monitor request counts, latency, cost, token use, validation failures, refusals, rate-limit events, and provider failures.
Select thresholds from workload evidence. A refusal spike can indicate abuse, a policy change, or a provider regression.
Restrict diagnostic payload access and retention. Do not log every prompt or response by default.

Before release or a model, prompt, retrieval, or tool-policy change:

- Test direct and indirect injection through each supported input channel.
- Test tenant isolation, revoked access, and unauthorized tool requests.
- Test schema rejection, safe rendering, malformed files, and unsupported output links.
- Test timeouts, retries, cancellation, budget exhaustion, and partial streams.
- Test privacy controls on provider requests, caches, logs, temporary storage, and artifacts.
- Compare useful task results and safety failures using a versioned evaluation set.

Model self-review and safety classifiers can supplement these tests. They do not replace deterministic access checks or isolation.
Snapshot tests detect prompt changes. They do not prove that a model will follow the prompt.
Use current APIs from the configured AI framework and validator. Verify hooks and guarantees against the installed version.
