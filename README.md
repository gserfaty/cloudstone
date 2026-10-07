# Cloudstone

A local data workbench: upload structured and semi-structured files, then profile, query and chart them in the browser. Backed by [DuckDB](https://duckdb.org).

## Features

- **Demo data** for every supported format, loaded into a read-only-by-convention `demo` schema on startup, plus one-click example queries in the sidebar:

  | Table | Source file | Shape |
  |-------|-------------|-------|
  | `demo.sales` | `demo/sales.csv` | Flat table: 120 orders |
  | `demo.employees` | `demo/employees.xlsx` | Spreadsheet: 8 staff (joins to sales via `rep_id`) |
  | `demo.products` | `demo/products.json` | JSON array: nested `specs` object, `tags` list, `variants` list of objects |
  | `demo.events` | `demo/events.ndjson` | NDJSON: 200 web events, nested `user`/`context`, optional `query` and `items` fields |
- **Upload** CSV, JSON, NDJSON/JSONL and XLSX (several at once). Each file becomes a table named after the file under **Your tables**; re-uploading replaces it.
- **Structured + nested data** — column types are inferred, and nested JSON is queryable directly (`SELECT context.page FROM demo.events`).
- **Auto profile** — per column: type, null %, approx distinct count, min/max, mean, std, quartiles.
- **SQL box** — any DuckDB SQL, results capped at 1,000 rows, with timing.
- **Charts** — bar, line or scatter from the last query result; pick the X and Y columns.
- Light/dark mode, works at phone width.

## Setup

Requires Python 3.10+.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

## Run

```bash
.venv/bin/python app.py
```

Open http://127.0.0.1:8000. The page opens on `demo.sales`; click any table to see its profile and first 100 rows. Your uploads persist in `data.duckdb` (git-ignored).

## Check

```bash
.venv/bin/python app.py check
```

Prints `ok` when loading, profiling and querying all work.

## Limits

- Excel: first sheet only.
- Single user, localhost only, no auth. The SQL box can run any statement, including `DROP`.
- No delete/export buttons yet; use SQL (`DROP TABLE x`, `COPY x TO 'x.parquet'`).
- Demo tables can be modified or dropped with SQL; they're reloaded from `demo/` on every restart.

See [ARCHITECTURE.md](ARCHITECTURE.md) for how it works and [CHANGELOG.md](CHANGELOG.md) for history.
