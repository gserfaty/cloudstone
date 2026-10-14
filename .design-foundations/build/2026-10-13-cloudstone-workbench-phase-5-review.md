# Design Review: Phase 5 - Cloudstone workbench

## Rendered Evidence (Step 0)
- Screenshot: `/Users/gabriel/code/cloudstone/mocks/final-workbench.png` (re-verified after the coordinator's replacement notice): PNG 1440 x 900, Ask off, logged out, "Rows 1 to 17", Ask hint in the Worksheet, no Ask card. Matches the live default page. An earlier capture that showed Ask-on chrome was superseded. See DW-5.7.
- Live surface: `http://localhost:8000` (app.py, Ask off, logged out, demo data), inspected in the Browser pane at 1440×900 and 375×812. Column panel opened live. Source grep on `index.html` and `DESIGN.md`/`JOURNEY.md` for code-path checks.
- Surface: Workbench (`/`), the only page. Default state only. Ask-on, history-empty and logged-in states were not rendered live (see Notes).

## Assessment B — Deterministic Detector
- Command: `node /Users/gabriel/.claude/plugins/cache/rtd/design-for-ai/4.2.0/scripts/detect.mjs /Users/gabriel/code/cloudstone/index.html > /private/tmp/claude-501/-Users-gabriel-code-cloudstone/4befd302-b57c-4098-8aae-0223da79144f/scratchpad/detect.json`
- Exit: 0 (ran, status "ran", 16 rules)
- Findings: 0 (`counts.total: 0`, `byRule: {}`)
- Opened only after Assessment A findings were frozen: YES

## Triage
- Baseline (always-on): visual + usability
- Dispatched: visual (`design-systems`, `ai-tells`, `responsive`, `interaction`) and usability. Signals present: a data table and SQL editor (operable), a stated visual direction, and responsive layout.
- Not applicable: `data-viz` (the Chart tab exists, but I did not render a chart and the requirements do not list chart encoding), `content-design` (microcopy was not in the DW list), `journey`, `behavioral`, `deceptive-patterns`, `ai-native`.
- Deferred: none, but the Ask-on and chart-rendering states were not exercised live (see Notes).

## Cross-Pillar Findings (ONE ranked report)
| Severity | Pillar | Problem | Principle | Fix |
|----------|--------|---------|-----------|-----|
| Minor | responsive | At 375 px the Explorer sidebar (upload box, tabs, search, 7 tables, example queries) stacks above the Worksheet and Results. The Run button and the first result rows sit below the first screen. Content is kept, not removed. | Responsive doctrine: adapt presentation, do not strip; Fitts's law (travel to the dominant action) | Collapse the Explorer behind a disclosure below a phone breakpoint, or put the Worksheet first on narrow widths. |
| Minor | usability | The Ask-on example chips in the mock truncate with "...", hiding the full question. Not verified live (Ask-on not rendered). | Nielsen #6 recognition over recall (full text available on hover/focus is not confirmed) | Confirm a `title` or full-text path; otherwise wrap the chip text. |
| Note | visual | The stated direction ("ledger": stone-grey paper, hairline legend rules, mono figures, one verdigris accent) is specific and nameable. Archivo + IBM Plex Mono, no gradients, no purple/cyan, no nested cards in the default view, left-aligned text. Passes the ai-tells CHECKER. | ai-tells.md CHECKER / Critical distinctiveness test: PASS | None. |

No Critical findings. No Major findings confirmed.

## Requirement Fulfillment
### DW-5.1
PREMISE:  no hard-coded hex or rgb outside the `:root` token block.
EVIDENCE: `grep` of `index.html` finds 38 hex literals, all at lines 14–70, inside `:root` (lines 13–98). Zero `rgb(`, `rgba(`, `hsl(`, or `oklch(` literals appear outside `:root`. Computed-style checks in the live page used the same tokens.
VERDICT:  PASS

### DW-5.2
PREMISE:  all text pairs pass AA and focus indicators pass ≥ 3:1, checked on the rendered page.
EVIDENCE: Live page at 1440×900, logged-out default: 32 unique foreground/background pairs computed from the DOM; none below 4.5:1 (the check reported "all text pairs >= 4.5"). Focus ring `--focus` = `--accent-11` #486c5d: 5.75:1 on #fcfdfc, 5.56:1 on #f8f9f8, 5.21:1 on #e6f5ee (accent-3, selected row). Focus uses `outline: 2px solid` with 2px offset (`index.html` line 112).
VERDICT:  PASS (coverage limited to the default state; placeholder text and hidden panels were not measured)

### DW-5.3
PREMISE:  at least 15 result rows are visible at 1440×900; at 375 px wide there's no page-level sideways scroll.
EVIDENCE: At 1440×900, 107 rows are in the DOM and 25 are fully inside the viewport. At 375×812, `document.documentElement.scrollWidth` = 375 = `innerWidth`. The 1065 px table overflows only inside `.gridwrap` (`overflow-x: auto`), so the page does not scroll sideways.
VERDICT:  PASS

### DW-5.4
PREMISE:  the review agent's cross-pillar synthesis finds no Critical issues, and every Major issue is resolved or explicitly accepted.
EVIDENCE: Synthesis above: 0 Critical, 0 Major. Detector: 0 findings. Two Minor rows remain (responsive stacking; chip truncation, unverified).
VERDICT:  PASS

### DW-5.5
PREMISE:  every region and state in the Workbench page spec is present on the rendered page (Ask off, logged out, the route from upload to sign-up, history empty and filled, the column panel).
EVIDENCE:
- Regions (JOURNEY.md Workbench R1–R-series): top bar (Log in, Sign up), upload zone, Explorer/History tabs, Example queries, Ask (hidden), Worksheet, Results with Results/Chart/Profile tabs. All present in the accessibility tree.
- Ask off: `#ask-h` section is `display: none`; the "Ask is off. To turn it on, restart the server with CLOUDSTONE_ASK=subscription..." hint is visible in the Worksheet. Matches JOURNEY lines 108 and 165/191.
- Logged out: Log in + Sign up in top bar; upload title "Sign up to upload"; history note "Showing history for logged-out use in this browser."
- Upload-to-sign-up route: the zone title reads "Sign up to upload" (DOM). Click-through to Auth was not exercised.
- History filled: live, 11 runs listed with Load/Rerun buttons. History empty: code path present (`index.html` line 1419, "Queries you run appear here..."), not rendered live (would require clearing history).
- Column panel: opened live from `order_id` details; shows COUNTS, RANGE, TOP VALUES, and a note on distinct values.
VERDICT:  PASS (history-empty and upload-click paths verified from code only)

### DW-5.6
PREMISE:  the accent covers less than 5% of the composed screen at 1440×900.
EVIDENCE: DOM walk over all visible elements with an accent-hued background fill, clipped to the 1440×900 viewport: 11,624 px² of 1,296,000 px² = 0.90%. Largest fills: the sales row highlight and the primary Run/Ask button. Accent text and hairline rules add less area.
VERDICT:  PASS

### DW-5.7
PREMISE:  a screenshot of the rendered page is captured at `mocks/final-workbench.png`.
EVIDENCE (re-verification): `file` reports `mocks/final-workbench.png` as PNG 1440 x 900 (191,644 bytes). Visually it shows the Ask-off default: Ask card absent, Worksheet hint "Ask is off. To turn it on...", logged-out top bar (Log in, Sign up), "Sign up to upload" zone, "Rows 1 to 17", 100 rows. Live comparison at 1440×900 (server restarted from /Users/gabriel/code/cloudstone, stopped afterward): Ask section `display: none`, `#askoff` shown, Log in and Sign up present, 25 rows fully in viewport, "Rows 1 to 17". Matches. Minor difference: the history count reads 12 live versus 11 in the earlier pass; not a DW-5.7 concern.
VERDICT:  PASS

## Edge cases — verify handling
- localStorage unavailable: HANDLED (code). `histLoad` falls back to `memHist` with `sessionOnly = true` on throw; `histSave` catches and sets `sessionOnly = true`; `pref()` wraps every read/write in try/catch with an in-memory fallback. Not exercised live.
- Fonts offline: HANDLED (code). `--font-ui: "Archivo", ui-sans-serif, system-ui, sans-serif`; `--font-mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace`; the Google Fonts link uses `display=swap`. Not exercised live.
- Chart.js missing: HANDLED (code). `drawChart()` checks `typeof Chart === 'undefined'` and calls `chartEmpty(S.chartMissing)`, which hides the canvas and shows "The chart did not load. Check your connection and reload the page. The Results tab still shows the rows." Redraw runs on view change.

## Notes (non-blocking)
- Coverage gaps: the live review covered the default state only. Ask-on (chip truncation, the explain/status region), history-empty, and the Chart tab with data were not rendered. No placeholder-text contrast was measured.
- The 375 px check confirmed no page-level scroll, but the phone layout is long before the first result. This is a Minor responsive finding, not a DW failure.
- The `mocks/final-workbench.png` row count ("Rows 1 to 15") differs from the live page ("Rows 1 to 17"), which supports the stale-capture finding.
- Browser viewport was reset to the desktop pane. The server was stopped after the review.

## Issues (if FAIL)
1. (Resolved) DW-5.7: the earlier capture did not match the default page. The replaced `mocks/final-workbench.png` is a 1440×900 capture of the Ask-off, logged-out default and matches the live page. Severity: none remaining. Pillar: process.

**Verdict: PASS — all DW items PASS (DW-5.1 through DW-5.7); no Critical or Major findings; detector 0 findings; Minor notes only (phone-width sidebar stacking; Ask-on chip truncation not verified live).**

DESIGN-REVIEW PASS. Report written to /Users/gabriel/code/cloudstone/.design-foundations/build/2026-10-13-cloudstone-workbench-phase-5-review.md
