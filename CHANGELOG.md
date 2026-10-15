# Changelog

Format: [Keep a Changelog](https://keepachangelog.com). Newest first.

## [Unreleased]

### Added
- 2026-10-14: browser verification report for the paths left untested after the redesign (Ask, Chart.js missing, blocked storage, keyboard-only): `.design-foundations/build/2026-10-14-browser-verification.md`.
- MIT license (`LICENSE`).
- Query history in the sidebar (Explorer | History): last 100 queries per account in this browser, with load, rerun and clear.
- Results grid: sorting by column name, keyboard cell navigation, a full-value popover and ⌘C / Ctrl+C copy, a sticky header and row-number column, and a "Rows a to b" readout.
- Column details panel: counts, nulls, distinct, min/max/mean, top values and a histogram over the returned rows.
- Cancel for running queries and Ask (button or Esc), and Undo when an action replaces unsaved worksheet text.
- `JOURNEY.md` `## Data surfaces`: grid, column panel, chart and profile specs with an edge-case matrix; the chart never aggregates client-side and never draws nulls as zero (design phase 4).
- `JOURNEY.md` `## Microcopy`: 104 strings for every workbench state, empty state, error and dialog (design phase 3).
- `mocks/workbench.html` (+ screenshots): styled mock of the redesigned workbench for the sign-off gate; reviewed on pixels with no Critical or Major findings.
- `DESIGN.md`: the "Verdigris Ledger" visual identity (Archivo + IBM Plex Mono, verdigris accent) with an AA-checked light token block (design phase 2; pending sign-off on the mock).
- `JOURNEY.md`: the analyst journey, flows and a full page spec for the workbench screen (design phase 1).
- Design brief and phased redesign plan under `.design-foundations/` (design-for-ai workflow: research → plan → mock → build).
- `.github/CODEOWNERS` naming @gserfaty as required reviewer, and a Contributing section in the README: changes from others go through pull requests reviewed by the owner.
- Demo data for messier formats: `customers.json` (records from 3 systems with mismatched keys and types), `web_server.log` (raw log lines) and `shipments.parquet` (joins to sales), plus four example queries showing JSON cleanup, regex log parsing and a Parquet join.
- Upload support for Parquet (`.parquet`) and log files (`.log`, one row per line).
- `CLOUDSTONE_ASK=subscription`: plain-English questions run through the local Claude Code CLI (`claude -p`), using your Claude Pro/Max plan's usage limits instead of a paid API key. Runs with no tools, no plugins or hooks, and all Anthropic/Claude environment variables removed.
- Ask questions in plain English: Claude (`claude-opus-5-5`, via the `anthropic` SDK) writes DuckDB SQL from your question and the tables you can see; the page shows the result, the SQL and a one-line explanation. Generated SQL runs in a rolled-back transaction.
- `anthropic` added to `requirements.txt`; set `ANTHROPIC_API_KEY` to use plain-English questions.
- User accounts: sign up, log in, log out, change password (ends other sessions), delete account (removes all its data).
- Per-user storage: each user's uploads persist in their own DuckDB file under `data/users/`.
- Security: scrypt password hashing, hashed session tokens in `HttpOnly; SameSite=Strict` cookies, login lockout after 5 failures, cross-origin POST refusal, 200 MB body cap.
- Demo data for every format (`demo/`: sales CSV, employees XLSX, products JSON, events NDJSON), loaded into a `demo` schema on startup.
- Sidebar sections for demo tables, your tables, and six one-click example queries (nested fields, `unnest`, cross-format join).
- Clicking a table shows its profile and runs a 100-row preview; the page opens on `demo.sales`.
- README, ARCHITECTURE and CHANGELOG docs, plus a `CLAUDE.md` rule to keep them current with every commit and push.

### Changed
- Applied the locked "Verdigris Ledger" design to the live UI (design phase 5): Archivo + IBM Plex Mono, verdigris accent, section legends on the top rule, ≥ 15 result rows visible at 1440×900, every text pair WCAG AA, all colors from the DESIGN.md token block.
- `/me` returns the Ask mode (`"off"`, `"subscription"` or `"api"`) instead of a boolean, so the page can say who pays for a question.
- Chart: one mark per returned row with no client-side aggregation, null values never drawn as zero, and both disclosed in a caption; bars have square ends.
- Logged-out upload control now reads "Sign up to upload" and opens sign-up.
- `DESIGN.md` locked: the user approved the Verdigris Ledger direction and its signature detail on the styled mock.
- Redesigned the UI after Snowflake's Snowsight: navy top bar, light cool-gray theme with a blue accent, an object explorer with expandable columns, a line-numbered worksheet, Results / Chart / Profile tabs, and dialogs for log in, sign up and account settings.
- Results grid: row numbers, right-aligned numbers, styled nulls and nested JSON, sticky header, CSV download (cells that look like spreadsheet formulas are escaped).
- Chart picks a label column for X and a numeric column for Y automatically, uses a line chart for dates, and follows single-series chart conventions (no legend, title names the measure, rounded bar ends, hover tooltips).
- Drag-and-drop upload, table search, notifications for uploads and sign-ins, loading spinners on buttons, empty states, `/` and ⌘↵ shortcuts, and focus outlines and live regions for keyboard and screen-reader users.
- Plain-English questions are off by default: the Ask box is hidden and `/ask` returns 403 until the server is started with `CLOUDSTONE_ASK=api`. Nothing can be billed by accident.
- SQL runs sandboxed: no file, network or extension access, so `COPY ... TO` and reading arbitrary files no longer work.
- Logged-out visitors can browse and query demo data but not upload.
- Demo data now lives in a read-only `data/demo.duckdb`, attached to every user's database as `demo`.

### Fixed
- 2026-10-14: The Chart tab hides its Type, X and Y controls when Chart.js fails to load, so only the message shows.
- 2026-10-14: When browser storage is blocked, History shows a neutral notice that no longer suggests freeing space; a full store keeps the free-space advice.
- 2026-10-14: The editor height is no longer saved as an empty value when it has not been resized.
- 2026-10-14: Explorer is one Tab stop with arrow keys (Right and Left expand, collapse, and return from a column); the log in dialog's Log in / Sign up control is a tablist.
- 2026-10-14: Ask now explains an expired or missing Claude Code login ("run claude in a terminal to log in again") instead of raw OAuth text and "try again in a moment".
- On phones the worksheet and results come first and the explorer moves below them, so Run is on the first screen.
- Month labels like `2026-03` count as dates, so "Revenue by month" opens as a line chart.
- Results grid groups thousands on every number of 1,000 or more (except id/year columns), so a column no longer shows `5693` next to `5,231.5`.
- Removed a stray copy of the design dealer ledger from the repo root; the full ledger is `.design-foundations/used-dna.json`.

### Removed
- The single shared `data.duckdb`. Uploads made before accounts aren't migrated; re-upload them after signing up.

## [0.1.0] - 2026-10-07

### Added
- Upload CSV, JSON, NDJSON/JSONL and XLSX into DuckDB tables.
- Auto profile per table (`SUMMARIZE`).
- SQL query box with a 1,000-row cap and timing.
- Bar, line and scatter charts of query results.
- Self-check: `python app.py check`.
