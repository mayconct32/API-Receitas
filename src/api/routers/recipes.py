from fastapi import APIRouter


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
def add_recipe():
    pass

@app.delete("/{recipe_id}")
def delete_recipe():
    pass

@app.put("/{recipe_id}")
def update_recipe():
    pass