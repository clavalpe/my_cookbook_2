from my_cookbook.recipes.domain.recipe_id import RecipeId
from my_cookbook.recipes.domain.recipe_name import RecipeName


class Recipe:
    def __init__(self, id: RecipeId, name: RecipeName, description: str) -> None:
        self.id = id
        self.name = name
        self.description = description
