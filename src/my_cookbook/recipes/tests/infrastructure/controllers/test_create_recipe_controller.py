from collections.abc import Iterator
from unittest.mock import MagicMock, create_autospec
from uuid import UUID

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text

from app import app
from my_cookbook.recipes.application.create_recipe import CreateRecipe
from my_cookbook.recipes.domain.exceptions import DuplicatedRecipe, InvalidRecipeName
from my_cookbook.recipes.infrastructure.dependencies import get_create_recipe
from my_cookbook.recipes.infrastructure.postgres_settings import PostgresSettings
from my_cookbook.recipes.tests.infrastructure.alembic_locations import ALEMBIC_INI


class TestCreateRecipeController:
    @pytest.fixture
    def migrated_database(self) -> None:
        command.upgrade(Config(str(ALEMBIC_INI)), "head")

    @pytest.fixture
    def engine(self) -> Iterator[Engine]:
        engine = create_engine(PostgresSettings.from_environment().url)
        yield engine
        engine.dispose()

    @pytest.fixture
    def created_recipe_ids(self, engine: Engine) -> Iterator[list[UUID]]:
        created_recipe_ids: list[UUID] = []
        yield created_recipe_ids
        with engine.begin() as connection:
            for recipe_id in created_recipe_ids:
                connection.execute(
                    text("delete from recipes where recipe_id = :recipe_id"),
                    {"recipe_id": recipe_id},
                )

    @pytest.fixture
    def mock_create_recipe(self) -> MagicMock:
        create_recipe: MagicMock = create_autospec(
            CreateRecipe, spec_set=True, instance=True
        )
        return create_recipe

    @pytest.fixture
    def client_with_mock_create_recipe(
        self, mock_create_recipe: MagicMock
    ) -> Iterator[TestClient]:
        def provide_mock_create_recipe() -> MagicMock:
            return mock_create_recipe

        app.dependency_overrides[get_create_recipe] = provide_mock_create_recipe
        yield TestClient(app, raise_server_exceptions=False)
        app.dependency_overrides.clear()

    @pytest.mark.usefixtures("migrated_database")
    def test_stores_the_requested_recipe_and_answers_with_its_id(
        self, engine: Engine, created_recipe_ids: list[UUID]
    ) -> None:
        response = TestClient(app).post(
            "/recipes/", json={"name": "Omelette", "description": "Eggs"}
        )

        created_recipe_id = UUID(response.json()["id"])
        created_recipe_ids.append(created_recipe_id)
        assert response.status_code == 201
        with engine.connect() as connection:
            stored_recipes = connection.execute(
                text(
                    "select recipe_id, name, description from recipes"
                    " where recipe_id = :recipe_id"
                ),
                {"recipe_id": created_recipe_id},
            ).all()
        assert [tuple(stored_recipe) for stored_recipe in stored_recipes] == [
            (created_recipe_id, "Omelette", "Eggs")
        ]

    def test_answers_with_the_reason_when_the_recipe_name_is_too_short(
        self,
        client_with_mock_create_recipe: TestClient,
        mock_create_recipe: MagicMock,
    ) -> None:
        mock_create_recipe.execute.side_effect = InvalidRecipeName(5)

        response = client_with_mock_create_recipe.post(
            "/recipes/", json={"name": "Ome", "description": "Eggs"}
        )

        assert response.status_code == 400
        assert response.json() == {
            "code": "INVALID_RECIPE_NAME",
            "detail": "recipe name must have at least 5 characters",
        }

    def test_does_not_create_a_recipe_when_the_request_has_no_name(
        self,
        client_with_mock_create_recipe: TestClient,
        mock_create_recipe: MagicMock,
    ) -> None:
        response = client_with_mock_create_recipe.post(
            "/recipes/", json={"description": "Eggs"}
        )

        assert response.status_code == 400
        assert response.json() == {
            "code": "INVALID_REQUEST",
            "detail": "body.name: Field required",
        }
        mock_create_recipe.execute.assert_not_called()

    def test_does_not_create_a_recipe_when_the_request_is_not_valid_json(
        self,
        client_with_mock_create_recipe: TestClient,
        mock_create_recipe: MagicMock,
    ) -> None:
        response = client_with_mock_create_recipe.post(
            "/recipes/",
            content='{"name": "Omelette",',
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 400
        assert response.json() == {
            "code": "INVALID_REQUEST",
            "detail": "body.20: JSON decode error",
        }
        mock_create_recipe.execute.assert_not_called()

    def test_does_not_create_a_recipe_when_the_request_is_not_readable_text(
        self,
        client_with_mock_create_recipe: TestClient,
        mock_create_recipe: MagicMock,
    ) -> None:
        response = client_with_mock_create_recipe.post(
            "/recipes/",
            content=b"\xff",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 400
        assert response.json() == {
            "code": "INVALID_REQUEST",
            "detail": "There was an error parsing the body",
        }
        mock_create_recipe.execute.assert_not_called()

    def test_does_not_create_a_recipe_when_the_request_has_an_unknown_field(
        self,
        client_with_mock_create_recipe: TestClient,
        mock_create_recipe: MagicMock,
    ) -> None:
        response = client_with_mock_create_recipe.post(
            "/recipes/",
            json={"name": "Omelette", "description": "Eggs", "calories": 300},
        )

        assert response.status_code == 400
        assert response.json() == {
            "code": "INVALID_REQUEST",
            "detail": "body.calories: Extra inputs are not permitted",
        }
        mock_create_recipe.execute.assert_not_called()

    def test_answers_with_a_server_error_when_the_recipe_cannot_be_created(
        self,
        client_with_mock_create_recipe: TestClient,
        mock_create_recipe: MagicMock,
    ) -> None:
        mock_create_recipe.execute.side_effect = RuntimeError

        response = client_with_mock_create_recipe.post(
            "/recipes/", json={"name": "Omelette", "description": "Eggs"}
        )

        assert response.status_code == 500
        assert response.text == "Internal Server Error"

    def test_answers_with_a_server_error_when_the_failure_has_no_error_code(
        self,
        client_with_mock_create_recipe: TestClient,
        mock_create_recipe: MagicMock,
    ) -> None:
        mock_create_recipe.execute.side_effect = DuplicatedRecipe()

        response = client_with_mock_create_recipe.post(
            "/recipes/", json={"name": "Omelette", "description": "Eggs"}
        )

        assert response.status_code == 500
        assert response.text == "Internal Server Error"
