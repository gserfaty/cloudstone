# Design: Verdigris Ledger
**Date:** 2026-10-13 · **Status:** converged — pending user lock at mock gate (DW-2.7). Not law until the user signs off on the styled mock; after that, deviations need an edit here first.
**Archetype:** Sage, inflected by Ruler · **Register:** calm product structure · expressive at: the focused region's legend, the run status line, empty states (all low amplitude)
**Grounding:** 1920s Art Deco metalwork's verdigris patina on stone + the bank ledger's ruling (hairline rows, double rule under the header)
**DNA:** Art Deco / Luxury (restrained end) + motion from Swiss / International + type voice from Data-Dense Professional · **Dominant axis:** composition (the ruling system)
**Composition:** Ledger Grid (dealer hand: family `art-deco-luxury` × discipline `ledger-grid`, variance 2, hue 165.61; seed `cloudstone|2026-10-13|1`, i.e. `--reroll 1` after round 0's five hues all collided with a functional color or with series-1). Ledger: `.design-foundations/used-dna.json`.
**Pins:** none from the user (light-only is a plan constraint, not a dealer axis). One converge-time swap, pending the user at the mock gate: signature `duotone-images` (no imagery in this product) → `border-interrupt-headings` (dealt to round 1, hand 2). Phase 2 discovery: `.design-foundations/build/2026-10-13-cloudstone-workbench-phase-2-discovery.md`.

## Direction

A ledger kept in good ink. Stone-grey paper, hairline rules and figures in a mono hand. One patina-green accent shows where the analyst is working and what will run. It serves SQL analysts in long keyboard sessions: the grid's ruling carries the structure, so the chrome can go quiet. That suits a tool whose content *is* rows and columns. Art Deco shows up only in its disciplined parts: fine rules, letterspaced caps labels and one metallic accent. Its ornament, symmetry and slow motion stay out.

## Signature move

**Legend labels on the rule.** Every region that groups content (Ask, Worksheet, Results, the column panel, Example queries, each dialog) is framed by a 1 px `--border` hairline. Its label sits *on* the top rule and interrupts it, like the legend on a map frame:

- Label: Archivo 600, 12 px, uppercase, `letter-spacing: .08em`, `--text-muted`. It's a real heading (`h2`, or a dialog's labelled title).
- Placement: left-aligned at a 12 px inset, with 8 px of the region's own background on each side to break the rule. Built with `fieldset`/`legend` geometry, or a positioned heading over the `border-top`.
- It replaces card headers and card shadows. There are no other region headers and no nested frames: the column panel inside Results is split off by a vertical hairline, not a second frame.
- Live state: while focus is inside a region (`:focus-within`), its legend turns `--accent-text` and the 24 px of rule to the legend's left turns `--accent-edge`. Only one region shows it at a time. It tells a keyboard user where they are.

## Expressive moments

Everything else holds the calm structure register.

1. **Focused region's legend** (the signature's live state). Amplitude: a color change on a 12 px label and a 24 px rule segment, 100 ms opacity crossfade.
2. **Run status line** in the Results header (`✓ 1,000 rows · 84 ms`, `✗ Binder error`). On completion it fades in over 150 ms. The figures are set in Plex Mono and the glyph in the functional `-11` color. No toast for a normal run.
3. **Empty states** (no rows, no history, nothing to chart). The message sits on three faint ledger rules (`--rule`), like a blank ledger page. No illustration, no icon tile.

## Type

- **UI:** Archivo (Google Fonts, Omnibus-Type). Stack: `"Archivo", ui-sans-serif, system-ui, sans-serif`. A grotesque built for screen and print, with a good x-height at 12–14 px. It replaces Inter (an ai-tells High flag).
- **SQL and data:** IBM Plex Mono (Google Fonts). Stack: `"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace`. Used for the editor, every grid cell, column types, figures in status lines and history. Mono numerals are tabular by construction. Elsewhere, UI numbers get `font-variant-numeric: tabular-nums`; if Archivo's `tnum` isn't honored, those numbers fall back to the mono stack.
- **Load:** `https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap`. Offline, the system stacks above take over (plan, Phase 5 edge case).
- **Pairing:** a contrast of roles (prose vs code), not two sans-serifs in the uncanny middle. Never a third family.
- **Scale (px / line-height):** 12/16 (labels, legends, meta, column types) · 13/20 (grid cells, explorer, history, secondary UI) · 14/20 (body, inputs, editor) · 16/24 (Ask input, dialog body lead) · display **20/28** (dialog titles and empty-state headings only; Archivo 600, `letter-spacing: -.01em`). There are no other sizes.
- **Weights:** 400 for text, 500 for buttons only, 600 for legends, headings and the wordmark. No other weights, and no faux bold or faux italic. The `null` token uses Plex Mono 400 italic (the real italic file, added to the font URL in Phase 5 as `ital,wght@0,400;0,500;1,400`).
- **Wordmark:** "CLOUDSTONE" in Archivo 600 at 13 px, uppercase, `letter-spacing: .16em`, `--text`. Set in the same voice as the legends.
- **Alignment:** flush-left everywhere. Numbers are right-aligned in the grid.

## Color tokens

Light only (plan constraint). There's one accent hue (165.61, verdigris) on stone-tinted neutrals of the same hue, and the scheme is monochromatic. The values come from `palette.mjs`:

- Neutrals and accent: `--seed 165.61 --chroma muted --harmony mono --scheme light`.
- Functional colors: the same seed with `--chroma balanced`. That keeps success clearly more saturated than the muted accent.

`.design-foundations/build/phase-2-tokens.mjs` assembles both runs, adds the aliases that `palette.mjs` doesn't emit (`--text-muted`, `--focus`, `--border-control`, `--accent-selected`, `--accent-edge`, `--rule`), checks every pair and exits non-zero on any failure. `--data-1` is series-1, which the plan pins. It's data ink only (charts and the column panel's bars) and never UI.

```css
:root {
  --neutral-1: #fcfdfc;
  --neutral-2: #f8f9f8;
  --neutral-3: #eef1f0;
  --neutral-4: #e4e9e7;
  --neutral-5: #d9e0dd;
  --neutral-6: #ccd4d1;
  --neutral-7: #bdc6c1;
  --neutral-8: #a3aea8;
  --neutral-9: #adbbb5;
  --neutral-10: #9ba8a2;
  --neutral-11: #5e6562;
  --neutral-12: #2b2f2d;
  --accent-1: #fafefc;
  --accent-2: #f4fbf7;
  --accent-3: #e6f5ee;
  --accent-4: #d9eee4;
  --accent-5: #c9e6d8;
  --accent-6: #b7dccb;
  --accent-7: #a2cfbb;
  --accent-8: #82b9a1;
  --accent-9: #84c8ab;
  --accent-10: #74b499;
  --accent-11: #486c5d;
  --accent-12: #20322a;
  --accent-on-solid: #05100b;
  --accent-bg-subtle: var(--accent-3);
  --accent-solid: var(--accent-9);
  --accent-solid-hover: var(--accent-10);
  --accent-text: var(--accent-11);
  --error-3: #ffebe9;
  --error-9: #e1524f;
  --error-11: #974843;
  --success-3: #e0f8e0;
  --success-9: #5ad664;
  --success-11: #337437;
  --warning-3: #f9f0dd;
  --warning-9: #dbb155;
  --warning-11: #76602f;
  --info-3: #e3f3ff;
  --info-9: #5baee5;
  --info-11: #3d6886;
  --background: var(--neutral-1);
  --surface: var(--neutral-2);
  --surface-hover: var(--neutral-3);
  --surface-active: var(--neutral-4);
  --rule: var(--neutral-5);
  --border-subtle: var(--neutral-6);
  --border: var(--neutral-7);
  --border-strong: var(--neutral-8);
  --border-control: color-mix(in oklab, var(--neutral-11) 45%, var(--neutral-8));
  --text: var(--neutral-12);
  --text-secondary: var(--neutral-11);
  --text-muted: var(--neutral-11);
  --accent-selected: var(--accent-4);
  --accent-edge: var(--accent-11);
  --focus: var(--accent-11);
  --data-1: #2a78d6;

  /* type */
  --font-ui: "Archivo", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --text-12: 12px; --lh-12: 16px;
  --text-13: 13px; --lh-13: 20px;
  --text-14: 14px; --lh-14: 20px;
  --text-16: 16px; --lh-16: 24px;
  --text-20: 20px; --lh-20: 28px;
  --tracking-label: .08em; --tracking-wordmark: .16em;

  /* space (4 px grid) */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px;
  --row-h: 32px; /* grid rows */

  /* shape + depth */
  --radius-control: 2px; --radius-float: 4px; /* grid cells and region frames: 0 */
  --hairline: 1px solid var(--border);
  --shadow-float: 0 1px 2px color-mix(in oklab, var(--neutral-12) 8%, transparent),
                  0 8px 24px color-mix(in oklab, var(--neutral-12) 14%, transparent);
  --focus-ring: 2px solid var(--focus); --focus-offset: 2px;

  /* motion */
  --dur-1: 100ms; --dur-2: 150ms;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in: cubic-bezier(0.7, 0, 0.84, 0);
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}
```

**How the tokens are used:**

| Role | Token(s) | Notes |
|---|---|---|
| Page background | `--background` | Stone paper. Never `#fff`. |
| Sidebar, results header, column panel | `--surface` | One step off the page. Hover uses `--surface-hover`, pressed uses `--surface-active`. |
| Grid row rules | `--rule` | One hairline per row; no zebra striping. |
| Header bottom rule | `--border-strong` | The ledger double rule: two 1 px lines 2 px apart (`border-bottom: 3px double`). |
| Region frames, dividers | `--border`, `--border-subtle` | Decorative separators. WCAG 1.4.11 doesn't apply because no control is identified by them. |
| Inputs, selects, secondary buttons, checkboxes | `--border-control` | 3.39:1 on `--background`, mixed from palette steps 11 and 8. |
| Primary action (Run, a dialog's submit) | fill `--accent-solid`, 1 px edge `--accent-edge`, label `--accent-on-solid` | A pale verdigris plate with a deep edge and ink label. There's exactly one per view. |
| Focus | `--focus-ring` + `--focus-offset` | 2 px, offset 2 px, on every focusable element. The grid's focused cell gets an inset 2 px ring. |
| Selection | `--accent-selected` fill | Selected explorer item, history item, sorted column header and current row. Text stays `--text`. |
| Links, active tab label, legend live state | `--accent-text` | Links are always underlined. |
| Status | `--{error,success,warning,info}-11` text and glyph on `-3` fill | Always glyph + words (✓ ✗ ⚠ ⓘ), never color alone. The `-9` steps are borders and indicator bars only, never text or a lone icon. |
| Muted text, placeholders, column types, `null` | `--text-muted` | |
| Chart and column-panel bars | `--data-1` | Data only. The accent never encodes data. |

Don't use `--neutral-9` or `--neutral-10`. Because of how `palette.mjs` places its step-9 cusp, they're lighter than step 8.

**Accent budget:** under 5% of the screen at 1440×900 (checked in Phase 5, DW-5.6). The accent appears only on the primary action, focus, selection and the focused legend.

**Contrast:** `palette.mjs` exits 0 on both runs. Its own report for the muted run is all PASS: neutral-11 on neutral-2 is 5.65:1, neutral-12 on neutral-2 12.88:1, accent-11 on neutral-2 5.46:1, and accent-on-solid on accent-9 10.2:1. The check script's full report (exit 0):

```
PASS  --text #2b2f2d on --background #fcfdfc: 13.31:1 (target 4.5:1)
PASS  --text-muted #5e6562 on --background #fcfdfc: 5.86:1 (target 4.5:1)
PASS  --accent-text #486c5d on --background #fcfdfc: 5.75:1 (target 4.5:1)
PASS  --text #2b2f2d on --surface #f8f9f8: 12.86:1 (target 4.5:1)
PASS  --text-muted #5e6562 on --surface #f8f9f8: 5.66:1 (target 4.5:1)
PASS  --accent-text #486c5d on --surface #f8f9f8: 5.56:1 (target 4.5:1)
PASS  --text #2b2f2d on --surface-hover #eef1f0: 11.94:1 (target 4.5:1)
PASS  --text-muted #5e6562 on --surface-hover #eef1f0: 5.26:1 (target 4.5:1)
PASS  --accent-text #486c5d on --surface-hover #eef1f0: 5.16:1 (target 4.5:1)
PASS  --text #2b2f2d on --surface-active #e4e9e7: 11.06:1 (target 4.5:1)
PASS  --text-muted #5e6562 on --surface-active #e4e9e7: 4.87:1 (target 4.5:1)
PASS  --accent-text #486c5d on --surface-active #e4e9e7: 4.78:1 (target 4.5:1)
PASS  --text #2b2f2d on --accent-bg-subtle #e6f5ee: 12.06:1 (target 4.5:1)
PASS  --text-muted #5e6562 on --accent-bg-subtle #e6f5ee: 5.31:1 (target 4.5:1)
PASS  --accent-text #486c5d on --accent-bg-subtle #e6f5ee: 5.21:1 (target 4.5:1)
PASS  --text #2b2f2d on --accent-selected #d9eee4: 11.18:1 (target 4.5:1)
PASS  --text-muted #5e6562 on --accent-selected #d9eee4: 4.92:1 (target 4.5:1)
PASS  --accent-text #486c5d on --accent-selected #d9eee4: 4.83:1 (target 4.5:1)
PASS  --accent-on-solid #05100b on --accent-solid #84c8ab: 9.98:1 (target 4.5:1)  (primary button label)
PASS  --accent-on-solid #05100b on --accent-solid-hover #74b499: 8.04:1 (target 4.5:1)  (primary button hover)
PASS  --error-11 #974843 on --background #fcfdfc: 6.20:1 (target 4.5:1)
PASS  --error-11 #974843 on --surface #f8f9f8: 5.99:1 (target 4.5:1)
PASS  --error-11 #974843 on --error-3 #ffebe9: 5.51:1 (target 4.5:1)
PASS  --success-11 #337437 on --background #fcfdfc: 5.58:1 (target 4.5:1)
PASS  --success-11 #337437 on --surface #f8f9f8: 5.39:1 (target 4.5:1)
PASS  --success-11 #337437 on --success-3 #e0f8e0: 5.05:1 (target 4.5:1)
PASS  --warning-11 #76602f on --background #fcfdfc: 5.91:1 (target 4.5:1)
PASS  --warning-11 #76602f on --surface #f8f9f8: 5.71:1 (target 4.5:1)
PASS  --warning-11 #76602f on --warning-3 #f9f0dd: 5.32:1 (target 4.5:1)
PASS  --info-11 #3d6886 on --background #fcfdfc: 5.85:1 (target 4.5:1)
PASS  --info-11 #3d6886 on --surface #f8f9f8: 5.65:1 (target 4.5:1)
PASS  --info-11 #3d6886 on --info-3 #e3f3ff: 5.26:1 (target 4.5:1)
PASS  --focus #486c5d on --background #fcfdfc: 5.75:1 (target 3:1)
PASS  --focus #486c5d on --surface #f8f9f8: 5.56:1 (target 3:1)
PASS  --focus #486c5d on --surface-hover #eef1f0: 5.16:1 (target 3:1)
PASS  --focus #486c5d on --accent-bg-subtle #e6f5ee: 5.21:1 (target 3:1)
PASS  --focus #486c5d on --accent-selected #d9eee4: 4.83:1 (target 3:1)
PASS  --focus #486c5d on --accent-solid #84c8ab: 3.03:1 (target 3:1)  (ring offset 2px sits on background; checked against fill too)
PASS  --border-control #838c88 on --background #fcfdfc: 3.39:1 (target 3:1)
PASS  --accent-edge #486c5d on --background #fcfdfc: 5.75:1 (target 3:1)  (primary button edge)
PASS  --border-control #838c88 on --surface #f8f9f8: 3.28:1 (target 3:1)
PASS  --accent-edge #486c5d on --surface #f8f9f8: 5.56:1 (target 3:1)  (primary button edge)
PASS  --error-11 #974843 on --background #fcfdfc: 6.20:1 (target 3:1)  (status glyph)
PASS  --success-11 #337437 on --background #fcfdfc: 5.58:1 (target 3:1)  (status glyph)
PASS  --warning-11 #76602f on --background #fcfdfc: 5.91:1 (target 3:1)  (status glyph)
PASS  --info-11 #3d6886 on --background #fcfdfc: 5.85:1 (target 3:1)  (status glyph)
PASS  accent hue 165.7 vs series-1 #2a78d6 hue 255.5: delta 89.8 deg (target >= 40)
INFO  accent-text oklch(0.499 0.048 166.6) vs success-11 oklch(0.501 0.115 144.8): dE_ok 0.072
```

## Space, shape, depth

- **Spacing:** a 4 px grid with steps 4 / 8 / 12 / 16 / 24 / 32 / 48. Spacing is tight inside a group (4–8) and generous between regions (16–24). Grid rows are 32 px: a 20 px line plus 6 px of padding top and bottom, with 13 px Plex Mono cells. That's a 1440×900 viewport fitting at least 15 rows with the editor at its default height.
- **Radius:** 0 for region frames, grid cells and the top bar. 2 px for controls (inputs, buttons, chips, tabs). 4 px for floating layers (popover, dialog, toast, menus). Nothing is pill-shaped except the existing count badges, which become 2 px rectangles too.
- **Structure:** 1 px hairlines carry all structure: region frames with their legends, row rules, the double rule under the header, and the vertical split between the grid and the column panel. Regions have no shadows and no filled card backgrounds beyond `--surface`.
- **Depth:** only floating layers are raised. Popovers, dialogs, toasts and menus use `--shadow-float`, a two-layer shadow mixed from `--neutral-12` (hue-shifted green-grey, never black). A dialog's backdrop is `--neutral-12` at 40%. There are just two depth levels: the page and things floating over it.
- **Top bar:** `--background`, closed by a `--border` hairline. The navy bar goes. The wordmark sits left and the account controls right.

## Motion

- **Timing:** 100 ms for micro changes (hover, pressed, legend live state, tab underline) and 150 ms for standard ones (popover, dialog, toast, the status line fading in, the column panel opening). Nothing runs longer than 150 ms.
- **Easing:** `--ease-out` for things entering and `--ease-in` for things leaving. There's no bounce and no overshoot.
- **Allowed:** opacity and transform only. Popovers and dialogs scale from 0.98 plus a fade; toasts translate 4 px plus a fade; the column panel translates 8 px from the right plus a fade. Each motion answers "what changed?".
- **Never:** animating width, height, margin, top or left; ambient or looping motion (the only exception is the existing Run/Ask busy indicator, which reduced-motion makes static); staggered list reveals; motion on scroll; hover effects on grid cells.
- **prefers-reduced-motion:** durations drop to about 0 through the global query in the token block. State changes stay visible because they're carried by color and position, not motion.

## Never (this project's tells at risk)

- Inter, Roboto, Open Sans, system-ui or Space Grotesk as the primary face. No third font family.
- Snowflake blue or a navy top bar. Never use `--data-1` or any blue as a UI color: blue is data.
- A second accent hue, gradients, glows, glassmorphism or gradient text.
- Cards inside cards. The column panel, notices and the chart controls live inside the Results frame, separated by hairlines, never as nested framed boxes.
- Uniform soft shadows on regions. Shadows belong only to floating layers.
- Color-only status. Every status pairs a glyph with words.
- The accent on data, on decoration, or on more than one primary action per view.
- Mono used as decoration. Mono is for SQL, cells, types and figures only.
- Centered text blocks. Bounce or elastic easing, or anything over 150 ms.
- Art Deco temptations the family invites: symmetry, ornament, gold or brass, display serifs, slow reveals.
- Em-dash-heavy or buzzword microcopy (Phase 3 owns the words).

## Open questions

- **For the user at the mock gate (DW-2.7):** confirm the dealt direction and the one converge-time swap (signature `duotone-images` → legend labels). If they reject it, re-deal with `--reroll 2`; never hand-edit the hand.
- **Accent vs success:** both sit on the green side of the wheel. They're held apart by chroma (accent C 0.048, success C 0.115), by hue (Δ 22°, ΔE_ok 0.072), by role (accent is never a status) and by the mandatory ✓ glyph. Check on the mock that a ✓ status never reads as "selected". If it does, the fallback is a user-requested hue swap, not a quiet edit.
- **Info vs data:** `--info-11` (hue about 240) is near the series-1 data blue. Info notices sit in the notice strip, never inside a chart. Phase 4/5 should confirm they don't touch.
- **Archivo `tnum`:** confirm in Phase 5 that the Google Fonts subset honors `font-variant-numeric: tabular-nums`. If it doesn't, UI figures switch to `--font-mono`.
- **Legend over the editor:** the Worksheet legend sits above the line-numbered editor's gutter. Check on the mock that the gutter and the legend inset (12 px) line up on one vertical.
