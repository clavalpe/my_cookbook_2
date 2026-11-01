class InvalidRecipeName(Exception):
    def __init__(self, minimum_length: int) -> None:
        super().__init__(f"recipe name must have at least {minimum_length} characters")


class DuplicatedRecipe(Exception):
    def __init__(self) -> None:
        super().__init__("a recipe with this id already exists")
