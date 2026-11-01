class InvalidRecipeName(Exception):
    def __init__(self, minimum_length: int) -> None:
        super().__init__(f"recipe name must have at least {minimum_length} characters")
