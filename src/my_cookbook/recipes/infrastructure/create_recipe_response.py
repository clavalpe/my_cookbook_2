from pydantic import BaseModel


class CreateRecipeResponse(BaseModel):
    id: str
