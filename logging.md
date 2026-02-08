
# Logging

## 1. Purpose and Mental Model

**Primary goal**
Logs must function as a **post-mortem, time-travel debugging system**. Assume that:

* The issue cannot be reproduced.
* A debugger cannot be attached.
* The incident is reported hours or days later.
* Logs are the *only* reliable source of truth.

**Design principle**
Prefer *over-logging with structure and configurability* over minimal logging. Excess verbosity must be controllable dynamically.

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

* Always support **both**:

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

  * One-way hashed
  * Deterministically masked (same input → same output)

### 7.2 Mask at the Logger Level

* Masking must be applied by:

  * Logging framework
  * Layout / formatter
* **Do not rely on developers remembering to mask manually.**

---

## 8. What Must Be Logged

### 8.1 Application Startup

* All configuration sources
* All environment variables (masked)
* Effective configuration values (masked)

### 8.2 Requests and Responses

* Log:

  * Headers (masked)
  * Payload summaries (size, counts)
  * Status codes
  * Duration
* Full payloads only at TRACE/DEBUG.

### 8.3 Queries

* Log:

  * Query type
  * Execution time
  * Result counts
  * Success/failure
* Avoid logging full result sets.

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

Below are **minimal, correct patterns** showing compliance.

---

### Go (zap + context)

```go
package main

import (
    "context"
    "log/slog"
    "os"
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
func logInfo(ctx context.Context, msg string, args ...any) {
    // Extract context
    cID, _ := ctx.Value(correlationIDKey).(string)
    tID, _ := ctx.Value(tenantIDKey).(string)
    
    // Add standard context attributes
    baseArgs := []any{
        slog.String("correlation_id", cID),
        slog.String("tenant_id", tID),
    }
    finalArgs := append(baseArgs, args...)
    
    slog.Info(msg, finalArgs...)
}

func processOrder(ctx context.Context, orderID string, amount float64) {
    // TRACE: Entry
    logInfo(ctx, "Entering processOrder", slog.String("order_id", orderID))

    // BRANCHING: Log condition data before "if"
    isHighValue := amount > 1000.0
    logInfo(ctx, "Evaluating high value check", slog.Bool("is_high_value", isHighValue))

    if isHighValue {
        logInfo(ctx, "Branch taken: High Value Protocol")
        // ... logic
    } else {
        logInfo(ctx, "Branch taken: Standard Protocol")
    }

    // EXIT
    logInfo(ctx, "Exiting processOrder")
}
```

---

### Java (SLF4J + Logback + MDC)

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

public class OrderService {
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    public void handleRequest(String userRequestID, String tenantID) {
        // CONTEXT: Setup MDC at entry point
        String correlationID = java.util.UUID.randomUUID().toString();
        MDC.put("correlation_id", correlationID);
        MDC.put("request_id", userRequestID != null ? userRequestID : generateMangledID());
        MDC.put("tenant_id", tenantID);

        try {
            logger.info("Request processing started");
            processData("sensitive_value");
        } catch (Exception e) {
            logger.error("Exception encountered", e);
        } finally {
            logger.info("Request processing finished");
            MDC.clear(); // Cleanup thread local
        }
    }

    private void processData(String input) {
        // MASKING: One-way hash for sensitive data
        String maskedInput = oneWayHash(input); 
        logger.debug("Entering processData with inputHash={}", maskedInput);
        
        // ... logic
    }

    private String generateMangledID() {
        // Reversable ID logic: Timestamp + HostIP
        return System.currentTimeMillis() + "-" + "192.168.1.1"; 
    }
    
    private String oneWayHash(String raw) {
        return Integer.toHexString(raw.hashCode()); // Simplified for example
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
import hashlib

# Context variables for async safety
correlation_id_ctx = contextvars.ContextVar("correlation_id", default="N/A")

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.correlation_id = correlation_id_ctx.get()
        return True

logging.basicConfig(format='%(asctime)s [%(correlation_id)s] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addFilter(ContextFilter())

def hash_sensitive(value):
    # SECURITY: One-way hash
    return hashlib.sha256(value.encode()).hexdigest()

def process_user_data(user_data):
    # TRACE: Entry with masked data
    safe_data = hash_sensitive(user_data['secret'])
    logger.debug(f"Entering process_user_data. SecretHash={safe_data}")

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

### TypeScript / Node.js (Pino + AsyncLocalStorage)

```ts
import { AsyncLocalStorage } from 'async_hooks';
import * as winston from 'winston';

const asyncLocalStorage = new AsyncLocalStorage<Map<string, string>>();

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(({ timestamp, level, message }) => {
      const store = asyncLocalStorage.getStore();
      const corrId = store?.get('correlationId') || 'no-context';
      const tenantId = store?.get('tenantId') || 'unknown';
      return `${timestamp} [${corrId}] [${tenantId}] ${level}: ${message}`;
    })
  ),
  transports: [new winston.transports.Console()]
});

async function sensitiveOperation(input: string) {
    // MASKING
    const hashedInput = Buffer.from(input).toString('base64'); // Simple hash example
    logger.info(`Entering sensitiveOperation. InputHash=${hashedInput}`);

    // BRANCHING
    const condition = input.length > 5;
    logger.debug(`Evaluating condition: input.length > 5 is ${condition}`);

    if (condition) {
        logger.info("Branch: Long input path");
    } else {
        logger.info("Branch: Short input path");
    }
}

// Middleware simulation
function requestHandler() {
    const store = new Map<string, string>();
    store.set('correlationId', 'uuid-1234-5678');
    store.set('tenantId', 'tenant-A');

    asyncLocalStorage.run(store, () => {
        sensitiveOperation("secretData");
    });
}

requestHandler();
```

---

## 13. Enforcement Checklist for Agents

Before delivering code, the agent **must verify**:

* [ ] Logging is configuration-driven
* [ ] Structured logs are used
* [ ] Context propagation exists
* [ ] Correlation/request IDs included
* [ ] Sensitive data masked
* [ ] Entry, exit, branches logged
* [ ] Errors always logged
* [ ] Dynamic verbosity supported

---

