<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 544ebe04-976e-4529-97f2-057b10113762
Created: 2026
-->

<!-- AGENT: Shared interaction, validation, accessibility, save safety, and experience requirements. -->

# UI and UX behavior

Read this guide for user-facing behavior in native apps, browser applications, websites, and interactive components.
Read only the component profiles needed by the task in [UI_UX_COMPONENTS.md](UI_UX_COMPONENTS.md).
[KEYBOARD.md](frontend/KEYBOARD.md) holds detailed browser shortcut tables and their focus scopes.
[FRONTEND.md](frontend/FRONTEND.md) holds browser implementation. [APPS.md](apps/APPS.md) holds native platform conventions.
[SAAS.md](saas/SAAS.md) holds the enterprise shell layout. [PERSISTENCE.md](PERSISTENCE.md) holds storage mechanics.

The common behavior below applies where the interface has that capability.
Browser catalog names, ARIA, CSS units, and Bootstrap examples describe browser implementations.
Native UIs use their declared platform controls and accessibility APIs, as specified in instructions/apps/APPS.md.
Named catalog components describe intended roles. Their availability comes from the consuming project's catalog.

## Read by task

| Changed behavior | Read |
| --- | --- |
| Semantic controls, field help, focus, states, and async feedback | [Common experience baseline](#common-experience-baseline) |
| Validation, warnings, system failures, and correction | [Validation and error behavior](#validation-and-error-behavior) |
| Pending, background, or multi-stage work | [Progress and long-running operations](#progress-and-long-running-operations) |
| Navigation, dirty work, and saves | [Navigation and workspaces](#navigation-and-workspaces), [save safety](#save-and-navigation-safety) |
| Specific fields, widgets, editors, or workflows | [Component profiles](UI_UX_COMPONENTS.md#select-component-profiles) |
| Completion review | [UI engineering acceptance checklist](#ui-engineering-acceptance-checklist) |

## Purpose

This guide groups shared experience behavior and the enterprise browser component profiles.

A feature specification defines what a feature does. This specification defines how users interact with that feature.

The enterprise browser profile covers forms, editors, grids, people controls, help, validation, policy tools, workflows, and navigation.
The common behavioral contract applies to the controls selected for the task.

The main rule is:

> **Match the richness of the interaction to the richness of the data and task.**

A value with domain meaning must not become a plain text field only because text is its storage format.

An email recipient is a person or address, not a string. A CEL expression is executable logic, not a string. A date is a temporal value, not formatted text. A service reference is an entity, not an identifier.

Each feature inherits four levels of requirements:

1. **Common baseline requirements** apply to all user interfaces.
2. **Data-type requirements** apply to the semantic value that a user reads or edits.
3. **Component-family requirements** apply to the interaction pattern.
4. **Workflow requirements** apply to complete tasks that combine several components.

A feature can add requirements. A feature must not silently remove baseline requirements.

### Requirement levels

This specification uses three requirement levels:

- **Required:** The implementation must meet the requirement before normal release.
- **Recommended:** The implementation should meet the requirement unless a documented reason prevents it.
- **Optional:** The implementation can provide the behavior when the product benefits from it.

An exception to a Required behavior must identify:

- The requirement that cannot be met.
- The reason.
- The user impact.
- The alternative behavior.
- The owner.
- The planned resolution, if applicable.

---

## Design principles

Our design philosophy is built on three pillars: **Clarity**, **Efficiency**, and **Consistency**.

We explicitly adopt the following principles from [Laws of UX](https://lawsofux.com/):

## Clarity and progressive disclosure

Users have a limited amount of mental energy. Every ambiguous label, hidden control, or inconsistent behavior adds to their cognitive load.
*   **Don't make users think:** Controls should do exactly what they look like they do.
*   **Progressive Disclosure:** Show only what is necessary for the current task. Hide advanced options until requested.
*   **Chunking:** Break long forms or complex processes into smaller, manageable steps (Miller's Law).

## Recognizable controls and feedback

*   **Affordance:** Buttons should look clickable. Input fields should look like they accept text.
*   **Feedback:** Every action must have an immediate reaction. If a user clicks a button, it should visually depress or change state immediately, even if the operation takes time.
*   **Jakob's Law:** Users spend most of their time on other sites. They expect your site to work like all the other sites they know. Don't reinvent the wheel—use standard patterns.

## Familiar meanings

*   **Do:** Use standard icons (gear for settings, trash can for delete).
*   **Don't:** Use a "star" icon for settings or a "minus" sign for delete unless explicitly clearing a list item.

## Target size and placement

*   **Do:** Make primary call-to-action (CTA) buttons large and prominent.
*   **Do:** Place the "Submit" button near the last input field of a form.
*   **Don't:** Place a tiny "Delete" icon right next to a "Save" button without spacing.

## Action hierarchy

*   **Do:** Limit the number of primary actions on a screen. If there are 10 actions, group the less common 7 into a "More Actions" dropdown.
*   **Don't:** Present a dashboard with 20 distinct, equally weighted buttons.

## Common experience baseline

### Semantic controls

The UI must use the semantic type of a value to select its interaction.

Do not use a generic text input when a more specific interaction can understand the value.

Examples include:

| Data | Required default interaction |
|---|---|
| Person | People picker |
| Email recipient | Recipient editor with identity resolution |
| Date | Date input and date picker |
| Time | Time input and time picker |
| Time zone | Searchable IANA time-zone picker |
| Duration | Duration editor |
| Entity reference | Entity lookup |
| Multiple entities | Multi-select lookup with entity pills |
| CEL or policy expression | Expression editor |
| JSON or YAML | Code editor |
| Secret | Masked secret control |
| Color | Color picker |
| File | File selector or upload manager |
| Query | Structured query builder or query-aware editor |
| Formula | Formula editor |
| Permission | Permission-aware selector or matrix |

A simple control remains acceptable when the semantic type is simple.

### Field anatomy

Every editable field must support the following field structure:

1. Label.
2. Required or optional state.
3. Reason for collection when the purpose is not obvious.
4. Short guidance when format or interpretation matters.
5. Input control.
6. Current validation or status message.
7. Field-level help.
8. Detailed contextual help.

Do not use an asterisk as the only indication that a field is required.

Optional fields should normally include `(optional)` in the label. GOV.UK also recommends this pattern and advises against required-field asterisks.

When a required value is not self-explanatory, explain why it is required.

Use:

> **Business unit**
>
> Required. The system uses this value to select the approval policy.

Do not use:

> **Business unit \***

### Help is part of every field

Every form field must provide field-level help.

The browser profile names `HelpTooltip` for brief guidance, `HelpDrawer` for persistent contextual help, and `HoverCard` for richer previews.
These names identify roles for the corresponding help surfaces.

Each field must support three levels of help.

**Level 1: Immediate guidance**

Show concise guidance beside the field when users commonly need it.

Examples include accepted format, units, scope, or an important consequence.

**Level 2: Help icon**

Provide a consistent help control beside the field label.

Activating the control must show a brief explanation without destroying the user's current work.

**Level 3: Detailed help**

The help control must provide access to a detailed topic in the contextual help surface.
The browser library profile uses `HelpDrawer` for this role.

The topic should include, when applicable:

- Purpose.
- Valid values.
- Examples.
- Default behavior.
- Required reason.
- Dependencies.
- Side effects.
- Permission requirements.
- Security implications.
- Related settings.
- Troubleshooting guidance.
- Links to deeper documentation.

The help drawer should remain open while the user works.

Opening help must not reset the form.

The drawer must preserve its topic when the user moves between nearby fields, unless the user requests automatic topic changes.

WCAG 2.2 includes a Consistent Help criterion. Help mechanisms should therefore remain in a predictable location and order.

### Keyboard behavior is part of the component

Keyboard behavior is not a later accessibility enhancement.

Every component must define its keyboard contract when the component is designed.

The general convention is:

- `Tab` moves to the next component.
- `Shift+Tab` moves to the previous component.
- Arrow keys navigate within a composite component.
- `Enter` activates or confirms the current item.
- `Space` activates controls where that convention applies.
- `Escape` dismisses the current temporary interaction.
- `Home` and `End` move to logical boundaries where useful.

This convention follows the WAI-ARIA Authoring Practices Guide. It uses Tab between components and arrow keys within composite components.

Components must not create keyboard traps.

Keyboard focus must remain visible and must not be hidden behind sticky headers, overlays, or other content. WCAG 2.2 adds explicit requirements for focus visibility and focus obstruction.

### Focus management

Every interactive component must define:

- Where focus enters.
- How focus moves inside the component.
- Where focus goes after completion.
- Where focus goes after cancellation.
- What happens when an item disappears.
- How focus behaves after validation fails.
- How focus behaves after an asynchronous update.

A popup must not unexpectedly move focus away from the control that opened it.

Autocomplete controls should normally keep focus in the input. They should expose the active result through ARIA relationships.

A modal dialog must trap focus within the dialog.

When a modal closes, focus must return to the control that opened it, unless the workflow has moved elsewhere.

### Pointer and touch input

All core behavior must work without drag, hover, or a precision pointer.

Any operation that uses drag must provide a non-drag alternative. WCAG 2.2 includes this requirement for dragging interactions.

Examples include:

- Move up and Move down actions.
- Reorder menus.
- Keyboard reordering.
- Destination selectors.
- Cut and paste operations.

Pointer targets must meet WCAG target-size requirements.

For the browser library, touch-oriented interfaces should target at least 44 by 44 CSS pixels where layout permits.

Hover information must also be available through keyboard focus or another explicit action.

### Component states

Every component must implement all states that can occur.

Do not implement only the ideal state.

The common state vocabulary is:

| State | Meaning |
|---|---|
| Idle | Ready for interaction |
| Focused | User has keyboard focus |
| Loading | Initial data is loading |
| Pending | User action is being checked or processed |
| Ready | Data is available |
| Empty | Valid state with no data |
| Valid | Current value passed meaningful validation |
| Warning | Value is allowed but deserves attention |
| Invalid | Value cannot be accepted |
| Partial | Some data or results are available |
| Stale | Displayed data may no longer be current |
| Offline | Required network service is unavailable |
| Disabled | Action is unavailable |
| Read-only | Value can be read but not changed |
| Error | The operation failed |

Components must distinguish `disabled` from `read-only`.

A disabled control should explain why it is unavailable when the reason is not obvious.

### Asynchronous behavior

An asynchronous control must expose its state.

Do not allow an asynchronous lookup to appear frozen.

The component must:

- Show pending state.
- Prevent stale responses from replacing newer responses.
- Preserve the user's current value.
- Allow retry when retry is safe.
- Explain network failures.
- Distinguish no results from request failure.
- Cancel obsolete requests when practical.
- Prevent duplicate commits.
- Preserve idempotency for retried mutations where the API supports it.

Async validation must use a generation number, cancellation token, or equivalent mechanism.

The newest user input must remain authoritative.

### Preserve user work

An error must not erase valid user input.

Navigation away from dirty work must follow an explicit policy.

The feature must use one of these approaches:

- Automatic save.
- Explicit save with dirty-state warning.
- Draft persistence.
- Intentional discard.

Do not silently discard work.

If an operation fails after partial completion, tell the user what succeeded and what failed.

### Undo before confirmation

Prefer reversible actions over confirmation dialogs when the action can safely be undone.

For example, an archive operation can complete immediately and provide Undo.

Use confirmation when an action:

- Is destructive.
- Is difficult to reverse.
- Has a large scope.
- Has security consequences.
- Creates external side effects.
- Affects many records.
- Sends communication.
- Starts an expensive process.

A destructive confirmation must identify the affected object and consequence.

Do not ask users to confirm routine, harmless actions.

### Current context

The UI must keep important context visible.

Examples include:

- Tenant.
- Environment.
- Organization.
- Project.
- Selected record.
- Active filter.
- Effective date.
- Time zone.
- Acting identity.
- Delegated identity.

Production and non-production environments must be visibly distinguishable.

The UI must not depend on color alone to communicate the difference.

### Responsive behavior

Responsive behavior must preserve task capability.

A narrow layout may rearrange or collapse controls.

It must not silently remove an essential action.

If an action moves into overflow, its name and keyboard access must remain available.

### Accessibility

WCAG 2.2 AA is the minimum accessibility target for the shared browser component library.

Accessibility must be built into the component API and automated tests where possible.

At minimum, every component must support:

- Keyboard operation.
- Visible focus.
- Programmatic name, role, and value.
- Text alternatives where required.
- Sufficient contrast.
- Status announcements.
- Error identification in text.
- Zoom and reflow.
- Reduced motion.
- Non-color state indicators.
- Non-drag alternatives.
- Predictable help.

WCAG 2.2 specifically adds requirements concerning focus obstruction, dragging, minimum target size, consistent help, and redundant data entry.

---

## Common control presentation

### Buttons
*   **Primary Button:** Only one per section/view. Filled color.
*   **Secondary Button:** Outline or lower contrast.
*   **Tertiary/Text Button:** For less important actions (e.g., "Cancel").
*   **Labeling:** Use verbs. "Save", "Delete", "Publish". Avoid generic "OK" or "Yes".

### Forms
*   **Labels:** Top-aligned labels are generally faster to scan.
*   **Validation:** Inline validation (immediate feedback) is preferred over "submit and fail".
*   **Defaults:** Provide smart defaults whenever possible.

### Icons
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

## Validation and error behavior

### Error placement

Choose the error surface from the failed operation and the interface available to explain it.

| Situation | Presentation |
| --- | --- |
| Invalid value in a visible form | Inline field error, with an error summary when needed |
| Form submission or save fails | The visible form's error summary or persistent operation-status area |
| User command fails without a suitable visible error surface, such as Save on a canvas | Literate error dialog with recovery advice and relevant technical details |
| Background work has an established progress or status surface | Persistent failure state in that surface, with escalation when immediate user action is required |

A Save button alone does not provide a form error surface. Its failed operation can require a literate dialog.
A form's operation error need not attach to a field when the failure is not caused by a field value.
Keep inline errors visible until corrected. Preserve user input and pending changes after a failure.
Do not report a failed command only in technical logs.

Use [literate error content](LITERATE_ERRORS.md) for either presentation.
Browser operation dialogs use the configured [error component](frontend/ERROR_DIALOG_COMPONENT.md).
Native interfaces use their platform equivalent. Bootstrap markup and browser API contracts remain browser-specific.

### Validation levels

Validation must be treated as a pipeline.

A field can require several independent checks.

| Level | Example |
|---|---|
| Lexical | The value contains valid characters |
| Structural | An email has a valid address shape |
| Type | A CEL expression applies an operator to compatible types |
| Range | Percentage is between 0 and 100 |
| Semantic | Referenced service exists |
| Cross-field | End date is after start date |
| Remote | Username is available |
| Policy | Current user may perform the requested operation |
| Conflict | Record changed after the form loaded |
| System | Required backend service is unavailable |

The UI must report the correct level of failure.

Do not show “Invalid value” when the system knows the actual problem.

### Validation timing

Validate early when validation provides useful guidance.

Do not interrupt typing with errors for incomplete values.

Use these general rules:

- Check obvious format requirements during input.
- Check completed values on blur.
- Check related fields when their dependency changes.
- Debounce remote validation.
- Perform authoritative validation before commit.
- Revalidate time-sensitive conditions immediately before the external action.

### Positive validation

Positive validation is useful when success removes uncertainty.

Examples include:

- Username is available.
- Connection test succeeded.
- Expression is valid.
- DNS record was found.
- Recipient was resolved.
- Secret has required permissions.

Do not add green success messages to every ordinary text field.

### Inline errors

Place an error beside or below the field that caused it.

An error must state:

1. What is wrong.
2. How the user can correct it.

GOV.UK recommends an error summary together with field-level errors for forms that contain errors.

Use:

> The end date must be after 19 August 2026.

Do not use:

> Invalid date.

### Form error summary

When a submitted form contains one or more blocking errors:

- Show an error summary near the start of the form.
- List each blocking error.
- Link each error to its field.
- Keep all valid values.
- Keep user-entered invalid values when correction is possible.
- Move focus to the error summary when appropriate.
- Announce the error state to assistive technology.

### Warning versus error

An error blocks completion.

A warning identifies risk but allows completion unless policy says otherwise.

Warnings must use explicit language.

For example:

> This address is outside your organization. You can still send this message.

Do not make a warning look like an error unless the action is actually blocked.

### System errors

A system failure must distinguish the failed operation from invalid user input.

A system error should include:

- User-facing explanation.
- Failed operation.
- Whether data was saved.
- Retry action.
- Recovery action.
- Correlation or request identifier when useful.
- Expandable technical details when appropriate.

The browser library profile uses `Error Dialog` for operation failures selected by [error placement](#error-placement).

---

## Response feedback

*   **Do:** Provide system feedback within 400ms. If loading takes longer, show a skeleton screen or a spinner immediately.
*   **Optimistic feedback:** Keep a pending change distinguishable from confirmed persistence. Preserve recoverable state if the operation fails.

## Progress and long-running operations

### Immediate feedback

When an operation is not immediate, show that the system accepted the action.

Do not leave an enabled button that appears to do nothing.

### Progress states

A long-running operation must identify:

- Queued.
- Running.
- Waiting for input.
- Completed.
- Completed with warnings.
- Failed.
- Canceled.

### Determinate progress

Use determinate progress when the system can calculate meaningful progress.

Use indeterminate progress when it cannot.

Do not show an invented percentage.

### Detailed progress

For multi-stage work, show meaningful steps.

The browser profile uses `Steppable Progress Modal` for blocking multi-stage work with pending, active, done, and error steps.

Show:

- Current step.
- Completed steps.
- Elapsed time.
- Failure location.
- Retry action.
- Cancel action when safe.

### Background work

Do not keep the whole application blocked for work that can continue in the background.

When possible:

- Let users leave the page.
- Keep a persistent job indicator.
- Send completion to the notification center.
- Allow reopening the job details.

---

## Navigation and workspaces

### State preservation

Navigation should preserve meaningful working state.

Examples include:

- Filters.
- Scroll position.
- Selected tab.
- Expanded nodes.
- Open record.
- Split-pane sizes.
- Draft edits.

### Deep links

Important views should have stable, shareable URLs where practical.

The URL should capture enough state to reopen the intended business context.

Do not encode secrets or sensitive transient data in URLs.

### Tabs

Workspace tabs should support:

- Keyboard navigation.
- Close.
- Close others.
- Reorder.
- Pin.
- Unsaved-state indicator.
- Session restoration when appropriate.

Closing a dirty tab must not silently discard changes.

### Context switching

Tenant, workspace, or environment switches must clearly show their effect.

If switching context discards work or changes authorization, warn before the switch.

---

## Save and navigation safety

Await saves whose result controls navigation or a later operation. Do not report success before persistence confirms it.
Coalesce autosave requests without losing mutations made during a pending save.
On failure, retain dirty state and give the user an actionable error.
Follow `instructions/PRAGMATIC_PROGRAMMER.md` when a failed load could otherwise overwrite saved data.
Test switching resources, reopening the app, and opening a deep link from a fresh launch.
Route fresh-launch and in-app navigation through the same resource-loading contract.
For native apps, test the relevant document and scene lifecycle events.

## Await changes before rendering

- **Await Everything:** All data modification functions must be `async` and properly `await`ed before rendering.

## Appearance and component lifecycle

Use the project's semantic appearance tokens and test supported light and dark modes.
Treat foreground and background colors as a pair. Verify contrast in the states where the colors actually meet.
In browser UIs, avoid inline literal colors that prevent theme changes from applying.
Release event listeners, observers, timers, and owned resources when a component is destroyed.
Test capture/restore round trips when a component's state must survive unmounting or virtualization.

## Security and permission behavior

### Authorization

For server-backed applications, the server must remain the authority for authorization.

The UI can hide or disable unavailable actions, but client-side controls are not security enforcement.

### Permission denial

A permission error should state:

- Which action is unavailable.
- Which resource is affected.
- Why the user cannot perform it, when disclosure is safe.
- Which role or approval is required, when known.
- What the user can do next.

### Destructive scope

A destructive action must show its effective scope.

For example:

> Delete 1 environment and its 14 deployment configurations.

Do not use:

> Are you sure?

### Sensitive environments

Production operations should receive stronger visual and confirmation treatment than development operations when the risk differs.

The current environment must remain visible during consequential operations.

---

## Irreversible actions

*   **Confirmation:** Always require confirmation for destructive actions that cannot be easily undone.
*   **Friction:** Add friction to irreversible actions (e.g., "Type 'DELETE' to confirm").
*   **Safety:** Default focus should be on the "Cancel" button, not the "Delete" button in a confirmation dialog.

## Design rule for future components

When a new component enters the library, do not begin by asking which basic control can store its value.

Ask these questions:

1. What does the value mean?
2. What does the user need to understand before changing it?
3. What mistakes can the system detect?
4. What mistakes can the system prevent?
5. What information can the system suggest?
6. What context can the system resolve automatically?
7. What can the user preview or test before committing?
8. What help is available at the point of use?
9. What keyboard pattern already exists for this interaction?
10. What happens when the network, API, or validation service fails?
11. What does the user need to recover from a mistake?
12. What state must persist when the user leaves and returns?
13. What security or permission context changes the behavior?
14. What would make an expert user faster?
15. What would let a new user succeed without becoming an expert?

The resulting component should make the domain easier to use.

It should not merely expose the domain's storage format.

---

## Design prerequisites

Always consider the user experience before finalizing UI or workflow changes.
- Read the configured ADDITIONAL.md refinements. Follow any project-owned experience references explicitly listed there.
- If the intended user flow is unclear, **pause and ask for clarification**.

## UI engineering acceptance checklist

A UI implementation is not complete until the engineer or reviewer checks all applicable items.

### Common behavior

- [ ] The implementation uses semantic controls instead of generic text fields where a semantic control exists.
- [ ] Every field has a visible label.
- [ ] Every field has field-level help.
- [ ] Required fields explain their purpose when the reason is not obvious.
- [ ] Optional fields are identified consistently.
- [ ] All reachable states have an intentional design.
- [ ] User-entered data survives validation and system errors.
- [ ] Loading, empty, warning, and error states are distinct.
- [ ] Disabled controls explain non-obvious restrictions.

### Validation

- [ ] Local validation identifies exact problems.
- [ ] Semantic validation is implemented where the domain permits it.
- [ ] Remote validation handles stale responses.
- [ ] Cross-field constraints are validated.
- [ ] Blocking errors and warnings have different behavior.
- [ ] Form submission errors provide both summary and field-level guidance when needed.
- [ ] Error messages explain how to correct the problem.

### Keyboard and accessibility

- [ ] All normal tasks can be completed with a keyboard.
- [ ] Tab order follows the task order.
- [ ] Composite components use established keyboard conventions.
- [ ] Focus remains visible.
- [ ] Dialogs manage focus correctly.
- [ ] Escape behavior is defined.
- [ ] Drag operations have a non-drag alternative.
- [ ] Important states do not depend on color.
- [ ] Status changes are announced when required.
- [ ] Reduced-motion preferences are respected.
- [ ] Touch targets meet the applicable target-size requirement.

### Async behavior

- [ ] Pending operations have visible feedback.
- [ ] Obsolete responses cannot replace newer results.
- [ ] Retry behavior is defined.
- [ ] Cancel behavior is defined where cancellation is safe.
- [ ] Partial completion is explained.
- [ ] Duplicate mutations are prevented.

### Help

- [ ] Every field has a field-level help topic.
- [ ] Detailed help is available in the contextual help surface.
- [ ] Help explains valid values and important side effects.
- [ ] Help remains accessible without losing current work.
- [ ] Help placement is consistent.

### Security and safety

- [ ] Permission restrictions are represented correctly.
- [ ] Server authorization remains authoritative.
- [ ] Secrets are not exposed in normal logs.
- [ ] Consequential actions show scope before commitment.
- [ ] Production context remains visible during high-risk operations.

### Rich editors

- [ ] Structured languages use an appropriate editor.
- [ ] Language-aware completion is available where practical.
- [ ] Syntax and semantic diagnostics are distinct.
- [ ] Contextual documentation is available.
- [ ] Test or preview behavior exists where execution is meaningful.
- [ ] Generated changes require explicit acceptance.

### People and recipients

- [ ] Selected identities use structured pills.
- [ ] Ambiguous people are distinguishable.
- [ ] Duplicate recipients are detected.
- [ ] External recipients are identifiable without color alone.
- [ ] Available recipient warnings are shown.
- [ ] Final send-time validation occurs when live data is available.

### Grids, trees, and visual interfaces

- [ ] Keyboard navigation follows the relevant established pattern.
- [ ] Focus and selection remain distinct.
- [ ] Drag has an alternative.
- [ ] Loading, empty, and error states are implemented.
- [ ] Important visual information has a structured alternative.
- [ ] Filters and selection scope remain visible.

---

## Research basis

The enterprise browser profiles use the component catalog as their implementation vocabulary.
They name help, form, editor, identity, policy, validation, workflow, and Smart Text Input Engine roles.

The accessibility requirements use WCAG 2.2 and the WAI-ARIA Authoring Practices Guide. These sources define established behavior for keyboard navigation, focus, composite widgets, dragging, target size, and consistent help.

The form and validation rules also use GOV.UK Design System guidance. That guidance emphasizes clear questions, explicit optional fields, field-level errors, and error summaries.

The Expression Workbench requirements use the capabilities of CEL and modern language-aware editors as their technical basis. CEL provides a typed declaration environment that can validate identifiers and function use before runtime.  Language Server Protocol patterns provide a mature model for diagnostics, completion, hover help, and other editor intelligence.

The email recipient requirements use enterprise mail and directory patterns. Microsoft Graph MailTips provides recipient conditions such as automatic replies, delivery restrictions, moderation, external membership, and mailbox-full status.

The writing in this specification follows the supplied language guide. That guide requires clear technical language, direct verbs, consistent terminology, and preservation of technical meaning.
