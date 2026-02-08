# UX/UI Design Guidelines

This document outlines the user experience (UX) and user interface (UI) design principles for the project. It complements the technical standards in `FRONTEND.md` by focusing on the *why* and *how* of user interaction.

## 1. Core Design Philosophy

Our design philosophy is built on three pillars: **Clarity**, **Efficiency**, and **Consistency**.

### 1.1. Minimize Cognitive Load
Users have a limited amount of mental energy. Every ambiguous label, hidden control, or inconsistent behavior adds to their cognitive load.
*   **Don't make users think:** Controls should do exactly what they look like they do.
*   **Progressive Disclosure:** Show only what is necessary for the current task. Hide advanced options until requested.
*   **Chunking:** Break long forms or complex processes into smaller, manageable steps (Miller's Law).

### 1.2. Respect Muscle Memory
Users shouldn't have to relearn how to use a computer when they use our software.
*   **Standard Shortcuts:** `Ctrl+C` must copy. `Ctrl+Z` must undo. `Esc` must close modals or cancel actions.
*   **Standard Locations:** The "Close" button goes in the top-right. The "Save" button goes at the bottom-right of a form (or top-right of a sticky header).
*   **Fitts's Law:** Make important targets (like "Save" or "Delete") large and easy to click. Place related controls close to each other.

### 1.3. Intuitive Understanding
*   **Affordance:** Buttons should look clickable. Input fields should look like they accept text.
*   **Feedback:** Every action must have an immediate reaction. If a user clicks a button, it should visually depress or change state immediately, even if the operation takes time.
*   **Jakob's Law:** Users spend most of their time on other sites. They expect your site to work like all the other sites they know. Don't reinvent the wheel—use standard patterns.

## 2. Laws of UX in Practice

We explicitly adopt the following principles from [Laws of UX](https://lawsofux.com/):

### 2.1. Jakob's Law (Familiarity)
*   **Do:** Use standard icons (gear for settings, trash can for delete).
*   **Don't:** Use a "star" icon for settings or a "minus" sign for delete unless explicitly clearing a list item.

### 2.2. Fitts's Law (Target Size & Distance)
*   **Do:** Make primary call-to-action (CTA) buttons large and prominent.
*   **Do:** Place the "Submit" button near the last input field of a form.
*   **Don't:** Place a tiny "Delete" icon right next to a "Save" button without spacing.

### 2.3. Hick's Law (Decision Time)
*   **Do:** Limit the number of primary actions on a screen. If there are 10 actions, group the less common 7 into a "More Actions" dropdown.
*   **Don't:** Present a dashboard with 20 distinct, equally weighted buttons.

### 2.4. Doherty Threshold (Speed)
*   **Do:** Provide system feedback within 400ms. If loading takes longer, show a skeleton screen or a spinner immediately.
*   **Do:** Optimistically update the UI. If a user deletes an item, remove it from the list immediately while the API call happens in the background. (Handle errors gracefully if it fails).

## 3. Visual Interface Guidelines

### 3.1. Color & Contrast
*   **Semantic Colors:**
    *   <span style="color:blue">**Primary (Blue/Brand)**</span>: Main actions (Save, Submit, Create).
    *   <span style="color:green">**Success (Green)**</span>: Confirmation messages, successful states.
    *   <span style="color:red">**Danger (Red)**</span>: Destructive actions (Delete, Remove).
    *   <span style="color:orange">**Warning (Yellow/Orange)**</span>: Non-blocking issues, alerts.
    *   <span style="color:gray">**Neutral (Gray)**</span>: Secondary actions (Cancel), borders, dividers.
*   **Accessibility:** Ensure a contrast ratio of at least 4.5:1 for text against its background.

### 3.2. Typography
*   **Hierarchy:** Use font size and weight to establish order.
    *   `h1`: Page titles.
    *   `h2`: Section headers.
    *   `h3`: Card/Panel headers.
    *   `body`: Standard readable text (14px-16px).
    *   `small`: Metadata, help text.
*   **Readability:** Keep line lengths between 45-75 characters for comfortable reading.

### 3.3. Spacing & Layout
*   **White Space:** Use white space to group related elements. Elements close together are perceived as related (Law of Proximity).
*   **Grid System:** Use the Bootstrap grid (Rows/Cols) to ensure alignment. Everything should align to a conceptual grid.
*   **Consistency:** Use consistent margins and padding (e.g., always `1rem` or `16px` between cards).

## 4. Interaction Patterns

### 4.1. Keyboard Shortcuts
Power users rely on keyboards. All apps must support:
*   **Global:**
    *   `?` : Show keyboard shortcuts help.
    *   `Esc`: Close modal / Cancel selection.
*   **Editing:**
    *   `Ctrl/Cmd + S`: Save.
    *   `Ctrl/Cmd + Z`: Undo.
    *   `Ctrl/Cmd + Shift + Z` (or `Y`): Redo.
*   **Selection:**
    *   `Ctrl/Cmd + A`: Select All.
    *   `Delete` / `Backspace`: Delete selected item(s).
    *   `Arrow Keys`: Nudge/Move selected items (in diagramming apps).

### 4.2. Feedback & States
*   **Hover:** Interactive elements must have a hover state to indicate clickability.
*   **Focus:** Focus rings are mandatory for accessibility. Never remove `outline: none` without replacing it.
*   **Loading & Progress (Crucial):**
    *   **Never leave the user guessing.** If an operation takes > 200ms, show an indicator.
    *   **Initial Load:** Use **Skeleton Screens** (gray placeholders) or a global loading spinner to indicate the app is initializing. Do not show a blank white screen.
    *   **Background Actions (Auto-save):** Show a non-intrusive status indicator (e.g., "Saving..." -> "All changes saved") in the toolbar or footer.
    *   **Blocking Operations:** If the user *cannot* interact with the app while processing (e.g., "Importing large file"), use a **Progress Modal** with a visible progress bar or spinner and a descriptive text ("Importing... 45%").
    *   **Lazy Loading:** When loading parts of the UI (like a heavy tool palette), show a local spinner placeholder where the content will appear.
*   **Success/Error:** Use toast notifications (top-right or bottom-right) for transient messages. Do not block the screen with "Success!" modals.

### 4.3. Modals vs. Inline
*   **Use Modals for:** Critical decisions, simple forms that don't require context from the main page, or "interruption" tasks.
*   **Use Inline/Sidebars for:** Complex configurations, context-dependent editing (properties panel), or tasks that allow referencing the main content.

### 4.4. Destructive Actions
*   **Confirmation:** Always require confirmation for destructive actions that cannot be easily undone.
*   **Friction:** Add friction to irreversible actions (e.g., "Type 'DELETE' to confirm").
*   **Safety:** Default focus should be on the "Cancel" button, not the "Delete" button in a confirmation dialog.

## 5. UI Components

### 5.1. Buttons
*   **Primary Button:** Only one per section/view. Filled color.
*   **Secondary Button:** Outline or lower contrast.
*   **Tertiary/Text Button:** For less important actions (e.g., "Cancel").
*   **Labeling:** Use verbs. "Save", "Delete", "Publish". Avoid generic "OK" or "Yes".

### 5.2. Forms
*   **Labels:** Top-aligned labels are generally faster to scan.
*   **Validation:** Inline validation (immediate feedback) is preferred over "submit and fail".
*   **Defaults:** Provide smart defaults whenever possible.

### 5.3. Icons
*   Use a consistent icon set (e.g., FontAwesome, Bootstrap Icons, Material Icons).
*   **Pair with text:** Icons alone are often ambiguous. Use tooltips or accompanying text labels where space permits.
*   **Standard meanings:**
    *   🔍 Magnifying Glass: Search
    *   ⚙️ Gear/Cog: Settings
    *   💾 Floppy Disk: Save (still the standard, despite the medium being obsolete)
    *   ✏️ Pencil: Edit
    *   🗑️ Trash Can: Delete
    *   ➕ Plus: Add/Create
    *   ✖️ X: Close/Remove

## 6. Accessibility (A11y)
Accessibility is not just for disabled users; it improves the experience for everyone.
*   **Alt Text:** All meaningful images must have `alt` text. Decorative images should have `alt=""`.
*   **Semantic HTML:** Use `<button>` for buttons, `<a>` for links. Don't use `<div>` with an `onclick` handler unless you reimplement all button behaviors (focus, enter key, space key).
*   **Screen Readers:** Ensure logical tab order.
