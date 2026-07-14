# AI Thought Refinement Assistant
## Software Specification (MVP)

## Project Overview

The AI Thought Refinement Assistant is an application that helps users transform raw, unstructured thoughts into organized and reusable knowledge.

The application does **not** generate new knowledge or expand ideas beyond the user's intent. Its primary responsibility is to refine, organize, and structure the user's own thinking while preserving the original meaning.

The output is stored as Markdown notes inside a local Obsidian vault.

---

# Objective

Build a minimal working MVP that demonstrates the complete workflow from user input to Markdown note generation.

The MVP should prioritize simplicity, readability, and modularity over advanced features.

---

# Functional Requirements

The application shall:

1. Receive a text message from a Telegram bot.

2. Send the user's message to an LLM.
2.1 If the message does not represent a meaningful thought, idea, or note
     (e.g., a greeting or general question), the assistant must politely
     reject it instead of generating a note, and reply to the user
     accordingly on Telegram.

3. Transform the raw thought into a structured note containing:

- Title
- Summary
- Key Points
- Tags
- Open Questions (only when information is incomplete)

4. Generate a Markdown document.

5. Save the Markdown file into a local folder that represents an Obsidian vault.

---

# Non-Functional Requirements

The project should:

- Be written in Python.
- Use clean and modular architecture.
- Keep responsibilities separated across modules.
- Store secrets inside a `.env` file.
- Be easy to understand for educational purposes.
- Prefer readability over optimization.

---

# MVP Scope

Included:

- Telegram text messages only.
- Single-turn interaction.
- Gemini API as the LLM provider.
- Markdown generation.
- Local file storage.

Not Included:

- Voice messages.
- Images.
- PDFs.
- Databases.
- Authentication.
- User accounts.
- Cloud deployment.
- Embeddings.
- Vector databases.
- Semantic search.
- Automatic note linking.
- Multi-turn conversations.
- Follow-up questions.
- Retrieval-Augmented Generation (RAG).

---

# Architecture Principles

The application should separate responsibilities into independent modules.

Expected responsibilities include:

- Telegram communication
- LLM communication
- Markdown generation
- Local file storage

Each module should have a single responsibility.

---

# Output Requirements

The generated note must preserve the user's original meaning.

The AI should never invent missing information.

If required information is missing, it should be listed under:

Open Questions

instead of being hallucinated.

---

# Error Handling

The application should gracefully handle:

- Missing API keys
- Telegram connection errors
- LLM request failures
- File writing failures

Errors should provide clear messages without crashing unexpectedly.

---

# Coding Guidelines

The project should:

- Use descriptive names.
- Keep functions small.
- Avoid duplicated logic.
- Avoid unnecessary dependencies.
- Use type hints when appropriate.
- Add comments only when they improve understanding.

---

# Future Features (Out of Scope)

The following ideas are intentionally excluded from the MVP:

- Obsidian backlinks
- Automatic note linking
- Knowledge graph
- OCR
- Voice input
- Mobile application
- Web interface
- Docker optimization
- Local Ollama models
- Multi-agent workflows

These may be implemented in future versions but must not be added during the MVP unless explicitly requested.

---

# Success Criteria

The MVP is considered complete when the following workflow functions successfully:

Telegram Message

↓

LLM Processing

↓

Structured Markdown Generation

↓

Markdown File Saved Locally

No additional features should be implemented unless explicitly requested.

-----------
This specification is the single source of truth for the project.

If a requested implementation conflicts with this specification, ask for clarification instead of making assumptions.

Do not introduce additional features, libraries, or architectural changes unless explicitly approved.