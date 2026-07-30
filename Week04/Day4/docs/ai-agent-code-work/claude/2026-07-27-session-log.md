# Session Log — 2026-07-27 — Claude

<summary>

Two pieces of work in this session:

1. A documentation consistency pass, making the whole `/docs` tree agree with `docs/00_MVP_SCOPE.md` as source of truth.
2. A frontend architecture decision: the existing React app (which already implements post-MVP modules like Knowledge Graph and Collaboration Hub) is being treated as an intentional long-term prototype, not scope creep to delete. Non-MVP modules were hidden from navigation via a feature flag, not removed.

No backend, Supabase, or n8n work has started yet. This log exists so that a future session (with no memory of this conversation) can pick up from here without re-deriving these decisions.

</summary>

---

<part_1>

## Part 1 — Documentation Consistency Pass

### Starting point

The user asked for an evaluation of `docs/00_MVP_SCOPE.md`, which surfaced several gaps and one contradiction between docs. The user then asked to resolve them, with `docs/00_MVP_SCOPE.md` as the fixed source of truth — other docs get edited to match it, not the other way around.

### Changes made

**1. Renamed `docs/enginnering/` → `docs/engineering/`**

The directory was misspelled ("enginnering") on disk since the initial commit. Every reference to it — in `README.md`, `AI_AGENT_CONTEXT.md`, and `PROJECT_STATUS.md` — already used the correct spelling "engineering." Any agent following those references would have hit a missing-file error. Renaming the directory fixed all three references at once; no doc text needed to change.

**2. Defined an Idea Status enum**
- `docs/engineering/07_DATABASE_SCHEMA.md` — added a `Status (MVP)` block to the `KnowledgeItem` entity: `Pending, Under Review, Approved, Rejected, Archived, Duplicate`. Noted that this is a manual manager-set status, distinct from the `KnowledgeRelationship` entity's own (future, automatic) "Duplicate" relationship type — those are two different mechanisms with the same name, which was worth disambiguating explicitly.
- `docs/engineering/10_API_SPEC.md` — added an "Update Knowledge Status" responsibility under the Knowledge domain, referencing the schema doc rather than re-listing the enum (avoids drift).

**3. Clarified duplicate handling is manual for the MVP**
- `docs/00_MVP_SCOPE.md` — the success metric "Reduce duplicate submissions" now explicitly says this happens via manually marking an idea Duplicate, not automatic AI detection.
- `docs/engineering/05_WORKFLOWS.md` — added a new "Idea Status Update" workflow (matching the existing workflow block format) describing the manager-driven status change, including the manual Duplicate marking.
- `docs/engineering/06_AI_PIPELINE.md` was **not** touched — it already correctly lists "Duplicate Detection" under `future_capabilities`, i.e. already excluded from MVP. That was the correct existing state; the actual gap was that nothing said how duplicates get handled *instead*.

**4. Added an MVP-scope banner to the Frontend Spec**
- `docs/engineering/09_FRONTEND_SPEC.md` — added an `<mvp_scope_note>` block near the top stating this document describes the long-term vision, naming the MVP subset (Dashboard, Executive Dashboard as a simplified view without AI widgets, Knowledge & Projects Explorer, Settings & Identity), and explicitly listing Knowledge Graph / Collaboration Hub / Executive Dashboard's AI-generated widgets / Advanced Analytics as out of MVP scope. Nothing was removed from the document — per instruction, the full long-term spec stays intact.

**5. Aligned the Roadmap with the MVP**
- `docs/engineering/16_ROADMAP.md` — Phase 2 ("Core Platform Implementation," the phase the project is entering) listed "Build the collaboration hub" as an immediate goal, and the "Immediate Features" list included "Collaboration suggestions." Both directly contradicted the MVP's exclusion of Collaboration Matching/Recommendation Engine. Removed the Phase 2 line; moved the feature bullet to "Next Features" (where Knowledge Graph already correctly sat). Added a one-line note pointing to `00_MVP_SCOPE.md` as authoritative whenever a roadmap phase runs ahead of it.

### Verified, not just asserted

Re-read all six edited files end-to-end afterward to confirm the edits read naturally in context and didn't introduce new inconsistencies (e.g. confirmed the Frontend Spec banner correctly keeps "Executive Review Dashboard" in the MVP subset, since `00_MVP_SCOPE.md` does include it — only its AI-generated widgets are excluded).

</part_1>

---

<part_2>

## Part 2 — Frontend Architecture Decision: Prototype, Not Scope Creep

### The decision (user's, recorded here for continuity)

The existing React frontend already has fully-implemented pages for post-MVP modules: `GraphView.tsx` (197 lines), `CollaborationView.tsx` (71 lines), `InsightsView.tsx` (142 lines) — all real, wired into `App.tsx`'s routing, not stubs. This was flagged earlier in the session as a potential doc/code mismatch.

**The user's explicit call: this is not a mistake.** The frontend was intentionally built as a prototype representing the long-term product vision. Instructions given:
- Do not delete any existing pages or components.
- Do not remove routes unless absolutely necessary.
- Hide unfinished/non-MVP modules from the normal navigation flow instead (mark as "Coming Soon" or hide from sidebar), while keeping the code intact.
- Organize so future modules can be enabled later without restructuring — think feature flags, not deletion.
- Preserve the existing design language, premium UI, and responsiveness.

This is a durable project decision — do not propose deleting `GraphView`, `CollaborationView`, or `InsightsView` in future sessions. If MVP-vs-vision tension comes up again, the answer is: hide via the flag, don't delete.

### Page classification (as of this session)

**MVP (kept active in nav):**
- `DashboardView` — kept, but see Open Items below re: mock content bleed.
- `KnowledgeView` — de facto "Idea Review" screen (search, type filters, status badges). Best-positioned MVP page as-is.
- `ProjectsView` — matches "Basic Project Assignment." Fine as-is.

**Not MVP (hidden from nav, code untouched):**
- `GraphView` — Knowledge Graph, explicitly excluded by `00_MVP_SCOPE.md`.
- `CollaborationView` — Collaboration Matching / Recommendation Engine, explicitly excluded.
- `InsightsView` — this is Advanced Analytics (Trending Topics, Recurring Challenges, Emerging Ideas), explicitly excluded. Note: it is *not* the same thing as the MVP's "Executive Review Dashboard," which is a much lighter feature that doesn't have a dedicated page yet (see Open Items).

**Gaps found (not a hide/show issue — these don't exist at all):**
- No Settings page. The sidebar's "Settings" nav button has no `onClick` handler today.
- No Authentication/Login screen. `LandingPage`'s "Enter" button jumps straight to the dashboard, bypassing auth entirely.

### Implementation

**`src/shared.tsx`** — `NAV_ITEMS` entries now carry an `mvp: true | false` flag:
```ts
export const NAV_ITEMS = [
  { id: "dashboard" as View, icon: LayoutDashboard, label: "Dashboard", mvp: true },
  { id: "knowledge" as View, icon: BookOpen, label: "Knowledge", mvp: true },
  { id: "projects" as View, icon: FolderKanban, label: "Projects", mvp: true },
  { id: "collaboration" as View, icon: Users, label: "Collaboration", mvp: false },
  { id: "insights" as View, icon: Sparkles, label: "AI Insights", mvp: false },
  { id: "graph" as View, icon: Network, label: "Knowledge Graph", mvp: false },
];
```
To re-enable a module later: flip its `mvp` flag to `true`. No other code changes are required — `App.tsx`'s `viewMap` already renders all six views unconditionally; only the sidebar reads the flag.

**`src/components/AppShell.tsx`** — the sidebar nav render was split into two blocks:
1. `NAV_ITEMS.filter(item => item.mvp)` — rendered exactly as before (interactive, active-state highlighting).
2. A "Coming Soon" section divider (same style as the existing "Workspace" divider), shown only if any non-MVP items exist.
3. `NAV_ITEMS.filter(item => !item.mvp)` — rendered as non-interactive `<div>`s (not `<button>`s): 50% opacity, `cursor-not-allowed`, a small "Soon" pill badge, no `onClick`. Still visible (so the product vision stays on display for stakeholders), but unreachable through normal navigation.

Verified with `npm run build` (vite 6.4.3) — compiles clean, 3041 modules transformed, no errors. (Note: `npx tsc --noEmit` throws a pre-existing, unrelated error — `tsconfig.json` uses a `baseUrl` option that TypeScript 7.0.2 removed. This predates this session's changes and did not block the actual Vite build; it's a separate config fix if the team wants strict `tsc` checking to work.)

### Open items / recommendations flagged to the user (not yet acted on)

- **Settings page and Auth screen need to be built** — genuine gaps, not nav visibility issues.
- **`DashboardView` has Collaboration-flavored mock content**: a "Collaborations: 23, +5 suggested" stat tile and an "AI Suggestions" card that suggests pairing two specific people. Both are Collaboration-Hub content sitting inside an in-scope MVP page. Deliberately not edited yet — it's all mock data that will be replaced once Supabase wiring happens anyway, so editing it now would be wasted effort. Whoever does that wiring should drop these two elements rather than port them forward.
- **`KnowledgeView`'s status badges currently say "Published"/"Draft"** — need to become the six-value enum (`Pending / Under Review / Approved / Rejected / Archived / Duplicate`) defined in `docs/engineering/07_DATABASE_SCHEMA.md` once real data is wired in.

</part_2>

---

<files_touched_this_session>

Documentation:
- `docs/enginnering/` renamed to `docs/engineering/` (11 files moved, no content changes)
- `docs/engineering/07_DATABASE_SCHEMA.md`
- `docs/engineering/10_API_SPEC.md`
- `docs/engineering/05_WORKFLOWS.md`
- `docs/00_MVP_SCOPE.md`
- `docs/engineering/09_FRONTEND_SPEC.md`
- `docs/engineering/16_ROADMAP.md`

Frontend code:
- `src/shared.tsx`
- `src/components/AppShell.tsx`

New (this entry):
- `docs/ai-agent-code-work/README.md`
- `docs/ai-agent-code-work/claude/2026-07-27-session-log.md` (this file)

Nothing has been committed to git as of the end of this session — all changes are sitting in the working tree, unstaged.

</files_touched_this_session>
