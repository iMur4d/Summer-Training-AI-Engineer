---
name: session-documentation
description:
  Generates structured development session logs following the documentation conventions defined by the target repository.
  Use this skill to document work
  completed during a development session, capturing decisions, progress,
  challenges, and outcomes in a consistent project-specific format.
---

# Session Documentation

This skill creates and maintains structured development session logs for any software project. It produces consistent, factual records of completed work, implementation decisions, unresolved items, and modified files, enabling future development sessions to resume from documented project history rather than previous chat conversations.

Rather than generating a generic summary, this skill documents the development
process in a format that aligns with the project's existing session log
conventions, ensuring continuity across multiple sessions and preserving the
reasoning behind important engineering decisions.

## When to Use This Skill

Use this skill when:

- A development session has ended.
- A long session needs an intermediate log.
- An existing session log should be updated.
- Project work needs to be documented following repository conventions.

## Mutability Rules

<summary>, <open_items>, and <files_touched_this_session> are cumulative sections and should be updated in place.

<session_update> blocks are immutable history and must only be appended.

## Log Structure

### <summary>

Limit the summary to a high-level overview only.
Avoid repeating implementation details already described inside <session_update> blocks.
The summary should help a reader decide whether the full log needs to be read.

### <session_update>

Represents a single invocation of this skill.

Each update must contain:

- start timestamp and end timestamp
  - Use the actual local time available to the AI runtime.
    If the runtime cannot determine the current time reliably, explicitly state that the timestamp is unavailable rather than estimating it.
- one or more <part_N> blocks produced during that invocation
  - Part numbering restarts from <part_1> inside every new <session_update>.

Append new <session_update> blocks chronologically. Never merge separate invocations into an existing block.

### <part_N>

Each part represents one distinct unit of work completed during the session.
Include:

- objective
- implementation
- decisions
- rationale (when needed)

### <open_items>

List confirmed unresolved work remaining after this session.

### <files_touched_this_session>

List every file modified since the last update.

## Workflow

### Step 1:

Read the project's session documentation guide (if available) before doing anything else. This document is the canonical source for the repository's folder structure, file naming, update rules, and writing standards, and takes precedence over the defaults in this skill.

### Step 2:

If a previous session log exists, read the most recent one to understand its structure and writing style.

When updating an existing log, first locate the latest <session_update>. Only traverse earlier <session_update> blocks if additional historical context is required.

Match the existing format, section ordering, and writing style (<summary>, <session_update>, <part_N>, <open_items>, and <files_touched_this_session>).

If neither a documentation guide nor a prior log exists, this is the first session log for this project — follow the Log Structure section below directly. See `references/example-session-log.md` in this skill for a fully worked example.

### Step 3:

Determine today's date in `YYYY-MM-DD` format.

Use the session log location defined by the project's documentation guide.
If no convention exists, default to:

`docs/ai-agent-code-work/<agent-name>/YYYY-MM-DD-session-log.md`

`<agent-name>` is the name of the agent invoking this skill (e.g. `claude`) — substitute the literal name, do not keep the placeholder.

Check whether today's session log already exists.

- **If it exists:**
  - Append a new `<session_update>` block.
  - Record the actual start and end timestamps.
  - Place all new `<part_N>` blocks inside that `<session_update>`.
  - Update `<summary>` and `<open_items>` to reflect the cumulative state of the current day's log.
  - Do not modify previous `<session_update>` blocks.

- **If it does not exist:**
  - Create a new daily session log.
  - Wrap the first entry inside a single `<session_update>` block.

## Writing Guidelines

Follow these steps whenever this skill is invoked:

- If a new daily log is created, its first content must still be wrapped inside a single <session_update>.
- Review the actual conversation to date and write only what really happened:
  - What changed, with real file paths — never vague language like "improved consistency" or "cleaned up code."
  - What was explicitly decided, rejected, or deferred, and why, if that reasoning isn't already recoverable by reading the code or docs themselves. (This folder documents decisions and reasoning that aren't visible from the code — not a change log the code already tells you.)
  - What's still open — genuine gaps the user already knows about, not speculative future work.
  - List every file touched this session (or since the last update to today's entry) at the end, under <files_touched_this_session>.

- Leave out anything that isn't related to the target software project. Exclude meta conversation about the AI assistant itself, unrelated tangents, or non-project discussion. The session log is a record of project work, not a conversation transcript.

- If nothing substantive has happened yet in the session, say so rather than padding the entry with filler.

- Only write the file. Do not git add or git commit it — leave that for the user to review and commit themselves.

- Treat <session_update> blocks as retrieval checkpoints. When reviewing an existing session log, start from the most recent checkpoint and traverse backward only as needed instead of processing the entire file.

## Success Criteria

A successful session log should:

- Follow the repository's documentation conventions.
- Accurately reflect the work completed during the session.
- Record implementation details and engineering decisions when relevant.
- Preserve continuity with previous session logs.
- Contain only factual, project-related information.
