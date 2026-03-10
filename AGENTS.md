## Project context
Project name: TeaShelf

This is a portfolio project for learning and job search.
The project is a backend-first tea inventory and tasting journal.
I want the codebase to stay simple, explicit, and easy to explain in interviews.

## Working style
- Do not implement large features unless explicitly asked.
- Prefer review, critique, scaffolding, small isolated generation, and debugging help.
- Assume I want to write core business logic myself.
- Do not rewrite unrelated files.
- Keep patches minimal and easy to review.
- Ask before introducing a new dependency.
- Ask before changing architecture or folder structure.
- Do not create clever abstractions unless they solve a real repeated problem.

## What AI is allowed to help with
- project skeleton and boilerplate
- config files
- test skeletons and test cases
- linting / formatting setup
- Docker / compose setup
- small refactors
- explaining tradeoffs
- reviewing my code
- generating isolated models, schemas, or route stubs when requested

## What should stay human-authored unless explicitly requested
- architecture decisions
- API shape
- database schema design
- business logic
- tricky queries
- feature scope decisions
- naming of major concepts
- final code review before commit

## Code style
- Prefer simple, readable code.
- Prefer explicit functions over premature abstractions.
- Follow existing patterns before introducing new ones.
- Keep functions focused.
- Use clear names.
- Add short comments only when they improve understanding.
- Do not add "enterprise" structure for a small project.

## Validation
After code changes, run:
- `pytest -q`
- `ruff check .`

If formatting is set up, also run:
- `ruff format --check .`

If models change, ensure migrations are updated.

## Done criteria
A task is done only when:
- the requested scope is complete
- tests pass
- lint passes
- the patch is small enough to review comfortably
- the final response explains:
  - what changed
  - which files changed
  - how it was validated
  - any concerns or follow-up suggestions

## Important repo behavior
- Do not implement future milestones unless explicitly asked.
- Do not silently expand scope.
- Do not turn this into a multi-user or social product in v1.
- Do not add auth unless explicitly asked.
