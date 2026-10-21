<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 297f1b32-2e2d-419a-b24f-8520dc2827c2
Created: 2026
-->

<!-- AGENT: Selectively loaded field, component, editor, and workflow behavior contracts. -->

# UI and UX component profiles

Read the [shared UI/UX baseline](UI_UX.md) with only the profiles that match the changed controls or workflow.
A component may use several profiles. A static page does not inherit expression, directory, or workflow requirements by default.
Catalog names refer to the enterprise browser library profile. They do not imply that every consuming project implements those components.
Native applications use their platform equivalents from [APPS.md](apps/APPS.md), rather than JavaScript options or ARIA APIs.
Client/server authorization requirements apply when the workflow uses a server.

## Select component profiles

| Changed control or workflow | Profile |
| --- | --- |
| Text, names, numbers, money, dates, time zones, secrets, files, or network values | [Data-type behavior requirements](#data-type-behavior-requirements) |
| Expressions, formulas, or policies | [Expression and policy editor](#expression-and-policy-editor) |
| People or email recipients | [People and email recipient editor](#people-and-email-recipient-editor) |
| Forms, schemas, dependencies, or wizard steps | [Forms and dynamic forms](#forms-and-dynamic-forms) |
| Search, autocomplete, filters, or saved views | [Search and filtering](#search-lookup-autocomplete-and-filtering) |
| Pickers | [Pickers and selectors](#pickers-and-selectors) |
| Grids | [Data grids and tables](#data-grids-and-tables) |
| Trees, graphs, or canvases | [Trees, graphs, diagrams, and canvases](#trees-graphs-diagrams-and-canvases) |
| Dialogs, drawers, or popovers | [Overlays](#dialogs-drawers-popovers-and-overlays) |
| Toolbars or command menus | [Toolbars and command surfaces](#toolbars-and-command-surfaces) |
| Charts | [Charts, metrics, and visualizations](#charts-metrics-and-visualizations) |
| Automation | [Workflows, automation, and policy](#workflows-automation-and-policy) |
| AI or agents | [AI and agent interactions](#ai-and-agent-interactions) |
| Browser text enrichment | [Smart Text Input Engine integration](#smart-text-input-engine-integration) |
| Reusable component API or feature specification | [Standard component contract](#standard-component-contract), [feature specification integration](#feature-specification-integration) |

## Data-type behavior requirements

### Plain text

Plain text inputs must support:

- Clear label.
- Length limit when one exists.
- Character count when the limit matters.
- Paste.
- Undo and redo.
- Browser spelling support where appropriate.
- Smart Text Input Engine integration when references are allowed.
- Input-purpose autocomplete when appropriate.

Do not use a textarea only because text might become long.

Choose a single-line input, textarea, rich-text editor, or structured editor based on the task.

### Rich text

Rich-text controls must support:

- Standard keyboard editing.
- Paste sanitization.
- Undo and redo.
- Clear formatting.
- Accessible toolbar navigation.
- Link editing.
- Structured inline tokens when references are supported.
- Plain-text or structured serialization.
- Predictable paste behavior from common office applications.

In the browser profile, Smart Text Input Engine enriches text, rich text, Markdown, CodeMirror, and Monaco inputs.
Domain semantics remain in the host application.

### Identifier, name, and slug

An identifier editor must understand whether the value is:

- User-facing.
- Immutable.
- Case-sensitive.
- Globally unique.
- Unique within a scope.
- Generated automatically.

When the system can generate a safe identifier, offer that value.

If changing an identifier breaks references, explain that consequence before allowing the change.

### Number

Numeric controls must:

- Accept only meaningful numeric syntax.
- Show the expected unit.
- Validate minimum and maximum values.
- Preserve required precision.
- Support keyboard entry.
- Support a stepper only when stepping is useful.
- Format for locale without changing the stored value.

Do not force users to remove display formatting before editing.

### Currency

Currency inputs must show:

- Currency code or symbol.
- Decimal precision.
- Whether tax is included.
- Exchange-rate assumptions when conversion occurs.

Never infer currency only from a symbol when several currencies use that symbol.

### Percentage and ratio

Show whether the stored representation is:

- `25`
- `25%`
- `0.25`

The user must not have to infer the conversion.

### Boolean values

Use a checkbox for independent yes or no choices.

Use a switch when changing the value immediately changes a system state.

Use radio buttons when the domain has two named alternatives that are more meaningful than yes and no.

Do not use a switch for a value that remains unsaved until form submission without making that behavior clear.

### Enumerations

For a small number of stable choices, prefer direct visible choices.

For longer lists, use a searchable selector.

A selector should support:

- Current selection.
- Keyboard navigation.
- Search when useful.
- Descriptions for unfamiliar options.
- Disabled options with reasons.
- Grouping where useful.
- Recently used options when repetition is common.

Do not use placeholder text as the field label.

### Entity reference

An entity lookup must return entities, not strings.

Each result should show enough context to disambiguate it.

Depending on the entity, this can include:

- Name.
- Type.
- Identifier.
- Status.
- Parent.
- Workspace.
- Owner.
- Environment.
- Icon.
- Short description.

Selected entities should become atomic tokens or structured references.

If the entity is deleted, inaccessible, or renamed later, the UI must show that state.

### Tags and taxonomy values

Tag controls must distinguish controlled taxonomy values from freeform tags.

The UI must not make a newly created freeform tag look identical to an existing governed taxonomy value.

When creation is allowed:

- Show an explicit Create action.
- Detect close matches.
- Prevent accidental duplicates.
- Apply normalization rules consistently.
- Show taxonomy ownership where useful.

### Date

Date fields must support both efficient keyboard entry and visual selection.

The UI must:

- Show the expected date format.
- Parse supported human input predictably.
- Validate impossible dates.
- Preserve date-only values without accidental time-zone conversion.
- Offer a calendar picker.
- Support direct year navigation for distant dates.
- Explain business-date constraints.

Examples include:

- Earliest valid date.
- Latest valid date.
- Business days only.
- Fiscal periods.
- Blackout dates.

### Time

Time inputs must show:

- 12-hour or 24-hour convention.
- Time zone when the value has one.
- Minute precision.
- Second precision when required.

Do not display local time without identifying the applicable time zone when ambiguity matters.

### Time zone

Time-zone controls must use stable IANA zone identifiers as the canonical value.

Search results should show:

- City or zone name.
- Current UTC offset.
- Daylight-saving behavior when useful.
- Common aliases where appropriate.

Do not store only the current UTC offset for a regional time zone.

### Duration

A duration control must distinguish duration from clock time.

Allow users to enter meaningful units such as:

- Days.
- Hours.
- Minutes.
- Seconds.

Show a normalized human-readable representation.

### Secrets and sensitive values

Secrets must use the library's masked-value behavior.

The default display must not reveal the full secret.

The control should support:

- Explicit reveal.
- Copy.
- Clear reveal state.
- Rotation.
- Expiration status.
- Scope.
- Last-used information when available.

Do not write secrets to normal client logs, analytics events, or error reports.

### Files

A file control must support keyboard file selection in addition to drag and drop.

Before upload, show:

- Accepted file types.
- Maximum size.
- Maximum count.
- Other relevant restrictions.

During upload, show progress for each file.

After failure, allow retry for the failed file without restarting successful uploads.

The system must distinguish:

- Upload complete.
- Processing.
- Security scan pending.
- Processing failed.
- Rejected.
- Ready.

### URL, host, domain, and network values

Network-related fields must use the correct semantic validator.

Do not treat these values as interchangeable:

- URL.
- Hostname.
- Domain.
- IPv4 address.
- IPv6 address.
- CIDR range.
- URI template.

When testing connectivity is possible, provide a Test action.

The test must identify whether failure occurred during DNS, transport, TLS, authentication, or application validation.

---

## Expression and policy editor

### Requirement

Any field that accepts an executable expression must use an **Expression Workbench** behavior.

This applies to CEL, formulas, policy expressions, conditional rules, query expressions, and similar languages.

A plain textarea is not an acceptable primary editor for these values.

The browser profile names Policy Rule Editor for nested conditions, simulation, precedence, and version history.
Expression Workbench applies the same principle to source-oriented expression languages.

### Interaction modes

The workbench must support these modes when the language permits them:

#### Builder

A structured visual editor lets users build expressions from fields, operators, functions, values, and logical groups.

The builder must prevent structurally invalid combinations where possible.

#### Source

An expert editor exposes the exact expression.

The editor must provide:

- Syntax highlighting.
- Line and column information.
- Bracket matching.
- Automatic indentation.
- Completion.
- Diagnostics.
- Hover documentation.
- Signature help.
- Type information.
- Formatting.
- Search.
- Undo and redo.

Language Server Protocol patterns standardize editor features such as completion, diagnostics, hover information, and language-aware assistance.

#### Explain

The system translates the current expression into plain language.

For example:

```text
request.user.department == "Finance" &&
resource.classification != "Restricted"
```

can display:

> Allow this condition only when the user's department is Finance and the resource is not Restricted.

The explanation must identify assumptions when the source is ambiguous.

#### Generate

Users can describe the required rule in natural language.

The system can propose an expression.

Generated expressions must never silently replace the existing expression.

The user must see:

1. The requested intent.
2. The generated expression.
3. A plain-language interpretation.
4. Diagnostics.
5. An explicit Apply action.

#### Test

Users can evaluate an expression with controlled input data.

#### Trace

Users can inspect how the evaluator reached the result.

This is an evaluation trace, not a traditional source-code debugger.

### Language environment

Every expression editor must receive a language environment from its host application.

The environment should describe:

- Available variables.
- Variable types.
- Object fields.
- Functions.
- Function overloads.
- Macros.
- Constants.
- Enumerations.
- Deprecated elements.
- Documentation.
- Examples.
- Security classification when useful.

CEL specifically supports declarations that its type checker can use to verify identifier and function references.

Completion must therefore be based on the actual host environment.

Do not provide generic CEL completion when the application exposes a narrower environment.

### Contextual completion

Completion should understand the expression at the cursor.

For example, after:

```text
request.user.
```

the editor should suggest only valid fields on `request.user`.

A suggestion row should show:

- Name.
- Type.
- Short description.
- Source.
- Deprecation state.
- Example value when useful.

Function completion should show signatures and parameter descriptions.

### Diagnostics

Diagnostics must include:

- Severity.
- Message.
- Line.
- Column.
- Affected expression.
- Suggested correction when one is known.

The workbench must distinguish:

- Syntax error.
- Unknown identifier.
- Unknown field.
- Type mismatch.
- Invalid function overload.
- Invalid literal.
- Deprecated feature.
- Runtime-only failure.

Diagnostics should update while the user edits.

The update must be debounced so that validation does not interfere with typing.

### Contextual documentation

Selecting or hovering over a symbol should provide contextual help.

The help can show:

- Definition.
- Type.
- Allowed values.
- Examples.
- Related functions.
- Security meaning.
- Source system.
- Link to the detailed help topic.

The help drawer should synchronize with the selected expression element when the user requests this behavior.

### Builder and source synchronization

Builder and source modes must represent the same canonical expression.

Switching modes must not change semantic meaning.

If the source contains syntax that the visual builder cannot represent:

- Preserve the source.
- Explain the unsupported construct.
- Keep Source mode available.
- Do not silently simplify the expression.

### Test data

Test mode must provide a fixture for all referenced inputs.

The system should generate initial sample values from the environment schema.

Users must be able to replace the generated values.

Test cases should support:

- Name.
- Input values.
- Expected result.
- Actual result.
- Pass or fail state.
- Notes.

Users should be able to save multiple test cases with a policy.

### Evaluation trace

Trace mode should show the expression as a tree of subexpressions.

For each evaluated subexpression, show:

- Source expression.
- Input values.
- Result.
- Result type.
- Evaluation order.
- Short-circuit behavior.
- Error, if one occurred.

For example:

```text
A && B
```

can show:

```text
A = false
B = not evaluated
Result = false
Reason: AND short-circuited after A
```

The trace must reflect the behavior of the real evaluator.

Do not simulate behavior that differs from production semantics.

### Sandbox behavior

Test evaluation must not create production side effects.

The evaluator should enforce appropriate:

- Time limits.
- Memory limits.
- Data access controls.
- Function restrictions.
- Output limits.

If an expression can invoke side-effecting extensions, Test mode must mock or block those operations.

### Runtime identity

The workbench must identify the environment used for validation and testing.

Show, when applicable:

- Language.
- Language version.
- Runtime version.
- Schema version.
- Policy version.
- Environment.
- Last refresh time.

If the environment changed after the editor loaded, warn before publish.

### Publish workflow

Editing, testing, and publishing must be separate concepts.

Before publishing a policy, show:

- Current expression.
- Validation state.
- Test results.
- Changes from the current published version.
- Scope of effect.
- Effective time.
- Author.
- Required approvals.

High-impact policies should support simulation against representative real or synthetic scenarios before activation.

---

## People and email recipient editor

### Semantic model

A To, Cc, or Bcc control is an identity editor.

It is not a multi-value text field.

Selected recipients must use structured identity objects.

Each identity can include:

- Stable identity identifier.
- Display name.
- Canonical email address.
- Avatar.
- Organization.
- Role or title.
- Domain.
- Internal or external state.
- Presence.
- Directory source.
- Delivery status metadata.

The browser profile names `PersonChip` and `PeoplePicker` for this interaction.

### Recipient entry

The editor must support:

- Typing a name.
- Typing an email address.
- Pasting one address.
- Pasting a list of addresses.
- Directory search.
- Group search.
- Recent recipients.
- Frequent recipients.
- Keyboard selection.

A selected recipient becomes an atomic pill.

Backspace at the start of an empty input should first select the previous pill.

A subsequent Backspace can remove it.

### Suggestions

Suggestions should rank meaningful candidates.

Possible ranking signals include:

- Exact match.
- Prefix match.
- Recent use.
- Frequent use.
- Same team.
- Same organization.
- Current collaboration context.

A result should show enough information to distinguish people with similar names.

At minimum, show name and address when ambiguity exists.

### Identity resolution

The control must distinguish:

- Resolved internal identity.
- Resolved external identity.
- Valid but unresolved address.
- Invalid address.
- Distribution group.
- External group.
- Disabled account.
- Unknown address.

Do not make all these states look identical.

### Duplicate handling

The editor must detect duplicate recipients across To, Cc, and Bcc.

If the same canonical recipient appears more than once, prevent duplication or explain the existing location.

Aliases that resolve to the same identity should also be treated as duplicates when the directory can determine this.

### Rich people cards

Hover or keyboard focus on a resolved person should offer a people card.

The card can show:

- Full name.
- Address.
- Title.
- Organization.
- Location.
- Presence.
- Manager.
- Contact actions.
- Relevant relationship.

The card must respect directory permissions.

### Domain awareness

External recipients must be visually identifiable.

Do not use color as the only external indicator.

The editor can use:

- External icon.
- Domain label.
- Pill treatment.
- Warning text.

Different external domains can receive distinct visual treatment when that information helps users detect mistakes.

### Recipient intelligence

Before sending, the application should evaluate available recipient intelligence.

Microsoft Graph MailTips can expose recipient information such as automatic replies, delivery restrictions, moderation requirements, external group membership, and mailbox-full state.

The editor should surface relevant conditions such as:

- Recipient is out of office.
- Mailbox is full.
- Recipient cannot accept the message.
- Message requires moderation.
- Group contains external members.
- Recipient is outside the organization.
- Recipient belongs to a very large audience.
- Address previously bounced, when delivery history is available.

A previous-bounce warning must come from the application's actual delivery history.

Do not infer a bounce from an unrelated signal.

### Typo protection

The editor should detect likely errors such as:

- Misspelled common domains.
- Similar internal names.
- Similar addresses.
- Confusable display names.
- An address that differs from a frequent recipient by one character.

A correction must remain a suggestion.

Do not silently replace a valid address.

### Send-time validation

Recipient state can change after composition begins.

Perform final validation immediately before sending when the application supports live recipient checks.

The final check should identify new blocking conditions.

Do not repeat low-value warnings that the user already acknowledged unless their meaning changed.

### Large audiences

When a message has a large audience:

- Show the approximate recipient count.
- Identify distribution groups.
- Identify external recipients.
- Consider recommending Bcc for suitable external bulk communication.
- Require confirmation when policy defines the audience as high risk.

### Privacy

Do not expose hidden group membership without permission.

Do not reveal private directory data merely because the user typed part of a name.

Search results must follow the same authorization policy as other directory views.

---

## Forms and dynamic forms

The Dynamic Form Builder profile covers conditional visibility, schema-defined fields, async validation, and read-only or edit modes.
These capabilities inherit the common form behavior below.

### Layout

Forms should follow the user's reading and completion order.

Prefer one logical column when fields have dependencies.

Use multiple columns when the fields are short, independent, and naturally related.

Do not use columns only to reduce vertical length.

### Sections

Group fields by task or concept.

A section heading must explain its subject.

Long forms should support:

- Section navigation.
- Completion status.
- Error counts.
- Save state.
- Help context.

### Conditional fields

When one value reveals another field:

- Insert the field in a predictable location.
- Announce the change to assistive technology when needed.
- Move focus only when the workflow requires it.
- Define what happens to hidden values.

A schema must specify one hidden-value policy:

- Preserve value.
- Clear value.
- Reset to default.

Do not let the implementation make this decision accidentally.

### Required fields

A field schema should support:

```text
required: true
requiredReason: "Used to determine the approval chain."
```

The `requiredReason` should be displayed when the reason is not obvious.

### Read-only values

A read-only field should remain readable and selectable.

Use disabled state only when interaction itself is unavailable.

If a field is read-only because of permission or process state, explain the reason.

### Save behavior

Every form must clearly communicate:

- Unsaved.
- Saving.
- Saved.
- Save failed.
- Conflict detected.

Automatic save must not make failure invisible.

### Multi-step forms

A wizard must:

- Show the current step.
- Show overall progress.
- Permit Back without losing completed values.
- Validate each step before dependent steps.
- Allow draft save when the workflow is long.
- Provide a review step for consequential submissions.

---

## Search, lookup, autocomplete, and filtering

### Search input

Search must provide immediate acknowledgement after input.

Remote searches should use a short debounce.

Search requests must prevent stale-result races.

### Search states

Search must distinguish:

- No query.
- Searching.
- Results.
- No results.
- Search failed.
- Partial results.
- More results available.

A no-results state should repeat the query and suggest a useful next action.

### Autocomplete

Autocomplete must support:

- Arrow navigation.
- Active-item indication.
- Enter to choose.
- Escape to close.
- Mouse or touch selection.
- Loading state.
- Empty state.
- Async results.

Focus should normally remain in the input.

### Structured search

When the product supports structured facets, the search control should understand them.

For example:

```text
status:open owner:@me environment:prod
```

The editor should provide completion for both facet names and values.

Invalid facets should receive expression-style diagnostics.

### Saved views

A saved view should capture all state that defines the view.

This can include:

- Query.
- Filters.
- Sorting.
- Grouping.
- Visible columns.
- Column order.
- Pinning.
- Density.
- Visualization mode.

The UI must identify whether a view is personal or shared.

---

## Pickers and selectors

Every picker must support both discovery and efficient repeat use.

### Common picker behavior

A picker should support, where applicable:

- Search.
- Keyboard navigation.
- Current value.
- Clear.
- Recent values.
- Favorites.
- Grouping.
- Disabled values.
- Descriptions.
- Preview.
- Custom value.
- Empty state.

### Visual values

Visual values should be shown visually.

Examples include:

- Fonts rendered in the font.
- Line widths rendered at the width.
- Line endings shown as line endings.
- Gradients shown as gradients.
- Page sizes shown proportionally.
- Layout algorithms shown with diagrams.

The browser picker profiles use this visual-selection pattern.

### Recent choices

Use most-recently-used suggestions when repeated selection is common.

Do not let recency reorder safety-critical enumerations whose order has semantic meaning.

---

## Data grids and tables

### Keyboard model

A data grid is a composite widget.

Tab should enter or leave the grid.

Arrow keys should navigate cells where the grid supports cell focus.

Selection and keyboard focus must remain separate concepts.

### Sorting

A sortable column must show:

- Whether sorting is active.
- Sort direction.
- Sort precedence when multiple columns are sorted.

Sorting must be available by keyboard.

### Filtering

Column filters must identify active filters.

A user must be able to clear:

- One filter.
- All filters.

The result count should update when practical.

### Editing

Editable cells must provide a consistent editing convention.

Recommended defaults are:

- `Enter` or `F2` starts editing.
- `Enter` commits.
- `Escape` cancels.
- `Tab` commits and moves to the next editable cell.

The application may change these conventions when another established domain convention is stronger.

### Bulk operations

When rows are selected, show a contextual action surface.

The surface should identify:

- Number selected.
- Selection scope.
- Available actions.
- Destructive actions.
- Whether hidden or paged rows are included.

“Select all” must state whether it means:

- Visible page.
- Loaded rows.
- All filtered results.

### Data states

Every grid must implement:

- Loading.
- Empty.
- No matching filters.
- Error.
- Partial.
- Stale.

Do not show the same blank grid for all states.

### Column customization

If columns can be resized, reordered, hidden, or pinned, provide non-drag alternatives.

Persist personal column configuration when the product benefits from it.

---

## Trees, graphs, diagrams, and canvases

### Tree navigation

Trees must use standard hierarchical keyboard behavior.

Users must be able to:

- Move between visible nodes.
- Expand and collapse.
- Move to parent.
- Move to first child.
- Activate a node.
- Select independently when selection differs from activation.

### Graph and canvas navigation

A visual graph must not require a mouse for essential inspection.

Provide keyboard commands for:

- Next node.
- Previous node.
- Connected nodes.
- Zoom in.
- Zoom out.
- Fit to view.
- Reset view.
- Open details.

Large graphs should provide search and a minimap.

The minimap must not be the only navigation method.

### Accessible alternative

A graph that communicates important data should provide a structured alternative.

Depending on the graph, this can be:

- Tree.
- List.
- Table.
- Relationship list.
- Text summary.

### Selection and detail

Selecting a visual object should expose a detail surface.

The detail surface should identify the selected object's:

- Name.
- Type.
- Status.
- Properties.
- Relationships.
- Actions.

### Drag editing

Node movement and edge creation must provide alternatives when these operations are necessary for task completion.

Undo must be available for direct-manipulation edits.

---

## Dialogs, drawers, popovers, and overlays

### Modal dialogs

Use a modal when the user must resolve the interaction before continuing.
A literate failure dialog also explains a failed user command that has no suitable visible error surface.
Use [error placement](UI_UX.md#error-placement) to distinguish that operation from visible form errors.

A modal must:

- Move focus into itself.
- Trap focus.
- Provide a clear title.
- Provide an obvious completion action.
- Provide a cancellation path when cancellation is valid.
- Respond to Escape where safe.
- Return focus after close.

### Drawers

Prefer a non-modal drawer when the user benefits from seeing the parent context.

Examples include:

- Help.
- Properties.
- Preview.
- Related records.
- Filters.

A drawer should not trap focus unless it intentionally acts as a modal.

### Popovers

A popover should remain attached to its source.

It must close predictably.

Escape should normally close it and restore normal interaction.

A popover must not contain a complex multi-step workflow when a drawer or dialog would work better.

### Nested overlays

Avoid nested modal dialogs.

If a modal task requires secondary selection, prefer an in-dialog picker, popover, or side panel.

---

## Toolbars and command surfaces

### Commands

A command surface must distinguish:

- Command.
- Toggle.
- Selector.
- Menu.
- Split command.

Do not use the same visual treatment for controls with different behavior.

### Disabled commands

A disabled command should expose the reason when the reason is not obvious.

For example:

> Delete is unavailable because you do not have permission to delete production services.

### Keyboard behavior

Toolbars should use a single Tab stop when they contain many controls.

Arrow keys should move between toolbar items.

Important commands should expose their keyboard shortcut.

### Overflow

Responsive overflow must preserve:

- Command name.
- State.
- Keyboard access.
- Tooltip.
- Shortcut.
- Permission behavior.

---

## Charts, metrics, and visualizations

### Data meaning

A visualization must identify:

- Metric.
- Unit.
- Time range.
- Time zone when relevant.
- Aggregation.
- Comparison period.
- Data source when useful.
- Freshness when useful.

### Color

Color must not be the only encoding for an important state.

Use another cue such as:

- Text.
- Icon.
- Pattern.
- Shape.
- Line style.
- Position.

### Tooltips

Data tooltips must be available through keyboard focus when the chart supports individual-point interaction.

A tooltip should show exact values rather than forcing users to estimate from the chart.

### Data alternative

Charts that communicate decision-relevant values must expose an accessible data alternative.

The browser `Chart Panel` profile uses a table for screen readers.

### Cross-filtering

When chart selection filters other components:

- Show the active filter.
- Provide a clear action.
- Keep filter state synchronized.
- Make the relationship visible.

---

## Workflows, automation, and policy

### Visual builders

Workflow builders must provide structured creation rather than raw configuration where practical.

A node should expose:

- Name.
- Type.
- Inputs.
- Outputs.
- Validation state.
- Execution state.
- Help.
- Configuration.

### Validation

A workflow must validate both local and whole-flow constraints.

Examples include:

- Missing required configuration.
- Invalid connection.
- Incompatible data types.
- Unreachable nodes.
- Cycles where cycles are forbidden.
- Missing terminal path.
- Permission mismatch.

### Test and simulation

Workflow and policy editors should provide test or dry-run behavior.

The browser profiles include simulation for policy rules and dry-run execution for workflow tooling.

Testing should show:

- Test input.
- Path taken.
- Conditions evaluated.
- Actions that would execute.
- Outputs.
- Warnings.
- Failures.

### Production activation

Publishing an automation should identify:

- Scope.
- Trigger.
- Effective environment.
- Side effects.
- Required credentials.
- Changed behavior.
- Test status.

A material change should provide a diff against the active version.

---

## AI and agent interactions

### AI suggestions

AI-generated output must remain distinguishable from committed application state.

The UI must identify when content is:

- Suggested.
- Generated.
- Reviewed.
- Applied.
- Published.

### Applying changes

An AI action that changes structured data should provide a preview when practical.

For code, policy, configuration, or documents, show a diff before applying consequential changes.

### Agent actions

Before a consequential agent action, the UI should show:

- Intended action.
- Target.
- Scope.
- Relevant parameters.
- Expected side effects.
- Required permission.
- Approval requirement.

### Human control

Agent workflows must support human intervention when the workflow requires judgment or approval.

The browser profile names context, recommendation, override, escalation, and batch review as human-intervention roles.

### Trace and explanation

Show observable execution information such as:

- Tool calls.
- Inputs.
- Outputs.
- Timing.
- Errors.
- Data sources.
- Policy checks.
- Concise rationale summaries.

Do not make the product depend on exposing hidden model chain-of-thought.

### Failure and retry

Regeneration or retry must not destroy the previous result.

Users should be able to compare the old and new result when the difference matters.

---

## Smart Text Input Engine integration

The catalog defines the Smart Text Input Engine as a reusable behavioral layer for mentions, references, formulas, and commands. It supports adapters for plain inputs, rich text, CodeMirror, and Monaco.

Use STIE only for text-oriented controls.

Do not attach STIE to structured controls such as password, numeric, date, select, file, or read-only inputs. The catalog explicitly excludes these cases.

STIE-enabled inputs must preserve the standard keyboard contract.

Its autocomplete behavior must:

- Keep focus in the editor.
- Support arrow navigation.
- Support Enter selection.
- Support Escape cancellation.
- Announce inserted tokens.
- Expose active results through ARIA.

These behaviors form the STIE browser accessibility profile.

---

## Component-family mapping

Each catalog family inherits the following additional requirements.

| Catalog family | Required behavior profiles |
|---|---|
| Pickers | Picker, typed value, validation, keyboard, help |
| Progress | Async state, cancel, retry, system feedback |
| Dialogs | Focus management, keyboard, dirty-state protection |
| Data entry | Form field, typed value, validation, help |
| Rich content editing | Editor, keyboard, serialization, STIE where applicable |
| Code and expression editing | Editor, language intelligence, diagnostics, test |
| Data grids | Grid navigation, filtering, selection, editing, async state |
| Trees | Tree navigation, selection, expansion, drag alternative |
| Toolbars | Composite keyboard model, command state, overflow |
| Status surfaces | Live state, accessible announcements, non-color encoding |
| Containers | Focus order, responsive behavior, state persistence |
| AI components | AI state, human control, trace, change preview |
| Metrics and charts | Units, data alternative, focus, filtering, freshness |
| Timelines and activity | Time zone, ordering, filtering, expandable detail |
| Onboarding | Dismissal, persistence, keyboard, reduced motion |
| Help | Field context, detailed topic, persistent drawer |
| Search and filtering | Async search, autocomplete, stale response protection |
| File management | File validation, progress, retry, non-drag input |
| Workspace navigation | Context, deep links, persistence, keyboard |
| Governance and security | Permission state, masking, auditability |
| Collaboration | Identity, mentions, people cards, notifications |
| Workflow and automation | Validation, simulation, versioning, publish safety |
| Kanban and layout | Drag alternative, keyboard movement, undo |
| Feedback controls | Consistent status vocabulary and live announcements |
| Dynamic forms | Field schema, dependencies, required reasons, async validation |
| Policy editors | Builder, source where applicable, simulation, precedence |
| Operational queues | Keyboard triage, bulk actions, SLA context |
| Process intelligence | Accessible graph alternative, drill-down, metric definitions |
| Agent management | Permissions, guardrails, cost, trace, human intervention |
| Dynamic canvas | Keyboard selection, non-drag operations, focus model |

A component can inherit more than one row.

For example, a CEL field inside a Dynamic Form inherits:

```text
Common baseline
  + Dynamic form
  + Expression editor
  + Validation
  + Help
  + Async state
  + Security, if the expression controls access
```

An email To field inherits:

```text
Common baseline
  + People and email
  + Autocomplete
  + Entity reference
  + Validation
  + Help
  + Async state
```

---

## Standard component contract

Every reusable component should document the following contract.

```text
Component:
Purpose:

Semantic data:
Primary user tasks:

States:
- idle
- focused
- loading
- pending
- ready
- empty
- valid
- warning
- invalid
- disabled
- read-only
- error

Keyboard:
- entry
- internal navigation
- activation
- cancellation
- exit
- shortcuts

Pointer:
- click behavior
- hover behavior
- drag behavior
- non-drag alternative

Validation:
- local
- semantic
- remote
- cross-field
- policy

Help:
- inline guidance
- HelpTooltip topic
- HelpDrawer topic
- examples

Async behavior:
- loading
- stale-response handling
- retry
- cancellation
- partial results

Persistence:
- current value
- dirty state
- layout state
- recent values

Accessibility:
- role
- name
- value
- descriptions
- focus
- live announcements
- reduced motion
- non-color indicators

Security:
- permissions
- sensitive values
- logging restrictions

Telemetry:
- meaningful user actions
- errors
- latency
- abandonment where useful

Test requirements:
- unit
- interaction
- keyboard
- accessibility
- async race
- error states
```

A new component is incomplete until this contract is defined.

---

## Feature specification integration

Every UI feature specification should contain a short **Experience requirements** section.

The section should identify inherited requirements rather than repeating this document.

Example:

```text
## Experience requirements

Baseline:
- Enterprise UI Experience Baseline Specification

Data types:
- Person
- Email recipient
- Date and time
- CEL expression

Component families:
- Dynamic Form
- People Picker
- Expression Workbench
- Form Dialog

Special requirements:
- Sending to an external domain requires a warning.
- Policy tests use the tenant's current CEL declaration environment.
- The form can be saved as a draft.
```

This structure keeps feature specifications focused on domain behavior.

It also makes common experience requirements enforceable without copying them into every feature.

---

## Overlay selection examples

*   **Use Modals for:** Critical decisions, simple forms that don't require context from the main page, or "interruption" tasks.
*   **Use Inline/Sidebars for:** Complex configurations, context-dependent editing (properties panel), or tasks that allow referencing the main content.
