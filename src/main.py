from fastapi import FastAPI, Request

from src.api.v1.routers.chefs import app as chefs
from src.api.v1.routers.recipes import app as recipes
from src.rate_limiter import limiter

app = FastAPI()


@app.get("/")
@limiter.limit("6/minute")
def hello_world(request: Request):
    return {"message": "hello world!"}


app.include_router(chefs)
app.include_router(recipes)

# uvicorn src.main:app --reload --host 0.0.0.0
