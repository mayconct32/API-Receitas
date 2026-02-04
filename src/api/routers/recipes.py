from fastapi import APIRouter
from src.models.recipe import Recipe,ResponseRecipe
from src.dependencies import CurrentChef,RecipeServiceDep
from typing import List

app = APIRouter(tags=["recipes"],prefix="/recipes")


@app.get("/",response_model=List[ResponseRecipe])
async def get_recipes(recipe_service: RecipeServiceDep, offset: int, limit: int):
    return await recipe_service.get_recipes(offset,limit)


@app.get("/my_recipes",response_model=List[ResponseRecipe])
async def get_my_recipes(recipe_service: RecipeServiceDep, current_chef: CurrentChef, offset: int, limit: int):
    return await recipe_service.get_my_recipes(
        current_chef["chef_id"], 
        offset, 
        limit
    )


@app.get("/{recipe_id}",response_model=ResponseRecipe)
async def get_recipe(recipe_service: RecipeServiceDep, recipe_id: str):
    return await recipe_service.get_recipe(recipe_id)


@app.post("/",response_model=ResponseRecipe)
async def add_recipe(
    recipe: Recipe,
    current_chef: CurrentChef,
    recipe_service: RecipeServiceDep
):
    return await recipe_service.add_recipe(
        recipe, 
        current_chef["chef_id"]
    )


@app.delete("/{recipe_id}")
async def delete_recipe(
    recipe_service: RecipeServiceDep, 
    current_chef: CurrentChef, 
    recipe_id: str
):
    return await recipe_service.delete_recipe(
        current_chef["chef_id"], 
        recipe_id
    )


@app.put("/{recipe_id}")
async def update_recipe(
    recipe_service: RecipeServiceDep, 
    current_chef: CurrentChef, 
    recipe_id: str, 
    recipe: Recipe
):
    return await recipe_service.update_recipe(
        current_chef["chef_id"], 
        recipe_id, 
        recipe
    )


    
