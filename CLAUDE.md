# Cloudstone

Local data workbench: `app.py` (stdlib server, accounts, per-user DuckDB, plain-English questions via Claude Code on the user's plan or the API; off by default), `index.html` (UI), `demo/` (demo data), `data/` (runtime state, git-ignored). Details in ARCHITECTURE.md.

## Docs rule: every commit, then push

Before each commit, update the docs in the same commit, then push to `origin` right after committing. The user has standing approval for this push.

- **CHANGELOG.md:** always. Add a line under `[Unreleased]` in the right group (Added / Changed / Fixed / Removed). When a version is tagged, rename `[Unreleased]` to `[x.y.z] - YYYY-MM-DD` and start a new empty `[Unreleased]`.
- **README.md:** when features, setup, run commands or limits change.
- **ARCHITECTURE.md:** when routes, the upload flow, components, dependencies or design decisions change.

Docs must describe the code as committed. Don't document planned work.

## Before committing

Run `.venv/bin/python app.py check` and make sure it prints `ok`.
