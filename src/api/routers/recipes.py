from fastapi import APIRouter
from src.models.recipe import CompleteRecipe
from src.dependencies import CurrentChef,RecipeServiceDep


app = APIRouter(tags=["recipes"],prefix="/recipes")


@app.get("/")
async def get_recipes(recipe_service: RecipeServiceDep, offset: int, limit: int):
    return await recipe_service.get_recipes(offset,limit)

@app.get("/{recipe_id}")
async def get_recipe(recipe_service: RecipeServiceDep, recipe_id: str):
    return await recipe_service.get_recipe(recipe_id)