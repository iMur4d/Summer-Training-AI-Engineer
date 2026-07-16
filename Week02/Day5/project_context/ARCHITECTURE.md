# Architecture

This document outlines the high-level system architecture of the AI Thought Refinement Assistant.

## System Flow

```text
User
  ↓
Telegram Bot
  ↓
LLM
  ↓
Validator
  ↓
Knowledge JSON
  ↓
Markdown Generator
  ↓
Vault (Obsidian)
  ↓
Frontend (Knowledge OS)
```

## Component Responsibilities

- **Telegram Bot (`telegram_bot/`):** Serves as the entry point for user interaction, receiving incoming messages and replying with success or failure confirmations.
- **LLM (`backend/llm.py`):** Handles communication with the Gemini model to parse the user's raw thought into structured data.
- **Validator (`backend/validator.py`):** Ensures the LLM's response adheres to the strict expected JSON schema before allowing it to proceed.
- **Markdown Generator (`backend/markdown_generator.py`):** Transforms the validated JSON knowledge representation into a clean, formatted Markdown document.
- **Vault/Storage (`backend/storage.py`):** Responsible for safely saving the generated Markdown files to the local file system while handling filename collisions and OS errors.
- **Frontend (`frontend/`):** A Streamlit-based "Knowledge OS" interface that visually renders the local vault contents as a 3D graph for exploration and reading.
