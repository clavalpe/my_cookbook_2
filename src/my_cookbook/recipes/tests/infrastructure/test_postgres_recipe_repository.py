from collections.abc import Iterator
from uuid import UUID

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from my_cookbook.recipes.domain.exceptions import DuplicatedRecipe
from my_cookbook.recipes.infrastructure.postgres_recipe_repository import (
    PostgresRecipeRepository,
)
from my_cookbook.recipes.infrastructure.postgres_settings import PostgresSettings
from my_cookbook.recipes.tests.infrastructure.alembic_locations import ALEMBIC_INI
from my_cookbook.recipes.tests.mothers.recipe_mother import RecipeMother


class TestPostgresRecipeRepository:
    @pytest.fixture(scope="class", autouse=True)
    def migrated_database(self) -> None:
        command.upgrade(Config(str(ALEMBIC_INI)), "head")

    @pytest.fixture
    def session(self) -> Iterator[Session]:
        engine = create_engine(PostgresSettings.from_environment().url)
        connection = engine.connect()
        outer_transaction = connection.begin()
        session = Session(connection, join_transaction_mode="create_savepoint")
        yield session
        session.close()
        outer_transaction.rollback()
        connection.close()
        engine.dispose()

    @pytest.fixture
    def recipe_repository(self, session: Session) -> PostgresRecipeRepository:
        return PostgresRecipeRepository(session)

    def test_stores_the_recipe_with_its_id_name_and_description(
        self, session: Session, recipe_repository: PostgresRecipeRepository
    ) -> None:
        recipe_repository.save(RecipeMother.omelette())

        assert self.stored_recipes(session) == [
            (RecipeMother.OMELETTE_ID, "Omelette", "Omelette description")
        ]

    def test_stores_two_recipes_with_the_same_name_and_different_ids(
        self, session: Session, recipe_repository: PostgresRecipeRepository
    ) -> None:
        recipe_repository.save(RecipeMother.omelette())
        recipe_repository.save(RecipeMother.another_omelette())

        assert self.stored_recipes(session) == [
            (RecipeMother.OMELETTE_ID, "Omelette", "Omelette description"),
            (RecipeMother.ANOTHER_OMELETTE_ID, "Omelette", "Omelette description"),
        ]

    def test_does_not_keep_the_recipe_when_the_work_in_progress_is_abandoned(
        self, session: Session, recipe_repository: PostgresRecipeRepository
    ) -> None:
        recipe_repository.save(RecipeMother.omelette())

        session.rollback()

        assert self.stored_recipes(session) == []

    def test_does_not_allow_to_save_two_recipes_with_the_same_id(
        self, recipe_repository: PostgresRecipeRepository
    ) -> None:
        recipe_repository.save(RecipeMother.omelette())

        with pytest.raises(DuplicatedRecipe) as error:
            recipe_repository.save(RecipeMother.gazpacho_with_the_id_of_the_omelette())

        assert str(error.value) == "a recipe with this id already exists"

    def test_keeps_the_original_recipe_and_stays_usable_after_a_duplicated_recipe(
        self, session: Session, recipe_repository: PostgresRecipeRepository
    ) -> None:
        recipe_repository.save(RecipeMother.omelette())

        with pytest.raises(DuplicatedRecipe):
            recipe_repository.save(RecipeMother.gazpacho_with_the_id_of_the_omelette())
        recipe_repository.save(RecipeMother.another_omelette())

        assert self.stored_recipes(session) == [
            (RecipeMother.OMELETTE_ID, "Omelette", "Omelette description"),
            (RecipeMother.ANOTHER_OMELETTE_ID, "Omelette", "Omelette description"),
        ]

    def test_does_not_hide_a_failure_that_is_not_a_duplicated_recipe(
        self, recipe_repository: PostgresRecipeRepository
    ) -> None:
        with pytest.raises(IntegrityError):
            recipe_repository.save(RecipeMother.omelette_without_description())

    def test_does_not_report_a_duplicated_recipe_when_the_ids_differ(
        self, session: Session, recipe_repository: PostgresRecipeRepository
    ) -> None:
        recipe_repository.save(RecipeMother.omelette())
        self.make_next_row_number_collide_with_the_stored_recipe(session)

        with pytest.raises(IntegrityError):
            recipe_repository.save(RecipeMother.another_omelette())

    @staticmethod
    def make_next_row_number_collide_with_the_stored_recipe(session: Session) -> None:
        session.execute(
            text(
                "SELECT setval(pg_get_serial_sequence('recipes', 'id'),"
                " (SELECT max(id) FROM recipes), false)"
            )
        )

    @staticmethod
    def stored_recipes(session: Session) -> list[tuple[UUID, str, str]]:
        rows = session.execute(
            text("SELECT recipe_id, name, description FROM recipes ORDER BY id")
        )
        return [(row.recipe_id, row.name, row.description) for row in rows]
