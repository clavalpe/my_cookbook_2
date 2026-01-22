from unittest.mock import create_autospec
import pytest

from my_cookbook.recipes.application.create_recipe import CreateRecipe
from my_cookbook.recipes.application.create_recipe_dto import CreateRecipeDTO
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository


class TestCreateRecipe:
    @pytest.fixture
    def mock_recipe_repository(self):
        return create_autospec(RecipeRepository, spec_set=True, instance=True)

    def test_create_recipe(self, mock_recipe_repository) -> None:
        create_recipe_dto = CreateRecipeDTO(
            name = "Omelette",
            description="Omelette description",
        )

        CreateRecipe(mock_recipe_repository).execute(create_recipe_dto)

        mock_recipe_repository.save.assert_called_once()
        recipe = mock_recipe_repository.save.call_args[0][0]
        assert recipe.name == "Omelette"
        assert recipe.description == "Omelette description"





