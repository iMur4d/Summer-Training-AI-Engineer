# Session Log — 2026-07-28 — Claude

<summary>

Four pieces of work, in order:

1. Reviewed and rejected the technical parts of a stakeholder-provided repository restructuring plan that had scaffolded speculative future folders; agreed on a minimal alternative in discussion, but did not execute it yet at that point.
2. Reviewed `old_project/` (a prior personal-productivity prototype, "Obsidian Brain") and extracted its AI-technique knowledge — prompt engineering, validation strategy, JSON schema shape, classification strategy, lessons learned — as concepts only. No code was ported.
3. Recorded a product pivot: the platform's real scope is summarizing whole Telegram discussions (ideas, suggestions, decisions, action items, questions, observations) for managers, not just collecting "student ideas." Updated wording in four docs to match; workflow and MVP boundaries unchanged.
4. Executed the actual minimal repository restructuring (`frontend/`, `backend/`, `automation/`, `supabase/`), committed it in two separate commits, then built and live-tested a Phase 1 local n8n Docker environment.

Backend business logic, Telegram, Gemini/LLM credentials, and Supabase are still **not** configured. Phase 1's only concrete infrastructure so far is a working, tested local n8n container. This log exists so a future session can pick up from here without re-deriving these decisions.

</summary>

---

<part_1>

## Part 1 — Rejected a speculative restructuring plan, extracted the sound parts

The user shared a plan (written in an agreeable, uncritical tone — "I completely agree with every point you made") proposing to scaffold `automation/{telegram,ideas,notifications}/`, `backend/{api,services,ai}/`, and `supabase/{migrations,seed,functions}/` all at once, rename `n8n/` to `automation/`, and move the frontend into `frontend/`.

### What was flagged as wrong
- Scaffolding folders for systems not yet being built (Supabase seed/functions, automation/notifications) directly contradicts `AI_AGENT_CONTEXT.md`'s own "do not build features outside MVP scope" rule and the project's Phase 1/2/3 sequencing (Phase 2/Supabase is explicitly blocked until Phase 1 passes).
- `n8n` is a **locked** tech-stack choice per `docs/engineering/14_TECHNOLOGY_STACK.md`, not a placeholder to be abstracted away — "automation over n8n" solves a swap-tools problem the project doesn't have.
- Git doesn't track empty directories — the plan's empty scaffold folders would silently vanish on commit without a placeholder file, which its own verification step wouldn't have caught.
- `pnpm-workspace.yaml` (root, pre-existing) pointing `packages: - '.'` would break once frontend moved, and was flagged as likely dead config even before confirming it (no `pnpm-lock.yaml` ever existed, only `package-lock.json`).

### What was kept
- Moving the frontend into `frontend/` via `git mv` (preserves history) was sound and later executed.
- Later, when the user asked for backend + n8n folder structure for *real, imminent* work (not speculative), the same objection did not apply — see Part 4.

No files were changed in this part; it was plan review only.

</part_1>

---

<part_2>

## Part 2 — `old_project/` reviewed as a reference implementation, not migrated

`CollaInsight/old_project/` is a prior working prototype ("Obsidian Brain"): `Telegram → Gemini → validated JSON → Markdown → local Obsidian vault`, built for one person to organize their own notes. The user was explicit: extract concepts only, do not port code, do not assume workflow/UX carries over.

### Extracted (concepts, not code — see files for the originals)
- **Prompt engineering**: negative persona framing ("you are not a chatbot"), a single prompt handling both input-validation and generation via an output-mode switch (invalid → plain text, valid → JSON only), a hidden "think silently" pre-generation step, an embedded self-verification checklist, few-shot classification examples in addition to category definitions.
- **Validation strategy**: escalating checks (valid JSON? → dict? → required fields + types? → list items individually type-checked? → enum allowlist re-checked in code, never trusting the model's self-report); JSON-parse failure treated as an expected "refusal" path, not an error; tri-state return (`is_valid, data, message`) instead of raising.
- **JSON schema shape**: `title, thought_type (enum), summary, key_points[], tags[], open_questions[]` — covers only the AI-authored content fields; status/ownership/project/audit fields belong to whatever persists the record, not the LLM.
- **Classification strategy**: closed fixed category set (proven necessary by an actual bug, not just theory), deterministic fallback category, single model call handling both classification and full generation (simpler than the multi-stage pipeline `06_AI_PIPELINE.md` describes — worth testing whether that's sufficient before building the full staged pipeline).
- **Lessons learned** (from `old_project/docs/BUG_LOG.md` and `old_project/project_context/DECISIONS.md`):
  - A strict validator alone isn't sufficient — the prompt must independently forbid the same things the validator rejects, or the model invents plausible-but-invalid values (this happened: the model produced `"Project Idea"` when the prompt only *listed* six categories without forbidding others).
  - Never let unsanitized AI output hit an external renderer un-escaped (a real bug: Telegram's Markdown parser choked on special characters in LLM output).
  - The old prototype's Telegram-side "review before save" (Save/Discard buttons) should **not** be ported as-is — per the Part 3 pivot, the equivalent safeguard belongs on the **manager's** dashboard (review/reject/edit after storage), not a submitter-side gate, since the submitter is no longer the primary user.
  - "Markdown over Database" (the old prototype's storage choice) explicitly does **not** carry forward — it was right for a single-user local tool, wrong for CollaInsight's multi-user, dashboard-reviewed, Supabase-backed design.

This was saved to persistent memory (outside the repo, in the assistant's own memory system) as well as here, since it's the kind of reasoning a fresh session would otherwise have to re-derive by reading `old_project/` from scratch.

No files in the repo were changed in this part.

</part_2>

---

<part_3>

## Part 3 — Product pivot: discussion summarization, not just idea collection

The user relayed a real stakeholder-meeting outcome: the platform's actual value is helping managers understand a whole Telegram discussion — ideas, suggestions, decisions, action items, questions requiring attention, important observations, plus an overall summary — not just collecting "student ideas" as a standalone category. Explicitly **not** an MVP scope change: same workflow (`Telegram → AI → structured data → Dashboard → manager review`), same exclusions (no Knowledge Graph, no recommendations, no semantic search).

### Checked before editing
Most docs (`01_PRODUCT_VISION.md`, `02_PROBLEM_STATEMENT.md`, `03_TARGET_USERS.md`, `11_BUSINESS_RULES.md`, `05_WORKFLOWS.md`, `06_AI_PIPELINE.md`, `07_DATABASE_SCHEMA.md`, `README.md`'s product description) **already** used the broader framing (ideas/questions/tasks/observations/insights as a list, never "student ideas" as the sole purpose) — these were deliberately left untouched.

### Changed (wording only, narrowed-to-"student ideas" framing corrected)
- `AI_AGENT_CONTEXT.md` — MVP Problem/Solution statements and the "CRITICAL RULE" litmus test broadened from "review a student's idea" to "understand and review a discussion."
- `docs/00_MVP_SCOPE.md` — `<problem>`, `<primary_goal>`, `<core_workflow>` step 3, and the `AI Idea Structuring` feature bullet (renamed to `AI Discussion Structuring (Ideas, Decisions, Action Items, Questions)`).
- `PROJECT_STATUS.md` — one changelog line describing the MVP scope.
- `docs/engineering/09_FRONTEND_SPEC.md` — Dashboard module description, "idea-review view" → "discussion-review view."

</part_3>

---

<part_4>

## Part 4 — Repository restructuring executed, then a Phase 1 local n8n environment built and tested

### Restructuring (this time for real, minimally scoped)

User's constraints: minimal, no speculative folders, every created folder either used immediately or required by the *next* phase.

- `git mv` moved all frontend/Vite files (`index.html`, `package.json`, `package-lock.json`, `vite.config.ts`, `tsconfig.json`, `postcss.config.mjs`, `default_shadcn_theme.css`, `src/`, `public/`) into `frontend/`. Verified with `npm install && npm run build` inside `frontend/` afterward — builds clean.
- Deleted `pnpm-workspace.yaml` — confirmed dead (no `pnpm-lock.yaml` ever existed; `README.md` already documented `npm install`).
- Created `backend/api/__init__.py`, `backend/ai/__init__.py` (empty, Python package markers — also the placeholder that makes the otherwise-empty folder survive a git commit).
- Created `automation/workflows/README.md` and `supabase/migrations/README.md` (one-line placeholders explaining each folder's purpose, chosen over bare `.gitkeep` per user preference).
- Updated `README.md`'s frontend run instructions to `cd frontend` first.
- **Not created**: `backend/services/`, `backend/repositories/`, `backend/domain/`, `automation/notifications/`, `automation/scheduled-jobs/`, `supabase/functions/`, `supabase/seed/` — none needed yet.

**Commit split**: initially landed as one commit that unexpectedly also swept in the Part 3 doc-wording changes and a `.gitignore` change adding `old_project/` (neither added intentionally — root cause not fully confirmed; no git hook or husky config was found configured). Per the user's request, re-split via `git reset --soft HEAD~1` (safe, nothing was pushed) into two commits:
- `2851807` — the restructuring (incl. the `.gitignore` addition, since it's structural).
- `88c3ca9` — the Part 3 doc-wording changes.

**Decision point surfaced and resolved**: the `.gitignore` addition means `old_project/` is now permanently untracked. Asked the user explicitly — decision: **keep it local-only**, do not commit it as shared reference material. No further action taken; this is the current, intended state.

### Phase 1 local n8n Docker environment

Scope explicitly limited by the user mid-task: n8n only. **Not** configured: Telegram, Gemini/LLM credentials, Supabase. Also explicitly told to stop and explain first if anything in the repo needed fixing before this (nothing did — checked for pre-existing docker/env files, found none; confirmed `.gitignore`'s existing generic `.env` patterns already cover a future `.env` without matching `.env.example`).

**Files created** (all at `CollaInsight/` root):
- `docker-compose.yml` — single `n8n` service, image `docker.n8n.io/n8nio/n8n:2.33.0` (pinned, not `:latest`), named volume `collainsight_n8n_data` mounted at `/home/node/.n8n`, `env_file: .env`, host port from `${N8N_HOST_PORT:-5678}`. Deliberately placed at repo root, not inside `automation/`, since it's cross-cutting infrastructure (will gain a `backend` service entry in a later phase) rather than automation-specific business-capability content.
- `.env.example` — `N8N_ENCRYPTION_KEY` (blank, generate via `openssl rand -hex 32`), `GENERIC_TIMEZONE`/`TZ` (default `UTC`), `N8N_HOST`/`N8N_HOST_PORT`/`N8N_PROTOCOL`/`N8N_SECURE_COOKIE`/`N8N_WEBHOOK_URL` (all `localhost`/`http`-appropriate for now), `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true`. No Telegram or LLM provider variables — those become n8n *credentials*, entered through its UI and encrypted at rest via `N8N_ENCRYPTION_KEY`, not container env vars.
- `README.md` — new "Running n8n Locally (Phase 1)" section.

**No `Dockerfile`** — consuming n8n's official image as-is; one would only be justified by a custom node or build step, which isn't a current need.

### Verified live, not just written

Actually ran the stack rather than handing over an untested checklist:
- Pulled `docker.n8n.io/n8nio/n8n:2.33.0`, started it, confirmed `http://localhost:5678` → `200` and `/healthz` → `{"status":"ok"}`.
- n8n's own boot log flagged two of the originally-chosen env vars as deprecated: `N8N_RUNNERS_ENABLED` ("remove this environment variable; it is no longer needed") and `WEBHOOK_URL` (→ `N8N_WEBHOOK_URL`). Both corrected in `.env.example` before handing it off — this was caught by testing, not anticipated in the initial design.
- Confirmed actual persistence, not just a restart: `docker exec` showed a real `database.sqlite` (1.5MB) in the volume; ran a full `docker compose down` (no `-v`) + `docker compose up -d` cycle; the volume survived (`docker volume ls` still showed `collainsight_n8n_data`) and no fresh-install log line reappeared, confirming n8n recognized its existing state rather than reinitializing.
- Noted and deliberately left alone: a log line about the internal Python task runner failing to start (Python 3 missing from the container) — expected, debug-only feature we don't need for Phase 1's JS-based validation; setting up an external Python task runner now would be scope creep.

A local `.env` (git-ignored) now exists in the working tree from this test run, with a real generated encryption key. It was not deleted after testing — the container is left running and usable.

</part_4>

---

<open_items>

## Open items / not yet done

- Telegram bot creation and n8n Telegram Trigger node — not started (explicitly deferred).
- LLM provider credential (Gemini/Claude/OpenAI) wiring in n8n — not started (explicitly deferred).
- The actual n8n workflow (Telegram → AI → structured JSON) — not built yet; this environment just makes building it possible.
- Whether the extracted `old_project` classification strategy (single model call, not the multi-stage pipeline in `06_AI_PIPELINE.md`) is sufficient should be tested empirically once workflow-building starts, per Part 2.
- A stray untracked file appeared at the outer repo root (one level above `CollaInsight/`, outside this project's scope) during this session: `implementation_plan_Local_n8n_Setup_Plan_(...).md`, apparently from a different tool ("Antigravity"). Not investigated or acted on — flagged here only so it isn't mistaken for something this session created.

</open_items>

---

<files_touched_this_session>

Documentation (Part 3):
- `AI_AGENT_CONTEXT.md`
- `docs/00_MVP_SCOPE.md`
- `PROJECT_STATUS.md`
- `docs/engineering/09_FRONTEND_SPEC.md`

Restructuring (Part 4):
- `git mv`: `index.html`, `package.json`, `package-lock.json`, `vite.config.ts`, `tsconfig.json`, `postcss.config.mjs`, `default_shadcn_theme.css`, `src/`, `public/` → all under `frontend/`
- Deleted: `pnpm-workspace.yaml`
- New: `backend/api/__init__.py`, `backend/ai/__init__.py`, `automation/workflows/README.md`, `supabase/migrations/README.md`
- `.gitignore` — gained an `old_project/` entry (see Part 4 for the unresolved "how" of this)
- `README.md` — frontend run instructions (`cd frontend`), plus new "Running n8n Locally (Phase 1)" section

Phase 1 n8n environment (Part 4):
- New: `docker-compose.yml`, `.env.example`
- Local only, not committed: `.env` (git-ignored, real encryption key generated during testing)

New (this entry):
- `docs/ai-agent-code-work/claude/2026-07-28-session-log.md` (this file)

Commits made this session: `2851807` (restructuring), `88c3ca9` (doc wording). Both are local, on `main`, 2 commits ahead of `origin/main` — **not pushed**.

</files_touched_this_session>
