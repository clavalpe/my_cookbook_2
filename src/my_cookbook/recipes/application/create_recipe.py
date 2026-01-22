from my_cookbook.recipes.application.create_recipe_dto import CreateRecipeDTO
from my_cookbook.recipes.domain.recipe import Recipe
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository


class CreateRecipe:
    def __init__(self, recipe_repository: RecipeRepository) -> None:
        self._recipe_repository = recipe_repository

    def execute(self, create_repository_dto: CreateRecipeDTO) -> None:
        recipe = Recipe(create_repository_dto.name, create_repository_dto.description)
        self._recipe_repository.save(recipe)