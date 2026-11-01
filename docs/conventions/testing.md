# Tests

## How everything is measured

```bash
make linting    # ruff check + ruff format --check + mypy
make test       # pytest inside the container
```

Both run inside the containers (`make env-start` first). A `pytest` run with your machine's interpreter
passes or fails depending on what you have installed, and that is not a yardstick.

## Shape of a test

- **Inside a class**, grouped by the behavior they pin down. Never loose functions.
- **Zero prose**: no comments and no docstrings. The test name is the sentence.
- The name says **what is guaranteed and why**, not which method is called:
  `test_does_not_allow_to_create_a_recipe_with_a_short_name`.
- **The name is written in business terms**, as `docs/conventions/code-style.md` requires of every name. It
  does not mention doubles, ports, DTOs, sessions or calls: `test_creates_a_recipe_with_the_requested_name_and_description`,
  not `test_hands_the_repository_a_recipe_with_the_name_and_description_of_the_dto`. If the name only makes
  sense to someone who has read the code, rewrite it as what the business would observe.
- A test's helpers are `@staticmethod`s of its test class or live in a shared module, never loose at module
  level. Fixtures go inside the class.
- Arrange / act / assert structure, separated by a blank line.

## What is tested and what is not

- **Outside-in**, in this order: first the use cases with the ports doubled, then infrastructure. What is
  inside the domain is covered **along that path**.
- **There are no domain unit tests**, not even when the domain has behavior: it is checked through the real
  path it arrives by. The only exception is a value object with its own validation that cannot be reached
  any other way. A test that only checks that a dataclass stores what you give it measures the language.
- **Application**: ports doubled through the constructor, and the assert on the **observable effect** (what
  the port received, what the use case returned).
- **Database adapter**: tested against the real Postgres of the environment, not against a doubled session.
  A `Session` double would only check that we call our own mapping. Each test leaves the database as it
  found it.
- **Controller**: **one test file per controller** (`tests/infrastructure/controllers/test_{feature}_controller.py`)
  with two kinds of test, and nothing that the application tests already cover:
  - **One happy path against the real database**: the real use case, adapter and session, no doubles, to prove
    the layers are wired together. It asserts the response and what ended up in the database, and deletes what
    it created so the database is as it was found. It is the **only** test of the controller that touches the
    database, and it already shows how the request becomes the use case input and how the result is
    serialized, so no other test repeats that.
  - **Unit tests with the application layer doubled** (the use case replaced through `dependency_overrides`),
    only for what the controller decides on its own and the happy path does not show: what is rejected before
    the use case runs, how an exception coming out of the use case is answered, any serialization the happy
    path does not exercise. Business rules are never tested here: they are tested at the application level.
  The assert is the **status code and the literal body** of the response, not a model of it rewritten in the
  test.
- **Dependency providers** (`tests/infrastructure/test_dependencies.py`): tested on their own, with their
  collaborators doubled, since they are not part of any controller.
- **Before adding a test, check whether the behavior is already covered.** It only goes in if it adds a
  different dimension.

## Object Mothers

A test's objects are built by a mother, not by the test itself: `tests/mothers/{thing}_mother.py`. It gives
sensible defaults and lets each test name **only what its case changes**. Its methods are named scenarios,
not a `create(...)` with everything defaulted.

## Doubles

- **`create_autospec(X, spec_set=True, instance=True)`** for stateless ports.
- **Hand-written stateful doubles** when the test needs to ask what it was handed.
- **A double doubles what its name says and nothing else.**
- **A double is named as a double**: `mock_` for an autospec double (`mock_recipe_repository`), `fake_` for a
  hand-written one. Business naming applies to everything else in the test, but a double must read as one.
- **Never mock value objects**: use real instances.
- The arrange **is not built with the piece under test**.

## Asserts

- The assert compares the **whole value**. A loose substring passes any text that contains it.
- A test that expects an exception checks its type and, when the message is part of the contract, the
  whole message.

## Anti-patterns

- A test as a loose function.
- A comment or a docstring in a test.
- A test name that describes the mechanism (doubles, ports, DTOs, calls) instead of what the business observes.
- A domain test that only exercises a dataclass.
- Building a domain object by hand in the test when there is a mother.
- A loose module-level test helper, or one repeated in two files.
- A database adapter test against a doubled `Session`.
- A controller test that exercises a business rule through a doubled repository.
- More than one test file for the same controller, or a second database-backed test of it.
- A controller test that repeats what the happy path or the application tests already cover (the request-to-input mapping, the id serialization, a business rule).
- A test that leaves rows in the database for the next one.
- An assert against a reimplemented model of the format instead of the literal payload.
