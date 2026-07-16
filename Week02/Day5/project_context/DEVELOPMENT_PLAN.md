# Development Plan

# Version Roadmap

The application must be developed incrementally.

Each version must be fully functional before moving to the next one.

Never skip versions.

Do not implement features from future versions.

---

## v0.1.0 — Telegram Communication ✅ Complete

Goal: A working Telegram bot.

---

## v0.2.0 — LLM Integration ✅ Complete

Goal: Connect the Telegram bot to Gemini/Gemma.

---

## v0.3.0 — Thought Refinement ✅ Complete

Goal: Transform raw thoughts into structured knowledge (Title, Summary,
Key Points, Tags, Open Questions), without hallucinating missing information.

---

## v0.4.0 — Markdown Generation ✅ Complete

Goal: Convert structured LLM output into a consistent Markdown template.

Refactored into a layered, provider-agnostic architecture:
`llm.py` (communication) → `validator.py` (JSON validation) →
`markdown_generator.py` (presentation) → `main.py` (orchestration).

---

## v0.5.0 — Local Storage ✅ Complete

Goal: Save notes locally with safe filenames, and confirm success/failure
back to the user on Telegram.

Tested: successful save, filename collision handling, simulated failure
path (no crash), and real end-to-end Telegram flow (Arabic + English).

---

## v0.6.0 — Knowledge OS Interface ✅ Stabilized (may receive minor fixes on Day 4)

Goal: Provide a visual, read-only interface for exploring saved notes,
in addition to the Telegram bot (per supervisor's request for a UI
beyond chat).

Delivered:

- Streamlit app (`app.py`) reading real notes from the local vault.
- Interactive 3D visual exploration (`brain_graph.html`, `brain.js`,
  `styles.css`) with a search/browse sidebar and a Markdown reading view.
- Visual grouping ("lobes") is a cosmetic/deterministic categorization
  based on tags — not semantic AI classification.
- Links/relationships between notes are intentionally empty
  (`"links": []`) — visual scaffolding only, no semantic linking
  implemented in this version.

Explicitly NOT included (confirmed in code and honored):

- No automatic semantic linking.
- No AI-generated relationships.
- No embeddings or vector databases.
- No note editing, no multi-user support.

Note: the interface does not auto-refresh when a new note is saved via
Telegram; the browser must be manually refreshed. This is a known,
accepted limitation for the MVP.

---

## v1.0.0 — MVP Release

Goal: Complete, tested, end-to-end MVP.

Workflow

Telegram → Gemma → Thought Refinement → Markdown → Save to Vault →
Telegram Confirmation → Browsable via Knowledge OS Interface

Success Criteria: The complete workflow functions end-to-end, notes are
never lost or silently failed, and all saved notes are visually
browsable and readable through the interface.

---

# Current Task — Day 4: Debugging

Per the supervisor's Day 4 task: intentionally introduce 3 realistic bugs,
diagnose and fix them with AI assistance, and document each as
Symptom → Diagnosis → Fix. This is bug-fixing work on the existing
v0.1.0–v0.6.0 codebase — it does not introduce new features or change
the JSON schema, the architecture, or any file's core responsibility.

---

# Future Vision (Post-MVP — Not Part of This Week's Deliverable)

These ideas were explored during development but intentionally deferred
beyond the one-week MVP to protect scope and delivery stability. They
remain valuable directions for future iterations of the project.

## Context Window / Lightweight Memory

Allow related follow-up messages to build on a recent thought instead of
being treated as fully independent (currently: strictly single-turn, per
SPECIFICATION.md). Deferred because it is a genuine architectural
challenge (relevance selection, token budget, ambiguity handling) that
risks destabilizing a working MVP under time pressure.

## v0.7.0 (Future) — Cognitive Representation Engine

A more refined thought-refinement layer: improved system prompt design,
richer classification of thought types (Concept, Task, Question,
Observation, Insight, Research Idea), and a deterministic "Brain Mapping"
layer to replace tag-based cosmetic grouping with something more
intentional. This is a logic/prompt-quality upgrade, not a new
capability — a strong candidate for a v2 iteration once the MVP is
stable and reviewed.

## v0.8.0 (Future) — Knowledge Connections

Semantic relationships between notes, AI-generated related-note
suggestions, and interactive connections inside the visual interface.
Explicitly excluded from the MVP (see SPECIFICATION.md: no embeddings,
no vector databases, no automatic note linking).

## Other deferred ideas

- Hosting the Streamlit interface as a public web app.
- Live-refresh of the interface when new notes are saved.
- Structured logging/observability — considered, deliberately dropped
  for the MVP to avoid adding complexity without a clear immediate need.

Note: Docker/containerized packaging is a deployment option, not a
feature, and is not part of this list — it can be applied to the
existing app once stable, whenever convenient.