# Contextware

Persistent, semantic memory for software development. Remembers project decisions, user preferences, and high-level code purpose.

## Commands

Use the following commands via `run_shell_command`. **ALWAYS** execute these from the `/workspaces/Contextware/skills/contextware` directory using `uv run`.

### Storing Information

- **Facts:** Save a persistent preference, constraint, or project decision.
  ```bash
  uv run scripts/store.py --type fact --content "<fact>"
  ```
- **Episodes:** Record the outcome of a significant task.
  ```bash
  uv run scripts/store.py --type episode --goal "<goal>" --result "success|failure|partial" --category "<category>" --content "<summary_of_actions_and_lessons>"
  ```
- **Indexing:** Manually index a file with a summary.
  ```bash
  uv run scripts/store.py --type index --path <path> --content "<summary>"
  ```

### Recalling Information

- **Search:** Retrieve relevant context from all or specific scopes.
  ```bash
  uv run scripts/recall.py --query "<query>" [--scope "all|memory|episodes|code"] [--limit 5] [--mode "summary|exact"]
  ```

### Maintenance

- **Crawl:** Re-index the entire project (crawls `.py`, `.md`, `.ts`, `.js`, `.json` files).
  ```bash
  uv run scripts/store.py --type crawl [--path <dir_path>]
  ```

## Strategy & Best Practices

1.  **Capture Facts:** When a user specifies a preference (e.g., "Always use functional components") or you discover a hard constraint, save it immediately as a **fact**.
2.  **Record Outcomes:** After completing a non-trivial task (fixing a bug, implementing a feature), record an **episode**. This helps in future sessions to understand *why* certain decisions were made.
3.  **Bootstrap Context:** At the start of a new session or task, run a `recall` query with the task's goal to see if there's any relevant "institutional knowledge" in the semantic memory.
4.  **Stay Fresh:** If `recall` returns a `[STALE]` marker for a file, it means the file has changed since it was last indexed. You should read the file directly to get the most accurate information.
