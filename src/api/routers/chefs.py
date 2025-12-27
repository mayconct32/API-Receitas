from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from http import HTTPStatus


app = APIRouter(tags=["chefs"],prefix="/chefs")

@app.get("/",status_code = HTTPStatus.OK)
def get_chefs():
    ...

@app.post("/",status_code = HTTPStatus.CREATED)
def add_chefs(user):
    ...

@app.delete("/",status_code = HTTPStatus.OK)
def delete_chefs(posiçao:int):
    ...

@app.put("/",status_code = HTTPStatus.OK)
def update_chefs(posiçao:int,user):
    ...

