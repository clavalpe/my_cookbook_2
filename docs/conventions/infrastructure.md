# Infrastructure layer

Port adapters, boundary models and entrypoints. It is the only layer that knows there is a database or an
HTTP server.

## What comes from outside is validated on the way in

A request body is validated with one **Pydantic** model per concept, in the controller file of its feature,
next to its router. A field we do not know is a rejection (`extra="forbid"`), not an ignored field.
Pydantic does not leave this layer: the controller turns the model into the use case DTO and calls
`execute`.

## HTTP contract

The API is internal: there are no custom status codes.

- **Success**: the standard code for the verb (`201` on create) and the body the endpoint contract declares.
- **Business or validation error**: always **`400`**, with a single body for the whole API:

```json
{"code": "<ErrorCode>", "detail": "<explanation for a person>"}
```

- `code` is a closed `StrEnum`, with one member per domain exception the entrypoint knows how to map
  (`InvalidRecipeName` → `INVALID_RECIPE_NAME`). It lives in `infrastructure/`: it is contract vocabulary,
  not domain vocabulary.
- `detail` is human-readable text, in English.
- **A domain exception with no mapping is not turned into a `400`**: it is a program failure and comes out
  as `500`. Adding an exception to the domain forces a decision about its `code`.
- The exception → `code` mapping is declared in **one place** (an exception handler registered in
  `src/app.py`), not in each endpoint.
- A malformed request body (invalid JSON, missing field) also comes out as `400` with this same body, not
  with FastAPI's default `422`.

## Adapters

- They implement one port and nothing else. **The module is named after the implementation**, not the
  port: `postgres_recipe_repository.py` implements `RecipeRepository`.
- **The SQLAlchemy session comes in through the constructor.** The adapter neither creates nor closes it;
  whoever wires the dependency graph does.
- **The SQLAlchemy table model belongs to infrastructure** and does not necessarily look like the entity.
  The conversion lives in the adapter (or in the model), never in the use case.
- **A library exception does not leave the adapter**: it is translated into one of our own.

## Database and migrations

- **alembic creates the schema**, not `create_all`. Every table change is a reviewable migration in
  `migrations/`.
- **Configuration comes from the environment** (`PG_*`), read in a single place. No connection URL written
  in the code.
- Migrations are applied with `make migrate` and generated with `make migrations`.

## Controllers and entrypoints

- **One file per feature** in `infrastructure/controllers/`, named `{feature}_controller.py`. It holds the
  router, the request model and the response model of that feature, all together: nothing of the feature's
  HTTP contract lives anywhere else.
- A controller does three things: validates the input, calls `execute`, returns the result in the contract
  format. Anything else belongs to another layer.
- **The providers that wire the dependency graph** -session, adapter, use case- live in
  `infrastructure/dependencies.py`, the only place where it is built. Controllers receive the already-built
  use case through `Depends`, and import their providers from there, never from `src/app.py`.
- `src/app.py` only creates the FastAPI app, includes the router of each controller and registers the
  exception handlers.
- Routes with a trailing slash, like `/health/`.

## Anti-patterns

- A business rule in a controller or an adapter.
- A request or response model outside the controller file of its feature.
- A dependency provider in a controller or in `src/app.py` instead of `infrastructure/dependencies.py`.
- A `try/except` per controller to produce the `400`, instead of a single handler.
- A status code other than `400` for a business error.
- A Pydantic model in `domain/` or `application/`.
- An adapter that opens its own connection.
- `create_all` instead of a migration.
- A database URL or password written in the code.
