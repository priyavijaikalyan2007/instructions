<!--
  ⚓ CONCEPT: KeyboardShortcutRegistry
  📜 PURPOSE: Defines the canonical set of keyboard combinations for the Enterprise SaaS platform to ensure consistency across all sub-apps (Diagramming, ToDo, Project Mgmt, etc.).
  🔗 RELATES: [[UX_UI_GUIDELINES]], [[AccessibilityFocus]], [[MASTER_COMPONENT_LIST]]
  ⚡ FLOW: [User Input] -> [Component Event Listener] -> [Keyboard Registry Mapping]
-->

# Keyboard Shortcut Registry

This document defines the mandatory keyboard shortcuts for all components and applications within the Enterprise SaaS ecosystem. Consistency is the primary goal: a key combination must perform the identical action regardless of the specific tool in focus.

## 1. Global Standard Shortcuts (OS Parity)

These shortcuts must always follow standard OS conventions.

| Shortcut | Action | Scope |
| :--- | :--- | :--- |
| `Ctrl + C` | **Copy** selected item(s) or text | Global |
| `Ctrl + V` | **Paste** from clipboard | Global |
| `Ctrl + X` | **Cut** selected item(s) | Global |
| `Ctrl + Z` | **Undo** last action | Global |
| `Ctrl + Y` | **Redo** last undone action | Global |
| `Ctrl + S` | **Save** current state / work item | Global |
| `Ctrl + F` | **Find** / Search within current view | Global |
| `Ctrl + P` | **Print** / Export to PDF | Global |
| `Ctrl + A` | **Select All** in current context | Global |
| `Delete` | **Delete** selected item(s) | Global |
| `Esc` | **Cancel** current action / Close dialog | Global |

## 2. Application Shell & Navigation

Shortcuts for interacting with the `DockLayout`, `Sidebar`, and `TabbedPanel`.

| Shortcut | Action | Component |
| :--- | :--- | :--- |
| `Ctrl + K` | **Command Palette** (Search actions/entities) | [[CommandPalette]] |
| `Ctrl + ` | **Toggle Left Sidebar** (Expand/Collapse) | [[Sidebar]] |
| `Ctrl + J` | **Toggle Bottom Panel** (Log/Terminal) | [[TabbedPanel]] |
| `Ctrl + B` | **Toggle Right Sidebar** (Properties) | [[Sidebar]] |
| `Ctrl + 1-9` | **Switch Tab** by index (1 to 9) | [[TabbedPanel]] |
| `Ctrl + Tab` | **Next Tab** | [[TabbedPanel]] |
| `Ctrl + Shift + Tab` | **Previous Tab** | [[TabbedPanel]] |
| `Alt + D` | **Focus Address Bar** / Breadcrumb | [[Breadcrumb]] |
| `F1` | **Help** / Documentation for current view | Global |

## 3. Data Views (Grids, Trees & Lists)

Standardized navigation for `TreeGrid`, `TreeView`, and `DataGrid`.

| Shortcut | Action | Component |
| :--- | :--- | :--- |
| `Arrow Keys` | **Move Selection** (Up/Down/Left/Right) | [[TreeGrid]], [[TreeView]] |
| `Enter` | **Edit Cell** or Open Item | [[TreeGrid]], [[TreeView]] |
| `Space` | **Toggle Selection** (Checkbox) | [[TreeView]], [[TreeGrid]] |
| `F2` | **Rename** selected item | [[TreeView]], [[TreeGrid]] |
| `Right Arrow` | **Expand** current node | [[TreeView]], [[TreeGrid]] |
| `Left Arrow` | **Collapse** current node | [[TreeView]], [[TreeGrid]] |
| `Home` | **Move to First** item/cell | [[TreeGrid]], [[DataGrid]] |
| `End` | **Move to Last** item/cell | [[TreeGrid]], [[DataGrid]] |
| `PageUp / Down` | **Scroll Page** | [[DataGrid]] |

## 4. Rich Content & Editors

Shortcuts for `MarkdownEditor`, `CodeEditor`, and `SmartTextInputEngine`.

| Shortcut | Action | Component |
| :--- | :--- | :--- |
| `Ctrl + B` | **Bold** selected text | [[MarkdownEditor]] |
| `Ctrl + I` | **Italic** selected text | [[MarkdownEditor]] |
| `Ctrl + K` | **Insert Link** (when text selected) | [[MarkdownEditor]] |
| `@` | **Trigger Mention** | [[SmartTextInputEngine]] |
| `#` | **Trigger Resource Link** | [[SmartTextInputEngine]] |
| `$` | **Trigger Formula** | [[SmartTextInputEngine]] |
| `/` | **Trigger Slash Command** | [[SmartTextInputEngine]] |
| `Shift + Enter` | **Soft Break** (New line without submit) | [[Conversation]] |

## 5. AI & Agent Interactions

Specific to `Conversation` and agentic monitoring tools.

| Shortcut | Action | Component |
| :--- | :--- | :--- |
| `Ctrl + Enter` | **Submit Message** to Agent | [[Conversation]] |
| `Ctrl + Up` | **Navigate History** (Previous message) | [[Conversation]] |
| `Ctrl + .` | **Stop Generation** / Cancel Agent | [[Conversation]] |
| `Ctrl + Shift + C` | **Copy Code Block** (Last response) | [[Conversation]] |

## 6. Planning & Strategy

Specific to `Timeline`, `Gantt`, and `Kanban`.

| Shortcut | Action | Component |
| :--- | :--- | :--- |
| `+` | **Zoom In** | [[Timeline]], [[Gantt]] |
| `-` | **Zoom Out** | [[Timeline]], [[Gantt]] |
| `0` | **Reset Zoom** to 100% | [[Timeline]], [[Gantt]] |
| `N` | **Create New Item** (Task/Event) | [[Kanban]], [[Backlog]] |
| `T` | **Scroll to "Today"** | [[Timeline]], [[Gantt]] |

---

## Overriding Key Bindings

Every interactive component accepts an optional `keyBindings` property in its options
object. Pass a partial map of **action name** to **combo string** to override the
defaults listed above.

### Combo String Format

`"Modifier+Modifier+Key"` — modifiers are `Ctrl`, `Shift`, `Alt`; the final segment
is the `KeyboardEvent.key` value (e.g., `"ArrowRight"`, `"Enter"`, `" "` for Space,
`"a"`, `"F2"`).

### Example — Override Conversation Submit Key

```typescript
const chat = new Conversation({
    // Revert to Enter (instead of the default Ctrl+Enter):
    keyBindings: {
        "submit": "Enter",
        "softBreak": "Shift+Enter",
    },
});
```

### Example — Remap TabbedPanel Tab Switching

```typescript
const panel = new TabbedPanel({
    keyBindings: {
        "nextTab": "Alt+ArrowRight",
        "prevTab": "Alt+ArrowLeft",
    },
});
```

### Available Action Names

Each component documents its action names in `DEFAULT_KEY_BINDINGS` near the top
of its TypeScript source file. Common action names across components:

| Action Name | Typical Default | Components |
| :--- | :--- | :--- |
| `moveUp` / `moveDown` | `ArrowUp` / `ArrowDown` | TreeView, TreeGrid, DataGrid, FileExplorer |
| `expand` / `collapse` | `ArrowRight` / `ArrowLeft` | TreeView, TreeGrid |
| `submit` | `Ctrl+Enter` | Conversation |
| `escape` | `Escape` | Most components |
| `nextTab` / `prevTab` | `Ctrl+Tab` / `Ctrl+Shift+Tab` | TabbedPanel |
| `zoomIn` / `zoomOut` | `+` / `-` | Timeline |

---

## Implementation Guidelines

1. **Prevent Default:** Always use `event.preventDefault()` for registered global shortcuts to avoid browser collisions (e.g., `Ctrl+S` trying to save the HTML page).
2. **Contextual Hijacking:** A shortcut should only be "hijacked" if the component has focus. For example, `Arrow Keys` move the selection in a Grid, but scroll the page if no focus is set.
3. **KeyTip System:** When the `Alt` key is pressed, components should optionally display [[KeyTips]] (small badges) over toolbar items to guide keyboard-only discovery.
4. **WCAG Compliance:** Ensure all shortcuts have high-contrast visual focus states [[AccessibilityFocus]].
