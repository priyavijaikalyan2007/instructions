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
Use [FRONTEND_LOGGING.md](./FRONTEND_LOGGING.md) for the component logging mechanism when that guide applies.

| Language or runtime | Integration guidance |
| --- | --- |
| Swift macOS/iOS | Use the project's logging API, such as `Logger` from `OSLog`, with appropriate privacy annotations. |
| Go | Use the established logger, such as standard-library `log/slog`, and propagate request context. |
| Rust | Use the configured `tracing` or `log` facade. Let the application configure subscribers or backends. |
| Java | Use the project's logging facade or the host platform's logger. Avoid competing runtime logging backends in plugins. |
| Python | Use configured `logging` handlers and `contextvars` for operation context across async tasks. |
| C# / .NET | Use the configured `ILogger` pipeline and scopes. |
| TypeScript / JavaScript | Use the declared browser or server logger and preserve useful error context. |

For command-line tools, keep machine-readable results on stdout and diagnostics on stderr unless the command contract states otherwise.
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

The following helpers illustrate the same contract in five languages. Put the helper in the project's central privacy/logging facility.
They accept a protected key and already-canonical text. They do not fetch secrets, change username semantics, or configure logging.
The payload starts with `log-user-v1` plus a zero byte, then length-prefixed tenant and username UTF-8 bytes.
Each length is an unsigned four-byte big-endian value. This encoding prevents ambiguous concatenation of fields.
The key must contain at least 32 bytes, and each input field is bounded to 1,024 UTF-8 bytes.
The result is `user-hmac-v1:` plus a lowercase hexadecimal HMAC-SHA-256 digest.
The surrounding log metadata carries the non-secret key version and environment.

Python uses the standard library:

```python
# File: log_identity.py
import hashlib
import hmac

def user_log_key(key: bytes, tenant_id: str, canonical_username: str) -> str:
    """Returns a stable tenant-scoped pseudonym for approved log correlation."""
    if len(key) < 32:
        raise ValueError("A logging key needs at least 32 bytes.")
    payload = bytearray(b"log-user-v1\x00")
    for field in (tenant_id, canonical_username):
        encoded = field.encode("utf-8")
        if len(encoded) > 1024:
            raise ValueError("A log identity field exceeds its limit.")
        payload.extend(len(encoded).to_bytes(4, "big"))
        payload.extend(encoded)
    digest = hmac.new(key, payload, hashlib.sha256).hexdigest()
    return "user-hmac-v1:" + digest
```

Go uses the standard library and four-space indentation:

```go
// File: log_identity.go
package logidentity

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/binary"
    "encoding/hex"
    "errors"
)

// UserLogKey returns a stable tenant-scoped pseudonym for approved log correlation.
func UserLogKey(key []byte, tenantID string, canonicalUsername string) (string, error) {
    if len(key) < 32 {
        return "", errors.New("a logging key needs at least 32 bytes")
    }
    payload := []byte("log-user-v1\x00")
    for _, field := range []string{tenantID, canonicalUsername} {
        encoded := []byte(field)
        if len(encoded) > 1024 {
            return "", errors.New("a log identity field exceeds its limit")
        }
        payload = binary.BigEndian.AppendUint32(payload, uint32(len(encoded)))
        payload = append(payload, encoded...)
    }
    mac := hmac.New(sha256.New, key)
    _, _ = mac.Write(payload) // Standard hash writers do not return write errors.
    return "user-hmac-v1:" + hex.EncodeToString(mac.Sum(nil)), nil
}
```

Java uses JDK cryptography and hexadecimal utilities:

```java
// File: LogIdentity.java
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.GeneralSecurityException;
import java.util.HexFormat;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public final class LogIdentity
{
    public static String userLogKey(byte[] key, String tenantId, String canonicalUsername)
        throws GeneralSecurityException
    {
        if (key.length < 32)
        {
            throw new IllegalArgumentException("A logging key needs at least 32 bytes.");
        }
        byte[] payload = payload(tenantId, canonicalUsername);
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(new SecretKeySpec(key, "HmacSHA256"));
        return "user-hmac-v1:" + HexFormat.of().formatHex(mac.doFinal(payload));
    }

    private static byte[] payload(String tenantId, String canonicalUsername)
    {
        byte[] domain = "log-user-v1\0".getBytes(StandardCharsets.UTF_8);
        byte[] tenant = tenantId.getBytes(StandardCharsets.UTF_8);
        byte[] user = canonicalUsername.getBytes(StandardCharsets.UTF_8);
        if (tenant.length > 1024 || user.length > 1024)
        {
            throw new IllegalArgumentException("A log identity field exceeds its limit.");
        }
        return ByteBuffer.allocate(domain.length + 8 + tenant.length + user.length)
            .put(domain).putInt(tenant.length).put(tenant).putInt(user.length).put(user).array();
    }
}
```

Swift uses CryptoKit. A distributed app must not contain a shared backend logging key.
Use a protected local key for local correlation or a server-issued opaque identifier for cross-device server correlation.

```swift
// File: LogIdentity.swift
import CryptoKit
import Foundation

struct LogIdentity
{
    enum ValidationError: Error
    {
        case invalidKey
        case oversizedField
    }

    static func userLogKey(key: Data, tenantID: String, canonicalUsername: String) throws -> String
    {
        guard key.count >= 32 else
        {
            throw ValidationError.invalidKey
        }
        let payload = try identityPayload(tenantID: tenantID, canonicalUsername: canonicalUsername)
        let digest = HMAC<SHA256>.authenticationCode(for: payload, using: SymmetricKey(data: key))
        return "user-hmac-v1:" + digest.map
        {
            String(format: "%02x", $0)
        }.joined()
    }

    private static func identityPayload(tenantID: String, canonicalUsername: String) throws -> Data
    {
        var payload = Data("log-user-v1\0".utf8)
        for field in [tenantID, canonicalUsername]
        {
            let bytes = Array(field.utf8)
            guard bytes.count <= 1024 else
            {
                throw ValidationError.oversizedField
            }
            let length = UInt32(bytes.count)
            payload.append(contentsOf: [24, 16, 8, 0].map
            {
                UInt8((length >> $0) & 0xff)
            })
            payload.append(contentsOf: bytes)
        }
        return payload
    }
}
```

Rust uses the established RustCrypto implementations. These versions illustrate compatible APIs, not a universal dependency upgrade requirement:

```toml
[dependencies]
hmac = "0.13"
sha2 = "0.11"
```

```rust
// File: log_identity.rs
use hmac::{Hmac, KeyInit, Mac};
use sha2::Sha256;

/// Returns a stable tenant-scoped pseudonym for approved log correlation.
pub fn user_log_key(key: &[u8], tenant_id: &str, canonical_username: &str) -> Result<String, &'static str>
{
    if key.len() < 32
    {
        return Err("a logging key needs at least 32 bytes");
    }
    let mut mac = Hmac::<Sha256>::new_from_slice(key).map_err(|_|
    {
        "invalid logging key"
    })?;
    mac.update(b"log-user-v1\0");
    for field in [tenant_id, canonical_username]
    {
        let bytes = field.as_bytes();
        if bytes.len() > 1024
        {
            return Err("a log identity field exceeds its limit");
        }
        mac.update(&(bytes.len() as u32).to_be_bytes());
        mac.update(bytes);
    }
    let hex = mac.finalize().into_bytes().iter().map(|byte|
    {
        format!("{byte:02x}")
    }).collect::<String>();
    Ok(format!("user-hmac-v1:{hex}"))
}
```

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
* All logging behavior must be controlled via **configuration files and environment variables**.
* Code may only:

  * Obtain a logger
  * Emit log statements

### 2.2 Environment Separation

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

Every log entry **must contain**:

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

```go
package main

import (
    "context"
    "log/slog"
)

// Key for Context
type key int
const (
    correlationIDKey key = iota
    tenantIDKey
)

// Middleware to inject context
func withContext(ctx context.Context, correlationID, tenantID string) context.Context {
    ctx = context.WithValue(ctx, correlationIDKey, correlationID)
    ctx = context.WithValue(ctx, tenantIDKey, tenantID)
    return ctx
}

// Logger helper to extract context
func logAt(ctx context.Context, level slog.Level, msg string, args ...any) {
    // Extract context
    cID, _ := ctx.Value(correlationIDKey).(string)
    tID, _ := ctx.Value(tenantIDKey).(string)
    
    // Add standard context attributes
    baseArgs := []any{
        slog.String("correlation_id", cID),
        slog.String("tenant_id", tID),
    }
    finalArgs := append(baseArgs, args...)
    
    slog.Log(ctx, level, msg, finalArgs...)
}

func processOrder(ctx context.Context, orderID string, amount float64) {
    // TRACE: Entry. Configure level -8 in the application's slog handler.
    logAt(ctx, slog.Level(-8), "Entering processOrder", slog.String("order_id", orderID))

    // BRANCHING: Log condition data before "if"
    isHighValue := amount > 1000.0
    logAt(ctx, slog.LevelDebug, "Evaluating high value check", slog.Bool("is_high_value", isHighValue))

    if isHighValue {
        logAt(ctx, slog.LevelDebug, "Branch taken: High Value Protocol")
        // ... logic
    } else {
        logAt(ctx, slog.LevelDebug, "Branch taken: Standard Protocol")
    }

    // EXIT
    logAt(ctx, slog.Level(-8), "Exiting processOrder")
}
```

---

### Java (SLF4J + Logback + MDC)

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

public class OrderService
{
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    public void handleRequest(String userRequestID, String tenantID)
    {
        // CONTEXT: Setup MDC at entry point
        String correlationID = java.util.UUID.randomUUID().toString();
        MDC.put("correlation_id", correlationID);
        MDC.put("request_id", userRequestID != null ? userRequestID : generateMangledID());
        MDC.put("tenant_id", tenantID);

        try
        {
            logger.info("Request processing started");
            processData("sensitive_value");
        }
        catch (Exception e)
        {
            logger.error("Exception encountered", e);
        }
        finally
        {
            logger.info("Request processing finished");
            MDC.clear(); // Cleanup thread local
        }
    }

    private void processData(String input)
    {
        // SECURITY: Exclude the sensitive input from logs.
        logger.debug("Entering processData");
        
        // ... logic
    }

    private String generateMangledID()
    {
        return java.util.UUID.randomUUID().toString();
    }
    
}
```

---

### C# (.NET + Serilog + AsyncLocal)

```csharp
using Serilog;
using Serilog.Context;

public class PaymentService
{
    public void ProcessPayment(string tenantId, decimal amount)
    {
        // CONTEXT: Push properties to context
        using (LogContext.PushProperty("CorrelationId", Guid.NewGuid()))
        using (LogContext.PushProperty("TenantId", tenantId))
        {
            Log.Information("Entering ProcessPayment");

            // BRANCHING: Pre-calculation logging
            bool requiresAudit = amount >= 10000;
            Log.Debug("Audit Condition Evaluation: Amount={Amount}, RequiresAudit={RequiresAudit}", amount, requiresAudit);

            try 
            {
                if (requiresAudit)
                {
                    Log.Information("Branch: Audit path taken");
                    // ...
                }
            }
            catch (Exception ex)
            {
                Log.Error(ex, "Failed to process payment");
                throw; // Rethrow implies we log and bubble up
            }
            finally
            {
                // FINALLY LOGGING
                Log.Debug("Exiting ProcessPayment (In Finally Block)");
            }
        }
    }
}
```

---

### Python (logging + contextvars)

```python
import logging
import contextvars

# Context variables for async safety
correlation_id_ctx = contextvars.ContextVar("correlation_id", default="N/A")

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_ctx.get()
        return True

logging.basicConfig(format='%(asctime)s [%(correlation_id)s] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addFilter(ContextFilter())

def process_user_data(user_data):
    # SECURITY: Exclude credentials and tokens from logs.
    logger.debug("Entering process_user_data")

    try:
        # QUERY LOGGING
        query = "SELECT * FROM users WHERE id = ?"
        logger.debug(f"Executing Query: {query}")
        
        result = None # Simulate DB call
        
        if result is None:
            # NULL RETURN LOGGING
            logger.warning("Query returned NULL/Empty result")
            
    except Exception as e:
        logger.exception("Error processing user data")

# Simulating entry
correlation_id_ctx.set("abc-123-xyz")
process_user_data({"secret": "my_password"})
```

---

### TypeScript / Node.js (Winston + AsyncLocalStorage)

```ts
import { AsyncLocalStorage } from 'node:async_hooks';
import * as winston from 'winston';

const asyncLocalStorage = new AsyncLocalStorage<Map<string, string>>();
const logger = winston.createLogger(
{
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.printf(({ timestamp, level, message }) =>
        {
            const store = asyncLocalStorage.getStore();
            const correlationID = store?.get('correlationId') ?? 'no-context';
            const tenantID = store?.get('tenantId') ?? 'unknown';
            return `${timestamp} [${correlationID}] [${tenantID}] ${level}: ${message}`;
        })
    ),
    transports: [new winston.transports.Console()]
});

function sensitiveOperation(input: string): void
{
    // SECURITY: Log approved branch metadata rather than the sensitive input.
    logger.debug("Entering sensitiveOperation");
    const condition = input.length > 5;
    logger.debug(`Evaluating condition: input.length > 5 is ${condition}`);
    if (condition)
    {
        logger.debug("Branch: Long input path");
    }
    else
    {
        logger.debug("Branch: Short input path");
    }
    logger.debug("Exiting sensitiveOperation");
}

function requestHandler(): void
{
    const store = new Map<string, string>();
    store.set('correlationId', 'uuid-1234-5678');
    store.set('tenantId', 'tenant-A');
    asyncLocalStorage.run(store, () =>
    {
        sensitiveOperation("secretData");
    });
}

requestHandler();
```

---

### Swift (OSLog + explicit operation context)

Pass approved context into the operation. Use a protected local pseudonym or a server-issued identifier, not a raw username.
Mark only approved fields public. Native unified logging controls storage and collection, so do not create a duplicate plaintext sink by default.

```swift
// File: OrderDiagnostics.swift
import OSLog

struct OrderDiagnostics
{
    let logger: Logger

    func recordValidation(correlationID: String, userKey: String, quantity: Int) -> Bool
    {
        logger.debug("validation.start correlation_id=\(correlationID, privacy: .public)")
        defer
        {
            logger.debug("validation.end correlation_id=\(correlationID, privacy: .public)")
        }
        guard quantity > 0 else
        {
            logger.error("validation.failed user_key=\(userKey, privacy: .public) reason=nonpositive_quantity")
            return false
        }
        logger.info("validation.ok user_key=\(userKey, privacy: .public) quantity=\(quantity)")
        return true
    }
}
```

The application creates the logger with its configured subsystem and category.
Attach task, scene, or document identifiers when they help diagnose concurrency and lifecycle behavior.
Do not assume that a thread identifier identifies an async operation.

### Rust (tracing + operation spans)

Use the project's configured subscriber and sinks. This synchronous example enters a span and receives an already-approved user key.
For async work, instrument the future instead of holding a synchronous entered-span guard across `await`.

```rust
// File: order_diagnostics.rs
pub fn validate_quantity(correlation_id: &str, user_key: &str, quantity: i64) -> Result<i64, &'static str>
{
    let span = tracing::info_span!("validate_quantity", correlation_id, user_key);
    let _entered = span.enter();
    tracing::trace!("operation started");
    let result = if quantity > 0
    {
        tracing::debug!(quantity, "positive quantity branch");
        Ok(quantity)
    }
    else
    {
        tracing::warn!(reason = "nonpositive_quantity", "validation failed");
        Err("quantity must be positive")
    };
    tracing::trace!(success = result.is_ok(), "operation finished");
    result
}
```

The example assumes the existing `tracing` dependency. It does not install a subscriber from library code.
Keep structured fields stable so tools can filter by correlation ID, user key, operation, and failure reason.

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
