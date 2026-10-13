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
| `index.html` | Whole UI: plain HTML/CSS/JS, no build step. Chart.js from cdnjs, Inter and JetBrains Mono from Google Fonts (falls back to system fonts offline). Light theme only; colors are CSS variables on `:root`. |
| Claude | Turns questions into SQL in `ask()`: through the local Claude Code CLI on your Claude plan (`subscription` mode) or the `anthropic` SDK with an API key (`api` mode). |
| `demo/` | Demo files, one per supported format. Rebuilt into `data/demo.duckdb` on every start. |
| `data/` | All runtime state, git-ignored. Created on first run. |
| `JOURNEY.md` | Design contract for the UI: the analyst's job, flows and the Workbench page spec (regions, states, keyboard). |
| `DESIGN.md` | Visual identity ("Verdigris Ledger") and the light-only CSS token block the UI uses. Locked on 2026-10-13 after the user approved the mock. |
| `.design-foundations/` | The design-for-ai workflow's research brief, phased plan, per-phase build/review reports and dealer ledger. |

## HTTP API

| Method | Path | Auth | Body / query | Returns |
|--------|------|------|--------------|---------|
| GET | `/` | | | `index.html` |
| GET | `/me` | | | `{user: name or null, ask: true/false}`; the page hides the Ask box when `ask` is false |
| GET | `/tables` | | | `["demo.sales", ..., "my_upload"]`: demo tables first, then your own |
| GET | `/profile` | | `?table=name` | `{columns, rows, truncated}` from `SUMMARIZE` |
| POST | `/query` | | `{"sql": "..."}` | `{columns, rows, truncated}` |
| POST | `/ask` | | `{"question": "..."}` | `{sql, explanation, columns, rows, truncated, error?}`; `error` is set when the generated SQL fails. 403 when Ask is off |
| POST | `/signup` | | `{username, password}` | `{user}` + session cookie |
| POST | `/login` | | `{username, password}` | `{user}` + session cookie |
| POST | `/logout` | ✓ | `{}` | `{user: null}`, clears cookie |
| POST | `/password` | ✓ | `{old, new}` | `{user}` + new cookie; all other sessions end |
| POST | `/account/delete` | ✓ | `{password}` | `{user: null}`; user's database and uploads deleted |
| POST | `/upload` | ✓ | `?name=file.ext`, raw file bytes | `{table, profile}` |

Errors return JSON `{"error": "..."}`: 400 bad input, 401 not logged in or wrong password, 403 cross-origin or locked out, 413 body over 200 MB, 502 Claude API failure (missing key, rate limit, outage). Values JSON-encode with `default=str` (dates, decimals, UUIDs become strings; structs and lists stay JSON).

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
   - `.json` / `.ndjson` / `.jsonl` → `read_json_auto` (nested objects become `STRUCT`, arrays become `LIST`; a field whose type differs between records becomes `JSON`)
   - `.xlsx` → openpyxl converts the first sheet to CSV, then `read_csv_auto`
   - `.parquet` → `read_parquet`
   - `.log` → `read_text`, split on `\r?\n` into rows `(line_no, line)`; trailing newlines are dropped, blank lines inside are kept
3. `CREATE OR REPLACE TABLE main."<name>" AS SELECT * FROM <reader>`, then the temp dir is removed. The name comes from `table_name()`: lowercase, non-word characters become `_`, and names starting with a digit get a `t_` prefix.
4. The response includes the profile, so the UI renders it without another request.

## Plain-English questions

`ask_mode()` reads `CLOUDSTONE_ASK`: `off` (default), `subscription` or `api`; any other value stops the server at startup. Off means the Ask box is hidden and `/ask` returns 403 without contacting Claude.

1. `describe()` lists every table the request's connection can see (demo plus the user's own), with column names, DuckDB types (nested `STRUCT`/`LIST` types included) and 3 sample rows, truncated to 1,500 characters per table.
2. The schema and question go to Claude with the same system prompt (one read-only DuckDB query, nested-field and `unnest` syntax, empty `sql` when the data can't answer) and the same JSON schema `{sql, explanation}`:
   - **`subscription` → `via_claude_code()`** runs `claude -p` with the prompt on stdin and `--output-format json --json-schema … --system-prompt …`, plus `--tools ""` (no tools), `--strict-mcp-config`, `--setting-sources project` and an empty temp working dir (no plugins, hooks, MCP servers or CLAUDE.md), and `--no-session-persistence`. Every `ANTHROPIC_*` / `CLAUDE*` environment variable is removed, so Claude Code can only use its own login, the user's Claude plan. The answer is read from `structured_output`; `is_error` (not logged in, usage limit reached), a missing `claude` binary and a 3-minute timeout become 400s with Claude Code's message.
   - **`api` → `via_api()`** calls `claude-opus-5-5` through the `anthropic` SDK with `output_config.format` (the JSON schema), `effort: "medium"`, and `fallbacks: "default"` (beta `server-side-fallback-2026-07-01`: if Opus's safety classifiers decline, the API retries on Anthropic's recommended fallback model). Refusals and cut-off replies become 400s.
3. `ask()` runs the SQL on the same connection inside `BEGIN TRANSACTION … ROLLBACK`, so even a bad `DELETE` changes nothing. A failing query returns its SQL plus `error` so the user can fix it.
4. The page shows the explanation, puts the SQL in the SQL box, and renders the result and chart like any other query.

The self-check passes stand-ins for the SDK client and for `subprocess.run`, so it tests both modes (prompt contents, the cleaned environment, no tools, rollback, errors, refusals, usage-limit and not-logged-in failures) without contacting Claude.

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
- **Claude writes SQL, DuckDB answers:** the model never sees full tables, only schema and samples, and the user can read and edit the exact query that produced the answer.
- **Stdlib server, no framework:** a dozen routes don't need one. Raw-body uploads avoid multipart parsing.
- **Single-threaded server:** fine for local use. Upgrade path: `ThreadingHTTPServer` plus `cursor()` per request. `USER_DBS` never closes idle connections; add an LRU if many users are active.
- **Results capped at 1,000 rows** (`MAX_ROWS`) to keep the browser responsive.
- **Bound to 127.0.0.1, plain HTTP:** exposing it needs HTTPS in front and a `Secure` cookie flag.
