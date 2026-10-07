# Cloudstone

Local data workbench: `app.py` (stdlib server + DuckDB) and `index.html` (UI). Details in ARCHITECTURE.md.

## Docs rule: every commit

Before each commit, update the docs in the same commit:

- **CHANGELOG.md:** always. Add a line under `[Unreleased]` in the right group (Added / Changed / Fixed / Removed). When a version is tagged, rename `[Unreleased]` to `[x.y.z] - YYYY-MM-DD` and start a new empty `[Unreleased]`.
- **README.md:** when features, setup, run commands or limits change.
- **ARCHITECTURE.md:** when routes, the upload flow, components, dependencies or design decisions change.

Docs must describe the code as committed. Don't document planned work.

## Before committing

Run `.venv/bin/python app.py check` and make sure it prints `ok`.
