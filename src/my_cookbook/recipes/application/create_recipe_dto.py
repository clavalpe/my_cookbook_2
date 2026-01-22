from dataclasses import dataclass

@dataclass(frozen=True)
class CreateRecipeDTO:
    name: str
    description: str