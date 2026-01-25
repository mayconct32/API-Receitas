from fastapi import APIRouter
from src.models.recipe import CompleteRecipe
from src.dependencies import CurrentChef,RecipeServiceDep


app = APIRouter(tags=["recipes"],prefix="/recipes")


@app.get("/")
def get_recipes():
    pass


@app.get("/my_recipes")
def get_my_recipes():
    pass


@app.get("/{recipe_id}")
def get_recipe():
    pass


@app.post("/")
async def add_recipe(
    recipe: CompleteRecipe,
    current_chef: CurrentChef,
    recipe_service: RecipeServiceDep
):
    await recipe_service.add_recipe(recipe,current_chef["chef_id"])
    return "ok"


@app.delete("/{recipe_id}")
def delete_recipe():
    pass


@app.put("/{recipe_id}")
def update_recipe():
    pass