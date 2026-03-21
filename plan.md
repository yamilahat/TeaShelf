# plan.md

## Project name
TeaShelf

## Project approach
This project will be built milestone by milestone.
Each milestone should be small, testable, and reviewable.
Do not move to the next milestone until the current one is complete and validated.

## Rules
- Keep scope tight.
- Do not add features outside the plan.
- Prefer one small clean step over one big patch.
- Human writes core decisions and important logic.
- AI helps with scaffolding, tests, review, and isolated repetitive pieces.
- Frontend work may only expose already-completed backend capabilities and must not expand feature scope or force backend API changes.

---

## Completed milestones

| # | Milestone | Status |
|---|---|---|
| 1 | Project skeleton | ✅ Done |
| 2 | Database setup | ✅ Done |
| 3 | Tea CRUD API | ✅ Done |
| 3.5 | Demo client shell (frontend) | ✅ Done |
| 4 | Tasting session API | ✅ Done |
| 5 | Filtering and search | ✅ Done |
| — | Teaware model, CRUD, UI | ✅ Done |
| — | Tea type enum + searchable dropdown | ✅ Done |
| — | Date inputs: free text → native date picker | ✅ Done |

---

## Milestone 6: Simple stats & dashboard

### Goal
Add lightweight stats and a home page to make the product feel complete.

### Human-owned
- Which stats matter
- Whether stats live in a new `/stats` endpoint or are computed client-side from existing data

### AI-assisted allowed
- Query boilerplate
- Response schema
- Tests
- Frontend dashboard component

### Deliverables
- `GET /stats` endpoint: total teas, total sessions, average rating, most-brewed tea, sessions this month
- `/dashboard` page showing those stats
- Aggregated stats on TeaDetailPage: session count, avg rating, last brewed date

### Validation
- `pytest -q`
- `ruff check .`
- Dashboard renders without errors

---

## Milestone 6.5: UX hardening

### Goal
Fix the small issues that make the app feel unpolished.

### Human-owned
- Rating scale decision (0–10)
- Whether to keep inline session creation or move to dedicated page

### AI-assisted allowed
- Route/component scaffolding
- Test generation for new constraints

### Deliverables
- Sessions list sorted newest-first (`ORDER BY session_date DESC`)
- Rating capped 0–10 in backend schema (`ge=0, le=10`) and form
- Session creation moved to `/sessions/new` (SessionsPage becomes list-only)
- Session filtering by tea and date range

### Validation
- `pytest -q` · new tests for sort order and rating bounds
- `ruff check .`

---

## Milestone 7: Brew parameters

### Goal
Capture the data that explains why a session tasted a certain way.

### Human-owned
- Final field list and whether `brew_method` is an enum or free text
- Unit choices (°C vs °F, ml vs oz)

### AI-assisted allowed
- Migration skeleton
- Schema + model boilerplate
- Form fields
- Tests

### Proposed fields (nullable)
- `brew_method` — enum: gongfu / western / grandpa / cold brew
- `water_temp_c` — int
- `steep_time_seconds` — int
- `water_ml` — int
- `leaf_grams` — float

### Validation
- `alembic upgrade head`
- `pytest -q`
- Form renders new fields

---

## Milestone 8: Tea inventory depth

### Goal
Track the physical state of a tea (quantity remaining, lifecycle status).

### Human-owned
- Status enum values
- Whether finished teas are hidden by default

### Proposed fields
- `quantity_grams` (float, nullable)
- `status` enum: `active | finished | wishlist`

### Deliverables
- Migration + model + schema update for Tea
- TeaForm new fields
- TeasPage filter by status
- Tests

### Validation
- `alembic upgrade head`
- `pytest -q`

---

## Milestone 9: Polish & portfolio-ready

### Goal
Make the repo presentable and explainable.

### Human-owned
- README narrative and architecture summary
- Tradeoff explanations

### AI-assisted allowed
- README cleanup and formatting
- Test coverage gap review
- Code review pass for naming and consistency

### Deliverables
- Strong README with setup, architecture, tradeoffs
- No dead code
- Fresh `docker-compose up` works from a clean clone

### Validation
- `pytest -q`
- `ruff check .`

---

## Infrastructure — when to do each thing

| Concern | When | Action |
|---|---|---|
| **Backups** | **Now** | `pg_dump` cron job; 7 rolling daily dumps |
| **HTTPS** | Before any LAN/internet exposure | Caddy in `docker-compose.yml`; automatic TLS |
| **Auth / multi-user** | Before sharing with others | FastAPI Users + JWT; adds `user_id` to every model — do before new features if multi-user planned |
| **Encryption at rest** | Only if deploying to untrusted cloud | Cloud provider encrypted volume / LUKS |

```
Personal local only?   → Backups only
Home server / LAN?     → Backups + HTTPS
Internet / shared?     → Backups + HTTPS + Auth
Cloud VM?              → All of the above + encrypted volume
```

---

## Out of scope unless explicitly added
- Auth / multi-user support
- Social features / sharing
- Recommendations / AI analysis
- Tea scraping / external data sources
- Background workers
- Photo uploads
- Frontend pagination (until data size demands it)

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
