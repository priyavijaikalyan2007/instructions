<!-- AGENT: Traditional AI/ML techniques and decision matrix for non-LLM approaches. -->

# Non-LLM AI/ML Techniques Guide for Coding Agents

**Goal:** Efficiently solve problems using specialized AI/ML techniques. While LLMs are powerful, traditional ML and graph algorithms are often faster, cheaper, deterministic, and more interpretable for specific tasks.

## Decision Matrix: Selecting a Non-LLM Technique

| Task Type | Problem Characteristics | Recommended Technique | Why? |
| :--- | :--- | :--- | :--- |
| **Graph Analysis** | Network structures, hierarchies, connectivity | **Graph Algorithms** (PageRank, Centrality) | Native to the data structure; mathematically proven results. |
| **Pattern Finding** | Outliers in logs, unusual data points | **Anomaly Detection** (Isolation Forest) | Specialized for finding deviations from the norm. |
| **Grouping** | Unlabeled data, organizing large sets | **Clustering** (K-Means, DBSCAN) | Discovers inherent structure without semantic understanding. |
| **Prediction** | Numerical forecasting, trends | **Regression** (Linear/Logistic) | Precise mathematical modeling of relationships. |
| **Categorization** | Labeled data sorting, tagging | **Classification** (SVM, Random Forest) | Fast, efficient training on specific domains. |
| **Search** | Exact/Fuzzy keyword matching | **Classic IR** (TF-IDF, BM25) | Better for specific keyword recall than semantic search. |

---

## Technique Details & Knobby.io Examples

### 1. Graph Algorithms
**Definition:** Mathematical algorithms that process data represented as graphs (nodes and edges) to find relationships, paths, and structural importance.
**Knobby Use Case:** Core logic for `Strukture` (org charts) and `Thinker` (concept maps).
**Knobby Examples:**
*   **Centrality Analysis (`Strukture`):** Use **Betweenness Centrality** to identify "bridge" employees who connect different departments.
    *   *Prompt:* "Implement a Betweenness Centrality algorithm in JavaScript to highlight key connector nodes in the org chart."
*   **Pathfinding (`Thinker`):** Use **Dijkstra's Algorithm** or **A*** to find the shortest connection between two distant concepts in a large mind map.
*   **Cycle Detection (`Strukture`):** Use **DFS (Depth-First Search)** to prevent invalid reporting lines (someone reporting to their own subordinate).

### 2. Anomaly Detection
**Definition:** Identifying rare items, events, or observations which raise suspicions by differing significantly from the majority of the data.
**Knobby Use Case:** System health monitoring and data integrity.
**Knobby Examples:**
*   **Log Monitoring:** Use **Isolation Forest** on backend logs to automatically flag unusual error spikes or latency issues that deviate from the baseline.
*   **Data Integrity (`Strukture`):** Flag potential data entry errors, such as a "Manager" having 0 reports or an "Intern" having 50 reports (outliers in `report_count` vs `role` distribution).

### 3. Clustering
**Definition:** Grouping a set of objects in such a way that objects in the same group (called a cluster) are more similar to each other than to those in other groups.
**Knobby Use Case:** Organizing user-generated content.
**Knobby Examples:**
*   **Auto-Categorization (`Thinker`):** Use **K-Means** or **DBSCAN** on 2D node coordinates to automatically create visual "Groups" or "Zones" for ideas that are placed close together on the canvas.
*   **User Segmentation:** Group tenants based on usage patterns (e.g., "Heavy Thinker Users", "Strukture Power Users") for feature targeting.

### 4. Regression
**Definition:** Estimating the relationships among variables. It focuses on the relationship between a dependent variable and one or more independent variables.
**Knobby Use Case:** Performance optimization and resource planning.
**Knobby Examples:**
*   **Load Prediction:** Use **Linear Regression** on historical API traffic data to predict server load for the next hour and auto-scale resources.
*   **Canvas Performance:** Predict rendering time based on node count and edge count to proactively switch to "low fidelity" mode for large graphs.

### 5. Classification
**Definition:** Identifying which of a set of categories a new observation belongs to, on the basis of a training set of data containing observations (or instances) whose category membership is known.
**Knobby Use Case:** Triage and organization.
**Knobby Examples:**
*   **Support Ticket Triage:** Train a **Random Forest** classifier on past support tickets to automatically tag new tickets as "Bug", "Feature Request", or "Billing" based on keywords (if we add a support system).
*   **Node Type Prediction (`Strukture`):** Predict a node's type (e.g., "Person" vs "Department") based on its attributes if the user leaves it blank.

---

## Instructions for Agents

1.  **Evaluate first:** Can this be solved with math/stats? If yes, avoid the LLM.
2.  **Library Selection:**
    *   **JavaScript (Frontend):** `graphology` (graphs), `simple-statistics` (regression), `clustering.js`.
    *   **Python (Backend):** `scikit-learn` (ML), `networkx` (graphs), `pandas` (data analysis).
3.  **Implementation:**
    *   Propose the algorithm clearly.
    *   Ensure data preprocessing steps are defined (e.g., normalizing coordinates for clustering).
    *   Implement efficient, vectorized operations where possible.
4.  **Hybrid Approach:** Consider **ReAct** (from `LLM_TECHNIQUES.md`) where the "Action" is running one of these specific ML algorithms.
    *   *Example:* "I need to group these ideas. -> Action: Run K-Means on coordinates. -> Observation: Found 3 clusters. -> Thought: I will label them..."
