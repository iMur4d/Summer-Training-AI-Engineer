---
name: session-documentation
description: Generates structured development session logs following the CollaInsight
  repository's documentation conventions. Use this skill to document work
  completed during a development session, capturing decisions, progress,
  challenges, and outcomes in a consistent project-specific format.
---

# Session Documentation

This skill creates and maintains structured development session logs for the
CollaInsight project. It follows the repository's established documentation
conventions to produce consistent, factual records of work completed during a
development session, including implementation progress, technical decisions,
challenges, open items, and files modified.

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

## Log Structure

### <summary>

Provide a concise overview of the session highlighting the most important outcomes.

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
### Step 1: Read `CollaInsight/docs/ai-agent-code-work/README.md` before doing anything else.
  This document is the canonical source for the project's session documentation conventions, including folder structure, file naming, update rules, and writing standards.

### Step 2: Read the most recent file in CollaInsight/docs/ai-agent-code-work/claude/
   to match its exact format and tone: <summary>, one <part_N> block per
   distinct piece of work, <open_items>, <files_touched_this_session>.

### Step 3: Determine today's date. Check whether
   CollaInsight/docs/ai-agent-code-work/claude/<today>-session-log.md already
   exists (this skill may be invoked more than once in the same session/day).
   - If it exists, extend it: add new <part_N> blocks for new work, update
     <summary> and <open_items> to reflect the current end state. Do not
     duplicate a second same-day file.
   - If it doesn't exist, create it.
   - Determine today's date using the `YYYY-MM-DD` format. Check whether: CollaInsight/docs/ai-agent-code work/claude/YYYY-MM-DD-session-log.md already exists.

## Writing Guidelines
Follow these steps whenever this skill is invoked:

- Review the actual conversation to date and write only what really happened:
   - What changed, with real file paths — never vague language like "improved consistency" or "cleaned up code."
   - What was explicitly decided, rejected, or deferred, and why, if that reasoning isn't already recoverable by reading the code or docs themselves. (This folder documents decisions and reasoning that aren't visible from the code — not a change log the code already tells you.)
   - What's still open — genuine gaps the user already knows about, not speculative future work.
   - List every file touched this session (or since the last update to today's entry) at the end, under <files_touched_this_session>.

- Leave out anything that isn't CollaInsight project work — meta conversation about Claude Code itself, unrelated tangents, etc. This log is a record of work done on CollaInsight, not a transcript.

- If nothing substantive has happened yet in the session, say so rather than padding the entry with filler.

- Only write the file. Do not git add or git commit it — leave that for the user to review and commit themselves.


## Success Criteria

A successful session log should:

- Follow the repository's documentation conventions.
- Accurately reflect the work completed during the session.
- Record implementation details and engineering decisions when relevant.
- Preserve continuity with previous session logs.
- Contain only factual, project-related information.