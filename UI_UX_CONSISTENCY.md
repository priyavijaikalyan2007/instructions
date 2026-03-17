<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 145ce583-b7d1-4e68-8a0a-961886e1e100
Created: 2026
-->

# UI/UX Consistency Standards for Coding Agents

This document defines the strict consistency standards that all coding agents MUST adhere to when building or modifying sub-applications within the super-app ecosystem. Consistency is not optional; it is fundamental to user efficiency, muscle memory, and the "enterprise-grade" feel of the platform.

## 1. Component Usage & Styling

### 1.1. Standardized Component Library
*   **Mandate:** Agents MUST NOT create new UI components if a suitable component exists in `MASTER_COMPONENT_LIST.md`.
*   **Execution:** Before implementing a feature (e.g., a date picker, a progress modal, or a tree view), search the `MASTER_COMPONENT_LIST.md` and use the approved implementation pattern.
*   **Reasoning:** Prevents "component bloat" and ensures that accessibility, keyboard shortcuts, and core behaviors are uniform across the entire platform.

### 1.2. Global Styling Application
*   **Mandate:** All components, including modal dialogs and dynamically generated elements, MUST inherit the main application's theme and font settings.
*   **Execution:** Use the global CSS theme defined in `FRONTEND.md` (§2.1). Do not use hardcoded colors or font-family declarations in component-specific styles.
*   **Modals:** Ensure Bootstrap modals use the standard theme classes. Buttons in modals must match the sizing and styling of buttons in the main application toolbar.

## 2. Layout & Muscle Memory Optimization

### 2.1. Standardized Panel Placement
To optimize for muscle memory, key functional areas must always appear in the same relative positions across all sub-apps:
*   **Resource Explorer / Navigation:** Always on the **LEFT** side.
*   **Details / Property Inspector / Settings:** Always on the **RIGHT** side.
*   **Log Console / Output:** Always at the **BOTTOM**.
*   **Main Workspace / Canvas:** Always in the **CENTER**.

### 2.2. Toolbar & Menu Consistency
Toolbars and Menu Bars MUST follow a predictable order for core operations.

#### 2.2.1. "File" Operations (Management)
Common management actions should be grouped at the **START** (left) of the toolbar or under a "File" menu item:
1.  **New** (Ctrl+N)
2.  **Save** (Ctrl+S)
3.  **Delete** (Delete)
4.  **Import**
5.  **Export**

#### 2.2.2. "Edit" Operations (Manipulation)
Common editing actions should be grouped together, typically after File operations or under an "Edit" menu item:
1.  **Undo** (Ctrl+Z)
2.  **Redo** (Ctrl+Y)
3.  **Cut** (Ctrl+X)
4.  **Copy** (Ctrl+C)
5.  **Paste** (Ctrl+V)

#### 2.2.3. View/Context Operations
Application-specific view controls (Zoom, Pan, Fit, Grid Snapping) should follow Edit operations.

### 2.3. Keyboard Shortcut Visibility
*   **Mandate:** Every menu item or toolbar button that supports a keyboard shortcut MUST display that shortcut next to the label or in its tooltip.
*   **Execution:** For menu items, use a right-aligned span for the shortcut (e.g., `Save <span class="shortcut">Ctrl+S</span>`). For toolbar buttons, include it in the `title` attribute or tooltip (e.g., `Save (Ctrl+S)`).

## 3. UI State Preservation

### 3.1. Persistence Mandate
*   **Mandate:** UI configuration state MUST be preserved across sessions and sub-app switches using `localStorage`.
*   **Execution:** Automatically save and restore the following states:
    *   Sidebar collapse/expand state and width.
    *   Log Console height and collapse state.
    *   Grid settings (size, snap-to-grid toggle).
    *   Last active tab in multi-tabbed panels.
    *   Selected view mode (e.g., List vs. Grid).

### 3.2. Implementation Pattern
```typescript
// Example state preservation pattern
const APP_STATE_KEY = 'subapp_name_ui_state';

function saveUIState(state: Record<string, any>) {
    const currentState = JSON.parse(localStorage.getItem(APP_STATE_KEY) || '{}');
    localStorage.setItem(APP_STATE_KEY, JSON.stringify({ ...currentState, ...state }));
}

function restoreUIState() {
    const state = JSON.parse(localStorage.getItem(APP_STATE_KEY) || '{}');
    // Apply state to components
    if (state.gridSize) setGridSize(state.gridSize);
    if (state.sidebarCollapsed) toggleSidebar(true);
}
```

## 4. Visual Feedback & Interaction

### 4.1. Action Feedback
*   Every button click must result in an immediate visual state change (active/pressed state).
*   Long-running operations MUST use the standardized `Progress Modal` from the `MASTER_COMPONENT_LIST.md`.

### 4.2. Error Handling
*   Write errors to the **Log Console** (§8.2 of `FRONTEND.md`) instead of using modal dialogs for non-critical failures.
*   Critical failures that require immediate user acknowledgement should use standard Bootstrap Modals, never browser `alert()` or `confirm()`.