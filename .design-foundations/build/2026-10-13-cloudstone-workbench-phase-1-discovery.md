# Discovery + Design: Phase 1 - Journey and page spec

## Artifacts Found / Current State
- No JOURNEY.md, no DESIGN.md. Plan and research brief read; research "Decisions (researcher defaults)" treated as binding.
- Current product read from README.md, ARCHITECTURE.md and index.html (939 lines). Inventory of what the spec must keep reachable:
  - Top bar: brand, Log in / Sign up (logged out), account button + Log out (logged in).
  - Sidebar: upload drop zone (click, drag-drop, multi-file; logged out routes to sign-up dialog), explorer (search filter, `my_data` and `demo` groups with counts, per-table expander showing columns+types, column click inserts into SQL, demo type badges), collapsible Example queries (10).
  - Main: Ask card (hidden when Ask off; input, Ask button, 4 suggestion chips, explanation/error line), Worksheet card (line-numbered editor, Run, status line, Ask-off hint), Results card (tabs Results/Chart/Profile with arrow-key tabs, row/column meta, CSV, grid, chart controls Type/X/Y, profile grid).
  - Dialogs: auth (login/signup segmented, show/hide password, hint, error), account (change password, delete account with confirm()).
  - Toasts (live region), shortcuts `/` and Cmd/Ctrl+Enter, Tab indents in editor, 1,000-row cap with "showing the first 1,000".
  - States today: Running..., error text in status, "No rows matched.", "No rows to show" for DDL, chart empty states, explorer "Loading...", "No matches.".
- New in scope (research defaults): Explorer|History switch, history (localStorage, 100), column panel, sorting, cell focus/popover/copy, truncation + sort notice.

## Gaps
- Today's page has no history, sorting, column panel, cell keyboard model; Profile tab label embeds table name; error for Ask is shown only in the explanation card (not in results).
- Plan says "five journeys" in IN: preview a table, iterate a query, Ask then refine, upload when logged out, rerun from history.
- Open: ARCHITECTURE says unauthenticated /upload is refused; spec routes to sign-up before any request (matches index.html).

## Gate Status
DESIGN.md absent (expected: Phase 2 creates it). JOURNEY.md is the gate this phase satisfies. Prerequisites met (research doc present). Spec is style-free so it does not depend on tokens.

## DW Verification
| DW-ID | Done-When Item | Status | Evidence |
|-------|---------------|--------|----------|
| DW-1.1 | Workbench entry: every region, states (empty, loading, error, logged out, Ask off), keyboard | COVERED | Region x state matrix + per-region keyboard rows in JOURNEY.md `## Page specs`; checked by grep that each region row names all five states and a Keys line |
| DW-1.2 | Flows cover all five journeys, each with visible outcome | COVERED | Five flows F1-F5 each with an explicit "Outcome (visible)" line; grep count = 5 |
| DW-1.3 | Hick's law + Cowan ~4+-1 cited where options are cut | COVERED | Citations inline at: top bar, sidebar sections, tab set, column panel stat groups, history rows, Ask chips, results header; grep for "Hick" and "Cowan" |
**All items COVERED:** YES (3/3 = 3 in prompt)

No palette.mjs/prototype evidence: this phase has no tokens or visuals (OUT: visual styling). Evidence is structural/traceability only.

## Design Decisions
- JTBD school: Moesta/Switch (four forces), per journey doctrine; one school only.
- Journey is a loop (explore <-> evaluate; loyalty-loop style), not a funnel (messy middle, Google 2020). Theater risk flagged: owner = repo owner, basis = research brief (no interviews), cadence = revisit at each phase gate.
- IA: task-organized sidebar (Explorer | History switch = Hick: two views not two stacked lists); Example queries stay in Explorer view footer so the logged-out on-ramp is not hidden. Ask above worksheet as today (matches research "keep structure").
- Cowan: results header limited to status + 3 tabs + 2 actions; column panel grouped into 4 chunks; history row shows 4 facts.
- Column-panel selection and chart column share one "selected column" state (research default).
- Grid keyboard: single tab stop, roving cell focus, per research.
- Sort/truncation notice placement specified as a results-card notice strip.

## Recommendation
BUILD
