from dataclasses import dataclass

from my_cookbook.recipes.domain.exceptions import InvalidRecipeName
from my_cookbook.recipes.domain.recipe import Recipe
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository


@dataclass(frozen=True)
class CreateRecipeDTO:
    name: str
    description: str


class CreateRecipe:
    def __init__(self, recipe_repository: RecipeRepository) -> None:
        self._recipe_repository = recipe_repository

    def execute(self, create_repository_dto: CreateRecipeDTO) -> None:
        if create_repository_dto.name == "" or len(create_repository_dto.name) <5:
            raise InvalidRecipeName("Recipe name cannot be empty")

        recipe = Recipe(create_repository_dto.name, create_repository_dto.description)
        self._recipe_repository.save(recipe)


