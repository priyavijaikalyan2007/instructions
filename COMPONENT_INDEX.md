<!-- AGENT: Auto-generated — do not edit. Run `npm run build` to regenerate. -->

# Component Index

106 implemented components. Use this file for quick lookup; see each component's README for full API details.

Full reference (all READMEs in one file): [COMPONENT_REFERENCE.md](COMPONENT_REFERENCE.md)

## Date, Time & Pickers

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| anglepicker | A circular dial input for selecting angles from 0 to 360 degrees. | `createAnglePicker()` | [README](components/anglepicker/README.md) |
| colorpicker | A canvas-based colour selection control with saturation/brightness gradient, vertical hue strip, optional opacity sli... | `createColorPicker()` | [README](components/colorpicker/README.md) |
| columnspicker | A dropdown showing column layout presets with visual SVG page thumbnails. | `createColumnsPicker()` | [README](components/columnspicker/README.md) |
| cronpicker | A visual builder for extended 6-field CRON expressions (second, minute, hour, day-of-month, month, day-of-week) with ... | `createCronPicker()` | [README](components/cronpicker/README.md) |
| datepicker | A calendar date picker with day, month, and year navigation views. | `createDatePicker()` | [README](components/datepicker/README.md) |
| durationpicker | A duration/interval picker with configurable unit patterns and ISO 8601 support. | `createDurationPicker()` | [README](components/durationpicker/README.md) |
| gradientpicker | A gradient colour picker that enables users to create, edit, and preview linear and radial gradients with full alpha ... | `createGradientPicker()` | [README](components/gradientpicker/README.md) |
| lineendingpicker | A dropdown picker that displays line ending (arrowhead / marker) styles with inline SVG previews, letting users selec... | `createLineEndingPicker()` | [README](components/lineendingpicker/README.md) |
| lineshapepicker | A dropdown picker that displays line shape/routing patterns with inline SVG previews, letting users select connector ... | `createLineShapePicker()` | [README](components/lineshapepicker/README.md) |
| linetypepicker | A dropdown picker that displays line dash patterns with inline SVG previews, letting users select stroke styles for g... | `createLineTypePicker()` | [README](components/linetypepicker/README.md) |
| linewidthpicker | A dropdown picker that displays line widths with visual CSS border previews, letting users select stroke thickness fo... | `createLineWidthPicker()` | [README](components/linewidthpicker/README.md) |
| marginspicker | A dropdown component showing page margin presets with visual page thumbnails, modelled after Microsoft Word's Margins... | `createMarginsPicker()` | [README](components/marginspicker/README.md) |
| orientationpicker | A simple dropdown picker for selecting page orientation (Portrait or Landscape). | `createOrientationPicker()` | [README](components/orientationpicker/README.md) |
| peoplepicker | Searchable person selector for share dialogs, assignment fields, and permission lists. | `createPeoplePicker()` | [README](components/peoplepicker/README.md) |
| periodpicker | Coarse time-period selector for enterprise project planning. | `createPeriodPicker()` | [README](components/periodpicker/README.md) |
| sizespicker | A dropdown listing page and frame sizes with proportional page thumbnails and dimensions. | `createSizesPicker()` | [README](components/sizespicker/README.md) |
| spacingpicker | A dropdown showing line/paragraph spacing presets with visual SVG thumbnails. | `createSpacingPicker()` | [README](components/spacingpicker/README.md) |
| sprintpicker | Agile sprint selector with list and calendar views. | `createSprintPicker()` | [README](components/sprintpicker/README.md) |
| symbolpicker | A grid-based symbol and icon picker for inserting Unicode characters and Bootstrap Icons. | `createSymbolPicker()` | [README](components/symbolpicker/README.md) |
| timepicker | A time-of-day picker with spinner columns and optional timezone selector. | `createTimePicker()` | [README](components/timepicker/README.md) |
| timezonepicker | A searchable dropdown selector for IANA timezones with grouped regions, UTC offset display, and live current-time pre... | `createTimezonePicker()` | [README](components/timezonepicker/README.md) |
| toolcolorpicker | A visual colour picker that displays colours as tool icons (pens, markers, pencils, highlighters, brushes). | `createToolColorPicker()` | [README](components/toolcolorpicker/README.md) |

## Inputs & Selection

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| editablecombobox | A combined text input and dropdown list component built on Bootstrap 5. | `createEditableComboBox()` | [README](components/editablecombobox/README.md) |
| maskedentry | A specialised input field that masks sensitive non-password data — API keys, tokens, SSNs, connection strings, and si... | `createMaskedEntry()` | [README](components/maskedentry/README.md) |
| multiselectcombo | A multi-select combo box that allows users to choose multiple items from a filterable dropdown list. | `createMultiselectCombo()` | [README](components/multiselectcombo/README.md) |
| searchbox | A debounced search input with search icon, clear button, loading spinner, and optional suggestions dropdown. | `createSearchBox()` | [README](components/searchbox/README.md) |

## Content & Editing

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| codeeditor | Bootstrap 5-themed code editor wrapping CodeMirror 6 with syntax highlighting, toolbar, and diagnostics. | `createCodeEditor()` | [README](components/codeeditor/README.md) |
| commentoverlay | Transparent overlay system for anchoring comment pins to DOM elements, enabling inline annotation with threaded discu... | `createCommentOverlay()` | [README](components/commentoverlay/README.md) |
| fileupload | A drag-and-drop file upload zone with progress bars, file type validation, size limits, batch upload, and an optional... | `createFileUpload()` | [README](components/fileupload/README.md) |
| markdowneditor | A Bootstrap 5-themed Markdown editor wrapper around [Vditor](https://github.com/Vanessa219/vditor) with tab/side-by-s... | `createMarkdownEditor()`, `showMarkdownEditorModal()`, `created()`, `showOverflowIndicator()` | [README](components/markdowneditor/README.md) |

## Data Display

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| datagrid | High-performance flat data table with sorting, filtering, pagination, column resize, row selection, inline editing, v... | `createDataGrid()`, `showColumn()` | [README](components/datagrid/README.md) |
| fileexplorer | Two-pane file navigation component with a folder tree sidebar, breadcrumb navigation, three view modes (grid, list, d... | `createFileExplorer()` | [README](components/fileexplorer/README.md) |
| treeview | A highly configurable, generic tree view component for representing multi-tree structured data. | `createTreeView()` | [README](components/treeview/README.md) |

## Data Visualization

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| activityfeed | Social-style activity feed with date grouping, infinite scroll, real-time additions, and compact mode. | `createActivityFeed()` | [README](components/activityfeed/README.md) |
| gauge | A visual measure component modeled after the ASN.1 Gauge type. | `createTileGauge()`, `createRingGauge()`, `createGauge()`, `createBarGauge()` | [README](components/gauge/README.md) |
| timeline | A horizontal event timeline component for displaying point and span events along a time axis. | `createTimeline()`, `showDetailPanel()` | [README](components/timeline/README.md) |

## Search & Filtering

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| commandpalette | Keyboard-first command palette (Ctrl+K omnibar) for searching and executing registered commands with fuzzy matching, ... | — | [README](components/commandpalette/README.md) |
| facetsearch | Facet-aware search bar that combines free-text search with structured `key:value` query facets. | `createFacetSearch()` | [README](components/facetsearch/README.md) |
| tagger | Combined freeform and controlled-vocabulary tag input with autocomplete, colored chips, taxonomy categories, and vali... | `createTagger()` | [README](components/tagger/README.md) |

## Dialogs & Modals

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| confirmdialog | A general-purpose confirmation modal with customizable title, message, icon, buttons, and a promise-based API. | `showConfirmDialog()`, `showDangerConfirmDialog()` | [README](components/confirmdialog/README.md) |
| errordialog | A Bootstrap 5 modal that displays literate error messages with user-friendly narrative and collapsible technical deta... | `showErrorDialog()` | [README](components/errordialog/README.md) |
| progressmodal | A modal dialog for displaying progress of long-running operations. | `showProgressModal()`, `showSteppedProgressModal()` | [README](components/progressmodal/README.md) |

## Feedback & Status

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| emptystate | A centered placeholder component shown when a view, list, table, or container has no data. | `createEmptyState()`, `showAction()` | [README](components/emptystate/README.md) |
| skeletonloader | Animated placeholder component that mimics content layout during loading. | `createSkeletonLoader()` | [README](components/skeletonloader/README.md) |
| statusbadge | Colour-coded pills/dots communicating process or system state with animated pulse and click-for-detail support. | `createStatusBadge()` | [README](components/statusbadge/README.md) |
| toast | A transient, non-blocking notification system with stacking, auto-dismiss, progress bar, and action support. | `showSuccessToast()`, `showErrorToast()`, `showToast()`, `showInfoToast()`, `showWarningToast()` | [README](components/toast/README.md) |

## Bars & Toolbars

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| bannerbar | A fixed-to-top viewport banner for announcing significant events such as service status updates, critical issues, mai... | `createBannerBar()`, `showBanner()` | [README](components/bannerbar/README.md) |
| graphtoolbar | Factory function that creates a preconfigured Toolbar instance for graph visualization applications. | `createGraphToolbar()` | [README](components/graphtoolbar/README.md) |
| statusbar | A fixed-to-bottom viewport status bar with configurable label/value regions separated by pipe dividers. | `createStatusBar()` | [README](components/statusbar/README.md) |
| toolbar | A programmable action bar component for grouping tools and actions into labelled regions. | `createToolbar()`, `showKeyTips()`, `createDockedToolbar()`, `createFloatingToolbar()` | [README](components/toolbar/README.md) |

## Panels & Navigation

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| sidebar | A dockable, floatable, resizable sidebar panel component that acts as a container for other components. | `createDockedSidebar()`, `createFloatingSidebar()`, `createSidebar()` | [README](components/sidebar/README.md) |
| tabbedpanel | A dockable, collapsible, resizable tabbed panel component for grouping related content into tabs. | `createTabbedPanel()`, `createDockedTabbedPanel()`, `createFloatingTabbedPanel()` | [README](components/tabbedpanel/README.md) |

## Identity & Navigation

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| usermenu | Avatar-triggered dropdown menu for user account actions. | `createUserMenu()` | [README](components/usermenu/README.md) |
| workspaceswitcher | Dropdown or modal control for switching between organisational workspaces and tenants. | `createWorkspaceSwitcher()` | [README](components/workspaceswitcher/README.md) |

## AI & ML

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| conversation | A programmable turn-by-turn conversation UI component for AI agent interactions in enterprise SaaS applications. | `createConversation()`, `showTypingIndicator()` | [README](components/conversation/README.md) |
| prompttemplatemanager | Two-pane CRUD interface for creating, editing, organising, and testing prompt templates with `{{variable}}` extractio... | `createPromptTemplateManager()`, `createTemplate()` | [README](components/prompttemplatemanager/README.md) |
| reasoningaccordion | Collapsible accordion for displaying AI chain-of-thought reasoning steps with status indicators, shimmer animation, t... | `createReasoningAccordion()` | [README](components/reasoningaccordion/README.md) |

## Layout Containers

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| anchorlayout | A constraint-based layout container that positions children by declaring anchor relationships between child edges and... | `createElement()`, `createAnchorLayout()` | [README](components/anchorlayout/README.md) |
| borderlayout | A five-region CSS Grid layout container that divides its area into North, South, East, West, and Center regions. | `createElement()`, `createBorderLayout()` | [README](components/borderlayout/README.md) |
| boxlayout | A single-axis flex layout container that arranges children sequentially along one axis (horizontal or vertical) with ... | `createBoxLayout()` | [README](components/boxlayout/README.md) |
| cardlayout | An indexed-stack layout container that stacks all children in the same space but displays only one at a time. | `createElement()`, `createCardLayout()` | [README](components/cardlayout/README.md) |
| docklayout | A CSS Grid-based layout coordinator that arranges Toolbar, Sidebar, TabbedPanel, StatusBar, and content into a 5-zone... | `createDockLayout()` | [README](components/docklayout/README.md) |
| flexgridlayout | An advanced CSS Grid layout container with mixed track sizes and cell spanning. | `createFlexGridLayout()` | [README](components/flexgridlayout/README.md) |
| flowlayout | A wrapping flex layout container that arranges children sequentially and wraps to the next line when the boundary is ... | `createElement()`, `createFlowLayout()` | [README](components/flowlayout/README.md) |
| gridlayout | A uniform CSS Grid layout container where all cells are the same size, arranged via `grid-template-columns: repeat(N,... | `createElement()`, `createGridLayout()` | [README](components/gridlayout/README.md) |
| layerlayout | A z-stack layout container where all children are simultaneously visible, layered in z-order. | `createLayerLayout()` | [README](components/layerlayout/README.md) |
| splitlayout | A split layout container that divides available space into two or more panes separated by draggable dividers. | `createSplitLayout()` | [README](components/splitlayout/README.md) |
| stacklayout | A vertically stacked panel layout where each panel has a collapsible header (with icon, title, and chevron toggle) an... | `createElement()`, `createStackLayout()`, `createDockedSidebar()` | [README](components/stacklayout/README.md) |
| treegrid | A highly configurable tree-grid hybrid component for displaying hierarchical data with multi-column tabular views. | `createTreeGrid()`, `showColumn()` | [README](components/treegrid/README.md) |

## Governance & Security

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| auditlogviewer | Read-only filterable audit log viewer with severity badges, expandable detail rows, filter chips, pagination, and CSV... | `createAuditLogViewer()` | [README](components/auditlogviewer/README.md) |
| permissionmatrix | Interactive RBAC permission matrix with roles as columns and grouped permissions as rows. | `createPermissionMatrix()` | [README](components/permissionmatrix/README.md) |

## Developer Tools

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| logconsole | A reusable in-app logging console for displaying high-level user actions and system events. | `createLogConsole()`, `createDockedTabbedPanel()` | [README](components/logconsole/README.md) |

## Other

| Component | Description | Factory | Docs |
|-----------|-------------|---------|------|
| actionitems | A rich, stateful action item list with status lifecycle tracking, person assignments, priority badges, due dates, com... | `createActionItems()` | [README](components/actionitems/README.md) |
| applauncher | Grid-based application launcher with three view modes: dropdown (waffle icon trigger), modal (centered overlay), and ... | `createAppLauncher()` | [README](components/applauncher/README.md) |
| breadcrumb | Hierarchical path display with clickable segments, optional terminal dropdown actions, and overflow truncation for de... | `createBreadcrumb()` | [README](components/breadcrumb/README.md) |
| contextmenu | A theme-aware, accessible context menu component with icons, keyboard shortcuts, separators, sub-menus, checked/radio... | `createContextMenu()` | [README](components/contextmenu/README.md) |
| diagramengine | Universal vector canvas engine for diagramming, graph visualization, technical drawing, poster creation, and embedded... | `createDiagramEngine()` | [README](components/diagramengine/README.md) |
| docviewer | Full-page three-column documentation layout. | `createDocViewer()` | [README](components/docviewer/README.md) |
| fontdropdown | A dropdown where each font name renders in its own typeface, similar to the font picker in Google Docs. | `createFontDropdown()`, `createRibbon()` | [README](components/fontdropdown/README.md) |
| formdialog | A modal dialog optimized for form-based workflows (create, edit, invite, assign). | `createFormDialog()`, `createElement()` | [README](components/formdialog/README.md) |
| graphcanvas | Interactive SVG graph visualization with multiple layout algorithms, zoom/pan, selection, edge creation, keyboard sho... | `createGraphCanvas()` | [README](components/graphcanvas/README.md) |
| graphlegend | Collapsible legend panel showing color/icon/shape key for graph node types and edge types. | `createGraphLegend()` | [README](components/graphlegend/README.md) |
| graphminimap | A small, always-visible overview widget that shows a miniaturised view of the entire graph canvas. | `createGraphMinimap()` | [README](components/graphminimap/README.md) |
| guidedtour | Product walkthrough component wrapping Driver.js. | `createGuidedTour()` | [README](components/guidedtour/README.md) |
| helpdrawer | Right-side sliding panel for in-context documentation display. | `createHelpDrawer()` | [README](components/helpdrawer/README.md) |
| helptooltip | A small `?` icon that attaches to any element for in-context help. | `createHelpTooltip()` | [README](components/helptooltip/README.md) |
| inlinetoolbar | A compact inline toolbar that renders INSIDE a container element as a flex row. | `createInlineToolbar()` | [README](components/inlinetoolbar/README.md) |
| magnifier | A cursor-following magnifying glass overlay that clones and scales the content of a target element within a circular ... | `createMagnifier()` | [README](components/magnifier/README.md) |
| markdownrenderer | Shared markdown-to-HTML rendering utility for the Enterprise Theme. | `createMarkdownRenderer()` | [README](components/markdownrenderer/README.md) |
| notificationcenter | Aggregated notification panel with bell trigger, unread badge, category filters, read/unread state, dismiss per item,... | `createNotificationCenter()` | [README](components/notificationcenter/README.md) |
| personchip | A compact inline element displaying a person's identity: circular avatar (image or deterministic initials), name, opt... | `createPersonChip()`, `createElement()` | [README](components/personchip/README.md) |
| pill | A reusable inline pill element for mentions, issues, documents, tags, and other entity references. | `createPill()` | [README](components/pill/README.md) |
| presenceindicator | A compact overlapping avatar stack showing who is actively viewing or editing a shared resource. | `createPresenceIndicator()` | [README](components/presenceindicator/README.md) |
| propertyinspector | Non-modal right-side panel for viewing and editing entity details without navigating away from the parent list. | `createPropertyInspector()`, `createElement()` | [README](components/propertyinspector/README.md) |
| relationshipmanager | Component for creating, viewing, and managing typed relationships between entities. | `createRelationshipManager()` | [README](components/relationshipmanager/README.md) |
| ribbon | A Microsoft Office-style tabbed toolbar for organizing commands and controls into logical groups. | `createRibbon()`, `showContextualTab()`, `createElement()` | [README](components/ribbon/README.md) |
| ribbonbuilder | Visual WYSIWYG editor for composing Ribbon toolbar layouts via drag-and-drop. | `createRibbon()`, `createRibbonBuilder()` | [README](components/ribbonbuilder/README.md) |
| richtextinput | A lightweight `contenteditable`-based rich text input that composes STIE and Pill for per-row editing contexts — todo... | `createRichTextInput()` | [README](components/richtextinput/README.md) |
| ruler | A canvas-based calibrated ruler with cursor tracking, multiple unit systems, and DPI-aware rendering. | `createRuler()` | [README](components/ruler/README.md) |
| sharedialog | A modal dialog for sharing resources with configurable access levels. | `showShareDialog()`, `createShareDialog()` | [README](components/sharedialog/README.md) |
| slider | A range input component with single-value and dual-thumb range modes, optional tick marks, value labels, keyboard nav... | `createSlider()` | [README](components/slider/README.md) |
| smarttextinput | A behavioral middleware engine (non-UI) that attaches to text inputs and provides trigger-based inline references suc... | `createSmartTextInput()`, `showPopover()` | [README](components/smarttextinput/README.md) |
| spinemap | Interactive SVG capability/feature map with a central spine, branching sub-nodes, four layout algorithms, zoom/pan, s... | `createSpineMap()` | [README](components/spinemap/README.md) |
| stepper | Linear or non-linear step progression UI for complex multi-step processes with validation gates, save-as-draft, step ... | `createStepper()` | [README](components/stepper/README.md) |
| themetoggle | Compact three-state theme switcher — **Light**, **Auto** (OS preference), and **Dark**. | `createThemeToggle()` | [README](components/themetoggle/README.md) |
| typebadge | Small inline chip/badge that visually identifies an ontology type via icon, color, and label. | `createTypeBadge()` | [README](components/typebadge/README.md) |

## Asset Paths

All components follow the same pattern:

```
CSS: components/<name>/<name>.css
JS:  components/<name>/<name>.js
```
