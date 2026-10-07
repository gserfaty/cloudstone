# Architecture

Two files, one process, one database file.

```
browser (index.html) ──fetch──▶ app.py (http.server) ──▶ DuckDB (data.duckdb)
```

## Components

| File | Role |
|------|------|
| `app.py` | Stdlib `HTTPServer` on `127.0.0.1:8000`. Serves the page, loads uploads, runs queries. Also holds the self-check (`python app.py check`). |
| `index.html` | Whole UI: plain HTML/CSS/JS, no build step. Chart.js loaded from cdnjs. |
| `data.duckdb` | All tables. Created on first run, git-ignored. |

## HTTP API

| Method | Path | Body / query | Returns |
|--------|------|--------------|---------|
| GET | `/` | | `index.html` |
| GET | `/tables` | | `["name", ...]` |
| GET | `/profile` | `?table=name` | `{columns, rows, truncated}` from `SUMMARIZE` |
| POST | `/upload` | `?name=file.ext`, raw file bytes | `{table, profile}` |
| POST | `/query` | `{"sql": "..."}` | `{columns, rows, truncated}` |

Errors return `400 {"error": "..."}`. Values JSON-encode with `default=str` (dates, decimals, UUIDs become strings; structs and lists stay JSON).

## Upload flow

1. The browser POSTs the raw file (no multipart) with its name in the query string.
2. `load()` writes the bytes to a temp dir, picks a reader by extension:
   - `.csv` → `read_csv_auto`
   - `.json` / `.ndjson` / `.jsonl` → `read_json_auto` (nested objects become `STRUCT`, arrays become `LIST`)
   - `.xlsx` → openpyxl converts the first sheet to CSV, then `read_csv_auto`
3. `CREATE OR REPLACE TABLE "<name>" AS SELECT * FROM reader(path)`. The name comes from `table_name()`: lowercase, non-word characters become `_`, and names starting with a digit get a `t_` prefix.
4. The response includes the profile, so the UI renders it without another request.

## Design decisions

- **DuckDB over SQLite/Postgres:** schema inference for CSV/JSON, native nested types, fast analytics, embedded (no server).
- **Stdlib server, no framework:** five routes don't need one. Raw-body uploads avoid multipart parsing.
- **Single-threaded server, one connection:** fine for one local user. Upgrade path: `ThreadingHTTPServer` plus `db.cursor()` per request.
- **Results capped at 1,000 rows** (`MAX_ROWS`) to keep the browser responsive.
- **Bound to 127.0.0.1:** the SQL box executes arbitrary SQL, so it must not be exposed without adding auth.
