# Architecture & Design Decisions

This document records the major engineering decisions made during the development of the MVP and the reasoning behind them.

---

## Markdown over Database

**Decision**

Store generated knowledge as Markdown files instead of using a database.

**Reason**

Markdown keeps the knowledge portable, human-readable, and fully compatible with Obsidian.

**Impact**

Users always own their notes and can access them without the application.

---

## Provider-Agnostic LLM Architecture

**Decision**

Separate the LLM communication layer from the rest of the application.

**Reason**

The project should be able to support different language models in the future with minimal changes.

**Impact**

Changing the LLM provider should only require modifying the communication layer.

---

## Layered Architecture

**Decision**

Separate responsibilities into independent modules.

**Reason**

Each module should solve one problem only.

**Impact**

The codebase is easier to maintain, test, and extend.

---

## Preserve User Meaning

**Decision**

The assistant must organize information without creating new knowledge.

**Reason**

The goal is thought refinement, not content generation.

**Impact**

Missing information is reported as Open Questions instead of being hallucinated.

---

## Local Knowledge Vault

**Decision**

Store notes inside a local Obsidian vault.

**Reason**

Users should keep complete ownership of their knowledge while benefiting from existing Obsidian workflows.

**Impact**

The generated notes remain accessible even without the application.

---

## Strict Thought Classification

**Decision**

Enforce exactly 6 static categories (`Concept, Task, Question, Observation, Insight, Research Idea`) for the `thought_type` field across both the LLM prompt and the Python validation layer.

**Reason**

LLMs are prone to hallucinating arbitrary categories (e.g., "Project Idea", "Note", "Brainstorm") which fragments the knowledge base. A strictly constrained list forces the AI to extract the underlying abstract knowledge model rather than just acting as a summarizer.

**Impact**

The frontend visualization can safely and deterministically group nodes by type, and the user gains a highly organized, predictable vault structure.

---

## Review-Before-Save Workflow

**Decision**

Implement an in-memory `PENDING_NOTES` state in the Telegram bot to display a preview of the parsed thought alongside inline Save/Discard buttons, rather than saving to disk immediately.

**Reason**

LLMs occasionally misinterpret a thought or miss the user's intent. Giving the user a chance to review the generated structure ensures that no corrupted, hallucinated, or incorrect notes permanently pollute the Obsidian vault.

**Impact**

The bot architecture requires lightweight state management and callback handlers, but the resulting data purity in the vault is vastly improved.

---

## MVP Scope Protection

**Decision**

Keep the MVP intentionally small.

**Reason**

Deliver a stable end-to-end workflow before introducing advanced capabilities.

**Impact**

Features such as semantic search, embeddings, RAG, automatic note linking, local LLMs, and multi-turn memory are intentionally deferred to future versions.
