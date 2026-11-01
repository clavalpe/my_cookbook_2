from dataclasses import dataclass
from uuid import uuid4

from my_cookbook.recipes.domain.recipe import Recipe
from my_cookbook.recipes.domain.recipe_id import RecipeId
from my_cookbook.recipes.domain.recipe_name import RecipeName
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

    def execute(self, requested_recipe: CreateRecipeDTO) -> CreateRecipeResult:
        recipe_name = RecipeName(requested_recipe.name)

        recipe = Recipe(RecipeId(uuid4()), recipe_name, requested_recipe.description)
        self._recipe_repository.save(recipe)

        return CreateRecipeResult(recipe.id)
