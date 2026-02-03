from fastapi import APIRouter
from src.models.recipe import CompleteRecipe
from src.dependencies import CurrentChef,RecipeServiceDep


app = APIRouter(tags=["recipes"],prefix="/recipes")


@app.get("/")
async def get_recipes(recipe_service: RecipeServiceDep, offset: int, limit: int):
    return await recipe_service.get_recipes(offset,limit)


app.get("/my_recipes")
async def get_my_recipes(recipe_service: RecipeServiceDep, current_chef: CurrentChef, offset: int, limit: int):
    return await recipe_service.get_my_recipes(current_chef["chef_id"], offset, limit)


@app.get("/{recipe_id}")
async def get_recipe(recipe_service: RecipeServiceDep, recipe_id: str):
    return await recipe_service.get_recipe(recipe_id)

@app.post("/")
async def add_recipe(
    recipe: CompleteRecipe,
    current_chef: CurrentChef,
    recipe_service: RecipeServiceDep
):
    db_recipe = await recipe_service.add_recipe(recipe, current_chef["chef_id"])
    return db_recipe


