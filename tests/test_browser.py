import os, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import expect

ROOT = Path(__file__).resolve().parent.parent
PORT = 8765


@pytest.fixture(scope="session")
def base_url():
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "CLOUDSTONE_PORT": str(PORT), "CLOUDSTONE_DATA": tmp}
        env.pop("CLOUDSTONE_ASK", None)
        proc = subprocess.Popen([sys.executable, str(ROOT / "app.py")], env=env, cwd=ROOT, stdout=subprocess.DEVNULL)
        url = f"http://127.0.0.1:{PORT}"
        try:
            for _ in range(100):
                try:
                    urllib.request.urlopen(url + "/me", timeout=1)
                    break
                except OSError:
                    time.sleep(0.2)
            else:
                raise RuntimeError("server did not start")
            yield url
        finally:
            proc.terminate()
            proc.wait(10)


@pytest.fixture
def app(page, base_url):
    page.errors = []
    page.on("console", lambda m: m.type == "error" and page.errors.append(m.text))
    page.on("pageerror", lambda e: page.errors.append(str(e)))
    page.goto(base_url)
    expect(page.locator("#outstatus")).to_contain_text("ms")  # first table loaded
    return page


def run_example(page):
    page.locator("#examples button").first.click()
    expect(page.locator("#outstatus")).to_contain_text(" ms")
    expect(page.locator("#gridres tbody tr").first).to_be_visible()


def test_loads_clean_on_demo_sales(app):
    expect(app.locator("#tables, #demo").locator("[aria-current=true]")).to_have_attribute("data-table", "demo.sales")
    expect(app.locator("#gridres tbody tr").first).to_be_visible()
    assert app.errors == []


def test_example_query_shows_rows_and_timing(app):
    run_example(app)
    expect(app.locator("#outstatus")).to_contain_text("rows")
    expect(app.locator("#outstatus")).to_contain_text("· ")


def test_sort_by_header_name(app):
    run_example(app)
    head = app.locator("#gridres th.h").first
    app.locator("#gridres th.h .hn").first.click()
    expect(head).to_have_attribute("aria-sort", "ascending")
    app.locator("#gridres th.h .hn").first.click()
    expect(head).to_have_attribute("aria-sort", "descending")


def test_column_details_open_and_esc_closes(app):
    run_example(app)
    app.locator("#gridres th.h").first.focus()
    app.keyboard.press("Shift+Enter")
    expect(app.locator("#colpanel")).to_be_visible()
    app.keyboard.press("Escape")
    expect(app.locator("#colpanel")).to_be_hidden()


def test_chart_tab_renders_canvas(app):
    run_example(app)
    app.get_by_role("tab", name="Chart").click()
    expect(app.locator("#chart")).to_be_visible()
    assert app.locator("#chart").evaluate("c => c.width > 0 && c.height > 0")


def test_history_records_a_run(app):
    run_example(app)
    app.get_by_role("tab", name="History").click()
    expect(app.locator("#hlist .hrow .f").first).to_contain_text(" ms")  # page load also logs its own run


def test_ask_hidden_when_off(app):
    expect(app.locator("#askcard")).to_be_hidden()
    expect(app.locator("#askoff")).to_be_visible()


def test_explorer_is_one_tab_stop(app):
    expect(app.locator("#explorer [tabindex='0']")).to_have_count(1)


def test_slash_focuses_editor_when_ask_off(app):
    app.locator("body").click(position={"x": 5, "y": 5})
    app.keyboard.press("/")
    expect(app.locator("#sql")).to_be_focused()


def test_signup_upload_and_delete_account(app, tmp_path):
    app.locator("[data-auth=signup]").click()
    app.locator("#username").fill("tester")
    app.locator("#password").fill("correct horse 123")
    app.locator("#authsubmit").click()
    expect(app.locator("#loggedin")).to_be_visible()
    csv = tmp_path / "pets.csv"
    csv.write_text("name,age\nrex,3\nfido,5\n")
    app.locator("#file").set_input_files(str(csv))
    expect(app.locator("#tables .name", has_text="pets")).to_be_visible()
    app.locator("#accountbtn").click()
    app.locator("#delpw").fill("correct horse 123")
    app.locator("#delgo").click()
    expect(app.locator("#loggedout")).to_be_visible()
