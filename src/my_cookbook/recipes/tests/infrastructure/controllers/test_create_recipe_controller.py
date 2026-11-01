from collections.abc import Iterator
from unittest.mock import MagicMock, create_autospec

import pytest
from fastapi.testclient import TestClient

from app import app
from my_cookbook.recipes.application.create_recipe import (
    CreateRecipe,
    CreateRecipeResult,
)
from my_cookbook.recipes.domain.recipe_id import RecipeId
from my_cookbook.recipes.infrastructure.dependencies import get_create_recipe
from my_cookbook.recipes.tests.mothers.create_recipe_dto_mother import (
    CreateRecipeDTOMother,
)
from my_cookbook.recipes.tests.mothers.recipe_mother import RecipeMother


class TestCreateRecipeController:
    @pytest.fixture
    def mock_create_recipe(self) -> MagicMock:
        create_recipe: MagicMock = create_autospec(
            CreateRecipe, spec_set=True, instance=True
        )
        create_recipe.execute.return_value = CreateRecipeResult(
            RecipeId(RecipeMother.OMELETTE_ID)
        )
        return create_recipe

    @pytest.fixture
    def client(self, mock_create_recipe: MagicMock) -> Iterator[TestClient]:
        def provide_mock_create_recipe() -> MagicMock:
            return mock_create_recipe

        app.dependency_overrides[get_create_recipe] = provide_mock_create_recipe
        yield TestClient(app, raise_server_exceptions=False)
        app.dependency_overrides.clear()

    def test_answers_with_the_id_of_the_created_recipe_as_text(
        self, client: TestClient
    ) -> None:
        requested_recipe = CreateRecipeDTOMother.omelette()

        response = client.post(
            "/recipes/",
            json={
                "name": requested_recipe.name,
                "description": requested_recipe.description,
            },
        )

        assert response.status_code == 201
        assert response.json() == {"id": "00000000-0000-0000-0000-000000000001"}

    def test_creates_the_recipe_with_the_requested_name_and_description(
        self, client: TestClient, mock_create_recipe: MagicMock
    ) -> None:
        requested_recipe = CreateRecipeDTOMother.omelette()

        client.post(
            "/recipes/",
            json={
                "name": requested_recipe.name,
                "description": requested_recipe.description,
            },
        )

        mock_create_recipe.execute.assert_called_once_with(requested_recipe)

    def test_does_not_create_a_recipe_when_the_request_has_an_unknown_field(
        self, client: TestClient, mock_create_recipe: MagicMock
    ) -> None:
        response = client.post(
            "/recipes/",
            json={"name": "Omelette", "description": "Eggs", "calories": 300},
        )

        assert response.status_code == 422
        mock_create_recipe.execute.assert_not_called()

    def test_answers_with_a_server_error_when_the_recipe_cannot_be_created(
        self, client: TestClient, mock_create_recipe: MagicMock
    ) -> None:
        mock_create_recipe.execute.side_effect = RuntimeError

        response = client.post(
            "/recipes/", json={"name": "Omelette", "description": "Eggs"}
        )

        assert response.status_code == 500
