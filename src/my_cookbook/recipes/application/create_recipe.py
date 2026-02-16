from dataclasses import dataclass

from my_cookbook.recipes.domain.exceptions import InvalidRecipeName
from my_cookbook.recipes.domain.recipe import Recipe, RecipeName
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository


@dataclass(frozen=True)
class CreateRecipeDTO:
    name: str
    description: str


class CreateRecipe:
    def __init__(self, recipe_repository: RecipeRepository) -> None:
        self._recipe_repository = recipe_repository

    def execute(self, create_repository_dto: CreateRecipeDTO) -> None:
        recipe_name = RecipeName(create_repository_dto.name)

        recipe = Recipe(recipe_name, create_repository_dto.description)
        self._recipe_repository.save(recipe)


