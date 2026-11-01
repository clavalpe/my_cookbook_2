from pydantic import BaseModel

from my_cookbook.recipes.infrastructure.recipe_error_code import RecipeErrorCode


class ErrorResponse(BaseModel):
    code: RecipeErrorCode
    detail: str
