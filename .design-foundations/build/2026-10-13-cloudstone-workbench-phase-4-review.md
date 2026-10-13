# Design Review: Phase 4 - Data surfaces (spec-only)

## Rendered Evidence (Step 0)
- Screenshot: none — spec-only phase. Structure-level critique of `JOURNEY.md` § `## Data surfaces` against `DESIGN.md` (locked tokens) and the rest of `JOURNEY.md`. Pixel-level contrast, spacing and density are unverified; the spec's own "measured on the mock" claim cannot be checked from this artifact.
- Surface: `/Users/gabriel/code/cloudstone/JOURNEY.md`, § Data surfaces (§1 model, §2 budget, §3 grid, §4 column panel, §5 chart, §6 profile, §7 edge matrix, §8 keys, §9 strings, §10 checks).

## Assessment B — Deterministic Detector
- Command: not run. No `.html`/mock artifact exists in this phase.
- Exit: N/A (no rendered artifact).
- Findings: N/A — no rendered artifact.
- Opened only after Assessment A findings were frozen: N/A.

## Triage
- Baseline (always-on): visual + usability.
- Dispatched:
  - `data-viz` — the spec defines a bar/line/scatter chart and a histogram over data (§5, §4). Read `skills/data-viz/SKILL.md` (chart-audit procedure: lies, data-ink, colorblind).
  - `usability` — grid, sort, keyboard, popover and status are operable UI (§3, §8). Read `skills/usability/SKILL.md` (Nielsen 10, 0–4 severity, cite-down rule).
  - `interaction` — the spec defines states for every control (loading, error, zero rows, disabled sort/chart controls, focus). Read `references/visual/interaction.md` headings and key definitions; applied its state-lifecycle check to §3, §4, §5 and §7 only, not the full doctrine.
- Not applicable: `content-design` (the new strings in §9 are the only copy; not reviewed for voice, outside the requested scope), `journey`, `behavioral`, `deceptive-patterns` (no persuasion surface).
- Deferred: none capped. The §9 copy was checked only for presence and format, not for voice.

## Cross-Pillar Findings (ONE ranked report)
| Severity | Pillar | Problem | Principle | Fix |
|----------|--------|---------|-----------|-----|
| Critical | data-viz | The chart plots "every returned row" as its own bar (§5, "Every returned row is plotted"), but §7 says the all-null X case is "a single bar" and the single-distinct-value X case is "one category". These cannot both hold. Duplicate X categories, the most common case in SQL results (for example `region` repeated across orders), have no defined rule: N bars with the same label, or an aggregate. The caption "{n} rows plotted" then means different things. | Truthful encoding (Cairo 2019); one mark per datum (Munzner 2014) | Pick one rule and write it in §5. Either (a) one bar per row, with repeated labels disclosed in the caption, or (b) an explicit aggregate (count, sum or mean) with the aggregate named on the Y axis and in the caption. Then rewrite the §7 rows for all-null X and single-distinct X to match. |
| Critical | data-viz | Null Y values have no rule. Nulls are allowed in `number` columns (§1 kind table, "every non-null value"), but the chart never says whether a null-Y row is drawn at zero, drawn as a gap, or dropped. Drawn at zero, a missing value is encoded as a measured zero, which is a lie. | Truthful encoding (Cairo 2019); absence vs zero (Tufte 1983, data ink) | State: a null-Y row has no bar or point; the caption discloses the count (for example "{k} rows with null {Y} not drawn"). Count it in "rows plotted" or say it is excluded. |
| Major | usability / spec consistency | Zero-row kind is undefined. The kind rule says `null` = "every value is null", which is vacuously true when there are no rows, so every column of a zero-row result would be typed `null` and carry the `null` hint. That conflicts with the numeric alignment rules and with "Header row stays" in §7. | Nielsen #1 (status must match reality); internal consistency | Add one line to §1: with zero rows the kind is `text` (or no hint is shown), and say which. Repeat it in §3 zero-row state. |
| Minor | data-viz | Decimal and huge-integer strings are `number` kind (§1), but Min, Max, Mean, histogram bins and bar lengths are not defined on their parsed value. Parsing to a float can lose digits, and §1 promises that huge integers keep every digit. | Truthful encoding (precision); Cleveland and McGill (1984), position on a common scale | Say that chart and statistic values are computed from `Number(…)`, and that huge integers are plotted at float precision with the full digits kept in the tooltip and the grid. |
| Minor | usability | Sort affordance on a 0- or 1-row result is `aria-disabled`, but the spec does not say whether the sort glyph is hidden or dimmed. | Norman, signifiers (1988/2013); interaction state lifecycle | Say dimmed or hidden, and keep it consistent with the other disabled controls. |
| Note | spec | "15 full rows at 1440 x 900 … measured in the browser on the mock" cannot be verified here (no screenshot). The arithmetic in §2 checks out (see Requirement Fulfillment). | Evidence over assertion | Attach the mock measurement or a screenshot in Phase 5. |
| Note | spec | Editor height of 104 px inside the 144 px worksheet is implied (60 px text + padding) but not itemised. | — | Not a defect; itemise in Phase 5 if the implementation diverges. |
| Note | spec | Kind inference from at most 1,000 values is an open risk the spec already names. Not a new finding. | — | None. |

## Requirement Fulfillment

### DW-4.1
PREMISE:  "the specs define behavior for every edge case above."
EVIDENCE: Edge matrix (§7) covers all five listed cases across grid, sort, panel, chart and status:
- All-null: grid kind `null`, sort allowed and inert (§3); panel = counts + MC-64 (§4); chart not offered as Y, but "can still be chosen as X (all 'null' categories, a single bar)" (§7). That X-row contradicts the per-row plotting rule in §5 ("Every returned row is plotted"). Unresolved.
- Single distinct value: grid normal (§7); panel = counts + MC-65, range/top/histogram omitted (§4); chart "as X: one category" (§7). Same contradiction as above, with N rows and one category. Unresolved.
- Mixed numeric and text: kind `mixed`, left-aligned, no separators, numbers before text on sort (§1, §3); panel DS-03 + MC-66, no range/histogram (§4); excluded from Y, allowed as X (§5, §7). Specified.
- 1,000-row truncation: MC-45 header, MC-50 strip always shown (§3, §7); footer MC-63 (§4); caption "first 1,000 rows plotted" (§5); CSV = returned rows (§7). Specified.
- Zero rows: header kept, MC-52 (§3); counts 0 + DS-05 (§4); MC-69, controls disabled (§5); status MC-44, CSV header-only (§7). Specified, except the kind of the zero-row columns, which the kind rule (§1) leaves undefined (Major finding above).
Two listed cases (all-null, single distinct) are unresolved on the chart. The spec does not define behavior for them that is consistent with the rule it states.
VERDICT:  FAIL

### DW-4.2
PREMISE:  "chart encodings pass the data-viz truthfulness audit (bars start at zero, one axis)."
EVIDENCE: The two named criteria are specified and hold. §5 audit table: "Bar Y axis always includes 0: min = min(0, data min), max = max(0, data max). No grace, no log scale." "Exactly one Y axis and one X axis, one series, no right-hand axis, no secondary series, no legend." Non-zero line baselines are labelled (DS-07). No rows are dropped. Sort and cap are disclosed in the caption.
The audit is not complete, though. The chart has no defined mapping for:
- repeated X categories (N bars with one label, or no aggregate), and
- null Y values (drawn as zero, or as a gap, which is not stated).
Both bear directly on the truthfulness of the bar length, which is the thing the audit is meant to check. Under the rule "every returned row is plotted", a null-Y row drawn at zero is a measured zero that does not exist. This is a Critical principle violation (Cairo 2019, truthful encoding) that the spec leaves open, not a visible violation.
VERDICT:  FAIL

### DW-4.3
PREMISE:  "data ink uses the series-1 blue only, never the accent."
EVIDENCE:
- §5 ink table: "Bars, line, scatter points: `--data-1` (#2a78d6) only." "Histogram and top-value bars in the panel: `--data-1`." §4: "Bars use `--data-1` only."
- §5 "The accent never encodes data: no accent bar, no highlighted bar for the selected column, no accent line. The selected column is shown in the grid only."
- §4 column-details glyph: "mini-bars glyph in `--text-muted` (never `--data-1`)."
- The only accent use in the grid is selection and focus (`--accent-selected`, `--focus`, §3), which is not data ink.
- Contrast, recomputed from the DESIGN.md hex values (sRGB relative luminance): `--data-1` #2a78d6 on `--background` #fcfdfc = **4.33:1** (matches the spec); on `--surface` #f8f9f8 = **4.18:1** (matches). `--text-muted` (neutral-11 #5e6562) on `--background` = **5.86:1** (matches). `--border-control` on `--background` is 3.35:1 by a sRGB approximation of the oklab mix, against the spec's 3.39:1. Either value clears the 3:1 bar for axis and control boundaries.
VERDICT:  PASS

**All requirements met:** NO

## Edge cases — verdicts
| Case | Handled? | Note |
|------|----------|------|
| All-null column | FAIL (chart-as-X) | Grid and panel specified; chart-as-X contradicts §5 |
| Single distinct value | FAIL (chart-as-X) | Grid and panel specified; chart-as-X contradicts §5 |
| Mixed numeric and text | PASS | DS-03, MC-66, excluded from Y, no sort or chart numeric implication |
| 1,000-row truncation | PASS | MC-45, MC-50, MC-63, caption disclosure, CSV scope |
| Zero rows | PASS with Major gap | Kind for zero-row columns undefined; behavior otherwise specified |

## Notes (non-blocking)
- No screenshot, so pixel-level claims (density, sticky header, scroll cues) are noted, not verified.
- Doctrine coverage: `interaction.md` was applied to the state lifecycle only (headings and definitions read). `content-design` was not applied to the §9 strings beyond format.
- The §2 density arithmetic was checked: 40+16+82+16+144+16+574+12 = 900; 532 − 36 header = 496 = 15 full rows + 16 px. Consistent.
- Row-count variants in §2 (18 rows Ask off, 14 with strip) are consistent with the 32 px row height.

## Issues (if FAIL)
1. **Chart row-to-bar mapping is contradictory and undefined for repeated X values.** §5 says every row is plotted; §7 says all-null X gives "a single bar" and single-distinct X gives "one category". Duplicate X labels have no rule. — Severity: Critical / Pillar: data-viz / Principle: truthful encoding (Cairo 2019), one mark per datum (Munzner 2014) / Fix: choose per-row bars with disclosure, or an explicit aggregate named on the axis and in the caption; rewrite the two §7 rows to match.
2. **Null Y values have no rule.** A null-Y row could be drawn as a zero bar, which encodes a missing value as a measured zero. — Severity: Critical / Pillar: data-viz / Principle: truthful encoding (Cairo 2019); absence vs zero (Tufte 1983) / Fix: no bar for null Y; caption discloses the excluded count.
3. **Zero-row kind is undefined.** The kind rule's vacuous truth types every zero-row column `null`. — Severity: Major / Pillar: usability / Principle: internal consistency; Nielsen #1 / Fix: define the zero-row kind (or no hint) in §1 and §3.

**Verdict: FAIL — blockers: DW-4.1 (chart-as-X rows for all-null and single-distinct contradict the per-row rule, §5 vs §7); DW-4.2 (null-Y and repeated-category truthfulness undefined, Critical).**

DESIGN-REVIEW FAIL. Report written to /Users/gabriel/code/cloudstone/.design-foundations/build/2026-10-13-cloudstone-workbench-phase-4-review.md
