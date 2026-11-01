from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from my_cookbook.recipes.application.create_recipe import CreateRecipe, CreateRecipeDTO
from my_cookbook.recipes.infrastructure.dependencies import get_create_recipe

router = APIRouter()


class CreateRecipeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str


class CreateRecipeResponse(BaseModel):
    id: str


@router.post("/recipes/", status_code=201)
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
