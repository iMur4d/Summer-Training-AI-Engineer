# AI Agent Code Work

<objective>

This folder is a persistent record of work done on CollaInsight by AI coding agents (Claude, and any future agents), across separate sessions and context windows.

Chat context does not carry over between sessions. This folder does. If you are an agent picking up this project in a new conversation, read this before making changes — it tells you what was already decided, why, and what is still open.

</objective>

---

<structure>

Each agent gets its own subfolder, named after the agent (e.g. `claude/`). Inside that subfolder, each significant work session gets one dated log file:

```
docs/ai-agent-code-work/
  README.md              <- this file
  claude/
    2026-07-27-session-log.md
    <next-date>-session-log.md
    ...
```

Do not edit past log entries to reflect new decisions — append a new dated entry instead. Logs are a history, not a living spec. The living spec is the rest of `/docs` (starting with `docs/00_MVP_SCOPE.md`).

</structure>

---

<how_to_use_this>

## If you are an AI agent starting a new session

1. Read `docs/AI_AGENT_CONTEXT.md` first (project rules, tech stack, current phase).
2. Read the most recent log file(s) in `claude/` (or your own agent's subfolder) to catch up on decisions made in prior sessions that may not yet be reflected elsewhere.
3. Check the "Open Items" section of the latest log before starting new work — those are known gaps the user already knows about.

## If you are the user

Each log entry should let you (or a fresh agent) answer: what changed, why, what was explicitly rejected or deferred, and what's still outstanding. If a log entry doesn't answer those questions, it's incomplete.

</how_to_use_this>

---

<constraints>

- This folder documents decisions and reasoning, not code itself — the code and `/docs` specs remain the source of truth for current state.
- Keep entries factual and specific (file paths, what changed, why). Avoid vague summaries like "improved consistency."
- If a session reverses or supersedes an earlier decision, say so explicitly and reference the earlier log entry rather than silently contradicting it.

</constraints>
