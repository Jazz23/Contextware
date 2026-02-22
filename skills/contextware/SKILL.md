---
name: contextware
description: Persistent, semantic memory for software development. Remembers project decisions, user preferences, and high-level code purpose. Designed for coding agents to RAG from the codebase and past sessions to provide context-aware assistance. Use with every prompt.
---

## Constraints

- Do not read or modify any files in the `skills/contextware` folder except for ones you've been explicitly instructed to. Do not include them in the database (do not use `scripts/store.py` to index them).

- Do not read the contents of files in the codebase directly. Always use `scripts/recall.py` to check if the file has been indexed and if the information is stale. Only read the file directly if `recall.py` indicates it's stale or it hasn't been indexed before.

- Do not index the codebase once this skill is loaded. Only index files as needed.

- Execute all commands in the `.gemini/skills/contextware` folder.

## Load the Spec

Read the file `references/spec.md` to understand the full syntax of the database.

## Store Instructions

1.  **Capture Facts:** When a user specifies a preference (e.g., "Always use functional components") or you discover a hard constraint or fact, save it immediately as a **fact**.

2.  **Record Outcomes:** After completing a non-trivial task (fixing a bug, implementing a feature), record an **episode**. This helps in future sessions to understand *why* certain decisions were made.

## Recall Instructions

3.  **Episode Recovery** When required to perform or discuss a complicated task, first run a `recall` query with the task's goal to see if there's any relevant "institutional knowledge" in the semantic memory. This can provide valuable context and insights from past experiences.

4.  **Stay Fresh:** If `recall` returns a `[STALE]` marker for a file, or the file hasn't been indexed before, you should read the file directly to get the most accurate information, then update the contextware database with the new content by indexing the file with `scripts/store.py`. If the codebase is in python, use automatic symbol extraction; otherwise, manually provide symbols.

6. **Recall**: When needing to gather information regarding source code or files, instead of reading the file directly, recall using `scripts/recall.py` first to check if it's already been indexed.