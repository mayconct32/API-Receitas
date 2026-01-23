from fastapi import FastAPI

from src.api.routers.chefs import app as chefs

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "hello world!"}


app.include_router(chefs)

# uvicorn src.main:app --reload --host 0.0.0.0
