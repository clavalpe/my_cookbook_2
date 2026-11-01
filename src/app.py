from collections.abc import Callable, Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from my_cookbook.recipes.application.create_recipe import CreateRecipe, CreateRecipeDTO
from my_cookbook.recipes.domain.recipe_repository import RecipeRepository
from my_cookbook.recipes.infrastructure.create_recipe_request import (
    CreateRecipeRequest,
)
from my_cookbook.recipes.infrastructure.create_recipe_response import (
    CreateRecipeResponse,
)
from my_cookbook.recipes.infrastructure.postgres_recipe_repository import (
    PostgresRecipeRepository,
)
from my_cookbook.recipes.infrastructure.postgres_settings import PostgresSettings

app = FastAPI()


@lru_cache
def get_session_factory() -> Callable[[], Session]:
    engine = create_engine(PostgresSettings.from_environment().url)
    return sessionmaker(engine)


def get_session(
    session_factory: Annotated[Callable[[], Session], Depends(get_session_factory)],
) -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_recipe_repository(
    session: Annotated[Session, Depends(get_session, scope="function")],
) -> RecipeRepository:
    return PostgresRecipeRepository(session)


def get_create_recipe(
    recipe_repository: Annotated[RecipeRepository, Depends(get_recipe_repository)],
) -> CreateRecipe:
    return CreateRecipe(recipe_repository)


@app.get("/health/")
async def health() -> str:
    return "OK"


@app.post("/recipes/", status_code=201)
def create_recipe(
    requested_recipe: CreateRecipeRequest,
    create_recipe: Annotated[CreateRecipe, Depends(get_create_recipe)],
) -> CreateRecipeResponse:
    created_recipe = create_recipe.execute(
        CreateRecipeDTO(
            name=requested_recipe.name, description=requested_recipe.description
        )
    )
    return CreateRecipeResponse(id=str(created_recipe.id.value))
