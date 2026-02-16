from dataclasses import dataclass

from my_cookbook.recipes.domain.exceptions import InvalidRecipeName


@dataclass
class RecipeName:
    _value: str

    def __init__(self, value: str) -> None:
        if value == "" or len(value) < 5:
            raise InvalidRecipeName()

        self._value = value

    @property
    def value(self) -> str:
        return self._value


class Recipe:
    def __init__(self, name: RecipeName, description: str) -> None:
        self.name = name
        self.description = description