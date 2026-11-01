from typing import cast
from uuid import UUID

from my_cookbook.recipes.domain.recipe import Recipe
from my_cookbook.recipes.domain.recipe_id import RecipeId
from my_cookbook.recipes.domain.recipe_name import RecipeName


class RecipeMother:
    OMELETTE_ID: UUID = UUID("00000000-0000-0000-0000-000000000001")
    ANOTHER_OMELETTE_ID: UUID = UUID("00000000-0000-0000-0000-000000000002")

    @classmethod
    def omelette(cls) -> Recipe:
        return Recipe(
            RecipeId(cls.OMELETTE_ID),
            RecipeName("Omelette"),
            "Omelette description",
        )

    @classmethod
    def another_omelette(cls) -> Recipe:
        return Recipe(
            RecipeId(cls.ANOTHER_OMELETTE_ID),
            RecipeName("Omelette"),
            "Omelette description",
        )

    @classmethod
    def gazpacho_with_the_id_of_the_omelette(cls) -> Recipe:
        return Recipe(
            RecipeId(cls.OMELETTE_ID),
            RecipeName("Gazpacho"),
            "Gazpacho description",
        )

    @classmethod
    def omelette_without_description(cls) -> Recipe:
        return Recipe(
            RecipeId(cls.OMELETTE_ID),
            RecipeName("Omelette"),
            cast(str, None),
        )
