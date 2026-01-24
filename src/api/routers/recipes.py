from fastapi import APIRouter
from src.models.recipe import Recipe,ResponseRecipe
from src.dependencies import CurrentChef
from datetime import datetime

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

@app.post("/",response_model = ResponseRecipe)
async def add_recipe(recipe: Recipe,current_chef: CurrentChef):
    return {
        **recipe.model_dump(),
        "recipe_id": 2,
        "chef_id": current_chef["chef_id"],
        "posted_at": datetime.now(),
        "updated_at": datetime.now()
    }

@app.delete("/{recipe_id}")
def delete_recipe():
    pass

@app.put("/{recipe_id}")
def update_recipe():
    pass