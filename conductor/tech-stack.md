# Tech Stack - Contextware

## Language & Runtime
- **Python (>=3.13):** The project is built using modern Python with strictly enforced versions.

## Build & Dependency Management
- **uv:** Efficient package management and dependency resolution for the Python environment.

## Primary Frameworks & Libraries
- **FastEmbed:** High-performance local text embeddings for efficient semantic search.
- **LanceDB:** Serverless vector database optimized for persistent project context.
- **Fire (CLI):** Simplifies the creation of a powerful command-line interface for the agent skill.
- **Pydantic:** Robust data validation and settings management.

## Project Structure
- **Agent Skill Layout:** All source code and skill logic are located in the `scripts/` directory (e.g., `db.py`, `recall.py`, `store.py`).
- **Test Codebases:** The `codebases/` directory contains example code used specifically for testing and benchmarking the skill's performance.
