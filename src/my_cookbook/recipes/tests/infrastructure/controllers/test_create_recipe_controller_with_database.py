from collections.abc import Iterator
from uuid import UUID

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text

from app import app
from my_cookbook.recipes.infrastructure.postgres_settings import PostgresSettings
from my_cookbook.recipes.tests.infrastructure.alembic_locations import ALEMBIC_INI


class TestCreateRecipeControllerWithDatabase:
    @pytest.fixture(scope="class", autouse=True)
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
