from fastapi import APIRouter


app = APIRouter(tags=["users"],prefix="/users")

@app.get("/")
def get_users():
    users = [
        {"username":"user1","email":"user1@example.com"},
        {"username":"user2","email":"user2@example.com"},
        {"username":"user3","email":"user3@example.com"}
    ]
    return users