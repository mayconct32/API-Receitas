from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from src.database import MysqlDBConnection
from src.interfaces.connection_db import ISqlDBConnection
from src.interfaces.repository import IRepository
from src.repositories.chef_repository import ChefRepository
from src.services.auth_service import AuthService
from src.services.chef_service import ChefService


def get_db_connection() -> ISqlDBConnection:
    return MysqlDBConnection()


def get_repository(
    connection: ISqlDBConnection = Depends(get_db_connection),
) -> IRepository:
    return ChefRepository(connection)


def get_chef_service(
    repository: IRepository = Depends(get_repository),
) -> ChefService:
    return ChefService(repository)


def get_auth_service(
    repository: IRepository = Depends(get_repository),
) -> AuthService:
    return AuthService(repository)


async def get_current_chef(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="chefs/auth")),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict:
    return await auth_service.decode_token(token)


ChefServiceDep = Annotated[ChefService, Depends(get_chef_service)]

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

CurrentChef = Annotated[dict, Depends(get_current_chef)]

AuthRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]
