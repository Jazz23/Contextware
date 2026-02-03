# Implementation Plan: Contextware Phase 1
## Infrastructure & Semantic Memory

This phase focuses on setting up the local vector database and implementing the mechanisms to save and recall facts and task outcomes.

### 1. Project Structure
The project will be located in the root `skills/` directory.

```text
skills/contextware/
├── SKILL.md                 # Agent instructions
├── pyproject.toml           # uv configuration
├── scripts/
│   ├── db.py                # LanceDB connection & schema
│   ├── store.py             # CLI for all write operations (facts, episodes, index)
│   └── recall.py            # (Placeholder) Search logic
└── data/                    # Vector DB storage (gitignored)
```

### 2. Core Components

#### A. Database Layer (`scripts/db.py`)
*   **Technology:** LanceDB.
*   **Schema (`code_index`):**
    *   `file_path` (string): Primary Key.
    *   `summary` (string): Semantic description.
    *   `symbols` (list[string]): Extracted classes/functions.
    *   `last_modified` (float): Timestamp for staleness checks.
    *   `vector` (vector): 384-dim embedding of the summary.
*   **Schema (`facts`):**
    *   `content` (string): The fact.
    *   `vector` (vector): 384-dim embedding.
*   **Schema (`episodes`):**
    *   `goal` (string): Objective.
    *   `summary` (string): Actions/Lessons.
    *   `result` (string): success/failure/partial.
    *   `category` (string): e.g., shell, git.
    *   `timestamp` (float).
    *   `vector` (vector): 384-dim embedding of goal + summary.

#### B. Storage CLI (`scripts/store.py`)
*   **Command:** `store.py --type fact|episode|index [--goal G] [--result R] [--category C] [--path P] ["<content>"]`
*   **Functionality:**
    1.  Generate embedding using `fastembed`.
    2.  For episodes, concatenate goal and summary for the embedding input.
    3.  Upsert record into the appropriate LanceDB table.
    4.  (For index) Invoke headless Gemini to summarize the file at `--path`.

### 4. Implementation Steps

1.  **Environment Setup:** Initialize `uv` project in `skills/contextware/` with dependencies (`lancedb`, `fastembed`, `pydantic`, `fire`).
2.  **DB & Schema:** Create `db.py` to handle table creation for `code_index`, `facts`, and `episodes`.
3.  **Storage Logic:** Implement `store.py` to handle vector embedding, metadata, and codebase indexing triggers.
4.  **Recall Logic:** Implement `recall.py` to search across scopes and format episodic results with their `[RESULT]` and `[CATEGORY]` markers.
5.  **Skill Integration:** Create `SKILL.md` so the Gemini CLI knows how to record and recall facts and outcomes.
