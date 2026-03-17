<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: f4e8d329-8ea6-475b-9fbc-3a561bfccd1a
Created: 2026
-->

# Linguistic Constraint Verification (LCV) Design

## 1. Objective
The Linguistic Constraint Verification (LCV) system aims to bridge the gap between high-level architectural requirements (expressed in quasi-natural language) and code-level enforcement. It provides a formal but readable way to specify, verify, and enforce coding behaviors, particularly for C# applications, to prevent common bugs, security flaws, and data loss.

## 2. The LCV Workflow
1.  **Specification**: Architect defines constraints in `agentknowledge/lcv_constraints.yaml` using a Controlled Natural Language (CNL).
2.  **Modeling**: The LCV engine translates these constraints into an internal Verification Model (Ruleset).
3.  **Enforcement**: 
    *   **Static Analysis**: Integrated into the build process via custom Roslyn analyzers or linting rules.
    *   **Architectural Tests**: Generated C# unit tests (using libraries like `NetArchTest`) that fail the build if constraints are violated.
    *   **Runtime Assertions**: (Optional) Generated guard clauses for critical data-integrity constraints.

## 3. Constraint Specification Format (YAML)

Constraints are defined in a structured YAML format that remains readable to humans.

```yaml
- id: "LCV-001"
  description: "Every API call must enforce authorization for entity access."
  quasi_nl: "In 'Controllers', every 'Method' with 'Http' attribute MUST have 'Authorize' attribute AND MUST call 'AuthorizationService.CheckPermission'."
  target: 
    namespace: "App.Web.Controllers"
    type: "Method"
  rules:
    - attribute_required: "AuthorizeAttribute"
    - call_required: "AuthorizationService.CheckPermission"
  severity: "Critical"

- id: "LCV-002"
  description: "Ensure nullable values use Optional<T> for returns."
  quasi_nl: "In 'Services', every 'Method' that returns a nullable type MUST return 'Optional<T>' instead."
  target:
    namespace: "App.Core.Services"
  rules:
    - forbidden_return_pattern: r"\?$"  # Regex for nullable types
    - required_return_wrapper: "Optional<*>"
  severity: "High"
```

## 4. Implementation Strategy

### 4.1. Architectural Unit Tests (C#)
We leverage `NetArchTest.eNet` to enforce structural constraints. For logic-flow constraints (like "must call X"), we use custom Reflection or Roslyn-based tests.

**Example Generated Test:**
```csharp
[Fact]
public void Controllers_Must_Have_Authorize_Attribute()
{
    var result = Types.InAssembly(typeof(BaseController).Assembly)
        .That().ResideInNamespace("App.Web.Controllers")
        .And().HaveNameEndingWith("Controller")
        .Should().HaveCustomAttribute(typeof(AuthorizeAttribute))
        .GetResult();

    Assert.True(result.IsSuccessful, "All controllers must have [Authorize] attribute.");
}
```

### 4.2. Static Analysis (Roslyn)
For deeper code verification (like "every branch must log"), we generate Roslyn `DiagnosticAnalyzers`.

## 5. Integration
*   **Agent Interaction**: Agents check `lcv_constraints.yaml` before generating code.
*   **CI/CD**: The `LCV.Tests` project runs as part of every PR.
*   **Documentation**: Constraints are automatically cross-referenced in `API_GUIDELINES.md` and `SECURITY_GUIDELINES.md`.

## 6. Supported Constraints (Initial)
*   **Attributes**: Required/Forbidden attributes on classes/methods (e.g., `[Authorize]`).
*   **Naming**: Strict naming conventions.
*   **Dependency**: Restricted namespaces (e.g., "Web cannot depend on Data directly").
*   **Signatures**: Required return types (e.g., `Optional<T>`, `Result<T>`).
*   **Behavioral**: Required method calls within a block (e.g., Logging, Permission checks).
*   **AI/ML Security**:
    *   **Anti-Interpolation**: Forbidding `$"{userInput}"` in string builders destined for LLM prompts to prevent Prompt Injection.
    *   **Strict Deserialization**: Enforcing strict `JsonSerializerOptions` when parsing LLM outputs to prevent Schema/Output exploitation.
