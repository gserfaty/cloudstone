# Browser verification, 2026-10-14

Real-browser pass (Browser pane, localhost:8000). No tracked file edited; scratch HTML copies lived outside the repo and are deleted; all servers stopped; viewport reset.

## 1. Real Ask question (CLOUDSTONE_ASK=subscription)
Asked "Which region has the highest revenue?" (1 question; a 2nd would have hit the same failure, so it was skipped).
- PASS /me returned ask=subscription; Ask card shown with chips and "Answered with your Claude plan."
- PASS Loading state: Ask button became "Cancel" with spinner, explanation line "Claude is writing a query..."
- PASS Error handling: after about 6 s the card showed, in error style, "Ask could not answer. Claude Code: Failed to authenticate: OAuth session expired and could not be refreshed. Try again in a moment, or write the SQL yourself." (ASK-E8 pattern). Button reset to "Ask", question text kept, worksheet SQL untouched.
- PASS No uncaught JS errors; only the expected 400 resource log for POST /ask.
- NOT TESTED (blocked by environment): explanation text on success, SQL landing in worksheet, results/chart, history entry with the Asked line, status line. Cause: the Claude Code OAuth session on this machine is expired. Re-run `claude` login, then retest.
- Note: a failed Ask adds no history entry (consistent with spec).

## 2. Chart.js fails to load (script tag removed in scratch copy)
- PASS Page loads, demo.sales auto-opens, 100 rows, Profile works; `typeof Chart` is "undefined".
- PASS Queries still run (GROUP BY query returned 4 rows) while on the Chart tab; Results unaffected.
- PASS Chart tab shows MC-72 text exactly: "The chart did not load. Check your connection and reload the page. The Results tab still shows the rows."; canvas collapsed to 0x0; no uncaught errors or unhandled rejections.
- MINOR (spec mismatch, R13 "no controls enabled"): Type/X/Y selects are disabled, which is right, but they stay populated and visible (Type Line, X order_date, Y order_id) above the message. Code: drawChart() `typeof Chart === 'undefined'` branch / chartEmpty() (~line 1183-1186).

## 3. localStorage blocked (getter throws SecurityError)
- PASS Page loads, no console errors, demo.sales opens.
- PASS Three consecutive runs (ok, ok, error) all recorded; History tab count went 1 to 4 and rows list correctly (in memory).
- PASS Session-only notice in History: "History is not saved in this browser, so it lasts only until you close this page. Free up browser storage to keep it."
- PASS Prefs (editor height 300px, Example queries collapse) work in memory, no throw, no uncaught errors.
- MINOR: the notice is styled as an error (red) though blocked storage is not a failure of the user's query, and "Free up browser storage" is wrong advice when storage is blocked rather than full. Code: sessionOnly notice in the history renderer, `saveHist()` catch (~line 1393).
- MINOR (also seen with storage OK): pref('cloudstone.editorH', ...) stores an empty string on the first ResizeObserver callback (a localStorage entry `cloudstone.editorH: ""` was observed). Harmless because the reader checks `if (h)`. Code: ~line 1379.

## 4. Keyboard-only walk-through (1440x900, Ask off, logged out)
Real key presses via the computer tool, with focus inspected after each press. Caveat: cmd+A did not select all in the textarea (tool limitation), and the browser pane denies clipboard access, so ⌘C hit the blocked-clipboard path.
Tab order (PASS, all focus rings visible: 2 px solid green outline, or editor wrapper outline): Log in, Sign up, upload drop zone (label role=button), Explorer tab, Search tables, then each table's expander and name button, Example queries toggle, editor, Run, Results tab, CSV, grid (single stop, lands on first body cell), toast Dismiss (when a toast is visible), then wraps to Log in. History tab and Chart/Profile tabs are roving (not extra stops).
- PASS `/` from the Explorer jumps to the SQL editor (Ask off) and does not fire inside the open dialog (typed into Username).
- PASS ⌘↵ runs from the editor; errors render in the grid area and status.
- PASS Tab in editor inserts two spaces and keeps focus (trap). Esc then Tab leaves to Run (verified when no run is in flight).
- PASS Esc right after ⌘↵ while the run is in flight cancels the run first (layer 4) and the next Tab still inserts spaces, per the precedence table. Expected, but note a fast Esc-Tab can look like a stuck trap.
- PASS Grid: arrows, Home/End move cells; ArrowUp reaches the header. Enter on header cycles asc, desc, original with aria-sort and the "Sorted by region (ascending). Clear sort" strip; Space also cycles; Shift+Enter opens Column details and focus lands on its heading (panel docked right at 1440).
- PASS Esc precedence: popover closes first (panel stays), then panel; Esc inside the panel returns focus to the header cell; Esc on a focused toast dismisses it only. Enter on a cell opens the popover (fades in); its Copy button is tabindex -1 (⌘C is the keyboard path).
- PASS ⌘C triggered copy; in this pane it showed the persistent error toast MC-58 because clipboard permission is blocked. Success toast path not verifiable here.
- PASS Explorer: Up/Down move through rows and columns; Right/Left on a table name expand/collapse; Enter on an expander expands; Enter on a column inserts its name at the cursor and moves focus to the editor.
- PASS Results/Chart/Profile tabs: Right/Left activate and wrap; CSV hides on Profile; Chart renders after keyboard switch.
- PASS History: Right arrow switches sidetab, Tab goes to Clear history then the list (one stop), Down moves, Enter loads into the worksheet.
- PASS Log in dialog: Enter on trigger opens, focus lands on Username, Tab cycles inside the modal (Username, Password, Show, submit, Close, mode tabs) and wraps, Esc closes and focus returns to the Log in button.
- MINOR (R4 spec mismatch): Explorer is not a single roving stop. Every table's expander and name is its own Tab stop (14+ stops before the worksheet), though Up/Down also work. Code: explorer renderer (button[data-nav] with default tabindex), `$('explorer')` keydown ~line 1346. Spec only says Up/Down moves; keeping all as tab stops makes reaching the worksheet costly.
- MINOR (R4 spec mismatch): Right/Left work only on the table name (`.tn`), not on the expander button or a focused column row. Left on a column cannot collapse its table. Code: line ~1351 `t.classList.contains('tn')`.
- MINOR (R15): dialog Tab order puts submit before the dialog's mode tabs and Close (reads Username, Password, Show, submit, Close, then mode tabs), so keyboard users reach the Sign up tab last.
- MINOR: editor itself has no outline (outline none); focus is shown only through the wrapper (`.editor` outline), which is visible but subtle in the screenshot.
- Observation: screenshots from the pane lag by a frame or two after key presses (popover and chart tab appeared stale); verify with DOM state, not a single screenshot.

## Defects (all non-blocking; no Critical, no Major found)
1. Minor: Chart-missing state leaves Type/X/Y selects populated and visible (drawChart / chartEmpty, ~1183).
2. Minor: blocked-storage notice uses error styling and "free up storage" wording that is wrong for a blocked store (saveHist / history notice, ~1393).
3. Minor: `cloudstone.editorH` is written as "" by the ResizeObserver's first callback (~1379).
4. Minor: Explorer rows are all Tab stops instead of one roving stop (~1346).
5. Minor: Explorer Right/Left only on table-name buttons, not expander or column rows (~1351).
6. Minor: Auth dialog Tab order puts Close and mode tabs after the submit button.
7. Untested, environment: real Ask success path blocked by expired Claude Code OAuth ("Failed to authenticate: OAuth session expired"); re-login and retest (worksheet landing, history Asked line, chart).
