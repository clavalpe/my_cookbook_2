from collections.abc import Iterator
from uuid import UUID

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

from my_cookbook.recipes.infrastructure.postgres_settings import PostgresSettings
from my_cookbook.recipes.tests.infrastructure.alembic_locations import ALEMBIC_INI


class TestRecipesTableMigration:
    RECIPES_COLUMNS: tuple[tuple[str, str, bool], ...] = (
        ("id", "INTEGER", False),
        ("recipe_id", "UUID", False),
        ("name", "TEXT", False),
        ("description", "TEXT", False),
    )

    @pytest.fixture
    def alembic_config(self) -> Config:
        return Config(str(ALEMBIC_INI))

    @pytest.fixture
    def engine(self) -> Iterator[Engine]:
        engine = create_engine(PostgresSettings.from_environment().url)
        yield engine
        engine.dispose()

    @pytest.fixture(autouse=True)
    def empty_database(self, alembic_config: Config) -> Iterator[None]:
        command.downgrade(alembic_config, "base")
        yield
        command.downgrade(alembic_config, "base")
        command.upgrade(alembic_config, "head")

    def test_creates_the_recipes_table_when_migrating_an_empty_database(
        self, alembic_config: Config, engine: Engine
    ) -> None:
        command.upgrade(alembic_config, "head")

        assert self.recipes_columns(engine) == self.RECIPES_COLUMNS

    def test_uses_the_serial_id_as_the_primary_key(
        self, alembic_config: Config, engine: Engine
    ) -> None:
        command.upgrade(alembic_config, "head")

        primary_key = inspect(engine).get_pk_constraint("recipes")

        assert primary_key["constrained_columns"] == ["id"]

    def test_generates_consecutive_ids_for_the_recipes_it_stores(
        self, alembic_config: Config, engine: Engine
    ) -> None:
        command.upgrade(alembic_config, "head")

        self.store_recipe(
            engine, UUID("00000000-0000-0000-0000-000000000001"), "Omelette"
        )
        self.store_recipe(
            engine, UUID("00000000-0000-0000-0000-000000000002"), "Gazpacho"
        )

        with engine.connect() as connection:
            ids = connection.execute(text("SELECT id FROM recipes ORDER BY id"))

            assert ids.scalars().all() == [1, 2]

    def test_rejects_two_recipes_with_the_same_recipe_id(
        self, alembic_config: Config, engine: Engine
    ) -> None:
        command.upgrade(alembic_config, "head")
        recipe_id = UUID("00000000-0000-0000-0000-000000000001")

        self.store_recipe(engine, recipe_id, "Omelette")

        with pytest.raises(IntegrityError):
            self.store_recipe(engine, recipe_id, "Gazpacho")

    def test_leaves_the_schema_unchanged_when_migrating_twice(
        self, alembic_config: Config, engine: Engine
    ) -> None:
        command.upgrade(alembic_config, "head")

        command.upgrade(alembic_config, "head")

        assert self.recipes_columns(engine) == self.RECIPES_COLUMNS

    def test_removes_the_recipes_table_when_downgrading_to_base(
        self, alembic_config: Config, engine: Engine
    ) -> None:
        command.upgrade(alembic_config, "head")

        command.downgrade(alembic_config, "base")

        assert "recipes" not in inspect(engine).get_table_names()

    @staticmethod
    def recipes_columns(engine: Engine) -> tuple[tuple[str, str, bool], ...]:
        return tuple(
            (column["name"], str(column["type"]), column["nullable"])
            for column in inspect(engine).get_columns("recipes")
        )

    @staticmethod
    def store_recipe(engine: Engine, recipe_id: UUID, name: str) -> None:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO recipes (recipe_id, name, description)"
                    " VALUES (:recipe_id, :name, :description)"
                ),
                {"recipe_id": recipe_id, "name": name, "description": "Description"},
            )
