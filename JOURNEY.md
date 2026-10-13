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
5. Optional: sort a column (click or Enter on the header label; cycle ascending, descending, original). If results were capped, the notice strip says the sort covers only the returned rows and suggests `ORDER BY`.
6. (Exit) **Outcome (visible):** new result in the grid with row/time status, a new top entry in History.
- DDL or statements with no result set: grid area shows "no result set" empty state, status shows success, CSV disabled.

### F3. Ask, then refine
1. (Entry) Ask card visible only if the server has Ask on. Type a question or click one of 4 suggestion chips (Hick: chips capped at 4).
2. Ask button busy; explanation line says Claude is writing a query.
3. Decision: Ask succeeded?
   - Yes, SQL ran: worksheet filled with the SQL, explanation shown, Results tab selected with the rows; history row records the question and the SQL.
   - SQL generated but failed: worksheet filled, explanation shown, error shown in status/Results; user edits and runs (continue as F2).
   - Request failed (limit reached, Ask off, network): error in the explanation line; worksheet unchanged.
4. Action: edit the generated SQL and Run.
5. (Exit) **Outcome (visible):** editable SQL in the worksheet plus either results or a clear error; the refined run appears in History marked as an edit of an Ask run only by its own SQL (no hidden linkage).
- Ask off: the card is absent, a hint under the Worksheet title says how to enable it, `/` goes to the editor.

### F4. Upload when logged out
1. (Entry) Click or drop files on the drop zone while logged out. The zone's label reads "Log in to upload".
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
- States: **empty** n/a - idle is its normal state. **loading** per-file toast "Uploading name..." (zone stays usable for more files). **error** per-file error toast naming the file. **logged out** title reads "Log in to upload"; click or drop opens Auth in Sign up mode and sends nothing (F4). **Ask off** n/a - unaffected. Drag-over: zone shows a drop-target state.
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
  - **logged out:** `my_data` is shown with "Log in to upload and keep your own tables."; demo tables fully usable.
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
  - **error:** explanation line in error style: what happened, why, how to fix (Phase 3 words).
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
- States: **empty** before any run: status blank, CSV disabled; no-result-set statement: status reads "Statement ran, no result set" with ok mark, CSV disabled; zero rows: status "0 rows - N ms", CSV enabled (header-only file). **loading** status "Running..." and tabs stay usable. **error** error mark and message. **logged out** same. **Ask off** same.
- Keys: arrow keys move between tabs and activate (existing behavior); CSV is a button, disabled when no result set; hidden on Profile.
- Cut: 3 tabs, 2 actions; status is plain text, not three badges (Hick).

##### R10 Notice strip (Results tab, above the grid)
- Content: shown only when needed: (a) truncation "Showing the first 1,000 rows" + "Sorting and column stats cover only these rows; add ORDER BY or LIMIT in SQL" (b) sort active "Sorted by col (ascending)" with a clear control.
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
| R2 Drop zone | idle | per-file toast | per-file toast | "Log in to upload" -> Auth | no effect |
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
