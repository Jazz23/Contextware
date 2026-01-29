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

#### B. Storage CLI (`scripts/storage.py`)
*   **Command:** `save-index --payload <BASE64_JSON>`
*   **Functionality:**
    1.  Decode Base64 payload containing `path`, `summary`, and `symbols`.
    2.  Generate embedding using `fastembed` (local).
    3.  Upsert record into LanceDB.

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
2.  **DB & Schema:** Create `db.py` to handle table creation and connections.
3.  **Storage Logic:** Implement `storage.py` to handle the Base64 payload and vector embedding.
4.  **Crawler Implementation:** Build the Python walker and the subprocess logic to pipe data to Gemini.
5.  **Skill Integration:** Create `SKILL.md` so the Gemini CLI knows how to trigger a full crawl.
