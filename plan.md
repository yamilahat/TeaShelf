# plan.md

## Project name
TeaShelf

## Project approach
This project will be built milestone by milestone.
Each milestone should be small, testable, and reviewable.
Do not move to the next milestone until the current one is complete and validated.

## Rules
- Keep scope tight.
- Do not add features outside spec.md.
- Prefer one small clean step over one big patch.
- Human writes core decisions and important logic.
- AI helps with scaffolding, tests, review, and isolated repetitive pieces.

---

## Milestone 1: project skeleton

### Goal
Create the minimal backend structure and get the app running.

### Human-owned
- choose folder structure
- choose naming conventions
- choose initial app layout

### AI-assisted allowed
- scaffold folders/files
- generate minimal FastAPI entrypoint
- generate health endpoint
- suggest a clean starter structure

### Deliverables
- backend structure exists
- FastAPI app starts
- `/health` endpoint returns 200
- one basic test exists

### Validation
- `pytest -q`
- `ruff check .`

---

## Milestone 2: database setup

### Goal
Set up database connection, models, and migrations.

### Human-owned
- decide model fields
- decide entity relationships
- decide what belongs in Tea vs TastingSession

### AI-assisted allowed
- generate SQLModel or SQLAlchemy boilerplate
- generate Alembic setup
- review model design for missing edge cases
- generate migration skeleton if requested

### Deliverables
- Tea model exists
- TastingSession model exists
- initial migration exists
- database tables can be created

### Validation
- `alembic upgrade head`
- `pytest -q`
- `ruff check .`

---

## Milestone 3: tea CRUD API

### Goal
Add basic tea endpoints.

### Human-owned
- endpoint design
- request/response shape
- validation behavior
- service/repository structure if used

### AI-assisted allowed
- route boilerplate
- schema boilerplate
- test case generation
- review for missing validations

### Deliverables
- create tea
- list teas
- get tea by id
- update tea
- delete tea

### Validation
- `pytest -q`
- `ruff check .`

---

## Milestone 4: tasting session API

### Goal
Allow logging and viewing tasting sessions tied to teas.

### Human-owned
- session logic
- required vs optional fields
- rules for linking sessions to teas

### AI-assisted allowed
- route boilerplate
- test generation
- validation review
- small refactors

### Deliverables
- create tasting session
- list tasting sessions for a tea
- get tasting session
- delete tasting session

### Validation
- `pytest -q`
- `ruff check .`

---

## Milestone 5: filtering and search

### Goal
Make the tea inventory more usable.

### Human-owned
- decide filter behavior
- decide supported query params
- decide whether search is name/vendor-only or broader

### AI-assisted allowed
- help write query boilerplate
- suggest indexing ideas
- generate tests for filter combinations

### Deliverables
- filter by tea type
- filter by vendor
- optional text search by name
- tests for search/filter behavior

### Validation
- `pytest -q`
- `ruff check .`

---

## Milestone 6: simple stats

### Goal
Add a few lightweight stats to make the product feel complete.

### Human-owned
- choose which stats matter
- keep scope small

### AI-assisted allowed
- small query helpers
- response schema boilerplate
- tests

### Example stats
- total teas
- total tasting sessions
- average rating
- most tasted tea

### Validation
- `pytest -q`
- `ruff check .`

---

## Milestone 7: polish

### Goal
Make the repo portfolio-ready.

### Human-owned
- README narrative
- project explanation
- architecture summary
- tradeoff explanations

### AI-assisted allowed
- README cleanup
- docs formatting
- test coverage gap review
- code review pass for naming and consistency

### Deliverables
- strong README
- clear setup instructions
- clear explanation of architecture
- cleaned-up code paths
- no obvious dead code

### Validation
- `pytest -q`
- `ruff check .`

---

## Out of scope unless explicitly added later
- auth
- multi-user support
- social features
- recommendations
- scraping
- frontend
- background workers
- AI tasting analysis

---

## How to use AI on this project
Use AI mainly for:
- critique
- scaffolding
- isolated code generation
- test generation
- review
- debugging

Do not use AI to generate entire milestones in one shot.
Do not accept major architectural changes without manual review.
Do not merge code you cannot explain.
