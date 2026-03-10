## Project overview
- Backend-first tea inventory and tasting journal built with FastAPI.
- Main app code lives under `backend/app/`.
- Tests live under `backend/tests/`.

## Working rules
- Keep patches small and scoped to one milestone.
- Ask before adding a new dependency.
- Do not change API shapes unless the task explicitly asks for it.
- Prefer simple, readable code over clever abstractions.
- Follow existing patterns before creating new ones.

## Validation
- Run `pytest -q` after backend changes.
- Run `ruff check .` before finishing.
- If models change, update Alembic migration.
- If validation fails, fix it before stopping.

## Done criteria
- Code runs locally.
- Tests pass.
- Lint passes.
- Update docs if behavior changed.
- Final message must list changed files and verification steps.