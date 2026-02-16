import time

from fastapi import FastAPI, Request

from src.api.v1.routers.chefs import app as chefs
from src.api.v1.routers.recipes import app as recipes
from src.rate_limiter import limiter

app = FastAPI()


@app.get("/")
@limiter.limit("6/minute")
def hello_world(request: Request):
    return {"message": "hello world!"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(chefs)
app.include_router(recipes)

# uvicorn src.main:app --reload --host 0.0.0.0
