from dataclasses import dataclass

from my_cookbook.recipes.domain.exceptions import InvalidRecipeName
from my_cookbook.recipes.domain.recipe_id import RecipeId


@dataclass
class RecipeName:
    _value: str

    def __init__(self, value: str) -> None:
        if len(value) < 5:
            raise InvalidRecipeName()

        self._value = value

    @property
    def value(self) -> str:
        return self._value


class Recipe:
    def __init__(self, id: RecipeId, name: RecipeName, description: str) -> None:
        self.id = id
        self.name = name
        self.description = description
