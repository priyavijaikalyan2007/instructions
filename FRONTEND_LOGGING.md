<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 539e0ee5-b59c-409f-9e11-44779a31c570
Created: 2026
-->

<!-- AGENT: Logging standards for post-mortem debugging and structured log output for frontends and frontend component libraries. -->

# Logging

## 1. Scope and Rationale

This is a **reusable theme and component library**. Components from this library are embedded into larger SaaS applications 
that may have their own logging infrastructure (Serilog, Winston, Pino, etc.). To keep things simple but flexible, this
component library ships with its own logging utility `LogUtility`. This is also a resuable component. Every other component:

1.  Has their own logging functions for `trace`, `debug`, `info`, `warn`, and `error` logging.
2.  Each component independently checks if the `LogUtility` is loaded into the `window` globals.
3.  If the `LogUtility` is loaded, the component will log via the `LogUtility`.
4.  If the `LogUtility` is NOT loaded, the component will log directly to console.

**Therefore:**, *every component MUST follow the same pattern.*

* Include the following code that sets up the logging functions appropriately

```typescript
/** Log prefix for all console messages from this component. */
const LOG_PREFIX = "[COMPONENT_NAME]";

const _lu = (typeof (window as any).createLogUtility === "function") ? (window as any).createLogUtility().getLogger(LOG_PREFIX.slice(1, -1)) : null;
function logInfo(...a: unknown[]): void { _lu ? _lu.info(...a) : console.log(new Date().toISOString(), "[INFO]", LOG_PREFIX, ...a); }
function logWarn(...a: unknown[]): void { _lu ? _lu.warn(...a) : console.warn(new Date().toISOString(), "[WARN]", LOG_PREFIX, ...a); }
function logError(...a: unknown[]): void { _lu ? _lu.error(...a) : console.error(new Date().toISOString(), "[ERROR]", LOG_PREFIX, ...a); }
function logDebug(...a: unknown[]): void { _lu ? _lu.debug(...a) : console.debug(new Date().toISOString(), "[DEBUG]", LOG_PREFIX, ...a); }
function logTrace(...a: unknown[]): void { _lu ? _lu.trace(...a) : console.debug(new Date().toISOString(), "[TRACE]", LOG_PREFIX, ...a); }
```

* **Use only `_lu` logger** abstraction for logging.
* **Do not install logging dependencies.** Do not introduce ANY other logging frameworks, wrappers, or abstractions. No Winston, Pino, log4js, or similar libraries.

The host application owns the logging pipeline. Our components simply write to the console, and the host can 
intercept or suppress console output as it sees fit.

---

## 2. Logging Methods (Level Mapping)

Use the `_lu` methods. Each maps to a severity level:

| Method | Use For | Browser DevTools |
| --------------- | ------------------------------------------- | ---------------- |
| `logTrace` | High voluem operations such as handler tracking | Verbose (hidden by default) |
| `logDebug` | Entry/exit, internal state, parameter values | Verbose (hidden by default) |
| `logInfo` | Lifecycle events, initialisation, disposal | Info |
| `logWarn` | Recoverable anomalies, fallback behaviour | Warning |
| `logError` | Failed operations, caught exceptions | Error |

**Rules:**

* Use `logTrace` for anything that would be high frequency or super noisy in normal use such as event handler tracing. 
  Browser DevTools hides debug output by default, so this is safe to leave in production builds.
* Use `logDebug` for anything that would be noisy in normal use. Browser DevTools hides debug output by default, 
  so this is safe to leave in production builds.
* Use `logInfo` sparingly for meaningful lifecycle events (component mounted, configuration applied).
* Use `logWarn` when the component recovers but the situation is unusual (missing optional parameter, deprecated usage).
* Use `logError` for genuine failures (DOM element not found, required parameter missing, API call failed).

* **Never use `console.info`.** It is functionally identical to `console.log` and adds no value. Prefer `console.log` for consistency.

---

## 3. Message Format

All messages are automatically prefixed with timestamp, level, and component name by the logging helpers.

**Output format:** `[ISO-TIMESTAMP] [LEVEL] [ComponentName] Message`

```
2026-03-30T10:15:00.000Z [INFO] [ErrorDialog] Initialised with 3 action buttons
2026-03-30T10:15:00.001Z [WARN] [ErrorDialog] No suggestion text provided; section will be hidden
2026-03-30T10:15:00.002Z [ERROR] [ErrorDialog] Target container element not found: my-container
2026-03-30T10:15:00.003Z [DEBUG] [ErrorDialog] Rendering technical details section
2026-03-30T10:15:00.004Z [TRACE] [ErrorDialog] DOM mutation: childList on .error-body
```

**In code**, use the logging helpers — never raw `console.*`:

```typescript
logInfo("Initialised with", actions.length, "action buttons");
logWarn("No suggestion text provided; section will be hidden");
logError("Target container element not found:", containerId);
logDebug("Rendering technical details section");
logTrace("DOM mutation:", { target: el, type: "childList" });
```

For messages with structured data, pass the data as a separate argument so the browser can render it as an expandable object:

```typescript
logDebug("Configuration:", { mode, actions, showTechnical });
logError("Failed to render:", error);
```

---

## 4. What to Log

### 4.1 Component Lifecycle

* Log when a component is initialised or disposed.
* Log the effective configuration after defaults are applied.

```typescript
logInfo("Initialised");
logDebug("Effective config:", resolvedOptions);
logInfo("Destroyed", instanceId);
```

### 4.2 Errors and Exceptions

* Every caught exception must be logged with `logError`.
* Include the original error object so the browser preserves the stack trace.

```typescript
try
{
    renderContent(container);
}
catch (error)
{
    logError("Failed to render content:", error);
}
```

### 4.3 Fallback Behaviour

* When a component falls back to a default because of missing or invalid input, log a warning.

```typescript
if (!options.title)
{
    logWarn("No title provided; using default 'Error'");
}
```

### 4.4 DOM Interaction Failures

* Log when an expected DOM element is not found.

```typescript
const container = document.getElementById(targetId);
if (!container)
{
    logError("Container element not found:", targetId);
    return;
}
```

### 4.5 Trace-Level Instrumentation

* Use `logTrace` for very high-frequency or low-level operations.
* Safe to leave in production — trace output is hidden by default.

```typescript
logTrace("mousedown handler fired:", { x: e.clientX, y: e.clientY });
logTrace("render cycle:", { objectCount: objects.length, frameId });
logTrace("DOM mutation:", { target: el.tagName, type: "childList" });
```

---

## 5. What NOT to Log

* **Sensitive data.** Never log tokens, passwords, API keys, or personally identifiable information (PII).
* **High-frequency events.** Do not log on every keystroke, mouse move, or scroll event. If such logging is needed during development, use `console.debug` and remove it before committing.
* **Redundant state.** Do not log values that are obvious from context (e.g., logging `true` inside an `if (isValid)` block).

---

## 6. Runtime Debug Flags

Global variables on `window` allow customer support or developers to enable verbose logging
at runtime without reloading the page:

| Flag | Effect |
|------|--------|
| `window.__ebt_debug_logging = true` | Enable DEBUG level output |
| `window.__ebt_info_logging = true` | Enable INFO level output |
| `window.__ebt_trace_logging = true` | Enable TRACE level output |

**WARN and ERROR are always enabled** — they cannot be suppressed.

Flags are checked on every log call, so toggling them in the browser console takes effect
immediately. This is useful for customer support scenarios where a customer reports a problem
and the support engineer needs to see verbose component output.

```javascript
// In the browser console:
window.__ebt_debug_logging = true;   // verbose debug output starts
window.__ebt_info_logging = true;    // informational messages appear
window.__ebt_trace_logging = true;   // ultra-verbose trace output

// Turn off when done:
window.__ebt_debug_logging = false;
```

**Studio apps and demo pages** automatically enable all flags for development convenience.

---

## 7. Production Considerations

Because we use `console.*` directly:

* **No build-time stripping is required.** `console.debug` is hidden by default in browser DevTools. `console.log` and `console.warn` provide useful runtime diagnostics for operators.
* **Host applications can suppress output** by overriding `console` methods or using DevTools filters. This is their responsibility, not ours.
* **LogUtility** is optional. If not loaded, components fall back to direct `console.*` calls with the same format. There is zero runtime overhead when LogUtility is absent.
* **Global flags** (`__ebt_*_logging`) provide runtime control without rebuilds or configuration changes — ideal for production troubleshooting.
* If a future need arises for build-time removal of debug statements, a simple Terser or ESBuild configuration in the consuming application can drop `console.debug` calls. The component library itself should not perform this stripping.

---

## 8. Reference: Full Application Logging

The guidelines above apply to **this component library only**. When building full SaaS applications that consume this library, the application itself should implement comprehensive structured logging with correlation IDs, context propagation, and log aggregation. Those concerns belong to the application, not to reusable UI components.

## 9. Enforcement Checklist for Agents

Before delivering code, the agent **must verify**:

  * [ ] Structured logs are used
  * [ ] Context propagation exists
  * [ ] All log calls use the `_lu` workaround that checks for the availability of the `logutility` component
        and redirects to `console.debug`, `console.log`, `console.warn`, or `console.error` if it is not available.
  * [ ] Correlation/request IDs are included if necessary and available.
  * [ ] No logging libraries or abstractions are imported or created except the `logutility` component.
  * [ ] All messages are prefixed with `[Timestamp] [LogLevel] [ComponentName]`
  * [ ] Errors include the original error object for stack trace preservation.
  * [ ] No sensitive data (tokens, passwords, PII) is logged.
  * [ ] High-frequency events are not logged (or use `logTrace`).
  * [ ] Entry, exit, branches logged
  * [ ] Errors always logged
  * [ ] Dynamic verbosity supported