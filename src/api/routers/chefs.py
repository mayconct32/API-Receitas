from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus
from typing import Annotated,List
from src.services.chef_service import ChefService,ChefSecurityService
from src.api.routers.dependencies import get_chef_service,get_chef_sec_service
from src.models.chef import Chef,ResponseChef
from src.models.auth import Token


ChefServiceDep = Annotated[
    ChefService,
    Depends(get_chef_service)
]

ChefSecServiceDep = Annotated[
    ChefSecurityService,
    Depends(get_chef_sec_service)
]

AuthRequestForm = Annotated[
    OAuth2PasswordRequestForm, 
    Depends()
]

app = APIRouter(tags=["chefs"],prefix="/chefs")

@app.get("/",status_code = HTTPStatus.OK,response_model = List[ResponseChef])
async def get_chefs(chef_service: ChefServiceDep):
    return await chef_service.get_all_the_chefs()

@app.post("/",status_code = HTTPStatus.CREATED,response_model = ResponseChef)
async def add_chefs(chef: Chef, chef_service: ChefServiceDep):
    chef = await chef_service.add_chef(chef)
    return chef

@app.post("/auth",status_code = HTTPStatus.CREATED,response_model=Token)
async def auth_chef(form_data: AuthRequestForm,chef_sec:ChefSecServiceDep):
    token = await chef_sec.create_access_token(form_data)
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.delete("/",status_code = HTTPStatus.OK)
def delete_chefs(chef_id: int, chef_service: ChefServiceDep):
    ...

@app.put("/",status_code = HTTPStatus.OK)
def update_chefs(chef: Chef, chef_id: int, chef_service: ChefServiceDep):
    ...

