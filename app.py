"""Cloudstone: upload CSV / JSON / NDJSON / XLSX into DuckDB, profile, query, chart.

Run:   python app.py            -> http://127.0.0.1:8000
Check: python app.py check
"""
import csv, hashlib, hmac, json, os, re, secrets, shutil, sqlite3, subprocess, sys, tempfile, time
from http.cookies import SimpleCookie
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import anthropic
import duckdb

HERE = Path(__file__).parent
DEMO = HERE / "demo"
DATA = HERE / "data"
MAX_ROWS = 1000
MAX_BODY = 200 * 1024 * 1024
SESSION_DAYS = 30
COOKIE = "cs_session"
USERNAME_RE = re.compile(r"[A-Za-z0-9_.-]{3,32}")
MAX_FAILS, LOCKOUT_S = 5, 15 * 60


# ---------- loading and querying ----------

def table_name(filename):
    name = re.sub(r"\W+", "_", Path(filename).stem).strip("_").lower() or "data"
    return f"t_{name}" if name[0].isdigit() else name


def xlsx_to_csv(src, dst):
    import openpyxl
    ws = openpyxl.load_workbook(src, read_only=True, data_only=True).active  # first sheet only
    with open(dst, "w", newline="") as f:
        csv.writer(f).writerows(ws.iter_rows(values_only=True))


def load(db, filename, data, tmp_root=None):
    """Load file bytes into a table in db's main schema. tmp_root must be readable by db's sandbox."""
    ext = Path(filename).suffix.lower()
    lines = ("(SELECT unnest(range(1, len(l) + 1)) AS line_no, unnest(l) AS line FROM "
             "(SELECT regexp_split_to_array(rtrim(content, chr(13) || chr(10)), '\\r?\\n') AS l FROM read_text(?)))")
    readers = {".csv": "read_csv_auto(?)", ".json": "read_json_auto(?)", ".ndjson": "read_json_auto(?)",
               ".jsonl": "read_json_auto(?)", ".xlsx": "read_csv_auto(?)", ".parquet": "read_parquet(?)",
               ".log": lines}  # one row per line: (line_no, line)
    if ext not in readers:
        raise ValueError(f"unsupported file type: {ext or filename}")
    with tempfile.TemporaryDirectory(dir=tmp_root) as tmp:
        path = os.path.join(tmp, "upload" + ext)
        Path(path).write_bytes(data)
        if ext == ".xlsx":
            xlsx_to_csv(path, path := os.path.join(tmp, "upload.csv"))
        name = table_name(filename)
        db.execute(f'CREATE OR REPLACE TABLE main."{name}" AS SELECT * FROM {readers[ext]}', [path])
    return name


def tables(db):
    """Demo tables as 'demo.x', then the connection's own tables."""
    rows = db.execute("SELECT table_catalog, table_schema, table_name FROM information_schema.tables "
                      "WHERE table_catalog IN ('demo', current_database()) "
                      "ORDER BY table_catalog <> 'demo', 2, 3").fetchall()
    return [f"demo.{t}" if c == "demo" else t if s == "main" else f"{s}.{t}" for c, s, t in rows]


def ident(name):
    """'demo.sales' -> "demo"."sales"; only call on names returned by tables()."""
    return ".".join(f'"{part}"' for part in name.split(".", 1))


def profile(db, name):
    if name not in tables(db):
        raise ValueError(f"no such table: {name}")
    return query(db, f"SUMMARIZE {ident(name)}")


def query(db, sql):
    cur = db.execute(sql)
    if cur.description is None:
        return {"columns": [], "rows": [], "truncated": False}
    rows = cur.fetchmany(MAX_ROWS + 1)
    return {"columns": [d[0] for d in cur.description], "rows": rows[:MAX_ROWS],
            "truncated": len(rows) > MAX_ROWS}


# ---------- natural-language questions (Claude) ----------

MODEL = "claude-opus-5-5"
ASK_SCHEMA = {
    "type": "object",
    "properties": {"sql": {"type": "string"}, "explanation": {"type": "string"}},
    "required": ["sql", "explanation"],
    "additionalProperties": False,
}
ASK_SYSTEM = """You turn a question about the user's data into one DuckDB SQL query.

- Use only the tables and columns in <schema>. Table names are exactly as listed (demo tables are demo.<name>).
- Read-only: a single SELECT or WITH ... SELECT. Never modify data.
- Nested data: struct fields are struct_col.field; expand lists with FROM t, unnest(list_col) AS u(item).
- Round money and averages to 2 decimals, name computed columns clearly, and order results meaningfully.
- If the data can't answer the question, return an empty sql and say why in the explanation.

explanation: one short sentence, for a non-technical reader, saying what the query returns."""

_claude = None
# off: hidden, nothing is ever sent (default). subscription: run Claude Code (`claude -p`) logged in
# with your Claude plan, so questions use its usage limits. api: Anthropic API key, billed per request.
ASK_MODES = ("off", "subscription", "api")
NO_KEY = "Claude API key missing or invalid: set ANTHROPIC_API_KEY and restart the server"


def ask_mode():
    mode = os.environ.get("CLOUDSTONE_ASK", "off")
    if mode not in ASK_MODES:
        raise SystemExit(f"CLOUDSTONE_ASK must be one of {', '.join(ASK_MODES)}, not {mode!r}")
    return mode


def describe(db):
    """Schema plus a few sample rows for every table this connection can see."""
    parts = []
    for name in tables(db):
        cols = db.execute(f"DESCRIBE {ident(name)}").fetchall()
        sample = json.dumps(db.execute(f"SELECT * FROM {ident(name)} LIMIT 3").fetchall(), default=str)
        parts.append(f"TABLE {name}\n" + "\n".join(f"  {c[0]} {c[1]}" for c in cols)
                     + f"\n  sample rows: {sample[:1500]}")
    return "\n\n".join(parts)


def via_claude_code(prompt, run=subprocess.run):
    """Ask through the local Claude Code CLI, which uses the Claude plan you're logged in with."""
    # Drop every Anthropic/Claude variable so it can only use your own Claude Code login, never an API key.
    env = {k: v for k, v in os.environ.items() if not k.startswith(("ANTHROPIC_", "CLAUDE"))}
    cmd = ["claude", "-p", "--output-format", "json", "--json-schema", json.dumps(ASK_SCHEMA),
           "--system-prompt", ASK_SYSTEM,
           "--tools", "", "--strict-mcp-config",  # no tools: it only writes text
           "--setting-sources", "project", "--no-session-persistence"]  # no plugins/hooks, no saved session
    try:
        with tempfile.TemporaryDirectory() as empty:  # empty working dir: no CLAUDE.md or project files
            p = run(cmd, input=prompt, cwd=empty, env=env, capture_output=True, text=True, timeout=180)
    except FileNotFoundError:
        raise ValueError("Claude Code isn't installed or isn't on PATH; install it and run `claude` once to log in")
    except subprocess.TimeoutExpired:
        raise ValueError("Claude Code took longer than 3 minutes; try again")
    try:
        out = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise ValueError(f"Claude Code failed: {(p.stderr or p.stdout).strip()[:300]}")
    if out.get("is_error") or not isinstance(out.get("structured_output"), dict):
        raise ValueError(f"Claude Code: {str(out.get('result') or out.get('subtype'))[:300]}")
    return out["structured_output"]


def via_api(prompt, client):
    global _claude
    if client is None:
        client = _claude = _claude or anthropic.Anthropic()
    try:
        resp = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",  # if Opus declines, Anthropic retries on its recommended fallback model
            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": ASK_SCHEMA}},
            system=ASK_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
    except TypeError as e:  # the SDK raises this when no credentials are configured
        if "authentication" not in str(e):
            raise
        raise ValueError(NO_KEY) from e
    if resp.stop_reason == "refusal":
        raise ValueError("Claude declined to answer that question")
    if resp.stop_reason == "max_tokens":
        raise ValueError("Claude's answer was cut off; try a simpler question")
    return json.loads(next(b.text for b in resp.content if b.type == "text"))


def ask(db, question, client=None, run=subprocess.run):
    """Ask Claude for SQL answering `question`, run it (changes rolled back), return sql + result."""
    question = question.strip()
    if not question:
        raise ValueError("type a question first")
    prompt = f"<schema>\n{describe(db)}\n</schema>\n\nQuestion: {question}"
    out = via_claude_code(prompt, run) if ask_mode() == "subscription" else via_api(prompt, client)
    result = {"sql": out["sql"], "explanation": out["explanation"], "columns": [], "rows": [], "truncated": False}
    if out["sql"].strip():
        db.execute("BEGIN TRANSACTION")  # the prompt says read-only; the rollback makes sure
        try:
            result.update(query(db, out["sql"]))
        except duckdb.Error as e:
            result["error"] = str(e)
        finally:
            db.execute("ROLLBACK")
    return result


# ---------- databases: demo, anonymous, per user ----------

def sq(path):
    return str(path).replace("'", "''")


def sandbox(db):
    """No file, network or extension access from SQL, and settings can't be changed back."""
    db.execute("SET enable_external_access = false")
    db.execute("SET lock_configuration = true")


def build_demo():
    """Rebuild data/demo.duckdb from demo/ (called on startup, before anything opens it)."""
    path = DATA / "demo.duckdb"
    path.unlink(missing_ok=True)
    with duckdb.connect(str(path)) as db:
        for f in sorted(DEMO.iterdir()):
            load(db, f.name, f.read_bytes())


def open_anon_db():
    db = duckdb.connect(str(DATA / "demo.duckdb"), read_only=True)
    sandbox(db)
    return db


USER_DBS = {}  # ponytail: one open DuckDB per active user, never evicted; add an LRU if user count grows


def user_db(uid):
    if uid not in USER_DBS:
        (DATA / "users").mkdir(parents=True, exist_ok=True)
        uploads = (DATA / "uploads" / str(uid))
        uploads.mkdir(parents=True, exist_ok=True)
        db = duckdb.connect(str(DATA / "users" / f"u{uid}.duckdb"))
        db.execute(f"ATTACH '{sq(DATA / 'demo.duckdb')}' AS demo (READ_ONLY)")
        db.execute(f"SET allowed_directories = ['{sq(uploads.resolve())}/']")
        sandbox(db)
        USER_DBS[uid] = db
    return USER_DBS[uid]


def drop_user_data(uid):
    if db := USER_DBS.pop(uid, None):
        db.close()
    for p in (DATA / "users" / f"u{uid}.duckdb", DATA / "users" / f"u{uid}.duckdb.wal"):
        p.unlink(missing_ok=True)
    shutil.rmtree(DATA / "uploads" / str(uid), ignore_errors=True)


# ---------- accounts ----------

def open_auth():
    db = sqlite3.connect(DATA / "auth.sqlite3")
    db.executescript("""
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE COLLATE NOCASE,
            salt BLOB NOT NULL,
            pw_hash BLOB NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS sessions (
            token_hash TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            expires_at REAL NOT NULL);
    """)
    return db


def hash_pw(password, salt):
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)


def check_password(password):
    if not 8 <= len(password) <= 128:
        raise ValueError("password must be 8-128 characters")


def signup(auth, username, password):
    if not USERNAME_RE.fullmatch(username):
        raise ValueError("username must be 3-32 letters, digits, '.', '_' or '-'")
    check_password(password)
    salt = secrets.token_bytes(16)
    try:
        with auth:
            return auth.execute("INSERT INTO users (username, salt, pw_hash) VALUES (?, ?, ?)",
                                (username, salt, hash_pw(password, salt))).lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("username is taken")


FAILS = {}  # username -> (failures, first failure time); ponytail: in-memory, resets on restart


def verify(auth, username, password):
    """Return the user id, or raise PermissionError. Locks a username after repeated failures."""
    key = username.lower()
    fails, since = FAILS.get(key, (0, 0))
    if fails >= MAX_FAILS and time.time() - since < LOCKOUT_S:
        raise PermissionError("too many failed attempts; try again in 15 minutes")
    row = auth.execute("SELECT id, salt, pw_hash FROM users WHERE username = ?", (username,)).fetchone()
    salt, expected = (row[1], row[2]) if row else (b"\0" * 16, b"")
    ok = hmac.compare_digest(hash_pw(password, salt), expected)  # hash even when unknown: same timing
    if not (row and ok):
        FAILS[key] = (fails + 1, since if fails and time.time() - since < LOCKOUT_S else time.time())
        raise PermissionError("wrong username or password")
    FAILS.pop(key, None)
    return row[0]


def new_session(auth, uid):
    token = secrets.token_urlsafe(32)
    with auth:
        auth.execute("INSERT INTO sessions VALUES (?, ?, ?)",
                     (hashlib.sha256(token.encode()).hexdigest(), uid, time.time() + SESSION_DAYS * 86400))
    return token


def session_user(auth, token):
    """(user id, username) for a valid session token, else None."""
    with auth:
        auth.execute("DELETE FROM sessions WHERE expires_at < ?", (time.time(),))
    return auth.execute("SELECT u.id, u.username FROM sessions s JOIN users u ON u.id = s.user_id "
                        "WHERE s.token_hash = ?", (hashlib.sha256(token.encode()).hexdigest(),)).fetchone()


def end_sessions(auth, uid=None, token=None):
    with auth:
        if token:
            auth.execute("DELETE FROM sessions WHERE token_hash = ?", (hashlib.sha256(token.encode()).hexdigest(),))
        else:
            auth.execute("DELETE FROM sessions WHERE user_id = ?", (uid,))


def change_password(auth, uid, username, old, new):
    verify(auth, username, old)
    check_password(new)
    salt = secrets.token_bytes(16)
    with auth:
        auth.execute("UPDATE users SET salt = ?, pw_hash = ? WHERE id = ?", (salt, hash_pw(new, salt), uid))
    end_sessions(auth, uid)  # log out everywhere; caller issues a fresh session


def delete_account(auth, uid, username, password):
    verify(auth, username, password)
    with auth:
        auth.execute("DELETE FROM users WHERE id = ?", (uid,))  # sessions cascade
    drop_user_data(uid)


# ---------- HTTP ----------

class Handler(BaseHTTPRequestHandler):
    auth = None
    anon = None

    def send(self, code, body, ctype="application/json", cookie=None):
        if ctype == "application/json":
            body = json.dumps(body, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if cookie is not None:
            age = SESSION_DAYS * 86400 if cookie else 0
            self.send_header("Set-Cookie", f"{COOKIE}={cookie}; Max-Age={age}; Path=/; HttpOnly; SameSite=Strict")
        self.end_headers()
        self.wfile.write(body)

    def token(self):
        c = SimpleCookie(self.headers.get("Cookie", "")).get(COOKIE)
        return c.value if c else ""

    def route(self, method):
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        me = session_user(self.auth, self.token()) if self.token() else None
        db = user_db(me[0]) if me else self.anon
        try:
            if method == "GET":
                if url.path == "/":
                    return self.send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
                if url.path == "/me":
                    return self.send(200, {"user": me[1] if me else None, "ask": ask_mode() != "off"})
                if url.path == "/tables":
                    return self.send(200, tables(db))
                if url.path == "/profile":
                    return self.send(200, profile(db, q.get("table", "")))
                return self.send(404, {"error": "not found"})

            origin = self.headers.get("Origin")
            if origin and urlparse(origin).netloc != self.headers.get("Host"):
                return self.send(403, {"error": "cross-origin request refused"})
            size = int(self.headers.get("Content-Length", 0))
            if size > MAX_BODY:
                return self.send(413, {"error": f"file too large (max {MAX_BODY // 2**20} MB)"})
            body = self.rfile.read(size)
            data = json.loads(body) if url.path != "/upload" and body else {}

            if url.path in ("/signup", "/login"):
                user, pw = str(data.get("username", "")), str(data.get("password", ""))
                uid = signup(self.auth, user, pw) if url.path == "/signup" else verify(self.auth, user, pw)
                name = self.auth.execute("SELECT username FROM users WHERE id = ?", (uid,)).fetchone()[0]
                return self.send(200, {"user": name}, cookie=new_session(self.auth, uid))
            if url.path == "/query":
                return self.send(200, query(db, data["sql"]))
            if url.path == "/ask":
                if ask_mode() == "off":
                    return self.send(403, {"error": "Ask is turned off; start the server with CLOUDSTONE_ASK=subscription (uses your Claude plan) or CLOUDSTONE_ASK=api"})
                return self.send(200, ask(db, str(data.get("question", ""))))
            if not me:
                return self.send(401, {"error": "log in to do that"})
            if url.path == "/logout":
                end_sessions(self.auth, token=self.token())
                return self.send(200, {"user": None}, cookie="")
            if url.path == "/password":
                change_password(self.auth, me[0], me[1], str(data.get("old", "")), str(data.get("new", "")))
                return self.send(200, {"user": me[1]}, cookie=new_session(self.auth, me[0]))
            if url.path == "/account/delete":
                delete_account(self.auth, me[0], me[1], str(data.get("password", "")))
                return self.send(200, {"user": None}, cookie="")
            if url.path == "/upload":
                name = load(db, q.get("name", ""), body, DATA / "uploads" / str(me[0]))
                return self.send(200, {"table": name, "profile": profile(db, name)})
            self.send(404, {"error": "not found"})
        except PermissionError as e:
            self.send(401 if url.path in ("/login", "/password", "/account/delete") else 403, {"error": str(e)})
        except (duckdb.Error, ValueError, KeyError, TypeError) as e:
            self.send(400, {"error": str(e)})
        except anthropic.AuthenticationError:
            self.send(502, {"error": NO_KEY})
        except anthropic.RateLimitError:
            self.send(502, {"error": "Claude API rate limit reached; try again in a minute"})
        except anthropic.AnthropicError as e:
            self.send(502, {"error": f"Claude API error: {e}"})

    def do_GET(self):
        self.route("GET")

    def do_POST(self):
        self.route("POST")


def start():
    print(f"Ask (plain-English questions): {ask_mode()}")
    DATA.mkdir(exist_ok=True)
    build_demo()
    Handler.auth, Handler.anon = open_auth(), open_anon_db()


# ---------- self-check ----------

def check():
    global DATA
    assert table_name("2024 Sales-Report.csv") == "t_2024_sales_report"

    db = duckdb.connect()
    assert load(db, "people.csv", b"name,age\nana,31\nbo,\n") == "people"
    prof = profile(db, "people")
    age = next(r for r in prof["rows"] if r[0] == "age")
    assert "INT" in age[prof["columns"].index("column_type")]
    assert float(age[prof["columns"].index("null_percentage")]) == 50
    load(db, "events.ndjson", b'{"id":1,"meta":{"tag":"a"}}\n{"id":2,"meta":{"tag":"b"}}\n')
    assert query(db, "SELECT meta.tag FROM events ORDER BY id")["rows"] == [("a",), ("b",)]
    load(db, "nested.json", b'[{"k":[1,2]},{"k":[3]}]')
    assert query(db, "SELECT sum(len(k)) FROM nested")["rows"] == [(3,)]
    import openpyxl
    wb = openpyxl.Workbook()
    wb.active.append(["x", "y"]); wb.active.append([1, 2.5])
    with tempfile.NamedTemporaryFile(suffix=".xlsx") as f:
        wb.save(f.name)
        load(db, "sheet.xlsx", Path(f.name).read_bytes())
    assert query(db, "SELECT x + y FROM sheet")["rows"] == [(3.5,)]
    raises(ValueError, load, db, "notes.txt", b"hi")

    with tempfile.TemporaryDirectory() as tmp:
        DATA = Path(tmp)
        start()
        auth, anon = Handler.auth, Handler.anon

        # demo data, read-only and sandboxed for anonymous visitors
        assert tables(anon) == ["demo.customers", "demo.employees", "demo.events", "demo.products",
                                "demo.sales", "demo.shipments", "demo.web_server"]
        cols = dict(c[:2] for c in anon.execute("DESCRIBE demo.customers").fetchall())
        assert cols["id"] == cols["tags"] == "JSON" and cols["email"] == "VARCHAR"  # mixed shapes stay queryable
        assert query(anon, "SELECT count(*) FROM demo.shipments JOIN demo.sales USING (order_id)")["rows"] == [(120,)]
        assert query(anon, "SELECT count(*) FROM demo.web_server WHERE line LIKE '%ERROR%'")["rows"][0][0] > 0
        assert query(anon, "SELECT count(*) FROM demo.sales s JOIN demo.employees e ON s.rep_id = e.employee_id "
                           "JOIN demo.products p USING (sku)")["rows"] == [(120,)]
        assert profile(anon, "demo.events")["rows"]
        raises(duckdb.Error, query, anon, "CREATE TABLE x AS SELECT 1")
        raises(duckdb.Error, query, anon, "SELECT * FROM read_csv_auto('/etc/passwd')")

        # accounts
        ana = signup(auth, "ana", "correct horse")
        raises(ValueError, signup, auth, "ANA", "another pass")  # case-insensitive unique
        raises(ValueError, signup, auth, "x", "long enough")
        raises(ValueError, signup, auth, "bob", "short")
        bo = signup(auth, "bob", "battery staple")
        assert verify(auth, "Ana", "correct horse") == ana
        raises(PermissionError, verify, auth, "ana", "wrong password")
        raises(PermissionError, verify, auth, "nobody", "whatever1")
        t = new_session(auth, ana)
        assert session_user(auth, t) == (ana, "ana") and session_user(auth, "forged") is None
        assert b"correct horse" not in (DATA / "auth.sqlite3").read_bytes()

        # per-user data: saved, isolated, sandboxed
        a, b = user_db(ana), user_db(bo)
        load(a, "mine.csv", b"v\n1\n2\n", DATA / "uploads" / str(ana))
        load(a, "app.log", b"10:00 INFO up\r\n10:01 ERROR down\n", DATA / "uploads" / str(ana))  # sandboxed reads
        assert query(a, "SELECT line_no, line FROM app")["rows"] == [(1, "10:00 INFO up"), (2, "10:01 ERROR down")]
        with tempfile.TemporaryDirectory() as t:
            duckdb.execute(f"COPY (SELECT 7 AS n, [1, 2] AS l) TO '{sq(Path(t) / 'p.parquet')}' (FORMAT parquet)")
            load(a, "nums.parquet", (Path(t) / "p.parquet").read_bytes(), DATA / "uploads" / str(ana))
        assert query(a, "SELECT n, len(l) FROM nums")["rows"] == [(7, 2)]
        assert "mine" in tables(a) and "mine" not in tables(b)
        assert query(a, "SELECT * FROM demo.sales LIMIT 1")["rows"]
        raises(duckdb.Error, query, a, "DROP TABLE demo.sales")
        raises(duckdb.Error, query, b, f"ATTACH '{sq(DATA / 'users' / f'u{ana}.duckdb')}' AS x")
        raises(duckdb.Error, query, b, f"SELECT * FROM read_csv_auto('{sq(HERE / 'app.py')}')")
        raises(duckdb.Error, query, a, "COPY mine TO '/tmp/cloudstone-leak.csv'")
        raises(duckdb.Error, query, a, "SET enable_external_access = true")
        USER_DBS.pop(ana).close()
        assert query(user_db(ana), "SELECT sum(v) FROM mine")["rows"] == [(3,)]  # persisted

        # lockout after repeated failures
        for _ in range(MAX_FAILS):
            raises(PermissionError, verify, auth, "bob", "nope nope")
        raises(PermissionError, verify, auth, "bob", "battery staple")
        FAILS.clear()

        # natural-language questions, with a stand-in for the Claude client
        from types import SimpleNamespace as NS
        sent, a = {}, user_db(ana)

        def fake(answer, stop="end_turn"):
            def create(**kw):
                sent.update(kw)
                return NS(stop_reason=stop, content=[NS(type="text", text=json.dumps(answer))])
            return NS(beta=NS(messages=NS(create=create)))

        r = ask(a, "total of my values?", fake({"sql": "SELECT sum(v) AS total FROM mine", "explanation": "Sum."}))
        assert r["rows"] == [(3,)] and r["sql"].startswith("SELECT")
        prompt = sent["messages"][0]["content"]
        assert "TABLE demo.sales" in prompt and "TABLE mine" in prompt and "v BIGINT" in prompt
        assert sent["model"] == MODEL and sent["output_config"]["format"]["schema"] == ASK_SCHEMA
        r = ask(a, "wipe it", fake({"sql": "DELETE FROM mine", "explanation": "x"}))
        assert query(a, "SELECT count(*) FROM mine")["rows"] == [(2,)]  # rolled back
        r = ask(anon, "bad", fake({"sql": "SELECT nope FROM demo.sales", "explanation": "x"}))
        assert "nope" in r["error"]
        assert ask(anon, "weather?", fake({"sql": "", "explanation": "No weather data."}))["rows"] == []
        raises(ValueError, ask, anon, "x", fake({}, stop="refusal"))
        raises(ValueError, ask, anon, "   ", fake({}))
        def no_key(**kw):
            raise TypeError("Could not resolve authentication method.")
        raises(ValueError, ask, anon, "x", NS(beta=NS(messages=NS(create=no_key))))

        # subscription mode: runs Claude Code with a clean environment and no tools
        calls = []

        def fake_run(cmd, **kw):
            calls.append((cmd, kw))
            return NS(stdout=json.dumps({"is_error": False, "structured_output":
                      {"sql": "SELECT count(*) FROM demo.sales", "explanation": "Counts orders."}}), stderr="")
        os.environ.update(CLOUDSTONE_ASK="subscription", ANTHROPIC_API_KEY="sk-ant-test-only")
        try:
            r = ask(anon, "how many orders?", run=fake_run)
        finally:
            del os.environ["ANTHROPIC_API_KEY"]
        cmd, kw = calls[0]
        assert r["rows"] == [(120,)] and cmd[:2] == ["claude", "-p"]
        assert cmd[cmd.index("--tools") + 1] == "" and "TABLE demo.sales" in kw["input"]
        assert not any(k.startswith(("ANTHROPIC_", "CLAUDE")) for k in kw["env"]) and kw["cwd"] != str(HERE)
        limit = json.dumps({"is_error": True, "result": "Claude usage limit reached"})
        raises(ValueError, ask, anon, "x", None, lambda *a, **k: NS(stdout=limit, stderr=""))
        raises(ValueError, ask, anon, "x", None, lambda *a, **k: NS(stdout="", stderr="Not logged in"))

        def missing(*a, **k):
            raise FileNotFoundError
        raises(ValueError, ask, anon, "x", None, missing)

        os.environ.pop("CLOUDSTONE_ASK", None)
        assert ask_mode() == "off"
        os.environ["CLOUDSTONE_ASK"] = "bogus"
        raises(SystemExit, ask_mode)
        del os.environ["CLOUDSTONE_ASK"]

        # password change ends sessions; account deletion removes data
        change_password(auth, ana, "ana", "correct horse", "new secret!")
        assert session_user(auth, t) is None and verify(auth, "ana", "new secret!") == ana
        delete_account(auth, bo, "bob", "battery staple")
        assert not (DATA / "users" / f"u{bo}.duckdb").exists()
        raises(PermissionError, verify, auth, "bob", "battery staple")
        for d in list(USER_DBS):
            USER_DBS.pop(d).close()
        anon.close()
    print("ok")


def raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError(f"{fn.__name__}{args} did not raise {exc.__name__}")


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        check()
    else:
        start()
        # ponytail: single-threaded server; fine for local use, ThreadingHTTPServer + per-request cursors to scale
        print("http://127.0.0.1:8000")
        HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
