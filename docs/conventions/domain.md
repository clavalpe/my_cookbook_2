# Domain layer

Entities, value objects, ports and exceptions. Pure Python: it does not import FastAPI, SQLAlchemy or
Pydantic.

## Value objects

- **Frozen dataclasses (`frozen=True`).** They validate on construction: a value object that exists is
  valid.
- A piece of data with a rule (`RecipeName` cannot be short) is a value object, not a bare `str` with the
  validation in the use case.
- **A value object that holds the data owns the question.** If each consumer derives a condition by hand
  from a field, the rule is spread out even though the field lives in one place.
- They compare by value, and tests use real instances: never mock value objects.

## Entities

- An entity has identity. **The id is born in the domain or the application, never in the database**: the
  recipe exists with its `RecipeId` (a UUID) before it is saved, and `save` returns nothing.
- What builds a valid entity is its constructor; there are no half-built states.

## Closed vocabulary

- A closed set of values is a `StrEnum` in its own module.
- **An absent state is a member of the vocabulary**, not a `| None`.
- **A port answers with the vocabulary, not with a `bool`** derived from it.

## Ports

- One abstract port (`abc.ABC`) per file, in `domain/`, using business vocabulary and no trace of the
  technology: `RecipeRepository.save(recipe)`, not `insert_row`.
- It is what the use case knows. Its adapter lives in `infrastructure/`.

## Exceptions

- Domain exceptions live together in `domain/exceptions.py` and read as a catalogue.
- Each one names **one business reason** (`InvalidRecipeName`), not a technical layer.
- **The message describes the reason**, it does not repeat the class name.

## No raw `dict` as a return value

What domain logic returns is a value object or an entity, not a `dict` or a tuple of positions that carry
meaning.

## Anti-patterns

- Pydantic, SQLAlchemy or FastAPI imported in `domain/`.
- An id that only exists after saving.
- A `bool` or a `| None` where the domain has a vocabulary.
- Validating a name in the use case or the endpoint instead of in its value object.
- An infrastructure exception (`IntegrityError`) escaping its adapter.
