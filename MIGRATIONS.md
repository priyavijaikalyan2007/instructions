<!-- AGENT: Standard operating procedures for code migrations between languages and frameworks. -->

# Migration Guidelines for Coding Agents

This document defines the standard operating procedure for migrating code between languages, frameworks, or versions (e.g., JavaScript to TypeScript, Python 2 to 3, Flask to ASP.NET).

**Core Philosophy**: Tests are the source of truth. The migration is not complete until the new code compiles AND passes the original behavior tests.

---

## The Golden Loop: Test-Driven Migration

When asked to migrate "Stack 1" (Legacy) to "Stack 2" (Target), you must strictly follow this iterative loop. **Do not attempt to migrate logic blindly.**

### Phase 1: Establish the Baseline (The "Safety Net")

Before writing a single line of target code, you must ensure the legacy code is fully covered by tests.

1.  **Analyze Existing Tests**: Check coverage of the legacy code.
2.  **Fill the Gaps**: If coverage is low (< 90%), write new unit/integration tests against the *Legacy* code.
3.  **Verify Baseline**: Run these tests. They **must pass** against the legacy code.
    *   *Why?* If tests fail now, you won't know if failures later are due to your migration or pre-existing bugs.

### Phase 2: The Migration (Iterative Compilation)

Convert the code to the target stack. Focus on syntax and structure first.

1.  **Draft Migration**: Translate the code to the target language/framework.
    *   *Tip*: Keep logic 1:1 where possible initially. Refactor for idiom *after* functionality is verified.
2.  **Compile/Lint**: Run the compiler or linter (e.g., `tsc`, `dotnet build`).
3.  **Fix Syntax Errors**:
    *   Feed error messages back into your context.
    *   Fix types, imports, and syntax issues.
    *   **Repeat until the code compiles cleanly.**

### Phase 3: The Verification (Test-Driven Repair)

Now that the code compiles, does it actually work?

1.  **Migrate Tests**: Translate the *Baseline Tests* from Phase 1 to the target language.
2.  **Run Tests**: Execute the new test suite against the new code.
3.  **Analyze Failures**:
    *   **Do NOT change the tests** (unless the API contract explicitly changed).
    *   Use the failure output (stack traces, expected vs. actual) to fix the *Migrated Code*.
4.  **Repeat**: Fix code -> Run Tests -> Check Failures.
5.  **Success**: The loop ends only when **100% of tests pass**.

### Phase 4: Refactoring (Optional but Recommended)

Once tests pass, the code is safe to modify.

1.  **Idiomatic Polish**: Now you can replace direct translations with language-specific features (e.g., changing a `for` loop to a LINQ query or `.map()`).
2.  **Verify**: Run tests after every refactoring step.

---

## Example Scenario: JavaScript to TypeScript

1.  **Phase 1**:
    *   User asks to migrate `utils.js`.
    *   *Agent Action*: Check for `utils.test.js`. If missing, create it. Run `jest utils.test.js` to confirm it passes.

2.  **Phase 2**:
    *   *Agent Action*: Rename `utils.js` to `utils.ts`. Add type annotations (`any` is acceptable temporarily if strictness causes blocks, but aim for specific types).
    *   Run `tsc`. Fix "Implicit any" or "Property does not exist" errors.

3.  **Phase 3**:
    *   *Agent Action*: Rename `utils.test.js` to `utils.test.ts`.
    *   Run `jest`.
    *   *Error*: "Expected 5, got '5'".
    *   *Fix*: Update `utils.ts` to ensure return type is `number`, not string.

4.  **Phase 4**:
    *   *Agent Action*: Change `interface` definitions to be more specific. Run tests. Pass.

---

## Checklist for Agents

- [ ] **Pre-Flight**: Are there passing tests for the legacy code?
- [ ] **Draft**: Is the code translated?
- [ ] **Compile**: Does the build command succeed without errors?
- [ ] **Verify**: Do the migrated tests pass against the migrated code?
- [ ] **Cleanup**: Did you remove temporary files or "commented out" legacy code?
