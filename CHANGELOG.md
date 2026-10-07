# Changelog

Format: [Keep a Changelog](https://keepachangelog.com). Newest first.

## [Unreleased]

### Added
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
- Plain-English questions are off by default: the Ask box is hidden and `/ask` returns 403 until the server is started with `CLOUDSTONE_ASK=api`. Nothing can be billed by accident.
- SQL runs sandboxed: no file, network or extension access, so `COPY ... TO` and reading arbitrary files no longer work.
- Logged-out visitors can browse and query demo data but not upload.
- Demo data now lives in a read-only `data/demo.duckdb`, attached to every user's database as `demo`.

### Removed
- The single shared `data.duckdb`. Uploads made before accounts aren't migrated; re-upload them after signing up.

## [0.1.0] - 2026-10-07

### Added
- Upload CSV, JSON, NDJSON/JSONL and XLSX into DuckDB tables.
- Auto profile per table (`SUMMARIZE`).
- SQL query box with a 1,000-row cap and timing.
- Bar, line and scatter charts of query results.
- Self-check: `python app.py check`.
