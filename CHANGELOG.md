# Changelog

Format: [Keep a Changelog](https://keepachangelog.com). Newest first.

## [Unreleased]

### Added
- Demo data for every format (`demo/`: sales CSV, employees XLSX, products JSON, events NDJSON), loaded into a `demo` schema on startup.
- Sidebar sections for demo tables, your tables, and six one-click example queries (nested fields, `unnest`, cross-format join).
- Clicking a table shows its profile and runs a 100-row preview; the page opens on `demo.sales`.
- README, ARCHITECTURE and CHANGELOG docs, plus a `CLAUDE.md` rule to keep them current with every commit and push.

## [0.1.0] - 2026-10-07

### Added
- Upload CSV, JSON, NDJSON/JSONL and XLSX into DuckDB tables.
- Auto profile per table (`SUMMARIZE`).
- SQL query box with a 1,000-row cap and timing.
- Bar, line and scatter charts of query results.
- Self-check: `python app.py check`.
