# Contextware Skill Specification

This document describes the command-line interface for the Contextware skill, which provides long-term memory, episodic recording, and codebase indexing.

## Core Commands

All commands are executed using `uv run`.

### Storing and Managing Information (`store.py`)

The `store.py` script is used to add or remove information from the Contextware database.

#### Facts (Long-term Memory)

*   **Store a Fact**
    ```bash
    uv run skills/contextware/scripts/store.py --type fact --content "Your fact text here"
    ```
    Stores a semantic fact in the long-term memory.

*   **Delete a Fact**
    ```bash
    uv run skills/contextware/scripts/store.py --type fact --content "query string" --delete
    ```
    Deletes the first fact that matches the query string (using partial matching).

#### Episodes (Experience Recording)

*   **Store an Episode**
    ```bash
    uv run skills/contextware/scripts/store.py --type episode --goal "Goal description" --result "Success/Failure" --category "Task Category" --content "Detailed summary of what happened"
    ```
    Records a specific task execution episode.

*   **Delete an Episode**
    ```bash
    uv run skills/contextware/scripts/store.py --type episode --goal "goal query" --delete
    # OR
    uv run skills/contextware/scripts/store.py --type episode --content "summary query" --delete
    ```
    Deletes the first episode matching the provided goal or summary query.

#### Codebase Indexing

*   **Index a File (Auto-extract symbols for Python)**
    ```bash
    uv run skills/contextware/scripts/store.py --type index --path "path/to/file.py" [--content "Optional summary"]
    ```
    Indexes a file. For Python files, it automatically extracts classes, methods, and top-level functions.

*   **Index a File (Manual symbols)**
    ```bash
    uv run skills/contextware/scripts/store.py --type index --path "path/to/file" --classes '{"ClassName": ["method1", "method2"]}' --functions "func1,func2" --content "File summary"
    ```
    Manually provides metadata for a file.

*   **Delete a File Index**
    ```bash
    uv run skills/contextware/scripts/store.py --type index --path "path/to/file" --delete
    ```
    Removes the specified file from the codebase index.

---

### Retrieving Information (`recall.py`)

The `recall.py` script is used to search the Contextware database.

#### Semantic Search

*   **Search All Scopes**
    ```bash
    uv run skills/contextware/scripts/recall.py --query "your search query"
    ```
    Performs a semantic search across facts, episodes, and the codebase index.

*   **Search Specific Scope**
    ```bash
    uv run skills/contextware/scripts/recall.py --query "your search query" --scope [fact|episodes|code]
    ```
    Restricts the search to a specific scope (`fact` (or `memory`), `episodes`, or `code`).

*   **Limit Search Results**
    ```bash
    uv run skills/contextware/scripts/recall.py --query "your search query" --limit 10
    ```
    Specifies the maximum number of results to return (default is 5).

#### Metadata Lookup

*   **Look up File Metadata**
    ```bash
    uv run skills/contextware/scripts/recall.py --path "path/to/file"
    ```
    Retrieves the indexed summary and symbol metadata for a specific file. It also checks if the index is stale (if the file has been modified since it was last indexed).
