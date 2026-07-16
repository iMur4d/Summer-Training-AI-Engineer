# Obsidian Brain (v1.0.0 MVP)

## Overview

Obsidian Brain is an AI-powered Thought Refinement system that transforms your raw ideas, observations, and tasks into structured knowledge directly via Telegram, saving them into a local Obsidian Vault. It features a stunning 3D Knowledge OS interface to visualize and explore your thoughts.

## Project State: v1.0.0 (MVP Complete)

The MVP is functionally complete and production-ready.

The repository is organized into a clean, modular architecture:

* `backend/` — Core application logic (LLM intelligence, validation, Markdown generation, storage).
* `telegram_bot/` — Interactive Telegram interface with Save/Discard review flows.
* `frontend/` — Streamlit application and custom 3D web assets.
* `project_context/` — Project documentation and development context.
* `vault/` — Local Obsidian knowledge base.

---

## Core Features

### 1. Thought Refinement (LLM)
- Acts as a knowledge extraction engine, not a simple summarizer.
- Strictly categorizes input into one of 6 types: `Concept, Task, Question, Observation, Insight, Research Idea`.
- Handles invalid inputs (conversations, greetings, empty messages) gracefully without attempting to save them.

### 2. Telegram Bot Workflow
- Users send raw thoughts via Telegram.
- The bot replies with a structured Markdown preview of how the AI parsed the thought.
- Inline `[Save]` and `[Discard]` buttons allow the user to review the thought before committing it to the vault.

### 3. Safe Local Storage
- Automatically generates safe, collision-resistant filenames.
- Outputs clean Markdown files with YAML frontmatter fully compatible with Obsidian.

### 4. Knowledge OS Interface
- A visually immersive dashboard built with Streamlit and Three.js.
- **Data-Driven Visualization**: Notes are placed in a 3D brain silhouette, colored strictly by their `thought_type`.
- **Recency Scaling**: Newer thoughts appear larger and pulse visibly, gradually shrinking over 30 days.
- **Hover Logic**: Hovering over a note visually highlights all other notes of the same type.
- Features a searchable left-hand sidebar and a polished reading workspace for markdown files.

---

## How to Run

### Telegram Bot

```bash
python -m telegram_bot.main
```

### Knowledge OS Interface

```bash
streamlit run frontend/app.py
```

---

## Future Vision

The v1.0.0 MVP focuses entirely on transforming single thoughts into structured notes safely and accurately. 

Future advanced capabilities remain outside the current scope but are planned for post-v1.0.0 development:
- Semantic linking & AI embeddings
- Vector databases (RAG)
- Contextual memory graphs
- Automatic note relationship mapping
- Cloud deployment and live synchronization
