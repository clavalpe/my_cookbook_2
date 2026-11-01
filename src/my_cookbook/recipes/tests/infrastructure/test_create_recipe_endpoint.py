from collections.abc import Iterator
from typing import Annotated
from unittest.mock import MagicMock, create_autospec

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import app, get_recipe_repository, get_session, get_session_factory
from my_cookbook.recipes.domain.recipe_name import RecipeName
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository
from my_cookbook.recipes.tests.infrastructure.fake_recipe_repository import (
    FakeRecipeRepository,
)


class TestCreateRecipeEndpoint:
    @pytest.fixture
    def fake_recipe_repository(self) -> FakeRecipeRepository:
        return FakeRecipeRepository()

    @pytest.fixture
    def mock_session(self) -> MagicMock:
        mock_session: MagicMock = create_autospec(Session, spec_set=True, instance=True)
        return mock_session

    @pytest.fixture
    def client(
        self, fake_recipe_repository: FakeRecipeRepository, mock_session: MagicMock
    ) -> Iterator[TestClient]:
        def provide_mock_session_factory() -> MagicMock:
            return MagicMock(return_value=mock_session)

        def provide_fake_recipe_repository(
            session: Annotated[Session, Depends(get_session, scope="function")],
        ) -> RecipeRepository:
            return fake_recipe_repository

        app.dependency_overrides[get_session_factory] = provide_mock_session_factory
        app.dependency_overrides[get_recipe_repository] = provide_fake_recipe_repository
        yield TestClient(app, raise_server_exceptions=False)
        app.dependency_overrides.clear()

    def test_creates_the_requested_recipe_and_answers_with_its_id(
        self, client: TestClient, fake_recipe_repository: FakeRecipeRepository
    ) -> None:
        response = client.post(
            "/recipes/", json={"name": "Omelette", "description": "Eggs"}
        )

        assert response.status_code == 201
        [saved_recipe] = fake_recipe_repository.saved_recipes
        assert response.json() == {"id": str(saved_recipe.id.value)}
        assert saved_recipe.name == RecipeName("Omelette")
        assert saved_recipe.description == "Eggs"

    def test_creates_two_different_recipes_when_the_same_recipe_is_requested_twice(
        self, client: TestClient, fake_recipe_repository: FakeRecipeRepository
    ) -> None:
        first_response = client.post(
            "/recipes/", json={"name": "Omelette", "description": "Eggs"}
        )
        second_response = client.post(
            "/recipes/", json={"name": "Omelette", "description": "Eggs"}
        )

        assert first_response.json()["id"] != second_response.json()["id"]
        assert [
            str(recipe.id.value) for recipe in fake_recipe_repository.saved_recipes
        ] == [first_response.json()["id"], second_response.json()["id"]]

    def test_keeps_the_created_recipe_once_the_request_succeeds(
        self, client: TestClient, mock_session: MagicMock
    ) -> None:
        response = client.post(
            "/recipes/", json={"name": "Omelette", "description": "Eggs"}
        )

        assert response.status_code == 201
        mock_session.commit.assert_called_once_with()
        mock_session.rollback.assert_not_called()
        mock_session.close.assert_called_once_with()

    def test_abandons_the_work_of_a_request_that_fails(
        self, client: TestClient, mock_session: MagicMock
    ) -> None:
        response = client.post(
            "/recipes/", json={"name": "Soup", "description": "Water"}
        )

        assert response.status_code == 500
        mock_session.rollback.assert_called_once_with()
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once_with()

    def test_does_not_create_a_recipe_when_the_request_has_an_unknown_field(
        self, client: TestClient, fake_recipe_repository: FakeRecipeRepository
    ) -> None:
        response = client.post(
            "/recipes/",
            json={"name": "Omelette", "description": "Eggs", "calories": 300},
        )

        assert response.status_code == 422
        assert fake_recipe_repository.saved_recipes == []
