from pydantic import BaseModel, ConfigDict


class CreateRecipeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
