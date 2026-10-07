"""Cloudstone: upload CSV / JSON / NDJSON / XLSX into DuckDB, profile, query, chart.

Run:   python app.py            -> http://127.0.0.1:8000
Check: python app.py check
"""
import csv, json, os, re, sys, tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import duckdb

HERE = Path(__file__).parent
MAX_ROWS = 1000


def table_name(filename):
    name = re.sub(r"\W+", "_", Path(filename).stem).strip("_").lower() or "data"
    return f"t_{name}" if name[0].isdigit() else name


def xlsx_to_csv(src, dst):
    import openpyxl
    ws = openpyxl.load_workbook(src, read_only=True, data_only=True).active  # first sheet only
    with open(dst, "w", newline="") as f:
        csv.writer(f).writerows(ws.iter_rows(values_only=True))


def load(db, filename, data):
    ext = Path(filename).suffix.lower()
    readers = {".csv": "read_csv_auto", ".json": "read_json_auto", ".ndjson": "read_json_auto",
               ".jsonl": "read_json_auto", ".xlsx": "read_csv_auto"}
    if ext not in readers:
        raise ValueError(f"unsupported file type: {ext or filename}")
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "upload" + ext)
        Path(path).write_bytes(data)
        if ext == ".xlsx":
            xlsx_to_csv(path, path := os.path.join(tmp, "upload.csv"))
        name = table_name(filename)
        db.execute(f'CREATE OR REPLACE TABLE "{name}" AS SELECT * FROM {readers[ext]}(?)', [path])
    return name


def profile(db, name):
    if name not in tables(db):
        raise ValueError(f"no such table: {name}")
    return query(db, f'SUMMARIZE "{name}"')


def tables(db):
    return [r[0] for r in db.execute("SELECT table_name FROM information_schema.tables ORDER BY 1").fetchall()]


def query(db, sql):
    cur = db.execute(sql)
    if cur.description is None:
        return {"columns": [], "rows": [], "truncated": False}
    rows = cur.fetchmany(MAX_ROWS + 1)
    return {"columns": [d[0] for d in cur.description], "rows": rows[:MAX_ROWS],
            "truncated": len(rows) > MAX_ROWS}


class Handler(BaseHTTPRequestHandler):
    db = None

    def send(self, code, body, ctype="application/json"):
        if ctype == "application/json":
            body = json.dumps(body, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def route(self, method):
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            if method == "GET" and url.path == "/":
                return self.send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
            if method == "GET" and url.path == "/tables":
                return self.send(200, tables(self.db))
            if method == "GET" and url.path == "/profile":
                return self.send(200, profile(self.db, q.get("table", "")))
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            if method == "POST" and url.path == "/upload":
                name = load(self.db, q.get("name", ""), body)
                return self.send(200, {"table": name, "profile": profile(self.db, name)})
            if method == "POST" and url.path == "/query":
                return self.send(200, query(self.db, json.loads(body)["sql"]))
            self.send(404, {"error": "not found"})
        except (duckdb.Error, ValueError, KeyError) as e:
            self.send(400, {"error": str(e)})

    def do_GET(self):
        self.route("GET")

    def do_POST(self):
        self.route("POST")


def check():
    db = duckdb.connect()
    assert table_name("2024 Sales-Report.csv") == "t_2024_sales_report"
    assert load(db, "people.csv", b"name,age\nana,31\nbo,\n") == "people"
    prof = profile(db, "people")
    cols = prof["columns"]
    age = next(r for r in prof["rows"] if r[0] == "age")
    assert "INT" in age[cols.index("column_type")] and float(age[cols.index("null_percentage")]) == 50
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
    try:
        load(db, "notes.txt", b"hi")
        assert False
    except ValueError:
        pass
    assert sorted(tables(db)) == ["events", "nested", "people", "sheet"]
    print("ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["check"]:
        check()
    else:
        Handler.db = duckdb.connect(str(HERE / "data.duckdb"))
        # ponytail: single-threaded server + one connection; fine for one local user
        print("http://127.0.0.1:8000")
        HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
