from fastapi import FastAPI

from my_cookbook.recipes.infrastructure.controllers.create_recipe_controller import (
    router as create_recipe_router,
)

app = FastAPI()
app.include_router(create_recipe_router)


@app.get("/health/")
async def health() -> str:
    return "OK"
