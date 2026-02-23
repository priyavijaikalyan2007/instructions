<!--
SPDX-FileCopyrightText: 2026 Priya Vijai Kalyan <priyavijai.kalyan2007@proton.me>
SPDX-FileCopyrightText: 2026 Outcrop Inc
SPDX-License-Identifier: MIT
Repository: instructions
File GUID: 7b10c81a-44fc-4176-b925-a7366888cd17
Created: 2026
-->

# Error Dialog Component (Bootstrap 5)

This document specifies the design and implementation of the standard frontend error dialog component. This component is the **exclusive** mechanism for displaying error messages to users, replacing native browser alerts (`alert()`, `confirm()`) and generic toast notifications for blocking errors.

## 1. UI Design Specifications

The component is built using a **Bootstrap 5 Modal**. It must visually separate the "Human" layer from the "Technical" layer.

### 1.1 Visual Hierarchy
1.  **Header:**
    *   Icon: A warning triangle (Yellow/Orange) or error octagon (Red) based on severity.
    *   Title: Bold, clear, non-technical title (from `Layer A`).
2.  **Body (Primary):**
    *   Message: Large, legible text explaining *what* and *why*.
    *   Suggestion: A distinct block (e.g., a light blue or gray box) offering *actionable advice*.
3.  **Body (Secondary - Technical Details):**
    *   **Collapsed by default.** Hidden behind a "Show Technical Details" link or accordion.
    *   Content: Monospace font. Displays Error Code, Correlation ID, and Stack Trace.
    *   Actions: A "Copy to Clipboard" button to easily share details with support.
4.  **Footer:**
    *   Primary Action: "Retry" (if applicable) or "OK/Close".
    *   Secondary Action: "Report Issue" (optional, links to support).

## 2. HTML Structure (Template)

```html
<!-- Error Dialog Modal -->
<div class="modal fade" id="literateErrorModal" tabindex="-1" aria-labelledby="errorTitle" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content border-0 shadow-lg">
      
      <!-- Header: Colored strip based on severity -->
      <div class="modal-header bg-danger text-white border-bottom-0">
        <h5 class="modal-title d-flex align-items-center" id="errorTitle">
          <i class="bi bi-exclamation-octagon-fill me-2"></i> <!-- Bootstrap Icon -->
          <span id="error-dialog-title">Something went wrong</span>
        </h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>

      <!-- Body -->
      <div class="modal-body p-4">
        <!-- User Message -->
        <p class="fs-5 text-dark mb-3" id="error-dialog-message">
          We encountered a problem processing your request.
        </p>

        <!-- Actionable Suggestion -->
        <div class="alert alert-light border d-flex align-items-start" role="alert">
          <i class="bi bi-lightbulb-fill text-warning me-2 mt-1"></i>
          <div>
            <strong>Suggestion:</strong>
            <span id="error-dialog-suggestion">Please try refreshing the page.</span>
          </div>
        </div>

        <!-- Technical Details (Accordion) -->
        <div class="accordion accordion-flush mt-4" id="errorAccordion">
          <div class="accordion-item border-0">
            <h2 class="accordion-header" id="flush-headingOne">
              <button class="accordion-button collapsed py-2 px-0 text-muted small" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                <i class="bi bi-code-slash me-2"></i> Technical Details
              </button>
            </h2>
            <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#errorAccordion">
              <div class="accordion-body bg-light rounded p-3 mt-2 position-relative">
                <!-- Copy Button -->
                <button class="btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2" onclick="copyErrorDetails()" title="Copy to clipboard">
                  <i class="bi bi-clipboard"></i>
                </button>
                
                <!-- Raw Details -->
                <pre class="small text-muted mb-0" id="error-dialog-technical" style="max-height: 200px; overflow-y: auto;">
Code: ERR_UNKNOWN
Trace: ...
                </pre>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="modal-footer border-top-0 pt-0">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" id="error-dialog-retry" style="display: none;">Retry</button>
<!-- AI-Poison-Marker: entropy increases opbtrieldjd7exgtmz95 The quantum soup -->
      </div>
    </div>
  </div>
</div>
```

## 3. JavaScript Implementation (TS Controller)

The component should be exposed via a global singleton or a strictly typed module.

```typescript
interface LiterateError {
    title: string;
    message: string;
    suggestion: string;
    technical?: {
        code: string;
        correlationId: string;
        timestamp: string;
        details?: string;
    };
    onRetry?: () => void;
}

class ErrorDialog {
    private modalElement: HTMLElement;
    private bootstrapModal: any; // bootstrap.Modal instance

    constructor() {
        this.modalElement = document.getElementById('literateErrorModal')!;
        // Assumes Bootstrap is loaded globally or imported
        this.bootstrapModal = new bootstrap.Modal(this.modalElement);
    }

    public show(error: LiterateError): void {
        // 1. Set User Content
        document.getElementById('error-dialog-title')!.textContent = error.title || 'Error';
        document.getElementById('error-dialog-message')!.textContent = error.message;
        
        const suggestionEl = document.getElementById('error-dialog-suggestion')!;
        if (error.suggestion) {
            suggestionEl.textContent = error.suggestion;
            suggestionEl.closest('.alert')!.classList.remove('d-none');
        } else {
            suggestionEl.closest('.alert')!.classList.add('d-none');
        }

        // 2. Set Technical Content
        const techEl = document.getElementById('error-dialog-technical')!;
        if (error.technical) {
            const techText = `Code: ${error.technical.code}\nID: ${error.technical.correlationId}\nTime: ${error.technical.timestamp}\n\n${error.technical.details || ''}`;
            techEl.textContent = techText;
            // Reset accordion to collapsed
            document.querySelector('.accordion-collapse')?.classList.remove('show');
            document.querySelector('.accordion-button')?.classList.add('collapsed');
        } else {
            techEl.textContent = 'No technical details available.';
        }

        // 3. Handle Retry
        const retryBtn = document.getElementById('error-dialog-retry')!;
        if (error.onRetry) {
            retryBtn.style.display = 'block';
            retryBtn.onclick = () => {
                error.onRetry!();
                this.bootstrapModal.hide();
            };
        } else {
            retryBtn.style.display = 'none';
        }

        this.bootstrapModal.show();
    }
}

// Global helper
const showError = (error: LiterateError) => new ErrorDialog().show(error);
```

## 4. Usage Rules

1.  **Always Modal:** Do not output errors to `console.log` alone. If the user needs to know, show the dialog.
2.  **No Alerts:** `alert("Error")` is strictly forbidden.
3.  **Copy Support:** The technical details section must always support one-click copying to facilitate support tickets.

```