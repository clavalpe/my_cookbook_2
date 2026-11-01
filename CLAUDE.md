# my_cookbook — repo instructions

Internal recipe-book API: FastAPI + PostgreSQL, with domain, application and infrastructure separated.
Code and documentation are written in English.

## Critical rule: conventions first

**BEFORE proposing any code change, tests included:**

1. **IDENTIFY** the affected layer in the table below.
2. **READ** with the Read tool the `docs/conventions/` file that matches it, in this session. Remembering
   it from another one does not count.
3. **APPLY** what it says, literally.
4. **DO NOT** assume, improvise or bring in patterns from other projects.

### Conventions by layer

**Always**, before any code change: `docs/conventions/code-style.md`.

| If you are going to touch... | Read |
|---|---|
| Folder structure, dependencies, tooling | `docs/conventions/architecture.md` |
| Entities, value objects, ports, exceptions | `docs/conventions/domain.md` |
| Use cases | `docs/conventions/application.md` |
| Adapters, endpoints, database, migrations | `docs/conventions/infrastructure.md` |
| Tests, mothers, doubles | `docs/conventions/testing.md` |
| Branches, commits, pull requests, merge | `docs/conventions/git-workflow.md` |

### Who reads what

| What it is | Where it lives | Who reads it |
|---|---|---|
| **The code yardstick** | `code-style`, `architecture`, `domain`, `application`, `infrastructure`, `testing` | Whoever implements before writing and whoever reviews before blocking |
| **How we work here** | `git-workflow.md`, this `CLAUDE.md` | You and me in session |

## Code that is NOT a reference

It predates the conventions. Do not imitate it when writing new code:

- `Recipe` and `CreateRecipe`: they do not yet fully follow `docs/conventions/domain.md` (the recipe has no
  id) nor `docs/conventions/application.md` (the name of the `execute` parameter). They are migrated when
  touched.

## How we work

- **TDD**: first the failing test, then the minimal code to make it pass, then the refactor.
- **Outside-in**: first the use case with ports doubled, then the adapter and the endpoint.
- **A business rule is written once**, in the domain.

## How a change is measured

```bash
make env-start   # starts app and db
make linting     # ruff check + ruff format --check + mypy
make test        # pytest inside the container
```

Everything green before considering anything done. The commands run inside the `app` container; the
`Makefile` is the interface.

## Database

PostgreSQL 17 (the `db` service in `docker/docker-compose.yml`), SQLAlchemy 2 and alembic. The schema is
created by migrations (`make migrations`, `make migrate`), never `create_all`.
