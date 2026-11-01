from typing import ClassVar

from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from my_cookbook.recipes.domain.exceptions import DuplicatedRecipe
from my_cookbook.recipes.domain.recipe import Recipe
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository
from my_cookbook.recipes.infrastructure.recipe_record import RecipeRecord


class PostgresRecipeRepository(RecipeRepository):
    _RECIPE_ID_UNIQUE_CONSTRAINT: ClassVar[str] = "recipes_recipe_id_key"

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, recipe: Recipe) -> None:
        try:
            with self._session.begin_nested():
                self._session.add(
                    RecipeRecord(
                        recipe_id=recipe.id.value,
                        name=recipe.name.value,
                        description=recipe.description,
                    )
                )
        except IntegrityError as error:
            if self._is_duplicated_recipe_id(error):
                raise DuplicatedRecipe() from error
            raise

    @classmethod
    def _is_duplicated_recipe_id(cls, error: IntegrityError) -> bool:
        return (
            isinstance(error.orig, UniqueViolation)
            and error.orig.diag.constraint_name == cls._RECIPE_ID_UNIQUE_CONSTRAINT
        )
