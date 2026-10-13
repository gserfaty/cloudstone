# Discovery + Design: Phase 2 - Visual identity and tokens

## Artifacts Found / Current State

- `DESIGN.md`: absent. This phase establishes it.
- `JOURNEY.md`: present (Phase 1, committed 7ffd640). Regions R1-R16, flows F1-F5. Style-free, so it constrains surfaces, not looks.
- `index.html` today: Inter + JetBrains Mono, navy top bar (`--navy #102a43`), Snowflake blue accent `#1a6ce7`, cyan brand `#29b5e8`, soft shadows on cards. The user called this generic; `ai-tells` flags Inter as primary (High).
- Dealer ledger: none before this phase. Created at `.design-foundations/used-dna.json`.
- Binding inputs: plan `## Constraints` (light only; one file; Google Fonts only; series-1 `#2a78d6` stays the data color; taste pins), research "Decisions (researcher defaults)": scale 12/13/14/16, 4 px grid, motion <= 150 ms opacity/transform only, hairlines over shadows (shadows only on floating layers), accent coverage < 5 %, weights 400/600 (+500 buttons).

## Gaps

1. `palette.mjs` emits `--text-secondary` but not `--text-muted` or `--focus` (DW-2.2 needs both). Add as aliases onto palette steps.
2. `palette.mjs` has no step that is a 3:1 control boundary on the light background (neutral-8 is about 2.2:1). Needs a derived `--border-control` (DW-2.6), mixed from two palette steps, not a hand-picked hex.
3. `palette.mjs` reports no functional-color pairs. Functional text pairs need their own check (DW-2.5).
4. Every functional hue in `palette.mjs` is fixed (error 25, warning 85, success 145, info 240). Any dealt accent near one of those reads as status. This turned out to decide the convergence (below).

## Gate Status

- JOURNEY.md page spec present: YES (prerequisite met).
- DESIGN.md: produced by this phase, status "converged, pending user lock at mock gate". DW-2.7 is left open by design; the lock happens on the styled mock.
- Non-interactive dispatch: pins come only from the research doc / plan. The taste signals (light only; Snowsight structural only; calm, no gradients) do not map to a dealer axis, so no `--pin` was passed.

## Register and archetype

- Personality words from the brief: precise, calm, trustworthy, fast, never decorative. Part C maps "smart, precise, rigorous" to **Sage / Ruler** and "calm, trustworthy, reliable" to Caregiver. Primary: **Sage**, inflected by **Ruler** (authority over the numbers). Caregiver rejected: its soft rounded visual gravity fights "precise".
- Structure register: product, calm baseline (grid, editor, explorer, forms). Expressive moments: few and small (see DESIGN.md).

## Deal, critique, converge (design-dna pipeline)

### Round 1: `dealer.mjs --project cloudstone --date 2026-10-13 --candidates 5` (seed `cloudstone|2026-10-13|0`)

Grounding pairs are disjoint across all ten candidates (two rounds).

| # | Hand (family x discipline, hue, signature) | Grounding | Distinctiveness | Register fit | Tells / hard constraints | Verdict |
|---|---|---|---|---|---|---|
| 1 | Neo-Brutalist x Swiss Modular (v3), blue 242, hard-offset-shadow | Swiss railway timetables' modular grid + Mute zine covers' hard shadows | Blue 242 is the Snowflake blue the user rejected | Offset shadows contradict "hairlines over shadows" | **Fails DW-2.8**: hue delta to series-1 (OKLCH 255.5) is 13 deg | Weak. Strongest element: Swiss Modular discipline |
| 2 | Playful Geometric x **Ledger Grid** (v2), "orange" 20, logo-polygon-mask | Double-entry ledger books' ruling + Memphis Group's flat marker shapes | Ledger Grid is the most content-derived discipline in the deal: the table is the dominant element | Family's springy, multi-hue defaults fight "calm" | **Accent collides with error**: palette run gives accent-9 `#e0515b` vs error-9 `#e1524f`; red accent in an analytical tool is a ch09 Critical flag. Signature needs images; there are none | Strongest composition, unusable hue |
| 3 | Warm Editorial x Split Stage (v6), green 157, accent-scarcity | Penguin paperback spines + Muji store signage | Split Stage restates the fixed sidebar/main split | Warm humanist reading voice suits prose, not a grid | Green 157 vs success 145 (12 deg); cream-editorial cluster risk | Strongest signature (accent scarcity matches the < 5 % budget) |
| 4 | Art Deco x Fractured Grid (v9), violet 295, baseline-ruler | Chrysler lobby metalwork + Gerstner's Programme fractured layouts | Fractured Grid (v9) breaks tabular reading | Transactional UI pushes away from Art Deco + v9 | Violet 295 sits in the purple-triplet tell zone (`#8B5CF6` is ~293) and misses DW-2.8 (39.5 deg) | Weak. Signature fits the line-numbered editor |
| 5 | Retro-Futurist x Editorial Spread (v7), yellow 72, exposed-grid | Braun ET66 calculator + 1990s Wired spreads | Oversized display type cannot live in a 12-16 px scale | Retro-Futurist pushed away by transactional UI | Yellow 72 vs warning 85 (13 deg); fails as text | Weak. Exposed grid is apt for a grid tool |

Critique finding: the five hues all land on a functional hue or on series-1. That is clustering on a failure, so the doctrine's **loop back once** applies: a fresh deal with `--reroll 1` (both deals kept in `used-dna.json`; round-1 cells now excluded).

### Round 2: `--reroll 1` (seed `cloudstone|2026-10-13|1`)

| # | Hand | Grounding | Distinctiveness | Register fit | Tells / hard constraints | Verdict |
|---|---|---|---|---|---|---|
| 1 | **Art Deco x Ledger Grid** (v2), teal 165.6, duotone-images | Verdigris copper of 1920s Deco fittings + bank-ledger ruling | Ledger Grid again, now under a Ruler family; verdigris on stone grey is far from every catalogued cluster | Ruler fits "authority over the numbers"; Art Deco's fine rules and letterspaced caps label survive at the restrained end; its slow motion does not (borrow motion) | Hue delta to series-1 = 89.8 deg (passes DW-2.8). Near success 145 (20 deg): separable by chroma (accent muted, success balanced) plus the mandatory check-mark glyph. Signature needs images | **Strongest overall** |
| 2 | Warm Editorial x Swiss Modular (v3), purple 303, border-interrupt-headings | Ordnance Survey map frames + Monocle's section heads | Purple 303 = purple-500 `#A855F7` tell (~304) | Fine | High tell on hue | Strongest signature of round 2 (legend headings) |
| 3 | Organic x Monolith Center (v1), yellow 80.6, accent-scarcity | Field-guide plates + Kinfolk centered pages | Centered single axis wastes width a grid needs | Organic pushed away by dense tables | Yellow vs warning 85 (4 deg) | Weak |
| 4 | Playful Geometric x Editorial Spread (v7), cyan 218, exposed-grid | Bauhaus toy blocks + Emigre spreads | Oversized display again | Fights calm | **Fails DW-2.8** (37.5 deg) | Weak |
| 5 | Neo-Brutalist x Frieze Bands (v4), red 355.6, marginalia-stamps | Customs-stamp paperwork + Brutalist concrete friezes | Stamps would suit history status | Bands fight one-screen density | Red vs error 25 (29 deg); red in analytics | Weak. Stamps are a good idea for history |

### Converge: synthesis (pending the user's pick at the mock gate)

- **Base hand:** round 2 #1, **Art Deco x Ledger Grid, hue 165.61 (verdigris)**, executed as dealt. The (family, discipline) cell and the hue are not edited.
- **Borrowed axes (remix rule: 1-2):** motion from **Swiss** (100-150 ms, sharp ease-out; the research cap is 150 ms) and type voice from **Data-Dense Professional** (compact grotesque + mono numerals). Color strategy stays Art Deco (deep stone base + one metallic accent: verdigris *is* the metal's patina). Composition is the dealt cell. Dominant axis: **composition** (the ruling system).
- **Signature swap:** the dealt `duotone-images` cannot execute (no imagery in the product). Synthesis takes round 2 #2's deck signature **border-interrupt-headings**: it is the strongest signature across both rounds and it executes Art Deco's letterspaced-caps labels on Ledger Grid's hairlines. Recorded as a converge-time swap pending the user (Pins line).
- **Chroma:** muted for neutrals + accent (Art Deco's controlled chroma; "calm"), balanced for functional colors so success stays clearly greener and more saturated than the accent. Both runs are `palette.mjs`.
- **Two-word name:** Verdigris Ledger.
- **Critique line on the synthesis:** strongest = the ruling system + legend labels read as one authored idea derivable from "ledger of query results"; weakest = accent and success share the green-blue side of the wheel, held apart only by chroma and lightness plus glyphs (measured, see evidence); tells = none hit (no Inter, no purple, no cyan-on-dark, no cards-in-cards, no uniform shadows, light by user decision).

## Design Decisions

- **Type (fonts doctrine):** Archivo (Omnibus-Type; built for screen and print, grotesque structure, good x-height, real 400/500/600 weights) for UI; IBM Plex Mono for SQL and every data cell (mono numerals = tabular by construction; Data-Dense family's listed mono). Pairing is deliberate contrast by role (prose vs code), not two sans in the uncanny middle. Replaces Inter (ai-tells High) and JetBrains Mono. Labels: Archivo 600 caps, tracked +0.08 em (the Art Deco carry-over). Scale 12/13/14/16 + display 20.
- **Color (color doctrine):** monochromatic scheme on hue 165.61 (calm/focused per ch09), stone-tinted neutrals, one accent. Functional colors follow convention (red error, green success, amber warning, blue info), each always paired with a glyph (ch08 redundant cue). Shadows hue-shifted from neutral-12, never black (ch09).
- **Motion:** state-change only, 100/150 ms, opacity + transform, no bounce, reduced-motion zeroes durations.
- **Tools reused:** `dealer.mjs` (deal), `palette.mjs` (both ramps), one small check script for the pairs `palette.mjs` does not report.

## DW Verification

| DW-ID | Done-When Item | Status | Evidence |
|-------|---------------|--------|----------|
| DW-2.1 | DESIGN.md with Direction, Signature move, Type, Color tokens, Space/shape/depth, Motion, Never | COVERED | Section headings present in `DESIGN.md` (grep) |
| DW-2.2 | Aliases `--background --surface --text --text-muted --border --accent-solid --accent-text --focus` resolve | COVERED | Token block; check script resolves every alias to a hex |
| DW-2.3 | Type scale 12/13/14/16 (+ display) | COVERED | `DESIGN.md` Type + `--text-12..--text-20` tokens |
| DW-2.4 | `--error/success/warning/info-*` defined | COVERED | Token block (-3/-9/-11 for each, from `palette.mjs`) |
| DW-2.5 | All text/background pairs >= 4.5:1 | COVERED | `palette.mjs` contrast report (exit 0) + check script for functional and alias pairs (exit 0) |
| DW-2.6 | Focus ring and control boundaries >= 3:1 | COVERED | Check script: `--focus` and `--border-control` vs background/surface |
| DW-2.7 | User confirms on the styled mock, then DESIGN.md is locked | OPEN BY DESIGN | Not this phase: the mock gate right after it. DESIGN.md status says so |
| DW-2.8 | Accent hue delta to `#2a78d6` >= 40 deg | COVERED | Check script prints OKLCH hue delta |

**All items COVERED:** YES for DW-2.1-2.6 and 2.8 (7/7 in scope); DW-2.7 is the mock-gate step, left open as instructed.

## Recommendation

BUILD
