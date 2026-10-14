# Discovery + Design: Phase 5 - Compose into the live app

## Artifacts Found / Current State
- index.html (939 lines): old Inter/JetBrains styling, navy-free but card-based, no history, no sort/kinds/panel, Chart.js 4.4.1 from cdnjs, in-canvas chart title.
- app.py `/me` returns `ask` as a boolean (the one allowed change: return `ask_mode()` string).
- DESIGN.md locked (Verdigris Ledger); JOURNEY.md R1-R16, Microcopy, Data surfaces present; mocks/workbench.html is the approved look.

## Gaps
- Everything in JOURNEY.md is unimplemented in the live page: legends, History (localStorage per account), kinds/sort/cell focus/popover/copy, column panel, chart rules, DS strings, Esc layers, toasts with Undo, cancel for Run/Ask.
- Server error strings must be mapped to MC/ASK strings client-side (no backend change).

## Gate Status
DESIGN.md locked: yes. JOURNEY.md present: yes. Prerequisites met.

## DW Verification
| DW-ID | Done-When Item | Status | Evidence |
|-------|---------------|--------|----------|
| DW-5.1 | no hex/rgb outside :root | COVERED | grep of index.html for `#[0-9a-f]{3,8}` / `rgb(` outside the :root block returns nothing |
| DW-5.2 | AA text + focus >= 3:1 on rendered page | COVERED | script in the browser computes ratios for every visible text node vs. its effective background, plus focus ring vs. neighbours |
| DW-5.3 | >= 15 rows at 1440x900; no sideways page scroll at 375 | COVERED | measured fully visible grid rows; scrollWidth vs clientWidth at 375 |
| DW-5.4 | review agent synthesis | PENDING (REVIEW sub-phase) | n/a |
| DW-5.5 | every region/state present | COVERED | rendered checks: Ask on/off, logged out, upload -> sign-up dialog, history empty/filled, column panel |
| DW-5.6 | accent < 5% of screen | COVERED | screenshot pixel count of accent-family colours at 1440x900 |
| DW-5.7 | screenshot mocks/final-workbench.png | COVERED | headless Chrome capture |
All 7 DW-IDs mapped (7/7).

## Design Decisions
- Reuse the approved mock's CSS structure verbatim (legend-on-rule via `.region > h2`, ledger table, panel) and the DESIGN.md token block; no hex outside :root. Chart colors are read from CSS custom properties at draw time.
- One vanilla JS file; a single `grid` component drives Results and Profile (read-only mode). Result view state = {result, order, sort, selectedCol}; CSV, grid and chart all read the view order.
- History in localStorage key `cloudstone.history.v1:<user>` / `...:` for logged out; try/catch with in-memory fallback and MC-22 notice.
- Server errors are mapped to Microcopy strings by pattern (ASK-E1..E8); unknown reasons fall back to the formula string with `{server reason}`.
- Native `<dialog>` for Auth/Account; native confirm() replaced with an inline confirm (delete requires password already + explicit second button state).
- Carry-forward: details button stops propagation; sort inert at <=1 row with title; post-error chart shows MC-68; Shift+Enter hint shown in grid caption/title attributes.

## Recommendation
BUILD
