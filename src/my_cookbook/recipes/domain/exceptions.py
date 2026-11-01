class InvalidRecipeName(Exception):
    def __init__(self) -> None:
        super().__init__("recipe name must have at least 5 characters")
