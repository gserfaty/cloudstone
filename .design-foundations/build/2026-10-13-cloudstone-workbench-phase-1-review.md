# Design Review: Phase 1 - Cloudstone workbench JOURNEY.md

## Rendered Evidence (Step 0)
- Screenshot: none. Spec-only phase; structure-level critique of the source document only. No pixel evidence applies.
- Surface: `/Users/gabriel/code/cloudstone/JOURNEY.md` (324 lines). Single Workbench page (R1-R16), flows F1-F5, journey table, IA tree, Hick/Cowan table, Esc precedence table, responsive rules.
- DESIGN.md: not present at project root. Not reviewed; not required by the DW items.

## Assessment B — Deterministic Detector
- Command: not run. No rendered .html exists for this spec-only phase.
- Exit: 3 N/A (no rendered artifact)
- Findings: N/A — no rendered artifact
- Opened only after Assessment A findings were frozen: YES (N/A, nothing to open)

## Triage
- Baseline (always-on): visual + usability. Visual is N/A for a style-free spec (the file states it is style-free); usability applied to the operability of every region.
- Dispatched: `journey` (the artifact is a JOURNEY.md page-spec + flows + IA; signal present). `usability` (multi-step flows, forms, keyboard model; signal present).
- Not applicable: `data-viz` (no chart encoding specified beyond control set; R13 names no data encoding claims). `content-design` (copy is not finalized; error/empty copy is described, not authored; not reviewed as microcopy). `behavioral` and `deceptive-patterns` (no persuasion surface; Ask cost is noted, not persuasive). `ai-native` (conventional screen UI, the Ask card is a single query box).
- Deferred (if capped): none. The surface was small enough to cover the two dispatched doctrines fully.

## Doctrine applied
- journey: JTBD (Moesta) with one school named; journey loop, not funnel (Google 2020 messy middle); theater-risk flag with owner, basis, cadence present; IA validation owed and flagged honestly; page-spec fields (purpose, entry, content, states, CTA, exit) present for R1-R16.
- usability: Nielsen 1 (visibility of status), 5 (error prevention: Undo, confirm-before-clear), 6 (recognition over recall), 9 (error recovery, SQL kept on failure); Hick and Cowan citations where options are cut; Fitts on Run placement; WCAG 2.2 keyboard and focus rules (2.1.2 no trap with documented exit, 2.4.3 order, 2.5.8 target size).

## Cross-Pillar Findings (ONE ranked report)
| Severity | Pillar | Problem | Principle | Fix |
|----------|--------|---------|-----------|-----|
| Minor | journey | Results-cap guidance is inconsistent: R10 says "add ORDER BY or LIMIT in SQL", F2 step 5 says the notice "suggests `ORDER BY`". LIMIT does not make sorting cover the full result, so the R10 wording is misleading on the exact anxiety the journey names ("Will sorting lie to me when results are capped?"). | Nielsen #1/#2 (honest status), journey anxiety row | Use one wording everywhere: "add ORDER BY in SQL to choose which rows are returned" and drop LIMIT from the sort hint. |
| Minor | usability | Logged-out upload zone label reads "Log in to upload" but the click opens Auth in Sign up mode. Returning users who read the label land on the wrong mode and must switch the segmented control. | Nielsen #4 consistency, #2 match system | Either label it "Sign up to upload" or open in the mode the label names; keep the sign-up route the DW requires. |
| Minor | usability | Upload after sign-up forces the user to repeat the drop because files are not retained (F4 step 3). Defensible as "no hidden state", but it adds a re-do step at the moment of commitment. | Nielsen #7 flexibility/efficiency; Fitts/Hick not involved | Note the trade-off in the spec, or keep the dropped file names in the drop zone until the next drop (session-only, visible). |
| Minor | usability | F3 failure branches list "Ask off" as a request failure, but F3 entry and the Ask-off edge case say the Ask card does not exist when Ask is off. The branch cannot occur. | Internal consistency (spec clarity) | Remove "Ask off" from the F3 step 3 failure list. |
| Minor | journey | F3 step 5 says the refined run is "marked as an edit of an Ask run only by its own SQL (no hidden linkage)". The sentence says both that it is marked and that it is not linked; a reader cannot tell what History shows. | Clarity of the page spec (journey: page spec must define the outcome) | State exactly what History shows for an edited Ask run (for example, no marker; the row carries its own SQL and the Ask line only if it was an Ask run). |
| Minor | journey | R7 error state says "how to fix (Phase 3 words)". "Phase 3" is a build-process label defined nowhere in JOURNEY.md, so the error copy owner and content are unresolved. | Journey: spec must be self-contained (theater/ownership flag) | Replace with "error copy to be written in content-design pass" and name the owner. |
| Minor | usability | R14 Profile "empty" is defined only after an Example query. Typed SQL, a failed query, or a cleared table have no defined current-table state, so the Profile tab's behavior is unspecified. | Nielsen #1; state completeness (DW-1.1) | Define current-table transitions: which actions set it, which clear it, and what R14 shows for ad hoc SQL. |
| Minor | usability | Capped results: the spec does not say what CSV exports (1,000 rows or the full query), and the status format for a capped run ("N rows" in R9) differs from the "1,000+" behavior already in index.html. The job story's trust anxiety is the reason this matters. | Nielsen #1; journey anxiety row | Specify CSV scope and the capped status string ("1,000+ rows") in R9 and R10. |
| Minor | journey | Journey validation is owed and flagged as an open risk (card sort and tree test not run). Honest, but the doctrine says validate before visual design; the spec does not set a gate for it. | Rosenfeld/Morville: sitemap is not IA (journey doctrine) | Add a gate: "IA validated (card sort + tree test) before DESIGN.md is accepted," or record the decision to accept the risk. |
| Minor | journey | JOURNEY.md is linked from DESIGN.md and CLAUDE.md `## Design Context` in the doctrine. DESIGN.md does not exist yet and CLAUDE.md has no Design Context block. | Journey doctrine, JOURNEY.md authoring step H.3 | Add the links when DESIGN.md and the Design Context block are written; record as a dependency. |
| Note | usability | R1 "Tab order brand-less, left to right" is unclear wording; the intent is "brand is not a tab stop". | Clarity | Reword. |
| Note | usability | Explorer column click "inserts at editor cursor" does not say whether focus moves to the editor. | Focus management (WCAG 2.4.3) | State whether focus stays in Explorer. |

## Requirement Fulfillment
### DW-1.1
PREMISE:  "`JOURNEY.md` `## Page specs` has a complete Workbench entry: every region, its states (empty, loading, error, logged out, Ask off) and its keyboard behavior."
EVIDENCE: `## Page specs > Workbench` lists R1-R16 in reading order. Each region has a States line covering empty, loading, error, logged out and Ask off (each either a state or an explicit "n/a" with a reason), and a Keys line. Regions cross-checked against the IA tree: top bar (R1), drop zone (R2), view switch (R3), Explorer (R4), Examples (R5), History (R6), Ask card (R7), Worksheet (R8), Results header (R9), notice strip (R10), grid (R11), column panel (R12), Chart (R13), Profile (R14), dialogs (R15), toasts (R16). The state matrix repeats the same coverage. Gaps only at the level of detail noted in Findings (R14 transitions, R10 wording), not missing regions or states.
VERDICT:  PASS

### DW-1.2
PREMISE:  "the flows cover all five journeys in IN, each ending in a visible outcome. (The five journeys: preview a table; iterate a query; Ask → refine; upload when logged out → sign-up route; rerun from history.)"
EVIDENCE: `## Flows` has F1 Preview a table, F2 Iterate a query, F3 Ask, then refine, F4 Upload when logged out, F5 Rerun from history. Each has an "(Exit) **Outcome (visible):**" line: F1 grid of 100 rows with highlighted table and status; F2 new grid result and new top History row; F3 editable SQL plus results or clear error; F4 auth dialog or signed-in top bar with enabled drop zone; F5 worksheet holds the SQL and a new History row after rerun. Minor concern: F4's Close branch returns to the page with no distinct outcome beyond the restored page; still a visible state.
VERDICT:  PASS

### DW-1.3
PREMISE:  "the regions and states in the page spec cite Hick's law and Cowan's ~4±1 limit where they cut options."
EVIDENCE: Cuts cited: R1 "max 3 targets (Hick)"; R3 "Why (Hick)"; R4 "2 groups (Hick); search carries the long-list case (Hick)"; R5 collapsed for returning users (Hick); R6 "exactly 4 chunks per row" (Cowan) and "one global clear (Hick)"; R7 "4 chips and one primary action (Hick)"; R9 "3 tabs, 2 actions (Hick)"; R12 "four groups" (Cowan); R15 segmented two-mode control (Hick); R16 "Max 3 toasts visible (Hick)". Cut-table at "Where the page cuts options" repeats these. R13 Chart Type (three options) is a choice set not presented as a cut and not listed in the cut table; not a DW failure because the spec does not claim a cut there.
VERDICT:  PASS

## Edge cases
- **Ask off: Ask region hidden and a hint shows.** R7 "absent from the DOM flow (hidden)"; R8 "Ask-off hint slot" in the Worksheet header with the enabling command; F3 "a hint under the Worksheet title." HANDLED. (Note: the hint text itself is not written; the spec says what it contains, not the words.)
- **Logged out: demo tables only, upload routes to sign-up.** R4 shows `my_data` with "Log in to upload..." and demo usable; R8 "only demo tables resolve"; R14 "demo tables only"; R2 click or drop opens Auth in Sign up mode and sends nothing; F4 steps 2-3. HANDLED.
- **Results capped at 1,000 rows: truncation notice and note sorting covers only returned rows.** R10 (a) "Showing the first 1,000 rows" plus "Sorting and column stats cover only these rows"; F2 step 5; R12 "based on N returned rows". HANDLED. Wording inconsistency and CSV scope noted as Minor findings.
- **Empty result and DDL statements that return no result set.** R9 zero rows "0 rows - N ms, CSV enabled (header-only)"; R11 "empty (zero rows): header row plus No rows matched"; R9 and R11 no-result-set "Statement ran, no result set", CSV disabled, no header; F2 DDL line. HANDLED.
- **Narrow width: column panel stacks under the grid.** `## Responsive behavior` 860-1099 px "column panel stacks under the grid"; R12 "stacked under the grid below [1100 px]". HANDLED.

**All requirements met:** YES

## Notes (non-blocking)
- No pixel evidence exists for this phase (spec-only). Visual contrast, spacing and hierarchy are unverified and out of scope for a style-free spec.
- IA validation (card sort, tree test) has not been run; the spec flags it. Not a FAIL.
- The theater-risk flag is present (owner @gserfaty, research basis, cadence at build gates). The basis is stated as the research brief and current product, with no user interviews. Treated as a hypothesis in the spec itself.
- The cited research brief `.design-foundations/research/2026-10-13-cloudstone-workbench.md` exists.
- The spec describes planned work (the redesign), not committed code. This is expected for a spec-phase artifact; the CLAUDE.md "describe code as committed" rule applies to the README, CHANGELOG and ARCHITECTURE docs, not to JOURNEY.md.
- Ask for logged-out visitors is available "when Ask is on" with the server API key. The journey names the anxiety "Will Ask spend money?" The mode note covers billing, but no rate limit for anonymous use is specified beyond the F3 "limit reached" branch. Not a listed requirement; recorded for the user.

## Issues (if FAIL)
None. No DW item, edge case, or Critical principle violation was found.

**Verdict: PASS**

DESIGN-REVIEW [PASS]. Report written to /Users/gabriel/code/cloudstone/.design-foundations/build/2026-10-13-cloudstone-workbench-phase-1-review.md
