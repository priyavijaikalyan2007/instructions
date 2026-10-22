<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 539e0ee5-b59c-409f-9e11-44779a31c570
Created: 2026
-->

<!-- AGENT: Logging standards for post-mortem debugging and structured log output for backends. -->

# Background

## Language and runtime integration

Use the application's established logging API and configuration. A reusable library must not take control of the host's logging pipeline.
Use [FRONTEND_LOGGING.md](frontend/FRONTEND_LOGGING.md) for the component logging mechanism when that guide applies.

Read the logging integration section in the selected language guide.
Service/request metadata and deployment-environment rules apply to server components that have those concepts.
Native Apple apps use Swift unified logging and local operation context. They do not invent HTTP requests or tenants for local actions.

Apps Script uses its [runtime logging guidance](apps-script/APPS_SCRIPT.md#logging) for Google-managed executions.
Do not add invented HTTP request metadata to an Editor callback.

See [TOOLS.md](tools/TOOLS.md#cli-output-and-diagnostics).
Do not add a new logging dependency when the existing API meets the requirement.

In high scale web services, logging is crucial to understand what happened when an issue occurs. 
Metrics are important to understand where something is happening and how the service is behaving.

For example, when a customer reports that their API calls are failing, we need to understand:

- Which API is failing? One, some or all?
- How is it failing? Is it failing with any of the 5xx HTTP errors in which case it is a service error. 
  Is it failing with any of the 4xx errors in which case it is a user error.
- How often is it failing? Are 100%, 50%, 10% or 5% of API calls failing?
- What are the correlated failures at the same time? E.g. are timeouts spiking which could be a 
  GC pause or data fetch latency issue. 

Logging should be comprehensive enough that a less-than-gifted high school student can read the logs, 
map the execution path to the code as deployed and understand where things failed. 
They can read the detailed logs and then understand why things failed as well. 
So, log enough information for this student to be able to wake up at 3 AM and still be able to debug production issues.

## Log Sources

Once we have identified that there is a problem and potentially where it is located based on the metrics, 
we need to look at logs to understand what is causing it. This could take many forms. 

- Application specific logs are emitted by developer of the code. 
- In other cases, logs may be need to be configured to be emitted. For example, HTTP clients will need 
  HTTP client request-response logging turned on via configuration to emit the full requests and responses. 
- Similarly, framework and library dependencies may also need a logging framework attached to emit logs appropriately. 
- In some systems such as Kubernetes, logs may need to be configured via YAML. 
- Finally, in some specific cases such as the JVM, garbage collection logs may need to be turned via JVM configuration. 

## Sensitive Data

Keep enough diagnostic context to trace an operation while controlling how each field enters the log.
Sensitive data is not one category with one transformation. Classify fields by their diagnostic purpose and disclosure risk.

| Field class | Logging treatment | Example |
| --- | --- | --- |
| Authentication and encryption secrets | Exclude the value in every environment. | Passwords, private keys, bearer tokens, session credentials. |
| Personal identifiers needed for correlation | Use a stable, scoped, one-way pseudonym under the approved policy. | Customer username or email mapped to `user_key`. |
| Personal or business content | Omit, redact, or retain only the approved summary. | Document text, payment details, message bodies. |
| Non-sensitive diagnostic data | Preserve the useful value and its meaning. | Operation name, attempt count, duration, public error code. |
| Configuration and external parameters | Log names and approved values, with field-specific transformations. | Endpoint name and timeout, with a secret value excluded. |

A customer username may be one-way hashed so operators can match events without storing the raw username.
For enumerable identifiers such as usernames and emails, prefer HMAC-SHA-256 with a protected logging key to an unkeyed hash.
The same canonical identifier, tenant, key, and algorithm version produce the same pseudonym.
An authorized diagnostic tool can compute that pseudonym to find matching events. The application must not log the lookup input.
Pseudonyms remain linkable data. Apply retention, access control, and export rules to them.

Define canonicalization explicitly before hashing. Do not merge case-sensitive accounts by blindly lowercasing their names.
Prefer a stable user identifier when renames would otherwise break correlation.
Separate tenant and environment scopes to prevent unintended correlation between customers or deployments.
Use a distinct, randomly generated logging key per environment. Environment metadata alone does not change the pseudonym.
Record a non-secret key version in event metadata. Rotation changes the resulting hash, so retain or retire lookup capability under policy.
Never log the HMAC key or reuse an authentication, encryption, or signing key for this purpose.

Transform fields before any console, file, system-log, or remote sink receives them.
A logger-level policy should enforce the transformation so application developers do not need to remember it at every call.
Post-processing alone leaves plaintext in local logs. Base64, `hashCode`, and reversible encodings do not provide one-way protection.
Use [OWASP logging guidance](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) and the project's explicit field policy.

### Correlation-safe user keys

The language guides provide helpers that implement the same contract. Put the selected helper in the project's central privacy/logging facility.
They accept a protected key and already-canonical text. They do not fetch secrets, change username semantics, or configure logging.
The payload starts with `log-user-v1` plus a zero byte, then length-prefixed tenant and username UTF-8 bytes.
Each length is an unsigned four-byte big-endian value. This encoding prevents ambiguous concatenation of fields.
The key must contain at least 32 bytes, and each input field is bounded to 1,024 UTF-8 bytes.
The result is `user-hmac-v1:` plus a lowercase hexadecimal HMAC-SHA-256 digest.
The surrounding log metadata carries the non-secret key version and environment.

Implementation examples are in the selected language guide under **Log identity helper**.

For a non-secret test key containing bytes 0 through 31, tenant `tenant-a`, and username `alice`, every helper returns:

```text
user-hmac-v1:cac1ffd631eda70d4e2e98de334d4a04dc40badb2867a5637b3eb213686cb21b
```

Test repeatability, different tenants, different keys, UTF-8 input, field-boundary ambiguity, and rejected oversized fields.
Keep real customer identifiers and real logging keys out of fixtures.

## Log Rotation

Log files can get quite large. So they must be rotated at intervals, typically every one hour. 

## Log Destinations

When logs are rewritten, logging frameworks can route them to multiple destinations for storage. 

Typically:

- For large scale, cloud based software as a service applications, this is often local files; 
  the local files are retrieved by some other system using the configured retention policy and 
  moved to a final destination. 
- For local browser based applications, the destination may be the JavaScript console. 
- For desktop applications, command line tools and scripts, it might be a local file and the terminal. 
- For system services such as the daemons and background services, it will be the system log. 

## Log Context

The log context is automatically added information that enables us to identify the surrounding environment 
for a particular log line. Typically, the context often includes:

- The log level.
- The granular timestamp.
- The thread ID. Preferably, the thread name as well for named threads.
- The logger / log source name (typically class name + method or function name)
- The host name.
- The application name.
- For software as a service, the request ID, the user ID and any trace / span / correlation IDs.

This is automatic so that the developer who is adding logs does not have to bother to add this information again. 
Most frameworks do provide this automatically and logging setup must take advantage of such configurability.

## Log Line ID

The log line ID is a technique that attaches a unique 8 or 16 digit hexadecimal code to every log line. 
The code is generated once when the log line is written and is typically globally unique. 
The code is static. This model enables a few things such as:

- Identifying when a particular log line is being logged excessively.
- Building metrics and creating dashboards for log lines that indicate warnings or errors.
- Throttling log lines when they are excessive and are not adding much value.

## Log Throttling

Sometimes, some code path can be hit at high velocity. For example, let's say there is some sort of 
immediate retry mechanism for fetching some configuration data. Let us also assume that this configuration 
data has to be fetched for each page such as static headers etc. Although an error, pages still render but 
an error log line is generated when these static header files are not present. For some reason, a recent 
deployment removed such a header file and suddenly, at scale, the logs are stuffed with thousands or 
even millions of error log lines from this missing header file. This will end up masking all other logs 
potentially leading to unknown issues. In such cases, we usually implement log throttling. 
In most cases, a buffered logger of some kind is used which does some super fast fingerprinting of the log lines 
(typically using the Log Line ID) and uses some sort of local rate counter to throttle at some configurable threshold. 

## Retention

Once emitted locally, logs may need to be offloaded to some central log storage system or pushed to storage 
such as AWS S3. This offload has to be configured separately. Elastic Beanstalk has its own configuration in the 
form of YAML. Other systems may have other configurations. 

# What to Log

Preserve execution and diagnostic detail at the appropriate level. Apply the field policy before emitting each value.
A transformed identifier is useful context, not a reason to remove the entire event.

- Log function entry and exit at TRACE or DEBUG, including the operation, relevant transformed parameters, and outcome.
- Log branch decisions and the approved values that explain them. Include a threshold or reason when it explains the branch.
- Log useful return values or bounded summaries, including whether a result is empty, partial, stale, canceled, or failed.
- Log configuration sources, key names, effective non-secret values, and the non-secret versions of applied secret configuration.
- Log dependency selection and inversion-of-control choices that explain which implementation executed.
- Log database and external-service operations with duration, affected-row or item count, retry attempt, and safe query/request metadata.
- Log user and tenant context through approved opaque identifiers or correlation-safe pseudonyms when raw values are sensitive.
- Log lifecycle actions, including initialization, configuration loading, session validation, rendering, queue operations, and disposal.
- Log handled errors with a useful cause, safe technical context, and correlation/request identifiers.
- Log cleanup, cancellation, timeout, fallback, and partial-write decisions when they change the operation's outcome.
- For CLI arguments and environment variables, preserve names and approved values. Transform identifiers and exclude credential values.
- For requests, responses, and documents, log approved fields or summaries rather than dumping unbounded or unclassified payloads.

For example, keep `operation=save_order`, `user_key=<stable HMAC>`, `attempt=2`, and `error_code=WRITE_TIMEOUT` together.
Operators can then follow the affected user and operation while the raw username remains outside the log.
Apply the same policy to exception messages and nested objects. Logging an entire exception or object must not bypass the field controls.

# Logging Instructions

## 1. Purpose and Mental Model

**Primary goal**
Logs must function as a **post-mortem, time-travel debugging system**. Assume that:

* The issue cannot be reproduced.
* A debugger cannot be attached.
* The incident is reported hours or days later.
* Logs are the *only* reliable source of truth.

**Design principle**
Prefer *over-logging with structure and configurability* over minimal logging. Excess verbosity must be controllable dynamically.

**Optimization**
Wrap all highly detailed log levels such as DEBUG/TRACE with an if check to make sure that log level is enabled. This eliminates unnecessary formatting, string conversion and log function calls.

---

## 2. Configuration Rules (Non-Negotiable)

### 2.1 Configuration-Driven Only

* **Do not hardcode logging behavior** (levels, formatters, appenders, sinks).
* Use the selected platform's logging configuration mechanism.
* Service deployments use configuration files and environment variables. Native apps and libraries follow their platform or host configuration.
* Code may only:

  * Obtain a logger
  * Emit log statements

### 2.2 Environment Separation

This deployment example applies to server components. Use the actual environment names from PROJECT.md.
Local native apps do not need staging or production service configurations merely to emit logs.

* Maintain **separate explicit configurations** for:

  * Local
  * Staging
  * Production
* Never reuse the same logging configuration across environments.

### 2.3 Output Targets

For services and local tools, support the configured console and durable collection targets.
For native Apple apps, use unified logging and an explicit support-export policy.
A component library uses the host's logger and must not create independent file or remote sinks.
Container stdout may feed durable platform collection without a local log file.

* Where the deployment requires these sinks, support both:

  * Console output (local / interactive)
  * File output (staging / production)
* File logs must be compatible with:

  * GCP Cloud Logging / AWS CloudWatch
  * Object storage offload (GCS / S3)
  * External systems (Splunk, ELK)

### 2.4 Structured Logging

* Logs **must be structured** (JSON preferred).
* Free-form text logs are unacceptable for production systems.

---

## 3. Log Levels (Strict Semantics)

| Level | Usage                                  |
| ----- | -------------------------------------- |
| TRACE | Entry/exit, branches, parameter values |
| DEBUG | Queries, request/response summaries    |
| INFO  | Business milestones, lifecycle events  |
| WARN  | Recoverable anomalies                  |
| ERROR | Failed operations, caught exceptions   |
| FATAL | Process-terminating conditions         |

Agents **must not** misuse levels.

---

## 4. Mandatory Metadata (Every Log Line)

Within request-handling services, every log entry **must contain**:

* Timestamp (UTC, ISO-8601)
* Log level
* Service name
* Environment
* Hostname
* Process ID
* Thread ID or name
* Source location (class/file + method/function)
* **Correlation ID**
* **Request ID**
* **Tenant ID** (if applicable)
* **User ID** (if applicable)

This metadata **must be injected automatically**, not manually appended in each log call.

---

## 5. Correlation, Request, Tenant, User IDs

The request/response rules below apply to service requests.
For native local work, use operation, document, scene, or task context where relevant, as described in instructions/swift/SWIFT.md.
Carry service correlation information through a generated SDK when the configured service contract provides it.

### 5.1 Correlation ID

* Generated at the **first entry point** (HTTP/gRPC/etc.).
* Constant for the entire logical operation.
* Propagated across:

  * Threads
  * Async tasks
  * External calls (via headers)

### 5.2 Request ID

* Accept customer-supplied request IDs.
* If absent:

  * Generate one.
  * Return it in the response.
* Maintain **1:1 mapping** between request ID and correlation ID.

### 5.3 Tenant and User IDs

* Always included for multi-tenant systems.
* Stored in logging context (MDC / TLS / AsyncLocal).

---

## 6. Context Propagation (Critical)

* Use framework-supported **context propagation mechanisms**:

  * ThreadLocal / MDC (Java)
  * context.Context (Go)
  * AsyncLocal (C#)
  * contextvars (Python)
  * AsyncLocalStorage (Node.js)
* Context **must flow across threads and async boundaries**.

---

## 7. Sensitive Data Handling (Mandatory)

### 7.1 Masking Rules

* Never log secrets, tokens, passwords, keys.
* Sensitive fields must be:

  * One-way pseudonymized when correlation is required, using the Sensitive Data contract above, or
  * Redacted, summarized, or excluded when the field policy requires it

### 7.2 Mask at the Logger Level

* Masking must be applied by:

  * Logging framework
  * Layout / formatter
* **Do not rely on developers remembering to mask manually.**

---

## 8. What Must Be Logged

### 8.1 Application Startup

* All configuration sources
* Relevant environment-variable names and approved transformed values
* Effective configuration values under the field policy, including non-secret key versions

### 8.2 Requests and Responses

* Log:

  * Headers (masked)
  * Payload summaries (size, counts)
  * Status codes
  * Duration
* Full payloads require explicit approval under the field policy and TRACE/DEBUG. A low log level does not authorize disclosure.

### 8.3 Queries

* Log:

  * Query type
  * Execution time
  * Result counts
  * Success/failure
* Avoid logging full result sets.

### 8.4 Application Flow

* Log before and after any significant action such as a database tranaction, API call, file action:

  * File or directory consulted or loaded.
  * Transaction status.
  * Query used in transaction.
  * API invoked.
  * API invocation result.
* Full requests, responses, queries, results, file contents, and directory listings require field-policy approval and TRACE/DEBUG.
---

## 9. Control Flow Logging (Very Important)

### 9.1 Entry and Exit

* Log function/method:

  * Entry (parameters)
  * Exit (return value)
* TRACE or DEBUG only.

### 9.2 Every Branch

* Before condition evaluation:

  * Log values used in the condition.
* When branch is taken:

  * Log which branch.
* Always log default cases in switch statements.

---

## 10. Errors and Exceptions

### 10.1 Catch and Log

* Every caught exception must be logged.
* Include:

  * Stack trace
  * Context
  * Correlation/request IDs

### 10.2 Nullable / Error-Code APIs

* Log:

  * Returned null / optional / error code
  * Caller context

### 10.3 Finally Blocks

* If language allows:

  * Log whether an exception occurred.

---

## 11. Dynamic Log Level Targeting

* Log levels **must be dynamically adjustable**:

  * Per tenant
  * Per user (if feasible)
* No redeployments required.
* Configuration must be reloadable at runtime.

---

## 12. Language-Specific Examples

The examples show API usage and context propagation. Production logger setup remains configuration-driven.
Use the correlation-safe helper for sensitive identifiers instead of logging their raw values.

---

### Go (slog + context)

See [Go](go/GO.md#logging-examples).

### Java (SLF4J + Logback + MDC)

See [Java](java/JAVA.md#logging-examples).

### C# (.NET + Serilog + AsyncLocal)

See [C#](csharp/CSHARP.md#logging-examples).

### Python (logging + contextvars)

See [Python](python/PYTHON.md#logging-examples).

### TypeScript / Node.js (Winston + AsyncLocalStorage)

See [TypeScript](typescript/TYPESCRIPT.md#logging-examples).

### Swift (OSLog + explicit operation context)

See [Swift](swift/SWIFT.md#logging-examples).

### Rust (tracing + operation spans)

See [Rust](rust/RUST.md#logging-examples).

## 13. Enforcement Checklist for Agents

Before delivering code, the agent **must verify**:

- ***For Backends, SDKs, Worker Threads and APIs***

  * [ ] Logging is configuration-driven
  * [ ] Structured logs are used
  * [ ] Context propagation exists
  * [ ] Correlation/request IDs included
  * [ ] Useful identifier correlation is preserved through approved stable pseudonyms
  * [ ] Secrets are excluded and other fields follow the explicit transformation policy
  * [ ] Entry, exit, branches logged
  * [ ] Errors always logged
  * [ ] Dynamic verbosity supported
