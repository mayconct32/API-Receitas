from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from http import HTTPStatus
from typing import Annotated
from src.services.chef_service import ChefService
from src.api.routers.dependencies import get_chef_service


ChefServiceDep = Annotated[ChefService, Depends(get_chef_service)]

app = APIRouter(tags=["chefs"],prefix="/chefs")

@app.get("/",status_code = HTTPStatus.OK)
async def get_chefs(chef_service: ChefServiceDep):
    return await chef_service.get_all_the_chefs()

@app.post("/",status_code = HTTPStatus.CREATED)
def add_chefs(user,chef_service: ChefServiceDep):
    ...

@app.delete("/",status_code = HTTPStatus.OK)
def delete_chefs(posiçao:int,chef_service: ChefServiceDep):
    ...

@app.put("/",status_code = HTTPStatus.OK)
def update_chefs(posiçao:int,chef_service: ChefServiceDep):
    ...

