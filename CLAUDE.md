# TeaShelf

TeaShelf is a backend-first tea inventory and tasting journal app.

Treat it as a real portfolio project, not a throwaway AI demo. Favor correctness, maintainability, and incremental delivery over speculative architecture, generic AI features, or flashy UI.

## What Claude should optimize for
- Make the smallest coherent change that solves the task.
- Follow the existing architecture unless there is a clear reason to change it.
- Prefer straightforward, readable code over clever abstractions.
- Preserve learning value. Do not over-automate or over-engineer the solution.
- Ground decisions in the actual codebase. Inspect relevant files before proposing or making changes.
- Do not invent endpoints, models, relationships, capabilities, or project goals that do not exist.

## Scope boundaries
- Assume TeaShelf is single-user unless explicitly told otherwise.
- Do not add auth, multi-user SaaS behavior, roles, permissions, background jobs, analytics, caching, or AI-heavy features unless explicitly requested.
- Keep the frontend simple, modern, and practical.
- Avoid generic “AI product” UI patterns, decorative dashboards, fake analytics, or unnecessary feature creep.
- Use the real backend API unless explicitly asked to use mock data.

## Project structure

### Backend
- `backend/app/main.py` — FastAPI app setup and router registration
- `backend/app/config.py` — settings and environment configuration
- `backend/app/models/` — SQLAlchemy ORM models such as `Tea` and `TeaSession`
- `backend/app/schemas/` — Pydantic request and response schemas
- `backend/app/routers/` — FastAPI route handlers such as `health`, `teas`, and `tea_sessions`
- `backend/app/db/` — DB utilities such as `session.py`, `types.py`, and `base.py`

### Frontend
- `frontend/src/App.tsx` — app shell and router
- `frontend/src/lib/api.ts` — shared API wrapper
- `frontend/src/features/teas/` — tea API logic, form helpers, and components
- `frontend/src/features/sessions/` — session API logic, form helpers, and components
- `frontend/src/pages/` — route-level pages

## Working rules
- Inspect the relevant files before changing code.
- Prefer minimal edits over broad refactors.
- Do not create new abstractions unless duplication or complexity clearly justifies them.
- Keep business logic aligned with the current project structure.
- Do not rewrite unrelated code for style consistency alone.
- When a task touches both frontend and backend, preserve existing API contracts unless the task explicitly requires changing them.
- If something is unclear, state the uncertainty instead of filling gaps with assumptions.

## Backend conventions
- All datetimes are stored and returned in UTC.
- The custom `UTCDateTime` type in `backend/app/db/types.py` enforces UTC behavior.
- Session dates in API responses use ISO 8601 with `Z` suffix, for example: `2024-01-15T10:30:00Z`.
- Use `model_dump(exclude_unset=True)` for PATCH-style updates so omitted fields are not overwritten.
- Favor explicit request and response schemas.
- Be careful with relationship correctness and database constraints.

## Frontend conventions
- Frontend API calls must go through `frontend/src/lib/api.ts` using `apiFetch`. Do not use raw `fetch` directly in feature code.
- Form state should use string values for controlled inputs, then convert to typed payloads in helper functions.
- Preserve existing React Query key conventions:
  - `["teas"]`
  - `["teas", teaId]`
  - `["sessions"]`
  - `["sessions", sessionId]`
- Keep UI changes calm, clear, and restrained. The project should not look like template-generated AI slop.

## Development commands

### Backend
~~~bash
# Start only the database
docker compose up db

# Run backend locally
uvicorn backend.app.main:app --reload --port 8000

# Run full stack with Docker
docker compose up
~~~

### Frontend
~~~bash
cd frontend
npm install
npm run dev
~~~

### Database
~~~bash
alembic upgrade head
alembic revision --autogenerate -m "describe change"
~~~

## Verification
- For backend changes, run:
  - `ruff check .`
  - `pytest`
- For migration changes, verify Alembic state and confirm the migration matches the intended schema change.
- Before finalizing, confirm that:
  - the change matches existing project conventions
  - no unnecessary abstractions were introduced
  - the scope did not drift beyond the requested task

## Environment
- `DATABASE_URL` defaults to:
  `postgresql+psycopg://postgres:postgres@localhost:5432/teashelf`

## Reference
- See `README.md` for broader project overview if needed.
- Keep `CLAUDE.md` focused on durable instructions, conventions, commands, and repo-specific working rules.
- If the project grows, move long explanations into docs and import them here when useful.