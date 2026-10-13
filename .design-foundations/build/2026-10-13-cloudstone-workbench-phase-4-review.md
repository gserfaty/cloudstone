# Design Review: Phase 4 - Data surfaces (spec-only)

## Rendered Evidence (Step 0)
- Screenshot: none. Spec-only phase, so there are no pixels to review. Critique is structure-level against `JOURNEY.md` § `## Data surfaces`, checked against `DESIGN.md` tokens and the rest of `JOURNEY.md`.
- Coverage gap: pixel-level density, spacing and rendering are unverified. The spec's "measured in the browser on the mock" claim cannot be checked from this artifact.
- Surface: `/Users/gabriel/code/cloudstone/JOURNEY.md`, § Data surfaces (§1 model, §2 budget, §3 grid, §4 column panel, §5 chart, §6 profile, §7 edge matrix, §8 keys, §9 strings, §10 checks).

## Assessment B — Deterministic Detector
- Command: not run. No rendered `.html` or mock exists in this phase.
- Exit: N/A (no rendered artifact).
- Findings: N/A — no rendered artifact.
- Opened only after Assessment A findings were frozen: N/A.

## Triage
- Baseline (always-on): visual + usability.
- Dispatched:
  - `data-viz` (signal: bar, line, scatter and histogram encodings in §5 and §4). Applied the chart-audit procedure: lies, one axis, zero baseline, data-ink, colour-as-encoding.
  - `usability` (signal: grid, sort, keyboard, popover, status and panel). Applied Nielsen heuristics and the 0–4 severity scale.
  - `interaction` (signal: every control's state across default, focus, disabled, loading, error, zero rows). Applied the state-lifecycle check to §3, §4, §5 and §7.
- Not applicable: `content-design` (only the §9 strings are new copy; checked for presence and consistency, not voice), `journey`, `behavioral`, `deceptive-patterns` (no persuasion surface).
- Deferred: none.

## Assessment A — Cross-Pillar Findings (frozen before reading detect.json)

| Severity | Pillar | Problem | Principle | Fix |
|----------|--------|---------|-----------|-----|
| Major | interaction | The sort target is described two ways. §3 says the sort target is "clicking the name, or Enter / Space on the focused header." §8 says "sort target is the full header cell." The details button (24 px) sits inside that same header cell and the spec never says its click stops propagation. A pointer user clicking the details button could also trigger a sort. | Nested-control ambiguity (WCAG 2.5.8, 4.1.2); Norman mapping (1988/2013) | Pick one sort target. State that the details button click does not bubble to the sort handler, and say so in §3 and §8. |
| Major | usability | The sort control is `aria-disabled` and dimmed on 0- or 1-row results, with no explanation. The interaction doctrine requires a disabled control to explain itself ("muted with an explanation, not just grayed out"). The chart's Scatter option does this (DS-11) and the sort control does not. | Nielsen #1 (visibility of status); interaction doctrine, disabled state | Give the disabled sort a title or tooltip that says why (for example "Sorting needs at least two rows"), or hide the sort glyph. |
| Minor | usability | Discoverability of the keyboard path: Enter sorts and Shift+Enter opens column details, and neither has a visible hint on the header. The details button is not in the tab order (only Shift+Enter reaches it). | Nielsen #6 (recognition over recall); WCAG 2.1.1 is met, but only by documentation | Add the Shift+Enter hint to the key help or to the details button's `title`. |
| Minor | usability | MC-68 ("Run a query to chart its result.") is reused for the chart after a run error. After a failed run, that copy reads as if nothing was run yet, not as "the query failed." | Nielsen #9 (help users recognise, diagnose and recover from errors); content-design consistency | Give the post-error chart state its own string, or say "The last run failed. Fix the query and run it again." |
| Minor | data-viz | When more than 60 categories are present, tick labels auto-skip. Bars then have no visible category label. Values are available by tooltip, which is pointer-only. The keyboard path is the Results tab, referenced by MC-73. | Direct labelling (Few 2006); no hover-only information (WCAG 1.4.13, 2.1.1) | Note in §5 that auto-skipped categories are reachable by keyboard through the Results tab, or label the extremes. |
| Minor | interaction | The loading state dims the grid with `opacity` only. Text under dimming can fall below 4.5:1. The state is transient, so the impact is small. | WCAG 1.4.3 (transient); interaction doctrine, loading state | Acceptable as written, or hold text colour and dim only the cell background. |
| Minor | data-viz | The `number` kind accepts "numeric strings with no leading zero," but the spec does not define the grammar. Forms like `1e5`, `+5` and `-0` are unspecified. | Truthful encoding: the inferred kind decides the chart and sort behaviour | Add one sentence defining the accepted numeric grammar. |
| Minor | data-viz | §1 promises huge integers keep every digit. The sort, mean, histogram and bar lengths compare or compute on values. If they parse with `Number`, huge integers near 2^53 can sort or bin incorrectly. This is not one of the five listed edge cases. | Truthful encoding (precision); Cleveland and McGill (1984) | State that chart, sort and statistic values use float precision, with full digits kept in the grid and tooltip. |
| Note | spec | A single-row result is not defined. Every column becomes "one distinct value" (MC-65), and the chart gets one bar. Not a listed edge case. | Consistency | Add one line to §7 if the team cares. |
| Note | spec | The density numbers (15 full rows, 16 px peek) depend on "measured in the browser on the mock." This cannot be verified here. The §2 arithmetic does check out (Requirement Fulfillment, DW-4.1 evidence). | Evidence over assertion | Attach the mock measurement or a screenshot in Phase 5. |
| Note | spec | The chart contrast table assumes the chart sits on `--background`. If it sits on `--surface`, `--data-1` is 4.18:1 (also ≥ 3:1, so it still passes). | Accuracy of claimed evidence | State the host surface in §5. |

Earlier-draft criticals not carried forward: the current text defines one mark per row with DS-13 disclosure, a null-Y rule with DS-14, and zero-row kind `unknown` (§1). Those are present in the artifact read for this review.

## Requirement Fulfillment

### DW-4.1
PREMISE:  "the specs define behavior for every edge case above."
EVIDENCE: JOURNEY.md § Data surfaces §7 edge matrix has a row for each of the five listed cases, and each row fills every column (grid and sort, column panel, chart, header status and CSV):
- All-null column: kind `null`, every cell the `null` token, counts then MC-64, never offered as Y, labelled `null` as X with DS-13.
- Single distinct value: counts then MC-65, range/top/histogram omitted, equal bars with zero baseline as Y.
- Mixed numeric and text: kind `mixed`, DS-03, MC-66, excluded from Y, allowed as X, numbers sort first.
- 1,000-row truncation: MC-45 header, MC-50 strip, MC-63 footer, DS-06 caption, CSV covers returned rows only.
- Zero rows: kind `unknown` (checked before the `null` rule), MC-52, DS-05, MC-69, CSV header-only, sort inert.
VERDICT:  PASS

### DW-4.2
PREMISE:  "chart encodings pass the data-viz truthfulness audit (bars start at zero, one axis)."
EVIDENCE: §5 audit table: "Bar Y axis always includes 0: min = min(0, data min) … No grace, no log scale." "Exactly one Y axis and one X axis, one series, no right-hand axis, no legend." Non-zero line/scatter baselines are disclosed by DS-07. Null Y is never drawn as zero (DS-14). Capped and sorted states are disclosed in the caption. Histogram and top-value bars also start at zero (§4). Nothing is dropped or aggregated in the browser.
VERDICT:  PASS

### DW-4.3
PREMISE:  "data ink uses the series-1 blue only, never the accent."
EVIDENCE: §5 ink table: bars, line and scatter points use `--data-1` (#2a78d6). Histogram and top-value bars in §4 use `--data-1` only. §5: "The accent never encodes data: no accent bar, no highlighted bar for the selected column." DESIGN.md line 159 agrees ("Chart and column-panel bars → `--data-1`; the accent never encodes data"). Accent appears only on grid selection and focus, not data ink. Contrast, computed from the hex values with the WCAG formula: `--data-1` #2a78d6 on `--background` #fcfdfc = 4.33:1; on `--surface` #f8f9f8 = 4.18:1; `--text-muted` #5e6562 on `--background` = 5.86:1 (all ≥ 3:1 for graphics, ≥ 4.5:1 for text). Border-control 3.39:1 is taken from DESIGN.md and was not recomputed.
VERDICT:  PASS

## Edge cases (verified, same standing as DW items)
- All-null column: handled (§7, row 1). PASS.
- Single distinct value: handled (§7, row 2). PASS.
- Mixed numeric and text: handled (§1 kind table, §4 DS-03/MC-66, §7 row 3). PASS.
- 1,000-row truncation: handled (§2, §3, §5, §7 row 4). PASS.
- Zero rows: handled (§1 `unknown` kind, §3, §4, §5, §7 row 5). PASS.

## Requirement Fulfillment summary
**All requirements met:** YES

## Notes (non-blocking)
- Pixel-level gap: no screenshot. Density, spacing and the "measured on the mock" claim are structure-checked only.
- Notes listed in the Assessment A table above (single-row result, huge-integer precision, numeric grammar, host surface for the contrast claim).
- Distinctiveness criterion: N/A for a spec-only phase (it applies to rendered surfaces).

## Issues (if FAIL)
None blocking. The two Major rows (nested sort/details target, unexplained disabled sort) are spec refinements, not unhandled edge cases or failed DW items, so they do not change the verdict.

**Verdict: PASS**
