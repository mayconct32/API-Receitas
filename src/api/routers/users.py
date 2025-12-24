from fastapi import APIRouter
from pydantic import BaseModel
from http import HTTPStatus


app = APIRouter(tags=["users"],prefix="/users")

#schema
class User(BaseModel):
    username: str
    email: str

#fake db
users = [
        {"username":"user1","email":"user1@example.com"},
        {"username":"user2","email":"user2@example.com"},
        {"username":"user3","email":"user3@example.com"}
    ]

@app.get("/",status_code = HTTPStatus.OK)
def get_users():
    return users

@app.post("/",status_code = HTTPStatus.CREATED)
def add_user(user:User):
    users.append(
        {
            "username":user.username,
            "email":user.email
        }
    )

    return {"message":"User added successfully."}

