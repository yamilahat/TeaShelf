# TeaShelf

A tea inventory and tasting journal app. FastAPI backend, React + TypeScript frontend.

## Project Structure

```
backend/app/
  main.py          # App factory, router registration
  config.py        # Settings (DATABASE_URL env var)
  models/          # SQLAlchemy ORM models (Tea, TeaSession)
  schemas/         # Pydantic request/response models
  routers/         # FastAPI route handlers (health, teas, tea_sessions)
  db/              # session.py (get_db), types.py (UTCDateTime), base.py

frontend/src/
  App.tsx          # Router + ShellLayout
  lib/api.ts       # Generic fetch wrapper (prepends /api)
  features/teas/   # Tea API, form state helpers, TeaForm component
  features/sessions/ # Session API, form state helpers, SessionForm component
  pages/           # TeasPage, NewTeaPage, TeaDetailPage, SessionsPage, SessionDetailPage
```

## Development

### Backend
```bash
# From repo root — requires PostgreSQL running (or use Docker)
docker-compose up db        # Start only the database
uvicorn backend.app.main:app --reload --port 8000

# Or run everything with Docker
docker-compose up
```

### Frontend
```bash
cd frontend
npm install
npm run dev     # Vite dev server on :5173, proxies /api → localhost:8000
```

### Database Migrations
```bash
alembic upgrade head        # Apply all migrations
alembic revision --autogenerate -m "describe change"  # Generate new migration
```

## Testing

```bash
# Backend tests (uses SQLite in-memory, no DB required)
pytest

# Lint
ruff check .
```

## Key Conventions

- All datetimes stored and returned in UTC. The `UTCDateTime` custom type (`db/types.py`) enforces this.
- Session dates in API responses use ISO 8601 with `Z` suffix (e.g. `2024-01-15T10:30:00Z`).
- Schemas use `model_dump(exclude_unset=True)` for PATCH-style updates so unset fields are not overwritten.
- Frontend form state converts all fields to strings for controlled inputs, then converts back to typed values in payload helpers (`formState.ts`).
- Frontend API calls go through `src/lib/api.ts` — always use `apiFetch`, never raw `fetch`.
- React Query cache keys: `["teas"]`, `["teas", teaId]`, `["sessions"]`, `["sessions", sessionId]`.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+psycopg://postgres:postgres@localhost:5432/teashelf` | PostgreSQL connection string |
