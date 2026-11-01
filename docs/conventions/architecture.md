# Architecture and tooling

## Structure

```
src/
  app.py                              FastAPI entrypoint: creates the app, includes the routers and registers the exception handlers
  my_cookbook/
    {context}/                        one context per business area (today, `recipes`)
      domain/
        {value_object}.py             one value object per module
        {entity}.py                   one entity per module
        {port}.py                     one port per file
        exceptions.py                 the domain exceptions, together
      application/
        {use_case}.py                 one use case per module, with its DTO
      infrastructure/
        {impl}_{port}.py              the adapter is named after its implementation
        {record}.py                   one table model per concept
        controllers/
          {feature}_controller.py     one file per feature: its router, request and response models together
        dependencies.py               the providers that wire session, adapter and use case
      tests/                          co-located, mirroring the layers above (controllers included)
        mothers/                      Object Mothers
migrations/                           alembic
```

- **One concept per module**, together with whatever cannot exist without it. The test: if you delete the
  main concept, is the other type left with no consumer and no meaning of its own? Only then do they share a
  file. A type that another place constructs or another layer consumes is a concept and gets its own module.
- Domain exceptions are the exception to the rule: they live together in `domain/exceptions.py`.
- **Dependencies point inwards**: `infrastructure` knows `application` and `domain`, `application` knows
  `domain`, and `domain` knows nobody.
- **Tests live inside the context**, not in a separate folder, and mirror the layers they test. There is no
  domain test tree (see `docs/conventions/testing.md`).

## A business rule is written once

The rule of three governs how similar code looks: repeated pieces get extracted when extracting leaves the
place better. **It does not govern where a decision lives.** A business rule -which name is valid, what
counts as a duplicate recipe- is written once, in the domain, and whoever needs it asks.

**The test: if this decision changed, how many files would have to change for the program to stay
coherent?** One, or it is spread out. Two places that say the same thing today in different words are
already spread out.

## Tooling

Python 3.14, FastAPI, SQLAlchemy 2, alembic, psycopg 3, PostgreSQL 17, `pytest`, `mypy`, `ruff`.
Everything runs inside the containers under `docker/`; the `Makefile` is the interface.

- **Frozen `dataclasses` for value objects and DTOs.** Pydantic only appears in the models that cross the
  HTTP boundary (see `docs/conventions/infrastructure.md`).
- **`abc.ABC` for ports**, `StrEnum` for closed vocabularies, `unittest.mock` for doubles.

## Anti-patterns

- Pydantic in `domain/` or in a use case DTO.
- `domain/` importing from `application/` or `infrastructure/`.
- A business rule written in two places, even if the two wordings differ.
- A helper that both copies call from where they were: the decision is still spread out, now with an
  indirection in front.
