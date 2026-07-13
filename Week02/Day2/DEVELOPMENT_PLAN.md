# Development Plan

# Version Roadmap

The application must be developed incrementally.

Each version must be fully functional before moving to the next one.

Never skip versions.

Do not implement features from future versions.

---

## v0.1.0 — Telegram Communication

Goal

A working Telegram bot.

Features

- Receive text messages.
- Print the received message.
- Reply with a simple confirmation.

Success Criteria

The bot successfully receives and replies to messages.

---

## v0.2.0 — LLM Integration

Goal

Connect the Telegram bot to Gemini.

Features

- Send user text to Gemini.
- Receive the model response.
- Return the response to Telegram.

Success Criteria

The user receives an AI-generated reply.

---

## v0.3.0 — Thought Refinement

Goal

Transform raw thoughts into structured knowledge.

Features

Generate:

- Title
- Summary
- Key Points
- Tags
- Open Questions

Success Criteria

The response follows the required structure without hallucinating missing information.

---

## v0.4.0 — Markdown Generation

Goal

Generate a Markdown note.

Features

- Convert the structured response into Markdown.
- Use a consistent template.

Success Criteria

A valid .md file is generated.

---

## v0.5.0 — Local Storage

Goal

Save notes locally, and confirm success back to the user.

Features

- Create the vault directory if needed.
- Save Markdown notes using safe filenames.
- After the file is saved successfully, send a confirmation message back
  to the user on Telegram (e.g. "✅ Note saved: [Title]").
- If saving fails, send a clear failure message instead of staying silent.

Success Criteria

- Generated notes are stored successfully.
- The user always receives a Telegram reply indicating whether the note
  was saved or not — the workflow must never end in silence.

---

## v0.6.0 — Code Quality (Deferred)

**Do not implement this version during Day 2 (initial build).**

This version is intentionally scheduled to run only after the Day 3 manual
code review (see AGENTS.md and the Week 2 schedule). The code produced through
v0.5.0 should reach Day 3 in its "as-built" state — functional but unpolished —
so there is real, unrefactored code available to review, annotate, and improve
by hand as that day's task requires.

Only start v0.6.0 after Day 3's manual review is complete and approved.

Goal

Improve maintainability without changing functionality.

Features

- Refactor code based on issues identified during the Day 3 manual review.
- Improve naming.
- Add logging.
- Improve error handling.

Success Criteria

The project becomes easier to maintain without changing functionality, and
the refactor reflects the specific improvements found during the Day 3 review.

---

## v1.0.0 — MVP Release

Goal

Complete the MVP.

Workflow

Telegram

↓

Gemini

↓

Thought Refinement

↓

Markdown

↓

Save to Vault

↓

Confirmation sent back to Telegram

Success Criteria

The complete workflow functions end-to-end, and the user receives a clear
confirmation (success or failure) for every submitted note.