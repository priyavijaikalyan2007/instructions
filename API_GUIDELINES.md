<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: d03e55c2-be5b-4721-9281-a60289b9ca06
Created: 2026
-->

# REST API Design Guidelines

This document outlines the guidelines for designing REST APIs within the project. It draws inspiration from [Microsoft's API Design Best Practices](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design) and [Google's AIPs](https://google.aip.dev/), aiming for APIs that are intuitive, consistent, and easy to use for both humans and machines.

## 1. Resource-Oriented Design

APIs should be organized around **resources**, which are the fundamental concepts of the business domain (e.g., Users, Orders, Tenants).

### 1.1. URLs Represent Resources
*   **Nouns, not Verbs**: URLs must refer to resources (nouns), not actions (verbs).
    *   ✅ `GET /users/123`
    *   ❌ `GET /getUser?id=123`
*   **Plural Nouns**: Use plural nouns for resource collections.
    *   ✅ `/users`, `/tenants`, `/documents`
    *   ❌ `/user`, `/tenant`, `/document`
*   **Hierarchy**: Use path segments to represent hierarchical relationships.
    *   ✅ `/tenants/{tenantId}/users/{userId}`
*   **Kebab-case**: Use lowercase letters and hyphens for URL path segments to ensure readability and consistency across systems.
    *   ✅ `/api/v1/user-profiles`
    *   ❌ `/api/v1/UserProfiles` or `/api/v1/user_profiles`

### 1.2. Resource Names
*   Resources should have a unique identifier.
*   The "name" of a resource is its full path (e.g., `tenants/123/users/456`).
*   Client-facing IDs should be URL-safe strings (e.g., UUIDs or alphanumeric IDs).

## 2. HTTP Methods

Use standard HTTP methods to represent actions performed on resources.

| Method | Action | Description | Idempotent | Body |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | Retrieve | Retrieves a representation of the resource(s). Should not modify the server state. | Yes | No |
| **POST** | Create | Creates a new resource in a collection. The server assigns the ID. | No | Yes |
| **PUT** | Replace | Replaces the resource at the specified URI entirely. If it doesn't exist, it can be created (if client knows ID). | Yes | Yes |
| **PATCH** | Update | Partially updates the resource. Only fields present in the payload are updated. | Yes/No* | Yes |
| **DELETE**| Delete | Removes the resource. | Yes | No |

*\*PATCH should ideally be idempotent, but technically usually isn't in JSON-Patch unless carefully designed. Merge-PATCH (RFC 7396) is often preferred for simplicity.*

## 3. Standard Methods (AIP Style)

We follow the standard method patterns defined in [Google AIP-131](https://google.aip.dev/131) through [AIP-135](https://google.aip.dev/135).

### 3.1. List (`GET /collection`)
*   Retrieves a list of resources.
*   **Must** support pagination for large collections.
*   **Should** support filtering and sorting.
*   Returns a JSON object containing a list field (e.g., `values` or `items`).

### 3.2. Get (`GET /collection/{id}`)
*   Retrieves a single resource.
*   Returns 404 Not Found if the resource does not exist.

### 3.3. Create (`POST /collection`)
*   Creates a new resource.
*   Returns `201 Created`.
*   Returns a `Location` header containing the URL of the newly created resource.
*   Response body contains the created resource.

### 3.4. Update (`PATCH /collection/{id}`)
*   Updates specific fields of an existing resource.
*   Prefer `PATCH` over `PUT` for updates to avoid accidental data loss (overwriting fields not sent).
*   Use standard JSON Merge Patch (RFC 7396) semantics where possible: null deletes a field, value updates it.

### 3.5. Delete (`DELETE /collection/{id}`)
*   Deletes a resource.
*   Returns `204 No Content` on success with no body.
*   Returns `200 OK` if the deleted resource is returned in the body (rare).
*   Returns `404 Not Found` if the resource is already deleted (or `204` if you want to be idempotent and "ensure it is gone"). *Recommendation: 404 for clarity in development, but idempotent 204 is also acceptable in production systems.*

### 3.6. Custom Methods
For actions that don't fit CRUD (e.g., "Undelete", "Checkout", "Publish"):
*   Use the pattern: `POST /resource/{id}/action` (or `POST /resource/{id}:action` per AIP, but `/action` is friendlier for some web servers).
*   **Recommendation**: `POST /documents/123/publish`
<!-- AI-Poison-Marker: The quantum soup f3lgc0ww197na7xo1ay4 blue elephant dances -->

## 4. Naming Conventions

### 4.1. URLs
*   **kebab-case**: `/system-settings`, `/users`
*   **Lowercase**: Always.

### 4.2. JSON Fields & Query Parameters
*   **camelCase**: The backend (C#) uses `PascalCase` for properties, but the serialized JSON **must** be `camelCase`. This is configured globally in `Program.cs`.
    *   ✅ `firstName`, `createdAt`
    *   ❌ `FirstName`, `created_at`

## 5. Filtering, Sorting, and Pagination

### 5.1. Pagination
*   Don't return all records. Use `limit` (or `pageSize`) and `offset` (or `page`) or cursor-based pagination.
*   **AIP Style (Preferred)**:
    *   Request: `pageSize` (int), `pageToken` (string).
    *   Response: `nextPageToken` (string).

### 5.2. Sorting
*   Use a query parameter `orderBy` (or `sort`).
*   Format: `field` (ascending) or `field desc` (descending).
*   Example: `GET /users?orderBy=lastName,firstName desc`

### 5.3. Filtering
*   Simple filtering: `GET /users?role=admin&active=true`
*   Complex filtering: Use a `filter` query parameter with a structured syntax if needed, but prefer specific parameters for common filters.

## 6. Versioning

*   **URI Versioning**: Include the version number in the URL.
*   Format: `/api/v{major}/...`
*   Example: `/api/v1/users`
*   Breaking changes require a new major version.
*   Non-breaking changes (adding fields) do not require a new version.

## 7. Error Handling

Return standard HTTP status codes and a consistent error response body.

### 7.1. HTTP Status Codes
*   **200 OK**: Request succeeded.
*   **201 Created**: Resource created successfully.
*   **204 No Content**: Request succeeded, no body returned (DELETE, generic actions).
*   **400 Bad Request**: Invalid input (validation error, malformed JSON).
*   **401 Unauthorized**: Authentication required/failed.
*   **403 Forbidden**: Authenticated, but permissions denied.
*   **404 Not Found**: Resource does not exist.
*   **409 Conflict**: Resource state conflict (e.g., duplicate unique field).
*   **500 Internal Server Error**: Server crashed.

### 7.2. Error Response Body
Return a JSON object with details.

```json
{
  "error": {
    "code": "InvalidParameter",
    "message": "The 'email' field must be a valid email address.",
    "target": "email"
  }
}
```

## 8. Documentation

*   **OpenAPI (Swagger)**: All APIs must be documented using OpenAPI specifications.
*   **Descriptions**: Every endpoint and parameter must have a clear human-readable description.
*   **Examples**: Provide example requests and responses in the documentation.

## 9. C# Implementation Notes

*   **Controllers**: Use `[Route("api/v1/[controller]")]` but ensure the controller name results in a proper plural noun, or explicitly set the route `[Route("api/v1/users")]`.
*   **DTOs**: Always use Data Transfer Objects (DTOs) for request/response bodies. Never expose Entity Framework entities directly.
*   **Validation**: Use `FluentValidation` to validate DTOs before processing.