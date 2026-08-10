# Test Plan

## Architecture

Two-tier testing strategy:

### Tier 1: Vitest + jsdom (Unit Tests)
- Fast, isolated tests for component logic
- Co-located: `components/<name>/<name>.test.ts`
- Run: `npm run test:unit`
- Coverage: `npm run test:unit:coverage`

### Tier 2: Playwright (Integration/E2E Tests)
- Real browser testing for visual, accessibility, keyboard, performance
- Centralized: `tests/components/<name>.spec.ts`
- Run: `npm run test:e2e`

### Structure Tests
- `test-local.sh` — verifies build output, links, file structure
- `test-cdn.sh` — verifies CDN asset accessibility
- Run: `npm run test:structure`

## Test Categories

| Category | Framework | Coverage |
|----------|-----------|----------|
| Factory functions | Vitest | Options, defaults, validation |
| DOM structure | Vitest | Elements, classes, ARIA |
| State management | Vitest | Open/close, enable/disable |
| Event handling | Vitest | Click, keyboard, callbacks |
| Edge cases | Vitest | Null, empty, repeated calls |
| Security (XSS) | Vitest | innerHTML sanitization |
| Visual rendering | Playwright | Screenshots, CSS |
| Keyboard navigation | Playwright | Tab, arrows, Escape |
| Accessibility audit | Playwright | axe-core WCAG AA |
| Performance | Playwright | Render time, large datasets |
| Cross-browser | Playwright | Chromium, Firefox, WebKit |

## Priority Order

### Tier 1: Security-Critical (Immediate)
1. markdownrenderer — SEC-3, SVG injection
2. richtextinput — SEC-1, innerHTML
3. spinemap — SEC-2, text extraction

### Tier 2: High-Usage Components
4. toast (DONE - 34 tests)
5. errordialog
6. editablecombobox
7. datepicker
8. treeview
9. datagrid
10. toolbar

### Tier 3: Interactive Components
11. tabbedpanel, sidebar, colorpicker, timepicker, conversation

### Tier 4: Layout & Utility
16. splitlayout, docklayout, gridlayout
17. confirmdialog, formdialog, progressmodal
18. breadcrumb, statusbar, stepper, slider, gauge

### Tier 5: Remaining (~60 components)

## Test Pattern

```typescript
import { describe, test, expect, beforeEach, afterEach, vi } from "vitest";
import { createXxx } from "./xxx";

describe("Xxx", () =>
{
    let container: HTMLElement;

    beforeEach(() =>
    {
        container = document.createElement("div");
        container.id = "test-container";
        document.body.appendChild(container);
        vi.useFakeTimers();
    });

    afterEach(() =>
    {
        container.remove();
        vi.useRealTimers();
    });

    test("createXxx_WithValidOptions_RendersRoot", () =>
    {
        const handle = createXxx({ container, ... });
        expect(container.children.length).toBeGreaterThan(0);
        handle.destroy();
    });
});
```

## Commands

```bash
npm run test:unit           # Run all unit tests
npm run test:unit:watch     # Watch mode
npm run test:unit:coverage  # Coverage report
npm run test:e2e            # Playwright integration tests
npm run test:structure      # File structure verification
npm run test:all            # Everything
```
