from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from http import HTTPStatus


app = APIRouter(tags=["users"],prefix="/users")

@app.get("/",status_code = HTTPStatus.OK)
def get_users():
    ...

@app.post("/",status_code = HTTPStatus.CREATED)
def add_user(user):
    ...

@app.delete("/",status_code = HTTPStatus.OK)
def delete_user(posiçao:int):
    ...

@app.put("/",status_code = HTTPStatus.OK)
def update_user(posiçao:int,user):
    ...

