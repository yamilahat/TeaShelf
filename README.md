# TeaShelf

TeaShelf is a backend-first tea inventory and tasting journal for a single user.

The project is intentionally small and explicit so it is easy to finish, test, and explain in interviews. The current implementation now includes a minimal FastAPI app, Docker-based local startup, and database scaffolding with SQLAlchemy and Alembic.

## Current status

- FastAPI app starts
- `GET /health` returns `200`
- Basic health test exists
- PostgreSQL, SQLAlchemy, and Alembic scaffolding are in place
- Tea and tasting-session models are not implemented yet
- No CRUD endpoints exist yet

## Tech stack

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pytest
- Ruff
- Docker Compose

## Local setup

TeaShelf requires Python 3.10 or newer. Python 3.11 is the recommended local version.

### Windows example

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

### Run the app locally

Start PostgreSQL first, either with Docker Compose or your own local instance.

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend
```

Then open `http://127.0.0.1:8000/health`.

## Run with Docker

```powershell
docker compose up --build
```

Services:

- API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Health endpoint: `http://localhost:8000/health`

The API container runs from `/app` and receives `DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/teashelf`.

### Run Alembic in Docker

```powershell
docker compose exec api python -m alembic -c alembic.ini upgrade head
```

## Database boilerplate

Scaffold included in this repo:

- SQLAlchemy base: `backend/app/db/base.py`
- Engine and session helper: `backend/app/db/session.py`
- Model registration package: `backend/app/models/__init__.py`
- Alembic config: `alembic.ini`
- Alembic environment: `alembic/env.py`
- Alembic versions folder: `alembic/versions/`

Suggested next steps for you:

1. Add your `Tea` and `TastingSession` model modules under `backend/app/models/`.
2. Import those models in `backend/app/models/__init__.py` so Alembic can see them.
3. Generate the initial migration.
4. Run `alembic upgrade head`.

## Validation

Run the project checks from the repo root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

When you add models and Alembic is installed locally, also run:

```powershell
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "initial schema"
.\.venv\Scripts\python.exe -m alembic upgrade head
```

## Project roadmap

The milestone plan lives in `plan.md`.

The product scope and constraints live in `spec.md`.
