from my_cookbook.recipes.application.create_recipe import CreateRecipeDTO


class CreateRecipeDTOMother:
    @staticmethod
    def omelette() -> CreateRecipeDTO:
        return CreateRecipeDTO(name="Omelette", description="Omelette description")

    @staticmethod
    def named(name: str) -> CreateRecipeDTO:
        return CreateRecipeDTO(name=name, description="Omelette description")
