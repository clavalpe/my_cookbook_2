# Application layer

The use cases. They orchestrate; the logic lives in the domain and input/output sits behind a port.

## Shape of a use case

- One module per use case, in `application/`, named after the use case in snake_case.
- The class has **no suffix**: `CreateRecipe`, not `CreateRecipeUseCase` or `CreateRecipeService`.
- Main method `execute(<business name>: <Name>DTO) -> <Result>`. The type is a `DTO`, the parameter is named
  for what it is for the business (`requested_recipe`), never `dto`.
- `<Name>DTO` -and `<Name>Result` if it returns data- are frozen dataclasses **in the same module**.
- Dependencies come in through the constructor and are ports, never adapters.

```python
# example/application/{do_something}.py
class {DoSomething}:
    def __init__(self, {port}: {Port}) -> None:
        self._{port} = {port}

    def execute(self, {requested_thing}: {DoSomething}DTO) -> {Result}: ...
```

## What it does

- Builds the domain entities and value objects from the DTO and hands them to the ports.
- **Generates the id** of what it creates, when the entity needs one and the use case is the one creating it.

## What it does not do

- **It does not translate to external formats.** It returns domain objects or a `Result`; serializing
  belongs to the boundary.
- **It does not catch exceptions to turn them into HTTP codes.** It propagates them typed and the
  entrypoint maps them.
- **It does not talk to the database or to FastAPI.** It only knows ports.
- **It holds no business rules**: it asks the domain.

## Anti-patterns

- A use case that imports an adapter or `sqlalchemy`.
- A `try/except` that translates a domain exception into a status code.
- A business rule written in `execute` instead of in the domain.
- A DTO built on Pydantic.
