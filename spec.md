# spec.md

## Project name
TeaShelf

## One-line summary
TeaShelf is a backend-first tea inventory and tasting journal for a single user.

## Why this project exists
I want a focused portfolio project that demonstrates backend engineering:
- API design
- database modeling
- testing
- migrations
- Docker
- clean project structure

It should be simple enough to finish and polished enough to discuss in interviews.

## Target user
One user: the app owner.

This is intentionally single-user for v1 so the project stays focused on the core product instead of auth, permissions, sessions, email flows, and account management.

## Core problem
Tea enthusiasts often keep tea information scattered across notes, memory, spreadsheets, photos, and vendor pages.
This project centralizes:
- tea inventory
- tasting sessions
- ratings
- notes
- simple filtering and stats

## Core features for v1
- Create, edit, list, view, and delete teas
- Store tea details such as name, type, vendor, origin, and notes
- Record tasting sessions for a tea
- Save tasting notes and ratings
- Delete tasting sessions
- Filter/search teas
- View a few simple stats

## Non-goals for v1
- No social features
- No sharing
- No recommendations engine
- No LLM tasting assistant
- No scraping
- No multi-user support
- No mobile app
- No advanced analytics dashboard
- No marketplace/community functionality

## Technical constraints
- Python
- FastAPI
- PostgreSQL
- Alembic
- Docker Compose
- Backend-first
- Testable locally
- Keep architecture simple and explainable

## Product principles
- Finishable over impressive
- Clear over clever
- Small scope over feature sprawl
- Human-understandable over AI-generated complexity

## Human-authored areas
These should remain primarily human-authored unless explicitly requested otherwise:
- feature scope
- data model decisions
- API design
- business logic
- architectural choices

AI may assist with scaffolding, tests, review, boilerplate, and debugging.

## Initial entities
### Tea
Represents a tea in the inventory.

Likely fields:
- id
- name
- tea_type
- vendor
- origin
- harvest_year or production_year (optional)
- notes
- created_at
- updated_at

### TastingSession
Represents one tasting/brewing session for a tea.

Likely fields:
- id
- tea_id
- session_date
- rating
- notes
- water_temp_c (optional)
- steep_time_seconds (optional)
- leaf_grams (optional)
- water_ml (optional)
- created_at

## Success criteria
The project is successful when:
- I can run it locally with Docker Compose
- I can create and list teas
- I can log tasting sessions
- I can delete teas and tasting sessions
- I can filter/search teas
- tests pass
- the codebase is clean enough to explain confidently in an interview

## v1 definition of done
- backend API works locally
- migrations work
- basic tests exist for core behavior
- README explains setup and project purpose
- code structure remains simple and maintainable
