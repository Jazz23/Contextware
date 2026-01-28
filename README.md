# Contextware

**Contextware** is an advanced agent skill designed to serve as the persistent cognitive layer for AI software engineering assistants. It automatically captures, organizes, and retrieves the critical context that is often lost between sessions, transforming ephemeral interactions into a continuous, coherent development lifecycle.

## 🧠 The Problem
AI agents typically operate in a "stateless" manner or rely on limited context windows. They often forget:
- Why a specific architectural decision was made three days ago.
- The high-level "trajectory" or goal of a refactoring effort.
- The semantic purpose of specific files beyond their code syntax.
- User preferences established in previous conversations.

## 💡 The Solution
Contextware acts as a dedicated "hippocampus" for the project. It runs in the background, maintaining a dynamic, queriable record of the project's state and history.

### Key Features

#### 1. 📂 Deep File Intelligence
Contextware doesn't just read files; it indexes them.
- **Content Tracking**: Monitors file modifications in real-time.
- **Semantic Summarization**: Automatically generates and updates descriptions of *what* a file does and *why* it exists.

#### 2. 💬 Conversation & Decision Memory
- **Interaction Logging**: Archives key insights, decisions, and user instructions from previous chat sessions.
- **RAG-Powered Retrieval**: Uses Retrieval-Augmented Generation to surface relevant past conversations when they are contextually appropriate for the current task.

#### 3. 🚀 Trajectory Alignment
- **Roadmap Awareness**: Keeps track of the "North Star" goals of the project.
- **Progress Monitoring**: analyzing the delta between the current state and the intended milestones.
- **Drift Detection**: Alerts when code changes seem to diverge from the established architectural patterns or project goals.

## 🛠️ How It Works
Contextware integrates directly into the agent's toolchain. When activated, it:
1.  **Scans**: Performs an initial analysis of the directory structure.
2.  **Embeds**: Vectorizes code snippets, comments, and documentation.
4.  **Serving**: Provides a specialized query API that the main agent can use to ask questions like *"Where is the authentication logic handled?"* or *"What did we decide about the database schema last week?"*