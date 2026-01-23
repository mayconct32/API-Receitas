from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import (
    get_auth_service,
    get_chef_service,
    get_current_chef,
)
from src.models.auth import Token
from src.models.chef import Chef, ResponseChef
from src.services.auth_service import AuthService
from src.services.chef_service import ChefService

ChefServiceDep = Annotated[ChefService, Depends(get_chef_service)]

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

CurrentChef = Annotated[dict, Depends(get_current_chef)]

AuthRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]

app = APIRouter(tags=["chefs"], prefix="/chefs")


@app.get("/me", status_code=HTTPStatus.OK, response_model=ResponseChef)
async def get_myself(current_chef: CurrentChef):
    return current_chef


@app.get("/", status_code=HTTPStatus.OK, response_model=List[ResponseChef])
async def get_chefs(offset: int, limit: int, chef_service: ChefServiceDep):
    return await chef_service.get_all_the_chefs(offset=offset, limit=limit)


@app.get(
    "/{chef_id}",
    status_code=HTTPStatus.OK,
    response_model=ResponseChef | None,
)
async def get_chef(chef_id: int, chef_service: ChefServiceDep):
    return await chef_service.get_chef(chef_id)


@app.post("/", status_code=HTTPStatus.CREATED, response_model=ResponseChef)
async def add_chef(chef: Chef, chef_service: ChefServiceDep):
    chef = await chef_service.add_chef(chef)
    return chef


@app.post("/auth", status_code=HTTPStatus.CREATED, response_model=Token)
async def auth_chef(form_data: AuthRequestForm, auth_service: AuthServiceDep):
    token = await auth_service.create_access_token(form_data)
    return {"access_token": token, "token_type": "bearer"}


@app.delete("/{chef_id}", status_code=HTTPStatus.OK)
async def delete_chef(
    chef_id: int, chef_service: ChefServiceDep, current_chef: CurrentChef
):
    response = await chef_service.delete_chef(chef_id, current_chef)
    return response


@app.put("/{chef_id}", status_code=HTTPStatus.OK, response_model=ResponseChef)
async def update_chef(
    updated_chef: Chef,
    chef_id: int,
    chef_service: ChefServiceDep,
    current_chef: CurrentChef,
):
    chef_updated = await chef_service.update_chef(
        updated_chef, chef_id, current_chef
    )
    return chef_updated
