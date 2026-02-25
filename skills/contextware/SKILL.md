---
name: contextware
description: Persistent, semantic memory for software development. Remembers project decisions, user preferences, and high-level code purpose. Designed for coding agents to RAG from the codebase and past sessions to provide context-aware assistance. Use with every prompt.
---

## Constraints

- Do not read or modify any files in the `skills/contextware` folder except for ones you've been explicitly instructed to. Do not include them in the database (do not use `scripts/store.py` to index them).

- Do not read the contents of files in the codebase directly. Always use `scripts/recall.py` to check if the file has been indexed and if the information is stale. Only read the file directly if `recall.py` indicates it's stale or it hasn't been indexed before.

- Do not index the codebase once this skill is loaded. Only index files as needed.

- Execute all commands in the `.gemini/skills/contextware` folder. This means the root of the project will be "../../../". For example, if trying to index `main.py` located at the root, the path argument should be `--path "../../../main.py"`.

- Do not do anything after activating this skill and loading the spec. Do not search for existing facts/episodes or anything. Wait for explicit instructions.

## Load the Spec

Read the file `references/spec.md` to understand the full syntax of the database.

## Store Instructions

1.  **Capture Facts:** When a user specifies a preference (e.g., "Always use functional components") or you discover a hard constraint or fact, save it immediately as a **fact**.

2.  **Record Outcomes:** After completing a non-trivial task (fixing a bug, implementing a feature), record an **episode**. This helps in future sessions to understand *why* certain decisions were made.

3. **Index Files:** When you need to understand a file, first check if it's indexed using `recall`. If the file is not in the database, or it comes up as [STALE], read the file yourself, extract relevant information/come up with a detailed summary, and store it in the database with `scripts/store.py`. For Python files, use automatic symbol extraction; for other languages, provide symbols manually. You should also re-index files you have modified yourself.

## Recall Instructions

1. **Fact Retrieval:** When needing to perform a task that requires a preference of some kind, or when the user requests information (unrelated to file contents/functionality), first query the database for relevant **facts**.

1.  **Episode Recovery** When required to perform or discuss a complicated task, first run a `recall` query with the task's goal to see if there's any relevant "institutional knowledge" in the semantic memory. This can provide valuable context and insights from past experiences.

3. **Source File Retrieval**: When needing to gather information regarding source code or files for any reason, instead of reading the file directly, recall using `scripts/recall.py` first to check if it's already been indexed.