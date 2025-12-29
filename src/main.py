from fastapi import FastAPI
from src.api.routers.chefs import app as chefs


app = FastAPI()

@app.get("/")
def hello_world():
    return {"message":"hello world!"}

app.include_router(chefs)

if __name__ == "__main__":
    import uvicorn 

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)