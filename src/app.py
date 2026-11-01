from fastapi import FastAPI

from my_cookbook.recipes.infrastructure.controllers.create_recipe_controller import (
    router as create_recipe_router,
)
from my_cookbook.recipes.infrastructure.exception_handlers import (
    register_exception_handlers,
)

app = FastAPI()
app.include_router(create_recipe_router)
register_exception_handlers(app)


@app.get("/health/")
async def health() -> str:
    return "OK"
