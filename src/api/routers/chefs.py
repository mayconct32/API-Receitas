from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from http import HTTPStatus
from typing import Annotated,List
from src.services.chef_service import ChefService
from src.api.routers.dependencies import get_chef_service
from src.models.chef import Chef,ResponseChef


ChefServiceDep = Annotated[ChefService, Depends(get_chef_service)]

app = APIRouter(tags=["chefs"],prefix="/chefs")

@app.get("/",status_code = HTTPStatus.OK,response_model = List[ResponseChef])
async def get_chefs(chef_service: ChefServiceDep):
    return await chef_service.get_all_the_chefs()

@app.post("/",status_code = HTTPStatus.CREATED)
async def add_chefs(chef: Chef, chef_service: ChefServiceDep):
    chef = await chef_service.add_chef(chef)
    return chef

@app.delete("/",status_code = HTTPStatus.OK)
def delete_chefs(posiçao: int, chef_service: ChefServiceDep):
    ...

@app.put("/",status_code = HTTPStatus.OK)
def update_chefs(chef: Chef, posiçao: int, chef_service: ChefServiceDep):
    ...

