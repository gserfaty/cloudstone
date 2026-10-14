# Plan: Cloudstone workbench redesign

- **Track:** Standard
- **Entry stage:** Discover. There's no `JOURNEY.md` or `DESIGN.md`, so no stage is skipped.
- **Seed:** `.design-foundations/research/2026-10-13-cloudstone-workbench.md` (confirmed for planning)
- **Date:** 2026-10-13
- **Status:** complete
- **Completed:** 2026-10-13

## Context

**Problem:** Turn Cloudstone's single workbench screen into a calm, precise daily tool for SQL analysts. It needs its own visual identity and a results area that does real work: formatting by data type, sorting, per-column stats and keyboard navigation of cells. It also gains query history. The job is to help the user understand a dataset's shape and iterate on questions without leaving their flow.

**Success criteria:**
- Every text and UI color pair passes WCAG AA.
- The page uses tokens only, with no stray hard-coded colors.
- At least 15 result rows are visible at 1440×900.
- Results, column stats, chart and history all work from the keyboard.
- The design-review agent finds no Critical issues.
- It no longer reads as a generic template.

## Constraints

- **Light mode only**, with no dark theme or toggle (user decision). "Both ramps pass" items don't apply; only the light ramp is produced.
- **One file:** `index.html`, vanilla JS, no build step. External assets only from cdnjs and Google Fonts.
- **Backend unchanged:** the HTTP API in ARCHITECTURE.md stays as is, and query history lives in `localStorage`.
- **Snowsight is a structural reference only**, not a brand reference. Its navy bar and Snowflake blue are what the user called generic.
- **No regressions:** every current feature keeps working:
  - Ask, on or off.
  - Logged-out access to demo data, accounts and uploads.
  - Example queries, and the explorer with expandable columns.
  - Line-numbered editor.
  - CSV download.
  - Shortcuts `/` and ⌘↵.
  - Live regions, and phone width with no page-level sideways scroll.
- **Chart data color:** stays the validated series-1 blue `#2a78d6`. The UI accent must be clearly distinct from it.
- **Taste signals (dealer pins, verbatim from research):**
  - Light only. Locked.
  - Snowsight as the structural reference, but not its brand colors wholesale.
  - Calm over flashy. No gradients or decoration for its own sake.

## Chosen approach

1. Specify the one screen's journey and page spec first.
2. Lock a Cloudstone-specific DNA (dealt and critiqued, not defaulted).
3. Write the words and the data-surface specs in parallel.
4. Compose everything into the live `index.html`, judged by the review agent on real pixels.

**Execution order:**
1. Phases 1–2 run first.
2. The mock gate renders a styled mock of the Workbench from the Phase 2 DNA. The user's sign-off there is Phase 2's lock step (DW-2.7).
3. Build then runs Phases 3–5.

DAG: **1 → 2 → [mock gate: user locks DESIGN.md] → {3, 4} → 5**. Gates: `JOURNEY.md` page spec before any Design phase; `DESIGN.md` locked before phases 3–5.

---

### Phase 1: Journey and page spec
**Stage:** Discover
**Model:** sonnet
**Doctrine:** journey, usability
**Gate:** Standard

**Goal:** Specify the analyst's loop and the single workbench screen it runs on.

**Scope:**
- IN:
  - A JTBD job story.
  - A journey map: first visit → explore a table → iterate queries → return through history.
  - IA: top bar, sidebar with Explorer and History, Ask, worksheet, results card with the column panel.
  - Flows:
    - Preview a table.
    - Iterate a query.
    - Ask → refine.
    - Upload when logged out (redirected to sign-up).
    - Rerun from history.
  - One page spec covering every region and state.
- OUT: visual styling; marketing pages.

**Edge cases:**
- Ask off: the Ask region is hidden and a hint shows.
- Logged out: demo tables only, and the upload control routes to sign-up.
- Results capped at 1,000 rows: show a truncation notice and a note that sorting covers only the returned rows.
- Empty result and DDL statements that return no result set.
- Narrow width: the column panel stacks under the grid.

**Produces:** `JOURNEY.md` sections `## Job`, `## Journey`, `## IA`, `## Flows`, `## Page specs` (the Workbench page).
**Depends on:** research doc | **Unlocks:** Phase 2

**Done when:**
- [ ] DW-1.1: `JOURNEY.md` `## Page specs` has a complete Workbench entry: every region, its states (empty, loading, error, logged out, Ask off) and its keyboard behavior.
- [ ] DW-1.2: the flows cover all five journeys in IN, each ending in a visible outcome.
- [ ] DW-1.3: the regions and states in the page spec cite Hick's law and Cowan's ~4±1 limit where they cut options.

### Phase 2: Visual identity and tokens
**Stage:** Design
**Model:** opus (override: fable needs extra usage credits; user wants no charges beyond the subscription)
**Doctrine:** design-dna, archetypes, foundations, fonts, color, motion, ai-tells
**Gate:** Full

**Goal:** A Cloudstone-specific DNA within the calm and precise feel, turned into a light-only token block.

**Scope:**
- IN:
  - Register.
  - An archetype.
  - Two named references per candidate.
  - A composition dealt by the dealer, critiqued across all candidates, then converged.
  - The signature move.
  - A type pairing that reconsiders Inter, which `ai-tells` flags as the main font.
  - Accent and neutral ramps through `palette.mjs`.
  - Functional colors.
  - The space/shape/depth system.
  - A motion budget of 150 ms or less.
- OUT: dark ramps; component specs.

**Constraints:**
- The accent is the identity hue. It must be distinct from the series-1 data blue `#2a78d6`, at OKLCH hue difference ≥ 40° or chroma/lightness clearly apart.
- Accent coverage stays under 5% of the screen.

**Edge cases:**
- The dealer emits an AI-tell cell: re-deal, never hand-edit the dealt hand.
- A candidate accent fails AA as text: use its solid step for fills only.

**Produces:** `DESIGN.md` with its token block, which becomes **locked** when the user signs off on the styled mock that follows this phase.
**Depends on:** Phase 1 | **Unlocks:** Phases 3, 4, 5

**Done when:**
- [ ] DW-2.1: `DESIGN.md` exists with Direction, Signature move, Type, Color tokens, Space/shape/depth, Motion and Never sections.
- [ ] DW-2.2: all semantic aliases resolve: `--background`, `--surface`, `--text`, `--text-muted`, `--border`, `--accent-solid`, `--accent-text`, `--focus`.
- [ ] DW-2.3: the type scale is present (12 / 13 / 14 / 16, plus any display step).
- [ ] DW-2.4: functional colors `--error/success/warning/info-*` are defined.
- [ ] DW-2.5: all text/background pairs pass AA (≥ 4.5:1 body), checked with `palette.mjs`.
- [ ] DW-2.6: the focus ring and control boundaries pass ≥ 3:1.
- [ ] DW-2.7: the user confirms the dealt direction on the styled mock rendered right after this phase, and only then is `DESIGN.md` marked locked.
- [ ] DW-2.8: the accent's OKLCH hue differs from series-1 `#2a78d6` by ≥ 40°, or its chroma/lightness is clearly apart.

### Phase 3: Words
**Stage:** Design
**Model:** haiku
**Doctrine:** content-design
**Gate:** Minimal

**Goal:** Microcopy in one voice for every state the page spec names.

**Scope:**
- IN:
  - Empty states: no tables, no rows, nothing to chart, no history.
  - Error messages in the order what happened → why → how to fix.
  - Toasts.
  - The Ask-off hint.
  - The truncation and sort notices.
  - History labels.
  - Column-panel labels.
  - Dialog copy.
- OUT: README and docs.

**Produces:** `JOURNEY.md` `## Microcopy`, a table of state, string and tone.
**Depends on:** Phases 1, 2 | **Unlocks:** Phase 5

**Done when:**
- [ ] DW-3.1: every state in the Workbench page spec has a string in `## Microcopy`.
- [ ] DW-3.2: every error string states what happened and how to fix it, and none blames the user.

### Phase 4: Data surfaces
**Stage:** Design
**Model:** sonnet
**Doctrine:** data-viz, interaction, usability
**Gate:** Standard

**Goal:** Specs for the results grid, column panel, chart and profile as one results experience.

**Scope:**
- IN:
  - **Grid:**
    - Rows 30–32 px with 13 px data text.
    - Formatting by type: tabular figures; thousands separators except for id/year columns; null token; JSON hints.
    - Sort cycle: ascending → descending → original.
    - Cell focus, popover and copy.
  - **Column panel:** stats, top values and histogram, computed over the returned rows.
  - **Chart:** defaults inherited from the column selected in the grid, the single-series conventions, and AA axis ink.
  - **Profile tab:** the whole table, as now.
- OUT: multiple worksheets; comparing results side by side.

**Edge cases:**
- All-null columns.
- A column with a single distinct value.
- Mixed numeric and text values.
- 1,000-row truncation.
- Zero rows.

**Produces:** `JOURNEY.md` `## Data surfaces`, with grid, panel, chart and profile specs.
**Depends on:** Phases 1, 2 | **Unlocks:** Phase 5

**Done when:**
- [ ] DW-4.1: the specs define behavior for every edge case above.
- [ ] DW-4.2: chart encodings pass the data-viz truthfulness audit (bars start at zero, one axis).
- [ ] DW-4.3: data ink uses the series-1 blue only, never the accent.

### Phase 5: Compose into the live app
**Stage:** Design
**Model:** sonnet
**Doctrine:** design-systems, interaction, responsive, usability, ai-tells
**Gate:** Full

**Goal:** Apply the tokens, words and specs to `index.html`, add query history, then render, review and fix.

**Scope:**
- IN:
  - All regions in the page spec.
  - History (`localStorage`, last 100 entries, load / rerun / clear).
  - The grid, panel and chart specs.
  - The microcopy.
- OUT: backend changes.

**Edge cases:**
- `localStorage` unavailable: history degrades to the current session.
- Fonts offline: fall back to system fonts.
- Chart.js missing: the Chart tab shows an empty state.

**Produces:** the redesigned `index.html` and `mocks/final-workbench.png`.
**Depends on:** Phases 2, 3, 4 | **Unlocks:** none

**Done when:**
- [ ] DW-5.1: no hard-coded hex or rgb outside the `:root` token block.
- [ ] DW-5.2: all text pairs pass AA and focus indicators pass ≥ 3:1, checked on the rendered page.
- [ ] DW-5.3: at least 15 result rows are visible at 1440×900; at 375 px wide there's no page-level sideways scroll.
- [ ] DW-5.4: the review agent's cross-pillar synthesis finds no Critical issues, and every Major issue is resolved or explicitly accepted.
- [ ] DW-5.5: every region and state in the Workbench page spec is present on the rendered page (Ask off, logged out, the route from upload to sign-up, history empty and filled, the column panel).
- [ ] DW-5.6: the accent covers less than 5% of the composed screen at 1440×900.
- [ ] DW-5.7: a screenshot of the rendered page is captured at `mocks/final-workbench.png`.

---

## Verification plan

- **Phases 1–4:** every DW item above, checked by the design-review agent.
- **Phase 5:** DW-5.1–5.7, checked in the browser. The functional regression list in Constraints is also checked in the browser, and the main session runs `app.py check` before committing (repository rule).
- **Failure cases to try:**
  - **Phase 1:** a page spec missing the Ask-off state, which should be rejected.
  - **Phase 2:** an accent within 40° of series-1, which should be rejected, and a token below AA, which should be rejected.
  - **Phase 3:** an error string with no fix, which should be rejected.
  - **Phase 4:** a bar chart with a non-zero baseline, which should be rejected.
  - **Phase 5:** `localStorage` throwing, where history must still work for the session, and a 1,000-row sort notice.
- **Level:** design review on the rendered page, plus manual browser checks of the regression list.

## Assumptions

- History in the browser is acceptable for a local, single-user tool. It's shared between logged-in and logged-out use in the same browser.
- Phase 5 changes product code, so it's committed by the main session under the repository's docs rule (CHANGELOG, README and ARCHITECTURE are updated, then pushed), not by the plugin's own commit step.

## Decision log

- **Standard track:** a single screen, but it combines a new identity and data surfaces, which needs both Discover and Design.
- **Phases 3 and 4 run in parallel:** both depend only on `JOURNEY.md` and `DESIGN.md`.
- **Phase 5 added** so the design ends in the live product, not just mocks, as the user asked.

## Execution log

### Phase 1: Journey and page spec (Gate: Standard)
- [x] BUILD: discovery, design and production complete (sonnet)
- [x] REVIEW: fail → fail → PASS (3 attempts, haiku; fresh reviewer each time)
- [x] Committed
Summary: `JOURNEY.md` specifies the analyst loop (F1–F5) and the Workbench page (R1–R16), with every state, an Esc precedence table, per-account history, undo on worksheet replace, cancel for Run/Ask, and the Ask mode note. 10 minor review findings are left for Phase 3 (words) and Phase 5.

### Phase 2: Visual identity and tokens (Gate: Full)
- [x] BUILD: discovery, two dealer rounds (round 0 all failed constraints; round 1 executed), critique and convergence (opus)
- [x] REVIEW: PASS (sonnet). DW-2.7 pending the mock gate. Major: signature swapped from hand 1 (`duotone-images`) to hand 2 (`border-interrupt-headings`); the user decides at the mock gate.
- [x] Committed
Summary: `DESIGN.md` "Verdigris Ledger" (Sage/Ruler; Archivo + IBM Plex Mono; verdigris accent hue 165.7, 89.8° from series-1) with an AA-verified light token block. Pending user lock at the mock gate.

### Mock gate
- [x] MOCK: styled mock `mocks/workbench.html` (+ desktop and narrow PNGs), minimal gate (sonnet)
- [x] REVIEW: PASS on pixels (sonnet); detector exit 0, 1 advisory (row-number column). Minors: histogram uses the data blue (intended), clipped grid bottom with no scroll hint, narrow tab wrap, small Esc close target.
- [x] User sign-off: **Approve**, and the signature swap kept. DESIGN.md locked (DW-2.7).

### Phase 3: Words (Gate: Minimal)
- [x] BUILD: minimal, produced directly (haiku); words check exits 0 (coverage, 104 unique IDs, error formula, no blame/exclamation, no stale placeholders)
- [x] REVIEW: SKIPPED. Minimal gate; design execution evidence is the gate.
- [x] Committed
Summary: `JOURNEY.md` `## Microcopy` has 104 strings covering every Workbench state, with errors in the what → why → fix form, and the six Phase 1 wording issues are fixed. For Phase 5: replace "Log in to upload" in index.html with "Sign up to upload", use the Microcopy strings instead of raw server text, and use "·" as the only status separator.

### Phase 4: Data surfaces (Gate: Standard)
- [x] BUILD: discovery, design and production (sonnet); 15-row density budget measured at 1440×900 (Ask 82 px, editor 3 lines, region gaps 16 px)
- [x] REVIEW: fail → PASS (2 attempts, haiku; fresh reviewer). Fixed: the one-mark-per-row chart rule, null Y never drawn as zero (disclosed count), and zero-row column kind `unknown`.
- [x] Committed
Summary: `JOURNEY.md` `## Data surfaces` specifies the grid (kinds, formatting, sort, cell focus/popover/copy, sticky header, scroll cues), the column panel, the chart and the profile, plus an edge-case matrix and DS-01–DS-15 strings. For Phase 5: only the header *name* sorts and the details button must not trigger a sort; disabled sort on 0/1-row results gets an explanatory title; give the post-error chart state its own string; show a Shift+Enter hint.

### Phase 5: Compose into the live app (Gate: Full)
- [x] BUILD: discovery, design and production (sonnet); the run was cut off by a usage limit, then resumed with its context; evidence: 864 text nodes ≥ 4.92:1, focus 5.56–5.75:1, accent ≈ 1% of the screen, no color literal outside `:root`, 375 px with no page scroll
- [x] REVIEW: fail → PASS (haiku). The only blocker was a screenshot of the Ask-on state rather than the default; it was recaptured. 0 Critical, 0 Major; detector exit 0 with 0 findings.
- [x] Orchestrator smoke test: no console errors; an example query runs and history records it. Fixed a grid formatting inconsistency (per-value grouping threshold → grouping at ≥ 1,000; JOURNEY.md updated).
- [x] Committed
Summary: the live `index.html` implements DESIGN.md and JOURNEY.md: Verdigris Ledger identity, query history, column details, a sortable keyboard grid, truthful chart, ≥ 15 rows at 1440×900. `/me` returns the Ask mode.

## Trust report
- **Contrast:** PASS (DESIGN.md token block AA-checked with palette.mjs; rendered page measured: 864 text nodes ≥ 4.92:1, focus ≥ 5.56:1). Light only, as the user decided.
- **Token coverage:** all semantic aliases resolved; type scale and functional colors present; no color literal outside `:root`.
- **Mocks:** `mocks/workbench.html` (approved), `mocks/final-workbench.png` (Ask off, default), `mocks/final-workbench-ask-on.png`.
- **Heuristic:** no unresolved Critical findings; no open Majors (Phase 4's two Majors were implemented in Phase 5).
- **Not verified live:** Ask-on states beyond idle (no question was submitted, to save the user's plan allowance); Chart.js missing and localStorage blocked (checked from the code paths only); a full real-keyboard Tab/Esc walk-through.
- **Follow-up:** both resolved after the build: at < 860 px main now comes before the explorer, and `YYYY-MM` counts as a date (line chart by default).
