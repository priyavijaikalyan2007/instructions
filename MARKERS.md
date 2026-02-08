# Agent Navigation Markers & Annotations

To accelerate agent comprehension and navigation, we utilise a standardized system of **Semantic Markers**. These markers act as high-speed indexing tags, allowing agents to understand a file's purpose, dependencies, and flow without analyzing the entire content.

## 1. The "Fast-Read" File Header

Every significant source file (Classes, Services, Controllers, Complex Components) must start with a **Structured Header Block**. This allows agents to read the first 20 lines of a file and immediately understand its context.

**Format:**
```csharp
/* 
 * ----------------------------------------------------------------------------
 * ⚓ COMPONENT: [ComponentName]
 * 📜 PURPOSE: [Concise description of what this file does]
 * 🔗 RELATES: [Reference to related files or specs, e.g., [[AuthSpec]]]
 * ⚡ FLOW: [Inbound Caller] -> [This Component] -> [Outbound Dependency]
 * 🛡️ SECURITY: [Security Role/Constraint, e.g., Requires 'Admin']
 * ----------------------------------------------------------------------------
 */
```

**Example:**
```typescript
/*
 * ----------------------------------------------------------------------------
 * ⚓ COMPONENT: UserProfileController
 * 📜 PURPOSE: Handles fetching and updating user profile settings and avatars.
 * 🔗 RELATES: [[UserProfileService]], [[AvatarUpload]]
 * ⚡ FLOW: [Router] -> [This] -> [Database]
 * 🛡️ SECURITY: Requires 'AuthenticatedUser' policy.
 * ----------------------------------------------------------------------------
 */
export class UserProfileController { ... }
```

## 2. In-Code Semantic Tags

Use these tags within comments to map logic flow and decision history.

### 2.1 Navigation Tags
*   `// @entrypoint`: Marks the start of a public API or execution flow.
*   `// @dependency: [File/Service]`: Explicitly marks a hidden or key dependency.
*   `// @maps_to: [DB_Table/Column]`: Links code entities to database schema.

### 2.2 Logic Flow Indicators
*   `// -> Dispatches: [EventName]`: Indicates an event emission.
*   `// <- Handles: [EventName]`: Indicates an event handler.
*   `// >> Delegates to: [Component]`: Indicates a hand-off of responsibility.

### 2.3 Context Anchors
*   `// ⚓ [ConceptName]`: Defines the canonical location for a business concept.
    *   *Usage:* "If you are looking for how 'Tax' is calculated, look for `⚓ TaxCalculation`."

## 3. Global Concept Registry

We use **Wiki-Style Links** `[[ConceptName]]` in comments to reference shared business logic across the stack.

*   **Syntax:** `[[Concept]]`
*   **Behavior:** Agents should search for `⚓ Concept` to find the definition.

**Example:**
```csharp
// Validates the cart items against the [[InventoryRules]].
public void ValidateCart() { ... }
```
