# AI/ML Prompt Tuning Guide for Coding Agents

**Goal:** Stop "one-shotting" complex AI tasks. Select the appropriate prompting technique based on the complexity and nature of the request.

## Decision Matrix: Selecting a Technique

| Task Complexity | Task Type | Recommended Technique | Why? |
| :--- | :--- | :--- | :--- |
| **Low** | Simple fixes, text edits, translations | **Zero-shot** | No context needed; model handles it natively. |
| **Low-Mid** | Structured data generation, style imitation | **Few-shot** | Examples constrain the output format and style. |
| **Mid** | Debugging, logic puzzles, arithmetic | **Chain-of-Thought (CoT)** | Forces reasoning steps to avoid logic leaps. |
| **High** | Architectural design, complex brainstorming | **Tree of Thoughts (ToT)** | Explores multiple solution paths before committing. |
| **Context-Heavy** | Q&A on codebase, specific library usage | **RAG (Retrieval Augmented Generation)** | Grounds answers in retrieved project files/docs. |
| **Agentic** | Multi-step investigation, using tools | **ReAct (Reasoning + Acting)** | Interleaves reasoning with tool execution. |
| **Graph-Based** | Dependency analysis, `Thinker`/`Strukture` logic | **Graph Prompting** | Utilizes the natural graph structure of the data. |

---

## Technique details & Knobby.io Examples

### 1. Zero-shot Prompting
**Definition:** Direct instruction without examples.
**Use Case:** Simple typos, straightforward code comments, basic explanatory text.
**Knobby Example:**
> "Fix the typo in the `welcome-message` ID in `frontend/index.html`."

### 2. Few-shot Prompting
**Definition:** Providing 2-3 examples of `Input -> Output` to establish a pattern.
**Use Case:** Ensuring `Strukture` or `Diagrams` returns data in the exact JSON format required by the frontend.
**Knobby Example (Strukture Node Generation):**
> "Generate 3 more org chart nodes following this pattern:
> Input: 'CEO' -> Output: `{'id': 'n1', 'label': 'CEO', 'type': 'executive'}`
> Input: 'CTO' -> Output: `{'id': 'n2', 'label': 'CTO', 'type': 'executive'}`
> Input: 'VP Eng' -> Output: ..."

### 3. Chain-of-Thought (CoT)
**Definition:** Asking the model to "Think step-by-step" or "Explain your reasoning" before giving the final answer.
**Use Case:** Debugging a race condition in `Thinker`'s sync logic or a complex CSS z-index issue.
**Knobby Example (Thinker Sync Debugging):**
> "The `sync-manager.js` is failing to update the server state when two nodes are moved simultaneously.
> **Instruction:** First, analyze the `markIdeaUpdated` function's debounce logic. Second, trace the websocket message flow. Third, identify where the state is being overwritten. Finally, provide the fix."

### 4. Tree of Thoughts (ToT)
**Definition:** Generating multiple "thoughts" (potential solutions) at each step, evaluating them, and discarding bad paths.
**Use Case:** Designing the architecture for the new "Diagrams" AI feature.
**Knobby Example (Diagrams AI Architecture):**
> "We need to add AI generation to the `Diagrams` app.
> **Step 1:** Propose 3 distinct approaches (e.g., Client-side generation, Server-side streaming, Hybrid).
> **Step 2:** Critique each approach based on latency, token cost, and security.
> **Step 3:** Select the best approach for our Python backend + Vanilla JS frontend stack.
> **Step 4:** Detail the implementation plan for the selected approach."

### 5. Retrieval Augmented Generation (RAG)
**Definition:** Injecting relevant code snippets or documentation into the prompt context.
**Use Case:** Writing code that depends on internal libraries (e.g., `KnobbyAPI`) or specific project conventions (`CODING_STYLE.md`).
**Knobby Example (Using Internal API):**
> "I need to fetch the current user's tenant ID in `frontend/js/shell.js`.
> **Context:** Here is the content of `frontend/static/auth.js` [INSERT FILE CONTENT].
> **Task:** Write the function to get the tenant ID using the exposed methods in `auth.js`."

### 6. ReAct (Reasoning + Acting)
**Definition:** An iterative process: `Thought -> Action (Tool Use) -> Observation -> Thought`.
**Use Case:** Root cause analysis where the bug's location is unknown.
**Knobby Example (Bug Investigation):**
> "Users report a 404 error when saving a session.
> **Thought 1:** I need to check the backend routes.
> **Action 1:** `search_file_content(pattern='/api/session', dir_path='api/Controllers')`
> **Observation 1:** Found `SessionsController.cs`.
> **Thought 2:** I need to check the `Save` method signature.
> **Action 2:** `read_file('api/Controllers/SessionsController.cs')`
> ... (Repeat until bug is found)"

### 7. Graph Prompting
**Definition:** Representing the problem as a graph (Nodes/Edges) to leverage the LLM's spatial/relational reasoning.
**Use Case:** analyzing dependencies in `Strukture` or ensuring connectivity in `Thinker`.
**Knobby Example (Strukture Dependency Check):**
> "Given the following list of nodes and 'reports_to' edges in `Strukture`:
> [List of Edges...]
> Identify any circular reporting relationships (cycles) that would break the org chart renderer."

---

## Instructions for Agents

1.  **Pause & Assess:** Before generating code, check the complexity of the request.
2.  **Select Technique:** Use the Decision Matrix above.
3.  **Construct Prompt:** Apply the chosen technique. Don't just ask "Write X".
4.  **Refine:** If the output is poor, escalate the technique (e.g., move from Zero-shot to CoT).
