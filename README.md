# Cloudstone

A local data workbench: upload structured and semi-structured files, then profile, query and chart them in the browser. Backed by [DuckDB](https://duckdb.org).

## Features

- **Demo data** for every supported format, read-only and open to everyone (no login needed), plus one-click example queries in the sidebar:

  | Table | Source file | Shape |
  |-------|-------------|-------|
  | `demo.sales` | `demo/sales.csv` | Flat table: 120 orders |
  | `demo.employees` | `demo/employees.xlsx` | Spreadsheet: 8 staff (joins to sales via `rep_id`) |
  | `demo.products` | `demo/products.json` | JSON array: nested `specs` object, `tags` list, `variants` list of objects |
  | `demo.events` | `demo/events.ndjson` | NDJSON: 200 web events, nested `user`/`context`, optional `query` and `items` fields |
- **Accounts** — sign up, log in, log out, change password, delete account. Each user's uploads are saved in their own database and survive restarts.
- **Upload** (logged in) CSV, JSON, NDJSON/JSONL and XLSX (several at once). Each file becomes a table named after the file under **Your tables**; re-uploading replaces it.
- **Structured + nested data** — column types are inferred, and nested JSON is queryable directly (`SELECT context.page FROM demo.events`).
- **Auto profile** — per column: type, null %, approx distinct count, min/max, mean, std, quartiles.
- **Ask in plain English** — type a question ("Which sales rep sold the most speakers?"); Claude writes the SQL, it runs, and you see the results, the SQL and a one-line explanation. Edit the SQL and press Run to refine. Works on demo data and your own tables.
- **SQL box** — any DuckDB SQL over the demo tables and your own, results capped at 1,000 rows, with timing.
- **Charts** — bar, line or scatter from the last query result; pick the X and Y columns.
- Light/dark mode, works at phone width.

## Setup

Requires Python 3.10+.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

## Claude API key (for plain-English questions)

Asking in plain English calls the Claude API. Everything else works without it.

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Set it in the shell you start the server from. Each question is one request to `claude-opus-5-5` and sends Claude your question, the names and types of every table you can see, and 3 sample rows of each.

## Run

```bash
.venv/bin/python app.py
```

Open http://127.0.0.1:8000. The page opens on `demo.sales`; click any table to see its profile and first 100 rows. Sign up in the sidebar to upload your own files.

All runtime data lives in `data/` (git-ignored): accounts in `data/auth.sqlite3`, each user's tables in `data/users/u<id>.duckdb`. Delete `data/` to reset everything.

## Check

```bash
.venv/bin/python app.py check
```

Prints `ok` when loading, profiling, querying, accounts, per-user isolation and plain-English questions all work. The check uses a stand-in for the Claude API, so it needs no key and costs nothing.

## Security

- Passwords are hashed with scrypt and a per-user salt. Sessions are random tokens, stored hashed, sent as `HttpOnly; SameSite=Strict` cookies, valid 30 days.
- 5 failed logins lock that username for 15 minutes.
- Each user's SQL runs in their own DuckDB with file, network and extension access turned off, so it can't read other users' data or files on disk. Demo data is attached read-only.
- Cross-origin POSTs are refused.
- SQL written by Claude runs in a transaction that's always rolled back, so a question can't change or delete data.

## Limits

- Excel: first sheet only.
- Runs on localhost over plain HTTP. Put it behind HTTPS (and add `Secure` to the cookie) before exposing it to a network.
- No password reset by email: a forgotten password means a new account.
- No delete/export buttons yet. Drop tables with SQL (`DROP TABLE x`); export isn't possible because SQL file access is disabled.
- Uploads are capped at 200 MB.
- Logged-out visitors can ask questions too, and every question is billed to the server's API key. Fine on localhost; add a login requirement or rate limit before exposing it.
- Questions don't carry context: each one is answered on its own, without the previous question.

See [ARCHITECTURE.md](ARCHITECTURE.md) for how it works and [CHANGELOG.md](CHANGELOG.md) for history.
