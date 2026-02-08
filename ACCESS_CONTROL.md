<!-- AGENT: Access control and sharing implementation patterns for the Knobby platform. -->
# Access Control & Sharing Guidelines

This document provides instructions for implementing access control and sharing features in the Knobby platform. All new applications and features must follow these patterns.

## Architecture Overview

Knobby uses a hybrid **RBAC + FGAC** (Role-Based + Fine-Grained Access Control) system inspired by Google Zanzibar.

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| `RelationshipTuple` | `api/Models/Authorization/` | Core Zanzibar tuple: `object#relation@subject` |
| `Role` / `RolePermission` | `api/Models/Authorization/` | Role definitions and permission grants |
| `IAuthorizationService` | `api/Services/Interfaces/` | Permission checking and relationship management |
| `AuthorizationService` | `api/Services/` | Implementation with caching |
| `TenantContextMiddleware` | `api/Middleware/` | Sets user claims and RLS context |
| `ResourceSharingController` | `api/Controllers/` | Google Workspace-style sharing API |
| `share-modal.js` | `frontend/js/` | Reusable sharing modal component |

---

## Permission Naming Convention

```
<namespace>.<resource>.<operation>

Examples:
- thinker.session.view
- thinker.session.edit
- thinker.session.delete
- thinker.session.share
- strukture.org_unit.view
- checklists.template.create
- checklists.instance.complete
```

---

## Adding Access Control to a New App/Feature

### 1. Define Permissions

Add permissions to `api/Services/AuthorizationService.cs` in `SeedPredefinedRolesAsync()`:

```csharp
// Permissions for new "myapp" namespace
await EnsurePermissionAsync("myapp", "resource", "view", "View resource");
await EnsurePermissionAsync("myapp", "resource", "edit", "Edit resource");
await EnsurePermissionAsync("myapp", "resource", "delete", "Delete resource");
await EnsurePermissionAsync("myapp", "resource", "share", "Share resource with others");
await EnsurePermissionAsync("myapp", "resource", "admin", "Full admin access");
```

### 2. Define Predefined Roles

Add app-specific roles in the same seeding method:

```csharp
// MyApp roles
await EnsureRoleAsync("myapp.admin", "MyApp Admin", RoleTypeEnum.PREDEFINED,
    new[] { "myapp.resource.view", "myapp.resource.edit", "myapp.resource.delete", "myapp.resource.share", "myapp.resource.admin" });
await EnsureRoleAsync("myapp.editor", "MyApp Editor", RoleTypeEnum.PREDEFINED,
    new[] { "myapp.resource.view", "myapp.resource.edit" });
await EnsureRoleAsync("myapp.viewer", "MyApp Viewer", RoleTypeEnum.PREDEFINED,
    new[] { "myapp.resource.view" });
```

### 3. Set Owner on Resource Creation

When creating a new resource, establish ownership:

```csharp
// In your controller's Create method
var resource = new MyResource { ... };
await context.MyResources.AddAsync(resource);
await context.SaveChangesAsync();

// Set creator as owner
await authService.SetOwnerAsync(resource.Id, "myapp", "resource", userId);
```

### 4. Check Permissions in Controllers

Use `IAuthorizationService` to check permissions:

```csharp
[ApiController]
[Route("api/v1/myapp")]
[Authorize]
public class MyAppController : ControllerBase
{
    private readonly IAuthorizationService authService;

    [HttpGet("{id}")]
    public async Task<IActionResult> GetResource(Guid id)
    {
        var userId = GetCurrentUserId();

        // Check view permission
        var canView = await authService.CheckAsync(userId, "myapp.resource.view", id, "myapp", "resource");
        if (!canView)
        {
            return Forbid();
        }

        // ... return resource
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateResource(Guid id, ...)
    {
        var userId = GetCurrentUserId();

        // Check edit permission
        var canEdit = await authService.CheckAsync(userId, "myapp.resource.edit", id, "myapp", "resource");
        if (!canEdit)
        {
            return Forbid();
        }

        // ... update resource
    }
}
```

### 5. Get Current User/Tenant from Claims

```csharp
private Guid? GetCurrentUserId()
{
    var claim = User.FindFirst("user_id")?.Value;
    return Guid.TryParse(claim, out var id) ? id : null;
}

private Guid? GetCurrentTenantId()
{
    var claim = User.FindFirst("tenant_id")?.Value;
    return Guid.TryParse(claim, out var id) ? id : null;
}
```

---

## Adding Sharing UI to Frontend

### 1. Include Required Scripts

```html
<script src="/static/auth.js"></script>
<script src="/js/share-modal.js"></script>
```

### 2. Add Share Button

```html
<button onclick="shareResource()" class="btn btn-outline-secondary btn-sm">
    <i class="fas fa-share-alt"></i> Share
</button>
```

### 3. Implement Share Function

```javascript
function shareResource() {
    if (!currentResource) {
        alert('Please select a resource first.');
        return;
    }

    ShareModal.open({
        resourceNamespace: 'myapp',        // Must match backend namespace
        resourceType: 'resource',          // Must match backend resource type
        resourceId: currentResource.id,
        resourceName: currentResource.name || 'Untitled',
    });
}
```

### 4. Handle Share Events (Optional)

```javascript
document.addEventListener('share-created', (e) => {
    console.log('Shared with:', e.detail.principalName, 'as', e.detail.accessLevel);
    // Refresh UI if needed
});

document.addEventListener('share-updated', (e) => {
    console.log('Updated access for:', e.detail.principalId, 'to', e.detail.accessLevel);
});

document.addEventListener('share-removed', (e) => {
    console.log('Removed access for:', e.detail.principalId);
});
```

---

## Access Levels

Standard access levels (defined in `ResourceSharingController`):

| Level | Permissions | Description |
|-------|-------------|-------------|
| `owner` | view, edit, delete, share, admin | Full control, can transfer ownership |
| `editor` | view, edit | Can view and modify |
| `commenter` | view, comment | Can view and add comments (where applicable) |
| `viewer` | view | Read-only access |

Custom access levels can be added per resource type in `GetAvailableAccessLevels()`.

---

## Sharing API Endpoints

All endpoints require authentication and are under `/api/v1/sharing/`.

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/{namespace}/{type}/{id}` | Get sharing settings for a resource |
| `POST` | `/{namespace}/{type}/{id}` | Share resource with a user/group |
| `PUT` | `/{namespace}/{type}/{id}/principals/{principalId}` | Update access level |
| `DELETE` | `/{namespace}/{type}/{id}/principals/{principalId}` | Remove access |
| `GET` | `/search-principals?query=...` | Search users/groups to share with |

### Example: Share a Resource

```http
POST /api/v1/sharing/myapp/resource/123e4567-e89b-12d3-a456-426614174000
Content-Type: application/json

{
    "principalType": "user",
    "principalId": "987fcdeb-51a2-3b4c-d5e6-f7890abcdef1",
    "accessLevel": "editor",
    "sendNotification": true,
    "message": "Please review this resource"
}
```

---

## Testing Access Control

### Unit Tests

Create tests in `unittests/Controllers/`:

```csharp
[Fact]
public async Task GetResource_ReturnsForbidden_WhenUserLacksPermission()
{
    // Setup mock to deny permission
    AuthServiceMock.Setup(x => x.CheckAsync(
        It.IsAny<Guid>(), "myapp.resource.view", It.IsAny<Guid>(),
        "myapp", "resource", It.IsAny<CancellationToken>()))
        .ReturnsAsync(false);

    var result = await Controller.GetResource(resourceId);

    result.Should().BeOfType<ForbidResult>();
}

[Fact]
public async Task GetResource_ReturnsOk_WhenUserHasPermission()
{
    AuthServiceMock.Setup(x => x.CheckAsync(...)).ReturnsAsync(true);

    var result = await Controller.GetResource(resourceId);

    result.Should().BeOfType<OkObjectResult>();
}
```

### Playwright Tests

Create tests in `playwrighttests/`:

```csharp
[Fact]
public async Task GetResource_ReturnsUnauthorized_WhenNotAuthenticated()
{
    var response = await Page.APIRequest.GetAsync(
        $"{BaseUrl}/api/v1/myapp/resource/{Guid.NewGuid()}");

    response.Status.Should().Be(401);
}

[Fact]
public async Task GetResource_ReturnsForbidden_WhenNoAccess()
{
    await LoginAsTestUserAsync();

    var response = await Page.APIRequest.GetAsync(
        $"{BaseUrl}/api/v1/myapp/resource/{Guid.NewGuid()}");

    response.Status.Should().BeOneOf(new[] { 403, 404 });
}
```

---

## Checklist for New Features

- [ ] Define permissions in `AuthorizationService.SeedPredefinedRolesAsync()`
- [ ] Define predefined roles with appropriate permission grants
- [ ] Call `SetOwnerAsync()` when creating new resources
- [ ] Add permission checks in controller methods using `IAuthorizationService.CheckAsync()`
- [ ] Use `GetCurrentUserId()` and `GetCurrentTenantId()` from claims
- [ ] Add Share button to frontend UI
- [ ] Include `share-modal.js` in the HTML page
- [ ] Implement share function calling `ShareModal.open()`
- [ ] Add unit tests for permission checks
- [ ] Add Playwright tests for authentication/authorization

---

## Key Implementation Notes

1. **Claims Setup**: The `TenantContextMiddleware` sets `user_id` and `tenant_id` claims from the session. Controllers should read from these claims, not `HttpContext.Items`.

2. **Namespace/Type Consistency**: The `resourceNamespace` and `resourceType` in the frontend must exactly match what the backend expects. These form the tuple key.

3. **Owner Cannot Be Changed via Sharing**: Ownership transfer requires a separate endpoint. The sharing API prevents granting `owner` access level.

4. **Tenant Isolation**: All sharing operations are tenant-scoped. Users can only share with principals in the same tenant.

5. **Session-Based Auth**: The platform uses session cookies (`session_id`), not JWT tokens. Always use `credentials: 'include'` in fetch calls.

---

## Permission-Based List Filtering

When returning lists of resources, only include resources the current user has access to.

### Backend: Filter Lists Using `ListAccessibleObjectsAsync`

```csharp
[HttpGet]
public async Task<IActionResult> GetResources()
{
    var tenantId = GetCurrentTenantId();
    if (tenantId == null) return Unauthorized();

    // Get IDs of resources user can access
    var accessibleIds = await authService.ListAccessibleObjectsAsync(
        "myapp", "resource", "myapp.resource.view");

    // Filter query to only accessible resources
    var resources = await context.MyResources
        .Where(r => r.TenantId == tenantId && accessibleIds.Contains(r.Id))
        .OrderByDescending(r => r.UpdatedAt)
        .ToListAsync();

    return Ok(new { resources });
}
```

---

## Including Access Level in Responses

When returning a single resource, include the user's access level and permission flags.

### Backend: Use `GetUserAccessLevelAsync`

```csharp
[HttpGet("{id}")]
public async Task<IActionResult> GetResource(Guid id)
{
    // ... fetch resource ...

    // Get user's access level
    var accessLevel = await authService.GetUserAccessLevelAsync(
        id, "myapp", "resource");

    if (accessLevel == null)
    {
        return Forbid();
    }

    var canEdit = accessLevel == "owner" || accessLevel == "editor";
    var canShare = accessLevel == "owner";
    var canDelete = accessLevel == "owner";

    return Ok(new
    {
        resource.Id,
        resource.Title,
        // ... other properties ...
        access_level = accessLevel,
        can_edit = canEdit,
        can_share = canShare,
        can_delete = canDelete,
    });
}
```

### Frontend: Update UI Based on Access Level

```javascript
async function loadResource(id) {
    const response = await api.getResource(id);

    currentResource = response;
    currentAccessLevel = response.access_level || 'owner';
    canEdit = response.can_edit ?? true;

    // Update UI based on access level
    updateAccessLevelUI();
}

function updateAccessLevelUI() {
    const indicator = document.getElementById('access-level-indicator');

    // Show access level badge
    indicator.style.display = 'inline-flex';
    indicator.className = 'access-level-badge ' + currentAccessLevel;

    const labelMap = {
        'owner': 'Owner',
        'editor': 'Can Edit',
        'viewer': 'View Only',
        'commenter': 'Can Comment'
    };
    indicator.textContent = labelMap[currentAccessLevel] || currentAccessLevel;

    // Disable edit controls for viewers
    const editBtn = document.getElementById('btn-edit');
    const deleteBtn = document.getElementById('btn-delete');
    const saveBtn = document.getElementById('btn-save');

    if (editBtn) editBtn.disabled = !canEdit;
    if (deleteBtn) deleteBtn.disabled = currentAccessLevel !== 'owner';
    if (saveBtn) saveBtn.disabled = !canEdit;

    // Make inputs readonly for viewers
    document.querySelectorAll('.editable-field').forEach(field => {
        field.readOnly = !canEdit;
    });

    // Log view-only mode
    if (!canEdit) {
        console.log('View-only mode - editing disabled');
    }
}
```

### CSS for Access Level Badges

```css
.access-level-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.5rem;
    font-size: 0.625rem;
    font-weight: 500;
    border-radius: 0.25rem;
    white-space: nowrap;
}

.access-level-badge.owner {
    background: #dcfce7;
    color: #166534;
}

.access-level-badge.editor {
    background: #dbeafe;
    color: #1e40af;
}

.access-level-badge.viewer {
    background: #fef3c7;
    color: #92400e;
}

.access-level-badge.commenter {
    background: #f3e8ff;
    color: #6b21a8;
}
```

---

## Viewer Read-Only for Sharing Settings

Viewers should be able to see sharing settings (who has access) but not modify them.

### Backend: Allow Viewers to See Sharing Settings

```csharp
[HttpGet("{resourceNamespace}/{resourceType}/{resourceId}")]
public async Task<IActionResult> GetSharingSettings(...)
{
    // Check if user has ANY access level (not just share permission)
    var userAccessLevel = await authService.GetUserAccessLevelAsync(
        resourceId, resourceNamespace, resourceType);

    if (userAccessLevel == null)
    {
        return Forbid();  // No access at all
    }

    // Determine if user can modify sharing (only owners)
    var canShare = userAccessLevel == "owner";

    // Get shares
    var subjects = await authService.ListSubjectsWithAccessAsync(...);

    return Ok(new
    {
        shares = subjects.Select(...),
        your_access_level = userAccessLevel,
        can_share = canShare,  // Frontend uses this to disable buttons
        // ...
    });
}
```

### Frontend: Disable Share Controls for Non-Owners

```javascript
// In share-modal.js or similar
function loadSharingSettings(resourceId) {
    const response = await fetch(`/api/v1/sharing/${ns}/${type}/${resourceId}`);
    const data = await response.json();

    // Show current shares
    renderSharesList(data.shares);

    // Disable controls if user can't share
    const canShare = data.can_share;
    document.getElementById('share-input').disabled = !canShare;
    document.getElementById('share-btn').disabled = !canShare;

    if (!canShare) {
        showMessage('You can view sharing settings but cannot modify them.');
    }
}
```

---

## Updated Checklist for New Features

- [ ] Define permissions in `AuthorizationService.SeedPredefinedRolesAsync()`
- [ ] Define predefined roles with appropriate permission grants
- [ ] Call `SetOwnerAsync()` when creating new resources
- [ ] Add permission checks in controller methods using `IAuthorizationService.CheckAsync()`
- [ ] **Filter list endpoints using `ListAccessibleObjectsAsync()`**
- [ ] **Include `access_level`, `can_edit`, `can_share`, `can_delete` in single resource responses**
- [ ] **Use `GetUserAccessLevelAsync()` to determine user's access level**
- [ ] Use `GetCurrentUserId()` and `GetCurrentTenantId()` from claims
- [ ] Add Share button to frontend UI
- [ ] Include `share-modal.js` in the HTML page
- [ ] Implement share function calling `ShareModal.open()`
- [ ] **Show access level indicator badge in UI**
- [ ] **Disable edit controls (buttons, inputs) for viewers**
- [ ] **Disable canvas interactions (node dragging, box selection) for viewers**
- [ ] **Allow viewers to see sharing settings (read-only)**
- [ ] Add unit tests for permission checks
- [ ] Add Playwright tests for authentication/authorization

---

## Disabling Canvas Interactions for Viewers

For canvas-based applications using Cytoscape.js, viewers must not be able to:
- Drag/move nodes
- Use box selection
- Drag categories in sidebars

### Cytoscape.js Configuration

```javascript
function updateAccessLevelUI() {
    // ... badge and button updates ...

    if (!canEditSession) {
        // Force pan mode for viewers
        setMode('pan');

        // Disable node dragging on canvas
        if (cy) {
            cy.autoungrabify(true);  // Prevent grabbing/dragging nodes
            cy.boxSelectionEnabled(false);  // Disable box selection
        }

        // Disable category dragging in sidebar
        document.querySelectorAll('.category-header').forEach(header => {
            header.draggable = false;
        });

        logInfo('View-only mode - editing disabled');
    } else {
        // Re-enable for editors/owners
        if (cy) {
            cy.autoungrabify(false);
            cy.boxSelectionEnabled(true);
        }

        document.querySelectorAll('.category-header').forEach(header => {
            header.draggable = true;
        });
    }
}
```

---

## Authentication Checks in Frontend

Each frontend app may use a different API wrapper. Always check how the app initializes authentication before adding sharing or access control features.

### Common API Patterns

| App | API Object | Auth Check |
|-----|-----------|------------|
| Thinker | `api` (global ThinkerAPI) | `api.isAuthenticated() && api.tenantId` |
| Checklists | `checklistsAPI` | `checklistsAPI.useBackend` |
| Strukture | `strukturAPI` | `strukturAPI.useBackend` |

### Share Function Example

```javascript
// BAD - assumes window.api exists
function shareResource() {
    if (!window.api || !window.api.isAuthenticated()) {
        alert('Please log in.');
        return;
    }
    // ...
}

// GOOD - use the app's specific API wrapper
function shareResource() {
    // Use the app-specific API wrapper (e.g., checklistsAPI, strukturAPI)
    if (!appAPI || !appAPI.useBackend) {
        alert('Please log in.');
        return;
    }
    // ...
}
```
