from my_cookbook.recipes.domain.recipe import Recipe
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository


class FakeRecipeRepository(RecipeRepository):
    def __init__(self) -> None:
        self.saved_recipes: list[Recipe] = []

    def save(self, recipe: Recipe) -> None:
        self.saved_recipes.append(recipe)
