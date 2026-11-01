from dataclasses import dataclass
from typing import ClassVar

from my_cookbook.recipes.domain.exceptions import InvalidRecipeName


@dataclass(frozen=True)
class RecipeName:
    MINIMUM_LENGTH: ClassVar[int] = 5

    value: str

    def __post_init__(self) -> None:
        if len(self.value) < self.MINIMUM_LENGTH:
            raise InvalidRecipeName(self.MINIMUM_LENGTH)
