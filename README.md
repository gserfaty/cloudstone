# Cloudstone

A local data workbench: upload structured and semi-structured files, then profile, query and chart them in the browser. Backed by [DuckDB](https://duckdb.org).

## Features

- **Upload** CSV, JSON, NDJSON/JSONL and XLSX (several at once). Each file becomes a table named after the file; re-uploading replaces it.
- **Structured + nested data** — column types are inferred, and nested JSON is queryable directly (`SELECT meta.page FROM events`).
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

Open http://127.0.0.1:8000. Data persists in `data.duckdb` (git-ignored).

## Check

```bash
.venv/bin/python app.py check
```

Prints `ok` when loading, profiling and querying all work.

## Limits

- Excel: first sheet only.
- Single user, localhost only, no auth. The SQL box can run any statement, including `DROP`.
- No delete/export buttons yet; use SQL (`DROP TABLE x`, `COPY x TO 'x.parquet'`).

See [ARCHITECTURE.md](ARCHITECTURE.md) for how it works and [CHANGELOG.md](CHANGELOG.md) for history.
