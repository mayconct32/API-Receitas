from fastapi import FastAPI

from src.api.routers.chefs import app as chefs
from src.api.routers.recipes import app as recipes

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "hello world!"}


app.include_router(chefs)
app.include_router(recipes)

# uvicorn src.main:app --reload --host 0.0.0.0
