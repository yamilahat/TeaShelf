# TeaShelf

TeaShelf is a backend-first tea inventory and tasting journal for a single user.

The project is intentionally small. The goal is to build something clean, testable, and easy to explain in an interview rather than something overly ambitious.

## Current status

Right now the backend includes:

- health endpoint
- tea CRUD API
- tasting session CRUD API
- SQLAlchemy models and Alembic migrations
- pytest coverage for the main API flows
- Docker Compose setup for local development

Current API routes:

- `GET /health`
- `POST /teas`
- `GET /teas`
- `GET /teas/{tea_id}`
- `PUT /teas/{tea_id}`
- `DELETE /teas/{tea_id}`
- `POST /sessions`
- `GET /sessions`
- `GET /sessions/{session_id}`
- `PUT /sessions/{session_id}`
- `DELETE /sessions/{session_id}`

## Stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pytest
- Ruff
- Docker Compose

## Local setup

TeaShelf requires Python 3.10+.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

Run the API locally:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend
```

## Docker

```powershell
docker compose up --build
```

API: `http://localhost:8000`

Run migrations in Docker:

```powershell
docker compose exec api python -m alembic -c alembic.ini upgrade head
```

## Checks

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

## Notes

This is still an in-progress project. The milestone plan is in `plan.md`, and the product scope is in `spec.md`.
