from fastapi import FastAPI
import uvicorn 
from api.routers.users import app as users



app = FastAPI()

@app.get("/")
def hello_world():
    return {"message":"hello world!"}

app.include_router(users)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)