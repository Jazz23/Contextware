---
name: contextware
description: Persistent, semantic memory for software development. Remembers project decisions, user preferences, and high-level code purpose. Designed for coding agents to RAG from the codebase and past sessions to provide context-aware assistance. Use with every prompt.
---

## Constraints

Do not read or modify any files in the `skills/contextware` folder except for ones you've been explicitly instructed to.

## Load the Spec

Read the file `references/spec.md` to understand the full syntax of the database. All commands must be executed in the `contextware` folder.

## Strategy & Best Practices

1.  **Capture Facts:** When a user specifies a preference (e.g., "Always use functional components") or you discover a hard constraint or fact, save it immediately as a **fact**.
2.  **Record Outcomes:** After completing a non-trivial task (fixing a bug, implementing a feature), record an **episode**. This helps in future sessions to understand *why* certain decisions were made.
3.  **Bootstrap Context:** At the start of a new session or task, if needed run a `recall` query with the task's goal to see if there's any relevant "institutional knowledge" in the semantic memory.
4.  **Stay Fresh:** If `recall` returns a `[STALE]` marker for a file, or the file hasn't been indexed before, you should read the file directly to get the most accurate information, then update the contextware database with the new content by indexing the file with `scripts/store.py`. If the codebase is in python, use automatic symbol extraction; otherwise, manually provide symbols.
