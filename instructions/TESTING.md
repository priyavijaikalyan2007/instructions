<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 03a890af-4a95-4f79-ab79-68f409e7e3be
Created: 2026
-->

<!-- AGENT: Testing guidelines and standards for AI coding agents on enterprise SaaS. -->
# Testing Guidelines for AI Coding Agents

This document provides comprehensive testing standards and practices for AI coding agents working on enterprise SaaS applications. These guidelines ensure maintainable, readable, and reliable test suites across all technology stacks.

## Core Philosophy

Testing is not an afterthought—it is an integral part of the development process. Every line of production code should have a corresponding test that validates its behavior. Tests serve three purposes: they verify correctness, they document intended behavior, and they enable safe refactoring.

When writing tests, optimize for clarity over cleverness. A test that another developer (or AI agent) can understand in 30 seconds is more valuable than a sophisticated test that requires 10 minutes to decipher.

## Test-Driven Development

We follow a test-driven development model. While strict TDD is not always possible, strive to write tests before or alongside implementation code.

### TDD Workflow

1. **Write the test first** when implementing new features. If you cannot write the complete test, write test stubs that outline the scenarios you intend to cover.

2. **Implement the minimum code** necessary to make the test pass. Resist the urge to over-engineer.

3. **Refactor with confidence** once tests pass. The tests provide a safety net for improvements.

4. **Iterate until complete**. Update tests as understanding of requirements evolves, then ensure the implementation satisfies all tests.

### When TDD Is Not Feasible

For exploratory work, spikes, or complex integrations where the interface is unclear, you may write implementation code first. However, you must write comprehensive tests before considering the work complete. Document why TDD was not followed in your commit message.

## Test placement

Apply the [shared folder convention](REPO.md#repository-roots).
Use repository-root test/ for new workflows that span services, frontends, SDKs, native clients, extensions, or tools.
Group those tests by component or workflow when needed. Keep their nonprivate fixtures beside them.
Keep unit tests and component integration tests with their owning project.
Retain language-required names such as Go *_test.go files, Rust tests/, Java src/test/java/, and Swift Tests/.
A tool-required tests/ inside a component does not change the root test/ convention.
Generic test paths in language examples are relative to their owning component unless explicitly identified as repository-root paths.
Preserve existing root tests/ until an approved migration updates all commands and references.
Store manual test procedures in playbooks/ and bug reproduction evidence in bugreports/.
Keep product acceptance requirements in specs/ and user-facing instructions in docs/.

## Test Categories

### Unit Tests

Unit tests validate individual functions, methods, or classes in isolation. They are fast, focused, and form the foundation of the test pyramid.

**Requirements:**
- Unit tests must pass before committing any code
- Target 80% or higher code coverage for business logic
- Execute in milliseconds, not seconds
- No external dependencies such as databases, file systems, or network calls
- Use mocks, stubs, or fakes to isolate the unit under test

**When to Write:**
- Every public method or function
- Complex private methods that warrant direct testing
- Edge cases and boundary conditions
- Error handling paths

### Integration Tests

Integration tests verify that multiple components work together correctly. They test the seams between systems.

**Requirements:**
- Required for all service boundaries and data access layers
- May use real databases, message queues, or external services in test containers
- Execute in seconds, not minutes
- Run by developers before pushing and in CI pipelines

**When to Write:**
- Database repository methods
- API endpoints
- Message queue producers and consumers
- Third-party service integrations
- Cross-module interactions

### End-to-End Tests

End-to-end tests validate complete user journeys using the tools for the affected surface.
Browser journeys use tools such as Playwright or Selenium. Native Apple journeys use XCTest UI tests from instructions/apps/APPS.md and instructions/swift/SWIFT.md.

**Requirements:**
- Required for critical user workflows
- For new browser projects, prefer Playwright. Native Apple targets use the configured XCTest UI test setup.
- Run by developers and in CI pipelines before deployment
- Include visual regression testing for UI-critical paths

**When to Write:**
- User authentication and authorization flows
- Core business workflows
- Payment and checkout processes
- Multi-step forms and wizards
- Features with complex client-server interactions

### Contract Tests

Contract tests verify that services honor their API contracts with consumers.

**When to Write:**
- Microservice boundaries
- Public API endpoints
- Event-driven integrations

## Evidence That Tests Exercise the Behavior

Confirm that a regression test reaches the defective path and fails for the expected reason before the fix.
Use isolated negative fixtures or temporary mutations when needed to verify that a gate detects its named defect.
Restore temporary mutations before committing. Do not weaken a valid assertion to make a run pass.
For counting tools, test the classifier and exclusions rather than trusting a matching total.
When the measured code changes shape, check representative classifications again.
Use real browsers for layout, resource loading, and other behavior that a simulated DOM cannot reproduce.
Verify packaged artifacts and consumer-facing APIs as well as source modules.
For a claimed type-only change, compare compiled output through the same build settings before and after the change.
Retain machine-readable test results when the runner supports them. Distinguish passed, failed, skipped, and unexecuted checks.

## Test Structure and Organization

### One Test Per Scenario

Each test should validate exactly one scenario or behavior. Never combine multiple test cases into a single test method.

See [C#](csharp/CSHARP.md#one-test-per-scenario).

### One Test Class Per Feature or Component

Group related tests into a single test class. The class should correspond to the production class or feature being tested.

See [C#](csharp/CSHARP.md#test-examples).

### Arrange-Act-Assert Pattern

Structure every test using the Arrange-Act-Assert pattern. Use blank lines or comments to delineate sections in longer tests.

See [C#](csharp/CSHARP.md#arrange-act-assert-pattern).

### Test Naming Conventions

Name the operation, scenario, and expected behavior using the selected language's conventions.
Keep names within 60 characters. Avoid vague names, implementation details, and unnecessary negative framing.

### Test Independence and Isolation

Tests must be completely independent. They should not rely on execution order, shared mutable state, or the side effects of other tests.

**Requirements:**
- Each test sets up its own required data in the Arrange phase
- Each test cleans up any persistent changes in a finally block or teardown method
- Use unique identifiers for test data to prevent collision
- Reset shared resources between tests

See [C#](csharp/CSHARP.md#test-independence-and-isolation).

## Test Data Management

### Test Factories and Builders

Use factory methods or builder patterns to create test data. This centralizes data creation, reduces duplication, and makes tests more readable.

See [C#](csharp/CSHARP.md#test-factories-and-builders).

See [TypeScript](typescript/TYPESCRIPT.md#test-factories-and-builders).

### Test Fixtures

For complex setup that is shared across multiple tests, use fixtures. Fixtures should be immutable or should provide fresh copies to each test.

See [C#](csharp/CSHARP.md#test-fixtures).

### Avoiding Magic Values

Never use unexplained literal values in tests. Use named constants, factory methods, or well-named variables that communicate intent.

See [C#](csharp/CSHARP.md#avoiding-magic-values).

## Mocking and Test Doubles

### When to Mock

Use mocks to isolate the unit under test from its dependencies. Mock external services, databases, file systems, and any component that introduces non-determinism or slowness.

**Mock these:**
- External HTTP services and APIs
- Database connections in unit tests
- File system operations
- Current time (inject a clock abstraction)
- Random number generation
- Email and notification services

**Do not mock these:**
- The class under test
- Simple value objects or DTOs
- Pure functions without side effects
- In integration tests, the components you are integrating

### Mocking Best Practices

See [C#](csharp/CSHARP.md#mocking-best-practices).

### Prefer Fakes Over Mocks for Complex Interactions

When testing complex interactions, consider using in-memory fakes instead of mocks. Fakes provide more realistic behavior and catch more bugs.

See [C#](csharp/CSHARP.md#prefer-fakes-over-mocks-for-complex-interactions).

## Comments and Documentation

Tests should be well-commented. Refer to instructions/COMMENTING.md for comprehensive commenting standards. The following guidelines are specific to test code.

### Comment the Why, Not the What

Test code should be self-explanatory through good naming and structure. Use comments to explain non-obvious decisions, edge cases, or the business context.

See [C#](csharp/CSHARP.md#comment-the-why-not-the-what).

### Document Test Scenarios in Class Headers

Add a summary comment to test classes explaining what scenarios are covered.

See [C#](csharp/CSHARP.md#document-test-scenarios-in-class-headers).

### Document Non-Obvious Test Data

When test data represents specific scenarios, document what it represents.

See [C#](csharp/CSHARP.md#document-non-obvious-test-data).

## Logging in Tests

Tests should include strategic logging to aid debugging when tests fail. Refer to instructions/LOGGING.md for comprehensive logging standards.

### What to Log

- Test setup completion and key configuration
- Input data for the scenario being tested
- Intermediate states during complex operations
- The actual result before assertions
- Cleanup operations

### How to Log

See [C#](csharp/CSHARP.md#how-to-log).

## Code Coverage

### Coverage Requirements

| Test Type | Minimum Coverage | Target Coverage |
|-----------|-----------------|-----------------|
| Unit Tests | 80% line coverage | 90% line coverage |
| Integration Tests | Track but no minimum | Maximize critical paths |
| E2E Tests | Track but no minimum | Cover all happy paths |

### What to Cover

- All public APIs and entry points
- All business logic branches
- Error handling and edge cases
- Boundary conditions

### What Not to Obsess Over

- Generated code and DTOs
- Simple property accessors
- Framework configuration code
- Logging statements

### Coverage Tools by Stack

Use coverage tools and commands from the selected language guide.
Do not install or switch a coverage stack merely because an example names one.

### Running Coverage

Run the project's configured coverage command. See the selected language guide for examples.

## Handling Test Failures

### Diagnosis Before Fixes

When a test fails during bug fixes, refactoring, or feature additions, do not immediately modify the production code. Follow this process:

1. **Read the failure message carefully.** Understand exactly what assertion failed and what values were involved.

2. **Determine the root cause.** Is it a test problem, a legitimate bug in new code, or an unintended regression?

3. **Categorize the failure:**
   - **Test is wrong:** The test has incorrect expectations, outdated assumptions, or a bug in the test itself. Fix the test.
   - **Test is flaky:** The test passes inconsistently due to timing, ordering, or external dependencies. Fix the test's reliability issues.
   - **Code has a bug:** The production code has a genuine defect. Request permission before modifying production code.
   - **Intentional behavior change:** The new feature intentionally changes behavior. Update the test to reflect the new expected behavior after confirming this is correct.

4. **Request permission for code changes.** If the production code needs modification, explain the diagnosis and proposed fix before making changes.

### Example Diagnosis Process

```
Test Failed: CreateUser_WithValidData_ReturnsCreatedUser
Expected: Status = "active"
Actual: Status = "pending"

Diagnosis Steps:
1. Check if the test expectation is correct for the current requirements
2. Review recent changes to user creation logic
3. Check if "pending" is a new valid initial state (perhaps for email verification)
4. Determine if this is:
   - A test that needs updating for new requirements ← Update test
   - A bug introduced in recent changes ← Request permission to fix code
   - A flaky test with race conditions ← Fix test isolation
```

## Testing Across Technology Stacks

Our applications use multiple technologies. Testing strategies must account for cross-stack interactions.

### TypeScript and JavaScript (Frontend)

See [JavaScript](frontend/FRONTEND.md#browser-testing).

### C# and .NET Core (Backend)

See [C#](csharp/CSHARP.md#testing).

### Python (Operational Scripts)

See [Python](python/PYTHON.md#testing).

### Swift (macOS and iOS)

See [Swift](swift/SWIFT.md#testing).

### Go

See [Go](go/GO.md#testing).

### Rust

See [Rust](rust/RUST.md#testing).

### Java

See [Java](java/JAVA.md#testing).

### Cross-Stack Testing

When a feature spans multiple stacks, ensure tests exist at each layer:

```
Feature: User Registration

Frontend (TypeScript):
- Unit: RegistrationForm validation logic
- Integration: Form submission to API client
- E2E: Complete registration flow in browser

Backend (C#):
- Unit: UserValidator, UserService methods
- Integration: UserController endpoints, UserRepository
- E2E: API scenario from registration to confirmation email

Scripts (Python):
- Unit: Email template generation
- Integration: Email service connectivity
```

## Testing Non-Code Assets

### SQL and Database Migrations

**Test migrations:**
- Run migrations up and down in a test database
- Verify data integrity after migrations
- Test rollback scenarios

See [C#](csharp/CSHARP.md#sql-and-database-migrations).

**Test stored procedures and functions:**
See [C#](csharp/CSHARP.md#sql-and-database-migrations).

### Infrastructure as Code (Terraform)

**Validate configurations:**
```bash
# Syntax validation
terraform validate

# Plan review (in CI)
terraform plan -detailed-exitcode

# Use Terratest for integration testing
```

**Test with Terratest (Go):**
See [Go](go/GO.md#infrastructure-as-code-terraform).

### Configuration Files

Test that configuration files are valid and complete:

See [C#](csharp/CSHARP.md#configuration-files).

### Shell Scripts

See [Shell](shell/SHELL.md#testing).

## Asynchronous Testing

### Testing Async Code

Async operations require special consideration to avoid race conditions and ensure deterministic tests.

See [C#](csharp/CSHARP.md#testing-async-code).

### Testing Event-Driven Systems

See [C#](csharp/CSHARP.md#testing-event-driven-systems).

### Handling Timeouts

Always include timeouts when waiting for async operations in tests:

See [C#](csharp/CSHARP.md#handling-timeouts).

## Flaky Test Prevention and Handling

### Common Causes of Flakiness

1. **Time dependencies:** Tests that depend on current time or specific timing
2. **Order dependencies:** Tests that depend on execution order
3. **Shared state:** Tests that share mutable state without proper isolation
4. **External services:** Tests that depend on network or external systems
5. **Race conditions:** Tests with concurrent operations that may complete in different orders

### Prevention Strategies

**Inject time dependencies:**
See [C#](csharp/CSHARP.md#prevention-strategies).

**Use deterministic identifiers:**
See [C#](csharp/CSHARP.md#prevention-strategies).

**Isolate external dependencies:**
See [C#](csharp/CSHARP.md#prevention-strategies).

### Handling Existing Flaky Tests

When you encounter a flaky test:

1. **Quarantine it:** Mark it with `[Trait("Category", "Flaky")]` or skip it temporarily
2. **Document the flakiness:** Add a comment explaining the observed behavior
3. **Create a ticket:** Track the fix as technical debt
4. **Fix the root cause:** Do not just retry the test

See [C#](csharp/CSHARP.md#handling-existing-flaky-tests).

## CI/CD Integration

### Test Execution in Pipelines

Configure CI pipelines to run tests at appropriate stages:

See [C#](csharp/CSHARP.md#test-execution-in-pipelines).

### Test Parallelization

Enable parallel test execution where safe:

See [C#](csharp/CSHARP.md#test-parallelization).

See [JavaScript](javascript/JAVASCRIPT.md#test-parallelization).

### Test Artifacts

Preserve test artifacts for debugging failed CI runs:

```yaml
- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: |
      **/TestResults/
      **/playwright-report/
      **/coverage/
```

## Performance and Load Testing

### When to Write Performance Tests

- Before and after performance-critical changes
- For operations with SLA requirements
- For database queries that may be called frequently

### Simple Performance Assertions

See [C#](csharp/CSHARP.md#simple-performance-assertions).

### Benchmark Tests

Use the benchmark or profiler tools in the selected language guide.
Java uses the configured benchmark harness and Java Flight Recorder. Native Apple apps use Instruments and Xcode diagnostics.
For .NET, use BenchmarkDotNet for detailed performance analysis:

See [C#](csharp/CSHARP.md#benchmark-tests).

## Security Testing

### Input Validation Tests

See [C#](csharp/CSHARP.md#input-validation-tests).

### Authentication and Authorization Tests

See [C#](csharp/CSHARP.md#authentication-and-authorization-tests).

## Accessibility Testing

Include accessibility checks in E2E tests:

See [TypeScript](typescript/TYPESCRIPT.md#accessibility-testing).

## Summary Checklist

Before considering a feature complete, verify:

- [ ] Unit tests cover all public methods and critical private methods
- [ ] Integration tests cover all service boundaries and data access
- [ ] E2E tests cover critical user journeys
- [ ] All tests pass locally and in CI
- [ ] Code coverage meets or exceeds targets
- [ ] Tests are independent and can run in any order
- [ ] Test names clearly describe the scenario
- [ ] Comments explain non-obvious logic or business rules
- [ ] No flaky tests introduced
- [ ] Test data uses factories or builders
- [ ] Mocks are used appropriately and not excessively
- [ ] Cross-stack changes have tests at each layer
- [ ] Non-code assets (SQL, configs, scripts) are tested where applicable

## Authorization Service Testing

See [C#](csharp/CSHARP.md#authorization-service-testing).

### Common Authorization Methods to Mock

See [C#](csharp/CSHARP.md#authorization-service-testing).

### Example: Mocking Access Level Checks

See [C#](csharp/CSHARP.md#authorization-service-testing).

### Keeping Mocks in Sync with Implementation

See [C#](csharp/CSHARP.md#authorization-service-testing).

### Testing Access Level Responses

See [C#](csharp/CSHARP.md#authorization-service-testing).

## Tests for code changes

You must always add unit tests for all code changes. This is non-negotiable.

## Regression and feature checks

- **Bug Fixes**: When fixing bugs, add regression tests to prevent the bug from recurring.
- **New Features**: When adding features, functionality, or capabilities, add unit tests that verify:
  - All expected functionality works correctly (happy paths)
  - Invalid inputs, edge cases, and failure conditions are handled properly (unhappy paths)
  - In other words, test both what *should* work and what *should not* be possible or work.
