<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 97dc43db-679b-4b46-b73e-14a02ce82b76
Created: 2026
-->

<!-- AGENT: Human-centric error handling guidelines for constructing literate error messages. -->

# Literate Errors: Guidelines for Human-Centric Error Handling

This document establishes the standard for how coding agents and developers must construct error messages. The goal is to move away from "computer-centric" errors (stack traces, obscure codes) towards "human-centric" literate errors that empower users to understand and resolve issues.

## 1. The Core Philosophy

An error is a conversation between the system and the user. It should answer three questions:
1.  **What happened?** (in plain language)
2.  **Why did it happen?** (contextualized to the user's action)
3.  **What can I do about it?** (actionable advice)

Technical details (stack traces, error codes) must be preserved but strictly separated from the user-facing narrative.

## 2. Structure of a Literate Error

Every custom exception or error response in the system must be structured to contain two distinct layers:

### Layer A: The User Facet (Human Readable)
This layer is for the end-user. It must be safe to display in the UI.

*   **Title:** A short, non-alarming summary (e.g., "Unable to Save Document" vs "WriteFaultException").
*   **Narrative:** A full sentence explaining the situation without jargon.
    *   *Bad:* "Connection refused on port 443."
    *   *Good:* "We couldn't connect to the secure server to upload your file."
*   **Actionable Advice:** Steps the user can take to fix the problem.
    *   *Examples:* "Please check your internet connection," "Try reducing the file size below 5MB," "Contact your team admin to request edit permissions."

### Layer B: The Technical Facet (Machine Readable)
This layer is for developers and support staff. It is hidden by default in the UI.

*   **Error Code:** A unique, searchable string constant for this specific error type (e.g., `DOC_SAVE_WRITE_LOCK`, `AUTH_TOKEN_EXPIRED`).
*   **Correlation ID:** A UUID (Trace ID) linking this error to backend logs.
*   **Timestamp:** UTC timestamp of occurrence.
*   **Technical Detail:** The raw exception message, stack trace, or inner exception details.
*   **Context Data:** Key-value pairs of relevant system state (e.g., `ResourceId: 123`, `UserId: 456`, `AttemptCount: 3`).

## 3. Writing Guidelines for Agents

When throwing exceptions or returning error objects, follow these rules:

1.  **No "Computer-Speak" in User Messages:**
    *   Avoid words like: *Exception, Null, Undefined, Array, Index, String, Buffer, Stack.*
    *   Use words like: *Item, Missing, Not Found, Text, List, Limit.*

2.  **Be Specific, Not Generic:**
    *   *Bad:* "An error occurred."
    *   *Good:* "We couldn't calculate the total because the tax rate for this region is missing."

3.  **Blameless Tone:**
    *   Do not accuse the user.
    *   *Bad:* "You entered invalid data."
    *   *Good:* "The date format wasn't recognized. Please use YYYY-MM-DD."

4.  **Downstream Errors:**
    *   If a downstream service (e.g., AWS S3, SQL Server) fails, **wrap** the error.
    *   *Scenario:* SQL Deadlock.
    *   *User Message:* "The system is currently busy processing other requests. Please try saving again in a moment."
    *   *Technical Detail:* `SqlException: Transaction (Process ID 55) was deadlocked...`

## 4. Example JSON Structure

APIs should return errors in this format (extending RFC 7807 Problem Details):

```json
{
  "type": "https://docs.api.com/errors/DOC_LOCK",
  "title": "Document is Locked",
  "status": 409,
  "detail": "This document is currently being edited by another user (Jane Doe) and cannot be saved right now.",
  "suggestion": "Please wait for them to finish or ask them to close the document.",
  "technical": {
    "code": "DOC_WRITE_LOCK_COLLISION",
    "correlationId": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "timestamp": "2023-10-27T10:00:00Z",
    "lockingUserId": "user_999",
    "stackTrace": "..."
  }
}
```

## 5. Implementation in Code (C# Example)

```csharp
// Throwing a Literate Error
throw new LiterateException(
    title: "Payment Failed",
    message: "Your card was declined by the bank.",
    suggestion: "Please check your card balance or try a different payment method.",
    code: ErrorCodes.PaymentDeclined,
    innerException: ex
)
.WithContext("Last4", "4242")
.WithContext("GatewayResponse", "DoNotHonor");
```

## 6. Frontend Components (TypeScript/Javascript)
A Bootstrap 5+ compatible component for displaying literate errors has been implemented in the component library. 
Prefer to use this component over vanilla Javascript `alert` messages. For confirmation dialogs such as `Are you sure about deleting this file?`
a `confirmdialog` component has been deleted.

The entire theme library and component catalog can be referenced at `theme.priyavijai-kalyan2007.workers.dev/docs/COMPONENT_REFERENCE.md`. Prefer to use
the prebuilt components to show literate errors.
