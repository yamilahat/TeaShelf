# TeaShelf

TeaShelf is a backend-first tea inventory and tasting journal for a single user.

The project is intentionally small and explicit so it is easy to finish, test, and explain in interviews. The current implementation is an early foundation: a FastAPI app with a health endpoint, project tooling, and Docker-based local startup.

## Current status

- FastAPI app starts
- `GET /health` returns `200`
- Basic health test exists
- Database models and CRUD endpoints are not implemented yet

## Tech stack

- Python
- FastAPI
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

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend
```

Then open `http://127.0.0.1:8000/health`.

## Run with Docker

```powershell
docker compose up --build
```

The API will be available at `http://localhost:8000/health`.

## Validation

Run the project checks from the repo root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

## Project roadmap

The milestone plan lives in `plan.md`.

The product scope and constraints live in `spec.md`.

The next major milestone is database setup with PostgreSQL and Alembic, followed by a narrow first slice of tea CRUD.
