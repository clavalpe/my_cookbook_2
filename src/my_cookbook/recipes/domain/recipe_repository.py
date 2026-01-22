from abc import ABC, abstractmethod
from my_cookbook.recipes.domain.recipe import Recipe


class RecipeRepository(ABC):
    @abstractmethod
    def save(self, recipe: Recipe) -> None:
        ...