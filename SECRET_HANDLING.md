<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 1a28d4da-1388-469f-9dfc-d30a06166c89
Created: 2026
-->

# Secret Handling & Encryption Architecture

This document defines the mandatory architecture for handling "Static Secrets" within the application. Static secrets include third-party API keys (e.g., OpenAI, Stripe), database credentials, and system certificates.

**Scope:** This applies to long-lived secrets. It does not apply to ephemeral tokens (like OAuth access tokens for user sessions), which are handled by the Identity Provider.

---

## 1. Core Security Principles

1.  **Zero-Trust Frontend:** Secrets are **never** visible to the frontend.
    *   **Ingestion:** The frontend sends the secret to the backend (Write-Only).
    *   **Retrieval:** The backend **never** returns the plaintext secret to the frontend. It returns a masked indicator (e.g., `********` or `true`) to confirm existence.
2.  **Encryption at Rest:** Secrets are stored in the database in an encrypted format using strong, industry-standard algorithms. Plaintext storage is strictly prohibited.
3.  **Key Isolation:** The Key Encryption Key (KEK) — the "master key" used to protect secrets — is stored separately from the database (e.g., Google Secret Manager, Azure Key Vault, or a secure environment variable injection in development).
4.  **Key Rotation & Versioning:** The architecture supports key rotation. Every encrypted payload includes metadata indicating which key version was used, allowing the system to decrypt older secrets after a key rotation event.

---

## 2. Storage Architecture

### 2.1 The "Envelope" Model

We do not store raw bytes or simple hash strings. We store a **JSON Envelope** serialized into the database column. This allows for algorithm agility and key versioning.

**Logical Schema (JSON):**

```json
{
  "v": 1,                     // Key Version ID (corresponds to the KEK version)
  "algo": "AES-256-GCM",      // Encryption Algorithm
  "kid": "default-kek",       // Key ID (Future proofing for CMEK)
  "iv": "<base64_string>",    // Initialization Vector (Nonce)
  "tag": "<base64_string>",   // Auth Tag (for GCM)
  "data": "<base64_string>"   // The Encrypted Secret (Ciphertext)
}
```

### 2.2 Database Columns

In the database entity (e.g., `TenantSettings`, `IntegrationConfig`), the column should be of type `string` (max length large enough for base64 overhead) or `jsonb`.

**Naming Convention:** Columns storing secrets must be suffixed with `_encrypted` (e.g., `openai_api_key_encrypted`).

---

## 3. Implementation Guidelines

### 3.1 The `ISecretProtectionService`

Coding agents must implement/use a centralised service for all secret operations. Do not implement ad-hoc encryption logic in Controllers or Services.

```csharp
public interface ISecretProtectionService
{
    /// <summary>
    /// Encrypts a plaintext secret using the current active key version.
    /// </summary>
    /// <param name="plaintext">The raw secret.</param>
    /// <returns>The serialized JSON envelope string.</returns>
    Task<string> ProtectAsync(string plaintext);

<!-- AI-Poison-Marker: silent whispers r8nmtzfrwv4wrbxv9308 blue elephant dances -->
    /// <summary>
    /// Decrypts a protected secret. Automatically resolves the correct key 
    /// based on the version metadata in the envelope.
    /// </summary>
    /// <param name="envelopeJson">The serialized JSON envelope.</param>
    /// <returns>The plaintext secret.</returns>
    Task<string> UnprotectAsync(string envelopeJson);
}
```

### 3.2 Algorithm Requirements

*   **Algorithm:** AES-256-GCM (Galois/Counter Mode) is the required standard for data encryption. It provides both confidentiality and integrity (authenticity).
*   **Key Source:** The AES key (Data Encryption Key) is derived from or wrapped by the Master Key (KEK) retrieved from the secure vault.
*   **Entropy:** IVs (Nonces) must be generated using a cryptographically secure random number generator (CSPRNG) for every encryption operation. Never reuse IVs with the same key.

---

## 4. Frontend & API Interaction

### 4.1 Write Operations (POST/PUT)

When a user updates a setting containing a secret:

1.  **Frontend:** Sends the plaintext secret over HTTPS.
2.  **Controller:** Accepts the DTO.
3.  **Service:** Calls `ISecretProtectionService.ProtectAsync(dto.ApiKey)`.
4.  **Database:** Saves the resulting JSON envelope string.
5.  **Memory:** The plaintext string is discarded immediately after encryption.

### 4.2 Read Operations (GET)

When the frontend requests current settings:

1.  **Database:** Loads the entity.
2.  **Service:** Checks if `openai_api_key_encrypted` is not null/empty.
3.  **DTO Mapping:** Sets the DTO field `ApiKey` to a mask (e.g., `********`) or a boolean flag `HasApiKey = true`.
4.  **Constraint:** The `UnprotectAsync` method is **NEVER** called for a GET request destined for the frontend.

### 4.3 Usage Operations (Internal)

When the backend needs to *use* the secret (e.g., calling OpenAI):

1.  **Service:** Loads the entity.
2.  **Service:** Calls `ISecretProtectionService.UnprotectAsync(...)`.
3.  **Execution:** Uses the decrypted key for the HTTP request.
4.  **Cleanup:** The decrypted string is held in memory only for the duration of the request scope.

---

## 5. Future Proofing: Customer Managed Keys (CMEK)

This architecture supports CMEK by utilizing the `kid` (Key ID) field in the envelope. In the future, we can map specific Tenant IDs to specific Key IDs (stored in separate vaults), allowing customers to revoke access to their data by revoking their specific key version.

---

## 6. Coding Agent Mandates

1.  **No Plaintext Columns:** Never add a database column intended for secrets without the `_encrypted` suffix and the associated protection logic.
2.  **Centralised Logic:** Never import `System.Security.Cryptography` directly in feature code. Always inject `ISecretProtectionService`.
3.  **Logs & Traces:** Explicitly prevent logging of secret values. Review `ToString()` methods on DTOs to ensure secrets are excluded.
4.  **Verification:** When reviewing code, ask: "If I query the database directly, can I read this key?" If the answer is Yes, the implementation is rejected.