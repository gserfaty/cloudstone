# Cloudstone workbench: JOURNEY

Companion to DESIGN.md (not yet written; Phase 2). Style-free: this file says what is on the screen, what it does and how it is operated, not how it looks. Sources: `.design-foundations/research/2026-10-13-cloudstone-workbench.md` (binding "researcher defaults"), README.md, ARCHITECTURE.md, current `index.html`.

Principles cited (from the design-for-ai usability principles; named, not re-derived): **Hick's law** (Hick-Hyman 1952), **Cowan's ~4+-1 chunks** (Miller's law revised, Cowan 2001), **Fitts's law** (Fitts 1954), Nielsen heuristics (#1 visibility of status, #5 error prevention, #6 recognition over recall, #9 error recovery), WCAG 2.2 AA. Journey method: JTBD job story (Moesta/Switch school only), messy-middle explore/evaluate loop (Google 2020), Rosenfeld/Morville IA systems.

## Job

**Job story (functional).** When I get a new dataset, I want to see its shape and try questions against it quickly, so I can answer them without leaving my flow.

- Emotional: feel in control and unhurried; trust that what I see is what the data holds.
- Social: be able to paste a query or a number into a message and stand behind it.

**Four forces (Moesta), from the research brief, not from interviews.**

| Force | Today |
|-------|-------|
| Push (away from now) | Results are hard to scan (no sort, no types, no stats); earlier queries vanish when the next one runs. |
| Pull (toward new) | Understand a column without writing a query; get back to a previous query in one click. |
| Anxiety | "Will sorting lie to me when results are capped?" "Will Ask spend money?" "Is my upload private?" |
| Habit | Writing SQL in a worksheet and re-running with ⌘↵ / Ctrl+↵; Snowsight-style layout. |

**Primary audience:** SQL-literate analysts in long, keyboard-first desktop sessions. **Secondary:** first-time and logged-out visitors on demo data (the example queries in R5 are their first-visit on-ramp and must stay visible; Ask chips are an extra on-ramp only when Ask is on).

## Journey

Loop, not funnel (messy middle: explore <-> evaluate, Google 2020). Actor: analyst. Scenario: understand a new dataset, then keep asking questions of it. Scope: the one Workbench screen plus the auth dialogs.

| Phase | Action | Mindset | Emotion | Touchpoint | Opportunity |
|-------|--------|---------|---------|-----------|-------------|
| 1 First visit | Page opens on `demo.sales` with a 100-row preview already run | "Does this work? what is here?" | Curious, slightly wary | Results grid, Explorer | Never show an empty screen on arrival; the preview is the proof |
| 2 Explore a table | Click tables, expand columns, click a column header | "What shape is this?" | Engaged | Explorer, grid, column panel, Profile tab | Answer shape questions without SQL |
| 3 Iterate queries | Edit SQL, ⌘↵ / Ctrl+↵, read, sort, tweak | "Getting warmer" | Focused, in flow (peak) | Worksheet, Results, status | Keep run -> read -> edit in one eye line; zero modal interruptions |
| 4 Ask and refine | Plain-English question, then edit generated SQL | "Get me started, I will fix it" | Hopeful, then in control | Ask card, worksheet | Generated SQL always lands editable in the worksheet |
| 5 Return | Come back to an earlier query | "What was that thing I ran?" | Relief if found | History view | One click to load or rerun |
| 6 Keep | Sign up to keep uploads | "Worth an account?" | Neutral | Upload drop zone, auth dialog | Route in, return to what I was doing |

**Theater risk (journey doctrine).** Owner: repo owner (@gserfaty). Research basis: the research brief and the existing product, no user interviews. Cadence: re-check against the rendered page at each build gate. Treat as a hypothesis, not a finding.

## IA

**Organization scheme:** task-oriented (what the analyst is doing), Rosenfeld/Morville. **Structure:** one hub screen, no routes; panels, tabs and dialogs are the only depth. **Systems:** global nav = top bar; local nav = sidebar views and results tabs; contextual = column panel, cell popover; search = Explorer filter; labeling below.

```
Top bar ............................ brand | [Log in][Sign up]  or  account | Log out
Sidebar (left)
  Upload drop zone
  View switch: [Explorer | History]
    Explorer: search -> my_data (own tables) -> demo (7 tables) -> columns (expand)
              Example queries (collapsible)
    History:  list of past runs, Clear history
Main
  Ask card .......................... hidden when Ask is off
  Worksheet ......................... editor, Run, status
  Results card
    Header: [Results | Chart | Profile]  status  CSV
    Results: notice strip, grid, column panel (docked right >=1100 px, stacked below otherwise)
    Chart:   Type / X / Y controls, canvas
    Profile: whole-table profile grid
Dialogs: Auth (log in / sign up), Account (password, delete)
Toasts: transient feedback
```

**Labels** (kept from today where they work): Databases/Explorer, Example queries, Worksheet, Run, Results, Chart, Profile, CSV. **New:** History, Clear history, Column details.

**Choice-cutting (Hick for choice counts; Cowan only for chunks).**
- Sidebar was three stacked lists (explorer, examples, plus new history). Two views behind one switch means the sidebar offers one list at a time (Hick: fewer simultaneous options shorten decision time). Examples stay under Explorer, collapsed by default once the user has any history, so first-timers still see them.
- Output has exactly three tabs (Hick: few choices); no tab for stats, they live in the panel.
- Top bar holds at most three items on the right (Hick).
- Tree depth is 3 (database > table > column); Explorer search handles breadth (Hick: search over scanning for long lists).
- Validation still owed: card sort and tree test were not run (sitemap is not IA, Rosenfeld/Morville); flagged as an open risk.

## Flows

Any flow step that replaces unrun worksheet text (F1 step 2, F3 step 3, F5 step 2, Example queries) follows the Worksheet replacement rule in R8: "Worksheet replaced" toast with Undo (8 s), or silent if unchanged since the last run. Any running Run or Ask can be cancelled (Esc).

Notation: circle = entry/exit, diamond = decision, rectangle = action. Written as step lists. Every flow ends in a visible outcome.

### F1. Preview a table (first visit and explore)
1. (Entry) Page loads. Results card shows loading, then 100 rows of `demo.sales`; status reads `100 rows - N ms`; worksheet holds `SELECT * FROM "demo"."sales" LIMIT 100`; Profile tab is filled in the background.
2. Action: click another table in Explorer. Worksheet text is replaced, query runs, that table is marked current.
3. Optional: expand the table's chevron to see columns; click a column to insert its name at the cursor.
4. Optional: click the small column-details button inside a grid header (or Shift+Enter on the focused header) to open Column details. The header label itself sorts.
5. (Exit) **Outcome (visible):** grid of the table's first 100 rows, current table highlighted in Explorer, status line with rows and time.
- Failure branch: query error -> error state in Results (not only the status line); Explorer selection still moves.
- Decision at step 2: is the table already current? Still rerun (cheap, predictable).

### F2. Iterate a query
1. (Entry) Focus in worksheet (`/` jumps to Ask when on, else the editor).
2. Edit SQL. ⌘↵ / Ctrl+↵ or Run.
3. Run button shows busy, status says Running.
4. Decision: succeeded?
   - Yes: grid replaced, status `N rows - ms`, history gets a new row at top, column panel closes if its column no longer exists.
   - No: error text in status and in Results; history gets an error row; SQL stays untouched so the user can fix it.
5. Optional: sort a column (click or Enter on the header label; cycle ascending, descending, original). If results were capped, the notice strip says the sort covers only the returned rows and suggests `ORDER BY` in the SQL (LIMIT does not help; R10).
6. (Exit) **Outcome (visible):** new result in the grid with row/time status, a new top entry in History.
- DDL or statements with no result set: grid area shows "no result set" empty state, status shows success, CSV disabled.

### F3. Ask, then refine
1. (Entry) Ask card visible only if the server has Ask on. Type a question or click one of 4 suggestion chips (Hick: chips capped at 4).
2. Ask button busy; explanation line says Claude is writing a query.
3. Decision: Ask succeeded?
   - Yes, SQL ran: worksheet filled with the SQL, explanation shown, Results tab selected with the rows; history row records the question and the SQL.
   - SQL generated but failed: worksheet filled, explanation shown, error shown in status/Results; user edits and runs (continue as F2).
   - Request failed (rate or time limit reached, network): error in the explanation line; worksheet unchanged.
4. Action: edit the generated SQL and Run.
5. (Exit) **Outcome (visible):** editable SQL in the worksheet plus either results or a clear error; the refined run appears as its own History row showing its SQL. History keeps no link from the Ask row to the run; each row is a complete record of what ran.
- Ask off: the card is absent, a hint under the Worksheet title says how to enable it, `/` goes to the editor.

### F4. Upload when logged out
1. (Entry) Click or drop files on the drop zone while logged out. The zone's label reads "Sign up to upload" (it opens Sign up mode).
2. No file is sent. The Auth dialog opens in Sign up mode, focus on Username.
3. Decision: create account / log in / close.
   - Account created or logged in: dialog closes, toast confirms, drop zone becomes "Upload data", Explorer shows `my_data`. The user repeats the drop (the dropped files are not retained; no hidden state).
   - Close: back to the page exactly as it was, focus returns to the drop zone.
4. (Exit) **Outcome (visible):** either the auth dialog (step 2) or, after success, a signed-in top bar and an enabled drop zone.
- Logged in: upload shows a progress toast per file, then "Loaded name as table", the table appears under `my_data`, opens, and previews (F1 step 1).

### F5. Rerun from history
1. (Entry) Switch sidebar to History. Rows newest first: query text (first line), time, rows, duration, ok/error mark.
2. Action: click or Enter a row = load SQL into the worksheet only (no run, safe to edit first). Rerun button on the row or ⌘↵ / Ctrl+↵ on the focused row = load and run.
3. Decision: list empty? Shows an empty state explaining runs will appear here; Clear history is disabled.
4. (Exit) **Outcome (visible):** worksheet holds that SQL; on rerun the grid shows fresh results and a new History row appears at the top (history is a log, never mutated).
- Clear history: asks for confirmation inline (undo is not possible), then shows the empty state.
- Storage unavailable: History works for this page session only, with a one-line notice (Nielsen #1).

## Page specs

### Workbench (the only page, `/`)

**Purpose (one sentence).** Let an analyst understand a dataset and iterate on questions about it, then return to earlier work, without leaving one screen.

**Entry points.** Direct load (auto-opens `demo.sales`); return after the auth dialog; none other (no routes).

**Exit / next.** None; the screen is the product. Leaving is closing the tab. Primary CTA: **Run** (the one primary action in the worksheet; Ask is primary only inside the Ask card; Sign up is primary in the top bar only while logged out). Fitts: Run sits at the editor's bottom-left, next to the status it updates.

**Global states to honor in every region** (matrix in the next section): `loading`, `empty`, `error`, `logged out`, `Ask off`.

#### Regions in reading order

##### R1 Top bar
- Content: brand; spacer; logged out: Log in, Sign up. Logged in: account button (avatar + name), Log out.
- States: **empty** n/a (always has content). **loading** n/a - static controls. **error** n/a - auth errors live in the dialog (R15). **logged out** Log in + Sign up. **Ask off** n/a - no Ask element here.
- Keys: Tab order brand-less, left to right through the buttons; Enter/Space activates.
- Cut: max 3 targets (Hick).

##### R2 Upload drop zone (sidebar top)
- Content: title, supported types hint, and the line "Saved only to your account, on this computer." (answers the upload-privacy anxiety); hidden file input accepting csv, json, ndjson, jsonl, xlsx, parquet, log (multiple).
- States: **empty** n/a - idle is its normal state. **loading** per-file toast "Uploading name..." (zone stays usable for more files). **error** per-file error toast naming the file. **logged out** title reads "Sign up to upload"; click or drop opens Auth in Sign up mode and sends nothing (F4). **Ask off** n/a - unaffected. Drag-over: zone shows a drop-target state.
- Keys: reachable by Tab; Enter/Space opens the file picker (logged in) or the Auth dialog (logged out).

##### R3 Sidebar view switch: Explorer | History
- Content: two-option segmented tab control with a history count.
- Why (Hick): one list visible at a time instead of three stacked ones.
- States: **empty** n/a - always two options. **loading** n/a - static. **error** n/a - no request. **logged out** same as logged in. **Ask off** n/a - unaffected.
- Keys: it is a tablist; Left/Right arrows switch (same pattern as the Results tabs); Tab leaves to the active panel.

##### R4 Explorer
- Content: search box (filters both groups); group `my_data` (own tables, count); group `demo` (7 tables, count, type badge each); each table has a name button (preview) and an expander (columns with types; click a column inserts its name at the editor cursor).
- States:
  - **empty:** no own tables: logged in "Nothing yet. Drop a file to add one."; filter with no match: "No matches."
  - **loading:** table list loading shows a loading line; column expander shows "Loading..."
  - **error:** `/tables` or `/profile` failure shows the message inline in place of the list (not only a toast).
  - **logged out:** `my_data` is shown with "Sign up to upload and keep your own tables."; demo tables fully usable.
  - **Ask off:** n/a - no Ask element in Explorer.
- Keys: `/` is not used here. Search box focusable by Tab; Up/Down moves between table rows and their expanders; Enter on the name previews; Right/Left expands/collapses columns (or Enter on the expander); Enter on a column inserts it.
- Cut: 2 groups (Hick); search carries the long-list case (Hick).

##### R5 Example queries
- Content: 10 one-click examples (label + format subtitle), collapsible group at the bottom of the Explorer view.
- States: **empty** n/a (static). **loading** n/a; clicking runs and shows R8/R9 loading. **error** a failing example shows the normal error state. **logged out** fully available (it is the on-ramp). **Ask off** unchanged: these are the first-visit on-ramp when Ask is off.
- Keys: Tab to each; Enter runs. Collapsed state is remembered per browser; default open until the user has 1+ history entries, then collapsed (Hick: fewer options for the returning user).

##### R6 History view (sidebar)
- Content (Cowan: exactly 4 chunks per row): (1) SQL first line, (2) time (relative), (3) rows + duration read together as one result chunk, (4) ok/error mark; an "Asked: ..." line appears only on Ask rows and replaces the SQL line as chunk 1's lead. Row actions: Load, Rerun. Header: Clear history. Last 100 kept.
- States:
  - **empty:** "Queries you run appear here." Clear disabled.
  - **loading:** n/a - local data is instantaneous.
  - **error:** `localStorage` unavailable or full: History is session-only, one-line notice at the top; never blocks Run.
  - **logged out:** uses its own logged-out history. History is keyed per account in `localStorage` (one key per username, plus one for logged-out use); logging out or switching account shows only that account's history. README must say it is per account, per browser.
  - **Ask off:** only Run entries appear; no Ask lines.
- Keys: the list is one tab stop with roving focus; Up/Down moves; Enter loads into the worksheet; ⌘↵ / Ctrl+↵ reruns; Esc closes the Clear-history confirm if open (Esc precedence, layer 1); Delete does nothing (no per-row delete; Clear history only, Hick).

##### R7 Ask card
- Content: question input, a one-line mode note under the input from `/me` ("Answered with your Claude plan" for subscription; "Each question is billed to the server's API key" for api), Ask button, 4 suggestion chips, explanation/error line. **The one allowed additive API change:** `/me` returns `ask` as "off"|"subscription"|"api" (today a boolean). Nothing else in the API changes.
- States:
  - **empty:** idle with placeholder; chips shown only because Ask is on.
  - **loading:** Ask button becomes "Cancel" and Esc cancels (same message as Run: "Cancelled - the server may still finish it in the background."); explanation line says "Claude is writing a query..." (live region).
  - **error:** explanation line in error style: what happened, why, how to fix. Exact strings are the Ask error rows (ASK-E1 to ASK-E8) in `## Microcopy`.
  - **logged out:** available when Ask is on (README limit: billed to server key).
  - **Ask off:** the whole card is absent from the DOM flow (hidden); the Worksheet header shows a hint with the enabling command; `/` focuses the editor instead.
- Keys: Esc while a question is in flight cancels it (Esc precedence, layer 4); `/` focuses the question input (when not typing and no dialog is open); Enter submits; chips are buttons activated by Enter/Space.
- Cut: 4 chips and one primary action (Hick).

##### R8 Worksheet
- **Worksheet replacement rule (all of: table preview, example, Ask, History load):** if the editor text has unrun edits (differs from the last run SQL), replacing it shows a toast "Worksheet replaced" with an Undo action (8 s) that restores the previous text and cursor position. If the text is unchanged since the last run, it is replaced silently.
- Content: header (title, Ask-off hint slot); line-numbered editor; toolbar with Run (+ shortcut hint) and a status line.
- States:
  - **empty:** placeholder `SELECT * FROM demo.sales LIMIT 100`; Run with empty text just focuses the editor.
  - **loading:** Run button becomes "Cancel" and Esc cancels; status "Running..." (aria-live polite). Cancel stops waiting client-side and the status reads "Cancelled - the server may still finish it in the background." No client timeout; Ask keeps its existing 3-minute server limit.
  - **error:** status shows the database error text, monospace, preserved line breaks; SQL untouched.
  - **logged out:** same; only demo tables resolve.
  - **Ask off:** hint visible in the header.
- Keys: ⌘↵ / Ctrl+↵ runs (from inside the editor); Tab inserts two spaces (focus trap is known; Esc then Tab is the way out; Esc follows the Esc precedence table, layer 5, so keyboard users are never stuck); a one-line hint "Esc then Tab leaves the editor" shows in the worksheet toolbar; `/` from anywhere not typing focuses it when Ask is off; line numbers are decorative (aria-hidden).

##### R9 Results card header
- Content: tablist [Results | Chart | Profile]; status chip (ok/error mark, rows, time); column count; CSV button.
- States: **empty** before any run: status blank, CSV disabled; no-result-set statement: status reads "Statement ran, no result set" with ok mark, CSV disabled; zero rows: status "0 rows - N ms", CSV enabled (header-only file). Capped at 1,000 rows: status "1,000+ rows · N ms · showing the first 1,000" (the truncation notice in R10 repeats the scope). **loading** status "Running..." and tabs stay usable. **error** error mark and message. **logged out** same. **Ask off** same.
- Keys: arrow keys move between tabs and activate (existing behavior); CSV is a button, disabled when no result set; hidden on Profile.
- Cut: 3 tabs, 2 actions; status is plain text, not three badges (Hick).

##### R10 Notice strip (Results tab, above the grid)
- Content: shown only when needed: (a) truncation "Showing the first 1,000 rows" + "Sorting and column stats cover only these rows. For the right rows in order, add ORDER BY to your SQL; LIMIT does not help." (b) sort active "Sorted by col (ascending)" with a clear control.
- States: hidden by default; **empty** n/a - hidden when there is nothing to say. **loading** n/a - hidden. **error** n/a - errors replace the grid (R11). **logged out** n/a - same as logged in. **Ask off** n/a - unaffected.
- Keys: the clear-sort control is a button in tab order; Esc does not touch it (not in the Esc precedence table).

##### R11 Results grid
- Content: sticky header with column name and a type hint; right-aligned numeric cells with tabular figures and separators (not for `id`, `*_id`, `year`); muted `null`; mono truncated JSON with `{...}` / `[3]` hints; ellipsis for long text; row numbers; rows 30-32 px; at least 15 rows visible at 1440x900.
- States:
  - **empty (zero rows):** header row still visible plus "No rows matched." row.
  - **empty (no result set, DDL):** icon + "No rows to show / statement ran but returned no result set"; no header.
  - **empty (nothing run yet):** same grid area says "Run a query to see results".
  - **loading:** keep the previous grid, dimmed, until the new result replaces it (no layout jump); first load shows a loading line.
  - **error:** replaces the grid with the error message, what happened, how to fix.
  - **logged out:** n/a - same as logged in (demo tables only).
  - **Ask off:** n/a - unaffected.
- Keys (single tab stop, roving cell focus): Arrow keys move cell focus; Home/End first/last column; Ctrl+Home/End (⌘↑/⌘↓ on macOS) first/last cell; PageUp/PageDown by a screenful; Enter on a data cell opens the cell popover (full value; Esc closes it first per Esc precedence, focus returns); ⌘C / Ctrl+C on a focused cell copies the raw full value (toast confirms); the header label is the sort target: click or Enter/Space cycles sort (ascending, descending, original); a separate small column-details button inside each header cell (click, or Shift+Enter on the focused header) opens Column details; Esc follows the Esc precedence table.
- Narrow (<1100 px): grid scrolls horizontally inside its own container only, never the page.

##### R12 Column details panel
- Content (Cowan: four groups): (1) name + type; (2) counts: non-null, nulls, distinct; (3) range: min, max, mean (numeric only); (4) top values with bars, plus a histogram (numeric only). Footer: "based on N returned rows".
- States: **empty** (no column selected): panel closed; **empty (all-null or single-value column)** shows what exists and says so rather than blank bars; **loading** instant (client-side); if rows > 1,000 cap it says so. **error** a column that cannot be summarized (e.g., nested JSON) shows counts and top values only. **logged out** n/a - same as logged in. **Ask off** n/a - unaffected.
- Placement: docked right inside the results card at >= 1100 px; stacked under the grid below that.
- Keys: opens from the header's column-details button or Shift+Enter on the focused header (never from the sort gesture); focus moves into the panel's heading; Esc closes it (Esc precedence, layer 3) and returns focus to the originating header cell; selection carries to the Chart X/Y defaults.

##### R13 Chart tab
- Content: Type (bar, line, scatter), X, Y selects; canvas; title; text alternative pointing to the Results tab.
- States: **empty** (centered text, no canvas, no controls enabled) "Run a query to chart its result" / "The result has no rows" / "No numeric column to plot" / no-result-set: "This statement returned no result set, so there is nothing to chart". **loading** n/a (redraws instantly). **error** if Chart.js failed to load, an empty state explains and points to the table. **logged out** n/a - same as logged in. **Ask off** n/a - unaffected.
- Keys: selects are native (arrows, type-ahead); the canvas is `role=img`; X/Y default to the column chosen in the grid when one is selected.

##### R14 Profile tab
- Content: tab label includes the current table; whole-table profile grid (type, null %, approx distinct, min/max, mean, std, quartiles) from the server.
- States: **empty** after an Example query (no current table): "Select a table to profile it." **loading** "Profiling table..." **error** message inline. **logged out** demo tables only. **Ask off** n/a - unaffected.
- Keys: same grid keyboard model as R11 (read-only, no column panel).

##### R15 Dialogs (Auth, Account)
- Auth: segmented Log in / Sign up, username, password with Show/Hide, hint (sign-up only), inline error (`role=alert`), one primary submit. Account: change password, delete account (password required + confirmation).
- Cut: the Log in / Sign up segmented control offers exactly two modes in one dialog instead of two separate dialogs or links (Hick).
- States: **empty** n/a - opened only by user action. **loading** submit busy. **error** inline, form data kept (except password on failure of delete). **logged out** in R15 only the Auth dialog is offered; Account is unreachable. **Ask off** n/a - unaffected.
- Keys: modal; Esc closes it (Esc precedence, layer 2); focus lands on Username; focus returns to the trigger on close; Enter submits.

##### R16 Toasts and live regions
- Toasts for outcomes that have no home elsewhere (upload done, copied, logged in/out). Errors use `role=alert`; success is announced through a polite live region. Status line, explanation line and Chart title are the other live regions. Max 3 toasts visible (Hick).
- Behavior: success toasts auto-dismiss after 4 s; error toasts stay until dismissed (close button, or Esc while the toast is focused, which dismisses only that toast). Hovering or focusing a toast pauses its timer (WCAG 2.2.1). Toasts never take focus. The Undo toast (see Worksheet replacement) lasts 8 s.
- States: **empty** no toasts rendered. **loading** an upload-in-progress toast stays until done. **error** persistent error toast. **logged out** n/a - same toasts. **Ask off** n/a - unaffected.
- Keys: toasts are not in the page tab order except their close/Undo buttons, which are reachable by Tab while a toast is visible; Enter/Space activates; Esc on a focused toast dismisses it and returns focus to where it was.

#### State matrix (region x state)

| Region | Empty | Loading | Error | Logged out | Ask off |
|--------|-------|---------|-------|-----------|---------|
| R1 Top bar | n/a | none | none | Log in + Sign up | no effect |
| R2 Drop zone | idle | per-file toast | per-file toast | "Sign up to upload" -> Auth (Sign up mode) | no effect |
| R3 View switch | n/a | n/a | n/a | same | no effect |
| R4 Explorer | no own tables / no match | list or columns "Loading..." | inline message | `my_data` hint, demo ok | no effect |
| R5 Examples | n/a | via R8/R9 | via R8/R9 | available | available |
| R6 History | "Queries you run appear here." | n/a | session-only notice | own per-account history | no Ask lines |
| R7 Ask card | idle + chips | busy + live text | error line | available if on | absent |
| R8 Worksheet | placeholder | Running... | error text | same | hint shown |
| R9 Header | blank, CSV off | Running... | error mark | same | no effect |
| R10 Notice | hidden | hidden | hidden | no effect | no effect |
| R11 Grid | zero rows / no result set / not run | dim previous | message replaces grid | same | no effect |
| R12 Column panel | closed / all-null / single value | n/a | partial stats | no effect | no effect |
| R13 Chart | three empty reasons | n/a | Chart.js missing | no effect | no effect |
| R14 Profile | no current table | profiling... | inline message | demo only | no effect |
| R15 Dialogs | n/a - user-opened | submit busy | inline error | Auth only | n/a |
| R16 Toasts | none | upload toast | alert toast | no effect | no effect |

#### Screen-level keyboard map

| Key | Action | Scope |
|-----|--------|-------|
| `/` | Focus Ask input (Ask on) or editor (Ask off) | not typing, no dialog open |
| ⌘↵ / Ctrl+↵ | Run | in editor; on a History row = rerun |
| Tab / Shift+Tab | Move through regions in reading order: top bar, sidebar, Ask, worksheet, results tabs, grid (one stop), panel | everywhere (editor traps Tab; Esc then Tab leaves) |
| Arrow keys | Tabs, view switch, grid cells, History rows, Explorer rows | roving focus within each widget |
| Enter | Activate; open cell popover; load History row; sort on header label | context |
| Shift+Enter | Open Column details from a focused header cell | grid |
| ⌘C / Ctrl+C | Copy focused cell | grid |
| Esc | Closes only the topmost layer; see the Esc precedence table below | layered |

**Esc precedence.** One Esc closes only the topmost layer. A focused toast's Esc dismisses that toast only.

| Order | Layer closed by Esc | Used by |
|-------|--------------------|---------|
| 1 | Open popover or menu (cell popover, history Clear confirm) | R6, R11 |
| 2 | Open dialog | R15 |
| 3 | Column panel | R12 |
| 4 | In-flight Run or Ask: cancel | R7, R8 |
| 5 | Editor: release the Tab trap for the next Tab | R8 |

Reading order = tab order = visual order (WCAG 2.4.3, 1.3.2). Targets at least 24 px (WCAG 2.5.8); Run and primary buttons larger (Fitts).

#### Responsive behavior (structure only)
- >= 1100 px: sidebar + main; column panel docked right inside the results card.
- 860 to 1099 px: sidebar + main; column panel stacks under the grid.
- < 860 px: sidebar stacks above main (as today); grid scrolls inside its container; page never scrolls sideways.

#### Where the page cuts options (Hick for choice counts, Cowan for chunks held in memory)

| Place | Cut | Law |
|-------|-----|-----|
| Sidebar | Explorer or History, one at a time | Hick |
| Output | 3 tabs, 2 actions | Hick |
| Top bar | 3 targets max | Hick |
| Ask | 4 chips, 1 primary | Hick |
| Column panel | 4 groups of stats | Cowan |
| History row | 4 facts per row (Cowan chunk); load or rerun only, one global clear (Hick) | Cowan, Hick |
| Explorer | search over scan for long lists | Hick |
| Toasts | 3 visible | Hick |
| Examples | collapsed once the user has history | Hick |

#### Out of scope (this page)
Split layout, multiple worksheets, side-by-side result comparison, server-side history, dark theme.

## Microcopy

One voice across the Workbench: **calm, precise, plain.** Sentence case. No exclamation marks. Use SQL terms analysts already use (rows, column, query, distinct, null); no other jargon. Placeholders in `{braces}` are filled at runtime. Strings are exact; change them here first, then in the UI.

**Voice vs tone (Podmajersky).** Voice is constant. Tone shifts with the moment. Never celebratory.

**Error formula (Yifrah).** Every error states what happened, why (when known), and how to fix it, in that order. The Formula column names the parts. No error blames the user: no "you entered", "invalid input", "wrong" as a verdict. A failed step says what state the user's work is in ("your SQL is unchanged", "nothing was deleted") so the user is not left guessing (Nielsen #9).

**Front-loading (Redish).** The first words of a line carry the meaning: the scanner reads the start of each status, toast and row.

Tone column: **neutral** = status and labels; **direct** = errors, warnings and confirmations that ask for a decision; **calm** = empty states and completed actions.

### Top bar, upload and sign-up routing (R1, R2)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-01 | R1 · logged out | Log in | neutral | |
| MC-02 | R1 · logged out | Sign up | neutral | |
| MC-03 | R1 · logged in | Log out | neutral | |
| MC-04 | R1 · logged in, account button | `{name}` (aria: "Account settings for {name}") | neutral | |
| MC-05 | R2 · idle | Upload data. Supported: CSV, JSON, NDJSON, JSONL, XLSX, Parquet, LOG. Saved only to your account, on this computer. | neutral | |
| MC-06 | R2 · logged out | Sign up to upload | neutral | |
| MC-07 | R2 · drag over | Drop to upload | neutral | |
| MC-08 | R2 · loading | Uploading {file}... | neutral | |
| MC-09 | R2 · done (toast) | Loaded {file} as {table}. | calm | |
| MC-10 | R2 · error (toast, stays) | Could not load {file}. {server reason}. Check that it is a supported type, then drop it again. | direct | happened · why · fix |
| MC-11 | F4 · after sign-up (toast) | Signed in. Drop your files again to upload them. | calm | |

### Sidebar: view switch and Explorer (R3, R4)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-12 | R3 · tabs | Explorer · History (aria on History: "History, {n} runs") | neutral | |
| MC-13 | R4 · empty, logged in | Nothing yet. Drop a file above to add one. | calm | |
| MC-14 | R4 · logged out | Sign up to upload and keep your own tables. | calm | |
| MC-15 | R4 · no match | No matches for '{query}'. Clear the search to see all tables. | neutral | |
| MC-16 | R4 · loading | Loading tables... (columns: Loading...) | neutral | |
| MC-17 | R4 · error, inline | Could not load tables. {server reason}. Reload the page to try again. | direct | happened · why · fix |
| MC-18 | R4 · column error, inline | Could not load columns for {table}. {server reason}. Click the table again to retry. | direct | happened · why · fix |

### Example queries (R5)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-19 | R5 · group | Example queries. The ten example labels and format subtitles keep their current wording; failing examples show the R8/R9 error strings. | neutral | |

### History (R6)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-20 | R6 · empty | Queries you run appear here. Your last 100 runs are kept in this browser. | calm | |
| MC-21 | R6 · Clear history, empty (tooltip) | Nothing to clear yet. | neutral | |
| MC-22 | R6 · session-only notice | History is not saved in this browser, so it lasts only until you close this page. Free up browser storage to keep it. | direct | happened · why · fix |
| MC-23 | R6 · logged out | Showing history for logged-out use in this browser. Log in to see your own history. | neutral | |
| MC-24 | R6 · row labels | `Asked: {question}` (Ask rows only) · `{time}` (e.g. "2 min ago") · `{n} rows · {ms} ms` · `OK` or `Error` | neutral | |
| MC-25 | R6 · row actions | Load (aria: "Load query from {time}") · Rerun (aria: "Rerun query from {time}") | neutral | |
| MC-26 | R6 · clear confirm | Clear all history? Every saved run in this browser for this account is removed. It cannot be undone. Buttons: Clear history · Cancel | direct | |
| MC-27 | R6 · cleared (toast) | History cleared. | calm | |

### Ask card (R7) and Ask-off hint

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-28 | R7 · idle placeholder | Ask a question about your data, for example: Which sales rep sold the most speakers? | neutral | |
| MC-29 | R7 · mode note, subscription | Answered with your Claude plan. | neutral | |
| MC-30 | R7 · mode note, api | Each question is billed to the server's API key. | neutral | |
| MC-31 | R7 · button | Ask (busy: Cancel) | neutral | |
| MC-32 | R7 · loading (live text) | Claude is writing a query... | neutral | |
| MC-33 | R7 · cancelled; also R8 | Cancelled - the server may still finish it in the background. | neutral | |
| MC-34 | R7 · empty question | Type a question first, then press Ask. | direct | |
| ASK-E1 | R7 · error · Claude Code missing | Ask could not start Claude Code. It is not installed or not on the PATH. Install it, run `claude` once to log in, then ask again. | direct | happened · why · fix |
| ASK-E2 | R7 · error · no API key | Ask could not reach the Claude API. The API key is missing or was refused. Set ANTHROPIC_API_KEY, restart the server, then ask again. | direct | happened · why · fix |
| ASK-E3 | R7 · error · time limit | Ask stopped after 3 minutes, before Claude finished writing a query. Ask a narrower question, or write the SQL yourself. | direct | happened · why · fix |
| ASK-E4 | R7 · error · declined | Claude declined to answer that question. Rephrase it, or write the SQL yourself in the worksheet. | direct | happened · why · fix |
| ASK-E5 | R7 · error · cut off | Claude's answer was cut off before it finished. Ask a simpler question. | direct | happened · why · fix |
| ASK-E6 | R7 · error · rate limit | Ask has reached the Claude API rate limit. Wait about a minute, then ask again. Run still works. | direct | happened · why · fix |
| ASK-E7 | R7/R8 · SQL written, did not run | Claude wrote a query, but it did not run. The database said: {db message}. The SQL is in the worksheet. Edit it and press Run. | direct | happened · why · fix |
| ASK-E8 | R7 · error · any other failure | Ask could not answer. {server reason}. Try again in a moment, or write the SQL yourself. | direct | happened · why · fix |
| ASK-E9 | R8 header · Ask off (hint, not an error) | Ask is off. To turn it on, restart the server with CLOUDSTONE_ASK=subscription (your Claude plan) or CLOUDSTONE_ASK=api (API key). | neutral | |

### Worksheet (R8)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-35 | R8 · empty placeholder | SELECT * FROM demo.sales LIMIT 100 | neutral | |
| MC-36 | R8 · button | Run (shortcut hint: ⌘↵ / Ctrl+↵; busy: Cancel) | neutral | |
| MC-37 | R8 · loading status (live) | Running... | neutral | |
| MC-38 | R8 · error status | Query failed: {db message}. Your SQL is unchanged. Fix it and press Run. | direct | happened · why · fix |
| MC-39 | R8 · Esc hint, toolbar | Esc then Tab leaves the editor. | neutral | |
| MC-40 | R8 · replace (toast) | Worksheet replaced · Undo | neutral | |
| MC-41 | R8 · undo done (toast) | Previous SQL restored. | calm | |
| MC-42 | R8 · editor label (aria) | SQL editor | neutral | |

### Results header (R9), notice strip (R10), grid (R11)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-43 | R9 · status, ok | {n} rows - {ms} ms | neutral | |
| MC-44 | R9 · status, zero rows | 0 rows - {ms} ms | neutral | |
| MC-45 | R9 · status, capped | 1,000+ rows · {ms} ms · showing the first 1,000 | neutral | |
| MC-46 | R9 · status, no result set | Statement ran, no result set | neutral | |
| MC-47 | R9 · status, running | Running... | neutral | |
| MC-48 | R9 · CSV disabled (tooltip) | Run a query to download CSV. (no result set: "Nothing to download: this statement returned no result set.") | neutral | |
| MC-49 | R9 · column count | {n} columns | neutral | |
| MC-50 | R10 · truncation notice | Showing the first 1,000 rows. Sorting and column stats cover only these rows. For the right rows in order, add ORDER BY to your SQL; LIMIT does not help. | direct | |
| MC-51 | R10 · sort active | Sorted by {col} ({ascending or descending}). Button: Clear sort | neutral | |
| MC-52 | R11 · zero rows | No rows matched. | neutral | |
| MC-53 | R11 · no result set (DDL) | No rows to show. The statement ran but returned no result set. | calm | |
| MC-54 | R11 · nothing run yet | Run a query to see results. | calm | |
| MC-55 | R11 · first load | Loading results... | neutral | |
| MC-56 | R11 · error, replaces grid | Query failed: {db message}. Your SQL is unchanged. Fix it and press Run. (Same as MC-38.) | direct | happened · why · fix |
| MC-57 | R11 · copy done (toast) | Cell copied. | calm | |
| MC-58 | R11 · copy blocked (toast, stays) | Could not copy the cell. Your browser blocked clipboard access. Allow it for this page, then press Ctrl+C or ⌘C again. | direct | happened · why · fix |
| MC-59 | R11 · column-details button (aria) | Column details for {col} | neutral | |

### Column details (R12) and Chart (R13)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-60 | R12 · title | Column details: `{col}` · `{type}` | neutral | |
| MC-61 | R12 · group labels | Counts (Non-null, Nulls, Distinct) · Range (Min, Max, Mean) · Top values | neutral | |
| MC-62 | R12 · footer | Based on {n} returned rows. | neutral | |
| MC-63 | R12 · footer, capped | Based on the first 1,000 rows. The result was capped, so this covers only those rows. | direct | |
| MC-64 | R12 · all-null column | Every value in {col} is null, so there is nothing to summarize. Counts are shown above. | calm | |
| MC-65 | R12 · single distinct value | {col} has one distinct value: {value}. | calm | |
| MC-66 | R12 · error, partial stats | Range and histogram are not available for this type. Counts and top values are shown. | neutral | |
| MC-67 | R13 · controls | Type (Bar, Line, Scatter) · X · Y | neutral | |
| MC-68 | R13 · empty, no run | Run a query to chart its result. | calm | |
| MC-69 | R13 · empty, zero rows | The result has no rows, so there is nothing to chart. | calm | |
| MC-70 | R13 · empty, no numeric column | No numeric column to plot. Pick a query that returns at least one number, such as a count or total. | calm | |
| MC-71 | R13 · empty, no result set | This statement returned no result set, so there is nothing to chart. | calm | |
| MC-72 | R13 · Chart.js missing | The chart did not load. Check your connection and reload the page. The Results tab still shows the rows. | direct | happened · why · fix |
| MC-73 | R13 · canvas text alternative | {Y} by {X}. The values are listed in the Results tab. | neutral | |

### Profile (R14)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-74 | R14 · tab label | Profile: {table} (no table: Profile) | neutral | |
| MC-75 | R14 · empty, after an example | Select a table to profile it. | calm | |
| MC-76 | R14 · loading | Profiling table... | neutral | |
| MC-77 | R14 · error, inline | Could not profile {table}. {server reason}. Try again, or choose another table. | direct | happened · why · fix |

### Dialogs (R15) and toasts (R16)

| ID | Where · state | Exact string | Tone | Formula |
|----|--------------|--------------|------|---------|
| MC-78 | R15 · Auth tabs and labels | Log in · Sign up · Username · Password · Show · Hide | neutral | |
| MC-79 | R15 · sign-up hint | Passwords: 8 to 128 characters. Usernames: 3 to 32 letters, digits, '.', '_' or '-'. | neutral | |
| MC-80 | R15 · submit | Log in (sign up: Create account; busy: Working...) | neutral | |
| MC-81 | R15 · error, credentials do not match | Could not log in. That username and password do not match an account here. Check both and try again. | direct | happened · why · fix |
| MC-82 | R15 · error, too many attempts | Log in is paused for this username after too many failed attempts. Try again in 15 minutes. | direct | happened · why · fix |
| MC-83 | R15 · error, username taken | Could not create the account. That username is already taken. Choose another and submit again. | direct | happened · why · fix |
| MC-84 | R15 · error, password length | Could not create the account. Passwords need 8 to 128 characters. Choose a longer password and submit again. | direct | happened · why · fix |
| MC-85 | R15 · error, username format | Could not create the account. Usernames use 3 to 32 letters, digits, '.', '_' or '-'. Change the username and submit again. | direct | happened · why · fix |
| MC-86 | R15 · error, network | Could not reach Cloudstone. Your details are still here. Check that the server is running, then submit again. | direct | happened · why · fix |
| MC-87 | R15/R16 · logged in (toast) | Logged in as {name}. After sign-up: Account created. Logged in as {name}. | calm | |
| MC-88 | R15 · Account, sections and labels | Account · Change password (Current password, New password, Change password) | neutral | |
| MC-89 | R15 · password changed (toast) | Password changed. | calm | |
| MC-90 | R15 · error, change password | Could not change the password. The current password does not match, so your password is unchanged. Enter it again and retry. | direct | happened · why · fix |
| MC-91 | R15 · Delete account | Delete account. This permanently deletes your account and the tables you uploaded. It cannot be undone. Enter your password to confirm. Buttons: Delete account · Cancel | direct | |
| MC-92 | R15 · error, delete | Could not delete the account. The password does not match, so nothing was deleted. Enter it again to confirm. | direct | happened · why · fix |
| MC-93 | R16 · account deleted (toast) | Your account and its tables were deleted. | calm | |
| MC-94 | R16 · logged out (toast) | Logged out. | calm | |
| MC-95 | R16 · dismiss and close (aria) | Dismiss message · Close | neutral | |

### Checks

- Every state in the Workbench page-spec matrix (R1 to R16, columns empty, loading, error, logged out, Ask off) has at least one row above, or is marked n/a there. Rows MC-19, MC-23 and ASK-E9 cover the examples, logged-out history and Ask-off hint.
- Every row with a `Formula` value follows what happened, why, how to fix. Blame words ("you entered", "invalid input", "wrong" as a verdict) do not appear.

## Data surfaces

Specs for the results experience: grid (R11), column details (R12), chart (R13) and profile (R14), plus the vertical budget that makes them fit. This section refines R9 to R14; where it adds a key or a string, the page spec's Esc precedence table and `## Microcopy` still govern, and the new strings (DS-xx) are merged into Microcopy in Phase 5. Tokens are DESIGN.md names only. Principles cited: data-ink and truthful encoding (Tufte 1983; Cairo 2019), marks and channels (Munzner 2014; position on a common scale is the most accurate channel, Cleveland and McGill 1984), Cowan chunks, Hick, Nielsen #1 and #5, WCAG 2.2 AA (1.4.11 graphics, 2.4.11 focus not obscured, 2.5.8 target size).

### 1. Shared model

**Result view.** One list of returned rows (at most 1,000; the server's `truncated` flag is the only source of "capped") and one *view order*: original, or sorted. The grid, the CSV download and the chart all read the view order, so what is on screen is what is charted and exported. CSV carries raw values, not formatted ones.

**Kinds (inferred in the browser).** The query payload has column names only, so each column gets a *kind* from its non-null values. The header shows the kind as its type hint.

| Kind | Rule | Align | Format |
|------|------|-------|--------|
| `null` | every value is null | left | `null` token |
| `number` | every non-null value is a JS number, or a numeric string with no leading zero (`"02134"` is text; `"0"` and `"0.5"` are numbers). Decimals and huge integers arrive as strings and count | right | tabular figures; en-US thousands separators on floats and on integers >= 10,000 (digit-grouped as text, never through `Number`, so huge integers keep every digit); no separators when the column is named `id`, ends in `_id`, or is `year` (case-insensitive); decimals exactly as returned; non-finite values are text |
| `date` | every non-null value matches ISO date or timestamp (`2026-10-13`, `2026-10-13 09:30:00`, `...T...Z`) | left | as returned |
| `bool` | every non-null value is `true` or `false` | left | `true` / `false` |
| `json` | every non-null value is an object or array | left | hint then truncated preview: `[3] [1,2,3]`, `{…} {"city":"Oslo","zip"…`; popover pretty-prints |
| `text` | everything else that is uniformly text | left | single line, ellipsis, whitespace collapsed |
| `mixed` | non-null values fall into more than one of the kinds above (for example numbers and text) | left | each value formatted as its own kind but aligned left, no separators on numbers, so nothing is implied to be a number |

Tokens: `null` in `--text-muted`, Plex Mono italic. An empty string shows `""` in the same muted style, so empty and null stay different. Hint text uses the 12/16 label size.

**Selected column.** At most one. Set only by opening Column details for it (details button or Shift+Enter on the header). Sorting, cell focus and arrow keys never change it. Effects: its cells get the `--accent-bg-subtle` tint, the panel shows it, and the Chart X/Y defaults start from it (section 5). Cleared when a new result no longer has a column of that name, on error, or when the panel's column is replaced by another. Closing the panel keeps the selection and its tint; selecting another column moves it.

### 2. Vertical budget and scroll (1440 x 900)

**(a) Density.** The criterion is at least 15 result rows fully visible at 1440 x 900, Ask on, editor at its default height, no notice strip. Row height stays 32 px (DESIGN.md `--row-h`); the 13 px mono text, 20 px line height and 6 px padding do not change. The room comes from the regions around the grid:

| Region | Mock (approved) | Spec | How |
|--------|-----------------|------|-----|
| Top bar | 40 | 40 | unchanged |
| Main padding top / bottom | 16 / 16 | 16 / 12 | legend overhang (8 px) still clears the top bar hairline |
| Ask (frame 2, pad 12 top / 8 bottom) | 126+ | **82** | one 32 px input row, then one 24 px line holding the 4 chips left and the mode note (MC-29/MC-30) right-aligned; 4 px between |
| Gap between regions | 24 | **16** | legend sits on the rule, 8 px of clear space remains |
| Worksheet | 188 | **144** | editor default **3 lines** (60 px text + padding), then the 40 px Run row |
| Results frame | rest | **574** | 2 frame + 40 header + 532 body |
| Gap x 2 | 48 | 32 | |

Sum: 40 + 16 + 82 + 16 + 144 + 16 + 574 + 12 = 900. The 532 px body holds the 36 px sticky header (33 px plus the 3 px double rule) and **496 px of rows = 15 full rows plus 16 px of the 16th**. Measured in the browser on the mock with this budget: 15 full rows, 16 px peeking. Variants, same arithmetic:

| State | Rows area | Full rows visible |
|-------|-----------|-------------------|
| Baseline (Ask on, no notice) | 496 | 15 (+ half row) |
| Ask off (the default install) | 594 | 18 |
| One-line notice strip (24 px: sort active, or truncation at >= 1180 px wide) | 472 | 14 (+ 3/4 row) |
| Two-line truncation notice (40 px, narrower results) | 456 | 14 |
| Panel docked | same height as baseline | 15 (the panel takes width, not height) |

The strip's cost is accepted: telling the analyst a sort covers only the returned rows outranks one row (Nielsen #1). A viewer 768 px tall gets about 11 rows.

**Layout rules that make the budget hold.**
- At >= 860 px wide the page is one viewport tall: `main` is a flex column; Results takes the remaining height (`min-height: 0`) and **the grid scrolls inside its own container**. The page does not scroll vertically at heights where the Results frame stays >= 238 px (78 chrome + 5 rows). Below that, `main` scrolls and the grid keeps its own scroller.
- Editor: 3 lines by default, fixed (it does not grow while typing, which would move the grid under the cursor), scrolls inside, with a vertical resize handle (up to 12 lines; the choice is remembered per browser). The 15-row criterion is measured at the default.
- Below 860 px: the page scrolls normally and the grid is capped at 420 px tall (own scroller, own horizontal scroll).

**(b) Scroll affordance and sticky header.**
- The grid container is the only scroller for the result. The **header row is sticky at the top** (opaque `--surface`, double rule beneath it) and the **row-number column is sticky at the left** (opaque), with the corner cell above both. Nothing scrolls under a transparent header.
- Three cues that more rows exist, none of them motion: (1) the half-row peek (a row is cut by the container edge); (2) while rows remain below the fold, the container's bottom edge shows a 2 px `--border-strong` rule (hairline when scrolled to the end); (3) a thin always-visible scrollbar (`scrollbar-width: thin`, `scrollbar-gutter: stable`, colored from `--border-control`), so macOS overlay scrollbars do not hide it. No gradient shade (DESIGN.md Never).
- A range readout in the Results header, left of CSV: **DS-01** "Rows {a} to {b}", 12 px mono, `--text-muted`, `aria-hidden`, updated on scroll (animation-frame throttled), shown only when the result has more rows than fit. It is not a live region.
- `scroll-padding-top: 36px` and `scroll-padding-left: 44px` on the container, so a focused cell scrolled into view is never hidden behind the sticky header or row-number column (WCAG 2.4.11).

### 3. Grid (R11)

**Geometry.** Rows 32 px; header 36 px; columns size to content with min 64 px and max 320 px (longer content ellipsizes; the full value is in the title and the popover). No zebra striping: one `--rule` hairline per row. Cells have no hover effect. Row-number column (44 px, right-aligned, `--text-muted`) shows the position in the *view order* (it renumbers when sorted).

**Header cell** = one roving-focus stop with two controls:
- Name (Plex Mono 500 13 px) followed by the kind hint in 12/16 `--text-muted` on the same line, so the header stays 36 px (the mock's second 11 px line is dropped). Numeric headers are right-aligned. Truncates with an ellipsis; `title` carries name and kind.
- Sort target: clicking the name, or Enter / Space on the focused header. Sorted state shows a glyph (up or down triangle) beside the name, `aria-sort`, and the `--accent-selected` fill, so it is never color alone.
- Column-details button: 24 x 24 px at the header's right edge (WCAG 2.5.8), mini-bars glyph in `--text-muted` (never `--data-1`), always visible (no hover reveal; Hick, recognition over recall); accessible name MC-59. Click, or Shift+Enter on the focused header.

**Sort cycle and rules.** Ascending, then descending, then original (restores the order the query returned). One column at a time; sorting another column starts at ascending. A new result clears the sort. Over returned rows only; when capped the strip (R10) says so (MC-50), and while a sort is active it also shows MC-51 with Clear sort. Comparison: numbers by value; dates, text and bool by locale collation of the displayed text (ISO dates sort chronologically; `false` before `true`); json by its compact text; mixed puts numbers (by value) before everything else (by text); **null always sorts last in both directions**; ties keep returned order (stable). Sorting is inert and the sort control is `aria-disabled` when the result has 0 or 1 rows.

**Cell focus.** Single tab stop for the whole grid (roving `tabindex`). Header row is row 0 of the focus grid; the row-number column is not a focus stop. The initial stop is the first data cell (the first header cell when there are no rows). Focused cell: inset 2 px `--focus-ring`; its row gets `--accent-selected`; the selected column keeps its tint. Down from a header goes to the first data row; Up from the first data row goes to the header.

**Cell popover.** Enter on a focused data cell opens it; a click focuses the cell and also opens it when the displayed value is clipped (ellipsis, JSON). Content: column name and kind (12/16 muted), then the raw value in Plex Mono 13, wrapped, scrolling past 240 px tall (max 360 px wide); JSON is pretty-printed (2 spaces); a Copy button for pointer users (not in the tab order; the keyboard path is the next bullet). A floating layer (4 px radius, `--shadow-float`, scale-fade 150 ms), non-modal, focus stays on the cell and the cell points to it with `aria-describedby`. Placement below the cell, flipping above near the container's bottom edge. Closes on Esc (Esc precedence layer 1), on any arrow key, on scroll of the grid, or on outside click.

**Copy.** ⌘C / Ctrl+C on a focused data cell copies the raw value (the full string, unformatted; objects as compact JSON); toast MC-57; blocked clipboard: MC-58. On a null cell nothing is copied and the toast is DS-02. On a focused header, it copies the column name (MC-57).

**Keys** (added to R11; nothing in it changes): Arrows move; Home/End first/last column; Ctrl+Home/End (⌘↑/⌘↓) first/last cell; PageUp/PageDown move by visible rows minus one; Enter on header sorts; Enter on data opens the popover; Shift+Enter on header opens details; ⌘C copies; Esc follows section 8.

**States** (extends R11's list, same strings): loading keeps the previous grid, dimmed (`opacity` only, `aria-busy`, no pointer events) so the layout does not jump; first load shows MC-55. Error (MC-56) replaces the grid, closes the panel, clears the selection and disables CSV. Zero rows keeps the header (sort inert, details buttons live) and shows one full-width left-aligned row "No rows matched." (MC-52) over three faint `--rule` lines (the empty-state moment). No result set shows MC-53 with no header.

### 4. Column details panel (R12)

**Placement and size.** >= 1100 px: docked right inside the Results frame, 280 px wide, `--surface`, split from the grid by a vertical hairline (never a second frame), full height of the body, scrolls inside. It takes width from the grid, not height, so the row budget holds. < 1100 px: stacked under the grid, full width, max 220 px tall, own scroll; the grid keeps the rest (at least 5 rows). Entering motion: translate 8 px plus fade, 150 ms.

**Content, four groups (Cowan).**
1. Title MC-60 (`Column details: {col} · {kind}`), as the panel's heading (focus lands here), and a close button (MC-95 "Close").
2. Counts: Non-null, Nulls, Distinct (right-aligned mono, separators on the figures).
3. Range (kinds `number` and `date` only): Min, Max, and Mean for numbers. Mean rounds to 2 decimals when |mean| >= 1, otherwise to 4 significant digits (never shows 0.00 for 0.0042). Min and Max show the cell formatting of the column.
4. Top values: the five most frequent non-null values (ties by value), each as `value`, a bar and its count; the bar length is count divided by the number of returned rows, starting at zero on a shared baseline, so lengths read as shares. If more distinct values exist, a muted line DS-12 "{k} more values". Numbers only: a histogram below it (rules below).
Footer: MC-62, or MC-63 when capped.

**Histogram (numbers only).** Equal-width bins between min and max: one bin per value when there are 10 or fewer distinct integers, otherwise 10 bins (last bin includes the max). Bar height is the bin count on a zero baseline; the tallest bin fills the 80 px area; a bin with a nonzero count is at least 1 px tall and an empty bin has no bar (so small counts stay visible and zeros stay zero). Min and Max labels sit at the two ends. `role="img"` with the text alternative DS-10. Bars use `--data-1` only.

**Per-kind and edge behavior.**

| Case | Panel shows |
|------|-------------|
| `number` | all four groups and the histogram |
| `date` | counts, range (min, max), top values; no mean, no histogram |
| `bool` | counts and top values (`true`, `false`) |
| `text` | counts and top values; no range (alphabetical min/max is not useful) |
| `json` | counts and top values (by compact text); MC-66 in place of range and histogram |
| `mixed` | counts, DS-03 breakdown line under the title, top values; MC-66 in place of range and histogram; no sort or chart implication of a numeric type |
| all null | counts only, then MC-64; no range, top values or histogram |
| one distinct value | counts, then MC-65; the range, top values and histogram are omitted because they would only repeat that value |
| every value distinct (and more than one) | counts and range; the top-values list is replaced by DS-04; the histogram still shows for numbers |
| zero rows | counts at 0, then DS-05; footer "Based on 0 returned rows." |
| result capped at 1,000 | footer MC-63 instead of MC-62 |

**Keys and focus.** Opens only from the details button or Shift+Enter on a header (never from the sort gesture); focus moves to the panel heading. Opening details for another column while open swaps the content and moves focus to the heading again. Tab moves through the close button and then on to the next region. **Esc closes the panel (precedence layer 3)** wherever focus is in Results; if focus was inside the panel it returns to the originating header cell, if it was in the grid it stays where it is. The panel closes by itself when a rerun no longer has the column (F2) and on error.

### 5. Chart (R13)

**Defaults inherited from the grid.** Controls: Type (bar, line, scatter), X, Y (MC-67). Y lists only `number` columns; X lists every column plus DS-08 "Row number". On a new result, and again whenever the selected column changes:
- Selected column is a number: Y = it. X = the first `date` column, else the first other non-number column, else DS-08.
- Selected column is not a number: X = it; Y = the first `number` column. If none exists, the empty state MC-70.
- No selection: X = the first non-number column (a `date` one first), Y = the first number column that is not X.
- Type: line when X is a `date` column and there are 3 or more rows; otherwise bar. Scatter is only chosen by the user, and its X list is restricted to number columns (when no other number column exists the Scatter option is disabled with the title DS-11).
- Changes the user makes to Type, X or Y are kept until the next result or the next change of the selected column.
- Data is the **view order**: sorting the grid reorders the bars and the line, so "sort, then chart" gives a ranked bar. The caption says when it is sorted.

**Every returned row is plotted; none are dropped to make the chart tidy.** With more than 60 categories the bars thin out and tick labels auto-skip (no rotation, no truncation below 12 characters, full value in the tooltip).

**Caption (HTML, not drawn in the canvas; replaces the in-canvas Chart.js title).** DS-06: "{Y} by {X} · {n} rows plotted"; capped: "{Y} by {X} · first 1,000 rows plotted. The result was capped."; sorted adds " · sorted by {col} ({ascending or descending})". It is the chart's live region (polite) and the canvas's text alternative is MC-73.

**Truthfulness and ink (the data-viz audit).**

| Check (source) | Spec |
|----------------|------|
| Bars start at zero (truncated-axis lie, Cairo 2019) | Bar Y axis always includes 0: min = min(0, data min), max = max(0, data max). No `grace`, no log scale. Bars are flat-topped (radius 0); length is the value. With negatives, bars grow from the zero line, which is drawn |
| One axis (dual-axis lie, Cairo 2019) | Exactly one Y axis and one X axis, one series, no right-hand axis, no secondary series, no legend (nothing to disambiguate) |
| Non-zero baseline on lines is labelled (Cairo's exception) | Line and scatter may auto-range; when the Y axis minimum is above 0 the chart shows DS-07 "Y axis starts at {min}, not zero." directly under the caption |
| No cherry-picked range | X shows the whole returned result; no zoom, no pan, no clipping of outliers |
| Line only when the order is meaningful (chart-type table) | Line is the default only for date X; otherwise bar. A line over category X is allowed by the user's choice and is not styled to imply time |
| Data-ink (Tufte 1983) | Horizontal gridlines only (scatter: both), 1 px `--rule`; no borders on the plot, no fills, no shadows, no 3D, no point glow; animation <= 150 ms and 0 under reduced motion |
| Labels and units | Both axes titled with the column names; tick figures use the grid's separators and are never abbreviated (no "1.2M"); tooltip shows X and Y with the same formatting |
| Position on a common scale (Cleveland and McGill 1984) | Bars and points are positions on one scale; no area or angle encodings, no pies |
| Truncation and sort disclosed | Capped and sorted states appear in the caption (above) |

**Ink and contrast (DW-4.3).**

| Element | Token | Check |
|---------|-------|-------|
| Bars, line, scatter points | `--data-1` (#2a78d6) only | 4.33:1 on `--background`, the chart's surface (>= 3:1, WCAG 1.4.11) |
| Histogram and top-value bars in the panel | `--data-1` | 4.18:1 on `--surface` |
| Tick labels, axis titles, caption | `--text-muted` | 5.86:1 on `--background` (>= 4.5:1) |
| Axis baseline and tick marks | `--border-control` | 3.39:1 on `--background` (>= 3:1) |
| Gridlines | `--rule` | decorative; the values are in the tooltip and the grid |
| Scatter point ring | 1 px `--background` | separates overlapping points without alpha |

The accent never encodes data: no accent bar, no highlighted bar for the selected column, no accent line. The selected column is shown in the grid only. The 4.33 and 4.18 ratios were computed from the DESIGN.md hex values.

**Chart states** (extends R13): empty reasons MC-68 to MC-71; Chart.js missing MC-72; after a run error the chart shows MC-68 (the grid and the chart agree that there is no result). While a run is in flight the chart is dimmed like the grid. Selects are native; the canvas is `role="img"`. X, Y or Type changes redraw instantly (no transition beyond 150 ms) and announce the new caption.

### 6. Profile tab (R14)

The whole table, from the server, and it says so: a scope line above the grid, **DS-09**: "Whole table · {rows} rows · {cols} columns. Computed by the server, not from your query result." (12/16, `--text-muted`, one line, shown in the tab's body not in a notice strip). The rest uses the same grid component, read-only:
- Columns as today (type, null %, approx distinct, min/max, mean, std, quartiles); the server's types are shown in their own column, so the header carries no kind hint and no details button.
- Min and max cells are text-aligned left whatever they hold (a table's columns have different types); the numeric statistics follow the number rules (right-aligned, separators); null statistics (for example min of an all-null column) show the `null` token.
- Sorting, cell focus, popover and copy work as in section 3 (same keys; ⌘C on a header copies the name). No selected column, no panel, no CSV (hidden on Profile, R9).
- States: MC-75, MC-76, MC-77 as in R14. A table with zero rows still lists every column, with 0 rows in the scope line and null tokens in the statistics. Switching table resets sort and focus.
- The Profile tab does not follow the query result: after an example query the tab says "Select a table to profile it" (MC-75) rather than showing a stale table.

### 7. Edge-case matrix (DW-4.1)

| Case | Grid and sort | Column panel | Chart | Header status, notice, CSV |
|------|---------------|--------------|-------|----------------------------|
| **All-null column** | Kind `null`, hint "null"; every cell the `null` token; sort is allowed and changes nothing | Counts (0 non-null, N nulls, 0 distinct), then MC-64; nothing else | Not offered as Y or X-default (it is not a `number`); can still be chosen as X (all "null" categories, a single bar) | Unchanged |
| **Single distinct value** | Normal; sort changes nothing visible | Counts, then MC-65; range, top values and histogram omitted | As Y: bars of equal height, axis includes 0 so equal bars are drawn truthfully; as X: one category | Unchanged |
| **Mixed numeric and text** | Kind `mixed`, hint "mixed"; left-aligned, no separators on its numbers; sort puts numbers first (by value), then text | DS-03 breakdown, counts, top values, MC-66; no range or histogram | Excluded from Y (needs every non-null value numeric); allowed as X (categories as text) | Unchanged |
| **1,000-row truncation** | Header says "1,000+ rows" (MC-45); strip MC-50 always shown; sort is over those rows; the row range readout reads up to 1,000 | Footer MC-63 | Caption states the first 1,000 rows were plotted; sorted state is also named | CSV downloads the returned rows, not the full result |
| **Zero rows** | Header row stays, "No rows matched." (MC-52), sort inert | Opens; counts 0, DS-05, footer "Based on 0 returned rows." | MC-69; controls disabled | Status MC-44; CSV enabled (header-only file); no range readout |

Also covered: no result set (grid MC-53, panel unavailable because no header exists, chart MC-71, CSV disabled MC-48); error (grid MC-56, panel closes, chart MC-68, CSV disabled); leading-zero numeric strings (text, not numbers); huge integers (digit-grouped without precision loss); null sorting (always last); capped result with an active sort (both notices, one strip, up to two lines).

### 8. Keyboard and Esc consolidation

Nothing here adds an Esc layer. Esc closes one layer per press, in the page spec's order: (1) the cell popover, (3) the column panel, (4) cancel an in-flight Run. With the popover and the panel both open, the first Esc closes the popover, the second the panel. Grid keys are in section 3. `/` still focuses Ask or the editor (the grid is not a text field). Reading order and tab order are unchanged: tabs, then the grid (one stop), then the panel. Targets are at least 24 px (details button 24, sort target is the full header cell).

### 9. New strings (merge into `## Microcopy` in Phase 5)

Same voice: calm, precise, plain; sentence case; "·" is the only status separator.

| ID | Where · state | Exact string | Tone |
|----|--------------|--------------|------|
| DS-01 | R9/R11 · scroll range readout (aria-hidden) | Rows {a} to {b} | neutral |
| DS-02 | R11 · copy on a null cell (toast) | That cell is null, so nothing was copied. | neutral |
| DS-03 | R12 · mixed column | Mixed: {a} numeric, {b} text. | neutral |
| DS-04 | R12 · every value distinct | Every value is distinct, so no value repeats. | calm |
| DS-05 | R12 · zero rows | The result has no rows, so there is nothing to summarize. | calm |
| DS-06 | R13 · caption | {Y} by {X} · {n} rows plotted. Capped: {Y} by {X} · first 1,000 rows plotted. The result was capped. Sorted adds: · sorted by {col} ({ascending or descending}) | neutral |
| DS-07 | R13 · non-zero baseline | Y axis starts at {min}, not zero. | neutral |
| DS-08 | R13 · X option | Row number | neutral |
| DS-09 | R14 · scope line | Whole table · {rows} rows · {cols} columns. Computed by the server, not from your query result. | neutral |
| DS-10 | R12 · histogram text alternative | Histogram of {col}: {k} bins from {min} to {max}. The fullest bin, {lo} to {hi}, has {count} rows. | neutral |
| DS-11 | R13 · Scatter disabled (title) | Scatter needs a second numeric column for X. | neutral |
| DS-12 | R12 · top values overflow | {k} more values | neutral |

### 10. Checks

- DW-4.1: the five plan edge cases are each filled across grid, panel, chart and status in the matrix (section 7); no cell is left blank.
- DW-4.2: bars include zero, one axis, one series, non-zero line baselines labelled, nothing dropped, capped and sorted data disclosed (section 5 audit table).
- DW-4.3: only `--data-1` encodes data; contrast values are listed in the ink table; the accent appears on selection and focus in the grid, never in a chart or the panel's bars.
- Density: 15 full rows at 1440 x 900 with Ask on (arithmetic in section 2, measured on the mock), grid scrolls in its own container with sticky header, and the scroll cues are specified.
- Open risk: kinds are inferred from at most 1,000 values, so a column whose first 1,000 values look numeric but later values do not is only caught if those values were returned. Adding DuckDB types to the query payload would remove the guess; it needs a backend change and is not specified here.
