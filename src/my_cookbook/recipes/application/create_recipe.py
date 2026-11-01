from dataclasses import dataclass
from uuid import uuid4

from my_cookbook.recipes.domain.recipe import Recipe, RecipeName
from my_cookbook.recipes.domain.recipe_id import RecipeId
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository


@dataclass(frozen=True)
class CreateRecipeDTO:
    name: str
    description: str


@dataclass(frozen=True)
class CreateRecipeResult:
    id: RecipeId


class CreateRecipe:
    def __init__(self, recipe_repository: RecipeRepository) -> None:
        self._recipe_repository = recipe_repository

    def execute(self, create_repository_dto: CreateRecipeDTO) -> CreateRecipeResult:
        recipe_name = RecipeName(create_repository_dto.name)

        recipe = Recipe(
            RecipeId(uuid4()), recipe_name, create_repository_dto.description
        )
        self._recipe_repository.save(recipe)

        return CreateRecipeResult(recipe.id)
