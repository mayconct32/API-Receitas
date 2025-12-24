from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from http import HTTPStatus


app = APIRouter(tags=["users"],prefix="/users")

#schema
class User(BaseModel):
    username: str
    email: str

#fake db
users = []

@app.get("/",status_code = HTTPStatus.OK)
def get_users():
    return users

@app.post("/",status_code = HTTPStatus.CREATED)
def add_user(user:User):
    users.append(user)
    return {"message":"User added successfully."}

@app.delete("/",status_code = HTTPStatus.OK)
def delete_user(posiçao:int):
    if posiçao>len(users) - 1:
        raise HTTPException(
            detail = "usuario não encontrado!",
            status_code = HTTPStatus.NOT_FOUND
        )
    users.pop(posiçao)
    return {"message":"User deleted successfully."}

@app.put("/",status_code = HTTPStatus.OK)
def update_user(posiçao:int,user:User):
    if posiçao>len(users) - 1:
        raise HTTPException(
            detail = "usuario não encontrado!",
            status_code = HTTPStatus.NOT_FOUND
        )
    users[posiçao] = user
    return user 

