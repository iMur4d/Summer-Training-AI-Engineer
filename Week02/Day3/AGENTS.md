# Project Rules

- Read SPECIFICATION.md and DEVELOPMENT_PLAN.md before coding.
- Never implement features outside the current version.
- Never modify unrelated files.
- Keep the code modular.
- Explain every architectural decision.
- Prefer simplicity over cleverness.
- If requirements are ambiguous, ask first.

## Versioning Rules

Always develop the application incrementally.

Every implementation belongs to a specific version, as defined in
DEVELOPMENT_PLAN.md.

Before writing code:

- State the current version.
- Explain its goal.
- Explain what will be implemented.
- Explain what will NOT be implemented.

After finishing:

- Verify that the version works.
- Summarize the completed features.
- Wait for approval before starting the next version.

Never skip versions.

Never implement future-version features unless explicitly instructed.

### Special Rule — v0.6.0 (Code Quality)

Do not implement v0.6.0 under any circumstances until explicitly told that
the Day 3 manual code review is complete. This version exists to refactor
code based on issues found during that review — implementing it early
removes the real problems the review is meant to catch. If asked to build
"the next version" while v0.5.0 is the latest complete version, stop and
confirm the Day 3 review has happened before proceeding to v0.6.0.

## Repository Rules

Only inspect files directly related to the current implementation.

Avoid searching unrelated project history.

Avoid scanning the entire repository unless necessary.

Do not search the internet if the required information already exists in the project documentation.

Do not inspect .env values.

Assume all secrets will be provided by the user when needed.

Do not perform git fetch, pull, push, merge, reset, or branch creation unless explicitly requested.

## Architecture Evolution

Start with the simplest architecture that satisfies the current version.

As the project grows, refactor incrementally into a modular object-oriented design.

Do not introduce classes, abstractions, or design patterns until they provide a clear benefit.

When introducing a new module or class, explain why it is needed and how it improves the architecture.

## Single Responsibility Rule

Each module should have one clear responsibility.

If a file begins to handle multiple unrelated responsibilities, propose splitting it into separate modules before adding more code.

## Git Workflow

Git operations are my responsibility.

Never execute Git commands automatically.

Instead:

- Explain why a Git operation is appropriate.
- Suggest the exact Git command(s).
- Wait for me to execute them manually.
- Continue only after I confirm the Git step is complete.

Assume I am learning Git through this project.
Teach the purpose of each Git command briefly before suggesting it.
When a Git operation is appropriate, explain why it is needed before suggesting the command. Assume I am learning Git throughout this project, so briefly teach the purpose of each Git command instead of only listing it.