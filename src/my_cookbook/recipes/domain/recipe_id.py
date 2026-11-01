from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RecipeId:
    value: UUID
