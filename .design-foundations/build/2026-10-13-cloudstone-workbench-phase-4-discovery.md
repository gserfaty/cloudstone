# Discovery + Design: Phase 4 - Data surfaces

## Artifacts Found / Current State
- JOURNEY.md: F1-F5, Workbench R1-R16 (R10-R14 are the data surfaces, one paragraph each), Microcopy MC-43..MC-77 (status, notices, grid, panel, chart, profile). No `## Data surfaces` yet.
- DESIGN.md: locked. Tokens used here: `--data-1`, `--row-h: 32px`, `--rule`, `--border-control`, `--accent-selected`, `--accent-bg-subtle`, `--text-muted`.
- Mock `mocks/workbench.html` (approved): ~11 rows visible at 1440x900; grid bottom clipped.
- `index.html` today: `renderGrid` (no types, no formatting beyond text, no sort), `setupChart`/`drawChart` (Chart.js, `--series-1`, rounded bars, 300 ms animation, `beginAtZero` only for bar, chart title drawn inside the canvas).
- `app.py`: query result is `{columns: [names], rows, truncated}`. **No column types in the payload** and dates/decimals/huge ints arrive as strings (`json.dumps(default=str)`). So grid type hints must be inferred in the browser (not DuckDB types). Profile does carry DuckDB types.

## Gaps
1. Density: mock gives ~11 rows; need >= 15 (resolved below with measured evidence).
2. Grid scroll affordance missing (resolved).
3. Result has no types -> kind inference rules needed, including leading-zero numeric strings ("02134") and mixed columns.
4. Chart default from the grid selection undefined; chart title duplicated in canvas; chart on capped/sorted data undefined.
5. Microcopy lacks strings for: mixed breakdown, all-distinct, zero-row panel, scroll range, empty copy, chart caption/axis note, profile scope. Added as DS-xx rows inside the new section (to be merged into `## Microcopy` in Phase 5; none changes an existing MC row).
6. Notice strip (R10) costs 24-40 px of grid height; criterion is evaluated in the baseline state (no notice).

## Gate Status
DESIGN.md locked: yes. JOURNEY.md present with page spec + microcopy: yes. Prerequisites met. No locked value needs to change (rows stay 32 px; no new font sizes; the mock's 11 px type hint is replaced by 12/16 inline).

## DW Verification
| DW-ID | Done-When Item | Status | Evidence |
|-------|---------------|--------|----------|
| DW-4.1 | specs define behavior for every edge case | COVERED | Edge-case matrix (5 cases x grid/sort/panel/chart/profile/status/CSV) in `## Data surfaces`; every cell filled, no "n/a" without a reason |
| DW-4.2 | chart encodings pass truthfulness audit | COVERED | Audit table in the section (zero baseline for bars, one Y axis, no dual axis, labelled non-zero line baseline, no silent dropping, capped-data caption) cited to Cairo/Tufte |
| DW-4.3 | data ink is series-1 blue only | COVERED | Ink table: only `--data-1` (#2a78d6) on marks; contrast computed: 4.33:1 on `--background`, 4.18:1 on `--surface` (>= 3:1 graphics); accent never on data; axis ink `--text-muted` 5.86:1, axis line `--border-control` 3.39:1 |
Count: 3 of 3. **All items COVERED:** YES

Density evidence (a): scratch copy of the approved mock with the budget applied (editor 3 lines, one-row Ask + chips line, 16 px region gaps, 12 px bottom pad), measured in the browser at 1440x900: Ask 82, Worksheet 144, Results 574 (header 40 + grid 532 incl. 36 sticky header) -> 15 full rows + 16 px of the 16th. Sum 40+16+82+16+144+16+574+12 = 900.

## Design Decisions
- Budget (not editing DESIGN.md): rows stay 32; savings from Ask (166 -> 82, chips + mode note share one line), editor default 3 lines (resizable), gaps 24 -> 16, no footer row (scroll hint = half-row peek + bottom rule + range readout). Ask is off by default, so 18 rows in the common case.
- Grid is the only scroller; sticky header + sticky row-number column; `scroll-padding` so focused cells are never under the sticky header (WCAG 2.4.11).
- Chart: bars always include zero; lines may auto-range but must say so; one Y axis; Chart.js title removed in favour of an HTML caption that also states capped/sorted scope.
- Selection model: one "selected column" shared by grid tint, panel and chart defaults.
- Notice cost accepted: 14 full rows with a one-line notice (honesty about capped sorts outranks 1 row).

## Recommendation
BUILD
