# Week 2 - Day 4

## Today's Topic
Debugging with AI

## Objective
Intentionally introduce bugs into the working application, then diagnose and fix them with AI assistance. Document each bug as a clear **Symptom → Diagnosis → Fix** entry.

## Starting Point
This folder is a snapshot of the project at the beginning of Day 4, following Day 2's initial build and Day 3's review and refactoring pass.

The following features (inherited from Days 2–3) are implemented and stabilized:

- **v0.1.0** — Telegram bot communication.
- **v0.2.0** — LLM integration (Gemini/Gemma).
- **v0.3.0** — Thought Refinement (extracting structured knowledge from raw thoughts; validating/rejecting non-thought messages).
- **v0.4.0** — Markdown generation via a layered, provider-agnostic architecture (`llm.py`, `validator.py`, `markdown_generator.py`, `main.py`).
- **v0.5.0** — Local storage in the Obsidian vault, featuring safe filenames and Telegram success/failure confirmation.
- **v0.6.0** — Knowledge OS Interface: An immersive Streamlit-based visual interface featuring a 3D Brain explorer, searchable sidebar navigation, and a Markdown reading workspace.

*(See `SPECIFICATION.md` and `DEVELOPMENT_PLAN.md` for full details.)*

## Project State
- The MVP is **functionally complete** through v0.6.0.
- Day 4 focuses entirely on **debugging and reliability**.
- **No architectural redesigns or new features** are in scope today. The existing workflow and architecture must remain stable.

## Planned Tasks
- [ ] Identify 3 realistic bugs to intentionally introduce.
- [ ] Introduce them one at a time.
- [ ] Observe and record the symptom of each.
- [ ] Diagnose the root cause with AI assistance.
- [ ] Fix each bug with minimal, targeted changes.
- [ ] Document each as **Symptom → Diagnosis → Fix**.

## Expected Outcome
A detailed bug log documenting 3 realistic bugs, their symptoms, root causes, and fixes. The application must remain fully functional at the end of the day.

## Notes
This folder will evolve throughout today's work. As a reminder for the AI Engineering training program, no new capabilities or architectural changes are permitted today. See `AGENTS.md` for the current status rules.