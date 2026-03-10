## Architecture
- FastAPI backend
- PostgreSQL database
- SQLModel or SQLAlchemy models
- Alembic migrations
- Docker Compose for local dev

## Rules
- Complete one milestone at a time.
- Run validation after each milestone.
- If validation fails, repair before continuing.
- Do not expand scope without updating this file.

## Milestone 1: Project skeleton
Goal:
Create the backend skeleton, app entrypoint, dependency setup, and health endpoint.

Acceptance criteria:
- FastAPI app starts
- `/health` returns 200
- basic test passes

Validation:
- `pytest -q`
- `ruff check .`

## Milestone 2: Data model
Goal:
Add Tea and TastingSession models plus migration.

Acceptance criteria:
- models exist
- migration runs
- database tables are created
- tests cover basic persistence

Validation:
- `alembic upgrade head`
- `pytest -q`
- `ruff check .`

## Milestone 3: CRUD API
Goal:
Add create/list/get endpoints for teas and tasting sessions.

Acceptance criteria:
- can create tea
- can list teas
- can create tasting session
- invalid payloads are rejected

Validation:
- `pytest -q`
- `ruff check .`

## Milestone 4: Search/filter
Goal:
Add filtering by tea type, vendor, and rating.

Acceptance criteria:
- query params work
- tests cover filtering behavior

Validation:
- `pytest -q`
- `ruff check .`

## Decision notes
- v1 is backend-first
- auth postponed
- recommendations postponed
- scraping postponed