from dataclasses import dataclass
from typing import ClassVar

from my_cookbook.recipes.domain.exceptions import InvalidRecipeName
from my_cookbook.recipes.domain.recipe_id import RecipeId


@dataclass
class RecipeName:
    MINIMUM_LENGTH: ClassVar[int] = 5

    _value: str

    def __init__(self, value: str) -> None:
        if len(value) < self.MINIMUM_LENGTH:
            raise InvalidRecipeName(self.MINIMUM_LENGTH)

        self._value = value

    @property
    def value(self) -> str:
        return self._value


class Recipe:
    def __init__(self, id: RecipeId, name: RecipeName, description: str) -> None:
        self.id = id
        self.name = name
        self.description = description
