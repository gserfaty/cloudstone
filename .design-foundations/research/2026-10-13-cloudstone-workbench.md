# Cloudstone workbench: UI/UX brief

**Summary:** Make Cloudstone's single-page workbench feel like a precise, calm daily tool for analysts, with its own identity, a much stronger results area, and query history.

- **Date:** 2026-10-13
- **Status:** confirmed for planning. Items marked **(D)** are researcher defaults that settle cold-read findings; the user reviews them on real pixels at the mock sign-off gate.

## Open questions

1. **Visual identity.** The current look borrows Snowsight's navy bar and Snowflake blue and reads as generic. What is Cloudstone's own signature (a hue, a type pairing, a detail) that stays calm and precise? Resolve in the design DNA step, within these limits:
   - **(D)** The identity hue *is* the UI accent (selection, focus, the one primary action).
   - **(D)** It must be clearly distinct from the chart's data color (validated series-1 blue `#2a78d6`), so the interface never reads as data.

## Decisions (researcher defaults)

- **(D) Snowsight is a structural and interaction reference only:** worksheet over results, a column-detail panel and query history. Its brand (navy bar, Snowflake blue) is *not* a reference.
- **(D) Feel, made concrete:**
  - **Type:** Inter for the UI and JetBrains Mono for SQL and data, with a 4-step size scale of 12 / 13 / 14 / 16 px. Weights are 400 and 600 only, plus 500 for buttons.
  - **Spacing:** a 4 px grid.
  - **Motion:** 150 ms or less, opacity and transform only.
  - **Borders:** 1 px hairlines rather than shadows for structure; shadows only on floating layers (dialogs, popovers, toasts).
  - **Color:** neutrals do the structural work, and accent coverage stays under 5% of the screen.
- **(D) Density:**
  - Grid rows are 30–32 px with 13 px data text.
  - At least 15 result rows are visible at a 1440×900 viewport with the editor at its default height.
  - Elsewhere, roomy spacing stays.
- **(D) Per-column stats:**
  - **Wide screens (≥ 1100 px):** clicking a column header opens a column-detail panel docked on the right *inside the results card*, the way Snowsight does it. It shows type, non-null count, nulls, distinct count, min, max, mean (numeric only), top values with bars, and a small histogram (numeric only).
  - **Narrower screens:** the panel stacks below the grid.
  - **Data source:** stats are computed in the browser over the returned rows (up to 1,000) and labelled "based on N returned rows".
  - **The Profile tab stays** as the whole-table profile from the server.
- **(D) One results experience:** a single results card whose header carries status (✓/✗, rows, time) and the tabs (Results / Chart / Profile), with the column panel available in Results. The chart's column choice starts from the column selected in the grid, so the views share one notion of "the column I'm looking at".
- **(D) Comparing results is out of scope** apart from reloading an earlier query from history. The JTBD is iterate and return, not side-by-side comparison.
- **(D) Query history:**
  - **Storage:** browser `localStorage` only, so there's no backend change. Last 100 entries; each keeps the SQL, the Ask question if it came from Ask, ok/error, rows, duration and timestamp.
  - **Placement:** a "History" view in the left sidebar, beside the explorer (Explorer | History switch).
  - **Use:** click to load into the worksheet, or use a rerun button. A "Clear history" control is included.
  - **Shared:** one history per browser, shared by logged-in and logged-out use. That's acceptable for a local single-user tool, and the README must say so.
- **(D) Sorting:** clicking a header sorts the returned rows in the browser (ascending → descending → original). When results were capped at 1,000, a note says the sort covers only the returned rows and suggests `ORDER BY`.
- **(D) Cell formatting:**
  - **Numbers:** right-aligned with tabular figures. Floats and integers ≥ 10,000 get en-US thousands separators, except columns whose name is `id`, ends in `_id`, or is `year`. Decimals show as returned.
  - **Dates and timestamps:** ISO, as returned.
  - **`null`:** a muted italic token.
  - **Nested JSON:** mono, truncated, with a type hint such as `{…}` or `[3]`.
  - **Long text:** ellipsis.
  - **Full value:** on hover (title) and in a cell popover on click or Enter.
  - **Copy:** ⌘C / Ctrl+C on a focused cell copies the full raw value through the Clipboard API (localhost is a secure context), with a toast to confirm.
- **(D) Keyboard model for new parts:**
  - **Grid:** a single tab stop. Arrow keys move the focused cell, Enter opens the cell popover, ⌘C copies, and Enter on a header cell sorts.
  - **Column panel:** Esc closes it.
  - **History:** arrow keys move, Enter loads, ⌘↵ reruns.
- **(D) Accessibility target:** WCAG 2.2 AA (4.5:1 for text, 3:1 for UI component boundaries and focus indicators).
- **(D) Platform:**
  - **Browsers:** current evergreen Chrome, Safari, Firefox and Edge.
  - **Offline:** fonts fall back to system fonts and Chart.js is still required for the Chart tab.
  - **Narrow screens:** the results grid may scroll horizontally *inside* its own container, but the page itself never scrolls sideways.
- **(D) Secondary audience:** first-time and logged-out visitors on demo data. Example queries and suggestion chips remain their on-ramp; the redesign must not hide them, but they aren't the design target.

## What it is

A local data workbench (`index.html`, served by `app.py`). People browse demo tables (CSV, XLSX, JSON, NDJSON, messy JSON, a raw log file, Parquet), upload their own files, write DuckDB SQL in a worksheet, optionally ask in plain English (Claude writes the SQL), and read the answer as a results grid, a chart, or a per-column profile.

## Who

**Analysts who live in it**: technical, SQL-literate, using it for long focused sessions on a desktop or laptop. Keyboard-first. They run many queries in a row, compare results, and come back to earlier queries. Phone support has to keep working but isn't the design target.

## Job to be done

"When I get a new dataset, help me understand its shape and answer questions about it quickly, without leaving my flow." Today the loop is: pick a table, look at a preview and profile, write a query, read the result, tweak, repeat. The friction is in the reading and the repeating: results are hard to scan and earlier queries are gone once you run the next one.

## What's wrong today

- **Looks generic.** Clean, but it could be any admin template; nothing says "Cloudstone".
- **Results area is weak.** It's a plain grid with row numbers. There's no sorting, column types aren't shown in the header, there are no per-column stats next to the data, and numbers and dates aren't formatted. The chart and the profile feel bolted on rather than part of one results experience.

## Feel

**Precise and calm.** The reference is Snowsight (Snowflake's web UI), with Linear-like restraint: quiet neutrals, crisp type, generous but not wasteful spacing, and color used only where it carries meaning (selection, status, the one primary action, data). It should feel trustworthy and fast, never decorative.

## Scope

- **Keep** the current structure: top bar, object explorer on the left, Ask box, worksheet, and a results card with Results / Chart / Profile tabs. The user chose not to add a split layout or multiple worksheets.
- **Add query history**: recent queries with time, row count, duration and success/error, one click to rerun or load into the worksheet.
- **Strengthen results**:
  - Type-aware formatting and column types in the header.
  - Sorting.
  - Quick per-column stats.
  - Copying a cell.
  - Clear handling of nulls, nested JSON and long text.
- **Give it an identity** within the calm/precise feel.

## Constraints

- **Light mode only.** No dark theme and no theme toggle (the user's decision).
- **One `index.html`**, vanilla JS, no build step. External assets only from cdnjs (Chart.js is already there) and Google Fonts.
- **Backend:** the HTTP API in ARCHITECTURE.md stays as is. Adding a small endpoint is possible only if history goes server-side (open question 2).
- **Nothing may regress:**
  - Ask can be off, in which case it's hidden with a hint.
  - Logged-out visitors get demo data only.
  - Uploads require login.
  - Account dialogs.
  - Example queries.
  - Shortcuts: `/` and ⌘↵.
  - Accessibility: focus outlines, live regions, keyboard tabs.
  - Phone width with no horizontal scroll.
- **Everything already on the surface stays reachable:**
  - Object explorer with expandable columns.
  - Line-numbered editor.
  - CSV download.
  - Drag-and-drop upload.

## References

- **Snowsight:** worksheet over results; results with a column-detail side panel (click a column to see its distribution and stats); query history with status, duration and rows.
- **Linear:** restraint, crisp type and an accent used sparingly.

## Taste signals

- **Light only.** Locked.
- **Snowsight as the structural reference,** but not its brand colors wholesale. The user called the current Snowflake-blue/navy look generic.
- **Calm over flashy.** No gradients or decoration for its own sake.
