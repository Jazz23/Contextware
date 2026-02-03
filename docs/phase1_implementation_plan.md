# Implementation Plan: Contextware Phase 1
## Infrastructure & Code Indexing

This phase focuses on setting up the local vector database and implementing the background process that summarizes and indexes the codebase.

### 1. Project Structure
The project will be located in the root `skills/` directory.

```text
skills/contextware/
├── SKILL.md                 # Agent instructions
├── pyproject.toml           # uv configuration
├── scripts/
│   ├── db.py                # LanceDB connection & schema
│   ├── storage.py           # CLI for database operations
│   ├── crawl_project.py     # File walker & Gemini aggregator
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

#### B. Storage CLI (`scripts/save_fact.py`)
*   **Command:** `save_fact.py --type fact|episode [--goal G] [--result R] [--category C] "<content>"`
*   **Functionality:**
    1.  Generate embedding using `fastembed`.
    2.  For episodes, concatenate goal and summary for the embedding input.
    3.  Upsert record into the appropriate LanceDB table.

#### C. Crawler Script (`scripts/crawl_project.py`)
*   **Functionality:**
    1.  Recursively walk the project directory (respecting `.gitignore`).
    2.  Filter out large files (>100KB) and binary files.
    3.  Concatenate content with headers: `--- FILE: <path> ---`.
    4.  Invoke the headless Gemini agent:
        `cat <concated_files> | gemini -p "<INDEX_PROMPT>"`

### 3. Headless Agent Strategy
The `crawl_project.py` script will use a specialized prompt to guide the headless Gemini instance:

**Index Prompt:**
> Analyze each file provided in the stream. For each:
> 1. Generate a 1-2 sentence summary.
> 2. Extract key symbols.
> 3. Create a JSON: `{"path": "...", "summary": "...", "symbols": [...]}`.
> 4. Base64 encode the JSON.
> 5. Execute: `uv run skills/contextware/scripts/storage.py save-index --payload <BASE64>`.

### 4. Implementation Steps

1.  **Environment Setup:** Initialize `uv` project in `skills/contextware/` with dependencies (`lancedb`, `fastembed`, `pydantic`, `fire`).
2.  **DB & Schema:** Create `db.py` to handle table creation for `code_index`, `facts`, and `episodes`.
3.  **Storage Logic:** Implement `save_fact.py` and `storage.py` (for codebase indexing) to handle vector embedding and metadata.
4.  **Crawler Implementation:** Build the Python walker and the subprocess logic to pipe data to Gemini.
5.  **Recall Logic:** Implement `recall.py` to search across scopes and format episodic results with their `[RESULT]` and `[CATEGORY]` markers.
6.  **Skill Integration:** Create `SKILL.md` so the Gemini CLI knows how to trigger a full crawl and record outcomes.
