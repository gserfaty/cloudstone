# Architecture

Two code files, one process, one DuckDB file per user.

```
browser (index.html) ──fetch + session cookie──▶ app.py (http.server)
                                                   ├─▶ data/auth.sqlite3        users, sessions
                                                   ├─▶ data/demo.duckdb         demo tables (read-only)
                                                   └─▶ data/users/u<id>.duckdb  one per user, demo attached read-only
```

## Components

| File | Role |
|------|------|
| `app.py` | Stdlib `HTTPServer` on `127.0.0.1:8000`. Serves the page, accounts, uploads, queries. Also holds the self-check (`python app.py check`). |
| `index.html` | Whole UI: plain HTML/CSS/JS, no build step. Chart.js loaded from cdnjs. |
| `demo/` | Demo files, one per supported format. Rebuilt into `data/demo.duckdb` on every start. |
| `data/` | All runtime state, git-ignored. Created on first run. |

## HTTP API

| Method | Path | Auth | Body / query | Returns |
|--------|------|------|--------------|---------|
| GET | `/` | | | `index.html` |
| GET | `/me` | | | `{user: name or null}` |
| GET | `/tables` | | | `["demo.sales", ..., "my_upload"]`: demo tables first, then your own |
| GET | `/profile` | | `?table=name` | `{columns, rows, truncated}` from `SUMMARIZE` |
| POST | `/query` | | `{"sql": "..."}` | `{columns, rows, truncated}` |
| POST | `/signup` | | `{username, password}` | `{user}` + session cookie |
| POST | `/login` | | `{username, password}` | `{user}` + session cookie |
| POST | `/logout` | ✓ | `{}` | `{user: null}`, clears cookie |
| POST | `/password` | ✓ | `{old, new}` | `{user}` + new cookie; all other sessions end |
| POST | `/account/delete` | ✓ | `{password}` | `{user: null}`; user's database and uploads deleted |
| POST | `/upload` | ✓ | `?name=file.ext`, raw file bytes | `{table, profile}` |

Errors return JSON `{"error": "..."}`: 400 bad input, 401 not logged in or wrong password, 403 cross-origin or locked out, 413 body over 200 MB. Values JSON-encode with `default=str` (dates, decimals, UUIDs become strings; structs and lists stay JSON).

## Which database a request uses

Every request looks up the `cs_session` cookie. Without a valid session it uses the shared anonymous connection (`demo.duckdb` opened read-only), so `/tables`, `/profile` and `/query` only see demo data. With a session it uses that user's connection from `user_db()`, opened on first use and kept in `USER_DBS`.

`user_db()` opens `data/users/u<id>.duckdb`, attaches `demo.duckdb` as catalog `demo` (read-only), allows reads only from `data/uploads/<id>/`, then calls `sandbox()`: `enable_external_access = false` and `lock_configuration = true`. After that, SQL can't read or write other files, attach other databases, install extensions, or undo those settings. The anonymous connection gets the same sandbox with no readable directory.

## Tables and names

- Uploads go into the user database's `main` schema and are named without a prefix (`my_upload`).
- Demo tables live in the `demo` catalog (`demo.sales`). `build_demo()` deletes and recreates `demo.duckdb` on startup using the same `load()` path as uploads, so demo data exercises every reader.
- `tables()` returns qualified names. `profile()` only accepts a name from that list, and `ident()` quotes it (`"demo"."sales"`) for SQL.

## Upload flow

1. The browser POSTs the raw file (no multipart) with its name in the query string. Requires a session.
2. `load()` writes the bytes to a temp dir inside `data/uploads/<id>/` (the only directory that user's sandbox can read), picks a reader by extension:
   - `.csv` → `read_csv_auto`
   - `.json` / `.ndjson` / `.jsonl` → `read_json_auto` (nested objects become `STRUCT`, arrays become `LIST`)
   - `.xlsx` → openpyxl converts the first sheet to CSV, then `read_csv_auto`
3. `CREATE OR REPLACE TABLE main."<name>" AS SELECT * FROM reader(path)`, then the temp dir is removed. The name comes from `table_name()`: lowercase, non-word characters become `_`, and names starting with a digit get a `t_` prefix.
4. The response includes the profile, so the UI renders it without another request.

## Accounts

- `data/auth.sqlite3` (stdlib `sqlite3`, kept apart from DuckDB so no user SQL can reach it):
  - `users(id, username UNIQUE COLLATE NOCASE, salt, pw_hash, created_at)`
  - `sessions(token_hash, user_id → users ON DELETE CASCADE, expires_at)`
- Usernames: 3-32 of `A-Z a-z 0-9 . _ -`, case-insensitive. Passwords: 8-128 characters.
- Passwords: `hashlib.scrypt` (n=2^14, r=8, p=1) with a 16-byte random salt, compared with `hmac.compare_digest`. Unknown usernames are hashed too, so timing doesn't reveal which usernames exist.
- Sessions: `secrets.token_urlsafe(32)` in an `HttpOnly; SameSite=Strict` cookie; only its SHA-256 is stored. 30-day expiry; expired rows are deleted on lookup.
- Lockout: `FAILS` counts failures per username in memory; 5 within 15 minutes locks it until the window passes. Resets on success or restart.
- POSTs with an `Origin` header that doesn't match `Host` are refused (on top of `SameSite=Strict`).

## Design decisions

- **DuckDB over SQLite/Postgres for data:** schema inference for CSV/JSON, native nested types, fast analytics, embedded (no server).
- **One DuckDB file per user:** isolation comes from separate files plus the sandbox instead of row-level permissions in a shared database, and deleting an account is deleting a file.
- **SQLite for accounts:** stdlib, and out of reach of user SQL.
- **Stdlib server, no framework:** a dozen routes don't need one. Raw-body uploads avoid multipart parsing.
- **Single-threaded server:** fine for local use. Upgrade path: `ThreadingHTTPServer` plus `cursor()` per request. `USER_DBS` never closes idle connections; add an LRU if many users are active.
- **Results capped at 1,000 rows** (`MAX_ROWS`) to keep the browser responsive.
- **Bound to 127.0.0.1, plain HTTP:** exposing it needs HTTPS in front and a `Secure` cookie flag.
