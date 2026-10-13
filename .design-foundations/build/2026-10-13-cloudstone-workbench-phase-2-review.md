# Design Review: Phase 2 - Verdigris Ledger tokens (cloudstone workbench)

## Rendered Evidence (Step 0)
- Screenshot: none. Tokens/spec phase, no rendered .html; structure and token-level critique only. Pixel-level hierarchy, spacing and the legend-on-rule geometry are unverified until the mock.
- Surface reviewed: DESIGN.md, .design-foundations/used-dna.json, .design-foundations/build/phase-2-tokens.mjs.

## Assessment B - Deterministic Detector
- Command: node scripts/detect.mjs (no html supplied)
- Exit: 3 (N/A, no rendered artifact). Not a failure.
- Findings: N/A
- Opened only after Assessment A findings were frozen: YES (nothing to open)

## Triage
- Baseline: visual + usability (token-level only)
- Dispatched: color, foundations/type, fonts, motion, archetypes, ai-tells (per prompt doctrine)
- Not applicable: data-viz, content-design, journey, behavioral (no rendered surface)

## Independent recomputation (own script, WCAG 2.x, from the hex values in the :root block)
- --text #2b2f2d: 13.31 bg / 12.86 surface / 11.94 hover / 11.06 active / 12.06 accent-subtle / 11.18 selected
- --text-muted #5e6562: 5.86 / 5.66 / 5.26 / 4.87 / 5.31 / 4.92 (lowest 4.87 on surface-active)
- --accent-text #486c5d: 5.75 / 5.56 / 5.16 / 4.78 / 5.21 / 4.83 (lowest 4.78)
- --accent-on-solid #05100b on --accent-solid #84c8ab 9.98; on hover #74b499 8.04
- Functional -11 on bg and on own -3: error 6.20/5.51, success 5.58/5.05, warning 5.91/5.32, info 5.85/5.26
- --focus #486c5d: 5.75 bg, 5.56 surface, 5.16 hover, 5.21 accent-subtle, 4.83 selected, 3.03 vs accent-solid fill
- --border-control (OKLab mix 45% neutral-11 / neutral-8 = #838c88): 3.39 bg, 3.28 surface, 3.04 on surface-hover
- Accent #84c8ab hue 165.7 vs #2a78d6 hue 255.5: delta 89.8 deg
- phase-2-tokens.mjs re-run: exit 0. All numbers in the document match my recomputation to 2 decimals.
- Dealer reproducibility: `dealer.mjs --project cloudstone --date 2026-10-13 --reroll 1 --used <ledger copy>` reproduces hand 1 (art-deco-luxury x ledger-grid, hue 165.61, 5 exclusions). Ledger matches the DESIGN.md claim.

## Cross-Pillar Findings
| Severity | Pillar | Problem | Principle | Fix |
|----------|--------|---------|-----------|-----|
| Major | design-dna / process | The signature was swapped from the dealt `duotone-images` to hand 2's `border-interrupt-headings`. That is a hand-edit of the dealt hand, while the same document says "never hand-edit the hand". It is disclosed and gated on the user, but the document contradicts itself. | Dealer contract: model executes the dealt hand, re-deals on rejection (`--reroll N+1`) | Keep the swap as an explicit user question at DW-2.7. If declined, re-deal with `--reroll 2`. Reword the Open questions bullet so it does not claim the hand was left unedited. |
| Minor | color | Primary-button focus ring is only 3.03:1 against the solid fill and --border-control is 3.04:1 on --surface-hover. Both pass, with almost no margin. Any hover state tweak or rendering shift can fail them. | WCAG 1.4.11 non-text contrast | Move the ring offset so it sits on --background only, and avoid placing inputs on --surface-hover. Re-run the script when tokens change. |
| Minor | color | --neutral-9/-10 are lighter than -8 (luminance 0.478 and 0.376 vs 0.409). The doc bans them, but they remain in the :root block as trap tokens. | Token hygiene / least surprise | Drop them from the shipped block, or leave an inline comment. |
| Minor | color | Accent-text (C 0.048) and success-11 (C 0.115) are 22 deg apart. The doc discloses this and mitigates with the glyph. | Color-only differentiation (WCAG 1.4.1), Nielsen #4 | Verify on the mock, as the doc already plans. |
| Minor | usability | Selected-state text uses --text-muted at 4.87 on --surface-active, close to the floor. | WCAG 1.4.3 | Acceptable. Watch if any 12px meta text sits on that surface. |
| Note | design-dna (distinctiveness) | Passes the CHECKER test. Direction is nameable in specific words: "verdigris ledger", with legend-on-rule labels, a double header rule and mono figures. Inter, gradients and shadows on cards are all explicitly refused. | ai-tells.md CHECKER mode | None. |

## Requirement Fulfillment
### DW-2.1
PREMISE:  `DESIGN.md` exists with Direction, Signature move, Type, Color tokens, Space/shape/depth, Motion and Never sections.
EVIDENCE: Headings present in order: Direction, Signature move, Expressive moments, Type, Color tokens, Space, shape, depth, Motion, Never, Open questions. Each section is substantive.
VERDICT:  PASS

### DW-2.2
PREMISE:  all semantic aliases resolve: `--background`, `--surface`, `--text`, `--text-muted`, `--border`, `--accent-solid`, `--accent-text`, `--focus`.
EVIDENCE: All eight are defined in :root and chain to existing palette steps: --background -> neutral-1 #fcfdfc, --surface -> neutral-2 #f8f9f8, --text -> neutral-12 #2b2f2d, --text-muted -> neutral-11 #5e6562, --border -> neutral-7 #bdc6c1, --accent-solid -> accent-9 #84c8ab, --accent-text -> accent-11 #486c5d, --focus -> accent-11 #486c5d. No dangling var() references. The assembly script resolves them and exits 0.
VERDICT:  PASS

### DW-2.3
PREMISE:  the type scale is present (12 / 13 / 14 / 16, plus any display step).
EVIDENCE: --text-12/13/14/16 with line-heights 16/20/20/24, plus a 20/28 display step. Declared in both prose and tokens.
VERDICT:  PASS

### DW-2.4
PREMISE:  functional colors `--error/success/warning/info-*` are defined.
EVIDENCE: -3, -9 and -11 steps defined for all four (e.g. --error-11 #974843, --success-9 #5ad664). Each has a documented role: -3 fill, -9 border/indicator, -11 text/glyph.
VERDICT:  PASS

### DW-2.5
PREMISE:  all text/background pairs pass AA (>= 4.5:1 body), checked with `palette.mjs`.
EVIDENCE: Recomputed independently (see section above). Minimum body-text pair is accent-text on surface-active at 4.78:1. All functional text pairs are at or above 5.05. The script uses palette.mjs output and exits 0. The accent fails nothing as text; solid accent is used for fills only, with the ink label at 9.98:1.
VERDICT:  PASS

### DW-2.6
PREMISE:  the focus ring and control boundaries pass >= 3:1.
EVIDENCE: --focus is 4.83 to 5.75 on all page surfaces and 3.03 on the solid fill. --border-control is 3.39 on background, 3.28 on surface and 3.04 on surface-hover. The accent edge is 5.75. Decorative --border (neutral-7) identifies no control, as stated.
VERDICT:  PASS (thin margins noted above)

### DW-2.7
PREMISE:  the user confirms the dealt direction on the styled mock rendered right after this phase, and only then is `DESIGN.md` marked locked.
EVIDENCE: PENDING - out of scope for this review. DESIGN.md correctly states "pending user lock" and is not marked locked.
VERDICT:  PENDING

### DW-2.8
PREMISE:  the accent's OKLCH hue differs from series-1 `#2a78d6` by >= 40 deg, or its chroma/lightness is clearly apart.
EVIDENCE: Accent-solid hue 165.7, series-1 hue 255.5, delta 89.8 deg (recomputed).
VERDICT:  PASS

**All requirements met:** YES (DW-2.7 pending by design)

### Edge cases
- Dealer emits an AI-tell cell, re-deal and never hand-edit: no banned cell was dealt (art-deco-luxury x ledger-grid is not in the dealer's banned list). Round 0 was re-dealt with `--reroll 1`, and both deals are in the ledger. I reproduced the deal. The signature swap is the one hand-edit (see Major finding), disclosed and gated on the user, and it does not concern an AI-tell cell. HANDLED, with the caveat.
- Candidate accent fails AA as text: the solid accent-9 is never used as text. Text uses accent-11 (5.75:1), and the solid step is for fills only, with a dark ink label. HANDLED.

## Notes (non-blocking)
- No screenshot exists. Legend-over-rule geometry, the gutter alignment, whether the pale-plate primary button reads as primary, and the accent-vs-success proximity can only be judged on the mock.
- Light-only is respected: no dark ramp is present.

## Issues (if FAIL)
None blocking.

**Verdict: PASS** (one Major process note for the DW-2.7 gate: the disclosed signature swap contradicts "never hand-edit the hand")
