# Architecture

This document outlines the high-level system architecture of the AI Thought Refinement Assistant (v1.0.0).

## System Flow

```text
User
  ↓
Telegram Bot
  ↓
LLM (Thought Refinement Engine)
  ↓
Validator
  ↓
Telegram Bot (Preview & Review)
  ↓
User (Clicks Save)
  ↓
Markdown Generator
  ↓
Vault (Obsidian Local Storage)
  ↓
Frontend (3D Knowledge OS)
```

## Component Responsibilities

- **Telegram Bot (`telegram_bot/`):** Serves as the interactive entry point. It receives raw thoughts, displays a structured Markdown preview of the LLM's classification, and manages the state of pending notes while waiting for user confirmation (Save/Discard).
- **LLM (`backend/llm.py`):** Handles communication with the Gemini API to extract the abstract knowledge model from the user's raw thought, constrained by a strict system prompt.
- **Validator (`backend/validator.py`):** Ensures the LLM's response adheres to the strict JSON schema and exactly matches one of the 6 allowed `thought_types` before allowing it to proceed to the preview stage.
- **Markdown Generator (`backend/markdown_generator.py`):** Transforms the validated JSON knowledge representation into a clean, formatted Markdown document with YAML frontmatter.
- **Vault/Storage (`backend/storage.py`):** Responsible for safely saving the generated Markdown files to the local file system, generating collision-resistant slugs, and handling OS file errors.
- **Frontend (`frontend/`):** A Streamlit-based "Knowledge OS" interface that visually renders the local vault contents. It maps the notes into an immersive 3D space, sizing them by recency and grouping them visually by `thought_type`.
