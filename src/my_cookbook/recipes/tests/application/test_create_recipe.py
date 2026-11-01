from unittest.mock import MagicMock, create_autospec

import pytest

from my_cookbook.recipes.application.create_recipe import CreateRecipe
from my_cookbook.recipes.domain.exceptions import InvalidRecipeName
from my_cookbook.recipes.domain.recipe import RecipeName
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository
from my_cookbook.recipes.tests.mothers.create_recipe_dto_mother import (
    CreateRecipeDTOMother,
)


class TestCreateRecipe:
    @pytest.fixture
    def mock_recipe_repository(self) -> MagicMock:
        repository: MagicMock = create_autospec(
            RecipeRepository, spec_set=True, instance=True
        )
        return repository

    def test_create_recipe(self, mock_recipe_repository: MagicMock) -> None:
        create_recipe_dto = CreateRecipeDTOMother.omelette()

        CreateRecipe(mock_recipe_repository).execute(create_recipe_dto)

        mock_recipe_repository.save.assert_called_once()
        recipe = mock_recipe_repository.save.call_args[0][0]
        assert recipe.name == RecipeName("Omelette")
        assert recipe.description == "Omelette description"

    def test_does_not_allow_to_create_an_empty_name_recipe(
        self, mock_recipe_repository: MagicMock
    ) -> None:
        create_recipe_dto = CreateRecipeDTOMother.named("")

        with pytest.raises(InvalidRecipeName):
            CreateRecipe(mock_recipe_repository).execute(create_recipe_dto)

    def test_does_not_allow_to_create_a_recite_with_a_short_name(
        self, mock_recipe_repository: MagicMock
    ) -> None:
        create_recipe_dto = CreateRecipeDTOMother.named("Ome")

        with pytest.raises(InvalidRecipeName):
            CreateRecipe(mock_recipe_repository).execute(create_recipe_dto)

    def test_returns_the_id_of_the_recipe_handed_to_the_repository(
        self, mock_recipe_repository: MagicMock
    ) -> None:
        result = CreateRecipe(mock_recipe_repository).execute(
            CreateRecipeDTOMother.omelette()
        )

        saved_recipe = mock_recipe_repository.save.call_args[0][0]
        assert result.id == saved_recipe.id

    def test_creates_a_different_recipe_on_every_execution_with_the_same_dto(
        self, mock_recipe_repository: MagicMock
    ) -> None:
        create_recipe = CreateRecipe(mock_recipe_repository)
        dto = CreateRecipeDTOMother.omelette()

        first_result = create_recipe.execute(dto)
        second_result = create_recipe.execute(dto)

        saved_ids = [
            call.args[0].id for call in mock_recipe_repository.save.call_args_list
        ]
        assert saved_ids[0] != saved_ids[1]
        assert first_result.id != second_result.id

    def test_allows_to_create_a_recipe_with_a_name_of_exactly_five_characters(
        self, mock_recipe_repository: MagicMock
    ) -> None:
        CreateRecipe(mock_recipe_repository).execute(
            CreateRecipeDTOMother.named("Pasta")
        )

        mock_recipe_repository.save.assert_called_once()
        saved_recipe = mock_recipe_repository.save.call_args[0][0]
        assert saved_recipe.name == RecipeName("Pasta")

    def test_does_not_allow_to_create_a_recipe_with_a_name_of_four_characters(
        self, mock_recipe_repository: MagicMock
    ) -> None:
        with pytest.raises(InvalidRecipeName):
            CreateRecipe(mock_recipe_repository).execute(
                CreateRecipeDTOMother.named("Soup")
            )

        mock_recipe_repository.save.assert_not_called()

    def test_explains_the_minimum_length_when_the_name_is_too_short(
        self, mock_recipe_repository: MagicMock
    ) -> None:
        with pytest.raises(InvalidRecipeName) as error:
            CreateRecipe(mock_recipe_repository).execute(
                CreateRecipeDTOMother.named("Soup")
            )

        assert str(error.value) == "recipe name must have at least 5 characters"
