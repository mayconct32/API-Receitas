from fastapi import APIRouter
from src.models.recipe import CompleteRecipe
from src.dependencies import CurrentChef,RecipeServiceDep


app = APIRouter(tags=["recipes"],prefix="/recipes")


@app.get("/")
async def get_recipes(recipe_service: RecipeServiceDep,offset: int, limit: int):
    return await recipe_service.get_recipes(offset,limit)

