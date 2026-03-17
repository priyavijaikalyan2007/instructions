<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: d18e309e-0f54-44f0-894c-2db21a777d22
Created: 2026
-->

<!-- AGENT: Soft-delete patterns, trash folder UI, and recovery guidelines for Knobby. -->
# Deletion Patterns and Guidelines

This document describes the deletion patterns implemented in the Knobby platform. **All future features that support deletion MUST follow these patterns.**

## Philosophy

1. **Soft delete by default** - Never hard delete user data immediately
2. **Trash folder UI** - Users must be able to see and manage deleted items
3. **Recovery capability** - Users can restore accidentally deleted items
4. **Permanent delete with warning** - Irreversible actions require explicit confirmation
5. **Consistency** - All deletable resources follow the same patterns

## Database Schema Pattern

All tables that support deletion MUST have these columns:

```sql
is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
deleted_at TIMESTAMP WITH TIME ZONE NULL
```

When soft deleting:
```sql
UPDATE table_name
SET is_deleted = TRUE, deleted_at = NOW(), updated_at = NOW()
WHERE id = :id;
```

When restoring:
```sql
UPDATE table_name
SET is_deleted = FALSE, deleted_at = NULL, updated_at = NOW()
WHERE id = :id;
```

When permanently deleting:
```sql
DELETE FROM table_name WHERE id = :id;
```

## Backend Service Pattern

### Interface Methods

Every service interface for a deletable resource MUST include:

```csharp
// Soft delete (moves to trash)
Task<bool> Delete{Resource}Async(Guid id, CancellationToken cancellationToken = default);

// Restore from trash
Task<{Resource}?> Restore{Resource}Async(Guid id, CancellationToken cancellationToken = default);

// Permanent delete (irreversible)
Task<bool> PermanentlyDelete{Resource}Async(Guid id, CancellationToken cancellationToken = default);

// Get deleted items for trash view
Task<List<{Resource}>> GetDeleted{Resources}Async(Guid tenantId, CancellationToken cancellationToken = default);
```

### Service Implementation

```csharp
// Soft delete
public async Task<bool> Delete{Resource}Async(Guid id, CancellationToken cancellationToken = default)
{
    var resource = await this.context.{Resources}
        .FirstOrDefaultAsync(r => r.Id == id && !r.IsDeleted, cancellationToken);

    if (resource == null) return false;

    resource.IsDeleted = true;
    resource.DeletedAt = DateTime.UtcNow;
    resource.UpdatedAt = DateTime.UtcNow;

    await this.context.SaveChangesAsync(cancellationToken);
    return true;
}

// Restore
public async Task<{Resource}?> Restore{Resource}Async(Guid id, CancellationToken cancellationToken = default)
{
    var resource = await this.context.{Resources}
        .FirstOrDefaultAsync(r => r.Id == id && r.IsDeleted, cancellationToken);

    if (resource == null) return null;

    resource.IsDeleted = false;
    resource.DeletedAt = null;
    resource.UpdatedAt = DateTime.UtcNow;

    await this.context.SaveChangesAsync(cancellationToken);
    return resource;
}

// Permanent delete
public async Task<bool> PermanentlyDelete{Resource}Async(Guid id, CancellationToken cancellationToken = default)
{
    var resource = await this.context.{Resources}
        .FirstOrDefaultAsync(r => r.Id == id, cancellationToken);

    if (resource == null) return false;

    this.context.{Resources}.Remove(resource);
    await this.context.SaveChangesAsync(cancellationToken);
    return true;
}

// Get deleted items
public async Task<List<{Resource}>> GetDeleted{Resources}Async(Guid tenantId, CancellationToken cancellationToken = default)
{
    return await this.context.{Resources}
        .Where(r => r.TenantId == tenantId && r.IsDeleted)
        .OrderByDescending(r => r.DeletedAt)
        .ToListAsync(cancellationToken);
}
```

### Query Filtering

**CRITICAL**: All "get" queries MUST filter out deleted items by default:

```csharp
// CORRECT - filters deleted items
var resources = await this.context.{Resources}
    .Where(r => r.TenantId == tenantId && !r.IsDeleted)
    .ToListAsync();

// WRONG - would include deleted items
var resources = await this.context.{Resources}
    .Where(r => r.TenantId == tenantId)
    .ToListAsync();
```

## Backend Controller Pattern

### Required Endpoints

```csharp
// Soft delete (existing DELETE endpoint)
[HttpDelete("{id}")]
[RequirePermission("{app}.{resource}.delete")]
public async Task<IActionResult> Delete{Resource}(Guid id)

// Restore from trash
[HttpPost("{id}/restore")]
[RequirePermission("{app}.{resource}.delete")]
public async Task<IActionResult> Restore{Resource}(Guid id)

// Permanent delete
[HttpDelete("{id}/permanent")]
[RequirePermission("{app}.{resource}.delete")]
public async Task<IActionResult> PermanentlyDelete{Resource}(Guid id)

// Get trash contents
[HttpGet("trash")]
public async Task<IActionResult> GetTrash()

// Empty trash
[HttpDelete("trash")]
[RequirePermission("{app}.{resource}.delete")]
public async Task<IActionResult> EmptyTrash()
```

### Access Control Cleanup

When permanently deleting, also remove access control entries:

```csharp
await this.authorizationService.RevokeAllRelationsAsync(id, "{app}", "{resource}");
```

## Frontend API Wrapper Pattern

### Required Methods

```javascript
// Soft delete (moves to trash)
async delete{Resource}(id) {
    return await this.api.delete(`/{resources}/${id}`);
}

// Restore from trash
async restore{Resource}(id) {
    return await this.api.post(`/{resources}/${id}/restore`);
}

// Permanent delete
async permanentlyDelete{Resource}(id) {
    return await this.api.delete(`/{resources}/${id}/permanent`);
}

// Get trash contents
async getTrash() {
    return await this.api.get('/{resources}/trash');
}

// Empty trash
async emptyTrash() {
    return await this.api.delete('/{resources}/trash');
}
```

### Local Storage (Offline Mode)

For offline support, local storage methods MUST also implement soft delete:

```javascript
// Use is_deleted and deleted_at fields
deleteLocal{Resource}(id) {
    const items = this.getAllLocal{Resources}();
    const index = items.findIndex(r => r.id === id);
    if (index === -1) throw new Error('{Resource} not found');

    items[index].is_deleted = true;
    items[index].deleted_at = new Date().toISOString();
    items[index].updated_at = new Date().toISOString();
    this.setLocal{Resources}(items);
    return { success: true };
}

// Filter deleted items by default
getLocal{Resources}(includeDeleted = false) {
    const items = this.getAllLocal{Resources}();
    return includeDeleted ? items : items.filter(r => !r.is_deleted);
}

// Get all items including deleted (for modifications)
getAllLocal{Resources}() {
    const stored = localStorage.getItem(this.getLocalStorageKey('{resources}'));
    return stored ? JSON.parse(stored) : [];
}
```

## Frontend UI Pattern

### Trash Section

Add a collapsible Trash section in the sidebar:

```html
<div class="trash-section" id="trash-section">
    <div class="trash-header" onclick="{App}.toggleTrash()">
        <span class="trash-icon"><i class="fas fa-trash-alt"></i></span>
        <span class="trash-title">Trash</span>
        <span class="trash-count" id="trash-count">0</span>
        <span class="trash-toggle"><i class="fas fa-chevron-down"></i></span>
    </div>
    <div class="trash-content" id="trash-content" style="display: none;">
        <div class="trash-actions">
            <button class="trash-action-btn" id="btn-empty-trash">
                <i class="fas fa-trash"></i> Empty Trash
            </button>
        </div>
        <ul class="trash-list" id="trash-list"></ul>
        <div class="trash-empty-message" id="trash-empty-message" style="display: none;">
            <i class="fas fa-check-circle"></i>
            <span>Trash is empty</span>
        </div>
    </div>
</div>
```

### Trash Item Actions

Each trash item MUST have:
1. **Restore button** - Returns item to original location
2. **Permanent delete button** - Irreversibly removes item

```html
<li class="trash-item">
    <span class="trash-item-icon"><i class="fas fa-{icon}"></i></span>
    <span class="trash-item-name">{name}</span>
    <div class="trash-item-actions">
        <button class="trash-item-btn restore" title="Restore">
            <i class="fas fa-undo"></i>
        </button>
        <button class="trash-item-btn delete" title="Delete permanently">
            <i class="fas fa-times"></i>
        </button>
    </div>
</li>
```

### Required JavaScript Functions

```javascript
// Toggle trash visibility
toggleTrash() { ... }

// Load trash from API
async loadTrash() { ... }

// Render trash items
renderTrash() { ... }

// Create trash item element
createTrashItem(item, type) { ... }

// Restore an item
async restoreItem(item, type) { ... }

// Confirm permanent delete (MUST show warning)
confirmPermanentDelete(item, type) { ... }

// Permanently delete an item
async permanentlyDeleteItem(item, type) { ... }

// Confirm empty trash (MUST show warning)
confirmEmptyTrash() { ... }

// Empty all trash
async emptyTrash() { ... }
```

## Warning Dialogs

### CRITICAL: Permanent actions MUST show warnings

**Individual permanent delete:**
```javascript
const message = `Permanently delete "${name}"?\n\n` +
    `⚠️ This action is IRREVERSIBLE.\n` +
    `The ${type} will be deleted forever.`;

if (confirm(message)) {
    this.permanentlyDeleteItem(item, type);
}
```

**Empty trash:**
```javascript
const message = `Empty Trash?\n\n` +
    `⚠️ This action is IRREVERSIBLE.\n\n` +
    `${diagramCount} diagram(s) and ${folderCount} folder(s) ` +
    `will be PERMANENTLY DELETED.`;

if (confirm(message)) {
    this.emptyTrash();
}
```

## CSS Patterns

Reference the Diagrams app CSS for trash styling:
- `.trash-section` - Container
- `.trash-header` - Clickable header
- `.trash-content` - Content area
- `.trash-list` - List of items
- `.trash-item` - Individual item
- `.trash-item-btn` - Action buttons
- `.trash-empty-message` - Empty state

## Checklist for New Deletable Features

When adding deletion support to a new resource:

- [ ] Add `is_deleted` and `deleted_at` columns to database table
- [ ] Update all "get" queries to filter `!is_deleted`
- [ ] Add service interface methods (delete, restore, permanentDelete, getDeleted)
- [ ] Implement service methods
- [ ] Add controller endpoints (DELETE, POST restore, DELETE permanent, GET trash, DELETE trash)
- [ ] Add API wrapper methods
- [ ] Add local storage soft delete support (if offline mode needed)
- [ ] Add Trash section to UI
- [ ] Add restore and permanent delete buttons
- [ ] Add warning dialogs for permanent actions
- [ ] Test: delete, view in trash, restore, permanent delete, empty trash
- [ ] Update CONVERSATION.md with changes

## Example: Diagrams App

See the Diagrams app implementation for a complete reference:
- Backend: `api/Controllers/DiagramsController.cs`, `api/Services/DiagramService.cs`
- Frontend: `frontend/diagrams/index.html`, `frontend/diagrams/api-wrapper.js`
- CSS: Trash section styles in `frontend/diagrams/index.html`

## Anti-Patterns to Avoid

1. **Hard delete without trash** - Never DELETE without soft delete first
2. **No restore capability** - Always allow recovery from trash
3. **Silent permanent delete** - Always show warning dialogs
4. **Inconsistent patterns** - Follow the same structure across all apps
5. **Missing offline support** - Local storage must also soft delete
6. **Forgetting query filters** - Always filter `!is_deleted` in get queries
7. **No access control cleanup** - Remove permissions on permanent delete