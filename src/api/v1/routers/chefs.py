from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Request, HTTPException

from src.dependencies import (
    AuthRequestForm,
    AuthServiceDep,
    ChefServiceDep,
    CurrentChef,
)
from src.models.auth import Token
from src.models.chef import Chef, ResponseChef
from src.rate_limiter import limiter
from src.exceptions.chef_exceptions import *


app = APIRouter(tags=["chefs"], prefix="/v1/chefs")


@app.get("/me", status_code=HTTPStatus.OK,response_model=ResponseChef)
@limiter.limit("5/minute")
async def get_myself(request: Request, current_chef: CurrentChef):
    return current_chef


@app.get("/", status_code=HTTPStatus.OK, response_model=List[ResponseChef])
@limiter.limit("5/minute")
async def get_chefs(
    request: Request, offset: int, limit: int, chef_service: ChefServiceDep
):
    try:
        return await chef_service.get_all_the_chefs(
            offset=offset, 
            limit=limit
        )
    except ChefErrorNotFound as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e)
        )


@app.get(
    "/{chef_id}",
    status_code=HTTPStatus.OK,
    response_model=ResponseChef | None,
)
@limiter.limit("5/minute")
async def get_chef(
    request: Request, chef_id: str, chef_service: ChefServiceDep
):
    try:
        return await chef_service.get_chef(chef_id)
    except ChefErrorNotFound as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=str(e)
        )


@app.post("/", status_code=HTTPStatus.CREATED, response_model=ResponseChef)
@limiter.limit("3/minute")
async def add_chef(
    request: Request, chef: Chef, chef_service: ChefServiceDep
):
    try:
        return await chef_service.add_chef(chef)
    except ConflictingNameError as e:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=str(e)
        )
    except ConflictingEmailError as e:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=str(e)
        )


@app.post("/auth", status_code=HTTPStatus.CREATED, response_model=Token)
@limiter.limit("3/minute")
async def auth_chef(
    request: Request, form_data: AuthRequestForm, auth_service: AuthServiceDep
):
    try:
        token = await auth_service.create_access_token(form_data)
        return {"access_token": token, "token_type": "bearer"}
    except CredentialsError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.delete("/{chef_id}", status_code=HTTPStatus.OK)
@limiter.limit("3/minute")
async def delete_chef(
    request: Request,
    chef_id: str,
    chef_service: ChefServiceDep,
    current_chef: CurrentChef,
):
    try:
        return await chef_service.delete_chef(chef_id, current_chef)
    except AuthorizationError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(e)
        )


@app.put("/{chef_id}", status_code=HTTPStatus.OK, response_model=ResponseChef)
@limiter.limit("3/minute")
async def update_chef(
    request: Request,
    updated_chef: Chef,
    chef_id: str,
    chef_service: ChefServiceDep,
    current_chef: CurrentChef,
):
    try:
        return await chef_service.update_chef(
            updated_chef, chef_id, current_chef
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(e)
        )
    except ConflictingNameError as e:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=str(e)
        )
    except ConflictingEmailError as e:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=str(e)
        )
