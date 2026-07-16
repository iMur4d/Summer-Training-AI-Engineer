# Development Plan

This document outlines the roadmap of the Obsidian Brain MVP from inception to its stable v1.0.0 release, followed by the future vision for post-MVP enhancements.

## Completed Roadmap (MVP Phase)

### v0.1.0 — Telegram Communication
- Set up a basic Python Telegram Bot.
- Echo user messages to confirm connectivity.
- *Status: Completed*

### v0.2.0 — LLM Integration
- Connect the bot to the Google Gemini API (or Gemma).
- Send user messages to the model and return the raw generated response to the user.
- *Status: Completed*

### v0.3.0 — Thought Refinement
- Implement a system prompt that forces the LLM to act as a thought organizer instead of a conversational chatbot.
- Structure output into JSON format (Title, Summary, Key Points, Tags).
- Handle non-thought inputs (greetings, meaningless queries) gracefully.
- *Status: Completed*

### v0.4.0 — Markdown Generation
- Validate the JSON output received from the LLM.
- Convert the validated JSON into structured Markdown.
- Add YAML frontmatter for compatibility with Obsidian.
- *Status: Completed*

### v0.5.0 — Local Storage
- Automatically save the generated Markdown files to a local `vault/` directory.
- Generate safe, collision-resistant filenames.
- Reply to the Telegram user with a success confirmation.
- *Status: Completed*

### v0.6.0 — Knowledge OS Interface
- Build a Streamlit dashboard to interact with the local vault.
- Implement a 3D visualization using Three.js to render notes in a space.
- Add a sidebar for easy navigation and searching.
- Integrate a markdown reader to view the full text of any saved note.
- *Status: Completed*

### v1.0.0 — MVP Release (Completed)
- **Review-before-save Telegram workflow:** Bot sends a structured preview before saving.
- **Save / Discard confirmation:** Inline buttons added to the Telegram interface.
- **Strict thought classification:** System prompt restricted to 6 strict categories.
- **Improved Thought Refinement system prompt:** Focuses on extracting the abstract knowledge model rather than summarizing text.
- **Validator synchronization:** Python backend strictly enforces the 6 allowed `thought_types`.
- **Data-driven visualization using thought_type:** Frontend colors nodes strictly by their real data type.
- **Removal of fake neuroscience mappings:** Stripped arbitrary biological lobe assignments from the graph.
- **Improved frontend UX and visualization polish:** Added hover-highlighting for related types, recency-based node sizing, and custom UI scrollbars.
- **Production-ready repository cleanup:** Final modular architecture established, unused code removed, and documentation aligned.
- *Status: Completed*

---

## Future Vision (Post v1.0.0)

These features represent the next generation of the application. They are intentionally excluded from the MVP to keep the initial architecture simple and stable.

### AI & Knowledge Graph Enhancements
- **Semantic Linking:** Automatically identify connections between different notes.
- **Embeddings & Vector Database:** Store notes as vectors to enable semantic search and Retrieval-Augmented Generation (RAG).
- **Automatic Note Relationships:** Programmatically generate the "links" array in the graph data to draw edges between related nodes.
- **Contextual Memory:** Allow the LLM to read previous notes when refining a new thought.

### Workflow & Infrastructure Enhancements
- **Editing Notes:** Allow users to edit or append to existing notes via the Telegram bot or frontend UI.
- **Cloud Deployment:** Package the backend into Docker containers for remote hosting.
- **Live Synchronization:** Seamlessly sync the local vault with remote storage (e.g., Google Drive, AWS S3) or the native Obsidian Sync service.