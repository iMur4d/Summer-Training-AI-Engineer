# Changelog

## [v1.0.0] - MVP Finalization
### Added
- **Review-Before-Save Telegram Workflow:** Added an inline button interface in Telegram. Users now receive a preview of their parsed thought and must click [Save] or [Discard].
- **Strict Thought Classification:** Implemented a rigorous 6-category system (`Concept, Task, Question, Observation, Insight, Research Idea`) enforced natively by both the LLM and the Python validation layer.
- **Data-Driven Visualization:** Nodes in the 3D graph are now colored strictly by their `thought_type`.
- **Recency Scaling:** Newer notes visually appear larger and pulse more intensely in the 3D graph, shrinking gradually as they age up to 30 days.
- **Hover Highlights:** Hovering over a note in the frontend now keeps all other notes of the same `thought_type` illuminated while fading unrelated notes into the background.

### Changed
- **Thought Refinement Engine:** The LLM prompt was upgraded from a simple summarizer to an abstract knowledge extractor.
- **Visualization Math:** Reverted the brain layout math to function solely as an immersive aesthetic container, removing all fake biological "lobe" mappings.
- **Frontend Polish:** Replaced default browser scrollbars with custom dark-themed glass scrollbars. Adjusted sidebar spacing and button hover animations.
- **Documentation:** Restructured the repository roadmap to reflect v1.0.0 as the finalized MVP version.

### Removed
- **Language Switcher:** Removed the broken Streamlit language switcher UI entirely to fix responsive layout overlapping issues. The app cleanly defaults to English navigation text.
- **Fake Neuroscience:** Stripped all pseudo-scientific mappings from the HTML legend and Python logic.

---

## [v0.6.0]
### Added
- Streamlit web interface (`frontend/app.py`).
- Interactive 3D Brain visualization using Three.js (`brain.js`, `brain_graph.html`).
- Vault explorer sidebar for reading generated Markdown notes directly in the browser.

---

## [v0.5.0]
### Added
- Local storage module (`backend/storage.py`).
- Collision-resistant file slug generation (supporting Arabic and English).
- Telegram confirmation message indicating successful disk save.

---

## [v0.4.0]
### Added
- Python validation layer (`backend/validator.py`) to parse LLM JSON responses.
- Markdown generator (`backend/markdown_generator.py`) to format valid JSON into Obsidian-compatible notes with YAML frontmatter.

---

## [v0.3.0]
### Added
- System prompt for Gemini (`backend/system_prompt.txt`).
- Structured JSON output requirements (Title, Summary, Key Points, Tags, Open Questions).
- Graceful error handling for non-thought conversational messages.

---

## [v0.2.0]
### Added
- Asynchronous LLM integration module (`backend/llm.py`).
- Google Gemini API connectivity.

---

## [v0.1.0]
### Added
- Basic Telegram Bot setup using `python-telegram-bot`.
- `main.py` entry point.
- `.env` configuration loading.
